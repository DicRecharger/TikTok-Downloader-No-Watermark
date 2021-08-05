import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def main(url):

	# chrome options for "invisible" chrome window
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--allow-running-insecure-content')
	chrome_options.add_argument("--window-size=720,480")

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
	chrome_options.add_argument(f'user-agent={user_agent}')

	# webdriver for our browser
	driver = webdriver.Chrome(options=chrome_options)
	
	driver.get("https://musicaldown.com")

	# enter url and submit
	elem = driver.find_element_by_id('link_url').send_keys(url)
	elem = driver.find_element_by_xpath('//*[@id="submit-form"]/div/div[2]/button').click()

	wait = WebDriverWait(driver, 20) # if your internet connection is very slow, change the "20" here with a larger number

	# wait until download buttons are found, then copy the link
	presence = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/a[3]')))
	link = presence.get_attribute('href')

	driver.quit()
	
	# filename is the tiktok's "id"
	filename = url.strip('https://vm.tiktok.com/')[:-1]

	if len(url) > 35:	# tiktok url's are usually 32 characters long, but some are way longer so we check for urls larger than 35 characters to be sure
		filename = url.split('?', 1)[0].split('/')[-1] 		# we do some split magic here to get the authors id of the longer url, as the tiktok's "id" isn't available here

	download(link, filename)
	
	

def download(mp4_link, filename):
	# user agent is need in order to access the .mp4 url
	user_agent = {'User-agent': 'Mozilla/5.0'}

	r = requests.get(mp4_link, headers=user_agent)
	
	with open(f'{filename}.mp4', 'wb') as f:
		f.write(r.content)

if __name__ == '__main__':
	url = input('Enter Tiktok URL: ')
	main(url)