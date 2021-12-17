# Umichi 21Fall SI 507 Final Project
Guowen Shao

Show different regions COVID-19 data on maps and plot some charts

Demo link (https://youtu.be/ok6veOSKuUw)

main files

       DataConstruct.py
       display.py
       
data

       covidData.json
       geoData.json
       
raw data

    in folder covidData
    
display html demo

    in folder display_demo
    

## Running environment

        python 3.8
    python package:
        json
        requests
        numpy
        os
        folium
        pyecharts
        webbrowser

## Data Source
    1. COVID-19 data from JHU CSSE on github (8 CSV files for 8 days)
        Source: [website](https://github.com/CSSEGISandData/COVID-19)
        
    2. Google Geocoding API (need authorized key)
        Using to get the latitude and longitude of a place
        Reference [website](https://developers.google.com/maps/documentation/geocoding/overview)
        API keys supply: sign up a google account, follow the step on the above website. There is a 300$ and 91 days free usage for new people.

## Rnning Step

1. Get data and reconstruct (optional)
    
        run DataConstruct.py, it will read 8 .csv files to get [countries, states, cities, date, confirmed, deaths] information.
    
        And set function main(updateloc = True), it will fetch the [latitude, longitude] information from Google Geocoding API. 
    
        Be patient, it will take quite a long time. 
    
        Then covid-19 data and geo data will be combined and reconstruct them in a tree construction, and save in covidData.json. 
    
        Additional, geo data will be saved seperately in tree construction to GeoData.json.
    
        Because all the data have been downloaded and saved, so this step is optional. Or used to update data. 
    
    
2. access and display data

    a. run display.py, it will save and open 4 .html file at first. include 
    
        (1) world confirmed and deaths map (data update 11-22-2021), 
        
        (2) world new cases and new deaths map (data update 11-23-2021), 
        
        (3) bar chart to display world new cases and deaths in 7 days (data include form 11-23-2021 to 11-29-2021), 
        
        (4) pie chart to display world different area percentage situation (data update 11-22-2021)
        
    b. Then can use command line to see details about a country/area (e. g. United States, China, Canada...), and also save and open 3 .html file. include
    
        (1) heatmap with label to show country/area confirmed and deaths (data update 11-22-2021), 
        
        (2) bar chart to display country/area new cases and deaths in 7 days (data include form 11-23-2021 to 11-29-2021), 
        
        (3) pie chart to display country/area different area percentage situation (data update 11-22-2021)
        
    c. Then user can enter 'e' to exit, or a state/province name to see more datails (e.g. Michigan, Texas...). It will show 2 .html file. include
    
        (1) heatmap with label to show state/province confirmed and deaths (data update 11-22-2021), 
        
        (2) bar chart to display state/province new cases and deaths in 7 days (data include form 11-23-2021 to 11-29-2021)
        
    d. User can enter 'e' to exit, or 'b' back to step b, or enter other state/province name

## Data Structure
    type: Trees
    
    covidData.json

    + -- country
        + -- state
            + -- city admin
                + -- latitude
                    + -- longitude
                        + -- date
                            + confirmed and deaths
    + -- United States
        + -- Michigan
            + -- Alger
                46.41292944	
                    -86.60260122
                        2021/11/23 4:22
                            [953, 9]
                        2021/11/23 4:2
                            [953, 9]
                        ...
            + -- Chippewa
                ...
        + -- Texas
            ...
        ...
    + -- China
    ...

    geoData.json
    
    + -- country
        + -- state
            + -- city admin
                + -- latitude and longitude

    + -- United States
        + -- Michigan
            + -- Alger
                [46.41292944, -86.60260122]
            + -- Chippewa
                ...
        + -- Texas
            ...
        ...
    + -- China
    ...



