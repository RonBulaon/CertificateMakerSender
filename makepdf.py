from fpdf import FPDF, HTMLMixin
import os.path

class HTML2PDF(FPDF, HTMLMixin):
    pass

def cert(name, event, _date, cert_name, filename, location, serialnumber, outputDir):
    pdf = HTML2PDF(orientation='L', unit='mm', format='letter')
    pdf.add_page()
    pdf.image(cert_name,x=0, y=0, w=290)
    #pdf.image(cert_name,x=0, y=0, w=290)

    pdf.set_font("times","I", size=16)
    pdf.set_text_color(31, 78, 121)
    pdf.cell(0, 50, txt="", ln=2,border='1',align='C')
    pdf.cell(0, 20, txt="THIS CERTIFICATE IS PRESENTED TO", ln=2,border='1',align='C')

    pdf.set_font("Arial","B",size=36)
    pdf.multi_cell(0,30,txt=name,border='TB',align='C')

    pdf.set_font("times","I", size=16)
    pdf.cell(0, 10, txt="", ln=2,border='1',align='C')
    pdf.cell(0, 10, txt="FOR ATTENDING THE SEMINAR", ln=2,border='1',align='C')
    pdf.cell(0, 5, txt="", ln=2,border='1',align='C')

    top = pdf.y
    offset = pdf.x + 30
    pdf.multi_cell(30,15,"",0)
    pdf.y = top
    pdf.x = offset
    pdf.set_font("Arial","B",size=36)
    pdf.multi_cell(200,15,event,0,align="C")
    pdf.cell(0, 10, txt="", ln=2,border='1',align='C')
    pdf.set_font("times","I", size=16)
    pdf.cell(0, 8, txt="HELD ON "+_date, ln=2,border='1',align='C')
    pdf.cell(0, 8, txt="AT "+location, ln=2,border='1',align='C')
    pdf.set_font("times","I", size=12)
    pdf.cell(0, 8, txt="Serial Number : "+serialnumber, ln=2,border='1',align='C')
    pdf.output(outputDir+'/'+filename)

    if os.path.isfile(outputDir+'/'+filename):
       return 'Success'

    return 'Error'
