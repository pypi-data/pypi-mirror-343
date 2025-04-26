from bs4 import BeautifulSoup

from django.template.response import TemplateResponse


class TableofcontentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response: TemplateResponse):
        soup = BeautifulSoup(response.rendered_content, 'lxml')
        headers_tags = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
        headers = soup.find_all(headers_tags)
        toc_headers = []
        for header in headers:
            toc_headers.append({
                'name': header.name,
                'content': header.text,
                'ref': header.get('id'),
                'padding': int(header.name[1:]) * 2
            })
        response.context_data.update({'isTableOfContentMiddlewareConnected': True})
        response.context_data.update({'toc_headers': toc_headers})
        return response