import numpy as np
from scipy.stats import t, norm
from scipy.optimize.cython_optimize cimport brenth
from timeit import default_timer as timer
import logging

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

from cython_exceedance import exceedance_core

def compute_IMT_exceedance(rx_lat, rx_lon, r, fr, p, lambdas, D, percentages_D, magnitudes, magnitude_pdf, magnitude_cdf, model, log_level=logging.INFO, imt='PGA', IMT_min=0.01, IMT_max=2.0, rx_label=None, verbose=False, rtol=0.1):
    
    logging.basicConfig(filename="application.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger('igfash.gm')
    logger.setLevel(log_level)
 
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

    def exceedance_root_function(a):
        return exceedance_core(a, r, fr, lambdas, D, percentages_D, magnitudes,
                               magnitude_pdf, magnitude_cdf, context_maker, ctx,
                               model, num_ground_motion_records) - p

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
        msg = "Function values at the interval endpoints must differ in sign for fsolve to work. Consider a different ground motion model."
        logger.error(msg)
        gm_est = np.nan
        return gm_est
        # raise ValueError(msg)
    
    # Find root of function
    start = timer()       
        
    try: 
        method='brenth'
        logger.debug("Now trying Scipy " + method)
        output = brenth(exceedance_root_function, bracket=[IMT_min, IMT_max], rtol=rtol, method=method)
        gm_est = output.root
        
    except Exception as error:
        logger.error(f"An exception occurred: {error}")
        logger.info("Set ground motion value to -1")
        gm_est = np.nan
        # gm_est = -1
        
    end = timer()
    logger.info(f"Ground motion estimation computation time: {round(end - start,1)} seconds")
    logger.info(f"Estimated {imt}: {gm_est}")  
    
    return gm_est