import json
import requests

class readCSV:
    '''
    Obtain Covid informatino for JHU CSV.

    Parameters
    ----------
    filePath: str
        the name of the file

    Returns
    -------
    [country, city, update time, cases, deaths]: list 
    '''
    def __init__(self, rows=4006, cols=8):
        self.rows = rows
        self.cols = cols
        self.array = [[None]*self.cols for i in range(self.rows)]
        self.array1 = [[None]*self.cols for i in range(4)]

    def readFile(self, filePath):
        with open(filePath, encoding='utf-8', errors='ignore') as rf:
            line = rf.readline().rstrip('\n')
            rowCounter = 0
        # loop until all lines of the data have been read
            while line:
                items = line.split(",")
                colCounter = 0
                col = 0 
                if items[0] == 'FIPS':
                    line = rf.readline().rstrip('\n')
                else:
                    if col == 0:
                        self.array[rowCounter][2] = str(items[colCounter+1])
                        colCounter += 1
                        col += 1

                    if col == 1:
                        self.array[rowCounter][1] = str(items[colCounter+1])
                        colCounter += 1
                        col += 1
                        if self.array[rowCounter][1] == '"Bonaire':
                            self.array[rowCounter][1] = 'Bonaire, Sint Eustatius and Saba'
                            colCounter += 1  
                        if self.array[rowCounter][1] == '"Saint Helena':
                            self.array[rowCounter][1] = 'Saint Helena, Ascension and Tristan da Cunha'
                            colCounter += 1  

                    if col == 2:
                        self.array[rowCounter][0] = str(items[colCounter+1])
                        colCounter += 1
                        col += 1
                        if self.array[rowCounter][0] == 'US':
                            self.array[rowCounter][0] = 'United States'
                        if self.array[rowCounter][0] == 'South Sudan':
                            self.array[rowCounter][0] = 'S. Sudan'
                        if self.array[rowCounter][0] == 'Congo (Brazzaville)':
                            self.array[rowCounter][0] = 'Congo'
                        if self.array[rowCounter][0] == 'Congo (Kinshasa)':
                            self.array[rowCounter][0] = 'Dem. Rep. Congo'
                        if self.array[rowCounter][0] == 'Central African Republic':
                            self.array[rowCounter][0] = 'Central African Rep.'
                        if self.array[rowCounter][0] == '"Korea':
                            self.array[rowCounter][0] = 'Korea'
                            colCounter += 1
                    # print(self.array[rowCounter][0])
                
                    for col in range(3,5):
                        try:
                            self.array[rowCounter][col] = float(items[colCounter+2]) 
                        except:
                            self.array[rowCounter][col] = 0
                        colCounter += 1

                    for col in range(5,7):
                        self.array[rowCounter][col+1] = int(items[colCounter+2])
                        colCounter += 1
                    
                    self.array[rowCounter][5] = str(items[colCounter-3])
                    rowCounter += 1
                    line = rf.readline().rstrip('\n')
            return self.array

    def printData(self, debug=False):
        for row in range(self.rows):
            rowText = ''
            for col in range(3):
                rowText += str(self.array[row][col]) + ' '
            for col in range(5,8):
                rowText += str(self.array[row][col]) + ' '
            print (rowText)
            if debug and row==9:
                print('\t')
                break

def GoogleGeocodingAPI(address):
    '''
    Obtain latitude and longitude data from Google Geocoding API.

    Parameters
    ----------
    address: str
        the name of that area

    Returns
    -------
    lat, lng: float
    '''
    address.replace(" ", "%20")
    YOUR_API_KEY = 'AIzaSyAxttZmAOXOv4T-OZ64S5kFZYiA69mkUd8'
    baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    parameter = {"address": address, "key": YOUR_API_KEY}
    resp = requests.get(baseurl, parameter)
    results_object = resp.json()
    results = results_object["results"]
    if not results:
        print("\nSorry! No search result for your enter!")
    else:
        lat = results[0]["geometry"]["location"]["lat"]
        lng = results[0]["geometry"]["location"]["lng"]
        return lat, lng

def addloc(data):
    '''
    Add latitude and longitude data to Covid-19 data.

    Parameters
    ----------
    data: list
        Covid-19 data

    Returns
    -------
    [country, city, latitude, longitude, update time, cases, deaths]: list 
    '''
    for i in range(len(data)):
        if data[1] and data[2]:
            lat, lng = GoogleGeocodingAPI(data[i][2])
        elif data[1]:
            lat, lng = GoogleGeocodingAPI(data[i][1])
        else:
            lat, lng = GoogleGeocodingAPI(data[i][0])
        data[i][3] = lat
        data[i][4] = lng
    return data

class treeConstruct:
    """
    Generates a tree-based data structure (dictionary) from a list of lists of data

    Parameters
    ----------
    data: list
        multi Covid-19 data

    Returns
    -------
    tree-based data structure: dictionry

    """
    def __init__(self, data=None):
        self.data = data

    def generate_tree(self, data):
        """
        creates a tree-based data structure from a list
        """
        self.data = data
        list_of_dicts = [treeConstruct.list_to_dict(d) for d in self.data]
        general_dict = {}
        for dict_ in list_of_dicts:
            general_dict = treeConstruct.join_two_dicts(general_dict, dict_)

        return general_dict

    def join_two_dicts(general_dict, new_dict):
        """
        merges two dictionaries in a nested one
        """

        if isinstance(general_dict, dict) and isinstance(new_dict, dict):

            if set(new_dict).issubset(set(general_dict)):
                key = list(new_dict)[0]
                new_dict = {key: treeConstruct.join_two_dicts(general_dict[key], new_dict[key])}

            return {**general_dict, **new_dict}

        elif isinstance(general_dict, dict) or isinstance(new_dict, dict):

            raise Exception('Some leaf node missing!')

        else:

            return list(set(general_dict + new_dict))

    def list_to_dict(list_):
        """
        generates a (nested) dictionary from a list
        """

        if len(list_) == 0:
            dict_ = {}
        elif len(list_) == 1:
            dict_ = {list_[0]: []}
            # dict_ = {}
        elif len(list_) == 2:
            dict_ = {list_[0]: [list_[1]]}
        elif len(list_) == 3:
            dict_ = {list_[0]: [list_[1], list_[2]]}
        else:
            dict_ = {list_[0]: treeConstruct.list_to_dict(list_[1:])}

        return dict_

def main(updateloc = False):
    """
    Combine 8 days data into tree, and save data in to a JSON
    And save area location data into tree, save in another JSON
    """
    data = []

    for i in range(8):
        rc = readCSV()
        covidData = rc.readFile(filePath=(f'covidData/11-{i+22}-2021.csv'))
        if updateloc == True:
            data = addloc(covidData)
        data +=covidData

    tc = treeConstruct()
    output = tc.generate_tree(data)
    filename='covidData.json'
    with open(filename,'w') as file_obj:
        json.dump(output,file_obj)

    geodata = []
    for i in range(len(covidData)):
        geodata.append(covidData[i][:5])
    tc2 = treeConstruct()
    output2 = tc2.generate_tree(geodata)
    filename='geoData.json'
    with open(filename,'w') as file_obj:
        json.dump(output2,file_obj)

    # return covidData, geodata


if __name__ == "__main__":
    main()

