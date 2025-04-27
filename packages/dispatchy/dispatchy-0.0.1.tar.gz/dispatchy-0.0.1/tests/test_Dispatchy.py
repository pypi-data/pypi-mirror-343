from Dispatchy import DiscordWebhook
import requests

webhook_url = "https://discord.com/api/webhooks/1365891541788262410/k5gQEnf8wNrWCL0jCXnnNiM5KvqwYzsaAjlGfbQaG5xw7hizWjY6n0UmeqJt9j6rf_C-"
catbox_video_url = "https://files.catbox.moe/l3l6sd.mp3"  #  The Catbox URL

try:
    # 1. Send the message with the Catbox URL
    webhook = DiscordWebhook(webhook_url)
    webhook.set_content(f"Hi from Hooky\nVideo URL: {catbox_video_url}")  # Combine the messages
    response = webhook.send()
    response.raise_for_status()
    print(f"Message sent successfully! Status code: {response.status_code}")



except requests.exceptions.RequestException as e:
    print(f"Error sending message to Discord: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
