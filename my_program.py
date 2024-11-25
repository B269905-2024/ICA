#!/usr/bin/python3

#import modules
import os, subprocess, shutil
import re
import random
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from fpdf import FPDF

########################functions

#define functions
def valid_number(top_num):
    """ this function asks for user input and checks if it's a number smaller than top_num and then returns it"""
    while True:
        user_input = input()
        if user_input.isdigit(): #make sure input is a number smaller than top num
            if int(user_input) <= int(top_num):
                break
            else:
                print(f'Enter a number smaller than {top_num}')
                continue
            break
        else:
            print('Enter a valid number')
            continue

    #print(user_input)
    user_input = int(user_input)
    return user_input


def add_line(line):
    """"adds a line to results.txt, s_count = print(line) has to be specified before"""
    with open("results.txt", "a") as file:
                file.write(line)



##############################the actual code

a = True # outer loop to be able to re-enter protein family and taxonomic group
while a:
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


    #read the file
    seq = open("my_sequence.fasta")
    seq_contents = seq.read()
    #print(seq_contents)

    #get organisms
    multiple_sequences = re.split('>', seq_contents)
    sequences = [] #list of sequences with '>' apended
    for sequence in multiple_sequences:
        x = '>'+ sequence
        sequences.append(x)
    sequences.pop(0) #remove first '<'
    #print(sequences)


    #create a list of organisms
    organisms = []
    for sequence in multiple_sequences:
        organism = re.search(r'\[(.*?)\]', sequence)
        if organism:
                    organisms.append(organism.group(1))

    #create a dictionary where organims is a key and sequence is a value
    org_seq_dict = {}
    for i in range(len(organisms)):
        org_seq_dict[organisms[i]] = sequences[i]



    #count number of sequences
    seq_count = seq_contents.count(">")
    print(f"{seq_count} sequences of {prot_fam} in {tax_gr} found. Would you like to run analysis on this data set? y/n")

    b = True
    while b: #inner loop
        restart = input()
        if restart.lower() == 'n':
            b = False

        elif restart.lower() == 'y':
            a = False #break outer loop
            b = False #break inner loop
        else:
            print ('enter y/n')
            continue

#line = print(f'{seq_count} sequences found')
add_line(f'{seq_count} sequences found')


#################################################Choosing sequences for conservation analysis####################
print(f'Conservation analysis \nThere are {seq_count} sequences in the current data set. Which sequences would you like to use for conservation analysis?')
print('A. all of them (not recommended)')
print('B. choose a smaller data set at random (specify the size)')
print('C. choose a new data set from the same Genus')
print('D. choose organims from a current data set manually')

c = True
while c:
    con_an = input()
    if con_an.lower() == 'a':
        con_an_seq = sequences
        #write a new fasta file
        con_an_seq = ''.join(con_an_seq)
        con_an_seq_out = open("con_an_seq_out.fasta", "w")
        con_an_seq_out.write(con_an_seq)
        con_an_seq_out.close()
        print('a done')
        c = False



    elif con_an.lower() == 'b':
        print('Specify random set size')
        size = input()
        if size.isdigit(): #check if user enterd a number
            if int(size) > seq_count: #check the if the new data set is smaller
                print(f'The new data set can not be bigger than current data set. Please enter a number smaller than {seq_count}')
            else:
                #write a new fasta file with less sequences
                con_an_seq = random.sample(sequences, int(size))
                #print(con_an_seq)
                con_an_seq = ''.join(con_an_seq)
                con_an_seq_out = open("con_an_seq_out.fasta", "w")
                con_an_seq_out.write(con_an_seq)
                con_an_seq_out.close()
                #print('b done')
                #line = print(f'{seq_count} sequences used for furter analysis. They are saved in con_an_seq_out.fasta')
                add_line(f'{seq_count} sequences used for furter analysis. They are saved in con_an_seq_out.fasta')

                c = False
        else:
            print('Please enter a valid number')

    elif con_an.lower() == 'c':
        #create list of genuses
        genus_list = []
        for organism in organisms:
            genus_end = organism.find(' ')
            #print(organism[0:genus_end])
            genus_list.append(organism[0:genus_end])

        #choose number of genuses
        num_gen = len(set(genus_list))
        print(f'There are {num_gen} Genera. Select the number of genrea you want to display along with their counts. They will be presented in order of highest to lowest frequency.')
        genus_input = valid_number(num_gen)
        #print(f'gen in: {genus_input}')


        #print genera
        genus_counts = Counter(genus_list)
        sorted_genus_counts = genus_counts.most_common()
        sorted_genus_counts_names_list = [genus for genus, count in sorted_genus_counts] #sorted list of genus counts
        top3_count = 0
        top3_list = [] #get names of 3 most frequent genera to include in the example

        #show chosen number of genera with their counter
        limit_show = genus_input
        count_show = 0

        for genus, count in sorted_genus_counts:
            if count_show >= limit_show:
                break

            if top3_count < 3:
                top3_list.append(genus)
                top3_count = top3_count + 1

            print(f"{genus}: {count}")
            count_show = count_show + 1

        top3_str=''
        for gen in top3_list:
            top3_str = top3_str + gen + ', '
        top3_str=top3_str[:-2]

        print('How would you like to choose genrea for the conservation analysis')
        print('A. Type names of genra you would like to use for the conservation analysis.')
        print(f'B. Select a number of genera with the highest species counts from the list to include in the analysis. For example, if you choose 3, the top 3 genera ({top3_str})  will be analysed.')

        while True:
            names_or_num = input()

            if names_or_num.lower() == 'a':
                print('enter the genera names e.g. Eudyptes, Corvus, Pygoscelis, Megadyptes')
                while True:
                    genera_names = input()
                    #genera_names = 'Eudyptes, corvUs, Pygoscelis, Megadyptes' #for testing
                    #genera_names = 'Eudyptes' #for testing
                    genera_names_list_cap_sen = genera_names.split(', ')
                    #make sure it's not caption sensitive
                    genera_names_list = []
                    for name in genera_names_list_cap_sen:
                        gen = name.lower()
                        gen = gen.capitalize()
                        genera_names_list.append(gen)

                    #in org_seq_dict find keys that start with any string from list of string 'genera_names_list' and create a list of values
                    genera_sequences_list = [
                    value for key, value in org_seq_dict.items()
                    if any(key.startswith(genus) for genus in genera_names_list)
                    ]

                    genera_names_list_str = str(genera_names_list)
                    genera_names_list_str = genera_names_list_str[1:-1]
                    #line = print(f'analysis run on protein sequences from {genera_names_list_str} genera')
                    add_line(f'analysis run on protein sequences from {genera_names_list_str} genera')




                    if len(genera_sequences_list) == 0:
                        print(f'Please re-enter the genera names. Make sure it follows this format "genus1, genus2, genus3" e.g. {top3_str}')
                    else:
                        break
                break


            elif names_or_num.lower() == 'b':
                print('Plese type a number of genera from the list to include in the analysis.')
                most_freq_gen_num = valid_number(genus_input)
                #print(most_freq_gen_num)
                #print(type(most_freq_gen_num))
                sorted_genus_counts_names_list = sorted_genus_counts_names_list[0:most_freq_gen_num]
                genera_sequences_list = [value for key, value in org_seq_dict.items()
                    if any(key.startswith(genus) for genus in sorted_genus_counts_names_list)
                    ]
                break
            else:
                print('Please enter A or B')


        #write a new fasta file
        con_an_seq = ''.join(genera_sequences_list)
        con_an_seq_out = open("con_an_seq_out.fasta", "w")
        con_an_seq_out.write(con_an_seq)
        con_an_seq_out.close()
        print('c done')
        c = False


    elif con_an.lower() == 'd':
        ogranisms_list = list(org_seq_dict.keys())
        organisms_str = ', '.join(ogranisms_list)
        print(f'{seq_count} sequences were identified, they come from the following species:')
        print(organisms_str)
        print('Enter names of species from above for for the conservation analysis')
        while True:
            species_names = input()
            #species names for testing
            #species_names = 'Eudyptes chrysolophus, Eudyptes moseleyi, Eudyptes robustus, Eudyptes pachyrhynchus, Eudyptula albosignata, Eudyptula minor, Eudyptes sclateri, Eudyptula minor novaehollandiae, Pygoscelis antarcticus, Megadyptes antipodes antipodes, Spheniscus mendiculus, Spheniscus demersus, Spheniscus magellanicus, Spheniscus humboldti, Corvus moneduloides, Meleagris gallopavo, Phasianus colchicus, Geospiza fortis'
            species_names_list_cap_sen = species_names.split(', ')
            #make sure it's not caption sensitive
            species_names_list = []
            for name in species_names_list_cap_sen:
                spec = name.lower() #make sure nothing is capitalised
                species_names_list.append(spec)

            #in org_seq_dict find keys that match species names create a list of values
            species_sequences_list = [
            value for key, value in org_seq_dict.items()
            if any(key.lower() == spec for spec in species_names_list)
            ]


            species_names_list_str = str(species_names_list)
            species_names_list_str = genera_names_list_str[1:-1]
            #line = print(f'analysis run on protein sequences from {species_names_list_str} species')
            add_line(f'analysis run on protein sequences from {species_names_list_str} species')

            if len(species_sequences_list) == 0:
                print(f'Please re-enter the species names. Make sure it follows this format "species1, species2, species3" e.g. Eudyptes chrysolophus, Eudyptes moseleyi, Eudyptes robustus')
            else:
                break

        #write a new fasta file
        con_an_seq = ''.join(species_sequences_list)
        con_an_seq_out = open("con_an_seq_out.fasta", "w")
        con_an_seq_out.write(con_an_seq)
        con_an_seq_out.close()
        print('done')
        print('d done')
        c = False

    else:
        print('choose A, B, C or D')







##########################End of choosing sequences for conservation analysis

#align sequences and then determine, and plot, the level of conservation between the protein sequences
print("specify alignment window size")
while True:
    win = input()
    if win.isdigit():
        break
    else:
        print('Enter a valid number')
#win = 3
subprocess.call("clustalo -i con_an_seq_out.fasta -o my_aligned_seq.fasta", shell=True)
subprocess.call("plotcon -sequence my_aligned_seq.fasta -winsize 3 -graph png", shell=True)

#add this as a top column in the report
#Query_ID	Subject_ID	%Identity	Alignment_Len	Mismatches	Gap_Openings	Q_Start	Q_End	S_Start	S_End	E-value	Bit_Score

subprocess.call("blastp -query con_an_seq_out.fasta -db swissprot -out blastp_con_an_deq.txt -evalue 1e-5 -outfmt 6 -remote", shell=True)



conservation_plot = mpimg.imread("plotcon.1.png")
plt.imshow(conservation_plot)

#########################Generate a report pdf
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

#add info about protein sequences
with open("results.txt", "r") as file:
    text = file.read()
    pdf.multi_cell(0, 10, text)

#add conservation plot
pdf.ln(10)
pdf.cell(0, 10, f"Similarity plot of Aligned Sequences of {prot_fam} in {tax_gr}", ln=True)
pdf.image("plotcon.1.png", x=10, y=pdf.get_y() + 10, w=100)


#blastp
pdf.cell(0, 10, "BlastP results:", ln=True)
with open("blastp_con_an_deq.txt", "r") as file:
    text = file.read()
    pdf.multi_cell(0, 10, text)

pdf.output(f"{prot_fam}_{tax_gr}_report.pdf")


##########################clean up and move to results folder
files_to_move = [
    "con_an_seq_out.fasta",
    "my_aligned_seq.fasta",
    "my_sequence.fasta",
    "plotcon.1.png",
    "results.txt",
    "blastp_con_an_deq.txt",
    f"{prot_fam}_{tax_gr}_report.pdf"
]

for file in files_to_move:
    shutil.move(file, os.path.join('results', file))


