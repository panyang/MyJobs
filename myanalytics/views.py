from django.http import HttpResponse
from pprint import pprint


def track(request):
    pprint(request.GET)
    return HttpResponse(status=200)

def track_pixel(request):
    #pprint(request.GET)
    print 'in pixel tracking view'
    pixel = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A
/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB90JExMWKvSLXnkAAAAZdEVYdENv
bW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAADUlEQVQI12P4//8/AwAI/AL+XJ/P2gAAAABJ
RU5ErkJggg=="""
    #return HttpResponse(r'P\x89GN\n\r\n\x1a\x00\x00\r\x00HIRD\x00\x00\x01\x00\x00\x00\x01\x00\x06\x08\x00\x00\x1f\x00\xc4\x15\x00\x89\x00\x00s\x01GR\x00B\xce\xae\xe9\x1c\x00\x00\x06\x00KbDG\xff\x00\xff\x00\xff\x00\xbd\xa0\x93\xa7\x00\x00\t\x00HpsY\x00\x00\x13\x0b\x00\x00\x13\x0b\x00\x01\x9c\x9a\x00\x18\x00\x00t\x07MI\x07E\t\xdd\x13\x13*\x16\x8b\xf4y^\x00\x00\x19\x00EttXoCmmne\x00trCaeet diwhtG MIWP\x0e\x81\x00\x17\x00\x00I\rAD\x08Tc\xd7\xff\xf8?\xff\x00\x03\xfc\x08\xfe\x02\x9f\\\xda\xcf\x00\x00\x00\x00EIDNB\xae\x82`', mimetype="image/png")
    return HttpResponse(pixel.decode('base64'), mimetype='image/png')
