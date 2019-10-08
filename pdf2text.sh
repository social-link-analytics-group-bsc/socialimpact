#!/bin/bash
shopt -s globstar
#echo "Converting pdfs to txt files..."
#for file in "/home/fabio/Documentos/SocialImpact/data"/**/**/*.pdf
#do
#  mv "$file" "${file// /_}"  
#  python2 /home/fabio/Documentos/SocialImpact/pdfminer-master/tools/pdf2txt.py ${file// /_} > ${file// /_}.txt
#done
#echo "Finished converting!"
echo "Searching for evidences of impact on text..."
python3 SocialImpact.py
