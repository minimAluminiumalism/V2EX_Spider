import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

url = "https://www.v2ex.com"
response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, "lxml")
items = soup.find_all("span", class_="item_title")
artical_url_list = []
for item in items:
	artical_url_list.append("https://www.v2ex.com"+ item.find("a")["href"])
for artical_url in artical_url_list:
	artical_url = "https://www.v2ex.com/t/553239"
	response = requests.get(artical_url, headers=headers)
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	title = soup.find("h1").text

	pages = soup.find("div", style="background-image: url('/static/img/shadow_light.png'); background-size: 20px 20px; background-repeat: repeat-x;").find_all("a")
	pages_url_list = []
	for page in pages:
		pages_url_list.append(artical_url + page["href"])
	#print(pages_url_list)
	if pages:
		for pages_url in pages_url_list:
			response = requests.get(pages_url, headers=headers)
			soup = BeautifulSoup(response.text, "lxml")
			reply_blocks = soup.find_all("div", class_="box")[-1].find_all("div", class_="cell")
			reply_blocks.pop(0)
			reply_blocks.pop(0)
			reply_blocks.pop(-1)
			for reply_block in reply_blocks:
				user_id = reply_block.find("a").text
				reply_content = reply_block.find("div", class_="reply_content").text
				print(user_id, reply_content)
	
	else:
		reply_blocks = soup.find_all("div", class_="box")[-1].find_all("div", class_="cell")
		reply_blocks.pop(0)
		for reply_block in reply_blocks:
			user_id = reply_block.find("a").text
			reply_content = reply_block.find("div", class_="reply_content").text
			print(user_id, reply_content)
	try:
		description = soup.find('div', class_="markdown_body").text
	except:
		description = soup.find("div", class_="topic_content").text
	#print(title, "\n", description, "\n", user_id, " ", reply_content)
