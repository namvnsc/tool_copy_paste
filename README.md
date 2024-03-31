
1. Clone the project from the repository.
2. Create a .env file in the project folder and define 2 variables as follows in the .env file, then enter your account after the '=' sign:
    - GMAIL_GITHUB=
    - PASSWORD=
3. Create two folders named **"input"** and **"output"** in the project folder, then place the .sas file(s) into the "input" folder.
4. Open the Anaconda prompt and navigate to the project folder, then execute:
    - pip install -r requirements.txt
    - python tool_copy_paste.py ./input ./output
    
