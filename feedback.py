from django.shortcuts import render
from datetime import date, timedelta
from django import forms
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from feedbacks.forms import CustomerResponseForm
from feedbacks.models.sources import Source
import json


def feedback_request_handler(request, uuid):

    source_data = Source.objects.filter(id=uuid)

    if len(source_data) > 0:
        source_data = source_data[0]
        context = {
            'name': source_data.source_name,
            'id': source_data.id
        }

        # Check the source_type and load the appropriate template
        if source_data.source_type == 'ATM':
            template_name = 'customer_response_atm.html'
        elif source_data.source_type == 'BRANCH':
            template_name = 'customer_response_branch.html'
        else:
            # Handle the case where source_type is neither ATM nor Branch
            return render(
                request=request, 
                template_name='error.html', 
                context={
                    'page_title': 'Error',
                    'h3': 'Invalid Source Type',
                    'p': f'The source type "{source_data.source_type}" is not recognized.'
                }
            )

        if request.method == 'POST':
            data = json.dumps(request.POST)
            data = json.loads(data)
            
            reponse = data.copy()
            del reponse['csrfmiddlewaretoken'] 
            del reponse['source']
            data['response'] = reponse

            print(data)

            form = CustomerResponseForm(data)

            if form.is_valid():
                form.save()
                context['page_title'] = 'Service Fulfillment Confirmation'
                return render(request, 'submitted.html', context=context)
            else:
                print(form.errors)
    
        context['page_title'] = 'Service Fulfillment Survey'
        return render(request=request, template_name=template_name, context=context)
    
    return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': 'Resource not found', 
            'h3': 'Resource Not Found!',
            'p': f'Requested - {uuid}'
        }
    )


def http_403_custom(request, *args, **argv):
    return render(
        request=request,
        template_name='error.html',
        context={
            'page_title': '403 Forbidden',
            'h3': '403 Forbidden!',
            'p': 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'
        }
    )


def http_404_custom(request, *args, **argv):
    return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': '404 Not Found',
            'h3': '404 Page Not Found!',
            'p': request.build_absolute_uri ()
        }
    ) 


def http_500_custom(request, *args, **argv):
        return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': '500 Internal Server Error',
            'h3': '500 Internal Server Error!',
            'p': request.build_absolute_uri ()
        }
    ) 

