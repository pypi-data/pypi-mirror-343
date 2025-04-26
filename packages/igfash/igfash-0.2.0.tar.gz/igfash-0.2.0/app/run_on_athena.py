# -*- coding: utf-8 -*-
# import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import MultipleLocator
from matplotlib.contour import ContourSet  # Tasos
from skimage.transform import resize
import logging
import igfash
from igfash.gm import compute_IMT_exceedance
from igfash.io import read_mat_cat, read_mat_m, read_mat_pdf, read_csv
from igfash.window import win_CTL, win_CNE
import igfash.kde as kde
from igfash.compute import get_cdf, hellinger_dist, cols_to_rows
from igfash.rate import lambda_probs, calc_bins, bootstrap_forecast_rolling
from igfash.mc import estimate_mc
import numpy as np
from timeit import default_timer as timer
import psutil
import dask
from dask.diagnostics import ProgressBar # use Dask progress bar
from dask.distributed import Client
from tqdm import tqdm
import math
import kalepy as kale
from math import ceil, floor
import sys
import utm

#%% BEGIN PROGRAM
if __name__ == '__main__':



    # Configuration
    # verbose = False
    verbose = True
    

    
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    log_filename = "application.log"

    logging.basicConfig(
                        filename = log_filename,
                        # filename="application_win.log",
                        filemode = 'w',
                        format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt = '%H:%M:%S')

    logger = logging.getLogger('igfash')
    logger.setLevel(log_level)
    
    # mode = 'M' # Magnitude distribution modeling only
    # mode = 'L' # Location distribution modeling only
    # mode = 'R' # Rate modeling only
    # mode = 'ML'
    # mode = 'Lforecast' # forecast using input model files, build support later
    mode = 'MLRforecast' # modeling and forecasting, same as None
    # mode = None # do full forecast
       
    
    
    lambdas = [0.3]
    lambdas_perc = [1]
    
    windowing = False
    
    file = "LGCD_catalog.mat" #mc=1.8 to 2, m_max=5
    mc = 2
    m_max = 5 
    

    catalog_file = "c:/igf/data/catalogs/" + file
    # catalog_file = "./" + file
    catalog_label='Ctg'
    # catalog_label='Catalog'
    mag_label='Mw'

    #load magnitude PDF from file
    if False:
    # if True:
        m_pdf = read_mat_pdf('./PDF.mat')
        m_range = read_mat_m('./m.mat')
    
        
    # Activite Rate modeling parameters; default 90 days
    time_range = 90
    time_unit = 'days'
    # time_unit = 'hours'
    # time_unit = 'weeks'
    # time_unit = 'years'
    
    #### Mdist configuration ####
    # kde_pkg = 'KDEpy-ISJ'
    # kde_pkg = 'KDEpy-silverman'
    # kde_pkg = 'KDEpy-scott'
    # kde_pkg = 'adaptiveKDE'
    kde_pkg = 'diffKDE'
    # kde_pkg = 'arviz-isj'
    # kde_pkg = 'arviz-silverman'
    # kde_pkg = 'arviz-scott'



    grid_dim = 2000.0 # in metres #for 2D KDE and also for forecasting... use same grid?
    
    # exclude_low_fxy = False
    exclude_low_fxy = True
    thresh_fxy = 1e-3 #minimum fxy value (location PDF) needed to do PGA estimation (to skip low probability areas); also should scale according to number of grid points
    
    xy_win_overlap = 0.1 #not used for 'TW' mode
    
    time_D = 100 #forecast length in time_units
    
    p = 0.05     # Probability of exceedance
    
    # use_pp = False
    use_pp = True #set to always True?  
    
    if use_pp:
        
        ncpu = psutil.cpu_count(logical=False)
        logger.debug(f"Number of physical cores: {ncpu}")
        
        # dask.config.set(scheduler='processes') #default use all the cores
        dask.config.set(scheduler='processes', num_workers = 4) #use all but 4 cores
        # logger.debug("Parallel processing activated") 


    if file[-3:] == 'mat':
        time, mag, lat, lon, depth = read_mat_cat(catalog_file, catalog_label=catalog_label, mag_label=mag_label)
    elif file[-3:] == 'csv':
        time, mag, lat, lon, depth = read_csv(catalog_file, datenum=False)
      
    if False:
    # if True:
        logger.info("No Mc provided; therefore automatically run magnitude completeness test.")
        mc_test = np.round(np.arange(mag.min(), mag.max(), 0.1), 2).tolist()
        ans = estimate_mc(mag, mc_test, delta_m=0.1, p_pass=0.1, stop_when_passed=True, n_samples=10000)
        mc = ans[3]
        logger.info(f"Mc estimated at {mc}")

    #remove events below Mc
    if mc != None:
        indices = np.argwhere(mag<mc)
        mag = np.delete(mag, indices)
        time = np.delete(time, indices)
        lat = np.delete(lat, indices)
        lon = np.delete(lon, indices)
    else:
        mc = mag.min() 

#%% M distribution modeling
    if 'M' in mode:
        logger.info("M mode - Magnitude distribution modeling")

        n_kde=128

        
            
        if kde_pkg == None:
            logger.warning("No KDE method specified, therefore use diffKDE by default")
            kde_pkg ='diffKDE'
    
        if mag_label == None:
            logger.warning("No magnitude label of catalog specified, therefore try ML by default")
            mag_label='ML'
              
        start = timer()
        

        t_windowed, r_windowed = win_CNE(time, [lon, lat, mag], win_size = len(mag), win_overlap = 0, min_events = 1)
    
        m_windowed = [r[2] for r in r_windowed] #extract only magnitude windows
    
            
        if kde_pkg[:5] == 'KDEpy':
            pdf = kde.compute_kde(m_windowed, xmin=mc,xmax=m_max, bw_method = kde_pkg[6:], n_kde=n_kde*2, pp=use_pp )
        elif kde_pkg == 'adaptiveKDE':
            pdf = kde.compute_adaptivekde(m_windowed, bw_method = "adaptive-local", xmin=mc, xmax=m_max, n_kde=n_kde*2, pp=use_pp)
        elif kde_pkg == 'diffKDE':
            pdf = kde.compute_diffkde(m_windowed, xmin=mc, xmax=m_max, n_kde=n_kde*2, pp=use_pp)
        elif kde_pkg[:5] == 'arviz':
            pdf = kde.compute_arvizkde(m_windowed, xmin=mc, xmax=m_max, bw_method=kde_pkg[6:], n_kde=n_kde*2, pp=use_pp)
            
        end = timer()
        logger.info(f"Magnitude KDE Computation time: {round(end - start, 1)} seconds")
    
        m_pdf = 2*pdf[-1] #select last window's pdf as the one to use for forecasting
        m_range= np.linspace(mc, m_max, n_kde)
        
        bin_width=0.1 #Tasos
        bins = np.arange(min(m_windowed[-1]), max(m_windowed[-1]) + bin_width, bin_width) #Tasos

        #plot only the last window                
        figsize=(8, 6)
        dpi=300
        fig = plt.figure(dpi=dpi, figsize=figsize)   
        # fig, ax = plt.subplots(dpi=dpi, figsize=figsize)
        plt.hist(m_windowed[-1], bins=bins, color='blue', edgecolor='black', alpha=0.6, density=True, label='Magnitude bins') #Tasos
        plt.plot(m_range, m_pdf, color='red', linewidth=2.5, label='KDE') #Tasos
        plt.legend() #Tasos
        
        # Configure ticks #Tasos
        ax = plt.gca() #Tasos
        ax.xaxis.set_major_locator(MultipleLocator(0.2)) # Major ticks every 0.2 #Tasos
        ax.xaxis.set_minor_locator(MultipleLocator(0.1)) # Minor ticks every 0.1 #Tasos
        ax.tick_params(axis='x', which='major', labelsize=10)  # Labels only for major ticks #Tasos
        ax.tick_params(axis='x', which='minor', length=5, labelsize=0)  # No labels for minor ticks #Tasos
        
        # Rotate ticks by 45 degrees #Tasos
        plt.xticks(rotation=45) #Tasos
        plt.ylabel("f(M)")
        plt.xlabel("Magnitude")

        plt.show()
        
        np.savetxt('last_window_KDE_PDF.csv', np.c_[m_range, m_pdf])

#%% L location distribution modeling
    if 'L' in mode:
        logger.info("L mode - Location distribution modeling")

        method = 'TW'
        # method = ''

        
        win_size = 100 #number of events
        
        # method = 'CTL'
        # win_size = 200 #number of events
    
        # if method == None:
        #     print("No method specified, therefore use CNE by default")
        #     method = 'CNE'
    
        #convert to UTM
        u = utm.from_latlon(lat, lon) 
        x = u[0]
        y = u[1]
        utm_zone_number = u[2]
        utm_zone_letter = u[3]
        #define corners of grid based on global dataset (or make it user selectable?)
        # x_min = lon.min()
        # y_min = lat.min()
        # x_max = lon.max()
        # y_max = lat.max()
        x_min = x.min()
        y_min = y.min()
        x_max = x.max()
        y_max = y.max()
        z_min = depth.min()
        z_max = depth.max()
        
        grid_x_max = int(ceil(x_max / grid_dim) * grid_dim)
        grid_x_min = int(floor(x_min / grid_dim) * grid_dim)
        grid_y_max = int(ceil(y_max / grid_dim) * grid_dim)
        grid_y_min = int(floor(y_min / grid_dim) * grid_dim)
        
        #rectangular grid
        nx = int((grid_x_max - grid_x_min) / grid_dim)+1            
        ny = int((grid_y_max - grid_y_min) / grid_dim)+1            




        # ensure a square grid is used
        if nx > ny: #enlarge y dimension to match x
            ny = nx
            grid_y_max = int(grid_y_min + (ny-1)*grid_dim)

        else: #enlarge x dimension to match y
            nx = ny
            grid_x_max = int(grid_x_min + (nx-1)*grid_dim)

        # new x and y range
        x_range = np.linspace(grid_x_min, grid_x_max, nx)
        y_range = np.linspace(grid_y_min, grid_y_max, ny)
        
       
        
        start = timer()
        
        t_windowed = time
        r_windowed = [[x, y]]
    

        #compute KDE and extract PDF
        logger.info("Computing KDE of each window...")
        
        if method == "TW":
            x_weights = np.linspace(0,15,len(t_windowed))
            weighting_fcn = np.exp(x_weights) #exponential weighting 
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx, weighting_fcn=weighting_fcn)
        else:
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx)
        
       
        end = timer()
    
        logger.info(f"2D KDE Computation time: {round(end - start,1)} seconds")
    
        #take only the last window for use in forecasting
        xy_kale = output_kale[-1] 
        xy_kde = output_kde[-1]
        
        xy_kale_km = type(xy_kale)(xy_kale.dataset / 1000) #Tasos
        
        #plot only the last window
        # corner = kale.corner(xy_kale)
        corner = kale.corner(xy_kale_km,quantiles=[0.025, 0.16, 0.50, 0.84, 0.975],cmap='hot') #Tasos

        from matplotlib.ticker import FormatStrFormatter
        from matplotlib.ticker import MultipleLocator
        ax00 = corner[0].axes[0][0] # bottom left plot
        ax00.set_ylabel("Probability Density")
        # ax00.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))  # Ensure 4 decimal places displayed
        
        # Remove the PDF ticks below zero
        yticks = ax00.get_yticks()
        new_yticks = yticks[yticks>=0]
        ax00.set_yticks(new_yticks)

        # ax01 = corner[0].axes[0][1] # bottom right plot
        
        ax10 = corner[0].axes[1][0] # top left plot
        # ax10.set_aspect('equal')  # Makes the units equal on both axes

        ax10.set_xlabel("UTM X (km)") #Tasos
        ax10.set_ylabel("UTM Y (km)") #Tasos
        ax10.ticklabel_format(style='plain') 
        for coll in ax10.collections: #Tasos
            if isinstance(coll, ContourSet):  # Check if it's a contour plot Tasos
                ax10.clabel(coll, inline=True, fontsize='smaller', fmt="%.1f") #Tasos
        # ax10.xaxis.set_major_locator(MultipleLocator(1000))
        # ax10.yaxis.set_major_locator(MultipleLocator(1000))

        ax11 = corner[0].axes[1][1] # top right plot
        ax11.set_xlabel("Probability Density")
        # ax11.set_ylabel("UTM Y (m)")
        ax11.ticklabel_format(style='plain') 
        # ax11.yaxis.set_major_locator(MultipleLocator(1000))
        
        # Remove the PDF ticks below zero
        xticks = ax11.get_xticks()
        new_xticks = xticks[xticks>=0]
        ax11.set_xticks(new_xticks)
        ax11.set_yticklabels([])  # This removes the ytick labels # Tasos

        
        # Rotate x-axis tick labels for all bottom-row plots
        for ax in corner[0].axes[-1, :]:  # Last row corresponds to the bottom x-axes
            for label in ax.get_xticklabels():
                label.set_rotation(46)
     
        # corner[0].legend()
        corner[0].fig.savefig('2d_kd_cornerplot.png', bbox_inches = "tight", dpi=300)
        # np.savetxt('last_window_KDE_PDF.csv', np.array(xy_kale[0]))
        # plt.hist(m_windowed[-1], bins='auto', density=True)
        # plt.plot(m_range, 2*pdf[-1])
        # plt.show()
        
        # np.savetxt('last_window_KDE_PDF.csv', 2*pdf[-1])

#%% Activity Rate modeling
    if 'R' in mode:
        logger.info("R mode - activity Rate modeling")

        if file[-3:] == 'mat':
            time, mag_dummy, lat_dummy, lon_dummy, depth_dummy = read_mat_cat(catalog_file, catalog_label=catalog_label, mag_label = mag_label, output_datenum=True)    
            datenum_data = time # REMEMBER THE DECIMAL DENOTES DAYS
            # datetime_data = [datenum_to_datetime(d) for d in datenum_data] # NOT NECESSARILY NEEDED 

        elif file[-3:] == 'csv':
            time, mag_dummy, lat_dummy, lon_dummy, depth_dummy = read_csv(catalog_file, datenum=False)
               
        if time_unit == 'hours':
            multiplicator = 24
        elif time_unit == 'days':
            multiplicator = 1
        elif time_unit == 'weeks':
            multiplicator = 1/7
        elif time_unit == 'years':
            multiplicator = 1/365
        
        # Selects dates in datenum format and procceeds to forecast value
        start_date = datenum_data[-1] - (2 * time_range / multiplicator)
        dates_calc = [date for date in datenum_data if start_date <= date <= datenum_data[-1]]
        forecasts, bca_conf95, rate_mean = bootstrap_forecast_rolling(dates_calc, multiplicator)

        # FINAL VALUES OF RATE AND ITS UNCERTAINTY IN THE 5-95 PERCENTILE
        unc_bca05=[ci.low for ci in bca_conf95]; unc_bca95=[ci.high for ci in bca_conf95]
        rate_unc_high=multiplicator/np.array(unc_bca05); rate_unc_low=multiplicator/np.array(unc_bca95); 
        rate_forecast= multiplicator / np.median(forecasts) #[per time unit]

        # Plot of forecasted activity rate with previous binned activity rate
        act_rate, bin_counts, bin_edges, out, pprs, rt, idx, u_e = calc_bins(np.array(datenum_data), time_unit, time_range, dates_calc, rate_forecast, rate_unc_high, rate_unc_low, multiplicator, quiet=True)

        # Assign probabilities 
        lambdas, lambdas_perc = lambda_probs(act_rate,dates_calc,bin_edges)

        lambdas = np.array(lambdas)
        lambdas_perc = np.array(lambdas_perc)

        logger.debug(f"Activity rates {lambdas} with percentages {lambdas_perc}")



#%% Forecasting        
    if "forecast" in mode:
        logger.info("Forecast mode - seismic hazard asssessment")

        # use these activity rates
        # lambdas = [0.5, 0.2, 1.1] # Vector of seismic activity rates for different sub-periods
        # percentages_D = [0.3, 0.2, 0.5] #Vector of percentage of D corresponding to each sub-period

        # lambdas = [rate_forecast]
        # lambdas = [1.0] #for testing
        # percentages_D = [1.0]
        
        # model = 'Lasocki2013' 
        model = 'Atkinson2015'
        # model = 'ConvertitoEtAl2012Geysers'
        # products =  ['PGA', 'SA(0.03)', 'SA(0.05)', 'SA(0.1)', 'SA(0.2)']
        # products =  ['PGA', '0.6']
        # products =  ['PGA']
        products =  ['SA(1.0)']

        Mag = 5.0 #placeholder mag, must be valid for that context; will be overwritten during function call
        rupture_aratio = 1.5
        Strike = 0
        Dip = 90
        Rake = 0


        m_cdf = get_cdf(m_pdf) 
               
        fxy=xy_kde[0]
        logger.debug(f"Verification that f(x,y) is normalized; Sum of all f(x,y) values = {np.sum(fxy)}")
                     
        
        plt.imshow(fxy, origin='lower')
        plt.show()


        xx, yy = np.meshgrid(x_range, y_range, indexing='ij')         # grid points
        
        
        # set every grid point to be a receiver
        x_rx = xx.flatten()
        y_rx = yy.flatten()
        
        distances = np.zeros(shape=(nx*ny, nx, ny))
        rx_lat=np.zeros(nx*ny)
        rx_lon=np.zeros(nx*ny)
        
        # compute distance matrix for each receiver
        for i in range(nx*ny):
            
            # Compute the squared distances directly using NumPy's vectorized operations
            squared_distances = (xx - x_rx[i])**2 + (yy - y_rx[i])**2
            
            distances[i] = np.sqrt(squared_distances)

            # create context object for receiver and append to list            
            # most of these parameters do not have any effect as our gmpe does not use this information
            
            rx_lat[i], rx_lon[i] = utm.to_latlon(x_rx[i], y_rx[i], utm_zone_number, utm_zone_letter) #get receiver location as lat,lon
            










        
        plt.imshow(distances[0], origin='lower')
        plt.show()
        
        
        #experimental - compute PGA at grid points that have minimum probability density of thresh_fxy
        if exclude_low_fxy:
            indices = list(np.where(fxy.flatten() > thresh_fxy)[0])
        else:
            indices = range(0,len(distances))
        # r = distances.flatten()

        
        fr = fxy.flatten()
        
        #For each receiver compute estimated ground motion values
        logger.info(f"Estimating ground motion at {len(indices)} grid points...")
        start = timer()

        #DEBUG just do this Rx
        if use_pp:
            pbar = ProgressBar()
            pbar.register()
            # iter = range(0,len(distances))
            iter = indices
            iml_grid_raw = []
            for imt in products:
                logger.info(f"Estimating {imt}")
                imls = [dask.delayed(compute_IMT_exceedance)(rx_lat[i], rx_lon[i], distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc,\
                                                             m_range, m_pdf, m_cdf, model, log_level=log_level, imt=imt, IMT_min = 0.0, IMT_max = 2.0, rx_label = i, precision = 1e-2) for i in iter]
                iml = dask.compute(*imls)
                iml_grid_raw.append(list(iml))
                
        else:
            # iter = tqdm(range(0,len(distances)))      
            iter = tqdm(indices)      
            
            iml_grid_raw = []
            for imt in products:

                iml = []
                for i in iter:
                    

                    iml_i = compute_IMT_exceedance(rx_lat[i], rx_lon[i], distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, model, imt=imt, IMT_min = 0.0, IMT_max = 20.0, rx_label = i)
    
                    iml.append(iml_i)
                    logger.info(f"Estimated {imt} at rx {i} is {iml_i}")
                iml_grid_raw.append(iml)

        end = timer()
        logger.info(f"Ground motion exceedance computation time: {round(end - start, 1)} seconds")

        
        #create list of one empty list for each imt
        iml_grid = [ [] for _ in range(len(products)) ] # final grids
        iml_grid_prep = iml_grid.copy() # temp grids
        
        if exclude_low_fxy:
                        
            for i in range(0,len(distances)):
                
                if i in indices:
                
                    for j in range(0,len(products)):    
                        iml_grid_prep[j].append(iml_grid_raw[j].pop(0))
                                        
                else:
                    list(map(lambda lst: lst.append(np.nan), iml_grid_prep)) # use np.nan to indicate grid point excluded
                    

        else:
            iml_grid_prep = iml_grid_raw

        
        if False:
        # if True:
        
            # idx_redo = list(np.where([math.isnan(pga_value) for pga_value in pga]))
            idx_redo = np.where([pga_value < 0 for pga_value in pga_grid_prep])[0] #list of indices where pga calculation failed
            
            
            if len(idx_redo)>0:            
                # ims_redo = [dask.delayed(compute_PGA_exceedance)(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0, rx_label = i) for i in idx_redo]
                # pga_redo = dask.compute(*ims_redo) 
            
            
            
                for i in idx_redo:
                    # run computation again with slightly different params and hope solver finds a solution?
                    pga_redone=compute_PGA_exceedance(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0, rx_label = i)
            
                    pga_grid_prep[i] = pga_redone
            
        
        
        # plot grid for each imt
        
        for j in range(0, len(products)):
  
            # get values for log color scale
            vmin = min(x for x in iml_grid_prep[j] if x is not np.nan)
            vmax = max(x for x in iml_grid_prep[j] if x is not np.nan)
            # vmin = min(x for x in pga_grid_prep if x is not None)
            # vmax = max(x for x in pga_grid_prep if x is not None)
            
            #swap np.nan for None values in grid
            # pga_grid_prep = np.where(pga_grid_prep != np.nan, pga_grid_prep, None) #doesn't work yet
            
            #debug individual receivers
            # r = distances[61].flatten()
            # PGA_value = compute_PGA_exceedance(r, fr, p, lambdas, time_D, percentages_D, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 5.0)
    
            # PGA = np.array(PGA, shape=(nx, ny))
            # PGA2 = np.reshape(PGA, (nx, ny), order='C') 
            iml_grid[j] = np.reshape(iml_grid_prep[j], (nx, ny)).astype(dtype=np.float64)  # this reduces PGA values to 8 decimal places
    
            dpi=300
            fig = plt.figure(dpi=dpi)   
            # extent = [int(grid_x_min/1000), int(grid_x_max/1000), int(grid_y_min/1000), int(grid_y_max/1000)] #display extent in kilometres
            plt.imshow(iml_grid[j], extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis') #linear color bar
            # plt.imshow(pga_grid, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis',  norm=colors.LogNorm(vmin=vmin, vmax=vmax)) #log color bar
            plt.xlabel('UTM X (km)')
            plt.ylabel('UTM Y (km)')
            plt.colorbar(label=products[j])
            # plt.scatter(x/1000,y/1000, alpha=0.1, c='grey', marker='.', s=1.5)
            # plt.scatter(x/1000,y/1000, alpha=0.8, c='grey', marker='.', s=5)
            
            # Generate scatter plot for each magnitude range # Tasos 
            sc_offset = abs(mc)+1 if mc < 0 else 0 # Support for negative magnitudes in scatter plot Tasos
            for i in range(int(np.floor(mc)), int(np.ceil(m_max))): # Tasos
                mask = (mag >= i) & (mag < i + 1)  # Magnitudes in range # Tasos
                sizes =  3 * (i + sc_offset)  # Size for circles # Tasos
                plt.scatter(x[mask]/1000, y[mask]/1000, alpha=0.7, c='grey', marker='o', s=sizes,
                            edgecolors='black', linewidths=0.2, label=f'{i:.1f}–{i+1:.1f}') # Tasos
            plt.legend(title="Magnitudes", fontsize=6, title_fontsize=6) # Tasos
            
            plt.show()
    
           
#%% Upscale grid (experimental)

            iml_grid_tmp = np.nan_to_num(iml_grid[j]) # change nans to zeroes
            
            up_factor = 4
            # Upscale the grid
            iml_grid_hd = resize(iml_grid_tmp, (up_factor*len(iml_grid_tmp), up_factor*len(iml_grid_tmp)), mode='reflect', anti_aliasing=False)
            # pga_grid_hd = resize(pga_grid, (up_factor*len(pga_grid), up_factor*len(pga_grid)), mode='symmetric', anti_aliasing=False)
            
            iml_grid_hd[iml_grid_hd == 0.0] = np.nan # change zeroes back to nan
            
            plt.imshow(iml_grid_hd, origin='lower', extent=[0, 1, 0, 1], aspect='auto')
            plt.colorbar()
            plt.title("Upscaled Grid with NumPy")
            plt.show()
            


    
    
            
            figsize=(3.54,3.54)
            dpi=300
            fig, ax = plt.subplots(dpi=dpi, figsize=figsize)
            plt.imshow(iml_grid_hd, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis')
            # plt.imshow(pga_grid_hd, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis',  norm=colors.LogNorm(vmin=vmin, vmax=vmax)) #log color bar
            plt.xlabel('UTM X (km)')
            plt.ylabel('UTM Y (km)')
            plt.colorbar(label=products[j])
            
            # Generate scatter plot for each magnitude range # Tasos 
            sc_offset = abs(mc)+1 if mc < 0 else 0 # Support for negative magnitudes in scatter plot Tasos
            for i in range(int(np.floor(mc)), int(np.ceil(m_max))): # Tasos
                mask = (mag >= i) & (mag < i + 1)  # Magnitudes in range # Tasos
                sizes =  3 * (i + sc_offset)  # Size for circles # Tasos
                plt.scatter(x[mask]/1000, y[mask]/1000, alpha=0.7, c='grey', marker='o', s=sizes,
                            edgecolors='black', linewidths=0.2, label=f'{i:.1f}–{i+1:.1f}') # Tasos
            plt.legend(title="Magnitudes", fontsize=6, title_fontsize=6) # Tasos
            
            plt.show()

            #%% Trim edges so the grid is not so blocky
            vmin_hd = min(x for x in iml_grid_hd.flatten() if not math.isnan(x))
            vmax_hd = max(x for x in iml_grid_hd.flatten() if not math.isnan(x))
            # trim_thresh = vmin_hd + 0.3*(vmax_hd-vmin_hd)
            trim_thresh = vmin
            iml_grid_hd[iml_grid_hd < trim_thresh] = np.nan


            # %% Visualization - generate overlay of PGA grid over map tiles
                      
            # cmap_name = 'magma'
            cmap_name = 'viridis'
            cmap = plt.get_cmap(cmap_name)
            
            north, south = lat.max(), lat.min()  # Latitude range
            east, west = lon.max(), lon.min()  # Longitude range
            bounds = [[south, west], [north, east]]
            
            map_center = [np.mean([north, south]), np.mean([east, west])]
            
            # Create an image from the grid
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(iml_grid_hd, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
            ax.axis('off')
            
            # Save the figure
            fig.canvas.draw()
            # image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8) #alt way using numpy file instead of png 
            # image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))        
            # plt.savefig("overlay_with_transparency.png", bbox_inches="tight", pad_inches=0, transparent=True)
            plt.savefig(products[j] + "_overlay.svg", bbox_inches="tight", pad_inches=0, transparent=True)
            plt.show()
            plt.close(fig)
            
            # make vertical color bar

            width = 50
            height = 500
            
            gradient = np.linspace(0, 1, height)
            gradient = np.vstack((gradient, gradient)).T
            gradient = np.tile(gradient, (1, width))
            
            fig, ax = plt.subplots(figsize=((width + 40) / 100.0, (height + 20) / 100.0), dpi=100) # Increase fig size for labels
            
            ax.imshow(gradient, aspect='auto', cmap=cmap.reversed(), extent=[0, 1, vmin, vmax_hd]) # Note: extent order is different for vertical
            
            # Set ticks and labels
            ax.set_xticks([]) # Remove x-ticks for vertical colorbar
            num_ticks = 11 # Show more ticks
            tick_positions = np.linspace(vmin, vmax_hd, num_ticks)
            ax.set_yticks(tick_positions)
            ax.set_yticklabels([f"{tick:.2f}" for tick in tick_positions])  #format tick labels
            
            ax.set_title(products[j], pad = 15) 

            # Adjust Layout
            fig.subplots_adjust(left=0.25, right=0.75, bottom=0.05, top=0.95)
            
            fig.savefig(products[j] + "_colorbar.svg", bbox_inches='tight')
            plt.show()
            plt.close(fig)

            
            continue