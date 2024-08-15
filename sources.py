from uuid import uuid4
from django import forms
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms import Form, ValidationError
from django.http import HttpRequest
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.decorators import action
from django.shortcuts import render
from helpers.generate_qr_admin import generate_qr_admin
import qrcode
from django.urls import reverse
from django.conf import settings
from PIL import Image
import os
import jinja2
import pdfkit
import imgkit
from django.contrib import messages




BLUE="#0671B9"
YELLOW="#E4A821"
WHITE="#FFFFFF"
QR_TEMPLATE_PATH = settings.MEDIA_ROOT
QR_TEMPLATE_FILE = 'QR_template.html'
# WKHTML2_PDF_PATH = os.path.join(settings.BASE_DIR, "dependency", "wkhtmltox", "bin", "wkhtmltoimage.exe")

# CONFIG = imgkit.config(wkhtmltoimage=WKHTML2_PDF_PATH)
CONFIG = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')


class SourceType(models.TextChoices):
    ATM = "ATM", "ATM"
    BRANCH = "BRANCH", "Branch"

class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    source_address = models.TextField()
    source_id = models.CharField(max_length=10, blank=False, null=False)
    source_name = models.CharField(max_length=255, blank=False, null=False)
    source_type = models.CharField(choices=SourceType.choices, max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.source_name


class SourceAdmin(ModelAdmin):
    search_fields = ("source_id", "source_name")
    ordering = ("source_id", )
    list_display = [
        "id",
        "source_name",
        "source_type",
        "created",
    ]
    list_filter = ('source_type', 'created')
    list_per_page=80

    def save_model(self, request, obj, form, change):
        success = generate_qr_admin(str(obj.source_name), str(obj.id)) # type: ignore #ok
        if success:
            super().save_model(request, obj, form, change)
            

    actions = ['change_source_type_to_atm', 'change_source_type_to_branch', 'generate_qr_manually']

    def change_source_type_to_atm(self, request, queryset):
        queryset.update(source_type=SourceType.ATM)
        messages.add_message(request, messages.SUCCESS, 'Changed Source Type to ATM!')
    change_source_type_to_atm.short_description = "Change selected sources to ATM"

    def change_source_type_to_branch(self, request, queryset):
        queryset.update(source_type=SourceType.BRANCH)
        messages.add_message(request, messages.SUCCESS, 'Changed Source Type to Branch!')
    change_source_type_to_branch.short_description = "Change selected sources to Branch"

    def generate_qr_manually(self, request, queryset):
        QR_FOLDER = 'qr'

        # source_data = Source.objects.all()
        Logo_link = os.path.join(settings.MEDIA_ROOT, 'BBL-fb.jpg')

        logo = Image.open(Logo_link)
        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)  # type: ignore

        for source in queryset:
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
            templateLoader = jinja2.FileSystemLoader(searchpath=QR_TEMPLATE_PATH)
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(QR_TEMPLATE_FILE)

            HTML_FILE_NAME = f"{SOURCE_NAME}.html"
            # HTML_FILE_PATH=f'file:///D:/Projects/BRAC%20ADC%20BAU%20Web%20Portal/Customer_Feedback_QR/CustomerFeedbackQR/local/qr/Test3.html'
            # print(HTML_FILE_PATH)
            HTML_FILE_PATH = os.path.join(os.path.join(settings.LOCAL_FOLDER, QR_FOLDER), HTML_FILE_NAME)
            # DRIVE, TEMP_PATH = HTML_FILE.split(':', 1)
            # HTML_FILE_ENC = urllib.parse.quote(TEMP_PATH.replace('\\', '/'))

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

            # HTML_FILE_PATH= f"file:///{DRIVE}:{HTML_FILE_ENC}"
            print(HTML_FILE_PATH)
            PDF_FILE_NAME = f"{SOURCE_NAME}.jpg"
            PDF_FILE_PATH = os.path.join(os.path.join(settings.LOCAL_FOLDER, QR_FOLDER), PDF_FILE_NAME)
            # PDF_FILE_PATH = f"file:\\\\{PDF_FILE_PATH}"
            print(PDF_FILE_PATH)

            #pdfkit.from_string(input=source_html,
            #                    output_path=PDF_FILE_PATH,
            #                    configuration=CONFIG,
            #                    options={"enable-local-file-access": "", 'page-size':'A4'})

            imgkit.from_file(HTML_FILE_PATH, PDF_FILE_PATH, config=CONFIG, options={"enable-local-file-access": "", 'encoding': 'UTF-8', 'format': 'jpg',
                                                                                    'width': 1400, 'height': 1000, 'zoom': 1.5,})

            print(f"Generated QR: {QR_FILE_NAME}, Generated HTML: {HTML_FILE_NAME}")

        messages.add_message(request, messages.SUCCESS, 'QR Generated Successfully!')
