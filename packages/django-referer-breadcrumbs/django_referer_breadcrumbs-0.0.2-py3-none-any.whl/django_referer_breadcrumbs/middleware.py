from urllib.parse import urlparse
from django.template.response import TemplateResponse


class BreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def remove_items(self, list, item): 
        # remove the item for all its occurrences 
        c = list.count(item) 
        for i in range(c): 
            list.remove(item) 
        return list 

    def process_template_response(self, request, response: TemplateResponse):
        ref_url = request.META.get('HTTP_REFERER')
        urls = []
        if ref_url: 
            parsed_url = urlparse(ref_url)
            folders_url = self.remove_items(parsed_url.path.split('/'),'')
            if len(parsed_url.query) > 0:
                folders_url.append(f'?{parsed_url.query}')

            current_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            for folder in folders_url:
                current_url += folder + '/'
                urls.append({
                    'path': current_url,
                    'name': folder
                })
            # Removing last '/' from the last element
            if len(parsed_url.query) > 0:
                urls[-1]['path'] = urls[-1]['path'][:-1]

        if response.context_data is not None:
            response.context_data.update({'isBreadcrumbsMiddlewareConnected': True})
            response.context_data.update({'breadcrumbs_urls': urls})
        return response