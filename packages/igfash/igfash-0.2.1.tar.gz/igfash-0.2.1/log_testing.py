# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 16:04:46 2025

@author: ftong
"""
import logging
import igfash

if __name__ == '__main__':


    # Configuration
    # verbose = False
    verbose = True
    
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    logging.basicConfig(filename="logtest.log",
                        filemode='w',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    logger = logging.getLogger('igfash')
    logger.setLevel(log_level)
    
    # igfash.toy.fct1()
    # igfash.gm.fct1()
    
    igfash.gm.compute_IMT_exceedance(r=[1], model='Lasocki2013')
