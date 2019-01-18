import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
from file_writer import FileWriter
from datetime import date, timedelta
from flask import Flask,jsonify
from flask import request as rq
import time as tm
app = Flask(__name__)
@app.route("/",methods=['GET', 'POST'])
def main():
	url = rq.args.get('url')
	checkin = rq.args.get('checkin')
	checkout = rq.args.get('checkout') 
	part_url = url.split('&checkin_year',1)[0]
	part_url = part_url+'&checkin_year=2019&checkin_month=4&checkin_monthday=12&checkout_year=2019&checkout_month=4&checkout_monthday=13'
	checkin = checkin.split('-',2)
	checkout = checkout.split('-',2)
	d1 = date(int(checkin[0]), int(checkin[1]), int(checkin[2]))  # start date
	d2 = date(int(checkout[0]), int(checkout[1]), int(checkout[2]))  # start date
	#d2 = date(2019, 1, 20)  # end date
	delta = d2 - d1
	hotels = []
	for i in range(delta.days):
		dt_from = d1 + timedelta(i)
		dt_to = d1 + timedelta(i+1)
		#[0] => Year [1] => month [2] => day
		split_from = str(dt_from).split('-',2)
		split_to = str(dt_to).split('-',2)
		dt_to_year = split_to[0]
		dt_to_month = split_to[1]
		dt_to_day = split_to[2]

		dt_from_year = split_from[0]
		dt_from_month = split_from[1]
		dt_from_day = split_from[2]
		turl = part_url+'&checkout_month='+dt_to_month+'&checkout_monthday='+dt_to_day+'&no_rooms=1&group_adults=2&group_children=0&sb_travel_purpose=business&b_h4u_keep_filters=&from_sf=1'
		#print(url)
		r = requests.get(turl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
		html = r.content
		parsed_html = BeautifulSoup(html, 'lxml')
		hotel = parsed_html.find_all('div', {'class': 'sr_item'})
		tm.sleep(5)
		print(len(hotel));
		for ho in hotel:
			#print(ho)
			name = ho.find('span', {'class': 'sr-hotel__name'})
			price = ho.find('strong', {'class': 'availprice'})
			hurl = ho.find('a', {'class': 'hotel_name_link'})['href']
			rating = ho.find('div', {'class': 'bui-review-score__badge'})
			#print(price)
			sub_r = requests.get('http://booking.com'+hurl.replace('\n',''),headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
			sub_html = sub_r.content
			tm.sleep(5)
			parsed_sub_html = BeautifulSoup(sub_html,'lxml')
			sub_hotels = parsed_sub_html.find('select',{'class':'hprt-nos-select'})
			if(sub_hotels):
				opt = sub_hotels('option')[-1]
				if(opt):
					#print(opt.text)
					occupancy = opt.text
					occupancy = occupancy.replace('\n','')
					occupancy = occupancy.split('(',1)[0]
					occupancy = occupancy.replace(' ','')
					occupancy = int(occupancy)
					occupancy = occupancy * 10
				else:
					occupancy = 0
			if(price):
				pr = price.text
			else:
				pr = ''
			if(rating):
				rate = rating.text
			else:
				rate = ''
			data = {}
			data['check_in_date'] = dt_from_year+'-'+dt_from_month+'-'+dt_from_day
			data['check_out_date'] = dt_to_year+'-'+dt_to_month+'-'+dt_to_day
			data['name'] = name.text.replace('\n','')
			data['price'] = pr.replace('\n','')
			data['URL'] = 'http://booking.com'+hurl.replace('\n','')
			rt = rate.replace('\n','')
			rt = rt.replace(' ','')
			data['rating'] = rate.replace('\n','')
			data['occupancy'] = occupancy
			hotels.append(data)
			tm.sleep(5)
	writer = FileWriter(hotels, out_format='JSON', country='JAPAN')
	file = writer.output_file()
	return jsonify(hotels)
if __name__ == "__main__":
    app.run()
