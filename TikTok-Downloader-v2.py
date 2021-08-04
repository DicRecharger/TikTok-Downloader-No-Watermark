import requests, re

def main(url):
	user_agent = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"}
	dl_url = 'https://toolav.herokuapp.com/id/?video_id='

	mobile_pattern = re.compile(r'(https?://[^\s]+tiktok.com/[^\s@]+)') # re pattern for tiktok links from mobile, e.x. "vm.tiktok.com/"
	web_pattern = re.compile(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)') # re pattern for tiktok links from a web browser, e.x. "www.tiktok.com/@user"

	if mobile_pattern.search(url):
		r = requests.get(url, headers=user_agent) # GET request to get the ID of the tiktok

		id_url = re.search(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)', r.text).group()
		tiktok_id = id_url.split('/')[-1]

	elif web_pattern.search(url):
		tiktok_id = url.split('/')[-1]

	else:
		return print('Incorrect tiktok URL.')

	r = requests.get(dl_url + tiktok_id)
	text = r.json()

	playAddr = text['item']['video']['playAddr']
	download(playAddr[0], filename = tiktok_id)

def download(video_link, filename = 'fallback'):
	user_agent = {'User-agent': 'Mozilla/5.0'} # user agent is need in order to access the video url

	r = requests.get(video_link, headers=user_agent)
	
	with open(f'{filename}.mp4', 'wb') as f:
		f.write(r.content)

if __name__ == '__main__':
	url = input('Enter Tiktok URL: ')
	main(url)