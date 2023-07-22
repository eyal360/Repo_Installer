import sys, os, time
from datetime import datetime

# Install required packages
print('Checking required packages ...')
sys.path.append(os.path.dirname(__file__))
os.popen('python -m pip install wheel pytz colorama gitpython').read()
sys.path.remove(os.path.dirname(__file__))
time.sleep(10)

import pytz
import git
import colorama
from colorama import Fore, Back, Style

def current_time() -> str:
    local_tz = pytz.timezone('Asia/Jerusalem')
    date = datetime.now().astimezone(tz=local_tz).strftime("%d/%m/%Y %H:%M:%S")
    return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")

def setup_env() -> list : 
    '''Setup the environment for the app to run'''
    print(f'\nThis is a repository Installer / Updater')
    print('    [+] Repositories will clone under "c:/" directory ...')
    print('    [+] Exisiting repositories will be updated')

    repos_lst = []
    clone = True
    while clone:
        local_repos = [folder for folder in os.listdir('c:/') if os.path.isdir(os.path.join('c:/', folder, '.git'))]
        if local_repos != []:
            print(f'\n[!] Found These Local Repositories:')
            for repo in local_repos:
                print(f'    [+] {repo}')

        REPO_URL = input(f"\nEnter Repository (https://github...git OR any local repo)\n")
        # Checking if the user entered a local repo or a github repo
        REPO_URL = f'https://github.com/eyal360/{REPO_URL}.git' if 'https' not in REPO_URL else REPO_URL
        INSTALLATION_FOLDER_PATH = os.path.join(os.path.join("c:/", REPO_URL.split('/')[-1].split('.')[0]))

        if not os.path.exists(INSTALLATION_FOLDER_PATH):
            print(f'    [+] Creating installation directory "{INSTALLATION_FOLDER_PATH}" ...')
            try:
                git.Git(working_dir=os.path.dirname(INSTALLATION_FOLDER_PATH)).clone(REPO_URL)
            except:
                print(Fore.RED + f'    [!] Failed to find "{REPO_URL}", check the URL' + Style.RESET_ALL)
                continue

            run_startup = input(f'[?] Run "{INSTALLATION_FOLDER_PATH}" on startup? (y/n) ')
            if 'y' in run_startup:
                # Get main file path
                checking_main_file = True
                while checking_main_file:
                    main_file = input(f"[?] What is the name of the main file? {os.listdir(INSTALLATION_FOLDER_PATH)}")
                    if main_file in os.listdir(INSTALLATION_FOLDER_PATH):
                        MAIN_FILE_PATH = os.path.join(INSTALLATION_FOLDER_PATH, main_file)
                        checking_main_file = False

                # Create startup BAT file
                print(f'    [+] Creating BAT file to run {MAIN_FILE_PATH} on startup...')
                BAT_FILE_PATH = os.path.join(os.path.expanduser( '~' ), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup", f"startup_run_{REPO_URL.split('/')[-1].split('.')[0]}.bat")
                file = open(BAT_FILE_PATH,'w+')
                file.write('@echo off\n')
                file.write(f'python {MAIN_FILE_PATH}')
                file.close()

        else:
            print(f'    [+] Pulling latest changes from "{INSTALLATION_FOLDER_PATH}" ...')
            local_repo = git.Repo(path=os.path.join(INSTALLATION_FOLDER_PATH, ".git"))
            local_repo.remotes.origin.pull()


        repos_lst.append(INSTALLATION_FOLDER_PATH)      
        clone = True if 'y' in input(f"\nAnother Repository to install? (y/n) ") else False        
    
    return repos_lst

if __name__ == '__main__':
    
    repos_lst = setup_env()
    
    print(Fore.GREEN + f'\nThese Repositories was pulled successfully:' + Style.RESET_ALL)
    for idx, repo in enumerate(repos_lst):
        print(f'    [{idx+1}] "{repo}"')

    print('Exiting in 10 seconds ...')
    time.sleep(10)