"""
Run this for the folder containing all the DAVESON with [ ] to change 
it to JSON that can be seralized
"""
import time
import json
import s3fs

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
    s3_bucket = 's3://uob-miniproject/b_02/'
    s3 = s3fs.S3FileSystem(anon=False)
    files = s3.ls(s3_bucket+'raw/')
    log('dir '+s3_bucket)

    for file in files:
        # Check if file is .txt
        if file.startswith('.') or not file.endswith('.txt'):
            log(file+' ignored')
            continue
        else:
            tik = time.time()
            try:
                log('Parsing: '+file)
                with s3.open(file,'rt', encoding = 'us-ascii') as file_in:
                    file_working = file_in.read()

                parsed_file = process_file(file_working)
                log(f'{file} parsed, dumping to file')

                with s3.open(file[:-4]+'.json','wt', encoding='us-ascii') as outfile:
                    json.dump(parsed_file, outfile)
                    
            except UnicodeDecodeError:
                log(f'Decoding error for {file}')
                log('Parsing with ignored errors: '+file)
                with s3.open(file,'rt', encoding = 'us-ascii', errors = 'ignore') as file_in:
                    file_working = file_in.read()

                parsed_file = process_file(file_working)
                log(f'{file} parsed, dumping to file')

                with s3.open(file[:-4]+'.json','w', encoding='us-ascii') as outfile:
                    json.dump(parsed_file, outfile)
            
            tok = time.time()
            print(f'{file} processed in {tok-tik}')
    log('Job Done')

    with open('s3://uob-miniproject/b_02/'+'log.txt','wt') as log_file:
        log_file.write(str(logs))