from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'delhi'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d73718a25679291778e337344a076d9b'
    PARAMS = {'units': 'metric'}

    API_KEY = 'AIzaSyAPHC0jf4cVOA8Ro_vKnNysyrNmJxuj7VA'
    SEARCH_ENGINE_ID = '20f6c026508b14869'

    image_url = ''
    if API_KEY and SEARCH_ENGINE_ID:
        query = city + " 1920x1080"
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

        try:
            data = requests.get(city_url).json()
            search_items = data.get("items")
            if search_items and len(search_items) > 1:
                image_url = search_items[1]['link']
        except Exception as e:
            print("Image fetch failed:", e)

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })
