from django.views.generic import TemplateView
from destinations.models import Destination, DestinationImage
from cities_light.models import City
import requests
from django.utils import timezone


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        city_name = 'Karachi'

        city = City.objects.get(name=city_name)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ab1511265be0e3512b8a68c06a71358f'
        city_weather = requests.get(url.format(city_name)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        destination = Destination.objects.filter(city=city).order_by(
            '-created')[:5]
        city_data = DestinationImage.objects.filter(
            destination=destination.first()).first()
        context['city_locations'] = destination
        context['city_data'] = city_data
        context['weather'] = weather
        context['now'] = timezone.now().hour
        print(timezone.now())

        return context
