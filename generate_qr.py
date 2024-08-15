import qrcode
from django.core.management.base import BaseCommand
from django.urls import reverse
from feedbacks.models.sources import Source
from django.conf import settings
from PIL import Image
import os
import jinja2
import pdfkit
import imgkit

BLUE="#0671B9"
YELLOW="#E4A821"
WHITE="#FFFFFF"
QR_TEMPLATE_PATH = settings.MEDIA_ROOT
QR_TEMPLATE_FILE = 'QR_template.html'
# WKHTML2_PDF_PATH = os.path.join(settings.BASE_DIR, "dependency", "wkhtmltox", "bin", "wkhtmltoimage.exe")

# CONFIG = imgkit.config(wkhtmltoimage=WKHTML2_PDF_PATH)
CONFIG = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')

class Command(BaseCommand):
    help = 'Generate QR Code'

    def handle(self, *args, **kwargs):
        QR_FOLDER = 'qr'
        
        source_data = Source.objects.all()
        Logo_link = os.path.join(settings.MEDIA_ROOT, 'BBL-fb.jpg')
        
        logo = Image.open(Logo_link)
        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)  # type: ignore

        for source in source_data:
            SOURCE_NAME = f"{source.source_name.replace(' ', '_').replace('/', '_')}"
            QR_FILE_NAME = f"{SOURCE_NAME}.png"
            QR_IMAGE_PATH = os.path.join(os.path.join(settings.LOCAL_FOLDER, QR_FOLDER), QR_FILE_NAME)
            
            #url = settings.SITE_URL + reverse('customer_feedback', kwargs={'uuid': source.id})
            url = f"{settings.SITE_URL}{reverse('customer_feedback', kwargs={'uuid': str(source.id)})}"

            QRcode = qrcode.QRCode( # type: ignore
                error_correction=qrcode.constants.ERROR_CORRECT_H  # type: ignore
            )            

            QRcode.add_data(url)
            QRcode.make()
            QRimg = QRcode.make_image(fill_color=BLUE, back_color=WHITE).convert('RGB')
            pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)
            QRimg.save(QR_IMAGE_PATH)

            templateLoader = jinja2.FileSystemLoader(searchpath=QR_TEMPLATE_PATH)
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(QR_TEMPLATE_FILE)   

            HTML_FILE_NAME = f"{SOURCE_NAME}.html"
            HTML_FILE_PATH = os.path.join(os.path.join(settings.LOCAL_FOLDER, QR_FOLDER), HTML_FILE_NAME)

            source_html = template.render(
                BBL_BRANDING=os.path.join(settings.MEDIA_ROOT, 'BBL-logo.png'),
                QR_IMAGE_PATH=QR_IMAGE_PATH, 
                SOURCE_NAME=source.source_name, 
		LOCATION_LOGO=os.path.join(settings.MEDIA_ROOT, 'location.png')
            )
            
            with open(HTML_FILE_PATH, 'w') as fh:
                fh.write(template.render(
                    BBL_BRANDING=os.path.join(settings.MEDIA_ROOT, 'BBL-logo.png'),
                    QR_IMAGE_PATH=QR_IMAGE_PATH, 
                    SOURCE_NAME=source.source_name,
		    LOCATION_LOGO=os.path.join(settings.MEDIA_ROOT, 'location.png') 
                ))

            PDF_FILE_NAME = f"{SOURCE_NAME}.jpg"
            PDF_FILE_PATH = os.path.join(os.path.join(settings.LOCAL_FOLDER, QR_FOLDER), PDF_FILE_NAME)

            # pdfkit.from_string(input=source_html, 
            #                    output_path=PDF_FILE_PATH,
            #                    configuration=CONFIG,
            #                    options={"enable-local-file-access": "", 'page-size':'A4'})

            # pdfkit.from_file(input=HTML_FILE_PATH, output_path=PDF_FILE_PATH, configuration=CONFIG, options={"enable-local-file-access": "", 'page-size':'A4'})
            
            imgkit.from_file(HTML_FILE_PATH, PDF_FILE_PATH, config=CONFIG, options={"enable-local-file-access": "", 'encoding': 'UTF-8', 'format': 'jpg',
                                                                                    'width': 1400, 'height': 1000, 'zoom': 1.6,})
            
            print(f"Generated QR: {QR_FILE_NAME}, Generated HTML: {HTML_FILE_NAME}, Icon Path: {os.path.join(settings.MEDIA_ROOT, 'location.png')}")
