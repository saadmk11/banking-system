from django.shortcuts import render

class LoadingAnimationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)

        if request.path in ['/transactions/deposit/', '/transactions/report/', '/transactions/withdraw/', '/transactions/transfer/']:
            print(response)
            # response.content_type = 'text/html'
            response['X-Loading-Animation'] = 'on'
            return render(request, '../templates/animations/loading.html')
        else:
            print(request.path)

        return response
