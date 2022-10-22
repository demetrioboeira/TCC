import dns.resolver
import subprocess
import concurrent.futures
import os
import re
from datetime import date


iphash = {}
ip6hash = {}
asnhash = {}
erro = 0
certo = 0

print (erro, certo)

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
		#print (AAAArecord)
		return AAAArecord
		
	except:
		pass


def querydominio (dominio):
	domainNSList = []
	Arecords = []
	AAAArecords = []
	dominio = dominio[:-1]
	listaempresas = []
	tempA = []
	tempAAAA = []
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
		
		
		for nsrecord in domainNSList:
			tempA = getArecords(nsrecord)
			for ip in tempA:
				Arecords.append(ip)
			tempAAAA = getAAAArecords(nsrecord)
			for ip in tempAAAA:
				AAAArecords.append(ip)
		
		
		
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
				global certo 
				certo = certo + 1
				print (dominio, domainNSList, Arecords, AAAArecords, listaempresas)
				
			
				with open ('Medição dia' + str(date.today()), 'a') as file:
						file.write('#######################################################')
						file.write("\n")
						file.write("dominio \n")
						file.write(str(dominio))
						file.write("\nlista de NS records \n")
						file.write(str(domainNSList))
						file.write("\nlista de A records \n")
						file.write(str(Arecords))
						file.write("\nlista de AAAA records \n")
						file.write(str(AAAArecords))
						file.write("\nlista de empresas \n")
						file.write(str(listaempresas))
						file.write("\n")
						file.close()
				
			except:
				pass
		else:
			global erro
			erro = erro + 1
			print ('nao encontrado a empresa do dominio' + '' + dominio)
		
		
		#return domainNSList
		#return dominio1
	except:
		pass
		
		

	
with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(querydominio, Domainlist):
		pass
	
print (erro, certo)
