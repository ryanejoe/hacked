from cryptography.fernet import Fernet
import socket
import subprocess
import sys
import os 
from datetime import datetime

def encryption_fernet():
    decrpt_or_encrpt = input("do you want to decrypt or encrypt the file(e/d):")
    if decrpt_or_encrpt == "e":
        file_name = input("enter path or file name:")
        key = Fernet.generate_key()
        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open(file_name, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    elif decrpt_or_encrpt == "d":
        file_name = input("enter path or file name:")
        key = input("Enter key:")
        fernet = Fernet(key)
        with open(file_name, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)

        with open(file_name, 'wb') as dec_file:
            dec_file.write(decrypted)
def port_scanner():
    subprocess.call('clear', shell=True)
    remoteServer    = input("Enter a remote host to scan: ")
    remoteServerIP  = socket.gethostbyname(remoteServer)
    print ("-" * 60)
    print ("Please wait, scanning remote host", remoteServerIP)
    print ("-" * 60)
    t1 = datetime.now()
    try:
        for port in range(1,1025):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print ("Port {}: 	 Open".format(port))
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print ("Couldn't connect to server")
        sys.exit()
    t2 = datetime.now()
    total =  t2 - t1
    print ('Scanning Completed in: ', total)
def sherlock():
    print("making sure that sherlock is installed...")
    if os.path.isfile('sherlock') == True:
        usr_name= input("enter username you want to search: ")
        subprocess.call('sherlock ' , usr_name, shell = True)
    elif os.path.isfile('sherlock') == False:
        print("downloading sherlock...")
        subprocess.call('git clone https://github.com/sherlock-project/sherlock.git', shell = True)
        subprocess.call('cd sherlock', shell = True)
        print("installing required libraries...")
        subprocess.call('pip install -r requirements.txt', shell = True)
        usr_name= input("enter username you want to search: ")
        subprocess.call('sherlock ' + usr_name, shell = True)
    else:
        print("error")
sherlock()