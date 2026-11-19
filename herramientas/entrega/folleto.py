"""Genera el folleto complementario sin modificar el documento académico."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Entregables/Material_Drive/10_Marketing/Folleto_Residata.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('Residata - Gestión de residuos sólidos')
c.setAuthor('Equipo DSU / Residata')
w,h = A4
paper, ink, green = map(HexColor, ['#fbfbf8','#17191c','#0b6b4f'])
c.setFillColor(paper); c.rect(0,0,w,h,fill=1,stroke=0)
c.setFillColor(green);c.rect(0,h-15,w,15,fill=1,stroke=0)
def text(x,y,s,size=12,bold=False,color=ink):
 c.setFont('ArialBold' if bold else 'Arial',size);c.setFillColor(color);c.drawString(x,y,s)
def para(x,y,s,width=510,size=11,color=ink):
 style=ParagraphStyle('p',fontName='Arial',fontSize=size,leading=size*1.45,textColor=color)
 p=Paragraph(s,style);_,height=p.wrap(width,500);p.drawOn(c,x,y-height);return y-height
text(38,773,'Residata',40,True,green)
text(38,738,'Gestión de residuos sólidos',22,True)
para(38,714,'Registro en campo, planificación y análisis para equipos que gestionan la recolección en campus e instituciones.',size=13)
c.drawImage(str(ROOT/'auditoria_gui/capturas/crossrole-20261119-005651-CR-tablero-supervisor.png'),38,392,width=w-76,height=258,preserveAspectRatio=True,anchor='c')
text(38,379,'Captura del sistema DSU con datos de demostración.',9,color=HexColor('#565b62'))
for y,title,body in [
 (348,'Registrar','Vaciados e incidencias asociados a los puntos y jornadas del equipo.'),
 (285,'Coordinar','Planificación de rutas, personal y vehículos, con acceso según el rol.'),
 (222,'Decidir','Tableros, mapa, reportes PDF/Excel y predicción con Random Forest y margen de error.')]:
 text(38,y,title,15,True,green);para(38,y-12,body,size=11)
qr=QrCodeWidget('https://residata-bolivia.vercel.app/');b=qr.getBounds();size=85
renderPDF.draw(Drawing(size,size,transform=[size/(b[2]-b[0]),0,0,size/(b[3]-b[1]),0,0],* [qr]),c,35,51)
text(138,122,'Conoce la demostración',14,True)
text(138,100,'residata-bolivia.vercel.app',11)
c.linkURL('https://residata-bolivia.vercel.app/',(138,95,420,114),relative=0)
text(138,80,'Contacto: rekteado@gmail.com',11)
text(38,33,'Proyecto académico DSU-UAGRM · Residata S.R.L. en constitución · Noviembre 2026',8,color=HexColor('#565b62'))
c.save()
print(OUT)
if __name__ == '__main__':
 import pypdfium2 as pdfium
 doc=pdfium.PdfDocument(str(OUT));out=ROOT/'tmp/pdfs';out.mkdir(parents=True,exist_ok=True)
 doc[0].render(scale=1.4).to_pil().save(out/'folleto.png')
 print('paginas',len(doc))
