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

def get_serp_results(request):
    
    # Serp API endpoint and parameters
    api_key = 'ab5c8496b40ee68d2b887dc8587cdb62b0f538ad87b479ae1374280242ef084c'
    query = request.GET.get('q', '')  # Get the query entered by the user
    search_engine = 'google_maps'
    num_results = 10  # Number of results to retrieve

    # Extract the number and location from the query using regular expressions
    number_match = re.search(r'\b(\d+)\b', query)
    location_match = re.search(r'in\s+([^,]+)', query)

    number = int(number_match.group(1)) if number_match else num_results
    location = location_match.group(1).strip() if location_match else ''  # Default location if not specified

    url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&location={location}&num={number}&api_key={api_key}"
    print(url)
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


def save_to_excel(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        search_results = get_serp_results(request)
        
        # Create a DataFrame from the search results
        df = pd.DataFrame(search_results)
        
        # Select the desired columns
        columns = ['title', 'website', 'rating', 'address', 'phone']
        
        # Save the DataFrame to an Excel file
        filepath = 'search_results.xlsx'
        df.to_excel(filepath, index=False)
        
        # Prepare the response for file download
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="search_results.xlsx"'
    
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




# def search_results(request):
#     query = request.GET.get('query') # get the user's query from the GET parameters
#     if query:
#         url = "https://serpapi.com/search"
#         businesses = []
#         params={
#                 'location': query.split('in ')[-1],
#                 'term': query.split('in ')[0],
#                 'limit': 50
#                 }
#         # params = {'term': query, 'location': 'Australia'}
#         response = requests.get(url, headers=headers, params=params)
#         data = response.json()['businesses']
#         print(data)
        
#         df = pd.DataFrame(columns=['Name', 'Rating', 'Address', 'Phone'])
#         for business in data:
#             name = business['name']
#             rating = business['rating']
#             address = ', '.join(business['location']['display_address'])
#             phone = business['display_phone']
#             df = df.append({'Name': name, 'Rating': rating, 'Address': address, 'Phone': phone}, ignore_index=True)
#         # convert dataframe to excel file
#         excel_file = df.to_excel('results.xlsx', index=False)
#         # return rendered response
#         context = {'data': data}
#         return render(request, 'loader.html', context)
#     else:
#         return render(request, 'index.html')


# def save_to_excel(request):
#     file_path = 'results.xlsx'
#     with open(file_path, 'rb') as fh:
#         response = HttpResponse(fh.read(), content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=' + file_path.split('/')[-1]
#         return response