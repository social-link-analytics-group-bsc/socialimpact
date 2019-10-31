#!/bin/bash
folder=/home/bsclife018/Desktop/socialimpact
#shopt -s globstar
#echo "Converting pdfs to txt files..."
#for file in ${folder}/data/**/**/*.pdf
#do
#  mv "$file" "${file// /_}"  
#  echo ${file}
#  python2 /home/bsclife018/Desktop/socialimpact/pdfminer-master/pdf2txt.py ${file// /_} > ${file// /_}.txt
#done
#echo "Finished converting!"
python3 ${folder}/inspect_reports.py
python3 ${folder}/retrieve_tweets.py
