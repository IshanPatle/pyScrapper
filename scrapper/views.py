from django.shortcuts import render
import os 
from django.http import HttpResponse    
from django.http import response
from django.shortcuts import render
from django.http import JsonResponse

import requests
import pandas as pd 
from bs4 import BeautifulSoup

from django.http import HttpResponseRedirect
from .forms import QueryForm
from .serializer import UserSerializer


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

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

# def search_results(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('search_query')
#         print(search_query)
#         # save businesses to database or Excel file
#         # return search results to user
#         return render(request, 'search/loader.html')

    
import requests
from django.shortcuts import render
from openpyxl import Workbook

def search_results(request):
    query = request.GET.get('query') # get the user's query from the GET parameters
    if query:
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {"accept": "application/json", 'Authorization': 'Bearer 91W-_HhIV_cJalivp6ChUNMZEul_amepQNmJqnjKp49mavL2pXJiNIBrp4BS95-skiNtOIlifMCZlcacZ9gxFRVWO7JSuZhR6hfMlofQKwSUwSIEPjiFhSNjlYtFZHYx'}
        businesses = []
        for offset in range(0, 100, 20):
            params = {
                'term': query,
                'location': 'Australia',
                'offset': offset
            }
        # params = {'term': query, 'location': 'Australia'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        businesses.extend(data['businesses'])
    else:
        data = []
    return render(request, 'loader.html')



def save_to_excel(request):
    data = request.GET.getlist('data') # get the search results from the GET parameters
    wb = Workbook()
    ws = wb.active
    ws.append(['Name', 'Rating', 'Address', 'Phone'])
    for result in data[:50]:
        ws.append([result['name'], result['rating'], f"{result['location']['address1']}, {result['location']['city']}, {result['location']['state']}", result['phone']])
    filename = 'search_results.xlsx'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
    