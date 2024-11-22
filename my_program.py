#!/usr/bin/python3

#import modules
import os, subprocess, shutil




#get user input - protein family and taxonomic group
print('Please enter the protein family e.g. glucose-6-phosphatase')
#prot_fam = input()
prot_fam = 'glucose-6-phosphatase'
prot_fam = prot_fam.lower()

print('Please enter the taxonomic group e.g. Aves')
#tax_gr = input()
tax_gr = 'Aves'
tax_gr = tax_gr.lower()

print(f'You chose {prot_fam} in {tax_gr}')

#prepare query
my_query = f"{prot_fam}[protein] AND {tax_gr}[Organism]"
print(my_query)

subprocess.run(['./fetch_sequence.sh', my_query])
