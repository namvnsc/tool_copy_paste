import os

def count_file_contain_miss_block(folder='./output_v2'):
    string_dectect = r'%let datadate' # 'Please provide the'
    files = os.listdir(folder)
    miss_block_file = []
    for file in files:
        try:
            file_content = open(folder + '/' + file, mode='r', encoding='windows-1252').read()
            if string_dectect in file_content:
                miss_block_file.append(file)
                os.rename(folder + '/' + file, './miss_block_file/' + file)
        except Exception as e:
            print(file, str(e))
    print(len(miss_block_file))
    print('\t' + '\n\t'.join(miss_block_file))


count_file_contain_miss_block('./input')