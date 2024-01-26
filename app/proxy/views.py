import re
import requests
from django.http import HttpResponse, HttpRequest
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from urllib.parse import urlparse, urljoin
from django.urls import reverse_lazy
from sites.models import Site
from tldextract import tldextract


class ProxyIndexView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        url = request.GET.get('url', '')
        if not url:
            return HttpResponse('No url specified', status=400)
        pk = request.GET.get('pk', '')
        if not pk:
            return HttpResponse('No pk specified', status=400)
        site = Site.objects.get(pk=pk)
        if request.user != site.user:
            return HttpResponse('You are not owner of this site', status=400)

        requests_args = (args or {'headers': {'accept-encoding': 'text/html'}}).copy()
        headers = self.get_headers(request.META)
        params = request.GET.copy()

        if 'headers' not in requests_args:
            requests_args['headers'] = {}
        if 'data' not in requests_args:
            requests_args['data'] = request.body
        if 'params' not in requests_args:
            requests_args['params'] = QueryDict('', mutable=True)

        # Overwrite any headers and params from the incoming request with explicitly
        # specified values for the requests library.
        headers.update(requests_args['headers'])
        params.update(requests_args['params'])

        # If there's a content-length header from Django, it's probably in all-caps
        # and requests might not notice it, so just remove it.
        for key in list(headers.keys()):
            if key.lower() == 'content-length':
                del headers[key]

        requests_args['headers'] = headers
        requests_args['params'] = params

        response = requests.request(request.method, url, **requests_args)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        modified_content = response.content
        view_link = reverse_lazy('proxy:index')

        def replace_url(match):
            matched_url = match.group(1)

            matched_url_netloc = urlparse(matched_url).netloc
            matched_url_domain = tldextract.extract(matched_url).domain
            url_domain = tldextract.extract(url).domain
            if matched_url_domain == url_domain:
                pass
            elif matched_url_netloc:
                return f'href="{matched_url}"'
            else:
                matched_url = urljoin(url, matched_url)
            replacement_url = f'href="{view_link}?url={matched_url}&pk={pk}"'
            return replacement_url

        # Decode the content using the correct encoding
        if encoding is not None:
            modified_content = re.sub(r'href="([^"]+)"', replace_url, modified_content.decode(encoding)).encode(encoding)
        else:
            modified_content = response.text

        proxy_response = HttpResponse(
            modified_content,
            status=response.status_code
        )

        excluded_headers = set([
            'connection', 'keep-alive', 'proxy-authenticate',
            'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
            'upgrade',
            'content-encoding',

            # Let Django set content-length
            'content-length',
        ])
        for key, value in response.headers.items():
            if key.lower() in excluded_headers:
                continue
            elif key.lower() == 'location':
                # If the location is relative at all, we want it to be absolute to
                # the upstream server.
                proxy_response[key] = self.make_absolute_location(response.url, value)
            else:
                proxy_response[key] = value

        site.visiting_count += 1
        site.data_volume += len(modified_content) + len(request.body)
        site.save()

        return proxy_response

    def make_absolute_location(self, base_url, location):
        """
        Convert a location header into an absolute URL.
        """
        absolute_pattern = re.compile(r'^[a-zA-Z]+://.*$')
        if absolute_pattern.match(location):
            return location

        parsed_url = urlparse(base_url)

        if location.startswith('//'):
            # scheme relative
            return parsed_url.scheme + ':' + location

        elif location.startswith('/'):
            # host relative
            return parsed_url.scheme + '://' + parsed_url.netloc + location

        else:
            # path relative
            return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path.rsplit('/', 1)[0] + '/' + location

        return location

    def get_headers(self, environ):
        """
        Retrieve the HTTP headers from a WSGI environment dictionary.  See
        https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
        """
        headers = {}
        for key, value in environ.items():
            # Sometimes, things don't like when you send the requesting host through.
            if key.startswith('HTTP_') and key != 'HTTP_HOST':
                headers[key[5:].replace('_', '-')] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                headers[key.replace('_', '-')] = value

        return headers
