import logging 
logging.basicConfig(level='DEBUG')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
       logging.info('x_forwarder_for: ', x_forwarded_for)
    else:
       ip = request.META.get('REMOTE_ADDR')
       logging.info('REMOTE_ADDR: ', ip)
    return ip
