import requests
from bs4 import BeautifulSoup
from file_writer import FileWriter

url = 'https://www.booking.com/searchresults.ja.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaHWIAQGYARW4AQfIAQzYAQHoAQH4AQuIAgGoAgM&lang=ja&sid=21963b21255262a85368955819125d52&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.ja.html%3Faid%3D304142%3Blabel%3Dgen173nr-1FCAEoggI46AdIM1gEaHWIAQGYARW4AQfIAQzYAQHoAQH4AQuIAgGoAgM%3Bsid%3D21963b21255262a85368955819125d52%3Btmpl%3Dsearchresults%3Bcheckin_month%3D4%3Bcheckin_monthday%3D11%3Bcheckin_year%3D2019%3Bcheckout_month%3D4%3Bcheckout_monthday%3D13%3Bcheckout_year%3D2019%3Bclass_interval%3D1%3Bdest_id%3D-246227%3Bdest_type%3Dcity%3Bfrom_sf%3D1%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=%E6%9D%B1%E4%BA%AC&is_ski_area=0&ssne=%E6%9D%B1%E4%BA%AC&ssne_untouched=%E6%9D%B1%E4%BA%AC&city=-246227&checkin_year=2019&checkin_month=4&checkin_monthday=11&checkout_year=2019&checkout_month=4&checkout_monthday=12&group_adults=1&group_children=0&no_rooms=1&sb_travel_purpose=business&from_sf=1'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/48.0'})
html = r.content
parsed_html = BeautifulSoup(html,'html.parser')
hotel = parsed_html.find_all('div', {'class': 'sr_item'})
hotels = []
print(len(hotel));
for ho in hotel:
	name = ho.find('span', {'class': 'sr-hotel__name'})
	price = ho.find('strong', {'class': 'availprice'})
	url = ho.find('a', {'class': 'hotel_name_link'})['href']
	rating = ho.find('div', {'class': 'bui-review-score__badge'})
	print(price)
	if(price):
		pr = price.text
	else:
		pr = ''
	if(rating):
		rate = rating.text
	else:
		rate = ''
	hotels.append('name:'+name.text+'| price: '+pr+'| URL: '+url+'| rating: '+rate)
writer = FileWriter(hotels, out_format='JSON', country='JAPAN')
file = writer.output_file()
print(file)
