from django.forms import ModelForm
from feedbacks.models.customer_responses import CustomerResponses

class CustomerResponseForm(ModelForm):
    class Meta:
        model = CustomerResponses
        exclude = ['created', 'updated']