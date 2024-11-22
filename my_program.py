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

#fetch sequences
subprocess.call("chmod 700 fetch_sequence.sh", shell=True)
subprocess.run(['./fetch_sequence.sh', my_query])


print("Would you like to run analysis on this number of sequences? y/n")

#align sequences and then determine, and plot, the level of conservation between the protein sequences
print("specify alignment window size") #maybe add option of multiple sizes?
#win = input()
win = 3
subprocess.call("clustalo -i my_sequence.fasta -o my_aligned_seq.fasta", shell=True)    
subprocess.call("plotcon -sequence my_aligned_seq.fasta -winsize 3 -graph png", shell=True)





