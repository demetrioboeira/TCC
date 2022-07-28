import dns.resolver
import subprocess
import os
domain = input('Please input an domain: ')
NS = dns.resolver.resolve(domain, 'NS')

NSlist = []
for answer in NS.response.answer:
   for item in answer.items:
      NSlist.append(item.to_text())

Arecords = []
AAAArecords = []
for nsrecord in NSlist:
	   nsrecord = nsrecord[:-1]
	   teste = subprocess.check_output(["nslookup", nsrecord])
	   first, *middle, last = teste.split()
	   try:
	   	AAAArecords.append(last.decode("utf-8"))
	   	Arecords.append(middle[8].decode("utf-8"))
	   except:
	   	Arecords.append(last.decode("utf-8"))	

print ("NS RECORDS:")
print (NSlist)
print ("A RECORDS:")
print (Arecords)

comand = "whois -h whois.cymru.com ' -v"
	
for A in Arecords:
	temp = comand + " " + A + "'"
	os.system(temp)
	
print ("AAAA RECORDS:")	
print (AAAArecords)	
for AAAA in AAAArecords:
	temp = comand + " " + AAAA + "'"
	os.system(temp)


      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
