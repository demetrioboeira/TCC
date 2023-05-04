import dns.resolver
import subprocess
import concurrent.futures
import os
import re
import glob
import shutil
from datetime import date

concentracao = {}
controle = 1

with open ('Medição dia2022-12-24', 'r') as arquivo:
	for line in arquivo:
		line = str(line)		
		if controle == 11:
			if line in concentracao.keys():
				concentracao[line] = concentracao[line] + 1
			else:
				concentracao[line] = 1
			controle = 1
		else:	
			controle = controle + 1



for item in sorted(concentracao, key=concentracao.get, reverse=True):
	with open('Concentracao dia 2022-12-24', 'a') as file:
		porcentagem = concentracao[item]/10000
		#print(porcentagem)
		file.write(item.strip() + ':' + str(concentracao[item]).strip() + ':' + str(porcentagem) + '\n')
		


