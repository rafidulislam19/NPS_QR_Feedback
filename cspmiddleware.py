import random
import string
from django.utils.deprecation import MiddlewareMixin
class CSPNonceMiddleware(MiddlewareMixin):
    def generate_nonce(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    def process_request(self, request):
        nonce = self.generate_nonce()
        request.csp_nonce = nonce
        return None
    def process_response(self, request, response):
        if hasattr(request, 'csp_nonce'):
            nonce = request.csp_nonce
            # Inject the nonce into the CSP header
            csp_header = (
                f"script-src 'self' 'unsafe-eval'; "
                f"style-src 'self' 'nonce-{nonce}';"
                f"style-src-elem 'self' 'nonce-{nonce}';"
                f"script-src-elem 'self' 'nonce-{nonce}';"
            )
            response['Content-Security-Policy'] = csp_header
            
            # Apply the nonce to inline scripts and styles in the response content
            if response.get('Content-Type', '').startswith('text/html'):
                content = response.content.decode('utf-8')
                content = content.replace('<script', f'<script nonce="{nonce}"')
                content = content.replace('<style', f'<style nonce="{nonce}"')
                content = content.replace('<link', f'<link nonce="{nonce}"')
                response.content = content.encode('utf-8')
         #   content = response.content.decode('utf-8')
          #  content = content.replace('<script', f'<script nonce="{nonce}">').replace('<style', f'<style nonce="{nonce}">')
           # response.content = content.encode('utf-8')
        return response
