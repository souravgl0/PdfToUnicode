from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar, LTLine

import pdfminer
import sys, getopt
from krutidev2unicode import kru2uni

def appendK(s,text):
    if len(s) > 0:
        latest = s[-1]
        if latest[0] == 'k':
            latest [1] += text
        else:
            s.append(['k',text])
    else:
        s.append(['k',text])
#     s+=krutidev2unicode.kru2uni(text.encode('utf-8'))
    return s
def appendN(s,text):
    if len(s) > 0:
        latest = s[-1]
        if latest[0] == 'n':
            latest [1] += text
        else:
            s.append(['n',text])
    else:
        s.append(['n',text])
    return s

def parse_obj(objs):
    result = []
    for obj in objs:
        if isinstance(obj,LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
#                     result = appendH(result,o.get_text())
                    for c in  o._objs:
                        if isinstance(c, pdfminer.layout.LTChar):
                            if hasattr(c,'fontname'):
                                if "KrutiDev" in c.fontname:
                                    result = appendK(result,c.get_text())
                                else:
                                    result = appendN(result,c.get_text())
                            else:
                                result = appendN(result,c.get_text())
                        elif isinstance(c, pdfminer.layout.LTAnno):
                            if c.get_text()=='\n':
                                result = appendK(result,c.get_text())
            result = appendK(result,"\n")
    return result



def pdftotext(filename):
    """
    Parses text from pdf. Returns text seperated by KrutiDev font
    and any other latin font. Pdf needs to have font information
    for it to work.
    Returns a list. Each element in the list is a list containing two
    elements. First element is 'k' to represent KrutiDev Font or 'n' to
    represent normal latin font. Second element is the extracted text.
    The order of text is preserved in the list.

    Note: The returned text is a unicode string.
    """

    with open(filename,'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # page_no = 2
        text = []
        for n,page in enumerate(PDFPage.create_pages(document)):
            # if n != page_no:
                # continue
            interpreter.process_page(page)
            layout = device.get_result()
            text += parse_obj(layout)

        return text

def convergetext(text):
    result = u""
    for element in text:
        if element[0] == 'k':
            # print repr(element[1])
            a= element[1].encode('utf-8')
            result += kru2uni(a).decode('utf-8')
        else:
            # print element[1]
            result += element[1]
    return result

def extracttext(infile,outfile):
    text = pdftotext(infile)
    otext = convergetext(text)
    with open(outfile,"w") as f:
        f.write(otext.encode('utf-8'))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:")
        for opt in opts:
            if opt[0] == "-i":
                infile = opt[1]
            if opt[0] == "-o":
                outfile = opt[1]
    except:
        infile = "1.pdf"
        outfile = "1.txt"

    extracttext(infile,outfile)
