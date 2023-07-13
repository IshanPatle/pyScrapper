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
    map_results= []
    start = 0
    # api_key = '7fdb7a9b8d8007d43e10d5c8698a834b0528bc41455c0fe3c7f5b87f6ac415c2' #support -PCon
    api_key = 'cfc8631972b4920cdcc97dd41a3a6a6528503b604a8381a5c6603e7788befde9' 
    # '002ae278dd8df72fa9a4125af4e40c9c5fcc96cae780f08de4a1d48b5d3fac86' - L of i
    # '91039cff9059ebf9f60e7189fe10ac358d028eacb52e4bde52831b17a2314f77' - zep.peg
    query = request.GET.get('q', '')  
    search_engine = 'google_maps'
    num_results = 20

    number_match = re.search(r'\b(\d+)\b', query)
    location_match = re.search(r'in\s+([^,]+)', query)

    number = int(number_match.group(1)) if number_match else num_results
    location = location_match.group(1).strip() if location_match else ''  # Default location if not specified
    
    #Open cage API parameters
    q = location
    key = 'be3984f8e5a042abbf6af3a3a8d5c604'
    geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={q}&key={key}&language=en"
    try:
        response_geo = requests.get(geo_url)
        data_geo = response_geo.json()
        lat = data_geo["results"][0]["geometry"]["lat"]
        lng = data_geo["results"][0]["geometry"]["lng"]
        ll = f"@{lat},{lng},21z"
    except requests.RequestException as e:
        # Handle request exception
        data_geo = None
    
    
    # url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&api_key={api_key}"
    while start < number: 
        remaining_results = number - len(map_results)  # Calculate the remaining number of results needed
        batch_size = min(20, remaining_results)
        url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&api_key={api_key}&start={start}&ll={ll}"
        try: 
            response = requests.get(url)
            data = response.json()
            batch_results = data.get('local_results', [])
            map_results.extend(batch_results)
            start += 20
        except requests.RequestException as e:
            break
    
    map_results = map_results[:number]
    return map_results


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



