import csv
import json

def convert():
    
    trade_by_country = {}
    
    with open('data.csv') as data:
        reader = csv.reader(data)
        headers = reader.next()
        for row in reader:
            direction = row[0].lower()
            year = row[1].replace('FY', '')
            country = row[2]
            commodity = row[3]
            try:
                aud_thousands = float(row[4])
            except ValueError:
                aud_thousands = 0
            
            if not country in trade_by_country.keys():
                trade_by_country[country] = {
                    'balance' : {},
                    'exports' : {},
                    'imports' : {}
                }
                
            if year not in trade_by_country[country][direction].keys():
                trade_by_country[country][direction][year] = 0
                
            if year not in trade_by_country[country]['balance'].keys():
                trade_by_country[country]['balance'][year] = 0
                
            trade_by_country[country][direction][year] += aud_thousands
            
            if direction == 'exports':
                trade_by_country[country]['balance'][year] += aud_thousands
            else:
                trade_by_country[country]['balance'][year] -= aud_thousands
              
    trade_by_country['ALL'] = None
        
    for country, values in trade_by_country.items():
        
        if country == 'ALL':
            continue
        
        if trade_by_country['ALL'] is None:
            trade_by_country['ALL'] = values
            
        else:
            for direction, years in values.items():
                for year, value in years.items():
                    trade_by_country['ALL'][direction][year] += value
        
    print trade_by_country['ALL']
            
    with open('trade-by-country.json', 'w') as tbc:
        tbc.write('var TRADE_BY_COUNTRY = {0};'.format(json.dumps(trade_by_country)))
    

if __name__ == '__main__':
    convert()