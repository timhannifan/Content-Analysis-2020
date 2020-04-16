import requests
import io
import pdfminer.pdfinterp
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfpage

DEMO_URL = 'https://mediawell.ssrc.org/literature-reviews/defining-disinformation/versions/1-0/?pdf=52268'


def request_content_stream(url):
    try:
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            return res.content
    except requests.HTTPError as e:
        print(e)

def readPDF(pdfFile):
    #Based on code from http://stackoverflow.com/a/20905381/4955164
    #Using utf-8, if there are a bunch of random symbols try changing this
    codec = 'utf-8'
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    retstr = io.StringIO()
    layoutParams = pdfminer.layout.LAParams()
    device = pdfminer.converter.TextConverter(rsrcmgr, retstr, laparams = layoutParams, codec = codec)
    #We need a device and an interpreter
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    password = ''
    maxpages = 0
    caching = True
    pagenos=set()
    for page in pdfminer.pdfpage.PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    device.close()
    returnedString = retstr.getvalue()
    retstr.close()
    return returnedString


def demo_pdf_read(url):
    return main(url)


def main(url=None):
    if url is None:
        url = DEMO_URL
    req_stream = request_content_stream(url)
    bytes_stream = io.BytesIO(req_stream)

    return readPDF(bytes_stream)

if __name__ == "__main__":
    main()