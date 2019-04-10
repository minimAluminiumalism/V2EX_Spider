import requests
import v2ex_login
import csv
import json
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
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
		title = soup.find("h1")
		if title:
			title = title.text
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
		else:
			pass
		
def main():
	with open("V2EX_info.csv", "w", encoding="UTF-8") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Title", "Description", "Reply_content"])
	for i in range(1, 51):
		index_url = "https://www.v2ex.com/recent?p={}".format(i)
		get_onepage_info(index_url)

if __name__ == "__main__":
	main()
