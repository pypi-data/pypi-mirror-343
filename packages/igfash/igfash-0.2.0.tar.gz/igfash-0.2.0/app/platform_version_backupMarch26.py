# -*- coding: utf-8 -*-
import sys
import logging
from timeit import default_timer as timer
import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def uninstall(package):
    if hasattr(pip, 'main'):
        pip.main(['uninstall', '-y', package])
    else:
        pip._internal.main(['uninstall', '-y', package])

def main(*args):
    """
    Python application that reads an earthquake catalog and performs non-parametric estimation of the earthquake location distribtion.
    Arguments:
        catalog_file: path to input file of type 'Catalog'
    Returns:
        PNG image files containing a plot of the probability distribution function obtained by non-parametric estimation and CSV files of these PDFs.
    """


    logging.basicConfig(filename="application.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')   
    logger = logging.getLogger('igfash')


    #DEBUGGING (delete later)
    #logger.setLevel(logging.DEBUG)
    #import importlib
    #import shutil
    #import openquake
    #import importlib.resources as ir
    
    #target_dir = ir.files('openquake') / 'hazardlib/gsim'
    #source_dir = ir.files('igfash') / 'gsim'

    #if source_dir.is_dir() and target_dir.is_dir():
    #    for file in [item for item in source_dir.iterdir() if item.is_file()]:
    #        logger.info(file)
    #        shutil.copy2(file, target_dir)

    try:
        import openquake.engine
    except ModuleNotFoundError:
        install('openquake.engine')
        import openquake.engine

    try:
        import igfash
        if igfash.__version__ != '0.1.4':
            uninstall('igfash')
            install('igfash==0.1.4')
            import igfash
    except ModuleNotFoundError:
        install('igfash')

    try:
        import fiona
    except ModuleNotFoundError:
        install('fiona')
#    try:
#        import numpy as np
#        if np.__version__ != '1.23.5':
#            uninstall('numpy')
#            install('numpy==1.23.5')
#            import numpy as np
#    except ModuleNotFoundError:
#        install('numpy==1.23.5')
    
#    try:
#        import scipy
#        if scipy.__version__ != '1.12.0':
#            uninstall('scipy')
#            install('scipy==1.12.0')
#            import scipy
#    except ModuleNotFoundError:
#        install('scipy==1.12.0')

    try:
        import obspy
        if obspy.__version__ != '1.4.1':
            uninstall('obspy')
            install('obspy==1.4.1')
            import obspy
    except ModuleNotFoundError:
        install('obspy==1.4.1')


    try:
        from tqdm import tqdm
    except ModuleNotFoundError:
        install('tqdm')
    
    try:
        import dask
    except ModuleNotFoundError:
        install('dask')

    #try:
     #   import numba
     #   if numba.__version__ != '0.59.1':
      #      uninstall('numba')
       #     install('numba==0.59.1')
    #except ModuleNotFoundError:
     #   install('numba==0.59.1')

    try:
        import kalepy as kale
        if kale.__version__ != '1.4.3':
            uninstall('kalepy')
            install('kalepy==1.4.3')
    except ModuleNotFoundError:
        install('kalepy==1.4.3')

#    try:
#        target_version = '0.0.14'
#        import igfash
#        if igfash.__version__ != target_version:
#            uninstall('igfash')
#            pip.main(['install', '--verbose', '-i', 'https://test.pypi.org/pypi/', '--extra-index-url', 'https://pypi.org/simple', 'igfash=='+target_version]) #install eqpi from testpypi repo for now
#    except ModuleNotFoundError:
#        pip.main(['install', '--verbose', '-i', 'https://test.pypi.org/pypi/', '--extra-index-url', 'https://pypi.org/simple', 'igfash=='+target_version]) #install eqpi from testpypi repo for now
    
    try:
        import diffKDE
    except ModuleNotFoundError:
        pip.main(['install', '--verbose', '-i', 'https://test.pypi.org/pypi/', '--extra-index-url', 'https://pypi.org/simple', 'diffKDE']) #install diffKDE from testpypi repo for now

    try:
        import utm
    except ModuleNotFoundError:
        install('utm')

    try:
        import Rbeast
    except ModuleNotFoundError:
        install('Rbeast')

    try:
        import pyroots
    except ModuleNotFoundError:
        install('pyroots')

    try:
        import resample
    except ModuleNotFoundError:
        install('resample')

    try:
        import folium
    except ModuleNotFoundError:
        install('folium')

    try:
        import skimage
    except ModuleNotFoundError:
        install('scikit-image')

    try:
        import branca
    except ModuleNotFoundError:
        install('branca')

    from math import ceil, floor
    from igfash.io import read_mat_cat, read_mat_m, read_mat_pdf, read_csv
    from igfash.window import win_CTL, win_CNE
    import igfash.kde as kde
    from igfash.gm import compute_IMT_exceedance
    from igfash.compute import get_cdf, hellinger_dist, cols_to_rows
    from igfash.rate import lambda_probs, calc_bins, bootstrap_forecast_rolling
    from igfash.mc import estimate_mc

    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    from matplotlib.contour import ContourSet
    import matplotlib.colors as colors

    import numpy as np
    import scipy
    import obspy
    from tqdm import tqdm
    import dask
    from dask.diagnostics import ProgressBar # use Dask progress bar
    import kalepy as kale
    import utm
    from skimage.transform import resize
    import branca
    import psutil

    import folium
    from folium.raster_layers import ImageOverlay
    from folium import TileLayer

    #get input files
    catalog_file = args[0]

    if args[1] != args[-17]:  #magnitude of completeness file provided
        mc_file = args[1]
    else:
        mc_file = None

    if args[2] != args[-16]:  #magnitude PDF file provided
        pdf_file = args[2]
        m_pdf = read_mat_pdf(pdf_file)
    else:
        pdf_file = None
        m_pdf = [None]

    if args[3] != args[-15]:  #magnitude range file provided
        m_file = args[3]
        m_range = read_mat_m(m_file)
    else:
        m_file = None
        m_range = [None]

    #parse user input parameters
    m_select = args[-17]
    mag_label = args[-16]
    mc = args[-15]
    m_max = args[-14]
    m_kde_method = args[-13] 
    xy_select = args[-12]
    grid_dim = args[-11]
    xy_win_method = args[-10] 
    rate_select= args[-9]
    time_win_duration = args[-8]  
    forecast_select = args[-7]
    custom_rate = args[-6]
    forecast_len = args[-5]
    time_unit = args[-4]
    model = args[-3]
    products_string = args[-2]
    verbose = args[-1]

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # temporary hard-coded configuration
    # exclude_low_fxy = False
    exclude_low_fxy = True
    thresh_fxy = 1e-3 #minimum fxy value (location PDF) needed to do PGA estimation (to skip low probability areas); also should scale according to number of grid points

    # log user selections
    logger.debug(f"User input files\n Catalog: {catalog_file}\n Mc: {mc_file}\n Mag_PDF: {pdf_file}\n Mag: {m_file}")
    logger.debug(f"User options\n m_select: {m_select}\n mag_label: {mag_label}\n mc: {mc}\n m_max:{m_max}\n m_kde_method: {m_kde_method}\n \
xy_select: {xy_select}\n grid_dim: {grid_dim}\n xy_win_method: {xy_win_method}\n rate_select: {rate_select}\n time_win_duration: {time_win_duration}\n \
forecast_select: {forecast_select}\n custom_rate: {custom_rate}\n forecast_len: {forecast_len}\n time_unit: {time_unit}\n model: {model}\n products: {products_string}\n \
verbose: {verbose}")

    # print key package version numbers
    logger.debug(f"Python version {sys.version}")
    logger.debug(f"Numpy version {np.__version__}")
    logger.debug(f"Scipy version {scipy.__version__}")  
    logger.debug(f"Obspy version {obspy.__version__}")
    logger.debug(f"Openquake version {openquake.engine.__version__}")
    logger.debug(f"Igfash version {igfash.__version__}")

    # print number of cpu cores available
    ncpu = psutil.cpu_count(logical=False)
    logger.debug(f"Number of cpu cores available: {ncpu}")
    for process in psutil.process_iter():
            with process.oneshot():
                
                # cpu = process.cpu_percent()
                cpu = process.cpu_percent() / ncpu
                
                if cpu > 1:
                    logger.debug(f"{process.name()}, {cpu}")
    
    logger.debug(f"BASELINE CPU LOAD% {psutil.cpu_percent(interval=None, percpu=True)}")

    dask.config.set(scheduler='processes')

    # run magnitude distribution modeling if selected by user and no magnitude pdf file provided
    if m_select and m_range[0] == None and m_pdf[0] == None:
        logger.info("Magnitude distribution modeling selected")

        if m_kde_method == None:
            logger.info("No KDE method specified, therefore use diffKDE by default")
            m_kde_method ='diffKDE'
        
        if mag_label == None:
            logger.info("No magnitude label of catalog specified, therefore try Mw by default")
            mag_label='Mw'

        #if cat_label == None:
         #   print("No magnitude label of catalog specified, therefore try 'Catalog' by default")
         #   cat_label='Catalog'

        time, mag, lat, lon, depth = read_mat_cat(catalog_file, mag_label=mag_label, catalog_label='Catalog')
        
        if mc != None:
            logger.info("Mc value provided by user")
            trim_to_mc = True
        elif mc_file != None:
            logger.info("Mc estimation output file provided; selecting largest Mc from the list")
            mc = read_mc(mc_file)
            trim_to_mc = True
        else:
            logger.info("No Mc provided; using all magnitudes from the catalog")
            trim_to_mc = False
            mc = mag.min()

        #remove events below mc
        if trim_to_mc:
            logger.info(f"Removing all magnitudes below {mc}")
            indices = np.argwhere(mag<mc)
            mag = np.delete(mag, indices)
            time = np.delete(time, indices)
            lat = np.delete(lat, indices)
            lon = np.delete(lon, indices)

        # if user does not provide a m_max, set m_max to 3 magnitude units above max magnitude in catalog
        if m_max == None:
            m_max = mag.max() + 3.0
             
        start = timer()

        t_windowed, r_windowed = win_CNE(time, [lon, lat, mag], win_size = len(mag), win_overlap = 0, min_events = 1)            
        m_windowed = [r[2] for r in r_windowed] #extract only magnitude windows
        
        if m_kde_method[:5] == 'KDEpy':
            pdf = kde.compute_kde(m_windowed, xmin=mc, xmax=m_max, bw_method = m_kde_method[6:], pp=False)
        elif m_kde_method == 'adaptiveKDE':
            pdf = kde.compute_adaptivekde(m_windowed, bw_method = "adaptive-local", xmin=mc, xmax=m_max, pp=False)
        elif m_kde_method == 'diffKDE':
            pdf = kde.compute_diffkde(m_windowed, xmin=mc, xmax=m_max, pp=False)
        elif m_kde_method[:5] == 'arviz':
            pdf = kde.compute_arvizkde(m_windowed, xmin=mc, xmax=m_max, bw_method=m_kde_method[6:], pp=False)

        end = timer()
        logger.info(f"Magnitude KDE Computation time: {round(end - start, 1)} seconds")

        m_pdf = 2*pdf[-1] #select last window's pdf as the one to use for forecasting
        m_range= np.linspace(mc, m_max, 256)
        
        bin_width=0.1
        bins = np.arange(min(m_windowed[-1]), max(m_windowed[-1]) + bin_width, bin_width)

        #plot only the last window
        fig = plt.figure(dpi=300, figsize=(8,6)) 
        plt.hist(m_windowed[-1], bins=bins, color='blue', edgecolor='black', alpha=0.6, density=True, label='Magnitude bins')
        plt.plot(m_range, m_pdf, color='red', linewidth=2.5, label='KDE')
        plt.legend()

        # configure ticks
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(0.2)) # Major ticks every 0.2
        ax.xaxis.set_minor_locator(MultipleLocator(0.1)) # Minor ticks every 0.1
        ax.tick_params(axis='x', which='major', labelsize=10)  # Labels only for major ticks
        ax.tick_params(axis='x', which='minor', length=5, labelsize=0)  # No labels for minor ticks
                
        plt.xticks(rotation=45) # Rotate ticks by 45 degrees
        plt.ylabel("f(M)")
        plt.xlabel("Magnitude")
        plt.savefig('KDE_magnitude_PDF.png')
        
        np.savetxt('KDE_magnitude_PDF.csv', np.c_[m_range, m_pdf])

    # run location distribution modeling
    if xy_select:
        logger.info("Event location distribution modeling selected")

        time, mag, lat, lon, depth = read_mat_cat(catalog_file)
        
        #convert to UTM
        u = utm.from_latlon(lat, lon) 
        x = u[0]
        y = u[1]
        utm_zone_number = u[2]
        utm_zone_letter = u[3]
        logger.debug(f"Latitude / Longitude coordinates correspond to UTM zone {utm_zone_number}{utm_zone_letter}")

        #define corners of grid based on global dataset
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
            
        t_windowed = time
        r_windowed = [[x, y]]

        #%% compute KDE and extract PDF
        start = timer()

        if xy_win_method == "TW":
            logger.info("Time weighting function selected")

            x_weights = np.linspace(0,15,len(t_windowed))
            weighting_fcn = np.exp(x_weights) #exponential weighting 
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx, weighting_fcn=weighting_fcn)
        else:
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx)

        end = timer()
        logger.info(f"Location KDE Computation time: {round(end - start,1)} seconds")

        xy_kale = output_kale[0]
        xy_kde = output_kde[0]

        #plot location PDF
        xy_kale_km = type(xy_kale)(xy_kale.dataset / 1000)
        corner = kale.corner(xy_kale_km,quantiles=[0.025, 0.16, 0.50, 0.84, 0.975],cmap='hot')
        
        # modify bottom left plot
        ax00 = corner[0].axes[0][0] 
        ax00.set_ylabel("Probability Density")        
        # Remove the PDF ticks below zero
        yticks = ax00.get_yticks()
        new_yticks = yticks[yticks>=0]
        ax00.set_yticks(new_yticks)

        # ax01 = corner[0].axes[0][1] # bottom right plot
        
        # modify top left plot
        ax10 = corner[0].axes[1][0] 
        ax10.set_xlabel("UTM X (km)")
        ax10.set_ylabel("UTM Y (km)")
        ax10.ticklabel_format(style='plain') 
        for coll in ax10.collections:
            if isinstance(coll, ContourSet):  # Check if it's a contour plot
                ax10.clabel(coll, inline=True, fontsize='smaller', fmt="%.1f")

        # modify top right plot
        ax11 = corner[0].axes[1][1] 
        ax11.set_xlabel("Probability Density")
        ax11.ticklabel_format(style='plain') 

        # Remove the PDF ticks below zero
        xticks = ax11.get_xticks()
        new_xticks = xticks[xticks>=0]
        ax11.set_xticks(new_xticks)
        ax11.set_yticklabels([])  # This removes the ytick labels
        
        # Rotate x-axis tick labels for all bottom-row plots
        for ax in corner[0].axes[-1, :]:  # Last row corresponds to the bottom x-axes
            for label in ax.get_xticklabels():
                label.set_rotation(46)

        corner[0].fig.savefig('KDE_location_PDF', bbox_inches = "tight", dpi=300)
        np.savetxt('KDE_location_PDF.csv', np.array(output_kde[0][0]))

    # run activity rate modeling
    lambdas = [None]
    if custom_rate != None and forecast_select:
        logger.info(f"Using activity rate specified by user: {custom_rate} per {time_unit}")
        lambdas = [custom_rate]
        lambdas_perc = [1]

    elif rate_select:
        logger.info(f"Activity rate modeling selected")

        time, mag_dummy, lat_dummy, lon_dummy, depth_dummy = read_mat_cat(catalog_file, output_datenum=True)    
        
        datenum_data = time # REMEMBER THE DECIMAL DENOTES DAYS
        
        if time_unit == 'hours':
            multiplicator = 24
        elif time_unit == 'days':
            multiplicator = 1
        elif time_unit == 'weeks':
            multiplicator = 1/7
        elif time_unit == 'years':
            multiplicator = 1/365

        # Selects dates in datenum format and procceeds to forecast value
        start_date = datenum_data[-1] - (2 * time_win_duration / multiplicator)
        dates_calc = [date for date in datenum_data if start_date <= date <= datenum_data[-1]]
        forecasts, bca_conf95, rate_mean = bootstrap_forecast_rolling(dates_calc, multiplicator)

        # FINAL VALUES OF RATE AND ITS UNCERTAINTY IN THE 5-95 PERCENTILE
        unc_bca05=[ci.low for ci in bca_conf95]; unc_bca95=[ci.high for ci in bca_conf95]
        rate_unc_high=multiplicator/np.array(unc_bca05); rate_unc_low=multiplicator/np.array(unc_bca95); 
        rate_forecast= multiplicator / np.median(forecasts) #[per time unit]

        # Plot of forecasted activity rate with previous binned activity rate
        act_rate, bin_counts, bin_edges, out, pprs, rt, idx, u_e = calc_bins(np.array(datenum_data), time_unit, time_win_duration, dates_calc, rate_forecast, rate_unc_high, rate_unc_low, multiplicator, quiet=True)

        # Assign probabilities 
        lambdas, lambdas_perc = lambda_probs(act_rate, dates_calc, bin_edges)

        #print("Forecasted activity rates: ", lambdas, "events per", time_unit[:-1])
        logger.info(f"Forecasted activity rates: {lambdas} events per {time_unit} with percentages {lambdas_perc}")
        np.savetxt('activity_rate.csv', np.vstack((lambdas, lambdas_perc)).T, header="lambda, percentage", delimiter=',', fmt='%1.4f')



    if forecast_select:
        products = products_string.split()
        logger.info(f"Ground motion forecasting selected with ground motion model {model} and IMT products {products_string}")

        if not xy_select:
            msg = "Event location distribution modeling was not selected; cannot continue..."
            logger.error(msg)
            raise Exception(msg)
        elif m_pdf[0] == None:
            msg = "Magnitude distribution modeling was not selected and magnitude PDF file was not provided; cannot continue..."
            logger.error(msg)
            raise Exception(msg)
        elif lambdas[0] == None:
            msg="Activity rate modeling was not selected and custom activity rate was not provided; cannot continue..."
            logger.error(msg)
            raise Exception(msg)

        Mag = 5.0 #placeholder mag, must be valid for that context; will be overwritten during function call
        rupture_aratio = 1.5
        Strike = 0
        Dip = 90
        Rake = 0

        p = 0.05     # Probability of exceedance

        m_cdf = get_cdf(m_pdf) 

        fxy=xy_kde[0]
        logger.debug(f"Normalization check; sum of all f(x,y) values = {np.sum(fxy)}")

        xx, yy = np.meshgrid(x_range, y_range, indexing='ij') # grid points

        # set every grid point to be a receiver
        x_rx = xx.flatten()
        y_rx = yy.flatten()

        # compute distance matrix for each receiver
        distances = np.zeros(shape=(nx*ny, nx, ny))
        rx_lat=np.zeros(nx*ny)
        rx_lon=np.zeros(nx*ny)

        for i in range(nx*ny):
            # Compute the squared distances directly using NumPy's vectorized operations
            squared_distances = (xx - x_rx[i])**2 + (yy - y_rx[i])**2  
            distances[i] = np.sqrt(squared_distances)

            # create context object for receiver and append to list
            rx_lat[i], rx_lon[i] = utm.to_latlon(x_rx[i], y_rx[i], utm_zone_number, utm_zone_letter) #get receiver location as lat,lon
  
        #experimental - compute ground motion only at grid points that have minimum probability density of thresh_fxy
        if exclude_low_fxy:
            indices = list(np.where(fxy.flatten() > thresh_fxy)[0])
        else:
            indices = range(0,len(distances))

        fr = fxy.flatten()
        
        #For each receiver compute estimated ground motion values
        logger.info(f"Estimating ground motion intensity at {len(indices)} grid points...")


        PGA = np.zeros(shape=(nx*ny))

        # use dask parallel computing
        start = timer()
        pbar = ProgressBar()
        pbar.register()
        #iter = range(0,len(distances))
        iter = indices
        iml_grid_raw = [] # raw ground motion grids
        for imt in products:
            logger.info(f"Estimating {imt}")
            
            imls = [dask.delayed(compute_IMT_exceedance)(rx_lat[i], rx_lon[i], distances[i].flatten(), fr, p, lambdas, forecast_len, lambdas_perc, m_range, m_pdf, m_cdf, model, log_level=logging.DEBUG, imt=imt, IMT_min = 0.0, IMT_max = 2.0, rx_label = i) for i in iter]
            iml = dask.compute(*imls)
            iml_grid_raw.append(list(iml))
        end = timer()
        logger.info(f"Ground motion exceedance computation time: {round(end - start, 1)} seconds")

        #create list of one empty list for each imt
        iml_grid = [ [] for _ in range(len(products)) ] # final ground motion grids
        iml_grid_prep = iml_grid.copy() # temp ground motion grids
        
        if exclude_low_fxy:
            for i in range(0,len(distances)):
                if i in indices:
                    for j in range(0,len(products)):    
                        iml_grid_prep[j].append(iml_grid_raw[j].pop(0))             
                else:
                    list(map(lambda lst: lst.append(np.nan), iml_grid_prep)) # use np.nan to indicate grid point excluded 
        else:
            iml_grid_prep = iml_grid_raw

        for j in range(0, len(products)):
            vmin = min(x for x in iml_grid_prep[j] if x is not np.nan)
            vmax = max(x for x in iml_grid_prep[j] if x is not np.nan)
            iml_grid[j] = np.reshape(iml_grid_prep[j], (nx, ny)).astype(dtype=np.float64)  # this reduces values to 8 decimal places
            iml_grid_tmp = np.nan_to_num(iml_grid[j]) # change nans to zeroes

            # upscale the grid
            up_factor = 4
            iml_grid_hd = resize(iml_grid_tmp, (up_factor*len(iml_grid_tmp), up_factor*len(iml_grid_tmp)), mode='reflect', anti_aliasing=False)
            iml_grid_hd[iml_grid_hd == 0.0] = np.nan # change zeroes back to nan

            # generate image overlay
            north, south = lat.max(), lat.min()  # Latitude range
            east, west = lon.max(), lon.min()  # Longitude range
            bounds = [[south, west], [north, east]]
            
            map_center = [np.mean([north, south]), np.mean([east, west])]
            
            # Create an image from the grid
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(iml_grid_hd, origin='lower', cmap='viridis')
            ax.axis('off')
            
            # Save the figure
            fig.canvas.draw()
            plt.savefig("overlay_" + str(j) + ".png", bbox_inches="tight", pad_inches=0, transparent=True)
            plt.close(fig)

            # Make the color bar
            cmap_name = 'viridis'
            width = 50
            height = 500
            
            gradient = np.linspace(0, 1, height)
            gradient = np.vstack((gradient, gradient)).T
            gradient = np.tile(gradient, (1, width))
            
            fig, ax = plt.subplots(figsize=((width + 40) / 100.0, (height + 20) / 100.0), dpi=100) # Increase fig size for labels
            ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(cmap_name), extent=[0, 1, vmin, vmax]) # Note: extent order is different for vertical
            ax.set_xticks([]) # Remove x-ticks for vertical colorbar
            num_ticks = 11 # Show more ticks
            tick_positions = np.linspace(vmin, vmax, num_ticks)
            ax.set_yticks(tick_positions)
            ax.set_yticklabels([f"{tick:.2f}" for tick in tick_positions])  #format tick labels       
            ax.set_title(imt, pad = 15) 
            fig.subplots_adjust(left=0.25, right=0.75, bottom=0.05, top=0.95) # Adjust Layout
            fig.savefig("colorbar_" + str(j) + ".png", bbox_inches='tight')
            plt.close(fig)