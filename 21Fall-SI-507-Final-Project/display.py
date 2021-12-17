import json
import numpy as np
import os
import folium
from folium.plugins import HeatMap
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Pie, Geo
from pyecharts.globals import ChartType
import webbrowser as web


def readCovidData():
    with open("covidData.json",'r') as load_f:
        data = json.load(load_f)

    countries = list(data.keys())

    countries_loc = []
    countries_lat = []
    countries_lng = []
    countries_day_cases = []
    countries_day_deaths = []

    for country in data.keys():
        country_day_cases = np.zeros(8)
        country_day_deaths = np.zeros(8)
        for state in data[country].keys():
            state_day_cases = np.zeros(8)
            state_day_deaths = np.zeros(8)
            for city in data[country][state].keys():
                city_lat = list(data[country][state][city].keys())[0]
                city_lng = list(data[country][state][city][city_lat].keys())[0]
                city_day_cases = []
                city_day_deaths = []
                last_cases = 0
                last_deaths = 0
                days = list(data[country][state][city][city_lat][city_lng].keys())
                for day in data[country][state][city][city_lat][city_lng]:
                    city_last_cases = data[country][state][city][city_lat][city_lng][day][0]
                    city_last_deaths = data[country][state][city][city_lat][city_lng][day][-1]
                    day_cases = (city_last_cases) - last_cases
                    day_deaths = (city_last_deaths) - last_deaths
                    city_day_cases.append(day_cases)
                    city_day_deaths.append(day_deaths)
                    last_cases = (city_last_cases)
                    last_deaths = (city_last_deaths)
                
                state_day_cases += np.array(city_day_cases)
                state_day_deaths += np.array(city_day_deaths)

            country_day_cases += np.array(state_day_cases)
            country_day_deaths += np.array(state_day_deaths)

        countries_day_cases.append(country_day_cases)
        countries_day_deaths.append(country_day_deaths)
        country_loc=[float(city_lat), float(city_lng)]
        countries_loc.append(country_loc)
        countries_lat.append(float(city_lat))
        countries_lng.append(float(city_lng))

    return countries, countries_loc, countries_lat, countries_lng, np.array(countries_day_cases), np.array(countries_day_deaths), days

def countryData(country):
    with open("covidData.json",'r') as load_f:
        data = json.load(load_f)
    states = list(data[country].keys())
    states_loc = []
    states_lat = []
    states_lng = []
    states_day_cases = []
    states_day_deaths = []
    for state in data[country].keys():
        state_day_cases = np.zeros(8)
        state_day_deaths = np.zeros(8)
        for city in data[country][state].keys():
            city_lat = list(data[country][state][city].keys())[0]
            city_lng = list(data[country][state][city][city_lat].keys())[0]
            city_day_cases = []
            city_day_deaths = []
            last_cases = 0
            last_deaths = 0
            for day in data[country][state][city][city_lat][city_lng]:
                city_last_cases = data[country][state][city][city_lat][city_lng][day][0]
                city_last_deaths = data[country][state][city][city_lat][city_lng][day][-1]
                day_cases = (city_last_cases) - last_cases
                day_deaths = (city_last_deaths) - last_deaths
                city_day_cases.append(day_cases)
                city_day_deaths.append(day_deaths)
                last_cases = (city_last_cases)
                last_deaths = (city_last_deaths)
            
            state_day_cases += np.array(city_day_cases)
            state_day_deaths += np.array(city_day_deaths)
        states_day_cases.append(state_day_cases)
        states_day_deaths.append(state_day_deaths)
        state_loc=[float(city_lat), float(city_lng)]
        states_loc.append(state_loc)
        states_lat.append(float(city_lat))
        states_lng.append(float(city_lng))
    return states, states_loc, states_lat, states_lng, np.array(states_day_cases), np.array(states_day_deaths)

def stateData(country, state):
    with open("covidData.json",'r') as load_f:
        data = json.load(load_f)
    cities = list(data[country][state].keys())
    citys_loc = []
    citys_lat = []
    citys_lng = []
    citys_day_cases = []
    citys_day_deaths = []

    for city in data[country][state].keys():
        city_lat = list(data[country][state][city].keys())[0]
        city_lng = list(data[country][state][city][city_lat].keys())[0]
        city_day_cases = []
        city_day_deaths = []
        last_cases = 0
        last_deaths = 0
        for day in data[country][state][city][city_lat][city_lng]:
            city_last_cases = data[country][state][city][city_lat][city_lng][day][0]
            city_last_deaths = data[country][state][city][city_lat][city_lng][day][-1]
            day_cases = (city_last_cases) - last_cases
            day_deaths = (city_last_deaths) - last_deaths
            city_day_cases.append(day_cases)
            city_day_deaths.append(day_deaths)
            last_cases = (city_last_cases)
            last_deaths = (city_last_deaths)
        citys_day_cases.append(city_day_cases)
        citys_day_deaths.append(city_day_deaths)
        city_loc=[float(city_lat), float(city_lng)]
        citys_loc.append(city_loc)
        citys_lat.append(float(city_lat))
        citys_lng.append(float(city_lng))
    return cities, citys_loc, citys_lat, citys_lng, np.array(citys_day_cases), np.array(citys_day_deaths)

def readGeoData():
    with open("geoData.json",'r') as load_f:
        geodata = json.load(load_f)
    return geodata

def showmap(scale, area, data, name):
    scale=str.lower(scale)
    map = Map()
    map.add(name[0], [list(z) for z in zip(area, data[0])], scale, is_map_symbol_show=False)
    map.add(name[1], [list(z) for z in zip(area, data[1])], scale, is_map_symbol_show=False)
    map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map.set_global_opts(
        title_opts=opts.TitleOpts(title=(scale)),
        visualmap_opts=opts.VisualMapOpts(max_=max(data[0]), min_=min(data[1])),
    )
    map.render(scale+'_'+name[0]+'_'+name[1]+".html")
    web.open('file://' + os.path.realpath(scale+'_'+name[0]+'_'+name[1]+".html"))

def showbar(scale, days, data, name):
    bar = Bar()
    bar.add_xaxis(days)
    bar.add_yaxis(name[0], data[0])
    bar.add_yaxis(name[1], data[1])
    # bar.add_yaxis(name[2], data[2])
    # bar.add_yaxis(name[3], data[3])
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title=scale),
    )
    bar.render('bar_'+scale+'.html')
    web.open('file://' + os.path.realpath('bar_'+scale+'.html'))

def showpie(scale, area, data, name):
    pie = Pie()
    pie.add(series_name='',data_pair=[list(z) for z in zip(area, data)])
    pie.set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=scale+'-'+name),
        )
    pie.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    pie.render('pie_'+scale+name+'.html')
    web.open('file://' + os.path.realpath('pie_'+scale+name+'.html'))

def showgeo(scale, area, data, name):
    geo = Geo()
    geo.add_schema(maptype=scale)
    geo.add(
        "geo",
        [list(z) for z in zip(area, data)],
        type_=ChartType.HEATMAP,
        )
    geo.set_global_opts(title_opts=opts.TitleOpts(title=scale+'-'+name))
    geo.render("geo_"+scale+"_"+name+".html")

def showhm(lat, lng, data, name, locs, zoom=4):
    m = folium.Map(location=[lat[0], lng[0]], zoom_start = zoom)
    data = data.tolist()
    HeatMap([list(z) for z in zip(lat, lng, data)]).add_to(m)
    for i in range(len(lat)):
        folium.Marker([lat[i], lng[i]],popup=f'{name}-{locs[i]}:{data[i]}').add_to(m) 
    m.save(name+'.html')
    web.open('file://' + os.path.realpath(name+'.html'))

if __name__ == '__main__':
    countries, countries_loc, countries_lat, countries_lng, countries_day_cases, countries_day_deaths, days= readCovidData()
    geodata = readGeoData()
    showmap("world", countries, [countries_day_cases[:, 0],countries_day_deaths[:, 0]], ["confirmed cases", "confiremd deaths"])
    showmap("world", countries, [countries_day_cases[:, 1],countries_day_deaths[:, 1]], ["new cases", "new deaths"])
    showpie("world", countries, countries_day_cases[:, 0], 'confirmed cases')
    showbar("world", days[1:], [list((np.sum(countries_day_cases,axis=0))[1:]),list((np.sum(countries_day_deaths,axis=0))[1:])], ["new cases", "new deaths"])
    
    while True:
        try:
            country = input("Choose a country to show more details, or e(xit):    ")
            states, states_loc, states_lat, states_lng, states_day_cases, states_day_deaths = countryData(country)
            showhm(states_lat, states_lng, states_day_cases[:,0], (country+'_confirmed_cases'), states)
            showbar(country, days[1:], [list((np.sum(states_day_cases,axis=0))[1:]),list((np.sum(states_day_deaths,axis=0))[1:])], ["new cases", "new deaths"])
            showpie(country, states, states_day_cases[:, 0], 'confirmed cases')
            while True:
                try:
                    state = input("Choose a state to show more details, or e(xit), or b(ack):    ")
                    cities, cities_loc, cities_lat, cities_lng, cities_day_cases, cities_day_deaths = stateData(country, state)
                    showhm(cities_lat, cities_lng, cities_day_cases[:,0], ('state_conf_cases'), cities, zoom=6)
                    showbar(state, days[1:], [(np.sum(cities_day_cases,axis=0)[1:]).tolist(),(np.sum(cities_day_deaths,axis=0)[1:]).tolist()], ["new cases", "new deaths"])

                except:
                    if state =='e':
                        country = 'e'
                        os._exit()
                    elif state == 'b':
                        break
                    else:
                        print("A wrong state name!")
        except:
            if country == "e":
                break
            else:
                print("A wrong country name!")

