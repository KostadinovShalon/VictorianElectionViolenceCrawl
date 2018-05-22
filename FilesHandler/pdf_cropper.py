from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO


def crop_bna(pdffile, xbottomleft, ybottomleft, xtopright, ytopright, width, height):
    input1 = PdfFileReader(pdffile)
    output = PdfFileWriter()

    page = input1.getPage(0)
    H = page.mediaBox.getUpperRight_y()
    W = page.mediaBox.getUpperRight_x()
    RW = float(W) / width
    RH = float(H) / height
    W1 = RW * xbottomleft
    W2 = RW * xtopright
    H1 = RH * (height - ytopright)
    H2 = RH * (height - ybottomleft)

    page.cropBox.lowerLeft = (W1, H1)
    page.cropBox.upperRight = (W2, H2)
    output.addPage(page)

    tmp = BytesIO()
    output.write(tmp)
    tmp.seek(0)
    return tmp
