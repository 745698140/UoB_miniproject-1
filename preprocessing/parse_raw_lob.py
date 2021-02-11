"""
Run this for the folder containing all the DAVESON with [ ] to change 
it to JSON that can be seralized
"""
from os import listdir

# Put path to directory containing files here
folder_dir = './test/'
files = listdir(folder_dir)

for file in files:
    if file.startswith('.'):
        print(file+' ignored')
        continue
    else:
        print('parsing '+file)
        file_in = open(folder_dir+file,'rt')
        file_out = open(folder_dir+file[:-4]+'.json','wt')
        file_working = file_in.read()
        file_in.close()
        file_working = file_in.replace('\n','')
        file_working = file_in.replace(' ','')
        file_working = file_in.replace('["time",','{"time":')
        file_working = file_in.replace('["bid",','"bid":')
        file_working = file_in.replace('],["ask",',',"ask":')
        file_working = file_in.replace(']]]]',']]},')
        file_working = file_in.replace(']]]',']},')
        final_file = '['+file_working[:-1]+']'
        file_out.write(final_file)
        file_out.close()
print('Job Done')
