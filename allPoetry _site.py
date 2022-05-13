# Scrape the allpoetry site

# Modules
import requests
import json
from bs4 import BeautifulSoup


initial_url = 'https://allpoetry.com/login'
final_url = 'https://allpoetry.com/'

payload = {
	# Credentials
}


# Save to a json file
def save_to_file(final_result,filename):
	with open(filename, "w+") as f:
		json.dump(final_result, f, indent = 2)


# Login function and an authorised request for testing
def login():
	s = requests.Session()
	authenticate_= s.post(initial_url, json=payload)
	return s


# Scrape a particular topic
def scrape_topic(s):
	body_list = []
	title_list = []
	di = {}
	# An authorised request after login
	r = s.get('https://allpoetry.com/poems/about/Racism')
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	poem_bodies = soup.findAll("div",class_="preview poem_body" or"preview poem_body center")
	poem_titles = soup.findAll("a", {"class": "nocolor"})
	for poem_title in poem_titles:
		final = poem_title.text
		title_list.append(final)
	for poem_body in poem_bodies:	
		x =poem_body.text
		body_list.append(x)
	for key in title_list:
		for value in body_list:
			di[key] = value
			body_list.remove(value)
			break  
	return di
	
	
# Scrape the trending poems	
def find_trending():
	s = login()
	li1 = []
	li2 = []
	li3 = []

	# An authorised request.
	r = s.get('https://allpoetry.com/')
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	time = soup.findAll("span", class_="date_sh")
	details = soup.findAll("div",class_="details")
	comments = soup.findAll("div",class_="extr")

	# for title
	for detail in details:
		final = detail.text
		li1.append(final)

	# for time 
	for t in time:
		finl = t.text
		li2.append(finl)

	# for no. of comments
	for c in comments:
		d = c.text
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

	# for links	
	url_list = []	
	for detail in details:
		links = detail.find_all("a")
		for link in links:
			link_url = link["href"]
			url_list.append(f"https://allpoetry.com{link_url}\n")

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
	for i in range(0, len(z)):
		di['title'] = x[i]
		di['comments'] = z[i]
		di['url'] = url_list[i]
		li.append(di)
		di ={}
	return li	
	
 
# Testing of the function
x, y, a, b = find_trending()
z = form_list_of_dict(x,y, a,b)
save_to_file(z, 'new.json')
