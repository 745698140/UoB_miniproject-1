"""
Run this for the folder containing all the DAVESON with [ ] to change 
it to JSON that can be seralized
"""
import os
import pandas as pd
import time
from duplicate_lobs import remove_dup_null
import json

logs= []

def log(str):
    print(str)
    logs.append(str)

def process_file(file):
    file_working = file.replace('\n','')
    file_working = file_working.replace(' ','')
    file_working = file_working.replace('["time",','{"time":')
    file_working = file_working.replace('["bid",','"bid":')
    file_working = file_working.replace('],["ask",',',"ask":')
    file_working = file_working.replace(']]]]',']]},')
    file_working = file_working.replace(']]]',']},')
    final_file = '['+file_working[:-1]+']'
    return final_file
    
# Put path to directory containing files here
if __name__ == "__main__":
    folder_dir = '../data/'
    files = os.listdir(folder_dir)
    log('dir '+folder_dir)

    for file in files:
        if file.startswith('.') or not file.endswith('.txt'):
            log(file+' ignored')
            continue
        else:
            tik = time.time()
            
            try:
                log('Parsing: '+file)
                file_in = open(folder_dir+file,'rt', encoding = 'us-ascii')
                
                file_working = file_in.read()
                file_in.close()
                parsed_file = process_file(file_working)
                processed_file = remove_dup_null(parsed_file)
                with open(folder_dir+file[:-4]+'.json','wt', encoding='us-ascii') as outfile:
                    json.dump(processed_file, outfile)
                    
            except UnicodeDecodeError:
                log(f'Decoding error for {file}')
                log('Parsing with ignored errors: '+file)
                file_in = open(folder_dir+file,'rt', encoding = 'us-ascii', errors='ignore')
                file_working = file_in.read()
                file_in.close()
                parsed_file = process_file(file_working)
                processed_file = remove_dup_null(parsed_file)
                with open(folder_dir+file[:-4]+'.json','wt', encoding='us-ascii') as outfile:
                    json.dump(processed_file, outfile)
            
            tok = time.time()
            print(f'{file} processed in {tok-tik}')
    log('Job Done')

    with open(folder_dir+'log.txt','wt') as log_file:
        log_file.write(str(logs))