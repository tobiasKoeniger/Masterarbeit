
# cd ~/Software/Masterarbeit; python3 start.py

import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('main.py', 'streamer.py')                                    
# processes = ('read_dht22.py', 'main.py', 'streamer.py')                                                             
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=2)                                                        
pool.map(run_process, processes)   
