import sys, os, time
from datetime import datetime

# Install required packages
print('Checking required packages ...')
sys.path.append(os.path.dirname(__file__))
os.popen('python -m pip install wheel pytz gitpython').read()
sys.path.remove(os.path.dirname(__file__))
time.sleep(10)

import pytz
import git

def current_time() -> str:
    local_tz = pytz.timezone('Asia/Jerusalem')
    date = datetime.now().astimezone(tz=local_tz).strftime("%d/%m/%Y %H:%M:%S")
    return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")

def setup_env() -> list : 
    '''Setup the environment for the app to run'''
    print(f'This is a repository installer, follow the next steps ...')
    print('[1] Repositories will clone under "c:/" directory ...')

    repos_lst = []
    clone = True
    while clone:
        REPO_URL = input(f"\n(Press ENTER to skip) Which repo to clone? (Ex.: https://github.com/eyal360/<APP_NAME>.git)")
        INSTALLATION_FOLDER_PATH = os.path.join(os.path.join("c:/", REPO_URL.split('/')[-1].split('.')[0]))
        repos_lst.append(INSTALLATION_FOLDER_PATH)

        if not os.path.exists(INSTALLATION_FOLDER_PATH):
            print(f'[-] Creating installation directory "{INSTALLATION_FOLDER_PATH}" ...')
            git.Git(working_dir=os.path.dirname(INSTALLATION_FOLDER_PATH)).clone(REPO_URL)

            MAIN_FILE_PATH = os.path.join(INSTALLATION_FOLDER_PATH,input(f"\nWhat is the name of the main file? ({os.listdir(INSTALLATION_FOLDER_PATH)})"))
            run_startup = input(f"\nRun it on startup? (y/n)")
            if 'y' in run_startup:
                # Create startup BAT file
                print(f'[-] Creating BAT file to run {MAIN_FILE_PATH.split("/")[-1]} on startup...')
                BAT_FILE_PATH = os.path.join(os.path.expanduser( '~' ), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup", f"startup_bot_{MAIN_FILE_PATH.split('/')[-1].split('.')[0]}.bat")
                file = open(BAT_FILE_PATH,'w+')
                file.write('@echo off\n')
                file.write(f'python {MAIN_FILE_PATH}')
                file.close()
        
        else:
            print(f'[-] "{INSTALLATION_FOLDER_PATH}" already exists, skipping ...')

        clone = True if 'y' in input(f"\nAnother repo to clone? (y/n)") else False        
    
    return repos_lst

if __name__ == '__main__':
    
    repos_lst = setup_env()
    for repo in repos_lst:
        print(f'[#] "{repo}" Repository installed successfully!')