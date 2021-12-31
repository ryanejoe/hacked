
from cryptography.fernet import Fernet
import socket
import subprocess
import sys
import os 
from datetime import datetime
from colorama import Fore, Back, Style
import csv
from email.message import EmailMessage
import smtplib
import pyfiglet
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
    print (Fore.YELLOW,"Please wait, scanning remote host", remoteServerIP)
    print ("-" * 60)
    t1 = datetime.now()
    try:
        for port in range(1,1025):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print (Fore.LIGHTGREEN_EX,"Port {}: 	 Open".format(port))
    except KeyboardInterrupt:
        print (Fore.RED,"You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print (Fore.Red,'Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print (Fore.RED,"Couldn't connect to server")
        sys.exit()
    t2 = datetime.now()
    total =  t2 - t1
    print (Fore.YELLOW,'Scanning Completed in: ', total)
def sherlock():
    print(Fore.YELLOW,"making sure that sherlock is installed..."  )
    if os.path.isfile('sherlock') == True:
        usr_name= input(Fore.LIGHTGREEN_EX,"enter username you want to search: ")
        subprocess.call('sherlock ' , usr_name, shell = True)
    elif os.path.isfile('sherlock') == False:
        print(Fore.LIGHTGREEN_EX,"downloading sherlock...")
        subprocess.call('git clone https://github.com/sherlock-project/sherlock.git', shell = True)
        subprocess.call('cd sherlock', shell = True)
        print(Fore.LIGHTGREEN_EX,"installing required libraries...")
        subprocess.call('pip install -r requirements.txt', shell = True)
        usr_name= input("enter username you want to search: ")
        subprocess.call('sherlock ' + usr_name, shell = True)
    else:
        print("error")
def bulk_email():
    print(Fore.LIGHTGREEN_EX, "-")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    email_address = input("enter sender email: ")
    email_pass = input("enter password:")
    print(Fore.LIGHTGREEN_EX, "-")
    s.ehlo()
    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    print(Fore.YELLOW, "--------------")
    print(Fore.YELLOW,"logged in...")
    print(Fore.YELLOW, "--------------")
    # message to be sent
    print(Fore.LIGHTGREEN_EX, "-")
    subject = input("enter subject: ")
    body = input("""enter your body:""")
    

    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    emails = input("enter filename or path to emails csv file:")
    print(Fore.LIGHTGREEN_EX, "-")
    with open(emails, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for email in spamreader:
            s.send_message(message,email_address, email[0])
            print("Send To " + email[0])
    s.quit()
        # terminating the session
       
    print(Fore.YELLOW, "--------------")
    print("sent")
    print(Fore.YELLOW, "--------------")
def mac_changer():
    print(Fore.LIGHTGREEN_EX,'[-] Please enter a valid MAC Address')
    new_mac = input("enter new mac address: ")
    interface = input("enter interface name: ")
    print('\n[+] Changing the MAC Address to', new_mac)
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])

while True:
    print(Fore.LIGHTGREEN_EX, "1. file encryption/decryption")
    print(Fore.LIGHTGREEN_EX, "2. sherlock")
    print(Fore.LIGHTGREEN_EX, "3.port scanner")
    print(Fore.LIGHTGREEN_EX, "4. mass emailer")
    print(Fore.LIGHTGREEN_EX, "5.mac changer")
    print(Fore.LIGHTRED_EX,"input exit to exit")
    print(Fore.LIGHTGREEN_EX,"-")
    inpt=input("enter choice:")
    if inpt == "1":
        encryption_fernet()
    elif inpt == "2":
        sherlock()
    elif inpt == "3":
        port_scanner()
    elif inpt == "4":
        bulk_email()
    elif inpt == "5":
        mac_changer()
    elif inpt == "exit":
        print(Fore.LIGHTRED_EX, "cya!")
        break
    else:
        print(Fore.LIGHTRED_EX, "error")