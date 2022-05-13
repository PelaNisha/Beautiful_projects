from unittest import result
from numpy import save
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen

from sqlalchemy import null


url = 'https://penzu.com/app/login'
uu = 'https://allpoetry.com/login'
final_url = 'https://allpoetry.com/'
# url = "https://penzu.com/api/journals/26645404/entries/77210802?next=10&previous=10"
payload = {
	# credentials
}

def save_to_file(final_result,filename):
	with open(filename, "w+") as f:
		json.dump(final_result, f, indent = 2)

def login():
	s = requests.Session()
	li1 = []
	li2 = []
	di = {}
	res= s.post(uu, json=payload)
	# An authorised request.
	r = s.get('https://allpoetry.com/poems/about/Racism')
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	results = soup.findAll("div",class_="preview poem_body" or"preview poem_body center")
	# res = results.find_all("a",class_= 'nocolor')
	mydivs = soup.findAll("a", {"class": "nocolor"})
	for mydiv in mydivs:
		final = mydiv.text
		# print("***************")
		li1.append(final)


	for result in results:	
			# print("***************")
		x =result.text
		li2.append(x)

	for key in li1:
		for value in li2:
			di[key] = value
			li2.remove(value)
			break  
	return di
	
def find_trending():
	s = requests.Session()
	li1 = []
	li2 = []
	di = {}
	li3 = []
	res= s.post(uu, json=payload)
	# An authorised request.
	r = s.get('https://allpoetry.com/')
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	results = soup.findAll("div",class_="popular_box")
	
	fin = soup.findAll("div",class_="items tiny one-line")
	time = soup.findAll("span", class_="date_sh")
	a = soup.findAll("div",class_="details")
	comments = soup.findAll("div",class_="extr")
	for mydiv in a:
		final = mydiv.text
		li1.append(final)

	for t in time:
		finl = t.text
		li2.append(finl)
	for c in comments:
		d = c.text
		e = d.split()
		if len(e)>1:
			f = " ".join(e[1:])
			li3.append(f)
		
	print(li3)
	return li1, li2
def form_list_of_dict(x,y):
	di = {}
	li = []
	for i in range(0, len(y)):
		di['title'] = x[i]
		di['time'] = y[i]
		li.append(di)
		di ={}
	return li	
	
 
x, y = find_trending()
z = form_list_of_dict(x,y)
save_to_file(z, 'new.json')