import pandas as pd 
import requests

class vaAPI(object):

    """ Class to pull links to images from Victoria and Albert API
    for more documentation, see http://www.vam.ac.uk/api/
    """

    def __init__(self, before, after, limit = 45, img = 1, offset = 1):

        self.base = 'http://www.vam.ac.uk/api/json/museumobject/'
        self.param = {'before' : before, 'after' : after, 
            'limit' : limit, 'images' : img, 'offset': offset}

    def getImages(self):

        """ Pull Images """
        
        return requests.get(self.base, params = self.param)
            
            

    def cleanImages(self, output):

        """ Clean up pulls"""

        rec = output.json()['records']

        res = []

        for i in rec:

            j = i['fields']

            res.append({
                "primary_image_id" : j['primary_image_id'],
                "year_start" : j['year_start'],
                "title" : j['title'],
                "place" : j['place'],
                'artist' : j['artist']
            })
            
        res = pd.DataFrame(res)
        return res

if __name__ == "__main__":
    
    res = pd.DataFrame()
    
    for bf in [2050, 1900, 1500]:
        for af in [1950, 1750, -3000]:
            for off in [45, 90, 135]:
                
                print('before: {0}, after {1}, off {2}'.format(bf, af, off))
                q = vaAPI(bf, af, off)
                y = q.getImages()
                y = q.cleanImages(y)
                y = y[y['year_start'] > af]
                
                res = res.append(y)
                
                res = res.drop_duplicates('primary_image_id')
    
    res.to_csv('art_list.csv', index = False)
    
    