import requests
import v2ex_login
import csv
import json
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    #"cookie": 'V2EX_LANG=zhcn; PB3_SESSION="2|1:0|10:1554484708|11:PB3_SESSION|36:djJleDoxNjcuMTc5LjgxLjM0OjE1MjQ4Njky|74ecb083c77ead823f31e662b71811a459934096c5389d9cc1b200c166ec6bc1"; V2EX_REFERRER="2|1:0|10:1554798234|13:V2EX_REFERRER|12:c2h1YW5nbXU=|56839dcb63f5d6592d613de1af2f8becafdf2dda887dea8dbc06a1411b8ac726"; _ga=GA1.2.1464248796.1554802661; _gid=GA1.2.1925094505.1554802661; A2="2|1:0|10:1554813686|2:A2|56:ODI0MTg0NWU2NWZlYTAzZTQzOTk5OWM4OTlmZWRmYTEwNjQ4MGZmNQ==|d3428705be0d82e7d011d77cf06ca5d9fc4f4ef093cdbea3db246a4c5020b5c5"; V2EX_TAB="2|1:0|10:1554813688|8:V2EX_TAB|8:YXBwbGU=|2ed3e038af78cb8c21936d08887ec83d007c1f97568b4ed9bab0428124f3193f"',
}

Session = v2ex_login.login().run()

def get_onepage_info(index_url):
	response = Session.get(index_url, headers=headers)
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	items = soup.find_all("span", class_="item_title")
	artical_url_list = []
	for item in items:
		artical_url_list.append("https://www.v2ex.com"+ item.find("a")["href"])
	for artical_url in artical_url_list:
		print(artical_url)
		response = Session.get(artical_url, headers=headers)
		html = response.text
		soup = BeautifulSoup(html, "lxml")
		title = soup.find("h1").text
		
		pages = soup.find("div", style="background-image: url('/static/img/shadow_light.png'); background-size: 20px 20px; background-repeat: repeat-x;")
		reply_dict = {}
		if pages:
			pages=pages.find_all("a")
			pages_url_list = []
			for page in pages:
				pages_url_list.append(artical_url + page["href"])
			#print(pages_url_list)
			for pages_url in pages_url_list:
				print(pages_url)
				response = Session.get(pages_url, headers=headers)
				soup = BeautifulSoup(response.text, "lxml")
				reply_blocks = soup.find_all("div", class_="box")[-2].find_all("div", class_="cell")
				reply_blocks.pop(0)
				reply_blocks.pop(0)
				reply_blocks.pop(-1)
				for reply_block in reply_blocks:
					user_id = reply_block.find("a").text
					reply_content = reply_block.find("div", class_="reply_content").text
					reply_dict[user_id] = reply_content
		
		else:
			reply_blocks = soup.find_all("div", class_="box")[-2].find_all("div", class_="cell")
			if len(reply_blocks) == 0:
				user_id = "null"
				reply_content = "null"
				reply_dict[user_id] = reply_content
			else:
				reply_blocks.pop(0)
				for reply_block in reply_blocks:
					user_id = reply_block.find("strong").find("a").text
					reply_content = reply_block.find("div", class_="reply_content").text
					reply_dict[user_id] = reply_content
		try:
			description = soup.find('div', class_="markdown_body").text
		except:
			description = soup.find("div", class_="topic_content")
			if description:
				description = description
			else:
				description = "null"
		print(title, "\n", description, "\n", json.dumps(reply_dict, ensure_ascii=False))
		with open("V2EX_info.csv", "a", encoding="UTF-8") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([title, description, json.dumps(reply_dict, ensure_ascii=False)])
		
def main():
	with open("V2EX_info.csv", "w", encoding="UTF-8") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Title", "Description", "Reply_content"])
	for i in range(1, 10):
		index_url = "https://www.v2ex.com/recent?p={}".format(i)
		get_onepage_info(index_url)

if __name__ == "__main__":
	main()
