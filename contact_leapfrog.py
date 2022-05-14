# scrape social media contacts of leapfrog 
import requests
from bs4 import BeautifulSoup
import json


url = "https://www.lftechnology.com/"


def get_contacts():
	r =  requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	results = soup.findAll("ul",class_="footer__menu")

	url_list = []	
	for result in results:
		links = result.find_all("a")
		for link in links:
			link_url = link["href"]	
			url_list.append(link_url)

	return url_list

def save_to_file(final_result,filename):
	with open(filename, "w+") as f:
		json.dump(final_result, f, indent = 2)


def organize_data(li):
	di ={}
	final_list = li[13:]
	di['company name'] = 'leapfrog'
	di['social media'] = final_list
	return di

li = get_contacts()
b = organize_data(li)
save_to_file(b, 'new.json')