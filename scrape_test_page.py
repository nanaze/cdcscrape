import csv
import datetime
import sys
import urllib

from bs4 import BeautifulSoup

_CDC_PAGE = 'https://www.cdc.gov/coronavirus/2019-ncov/testing-in-us.html'

def _get_cdc_content():
  response = urllib.request.urlopen(_CDC_PAGE)
  assert response.getcode() == 200
  return response.read()

def _process_table(table):
  for tr in table.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds): # skip empty rows
      parts = tds[0].get_text().split('/')
      if len(parts) > 1:
        month, day = int(parts[0]), int(parts[1])
        date = datetime.date(2020, month, day)
        yield (date.isoformat(), int(tds[1].get_text()), int(tds[2].get_text()))

def main():
  soup = BeautifulSoup(_get_cdc_content(), features="lxml")
  tables = soup.find_all('table')
  last_table = tables[-1]
  writer = csv.writer(sys.stdout)
  for record in  _process_table(last_table):
    writer.writerow(record)
    
  
  
  
  

main()
