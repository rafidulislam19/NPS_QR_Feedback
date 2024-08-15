from uuid import uuid4
from django.db import models
from django.forms import ValidationError
from unfold.admin import ModelAdmin

class SourceType(models.TextChoices):
    ATM = "ATM", "ATM"
    BRANCH = "BRANCH", "Branch"

class DataUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    file = models.FileField(
        upload_to='BRANCH_DATA', 
        null=True,
        blank=True,
        default=None,
        help_text='''
            This is required to upload data to show growth graphs.
            <a href="/media/growth_excel/samples/SAMPLE_GROWTH_FORMAT.xlsx"> Sample CSV Sheet</a>
        '''
    )
    source_type = models.CharField(choices=SourceType.choices, max_length=50, default=SourceType.ATM)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        try:
            if self.file:
                if self.file.name.endswith('xlsx'):
                    if not self.file.size < int(5000000):
                        raise ValidationError("File size must not exceed 5 MB")
                else:
                    raise ValidationError("Please upload .xlsx extension files only")
                    
        except Exception as e:
            raise ValidationError(f"Invalid file: {str(e)}")

class DataUploadAdmin(ModelAdmin):
    search_fields = ("file", )
    ordering = ("-created", )
    list_display = [
        "id", 
        "file", 
        "source_type",
        "created", 
        "updated", 
    ]
    fields = ('file', 'source_type')
    
    
