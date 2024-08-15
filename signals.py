import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.data_upload import DataUpload
from django.db.models import F
from .models.sources import Source
from helpers.generate_qr_admin import generate_qr_admin

@receiver(post_save, sender=DataUpload,  dispatch_uid="Upload_data")
def upload_data(sender, instance, created, **kwargs):
    if instance.file:          
        df = pd.read_excel(instance.file, dtype=str, index_col=False)
        for _, row in df.iterrows():
            source, created = Source.objects.get_or_create(source_id=row['ID'])
            print(source, created)
            if created:
                print(f"created: {row['ID']}")   
                source.source_address = row['ADDRESS'] 
                source.source_name = row['NAME']
                source.source_type = instance.source_type
                source_name = str(source.source_name)
                source_name = f"{source_name.replace(' ', '_').replace('/', '_')}"
                id = str(source.id)
                print("Printing SOURCE: ")
                print(source_name, id)
                success = generate_qr_admin(source_name, id)
                if success:
                    source.save()
            if not created and (source.source_address != row['ADDRESS']):
                print(f"Updating: {row['ID']}")
                source.source_address = row['ADDRESS']  
                source.source_name = row['NAME']
                source.source_type = instance.source_type
                source_name = str(source.source_name)
                source_name = f"{source_name.replace(' ', '_').replace('/', '_')}"
                id = str(source.id)
                print("Printing SOURCE: ")
                print(source_name, id)
                success = generate_qr_admin(source_name, id)
                if success:
                    source.save()               