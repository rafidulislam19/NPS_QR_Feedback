from bs4 import BeautifulSoup
import random
import string
from django.utils.deprecation import MiddlewareMixin
class CSPNonceMiddleware(MiddlewareMixin):
  def generate_nonce(self):
          """Generate a random nonce for CSP."""
          return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
  def process_request(self, request):
          """Attach a nonce to the request."""
          nonce = self.generate_nonce()
          request.csp_nonce = nonce
  def process_response(self, request, response):
          """Add nonce to <script> and <style> tags and set CSP header."""
          if 'text/html' in response.get('Content-Type', ''):
                  nonce = request.csp_nonce
                  # Decode the response content
                  content = response.content.decode('utf-8')
                  # Parse HTML with BeautifulSoup
                  soup = BeautifulSoup(content, 'html5lib')
                  # Add nonce to all <script> and <style> tags
                  for tag in soup.find_all(['script', 'style', 'link']):
                          tag['nonce'] = nonce
                  # Convert the soup object back to a string
                  response.content = str(soup).encode('utf-8')
                  # Remove the Content-Length header to avoid mismatches
                  if 'Content-Length' in response:
                          del response['Content-Length']
                  # Add the CSP header with the nonce
                  response['Content-Security-Policy'] = (
                          f"script-src 'self' 'unsafe-eval'; "
                          f"style-src 'self' 'nonce-{nonce}';"
                          f"style-src-elem 'self' 'nonce-{nonce}';"
                          f"script-src-elem 'self' 'nonce-{nonce}';"
                  )
          return response

