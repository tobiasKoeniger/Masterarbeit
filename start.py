
# command to run file:
# cd ~/Software/Masterarbeit; python3 start.py

# Import multiprocessing libraries
import os                                                                       
from multiprocessing import Pool                                                
                                                                                
# Processes to run                                                                
processes = ('main.py', 'streamer.py')                                    
                  
# Function to run process
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
# Pool processes                                                                                
pool = Pool(processes=2)  

# Run processes                                                      
pool.map(run_process, processes)   
