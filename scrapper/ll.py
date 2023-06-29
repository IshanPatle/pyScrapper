# import requests 

# q = 'New Zealand'
# key = 'be3984f8e5a042abbf6af3a3a8d5c604'
# geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={q}&key={key}&language=en"
# try:
#     response_geo = requests.get(geo_url)
#     data_geo = response_geo.json()
#     lat = data_geo["results"][0]["geometry"]["lat"]
#     lng = data_geo["results"][0]["geometry"]["lng"]
#     ll = f"@{lat},{lng},20z"
# except requests.RequestException as e:
#     # Handle request exception
#     data_geo = None
    
# print(ll)

# import re
# query = '50 ios developers in london'
# location_match = re.search(r'in\s+([^,]+)', query)
# print(location_match)


import spacy

nlp = spacy.load("en_core_web_sm")
user_query = "Find restaurants in Brisbane"
doc = nlp(user_query)
locations = [entity.text for entity in doc.ents if entity.label_ in ["LOC", "GPE"]]
for location in locations:
    print(location)
