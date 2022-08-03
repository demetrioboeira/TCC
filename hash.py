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
		

print (asnhash[ip6hash['2c0f:6400:1000::'][:-1]])

