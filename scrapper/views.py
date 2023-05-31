from django.shortcuts import render
import os 
from django.http import HttpResponse    
from django.http import response
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd 
import re 
from django.http import HttpResponseRedirect
from .forms import QueryForm
from .serializer import UserSerializer

from openpyxl import Workbook  
import requests
from googlesearch import search
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from django.db.models import Q
from django.shortcuts import render
from .models import Faq

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

def index(request):
    return render(request, 'index.html')

def faq(request):
    return render(request, 'faq.html')

def loader(request):
    return render(request, 'loader.html')

def login(request):
    return render(request, 'login.html')

map_results = []

def get_serp_results(request):
    
    # Serp API endpoint and parameters
    global map_results  
    api_key = 'ab5c8496b40ee68d2b887dc8587cdb62b0f538ad87b479ae1374280242ef084c'
    query = request.GET.get('q', '')  # Get the query entered by the user
    search_engine = 'google_maps'
    num_results = 30  # Number of results to retrieve

    # Extract the number and location from the query using regular expressions
    number_match = re.search(r'\b(\d+)\b', query)
    location_match = re.search(r'in\s+([^,]+)', query)

    number = int(number_match.group(1)) if number_match else num_results
    location = location_match.group(1).strip() if location_match else ''  # Default location if not specified

    url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&location={location}&num={number}&api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        map_results = data.get('local_results', [])
    except requests.RequestException as e:
        # Handle request exception
        map_results = []
    return map_results;

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            results = get_serp_results(request)
            context = {'results': results}
            return render(request, 'loader.html', context)
    return render(request, 'index.html')

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from django.http import HttpResponse
from openpyxl import Workbook


from openpyxl import Workbook

def save_to_excel(request):
    global map_results
    # Create a new Excel workbook
    wb = Workbook()
    sheet = wb.active

    # Add headers to the sheet
    headers = ['Name', 'Website', 'Rating', 'Address', 'Phone']
    sheet.append(headers)

    # Populate the data in the sheet
    for result in map_results:
        row_data = [result.get('title'), result.get('website'), result.get('rating'), result.get('address'), result.get('phone')]
        sheet.append(row_data)

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=serp_results.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response




def search_faq(request):
    # Get search query from GET parameters
    query = request.GET.get('q')

    if query:
        # Search for Faq objects that match the query
        results = Faq.objects.filter(
            Q(question__icontains=query) | Q(answer__icontains=query)
        )
    else:
        results = None

    # Render the search results in the search_faq.html template
    return render(request, 'faq.html', {'results': results})



