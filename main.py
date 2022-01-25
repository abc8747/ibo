import os
import fitz
from rich import print

class Document:
    def __init__(self, dir:str, docid:str) -> None:
        self.dir = dir
        self.docid = docid
        # print(f'Processing {self.docid}')
    
    def extractWords(self):
        self.words = []
        for p in fitz.open(self.dir):
            t = p.get_text('dict')
            if 'blocks' not in t: continue
            for b in t['blocks']:
                if 'lines' not in b: continue
                for l in b['lines']:
                    if 'spans' not in l: continue
                    for s in l['spans']:
                        self.words.append({
                            'size': s['size'],
                            'text': s['text'],
                        })
    
    def organiseQuestions(self):
        for w in self.words:
            print(w)

if __name__ == '__main__':
    inDir = 'data/sr'
    for srFile in os.listdir(inDir):
        doc = Document(dir=os.path.join(inDir, srFile), docid=os.path.splitext(srFile)[0])
        doc.extractWords()
        doc.organiseQuestions()