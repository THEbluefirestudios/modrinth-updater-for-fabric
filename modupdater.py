import hashlib
import os
import requests
from pyfiglet import Figlet as fig
from colorama import Fore as col

username = os.environ.get('USERNAME')
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

f1 = fig(font='ansi_shadow')

print(col.WHITE+'='*75)
print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
print(col.WHITE+'='*75)
MODS_FOLDER = f'C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\mods'
print(col.RED+ '[ ! ] WARNING, THIS SCRIPT IS ONLY FOR THE FABRIC MOD LOADER')
MC_VERSION = str(input(col.WHITE+'\nEnter your current Minecraft version: '))
LOADER = 'fabric'





def get_file_hash(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def update_mods():
    if not os.path.exists(MODS_FOLDER):
        clear_screen()
        print(col.WHITE+'='*75)
        print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
        print(col.WHITE+'='*75)
        print(col.RED+f"\n[ !! ] Error: Folder {MODS_FOLDER} not found.\n")
        print(col.WHITE+'='*75)
        return
    clear_screen()
    print(col.WHITE+'='*75)
    print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
    print(col.WHITE+'='*75)
    print(col.CYAN+f"\n[ i ] Checking for update Minecraft Versiom{MC_VERSION}, Mod Loader {LOADER}\n")    
    print(col.WHITE+'='*75)
    all_mods = [f for f in os.listdir(MODS_FOLDER) if f.endswith(".jar")]
    global mod_no
    mod_no = len(all_mods)
    inspected_mods = 0
    
    for filename in os.listdir(MODS_FOLDER):
        prog_str = '▒'*int(inspected_mods*75/mod_no) + '░'*int(75 - inspected_mods*75/mod_no)
        if not filename.endswith(".jar"):
            continue
            
        path = os.path.join(MODS_FOLDER, filename)
        file_hash = get_file_hash(path)
        lookup_url = f"https://api.modrinth.com/v2/version_file/{file_hash}"
        response = requests.get(lookup_url)
        
        if response.status_code != 200:
            clear_screen()
            print(col.WHITE+'='*75)
            print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
            print(col.WHITE+'='*75)
            print(col.YELLOW+f"\n[ i ] Skipping {filename} as it is not available on Modrinth\n")
            inspected_mods += 1
            print(col.BLUE + '\n',prog_str, ' ', inspected_mods,'/', mod_no,'\n')
            print(col.WHITE+'='*75)
            continue
            
        current_version_data = response.json()
        project_id = current_version_data['project_id']
        versions_url = f"https://api.modrinth.com/v2/project/{project_id}/version"
        params = {
            "loaders": f'["{LOADER}"]',
            "game_versions": f'["{MC_VERSION}"]',
            "version_type": "release"
        }
        v_response = requests.get(versions_url, params=params)
        
        if v_response.status_code == 200 and v_response.json():
            latest_version = v_response.json()[0] 
            latest_file = latest_version['files'][0]
            
            if latest_file['hashes']['sha1'] != file_hash:
                clear_screen()
                print(col.WHITE+'='*75)
                print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
                print(col.WHITE+'='*75)
                print(col.CYAN+f"\n[ i ] Updating {filename} to {MC_VERSION} Release\n")
                inspected_mods += 1
                print(col.BLUE + '\n',prog_str, ' ', inspected_mods,'/', mod_no,'\n')
                
                print(col.WHITE+'='*75)
                

                new_file_data = requests.get(latest_file['url']).content
                with open(os.path.join(MODS_FOLDER, latest_file['filename']), "wb") as f:
                    f.write(new_file_data)
                
              
                os.remove(path)
            else:
                clear_screen()
                print(col.WHITE+'='*75)
                print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
                print(col.WHITE+'='*75)
                print(col.YELLOW+f"[ ! ] {filename} is already up to date.")
                inspected_mods += 1
                print(col.BLUE + '\n',prog_str, ' ', inspected_mods,'/', mod_no,'\n')
                print(col.WHITE+'='*75)
    



update_mods()
clear_screen()
print(col.WHITE+'='*75)
print(col.GREEN+f1.renderText('MODRINTH UPDATER'))
print(col.WHITE+'='*75)
print(col.GREEN+"[ i ] Done! Press Enter to close.\n")
print('▒'*75+' '+str(mod_no)+'/'+str(mod_no)+'\n')
print(col.WHITE+'='*75)
input()
