from PyPDF2 import PdfFileWriter, PdfFileReader
import paramiko
from io import BytesIO

with open("test.pdf", "rb") as in_f:
    input1 = PdfFileReader(in_f)
    output = PdfFileWriter()

    width = 8034
    height = 10715
    xbottomleft = 5294
    ybottomleft = 3750
    xtopright = 6508
    ytopright = 6110

    page = input1.getPage(0)

    H = page.mediaBox.getUpperRight_y()
    W = page.mediaBox.getUpperRight_x()
    r = float(height) / width
    h = (H - r*W) / 2
    print W, H
    R = float(W) / float(width)
    R2 = float(H) / float(height)
    print R
    W1 = R*xbottomleft
    W2 = R*xtopright
    H1 = R2*(height - ytopright)
    H2 = R2*(height - ybottomleft)

    page.cropBox.lowerLeft = (W1, H1)
    page.cropBox.upperRight = (W2, H2)
    output.addPage(page)

    with open('out.test.pdf', 'wb') as ff:
        output.write(ff)
    # tmp = BytesIO()
    # output.write(tmp)
    # tmp.seek(0)
    # transport = paramiko.Transport(("coders.victorianelectionviolence.uk", 22))
    # transport.connect(username="data_feeder", password="Arp48dEx")
    # sftp = paramiko.SFTPClient.from_transport(transport)
    # sftp.chdir("documents")
    # try:
    #     sftp.chdir("1")  # Test if remote_path exists
    # except IOError:
    #     sftp.mkdir("1")  # Create remote_path
    #     sftp.chdir("1")
    # sftp.putfo(tmp, './cropped.pdf')  # At this point, you are in remote_path in either case
    # sftp.close()
