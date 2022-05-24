# Scrape the allpoetry site


# Modules
import requests
import json
from bs4 import BeautifulSoup
import re


final_url = 'https://allpoetry.com/'


# Save to a json file
def save_to_file(final_result,filename):
	with open(filename, "w+") as f:
		json.dump(final_result, f, indent = 2)
	
	
# Scrape the trending poems	
def find_trending():
	li1 = []
	li2 = []
	li3 = []
	# An authorised request.
	r = requests.get('https://allpoetry.com/')
	html = r.text
	soup = BeautifulSoup(html, "html.parser")

	i = re.compile('itm tip u_.*')
	all_data = soup.find_all('div', class_ = i)
	url_list = []

	for data in all_data:
		title = data.find('div', class_="details")
		li1.append(title.string)
		link = title.find("a")
		link_url = link["href"]
		url_list.append(f"https://allpoetry.com{link_url}\n")
		date = data.find('span', class_="date_sh")
		if not date:
			date = "Date not available!"		
			li2.append(date)
		else:
			li2.append(date.string)
		comment = data.find('div',class_="extr")
		d = comment.text
		li3.append(d)
			
	li4 = []
	for ele in li3:
		if 'dy' in ele:
			x = ele.split("dy")
			z = edit(x)
			li4.append(z)
		elif "h" in ele:
			x = ele.split("h" or "dy")
			z = edit(x)		
		else:
			li4.append(ele)
	return li1, li2, li4, url_list


# Edits the scraped comments and time to get the no. of comments
def edit(x):
	if len(x[1])>3:
		y = str(x).split(" ")
		z = y[1]
	else:
		z = x[1]
	return z


# form of dict of all the scraped list data
def form_list_of_dict(x,y, z, url_list):
	di = {}
	li = []
	for i in range(0, len(y)):
		di['title'] = x[i]
		di['date'] = y[i]
		di['comments'] = z[i]
		di['url'] = url_list[i]
		li.append(di)
		di ={}
	return li	
	
 
# Testing of the function
x, y, a, b = find_trending()
z = form_list_of_dict(x,y, a,b)
save_to_file(z, 'new.json')
