import requests
import re

USER_AGENT = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"
}

def get_tiktok_video_id(url):
    mobile_pattern = re.compile(r'(https?://[^\s]+tiktok.com/[^\s@]+)')
    web_pattern = re.compile(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)')
    
    if match := mobile_pattern.search(url) or web_pattern.search(url):
        if match.group().startswith('https://www'):
            return match.group().split('/')[-1]
        else:
            try:
                response = requests.get(url, headers=USER_AGENT)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                id_url = re.search(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)', response.text).group()
                return id_url.split('/')[-1]
            except requests.RequestException as e:
                print(f"Error during requests to {url}: {e}")
    else:
        print('Incorrect TikTok URL format.')
        return None

def download_video(video_link, filename):
    try:
        response = requests.get(video_link, headers=USER_AGENT)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        with open(f'{filename}.mp4', 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading video: {e}")

def download_tiktok(url):
    tiktok_id = get_tiktok_video_id(url)
    if tiktok_id:
        # Assuming the toolav.herokuapp.com service is up and returns a direct video URL in the expected format
        dl_url = f'https://toolav.herokuapp.com/id/?video_id={tiktok_id}'
        try:
            response = requests.get(dl_url)
            response.raise_for_status()  # Check if request was successful
            video_link = response.json()['item']['video']['playAddr']
            download_video(video_link, tiktok_id)
        except requests.RequestException as e:
            print(f"Error retrieving video download link: {e}")

if __name__ == '__main__':
    url = input('Enter TikTok URL: ')
    download_tiktok(url)
