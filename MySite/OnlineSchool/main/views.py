from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Students, Courses, Lessons, Teachers, RecordsStudents
from django.contrib import messages
from django.conf import settings
import logging
from django.contrib.auth.hashers import make_password
import re
from django.core.exceptions import ValidationError
import io
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string


def index(request):
    return render(request, 'main/main_page.html')

