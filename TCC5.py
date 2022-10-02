import dns.resolver
import subprocess
import concurrent.futures
import os
import re
from datetime import date


iphash = {}
ip6hash = {}
asnhash = {}

with open ("ip2as.txt", "r") as ip:
	for line in ip:
		token = line.split('	')
		rede = token[0]
		asn = token[2]
		iphash[rede] = asn
		
		
#print (iphash['185.241.125.0'])

with open ("ip62as.txt", "r") as ip6:
	for line in ip6:
		token = line.split('	')
		rede = token[0]
		asn = token[2]
		ip6hash[rede] = asn
		
#print (ip6hash['2c0f:2e00:1a0::'])

with open ("as2org.txt", "r") as asn:
	for line in asn:
		token = line.split('|')
		asn = token[0]
		org = token[2]
		asnhash[asn] = org
'''	
with open ("Ipv4List.txt 2022-09-21", "r") as listaip:
	for line in listaip:
		token = line.split('.')
		token[3] = 0
		mascara = str(token[0]) + "." + str(token[1]) + "." + str(token[2]) + "." + str(token[3])
		try:
			print (asnhash[iphash[mascara][:-1]])
		except:
			print ("mascara de rede " + mascara + " não encontrada na lista" )
			
with open ("Ipv6List.txt 2022-09-21", "r") as listaip6:
	for line in listaip6:
		token = line.split(':')
		mascara = str(token[0]) + ":" + str(token[1]) + ":" + str(token[2]) + "::"
		try:
			print(asnhash[ip6hash[mascara][:-1]])
		except:
			print ("mascara de rede " + mascara + " não encontrada na lista" )
'''

Domainlist = []


class Dominio:
	def __init__(self, nome, nsrecords, arecords, aaaarecords, empresa):
		self.nome = nome
		self.nsrecords = nsrecords
		self.arecords = arecords
		self.aaaarecords = aaaarecords
		self.empresa = empresa
	


with open ('trancolistreduzida.txt' , 'r') as dominios:
	for dominio in dominios:
		dominio = ''.join([i for i in dominio if not i.isdigit()])
		dominio = dominio[1:]
		Domainlist.append(dominio)

#print (Domainlist)
NSlist = []

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


def getNSrecords (dominio):
	domainNSList = []
	Arecords = []
	AAAArecords = []
	dominio = dominio[:-1]
	listaempresas = []
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
		
		with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
			for result in executor.map(getArecords, domainNSList):
				try:
					for item in result:
						#print (item)
						Arecords.append(item)
				except:
					pass
			
		with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
			for result in executor.map(getAAAArecords, domainNSList):
				try:
					for item in result:
						#print (item)
						AAAArecords.append(item)
				except:
					pass
		for line in Arecords:
			token = line.split('.')
			token[3] = 0
			mascara = str(token[0]) + "." + str(token[1]) + "." + str(token[2]) + "." + str(token[3])
			try:
				empresa = asnhash[iphash[mascara][:-1]]
				if empresa not in listaempresas:
					listaempresas.append(empresa)
			
			except:
				pass
		
		for line in AAAArecords:
			token = line.split(':')
			mascara = str(token[0]) + ":" + str(token[1]) + ":" + str(token[2]) + "::"
			try:
				empresa = asnhash[ip6hash[mascara][:-1]]
				if empresa not in listaempresas:
					listaempresas.append(empresa)
			except:
				pass
		
		#print (listaempresas)
		if len(listaempresas) != 0:
			#print (listaempresas)
			try:
				dominio1 = Dominio(dominio, domainNSList, Arecords, AAAArecords, listaempresas)
				print (dominio1.nome, dominio1.nsrecords, dominio1.arecords, dominio1.aaaarecords, dominio1.empresa)
			except:
				pass
		else:

			print ('nao encontrado a empresa do dominio' + '' + dominio)
		
		
		#return domainNSList
		return dominio1
	except:
		pass
		
		

	
with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(getNSrecords, Domainlist):
		try:
			#rint (result)
			NSlist.append(result)
			#print (NSlist)
		except:
			pass
		
#print (NSlist)

'''
Arecords = []



		




print (Arecords)


AAAArecords = []		




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
		
'''
