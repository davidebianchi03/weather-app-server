from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from weather.py_3b import Py3B

# Create your views here.
@csrf_exempt
def GetWeatherForecast(request):
    canonical = request.GET.get('canonical')
    index = request.GET.get('index')
    if not canonical == None and not canonical == "" and not index == None:
        # try to parse index
        try:
            index = int(index)
            forecast = Py3B.GetWeatherData(canonical, index)
            return JsonResponse(forecast, safe=False)
        except:
            return HttpResponseBadRequest("missing parameter or parameter invalid type GET /dayforecast?canonical=[canonical_str]&index=[index_int]")
    return HttpResponseBadRequest("missing parameter or parameter invalid type GET /dayforecast?canonical=[canonical_str]&index=[index_int]")

@csrf_exempt
def WeekForecastView(request):
    canonical = request.GET.get('canonical')
    if not canonical == None and not canonical == "":
        return JsonResponse(Py3B.GetWeekForecast(canonical), safe=False)
    return HttpResponseBadRequest("missing parameter GET /searchplace?canonical=[canonical]")
    

@csrf_exempt
def SearchPlaceView(request):
    place = request.GET.get('place')
    if not place == None and not place == "":
        places = Py3B.SearchPlace(place)
        return JsonResponse(places, safe=False)
    return HttpResponseBadRequest("missing parameter GET /searchplace?place=[place_str]")