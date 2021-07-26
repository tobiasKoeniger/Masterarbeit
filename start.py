import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('read_dht22.py', 'main.py', 'read_ec_level.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)   
