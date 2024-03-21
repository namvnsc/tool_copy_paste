from os import walk
import shutil


def list_all_file(_type='.sas', folder=r'C:\Users\nnam1\Desktop\dev_tool\India_codes'): 
    res = []
    for (dir_path, dir_names, file_names) in walk(folder):
        for file in file_names:
            if file.lower().endswith(_type):
                res.append((file, dir_path))
    return res


py_files = list_all_file(_type='.py', folder=rf'C:\Users\nnam1\Desktop\dev_tool\done\SG_out')
sas_files = list_all_file(_type='.sas', folder=rf'C:\Users\nnam1\Desktop\dev_tool\input\origin_input\SG')

py_files_good = []
py_files_miss = []
for py_file in py_files:
    code = open(py_file[1] + '/' + py_file[0]).read()
    if 'Please provide the' in code:
        py_files_miss.append(py_file)
    else:
        py_files_good.append(py_file)


print(f'no sas: {len(sas_files)}  \nno py: {len(py_files)}\nno py good: {len(py_files_good)}')
# print(len(set(sas_files)), len(set(py_files)))


py_files_without_end = [e[0][:-3] for e in py_files_good]
sas_files_without_end = [e[0][:-4] for e in sas_files]
miss_match_file = []

for sas_file in sas_files:
    file_name_sas_without_end = sas_file[0][:-4]
    if (file_name_sas_without_end not in py_files_without_end):
        src = sas_file[1] + '/' + sas_file[0]
        dst = r'C:/Users/nnam1/Desktop/dev_tool/miss_input/SG/' + sas_file[0]
        shutil.copyfile(src, dst)
        # print(file_name_sas_without_end, src)
        miss_match_file.append(sas_file)

print(len(miss_match_file))