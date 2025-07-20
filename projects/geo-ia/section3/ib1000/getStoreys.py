import csv
import requests
from bs4 import BeautifulSoup
import json
import time

init = requests.get("https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true&lang=en")
soup = BeautifulSoup(init.text, "lxml")
view_state = soup.find_all("input", {"name":"javax.faces.ViewState"})[0].get('value')
jsessionid = init.headers.get('Set-Cookie', '').split(';')[0].split('=')[-1]

def getEntriesByName(name):
    return requests.post('https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://bmis1.buildingmgt.gov.hk',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }, cookies={
            'JSESSIONID': jsessionid#'0l9XUkg7J0aGWzJJ6uw3jmWkXBiRL6jyyuXPBvaa.node2',
        }, data={
            'language':'en',
            '_bld_search_frm:district_focus': '',
            '_bld_search_frm:district_input': '',
            '_bld_search_frm:building_name': name,
            '_bld_search_frm:estate_name': '',
            '_bld_search_frm:street_name': '',
            '_bld_search_frm:village_name': '',
            '_bld_search_frm:street_no': '',
            '_bld_search_frm:storey': '',
            '_bld_search_frm:unit': '',
            '_bld_search_frm:year_from': '',
            '_bld_search_frm:year_to': '',
            '_bld_search_frm:search_btn': '',
            '_bld_search_frm:panelSearchBld_collapsed': 'false',
            '_bld_search_frm_SUBMIT': '1',
            'autoScroll': '',
            'javax.faces.ViewState': view_state#'vKJyS49RNmpPvunBmzBjuBehAjcOdmJQGd6gcszrhF8S44F0'
        }).text

def getEntriesByStreet(sno, sname):
    return requests.post('https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://bmis1.buildingmgt.gov.hk',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }, cookies={
            'JSESSIONID': jsessionid#'0l9XUkg7J0aGWzJJ6uw3jmWkXBiRL6jyyuXPBvaa.node2',
        }, data={
            'language':'en',
            '_bld_search_frm:district_focus': '',
            '_bld_search_frm:district_input': '',
            '_bld_search_frm:building_name': '',
            '_bld_search_frm:estate_name': '',
            '_bld_search_frm:street_name': sname,
            '_bld_search_frm:village_name': '',
            '_bld_search_frm:street_no': sno,
            '_bld_search_frm:storey': '',
            '_bld_search_frm:unit': '',
            '_bld_search_frm:year_from': '',
            '_bld_search_frm:year_to': '',
            '_bld_search_frm:search_btn': '',
            '_bld_search_frm:panelSearchBld_collapsed': 'false',
            '_bld_search_frm_SUBMIT': '1',
            'autoScroll': '',
            'javax.faces.ViewState': view_state#'vKJyS49RNmpPvunBmzBjuBehAjcOdmJQGd6gcszrhF8S44F0'
        }).text

def getDetail(identifier, vs):
    return requests.post('https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://bmis1.buildingmgt.gov.hk',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }, cookies={
        'JSESSIONID': jsessionid,
    }, data={
        '_bld_result_frm:_result_tbl_columnOrder': '_bld_result_frm:_result_tbl:j_id_57,_bld_result_frm:_result_tbl:j_id_5d,_bld_result_frm:_result_tbl:j_id_5j',
        '_bld_result_frm_SUBMIT': '1',
        'autoScroll': '',
        'javax.faces.ViewState': vs,
        identifier: identifier
    }).text

def parseDetail(detail):
    d = {}

    detail_soup = BeautifulSoup(detail, "lxml")
    d['district'] = detail_soup.find(id='_detail_form:j_id_3g').parent.next_sibling.next_sibling.find('div').string.strip()
    d['bldgName'] = detail_soup.find(id='_detail_form:j_id_3m').parent.next_sibling.next_sibling.find('div').string.strip()
    d['estateName'] = detail_soup.find(id='_detail_form:j_id_3s').parent.next_sibling.next_sibling.find('div').string.strip()
    d['storeys'] = detail_soup.find(id='_detail_form:j_id_3y').parent.next_sibling.next_sibling.find('div').string.strip()
    d['basements'] = detail_soup.find(id='_detail_form:j_id_42').parent.next_sibling.next_sibling.find('div').string.strip()
    d['units'] = detail_soup.find(id='_detail_form:j_id_46').parent.next_sibling.next_sibling.find('div').string.strip()
    d['years'] = detail_soup.find(id='_detail_form:j_id_4a').parent.next_sibling.next_sibling.find('div').string.strip()
    d['address'] = detail_soup.find(id='_detail_form:j_id_4f_data').string
    d['address'] = d['address'].strip() if d['address'] else ''

    return d

with open('BuildingAndBuildingName.csv', 'r') as namefile:
    names = tuple(csv.reader(namefile))

with open('BuildingAndBuildingAddress.csv', 'r') as addressfile:
    addresses = tuple(csv.reader(addressfile))

full = {}
with open('in.csv', 'r') as infile:
    rows = list(csv.reader(infile))
    for trialCount in range(5):
        for r in rows[:]:
            bid = r[0]
            ds = []

            try:
                for a in addresses:
                    if a[0] == bid:
                        print(f'[{bid}_{trialCount}] ADDRESS: {a[1]}{a[2]}{a[3]} {a[4]}') # buildingname found
                        entries_soup = BeautifulSoup(getEntriesByStreet(f'{a[1]}{a[2]}{a[3]}', a[4]), "lxml")
                        break
                else:
                    for n in names:
                        if n[0] == bid:
                            if not n[1]:
                                continue

                            print(f'[{bid}_{trialCount}] NAME: {n[1]}') # buildingname found
                            entries_soup = BeautifulSoup(getEntriesByName(n[1]), "lxml")
                            break
                    
                # print(entries_soup)
                ds = []
                try:
                    entries_view_state = entries_soup.find_all("input", {"name":"javax.faces.ViewState"})[0].get('value')
                except:
                    init = requests.get("https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true&lang=en")
                    soup = BeautifulSoup(init.text, "lxml")
                    view_state = soup.find_all("input", {"name":"javax.faces.ViewState"})[0].get('value')
                    jsessionid = init.headers.get('Set-Cookie', '').split(';')[0].split('=')[-1]

                    print('Error detected, sleeping 10 seconds.')
                    time.sleep(10)
                else:
                    matches = entries_soup.find(id="_bld_result_frm:_result_tbl_data").find_all('a')
                    # print(len(matches))
                    for i, t in enumerate(matches):
                        if i % 2: # discard building name, only query building's address
                            d = parseDetail(getDetail(t['id'], entries_view_state))
                            d['score'] = (i+1) / 2
                            print(d)
                            ds.append(d)
            except Exception as e:
                print(e)

            full[f'{bid}_{trialCount}'] = ds
            print('===================')

with open('out.json', 'w+') as outfile:
    json.dump(full, outfile, indent=4)