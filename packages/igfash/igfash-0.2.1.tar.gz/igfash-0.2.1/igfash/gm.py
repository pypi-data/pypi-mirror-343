import numpy as np
from scipy.stats import t, norm
from scipy.optimize import root_scalar
from timeit import default_timer as timer
from pathlib import Path
import importlib
import os
import shutil
import logging
logger = logging.getLogger(__name__)

from openquake.hazardlib.geo import Point #This class represents a geographical point in terms of longitude, latitude, and depth (with respect to the Earth surface).
from openquake.hazardlib.geo.surface.planar import PlanarSurface
from openquake.hazardlib.source.characteristic import CharacteristicFaultSource
from openquake.hazardlib.mfd import ArbitraryMFD
from openquake.hazardlib.tom import PoissonTOM
from openquake.hazardlib.scalerel import WC1994 #Wells and Coppersmith magnitude – rupture area relationships
from openquake.hazardlib.site import Site, SiteCollection
from openquake.hazardlib.contexts import ContextMaker
from openquake.hazardlib.valid import gsim
from openquake.hazardlib.imt import PGA


def export_GSIM_to_openquake(source_dir=None):
    target_dir = importlib.resources.files('openquake') / 'hazardlib/gsim'
    
    if source_dir == None:
        source_dir = importlib.resources.files('igfash') / 'gsim'
    else:
        source_dir = Path(source_dir)

    if source_dir.is_dir() and target_dir.is_dir():
        for file in [item for item in source_dir.iterdir() if item.is_file()]: #skip directories and copy only files
            if not os.path.exists(target_dir / file.name):
                shutil.copy2(file, target_dir)
                logger.info(f"Copied {file.name} to the openquake gsim directory")
            else:
                logger.info(f"{file.name} already exists in the openquake gsim folder {target_dir}")


def compute_IMT_exceedance(rx_lat, rx_lon, r, fr, p, lambdas, D, percentages_D, magnitudes, magnitude_pdf, magnitude_cdf, model, imt='PGA', IMT_min=0.01, IMT_max=2.0, rx_label=None, rtol=0.1, use_cython=False, **kwargs):
    
    n_events = len(r)
        
    try:
        gmpes = [gsim(model)]
    except:
        msg = f"{model} was not found in the openquake gsim directory" 
        logger.error(msg)
        raise Exception(msg) 
    
    if model == 'Lasocki2013': #this model requires the number of earthquake records
    
        if imt=='PGA': #extract number of records for PGA
            num_ground_motion_records = gmpes[0].COEFFS.non_sa_coeffs[PGA()]['N']
        else: #extract number of records for SA()
            freq = float(imt[imt.find('(')+1:imt.find(')')]) # get the desired frequency of SA
            first_index = np.where(gmpes[0].COEFFS.get_coeffs('N')[0]==freq)[0][0]
            num_ground_motion_records = gmpes[0].COEFFS.get_coeffs('N')[1][first_index][0]
    else:
        num_ground_motion_records = 0
                               
    #placeholder values that do not have any effect
    Mag = 5.0 #placeholder mag, must be valid for that context; will be overwritten in loop
    rupture_aratio = 1.5
    Strike = 0
    Dip = 90
    Rake = 0
    
    Hypocenter = Point(rx_lon, rx_lat, 0.0) #does not matter in our case; just set eq location to be same as receiver
    #according to the magnitude and MSR calculate planar surface
    planar_surface = PlanarSurface.from_hypocenter(
            hypoc=Hypocenter,
            msr=WC1994(),
            mag=Mag,
            aratio=rupture_aratio,
            strike=Strike,
            dip=Dip,
            rake=Rake,
            )

    # site for which we compute (receiver location)    
    site_collection = SiteCollection([Site(location=Point(rx_lon, rx_lat, 0))])

    imtls = {s: [0] for s in [imt]} #required for context maker, M = 2 IMTs

    context_maker = ContextMaker('Induced', gmpes, {'imtls': imtls, 'mags': [Mag]}) #necessary contexts builder

    src = CharacteristicFaultSource(source_id = 1,
                                    name = 'rup',
                                    tectonic_region_type = 'Induced',
                                    mfd = ArbitraryMFD([Mag], [0.01]), #this does not have any effect
                                    temporal_occurrence_model = PoissonTOM(50.), #this is also not really used
                                    surface = planar_surface,
                                    rake = Rake)

    ctx = context_maker.from_srcs([src], site_collection)[0] #returns one context from the source for one rupture   

    if use_cython:

        from cython_exceedance import exceedance_core
    
        def exceedance_root_function(a):
            return exceedance_core(a, r, fr, lambdas, D, percentages_D, magnitudes,
                                   magnitude_pdf, magnitude_cdf, context_maker, ctx,
                                   model, num_ground_motion_records) - p

    else:
    
        def exceedance_root_function(a):
            exceedance_prob_sum = 0
            log_a = np.log(a) # Precompute log(a)
        
            for j in range(len(lambdas)): #loop through all lambdas
                lambda_j = lambdas[j]
                D_j_val = percentages_D[j] * D # Use a different name to avoid shadowing D
                lambda_D_j = lambda_j * D_j_val
                denom_j = (1 - np.exp(-lambda_D_j))
                if denom_j == 0: # Avoid division by zero if lambda_D_j is very small or zero
                   continue
        
                for i in range(n_events): #loop through all events
                    ri = r[i] # Epicentral distance
                    fr_i = fr[i] # Location probability f(r)
                    ctx.repi = ri
        
                    # Precompute terms only dependent on lambda_j, D_j, m
                    lambda_D_j_f_m = lambda_D_j * magnitude_pdf
                    exp_term_m = np.exp(-lambda_D_j * (1 - magnitude_cdf))
                    f_conditional_base_m = (lambda_D_j_f_m * exp_term_m) / denom_j
        
                    for k in range(len(magnitudes)):  #loop through all values of magnitude pdf and cdf
                        m = magnitudes[k]
                        ctx.mag = m # update context magnitude 
        
                        # Calculate f_conditional (simpler now)
                        f_conditional = f_conditional_base_m[k]
        
                        mean, sig, _, _ = context_maker.get_mean_stds(ctx)
                        log_gm_predicted = mean[0][0][0]
                        variance_term = sig[0][0][0]
                        residual = log_a - log_gm_predicted # Use precomputed log_a
        
                        if residual <= 0:
                             exceedance_probability = 1.0
                        else:
                             # Avoid division by zero or very small numbers if variance_term is ~0
                             if variance_term < 1e-15: # Adjust threshold as needed
                                 exceedance_probability = 0.0
                             else:
                                t_value = residual / variance_term
                                
                                if model == 'Lasocki2013':
                                    exceedance_probability = t.sf(t_value, num_ground_motion_records - 3) # student t distribution, degrees of freedom: n-3; sf = 1 - cdf
                                else:
                                    exceedance_probability = norm.sf(t_value) # equivalent to 1.0 - norm.cdf(t_value)
        
                        location_exceedance_prob = exceedance_probability * f_conditional * fr_i
                        exceedance_prob_sum += location_exceedance_prob
        
            return exceedance_prob_sum - p
    
      
    
    # Check function values at different test points
    IMT_mid = (IMT_max-IMT_min)/2
    lower_bound_value = exceedance_root_function(IMT_min)
    mid_point_value = exceedance_root_function(IMT_mid)
    upper_bound_value = exceedance_root_function(IMT_max)
    
    logger.info(f"Receiver: {str(rx_label)}")
    logger.info(f"Function value at {imt} = {str(IMT_min)} : {lower_bound_value}")
    logger.info(f"Function value at {imt} = {str(IMT_mid)} : {mid_point_value}")
    logger.info(f"Function value at {imt} = {str(IMT_max)} : {upper_bound_value}")
    
    if np.sign(lower_bound_value) == np.sign(upper_bound_value):
        msg = "Function values at the interval endpoints must differ in sign for fsolve to work. Expand the interval or use a different model."
        logger.error(msg)
        gm_est = np.nan
        return gm_est
        # raise ValueError(msg)
    
    # Find root of function
    start = timer()       
        
    try: 
        method='brenth'
        logger.debug("Now trying Scipy " + method)
        output = root_scalar(exceedance_root_function, bracket=[IMT_min, IMT_max], rtol=rtol, method=method)
        gm_est = output.root
        
    except Exception as error:
        logger.error(f"An exception occurred: {error}")
        logger.info("Set ground motion value to nan")
        gm_est = np.nan
        
    end = timer()
    logger.info(f"Ground motion estimation computation time: {round(end - start,1)} seconds")
    logger.info(f"Estimated {imt}: {gm_est}")  
    
    return gm_est