#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

def parse(params):
    url = 'http://kma.go.kr/weather/observation/past_cal.jsp?stn={station}&yy={year}&mm={month}&obs=1'.format(**params)
    print 'parsing', params['year'], params['month'] 
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    tds = soup.findAll('td', {"class": "align_left"})

    pre_list = [] 
    for td in tds:
        if u'평균기온' in td.contents[0]:
            try:
                precipitation = float(td.contents[8].split(':')[1].strip('mm'))
            except ValueError:
                precipitation = 0.0
            pre_list.append(precipitation)

    return pre_list

def main():
    params = {'station': 108,  # Seoul
              'year': None, 
              'month': None,
              }
   
    with open('seoul_precip_1960-2011.txt', 'w') as fout:
        for year in xrange(1960, 2012):
            for month in xrange(1, 13):
                params['year'] = year
                params['month'] = month
                pre_list = parse(params)
                if pre_list:
                    print >>fout, '\t'.join(map(str, [year, month] + pre_list))

if __name__ == '__main__':
    main()
