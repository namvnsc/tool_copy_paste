from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pyperclip
import os
import sys
import logging
import undetected_chromedriver as uc
import sqlparse


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s - %(filename)-20s - %(funcName)-20s - %(lineno)-4d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class WebTool:
    def __init__(self, username_github='', password_github=''):
        self.url = "https://www.codeconvert.ai"
        self.driver = None
        self.username_github = username_github
        self.password_github = password_github

    def init_chrome_brower(self):
        try:
            if self.driver is None:
                logging.info('start chrome driver')
                options = uc.ChromeOptions()
                # options.add_argument("--headless=new")
                self.driver = webdriver.Chrome(options=options)
                self.driver.get("https://www.codeconvert.ai")
            else:
                logging.warning('chrome driver aleady start')
        except Exception as e:
            logging.error('fail to init chrome brower --> ', str(e))

    def close_chrome_brower(self):
        try:
            if self.driver != None:
                logging.info('close chrome driver')
                self.driver.quit()
                self.driver = None
        except Exception as e:
            logging.error('fail to close chrome brower --> ', str(e))



    def login(self):
        try:
            logging.info('login')
            button_login = self.driver.find_elements(By.CLASS_NAME, "button-28")[0]
            print(button_login)
            button_login.click()
            time.sleep(1) #wait to load login page
            button_signup_github = self.driver.find_elements(By.CLASS_NAME, "button-28")[2]
            button_signup_github.click()

            email_field = self.driver.find_element(By.ID, "login_field")
            email_field.clear()
            email_field.send_keys(self.username_github)

            pass_field = self.driver.find_element(By.ID, "password")
            pass_field.clear()
            pass_field.send_keys(self.password_github)
            button_sumit = self.driver.find_elements(By.CLASS_NAME, "js-sign-in-button")
            button_sumit[0].click()
            time.sleep(1)
            # try:
            #     auth_bth = self.driver.find_element(By.ID, "js-oauth-authorize-btn")
            #     auth_bth.click()
            # except Exception as e:
            #     logging.error(f'fail to click auth button on login --> {str(e)}')
        except Exception as e:
            logging.error('error login to convertcode.ai --> ' + str(e))


    def select_language(self):
        try:
            logging.info('select language')
            time.sleep(1)
            
            dropdowns = self.driver.find_elements(By.CLASS_NAME, "langselector_selectPanel__ZcvZA")
            while len(dropdowns) == 0:
                try:
                    dropdowns = self.driver.find_elements(By.CLASS_NAME, "langselector_selectPanel__ZcvZA")
                    self.driver.find_element(By.ID, "js-oauth-authorize-btn").click()
                except Exception as e:
                    time.sleep(1)
                    dropdowns = self.driver.find_elements(By.CLASS_NAME, "langselector_selectPanel__ZcvZA")
                    # logging.error(str(e)[:50])
            dropdowns = self. driver.find_elements(By.CLASS_NAME, "langselector_selectPanel__ZcvZA")
            select_language_source_dropdown = Select(dropdowns[0])
            select_language_source_dropdown.select_by_visible_text("Python")
            select_language_source_dropdown.select_by_visible_text("SAS")
            time.sleep(1)

            select_language_targett_dropdown = Select(dropdowns[1])
            select_language_targett_dropdown.select_by_visible_text("Python")
            # time.sleep(1)
        except Exception as e:
            logging.error('fail to select language -->', str(e))

    def start_session(self):
        try:
            self.close_chrome_brower() #try to stop all session
            self.init_chrome_brower()
            self.login()
            self.select_language()
        except Exception as e:
            logging.error('fail to create session  --> ', str(e))

    # def format_sql(self, block):
    #     sql_script = ''
    #     start = False
    #     for line in block:
    #         if 'select ' in line or start == True:
    #             start = True
    #             sql_script += '\n\t\t' + line.replace('^=', '!=')
    #             if ';' in line and not line.startswith('/*'):
    #                 break
    #     sql_script = sqlparse.format(sql_script, reindent=True).split('\n')
    #     sql_script = ['\t' + line for line in sql_script]
    #     sql_script = '\n'.join(sql_script)
    #     return sql_script

    def fix_syntax_error(self, py_code):
        try:
            start_n, start_nn = False, False
            start_ampersand = False
            #fix &
            py_code_remove = ''
            for i, e in enumerate(py_code):
                if e in (' ', '[', '(', '{', '\\'):
                    if start_nn == False and start_n == False:
                        start_ampersand = False
                    else:
                        if start_ampersand:
                            py_code_remove += '}'
                        start_ampersand = False
                    py_code_remove += e
                elif e == '"':
                    if start_nn == True:
                        start_nn = False
                        if start_ampersand:
                            py_code_remove += '}'
                        start_ampersand = False
                    else:
                        start_nn = True
                        if i > 2 and 'r' not in (py_code[i-1], py_code[i-2]):
                            py_code_remove += 'r'
                        if i > 2 and 'f' not in (py_code[i-1], py_code[i-2]):
                            py_code_remove += 'f'
                    py_code_remove += e
                    
                elif e == "'":
                    if start_n == True:
                        start_n = False
                        if start_ampersand:
                            py_code_remove += '}'
                        start_ampersand = False
                    else:
                        start_n = True
                        if i > 2 and 'r' not in (py_code[i-1], py_code[i-2]):
                            py_code_remove += 'r'
                        if i > 2 and 'f' not in (py_code[i-1], py_code[i-2]):
                            py_code_remove += 'f'
                    py_code_remove += e
                    
                elif e == "&":
                    start_ampersand = True
                    if start_n or start_nn:
                        py_code_remove += '{'
                    else:
                        if i > 0 and py_code[i-1] not in (' ', ')'):
                            py_code_remove += '_'
                        else:
                            if py_code[i+1] in (' ', '('):
                                py_code_remove += '&'
                        
                elif e == '.':
                    if start_ampersand:
                        if start_n or start_nn:
                            py_code_remove += '}'
                            start_ampersand = False
                        else:
                            pass
                    else:
                        py_code_remove += e
                else:
                    py_code_remove += e
                    
            #fix read_csv -> read_sas
            py_code = py_code_remove.split('\n')
            py_code_remove = ''
            for line in py_code:
                if 'read_csv' in line:
                    path = line.split('(')[1].split(')')[0]
                    if '.csv' not in path and '.txt' not in path:
                        line = line.split(' = ') [0]+ f' = read_sas({path})'
                py_code_remove += line + '\n'
                    

            # fix path has .
            py_code = py_code_remove.split('\n')
            py_code_remove = ''
            for line in py_code:
                if 'read_sas' in line:
                    path = line.split('(')[1].split(')')[0]
                    if '.sas7bdat' not in path and len(path.split('.')) > 1:
                        py_code_remove += '#' + line + '\n'
                        path = path.replace('"', "'")
                        path = path.split('.')[0].split("'")[1] + " + rf'\\\\" + path.split('.')[1][:-1] + ".sas7bdat'"
                        line = line.split(' = ') [0]+ f' = read_sas({path})'
                py_code_remove += line + '\n'

            #remove rsubmit, sumbit
            py_code = py_code_remove.split('\n')
            py_code_remove = ''
            for line in py_code:
                if line.lower().startswith('rsubmit') or line.lower().startswith('endrsubmit'):
                    py_code_remove += '#' + line + '\n'    
                else:
                    py_code_remove += line + '\n'
            
            return py_code_remove
        except Exception as e:
            logging.error(str(e))
            logging.info(py_code)
            return None




    def convert_block(self, block):
        num_retry = 0
        while True:
            input_field = self.driver.find_element(By.CLASS_NAME, "ace_text-input")
            input_field.send_keys(Keys.CONTROL + 'a')
            input_field.send_keys(Keys.DELETE)


            sas = '\n'.join([e for e in block if not e.lower().startswith('format') and not e.lower().startswith('informat')])
            if len(sas) > 18500:
                logging.info('sas block too large here')
                return '# block large'
            if sas.endswith(')'):
                logging.info('\n'.join(block)[:1000])

            input_field.send_keys(sas)  # paste sas code to web
            time.sleep(len(sas)/5000)
            time.sleep(0.1*num_retry)
            num_retry += 1
            if num_retry > 20:
                return '# retry 20 time and fail'
            button_convert = self.driver.find_element(By.ID, "convert-btn")
            button_convert.click()
            time_wait = 0
            while button_convert.text == 'Please wait': # wait tool convert
                time.sleep(0.5)
                time_wait += 0.5
                if time_wait > 300:
                    return '# wait too long'
            time.sleep(1)
            button_copy = self.driver.find_element(By.CLASS_NAME, "overlay-copy-button")
            button_copy.click() # copy python code to clip board
            time.sleep(0.5)
            button_copy = self.driver.find_element(By.CLASS_NAME, "overlay-copy-button")
            button_copy.click() # copy python code to clip board
            time.sleep(0.5)
            button_copy = self.driver.find_element(By.CLASS_NAME, "overlay-copy-button")
            button_copy.click() # copy python code to clip board
            time.sleep(0.5)
            button_copy = self.driver.find_element(By.CLASS_NAME, "overlay-copy-button")
            button_copy.click() # copy python code to clip board
            time.sleep(0.5)
            block_python_code = pyperclip.paste().replace('\r', '')
            block_python_code = pyperclip.paste().replace('\r', '')
            # time.sleep(1)

            if not block_python_code.startswith('Please provide') and block_python_code.strip() != '' \
                and ('code translation here' not in block_python_code)\
                and ('code translation goes here' not in block_python_code):
                time.sleep(2)
                block_python_code = self.fix_syntax_error(block_python_code)
                return block_python_code
            else:
                logging.warning('retry convert')
                # self.select_language()
                time.sleep(1)

    def convert_code(self, blocks):
        try:
            python_code = ''
        
            for i, block in enumerate(blocks):
                print(f'\r\t\t\t\tconverting {(i+1)} / {len(blocks)} blocks', end='')
                try:
                    block_python_code = self.convert_block(block)
                    # logging.info('\n'.join(block))
                    # logging.info(block_python_code)
                    # logging.info('_'*70)
                    if block_python_code in ['# retry 20 time and fail', '# wait too long', '# block large'] or block_python_code is None:
                        logging.error(block_python_code)
                        return '', -1
                    if block[0].lower().startswith('proc sql'):
                        
                        _sql = sqlparse.format('\n'.join(block), reindent=True).split('\n')
                        sas_cm = ['\t\t' + line for line in _sql[:-1]] + ['\t' + _sql[-1]]
                        sas_cm = '\n'.join(sas_cm)
                        sas_cm = sas_cm.replace('\t\tproc', '\tproc').replace('\t\tPROC', '\tPROC').replace('\t\tProc', '\tProc')
                    else:
                        sas_cm = "\n\t\t".join(block[:-1])
                        sas_cm += '\n\t' + block[-1]
                    sas_cm = sas_cm.replace('\t\trun', '\trun').replace('\t\tRun', '\tRun').replace('\t\tRUN', '\tRUN')\
                                    .replace(r'\t\t%let', r'\t%let')\
                                    .replace('\t\tLibname', '\tLibname').replace('\t\tlibname', '\tlibname').replace('\t\tLIBNAME', '\tLIBNAME')

                    block_python_code = f'\n\n"""\n\tBLOCK {i + 1}:\n\n' + \
                                        '\t' + sas_cm + '\n"""\n\n' + \
                                        block_python_code 
                    
                    python_code += block_python_code
                except Exception as e:
                    logging.error(str(e))
                    logging.error('\n'.join(block)[:1000])
                    return '', 0
            print('')
            return python_code, 1
        except Exception as e:
            logging.error(str(e))
            return '', 0 

class SasCodeReader:
    def __init__(self, path_to_sascode='') -> None:
        self.path_to_sascode = path_to_sascode
        self.sascode = ''
        self.blocks_sascode = []
        self.loc = 0
        self.no_block = 0

    def get_blocks_code(self):
        self.read_and_clean_code()
        self.split_to_block()
        return self.blocks_sascode, len(self.sascode), len(self.blocks_sascode)

    def read_and_clean_code(self):
        try:
            # try:
            #     logging.info(f'read sas: {self.path_to_sascode}')
            #     self.sascode = open(self.path_to_sascode, mode='r').readlines()
            # except Exception as e:
            #     logging.info('fail to read try with encoding win')
            #     self.sascode = open(self.path_to_sascode, mode='r', encoding='windows-1252').readlines()
                
            
            # self.sascode = [line.replace('\n', ' ')\
            #                     .replace('\t', ' ')\
            #                     .strip()
            #                         for line in self.sascode]
            # self.sascode = [   line for line in self.sascode \
            #                             if ((line.strip() != '' ) and (not line.startswith('/*') and not line.endswith('*/')))] #remove empty line and comment line /*  ... */
            
            # try:
            try:
                logging.info(f'read sas: {self.path_to_sascode}')
                content = open(self.path_to_sascode, mode='r').readlines()
            except Exception as e:
                logging.warning('fail on utf-8, try with encoding win')
                content = open(self.path_to_sascode, mode='r', encoding='windows-1252').readlines()
                
            content = '$$$$$'.join(content).replace('\n', ' ').replace('\t', ' ')
            
            clean_content = ''
            start_comment = False
            for i in range(len(content) - 1):
                if start_comment == True:
                    if content[i-1 : i+1] == '*/':
                        start_comment = False
                    else:
                        continue
                else:
                    if content[i:i+2] == '/*':
                        start_comment = True
                    else:
                        clean_content += content[i]
                        
            for i in range(100):
                clean_content = clean_content.replace('  ', ' ')
            clean_content = clean_content.replace("$$$$$", ' ').split(';')
    
            self.sascode = [line.strip() + ';' for line in clean_content if (line.strip() != '' )]
            
        except Exception as e:
            logging.error('fail to read from ' + self.path_to_sascode, str(e))
        except Exception as e:
            logging.error('fail to read from ' + self.path_to_sascode, str(e))


    def split_to_block(self):
        self.blocks_sascode = []
        lines = []
        start_macro = False
        
        for line in self.sascode:
            if start_macro == True:
                if line.lower().startswith('%mend'):
                    lines.append(line)
                    self.blocks_sascode.append(lines)
                    lines = []
                    start_macro = False
                else:
                    lines.append(line)
            else:
                if (line.startswith('proc ') | line.startswith('data ') 
                    | line.startswith('PROC ') | line.startswith('DATA ')
                    | line.startswith('Proc ') | line.startswith('Data ')
                    | line.lower().startswith('%macro')):
                    
                    self.blocks_sascode.append(lines)
                    lines = [line]
                    if line.lower().startswith('%macro'):
                        start_macro = True
                else:
                    lines.append(line)
        
        self.blocks_sascode.append(lines)
        self.blocks_sascode = [e for e in self.blocks_sascode if len(e) > 0]

class Converter:
    def __init__(self, input_folder, output_folder, 
                        username_github, password_github) -> None:
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.username_github = username_github
        self.password_github = password_github
        self.webtool = WebTool(username_github, password_github)
    
    def process(self, input_path = '', output_path=''):
        def write_code(python_code, full_path):
            logging.info(f'write file on {full_path}')
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
        try:
            start_time = time.time()

            sasreader = SasCodeReader(input_path)
            blocks, loc, nob = sasreader.get_blocks_code()
            max_len_block = max([len('\n'.join(bl)) for bl in blocks ])
            if max_len_block > 19000:
                logging.info(f'this file contain large blocks: {max_len_block} character -------------> please convert it manually')
                return
            logging.info(f'file contain: {loc} LoC, {nob} blocks')
            
            while True:
                python_code, status = self.webtool.convert_code(blocks)
                if status == 0:
                    self.webtool = WebTool(self.username_github, self.password_github)
                    self.webtool.start_session()
                elif status == 1:
                    write_code(python_code, output_path)
                    end_time = time.time()
                    logging.info(f'done, time convert: {(end_time - start_time) // 60} min')
                    break
                else:
                    logging.info(f'fail to convert {input_path}, ---> please convert it manually')
                    break

        except Exception as e:
            logging.error(f'fail on process {input_path}   ---> ex: {str(e)}')
        


    def run(self):

        list_file_need_convert = []
        for (dir_path, dir_names, file_names) in os.walk(self.input_folder):
            for file in file_names:
                if file.lower().endswith('.sas') or file.lower().endswith('.txt'):
                    
                    sas_file_path = dir_path + '/' + file
                    py_file_path = dir_path.replace(self.input_folder, self.output_folder) +'/'+ file[:-4] + '.py'

                    if not os.path.exists(py_file_path):
                        file_stats = os.stat(sas_file_path)
                        list_file_need_convert.append((sas_file_path, py_file_path, file_stats.st_size / 1024))
                        
        list_file_need_convert = sorted(list_file_need_convert, key=lambda f: f[2]) 
        logging.info(f'total {len(list_file_need_convert)} sas need convert')
        
        self.webtool.start_session()
        i = 0
        for sas_in, py_out, size in list_file_need_convert:
            logging.info(f'convert {i + 1} / {len(list_file_need_convert)} file')
            i += 1
            self.process(sas_in, py_out)



import json
username, password, input_folder, output_folder = sys.argv[1:]
logging.info(json.dumps({
    'username' : username, 
    'password' : password, 
    'input_folder' : input_folder, 
    'output_folder' : output_folder
}, indent=4))

convert = Converter(input_folder, output_folder, username, password)

convert.run()
