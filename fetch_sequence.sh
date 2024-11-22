#!/bin/bash

#delete any old reports and generate a new report file
if [ -d "results" ]; then rm -fr results ; echo -e "previous results deleted."; mkdir results; echo -e "new results directory created"
else
	touch results.txt; mkdir results; echo -e "new results directory created"
fi

#create a results file
echo -e "query: $1" > results.txt

#fetch the seqence 
esearch -db protein -query "$1" | efetch -format fasta > my_sequence.fasta


#check if my_sequence.fasta it's not empty
num_seq=$(grep -c ">" my_sequence.fasta)
if [[ "$num_seq" -eq 0 ]]; then
    echo -e "No sequences found"
else
    echo -e "$num_seq sequences found"
fi
