import os
from venv import create
import fitz
from rich import print
import re

def approx(val, target, errmargin):
    return abs(val - target) <= errmargin

class Document:
    def __init__(self, dir:str, docid:str) -> None:
        self.dir = dir
        self.docid = docid
    
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
                        if s['text'] in [' ', '\uf096']: continue
                        self.words.append({
                            'size': s['size'],
                            'text': s['text'],
                        })
    
    def organiseQuestions(self):
        hlmapping = {
            'higher and standard level': True,
            'standard and higher level': True,
            'hl and sl': True,
            'sl and hl': True,
            'higher level': True,
            'standard level': False,
            'hl': True,
            'sl': False,
        }
        slmapping = {
            'higher and standard level': True,
            'standard and higher level': True,
            'hl and sl': True,
            'sl and hl': True,
            'higher level': False,
            'standard level': True,
            'hl': False,
            'sl': True,
        }
        papermapping = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
        }
        
        currHL = None
        currSL = None
        currPaper = None

        found = False
        for w in self.words:
            wl = w["text"].lower()
            r0 = re.compile(r"^(higher level|standard level|higher and standard level|hl|sl|hl and sl|sl and hl|standard and higher level) paper (one|two|three|four|five|six|1|2|3|4|5|6).*").match(wl)
            r1 = re.compile(r"^paper (one|two|three|four|five|six).*").match(wl)
            r2 = re.compile(r"^(higher level|standard level|higher and standard level|hl|sl|hl and sl|sl and hl|standard and higher level).*").match(wl)
            if r0:
                currHL, currSL, currPaper = hlmapping[r0.group(1)], slmapping[r0.group(1)], papermapping[r0.group(2)]
            elif r1:
                currPaper = papermapping[r1.group(1)]
            elif r2:
                currHL, currSL = hlmapping[r2.group(0)], slmapping[r2.group(1)]

            if r0 or r2:
                found = True

        if not found:
            print(self.docid)

if __name__ == '__main__':
    inDir = 'data/sr'
    for srFile in os.listdir(inDir):
        doc = Document(dir=os.path.join(inDir, srFile), docid=os.path.splitext(srFile)[0])
        doc.extractWords()
        doc.organiseQuestions()
        # break