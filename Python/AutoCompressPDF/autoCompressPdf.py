#!/usr/bin/env python
from os import walk, path, system
import pdf_compressor

###
# Get Path from a file from his name
###
def getPath(fileName):
    for root, dirs, files in walk(folder):
        if fileName in files:
            return root

folder = "/Users/Pierre-Adrien/OneDrive - univ-lyon2.fr/Lyon2/L2"

###
# Get all files in the 'folder' path
###
listeFichiers = []
for (repertoire, sousRepertoires, fichiers) in walk(folder):
    listeFichiers.extend(fichiers)

###
# Check if name exist in file, if not compress and add file name
###
existingPDF = open("/Users/Pierre-Adrien/Desktop/PA/Programmation/Python/AutoCompressPDF/existingPDF.txt", "r+")
readingFile = existingPDF.readlines()
for i in range(len(listeFichiers)):
    if ".pdf" in listeFichiers[i]:
        print(listeFichiers[i])
        if not (listeFichiers[i]+"\n" in readingFile):
            filePath = getPath(listeFichiers[i])
            filePath = filePath+"/"+listeFichiers[i]
            filePath = filePath.replace(" ", "\ ")
            call = "/usr/local/bin/python3 /Users/Pierre-Adrien/Desktop/PA/Programmation/Python/AutoCompressPDF/pdf_compressor.py " + filePath
            system(call)
            existingPDF.write(listeFichiers[i]+"\n")