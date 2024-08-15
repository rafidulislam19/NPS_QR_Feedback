from django.contrib import admin
from .models.sources import Source, SourceAdmin
from .models.data_upload import DataUpload, DataUploadAdmin
from .models.customer_responses import CustomerResponses, CustomCustomerResponseAdmin
from .models.questions import Question, QuestionAdmin


admin.site.register(Source, SourceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(DataUpload, DataUploadAdmin)
admin.site.register(CustomerResponses, CustomCustomerResponseAdmin)