import dns.resolver
import subprocess
import concurrent.futures
import os
import re
#NS = dns.resolver.resolve(domain, 'NS')

Domainlist = []


with open ('trancolistreduzida.txt' , 'r') as dominios:
	for dominio in dominios:
		dominio = ''.join([i for i in dominio if not i.isdigit()])
		dominio = dominio[1:]
		Domainlist.append(dominio)

#print (Domainlist)
NSlist = []

def getNSrecords (dominio):
	domainNSList = []
	dominio = dominio[:-1]
	#print (dominio)
	
	try:	
		NS = dns.resolver.resolve(dominio, 'NS')
		#print (NS)
		for answer in NS.response.answer:
			#print (answer)
			for item in answer.items:
				#print (item)
				#global NSlist
				domainNSList.append(item.to_text())
				#print (NSlist)
		#print (domainNSList)
		return domainNSList
	except:
		pass

	
with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getNSrecords, Domainlist):
		try:
			for item in result:
				NSlist.append(item)
		except:
			pass
		

print (NSlist)


Arecords = []


def getArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	Arecord = ''
	try:
		teste = subprocess.check_output(["nslookup", nsrecord])
		first, *middle, last = teste.split()
		try:
	   		Arecord = middle[8].decode("utf-8")
		except:
	   		Arecord = last.decode("utf-8")
		#print (Arecord)
		return Arecord
	except:
		pass
		
with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getArecords, NSlist):
		if result != None:
			print (result)
			Arecords.append(result)
		#else:
			#print ('Era none')	

print ("A RECORDS:")
print (Arecords)


AAAArecords = []		
def getAAAArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	AAAArecord = ''
	Arecord = ''
	try:
		teste = subprocess.check_output(["nslookup", nsrecord])
		first, *middle, last = teste.split()
		try:
			Arecord = middle[8].decode("utf-8")
			AAAArecord = last.decode("utf-8")
		except:
	   		pass
	   	
		return AAAArecord
	except:
		pass


with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getAAAArecords, NSlist):
		if result != None:
			print (result)
			AAAArecords.append(result)
		#else:
			#print ('Era none')

print ("AAAA RECORDS:")
print (AAAArecords)

with open ('IpList.txt', 'w') as file:
	file.write("begin \n")
	for ip in Arecords:
		file.write(ip)
		file.write("\n")
	for ip in AAAArecords:
		file.write(ip)
		file.write("\n")
	file.write("end")	


'''
comand = "netcat whois.cymru.com 43 <IpList.txt | sort -n > listaordenada"


os.system(comand)

for A in Arecords:
	temp = comand + " " + A + "'"
	os.system(temp)
	
print ("AAAA RECORDS:")	
print (AAAArecords)	
for AAAA in AAAArecords:
	temp = comand + " " + AAAA + "'"
	os.system(temp)
'''
