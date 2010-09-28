from django.shortcuts import render_to_response

__author__ = 'sybarite'

def test(request):
    return render_to_response('test.html', {'params': request})


  