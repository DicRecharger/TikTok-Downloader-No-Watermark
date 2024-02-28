import requests
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

def download_tiktok(url):
    # Define user agent to mimic a real browser request
    user_agent = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"}
    dl_url = 'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id='

    # Patterns to match TikTok URLs
    mobile_pattern = re.compile(r'(https?://[^\s]+tiktok.com/[^\s@]+)')
    web_pattern = re.compile(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)')

    if mobile_pattern.search(url):
        r = requests.get(url, headers=user_agent) # GET request to resolve the redirection or to fetch the final URL
        id_url = re.search(r'(https?://www.tiktok.com/@[^\s]+/video/[0-9]+)', r.text)
        if id_url:
            tiktok_id = id_url.group().split('/')[-1]
        else:
            print('Failed to extract TikTok ID from mobile URL.')
            return
    elif web_pattern.search(url):
        tiktok_id = url.split('/')[-1]
    else:
        print('Incorrect TikTok URL format.')
        return

    # Fetching video details using the TikTok ID
    r = requests.get(dl_url + tiktok_id, headers=user_agent)
    if r.status_code == 200:
        text = r.json()
        playAddr = text.get('item', {}).get('video', {}).get('playAddr', None)

        if playAddr:
            download(playAddr[0], filename=tiktok_id)  
            return 'Success'
        else:
            return f'Video URL not found for TikTok ID {tiktok_id}.'
    else:
        return f'Failed to fetch video details for TikTok ID {tiktok_id}.'


def download(video_link, filename='fallback'):
    user_agent = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(video_link, headers=user_agent)
    if r.status_code == 200:
        with open(f'{filename}.mp4', 'wb') as f:
            f.write(r.content)
        print(f'Video downloaded as {filename}.mp4')
    else:
        print(f'Failed to download video from {video_link}.')


def gui_download():
    url = url_entry.get().strip()  # Use strip() to remove leading/trailing whitespace
    if not url:  # Check if the URL is empty
        messagebox.showerror("Error", "Please enter a TikTok URL.")
        return

    # Now calling download_tiktok and handling the response
    response = download_tiktok(url)
    if response == 'Success':
        messagebox.showinfo("Success", "Download successful!")
    else:
        messagebox.showerror("Error", response)

def create_gui():
    window = tk.Tk()
    window.title("TikTok Downloader")

    window_width = 500
    window_height = 350

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position for window to be centered
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the window size and position
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Load and display an image
    image = PhotoImage(file='assets/Tiktok_Logo.png')  # Ensure this path is correct
    image_label = tk.Label(window, image=image)
    image_label.pack(pady=10)

    # Customize Label font
    custom_font = ("Calibri", 14, "bold")

    # URL Entry Label with custom font
    tk.Label(window, text="Enter TikTok URL:", font=custom_font).pack(pady=5)

    # Entry widget customization
    entry_font = ("Calibri", 12)  # Making the font size larger
    global url_entry
    url_entry = tk.Entry(window, font=entry_font, width=50, borderwidth=2, relief="groove")
    url_entry.pack(pady=5, ipady=4)  # ipady adds internal padding to make the entry taller

    # Download Button Customization
    button_font = ("Calibri", 12, "bold")  # Making the font bigger
    download_button = tk.Button(window, text="Download", command=gui_download,
                                font=button_font, bg="green", fg="white", 
                                relief="groove", borderwidth=0)
    download_button.pack(pady=20)

    window.mainloop()



if __name__ == '__main__':
    create_gui()
