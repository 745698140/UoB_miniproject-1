"""
Run this for the folder containing all the DAVESON with [ ] to change 
it to JSON that can be seralized
"""
from os import listdir

def log(str):
    print(str)
    logs+= str+'\n'

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
folder_dir = '/home/charliepearce/UoB_miniproject/data/b_02/lob3/'
files = listdir(folder_dir)
logs= ''
log('dir '+folder_dir)

for file in files:
    if file.startswith('.') or not file.endswith('.txt'):
        log(file+' ignored')
        continue
    else:
        try:
            log('Parsing: '+file)
            file_in = open(folder_dir+file,'rt', encoding = 'us-ascii')
            file_out = open(folder_dir+file[:-4]+'.json','wt', encoding='us-ascii')
            file_working = file_in.read()
            file_in.close()
            processed_file = process_file(file_working)
            file_out.write(processed_file)
            file_out.close()
        except UnicodeDecodeError:
            log(f'Decoding error for {file}')
            log('Parsing with ignored errors: '+file)
            file_in = open(folder_dir+file,'rt', encoding = 'us-ascii', errors='ignore')
            file_out = open(folder_dir+file[:-4]+'.json','wt', encoding='us-ascii')
            file_working = file_in.read()
            file_in.close()
            processed_file = process_file(file_working)
            file_out.write(processed_file)
            file_out.close()
log('Job Done')

with open(folder_dir+'log.txt','wt') as log_file:
    log_file.write(str(logs))
    log_file.close()