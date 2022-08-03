import dns.resolver
import subprocess
import os
import re
#NS = dns.resolver.resolve(domain, 'NS')
NSlist = []
Domainlist = []
with open ('DomainList.txt' , 'r') as dominios:
	for dominio in dominios:
		Domainlist.append(dominio)

for dominio in Domainlist:
	dominio = dominio[:-1]
	#print (dominio)
	try:	
		NS = dns.resolver.resolve(dominio, 'NS')
		for answer in NS.response.answer:
			for item in answer.items:
				NSlist.append(item.to_text())
	except:
		continue

Arecords = []
AAAArecords = []
for nsrecord in NSlist:
	   nsrecord = nsrecord[:-1]
	   try:
	   	teste = subprocess.check_output(["nslookup", nsrecord])
	   	first, *middle, last = teste.split()
	   	try:
	   		AAAArecords.append(last.decode("utf-8"))
	   		Arecords.append(middle[8].decode("utf-8"))
	   	except:
	   		Arecords.append(last.decode("utf-8"))
	   except:
	   	continue	

#print ("NS RECORDS:")
#print (NSlist)
#print ("A RECORDS:")
#print (Arecords)

with open ('IpList.txt', 'w') as file:
	file.write("begin \n")
	for ip in Arecords:
		file.write(ip)
		file.write("\n")
	for ip in AAAArecords:
		file.write(ip)
		file.write("\n")
	file.write("end")	

comand = "netcat whois.cymru.com 43 <IpList.txt | sort -n > listaordenada"

'''
os.system(comand)

for A in Arecords:
	temp = comand + " " + A + "'"
	os.system(temp)
	
print ("AAAA RECORDS:")	
print (AAAArecords)	
for AAAA in AAAArecords:
	temp = comand + " " + AAAA + "'"
	os.system(temp)
