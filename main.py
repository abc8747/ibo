import os
import fitz
import rich

class Document:
    def __init__(self, dir:str, docid:str) -> None:
        self.dir = dir
        self.docid = docid
        print(f'Processing {self.docid}')
    
    def populateData(self):
        for page in fitz.open(self.dir):
            print(page)

inDir = 'data/sr'
for srFile in os.listdir(inDir):
    doc = Document(dir=os.path.join(inDir, srFile), docid=os.path.splitext(srFile)[0])
    doc.populateData()
    break