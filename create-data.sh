#!/bin/bash
if [ -z $1 ]; then n=5; else n=$1; fi 
mkdir -p data/
# TWL06 Scrabble Word List
if [ ! -f data/twl06.txt ]; then 
    wget https://www.wordgamedictionary.com/twl06/download/twl06.txt -O data/twl06.txt
    sed -i 's/\s//g' data/twl06.txt # remove white space
fi
# SOWPODS Scrabble Word List
if [ ! -f data/sowpods.txt ]; then 
    wget https://www.wordgamedictionary.com/sowpods/download/sowpods.txt -O data/sowpods.txt
    sed -i 's/\s//g' data/sowpods.txt # remove white space
fi

if [ ! -f data/BIN_ordmyndir.txt ]; then 
    wget https://bin.arnastofnun.is/django/api/nidurhal/?file=BIN_ordmyndir.txt.zip -O data/BIN_ordmyndir.txt.zip
    unzip data/BIN_ordmyndir.txt.zip -d data
    rm data/BIN_ordmyndir.txt.sha256sum data/BIN_ordmyndir.txt.zip
    sed -i 's/\s//g' data/BIN_ordmyndir.txt
fi 

filename=data/en-len$n.txt
if [ ! -f $filename ]; then 
    awk -v word_length=$n '{if(length($0)==word_length){print toupper($0)}}' data/twl06.txt data/sowpods.txt | sort -u > $filename
fi
filename=data/is-len$n.txt
if [ ! -f $filename ]; then 
    awk -v word_length=$n '{if(length($0)==word_length){print toupper($0)}}' data/BIN_ordmyndir.txt | grep -v '-' | sort -u > $filename
fi 

for filename in `ls data/*-len*.txt`; do
    wc -l $filename     
done
