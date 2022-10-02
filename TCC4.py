import dns.resolver
import subprocess
import concurrent.futures
import os
import re
from datetime import date
#NS = dns.resolver.resolve(domain, 'NS')

Domainlist = []


class Dominio:
	def __init__(self, nome, nsrecords, arecords, aaaarecords, empresa):
		self.nome = nome
		self.nsrecords = nsrecords
		self.arecords = arecords
		self.aaaarecords = aaaarecords
		self.empresa = empresa
	
dominio1 = Dominio('google.com', Domainlist, Domainlist, 11, 'google')



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
	except Exception as erro:
		global dominioscomerro
		dominioscomerro.append(dominio)
		

	
with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getNSrecords, Domainlist):
		try:
			for item in result:
				print (item)
				NSlist.append(item)
		except:
			pass
		
print (NSlist)


Arecords = []


def getArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	Arecord = []
	try:
		query = dns.resolver.resolve(nsrecord, 'A')
		for item in query:
			Arecord.append(item.to_text())
		#print (Arecord)
		return Arecord
		
	except:
		pass
		

with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getArecords, NSlist):
		try:
			for item in result:
				print (item)
				Arecords.append(item)
		except:
			pass


print (Arecords)


AAAArecords = []		
def getAAAArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	AAAArecord = []
	try:
		query = dns.resolver.resolve(nsrecord, 'AAAA')
		for item in query:
			AAAArecord.append(item.to_text())
		#print (Arecord)
		return AAAArecord
		
	except:
		pass


with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getAAAArecords, NSlist):
		try:
			for item in result:
				print (item)
				AAAArecords.append(item)
		except:
			pass


print (AAAArecords)

today = date.today()

with open ('Ipv4List.txt' + " " + str(today), 'w') as file:
	for ip in Arecords:
		file.write(ip)
		file.write("\n")
	
with open ('Ipv6List.txt' + " " + str(today), 'w') as file:
	for ip in AAAArecords:
		file.write(ip)
		file.write("\n")
