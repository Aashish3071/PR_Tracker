class DisableSSLRedirectMiddleware:
    """
    Middleware to disable SSL redirects in development.
    This overrides Django's SecurityMiddleware SSL redirect.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable the SSL redirect by setting the _secure attribute
        request._secure = False
        
        # Continue with the normal request/response cycle
        response = self.get_response(request)
        
        # If there's a redirect to HTTPS, change it to HTTP
        if response.status_code == 301 and response.get('Location', '').startswith('https:'):
            response['Location'] = response['Location'].replace('https:', 'http:', 1)
        
        return response 