# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.contrib.staticfiles.views import serve


def static_file(request, fname):
    result = serve(request, fname)
    return result


def index(request):
    return render_to_response("index.html")
