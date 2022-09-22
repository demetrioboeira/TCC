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
	
with open ("Ipv4List.txt 2022-09-21", "r") as listaip:
	for line in listaip:
		token = line.split('.')
		token[3] = 0
		mascara = str(token[0]) + "." + str(token[1]) + "." + str(token[2]) + "." + str(token[3])
		try:
			print (asnhash[iphash[mascara][:-1]])
		except:
			print ("mascara de rede " + mascara + " não encontrada na lista" )

'''			
with open ("Ipv6List.txt 2022-09-21", "r") as listaip6:
	for line in listaip6:
		token = line.split(':')
		mascara = str(token[0]) + ":" + str(token[1]) + ":" + str(token[2]) + "::"
		try:
			print(asnhash[ip6hash[mascara][:-1]])
		except:
			print ("mascara de rede " + mascara + " não encontrada na lista" )
'''
#print (asnhash[iphash['185.89.219.0'][:-1]])

