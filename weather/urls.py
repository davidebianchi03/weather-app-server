from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dayforecast', views.GetWeatherForecast, name = "weather_forecast_api"),
    path('weekforecast', views.WeekForecastView, name = 'search_place_view'),
    path('searchplace', views.SearchPlaceView, name = 'search_place_view'),
]
