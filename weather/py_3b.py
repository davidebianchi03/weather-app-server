import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

class Py3B:
    # function that returns list of weather forecast for 1 day
    def GetWeatherData(canonical: str, day: int):# day 0 is today, day 1 is tomorrow....
        if day == 0:
            place_page_path = "https://www.3bmeteo.com/meteo/" + canonical      # url to meteo weather forecast for the place passed as param
        else:
            if day > 0 and day < 7:
                place_page_path = "https://www.3bmeteo.com/meteo/" + canonical + "/dettagli_orari/" + str(day)
            else:
                raise Exception("Invalid day number, day range is 0-7")
        # get html page content
        request_result = requests.get(place_page_path)                
        response_dict = dict()
        # add status code to response dict
        response_dict["status_code"] = request_result.status_code

        if request_result.status_code == 200:
            soup = BeautifulSoup(request_result.text)
            # parse time slots
            list_time_slots = list()
            time_container_classes = "col-xs-1-4 big zoom_prv"
            time_div_list = soup.body.find_all('div', attrs={'class' : time_container_classes}) 
            time_div_list = time_div_list + soup.body.find_all('div', attrs={'class' : 'col-xs-1-4 big'})
            for time_div in time_div_list:
                list_time_slots.append(time_div.text)
            # print("time slots", len(list_time_slots))

            # parse weather icons
            weather_icons_list = list()
            weather_icon_container_classes = "col-xs-1-4 text-center no-padding zoom_prv"
            weather_icon_div_list = soup.body.find_all('div', attrs={'class' : weather_icon_container_classes}) 
            weather_icon_div_list = weather_icon_div_list + soup.body.find_all('div', attrs={'class' : 'col-xs-1-4 text-center no-padding'}) 
            for weather_icon in weather_icon_div_list:
                img_container = weather_icon.find("img")
                weather_icons_list.append(img_container["src"])
            # print("weather icon", len(weather_icons_list))

            # parse weather description
            weather_description_list = list()
            weather_description_container_classes = "col-xs-2-4"
            weather_description_div_list = soup.body.find_all('div', attrs={'class' : weather_description_container_classes}) 
            for weather_description in weather_description_div_list:
                weather_description_list.append(weather_description.text.replace(' ', '').replace('\n',''))
            # print("weather description", len(weather_description_list))


            # temperatures list
            list_temperature = list()
            temperature_container_div_classes = "col-xs-1-2 col-sm-1-5 big"
            temperature_container_div_list = soup.body.find_all('div', attrs={'class' : temperature_container_div_classes}) 
            for temperature_container_div in temperature_container_div_list:
                list_temperature.append(float(temperature_container_div.find('span').text.replace('°','')))
            # print("temperatures", len(list_temperature))
                
            # rainfall list
            rainfall_list = list()
            rainfall_container_classes = "col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active altriDati-precipitazioni altriDatiM-active"
                                         
            rainfall_div_list = soup.body.find_all('div', attrs={'class' : rainfall_container_classes}) 
            rainfall_div_list = rainfall_div_list + soup.body.find_all('div', attrs={'class' : "col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active hidden-xs altriDati-precipitazioni altriDatiM-active"}) 
            for rainfall_div in rainfall_div_list:
                span_container = rainfall_div.find('span')
                if not span_container == None:
                    rainfall_list.append(rainfall_div.find('span').text.replace('\n','').replace(' ', ''))
                else:
                    rainfall_str = ""
                    for c in rainfall_div.text:
                        if (ord(c) >= ord('0') and ord(c) <= ord('9')) or c == '.':
                            rainfall_str = rainfall_str + c
                    try:
                        rainfall_list.append(float(rainfall_str))
                    except:
                        pass
            # print("rainfall", len(rainfall_list))

            # wind list
            list_wind = list()
            wind_container_classes = "col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active altriDati-venti"
            wind_div_list = soup.body.find_all('div', attrs={'class' : wind_container_classes}) 
            wind_div_list = wind_div_list + soup.body.find_all('div', attrs={'class' : 'col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active altriDati-venti orario-allerta'}) 
            for wind_div in wind_div_list:
                wind_span_list = wind_div.find_all('span')
                if len(wind_span_list) > 0 and not wind_span_list[0] == None and not wind_span_list[1] == None:
                    wind_dict = dict()
                    wind_dict["speed"] = float(wind_span_list[0].text)
                    # get direction
                    direction_str = ""
                    for c in wind_div.text:
                        if ord(c) >= 65 and ord(c) <= 90:
                            direction_str = direction_str + c
                    wind_dict["direction"] = direction_str
                    list_wind.append(wind_dict)
            # print("wind", len(list_wind))
                    
            # humidity list
            list_humidity = list()
            humidity_container_classes = "col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active altriDati-umidita"
            humidity_div_list = soup.body.find_all('div', attrs={'class' : humidity_container_classes}) 
            for humidity_div in humidity_div_list:
                if not humidity_div == None:
                    text_str = humidity_div.text.replace('%', '')
                    try:
                        list_humidity.append(int(text_str))
                    except:
                        pass
            # print("humidity", len(list_humidity))

            # perceived temperature list
            list_perceived_temperature = list()
            perceived_temperature_classes = "col-xs-1-2 col-sm-1-5 altriDati altriDatiD-active altriDati-percepita"
            perceived_temperature_div_list = soup.body.find_all('div', attrs={'class' : perceived_temperature_classes}) 
            perceived_temperature_div_list = perceived_temperature_div_list + soup.body.find_all('div', attrs={'class' : "col-xs-1-2 col-sm-1-5 altriDati altriDati-percepita"}) 
            for perceived_temperature_div in perceived_temperature_div_list:
                try:
                    print
                    list_perceived_temperature.append(float(perceived_temperature_div.find_all('span')[0].text.replace('°', '')))
                except:
                    pass
            # print("perceived temperature", len(list_perceived_temperature))
                
            list_pressure = list()
            pressure_container_classes = "col-xs-1-2 col-sm-1-5 altriDati altriDati-pressione"
            pressure_div_list = soup.body.find_all('div', attrs={'class' : pressure_container_classes}) 
            for pressure_div in pressure_div_list:
                try:
                    list_pressure.append(float(pressure_div.text))
                except:
                    pass
            # print("pressure", len(list_pressure))

            if (
                len(list_time_slots) == len(weather_icons_list) and len(weather_icons_list) == len(list_temperature) and len(list_temperature) == len(rainfall_list) and
                len(rainfall_list) == len(list_wind) and len(list_wind) == len(list_humidity) and len(list_humidity) == len(list_perceived_temperature) and
                len(list_humidity) == len(weather_description_list)
              ):
                response_list = list()
                
                for i in range(len(list_time_slots)):
                    time_slot_dict = dict()
                    time_slot_dict["time_slot"] = list_time_slots[i]
                    time_slot_dict["weather_condition_icon_url"] = weather_icons_list[i]
                    time_slot_dict["weather_condition_description"] = weather_description_list[i]
                    time_slot_dict["temperature"] = list_temperature[i]
                    time_slot_dict["rainfall"] = rainfall_list[i]
                    time_slot_dict["wind"] = list_wind[i]
                    time_slot_dict["humidity"] = list_humidity[i]
                    time_slot_dict["perceived_temperature"] = list_perceived_temperature[i]
                    response_list.append(time_slot_dict)
                response_dict["weather_forecast"] = response_list
            else:
                response_dict["weather_forecast"] = []
                # print("not ok")
                # print("time slots", len(list_time_slots))
                # print("weather icon", len(weather_icons_list))
                # print("weather description", len(weather_description_list))
                # print("temperatures", len(list_temperature))
                # print("rainfall", len(rainfall_list))
                # print("wind", len(list_wind))
                # print("humidity", len(list_humidity))
                # print("perceived temperature", len(list_perceived_temperature))
                # print("pressure", len(list_pressure))
            return response_dict

    # function used to search places
    def SearchPlace(place: str):
        place = urllib.parse.quote_plus(place)
        place_page_path = "https://www.3bmeteo.com/search/search_localita/" + place
        request_result = requests.get(place_page_path)     
        if request_result.status_code == 200:
            place_list = json.loads(request_result.text)
            result_dict = dict()
            result_dict["status_code"] = 200
            result_dict["result"] = place_list

            # get latitude and longitude of searched place
            counter = 0
            for place in place_list:
                place_page_path = "https://www.3bmeteo.com/meteo/" + place["canonical"] 
                request_result = requests.get(place_page_path)
                if request_result.status_code == 200:
                    soup = BeautifulSoup(request_result.text)
                    latitude = soup.find('span', attrs={'id':'latitudine'}).text
                    longitude = soup.find('span', attrs={'id':'longitudine'}).text
                    result_dict["result"][counter]["lat"] = latitude
                    result_dict["result"][counter]["lon"] = longitude
                    sunset_request_result = json.loads(requests.get('https://api.sunrise-sunset.org/json?lat='+str(latitude)+'&lng='+str(longitude)+'&formatted=0').text)
                    
                    result_dict["result"][counter]["sunrise"] = sunset_request_result["results"]["sunrise"]
                    result_dict["result"][counter]["sunset"] = sunset_request_result["results"]["sunset"]
                counter = counter + 1

            return result_dict
        else:
            result_dict = dict()
            result_dict["status_code"] = request_result.status_code
            result_dict["result"] = list()
            return result_dict

    # function that returns
    def GetWeekForecast(canonical: str):
        place_page_path = "https://www.3bmeteo.com/meteo/" + canonical      # url to meteo weather forecast for the place passed as param
        print(place_page_path)
        # get html page content
        request_result = requests.get(place_page_path)                
        response_dict = dict()

        if request_result.status_code == 200:
            response_dict["status_code"] = request_result.status_code
            forecast_list = list()
            soup = BeautifulSoup(request_result.text)
            # parse time slots
            daily_forecast_list = list()
            week_forecast_container = soup.body.find('div', attrs={'id' : 'nav_giorni'})
            day_container_list = week_forecast_container.find_all('div', attrs={'class':'navDays'})
            
            for day_container in day_container_list:
                if not day_container == None and not day_container.find('img') == None:
                    day_forecast_dict= dict()
                    day_forecast_dict["day"] = day_container.find('div').text
                    day_forecast_dict["icon"] = day_container.find('img')["src"]
                    max_min_temperature_text= str(day_container.find('small').text).strip()
                    print(max_min_temperature_text)
                    try:
                        day_forecast_dict["min_temperature"] = float(max_min_temperature_text.split(' ')[0].replace('°',''))
                    except:
                        day_forecast_dict["min_temperature"] = None
                    try:
                        day_forecast_dict["max_temperature"] = float(max_min_temperature_text.split(' ')[1].replace('°',''))
                    except:
                        day_forecast_dict["max_temperature"] = None

                    forecast_list.append(day_forecast_dict)
            response_dict["forecast"] = forecast_list
            return response_dict
        
        response_dict["status_code"] = request_result.status_code
        response_dict["forecast"] = list()
        return response_dict

        
        
            
            