from django.http import HttpResponse


def track(request):
    pixel = 'R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==\n'
    return HttpResponse(pixel.decode('base64'), content_type='image/gif')
