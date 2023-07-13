def get_serp_results(request):
    # Serp API endpoint and parameters
    api_key = 'ab5c8496b40ee68d2b887dc8587cdb62b0f538ad87b479ae1374280242ef084c'
    query = request.GET.get('q', '')  # Get the query entered by the user
    search_engine = 'google_maps'
    num_results = 30  # Number of results to retrieve

    # Extract the number and location from the query using regular expressions
    number_match = re.search(r'\b(\d+)\b', query)
    location_match = re.search(r'in\s+([^,]+)', query)

    number = int(number_match.group(1)) if number_match else num_results
    location = location_match.group(1).strip() if location_match else ''  # Default location if not specified

    map_results = []  # List to store all the results
    
    # Perform pagination to retrieve the desired number of results
    start = 0
    while number > 0:
        # Adjust the start value to be a multiple of 20
        start = (start // 20) * 20
        
        # Calculate the number of results to request for this iteration
        results_per_page = min(number, 20)
        
        # Create the API URL with the updated start value and number of results
        url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&location={location}&start={start}&num={results_per_page}&api_key={api_key}"
        print(url)
        try:
            response = requests.get(url)
            data = response.json()
            # Extract the local results from the response
            local_results = data.get('local_results', [])
            
            # Append the local results to the main results list
            map_results.extend(local_results)
        except requests.RequestException as e:
            # Handle request exception
            map_results = []
            break
        
        number -= results_per_page
        start += results_per_page

    return map_results







# somehat working while to load multiple results 
def get_serp_results(request):
    
    # Serp API endpoint and parameters
    global map_results  
    map_results= []
    start = 0
    api_key = '002ae278dd8df72fa9a4125af4e40c9c5fcc96cae780f08de4a1d48b5d3fac86'
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
        ll = f"@{lat},{lng},20z"
    except requests.RequestException as e:
        # Handle request exception
        data_geo = None
    
    
    # url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&api_key={api_key}"
    while len(map_results) < number:
        remaining_results = number - len(map_results)  # Calculate the remaining number of results needed
        batch_size = min(20, remaining_results)
        url = f"https://serpapi.com/search.json?engine={search_engine}&q={query}&api_key={api_key}&start={start}&ll={ll}"
        try:
            response = requests.get(url)
            data = response.json()
            batch_results = data.get('local_results', [])
            map_results.extend(batch_results)
            start += batch_size
        except requests.RequestException as e:
            break
    
    map_results = map_results[:number]
    return map_results