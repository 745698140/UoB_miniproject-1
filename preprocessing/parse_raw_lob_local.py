"""
Run this for the folder containing all the DAVESON with [ ] to change 
it to JSON that can be seralized
"""
import time
import json
import os

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
    file_working = '['+file_working[:-1]+']'
    print(len(file_working))
    #print((file_working[153471509:153474666]))
    #file_working = file_working[:153471509]+file_working[153474664:]
    file_working = remove_dup_null(file_working)
    return file_working

def remove_dup_null(string_in):
    print('Removing duplicate lobs and null vals')

    j_son = json.loads(string_in)
    processed_json = []
    for i, lob in enumerate(j_son):
        if (lob['ask'] == j_son[i-1]['ask'] and lob['bid'] == j_son[i-1]['bid']) \
        or not lob['ask'] or not lob['bid']:
            continue
        else:
            processed_json.append(lob)
    return processed_json
    
# Put path to directory containing files here
if __name__ == "__main__":
    dir = './'
    log('dir '+dir)
    files = os.listdir(dir)

    for file in files:
        # Check if file is .txt
        if file.startswith('.') or not file.endswith('.txt'):
            log(file+' ignored')
            continue
        else:
            tik = time.time()
            try:
                log('Parsing: '+file)
                with open(dir+file,'rt', encoding = 'ISO-8859-1') as file_in:
                    file_working = file_in.read()
                    
                parsed_file = process_file(file_working)
                log(f'{file} parsed, dumping to file')

                with open(dir+file[:-4]+'.json','wt', encoding='utf8') as outfile:
                    json.dump(parsed_file, outfile)
                    
            except UnicodeDecodeError:
                log(f'Decoding error for {file}')
                log('Parsing with ignored errors: '+file)
                with open(dir+file,'rt', encoding = 'us-ascii', errors = 'ignore') as file_in:
                    file_working = file_in.read()

                parsed_file = process_file(file_working)
                log(f'{file} parsed, dumping to file')

                with open(dir+file[:-4]+'.json','w') as outfile:
                    json.dump(parsed_file, outfile, ensure_ascii=True)
            
            tok = time.time()
            print(f'{file} processed in {tok-tik}')
    log('Job Done')
"""
    with open(dir+'log.txt','wt') as log_file:
        log_file.write(str(logs))
"""