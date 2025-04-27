#  __init__.py for the dispatchy package

import sys
import requests
import json  # Import the json module

print("Hi from Dispatchy :D")

class DiscordWebhook:
    """
    A class to simplify sending Discord webhook messages.
    Designed for ease of use and robust error handling.
    """
    def __init__(self, url=None):
        """
        Initializes a DiscordWebhook instance.

        Args:
            url (str, optional): The Discord webhook URL.  If not provided here,
                it must be set using set_url() before sending.
        """
        if url:  # Allow initializing with or without a URL
            self.set_url(url) # use the setter
        else:
            self.url = None
        self.content = None
        self.username = None
        self.avatar_url = None
        self.tts = False  # Add tts as an attribute
        self.embeds = []
        self.thread_name = None # Add thread_name
        self.applied_tags = [] # add applied tags
        self.files = [] # add files

    def set_url(self, url):
        """
        Sets the Discord webhook URL.

        Args:
            url (str): The Discord webhook URL.

        Raises:
            TypeError: If url is not a string.
            ValueError: If url is empty or not a valid URL (basic check).
        """
        if not isinstance(url, str):
            raise TypeError("Webhook URL must be a string.")
        if not url:
            raise ValueError("Webhook URL cannot be empty.")
        #  Basic URL validation (you might want a more robust check)
        if not url.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("Invalid Discord webhook URL. Must start with 'https://discord.com/api/webhooks/'.")
        self.url = url
        return self

    def set_content(self, content=None): # Allow None
        """
        Sets the content of the webhook message.

        Args:
            content (str, optional): The main text content.  Can be None.
        """
        if content is not None and not isinstance(content, str):
            raise TypeError("Content must be a string or None.")
        self.content = content
        return self

    def set_username(self, username=None): # Allow None
        """
        Sets the username for the webhook message.

        Args:
            username (str, optional): The displayed username. Can be None.
        """
        if username is not None and not isinstance(username, str):
            raise TypeError("Username must be a string or None.")
        self.username = username
        return self

    def set_avatar_url(self, avatar_url=None): # Allow None
        """
        Sets the avatar URL for the webhook message.

        Args:
            avatar_url (str, optional): The URL of the displayed avatar. Can be None
        """
        if avatar_url is not None and not isinstance(avatar_url, str):
            raise TypeError("Avatar URL must be a string or None.")
        self.avatar_url = avatar_url
        return self

    def set_tts(self, tts):
        """
        Sets whether the message should be read aloud (text-to-speech).

        Args:
            tts (bool): True if the message should be read aloud, False otherwise.
        """
        if not isinstance(tts, bool):
            raise TypeError("TTS must be a boolean value.")
        self.tts = tts
        return self

    def add_embed(self, embed):
        """
        Adds an embed to the webhook message.

        Args:
            embed (dict): A dictionary representing the embed.

        Raises:
            TypeError: If embed is not a dictionary.
            ValueError: If the embed is empty.
        """
        if not isinstance(embed, dict):
            raise TypeError("Embed must be a dictionary.")
        if not embed:
            raise ValueError("Embed cannot be an empty dictionary.")
        self.embeds.append(embed)
        return self

    def clear_embeds(self):
        """
        Clears all embeds from the message.
        """
        self.embeds = []
        return self

    def set_thread_name(self, thread_name):
        """
        Sets the name of the thread to create (if sending to a thread-enabled channel).

        Args:
            thread_name (str): The name of the thread.
        """
        if not isinstance(thread_name, str):
            raise TypeError("Thread name must be a string.")
        self.thread_name = thread_name
        return self

    def set_applied_tags(self, applied_tags):
        """
        Sets the applied tags for the message.

        Args:
            applied_tags (list[int]): A list of applied tag IDs.
        """
        if not isinstance(applied_tags, list):
            raise TypeError("Applied tags must be a list.")
        for tag in applied_tags:
            if not isinstance(tag, int):
                raise TypeError("Each tag ID in applied_tags must be an integer.")
        self.applied_tags = applied_tags
        return self

    def add_file(self, file_path, filename=None):
        """
        Adds a file to the webhook message.

        Args:
            file_path (str): Path to the file.
            filename (str, optional): Filename to use in Discord.  If None, uses the
                filename from file_path.
        Raises:
            TypeError: If file_path is not a string.
            ValueError: If file_path is empty or the file does not exist.
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string.")
        if not file_path:
            raise ValueError("file_path cannot be empty.")
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        if filename is None:
            filename = os.path.basename(file_path)
        self.files.append({'path': file_path, 'filename': filename})
        return self

    def clear_files(self):
        """
        Clears all files from the message.
        """
        self.files = []
        return self
    def send(self):
        """
        Sends the webhook message to Discord.

        Returns:
            requests.Response: The response object from the Discord API.  Contains
                status code and content.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the send.
            ValueError: If the URL has not been set.
            TypeError: If the payload construction fails.
        """
        if not self.url:
            raise ValueError("Webhook URL must be set before sending.")

        payload = {}
        files = [] # list of files
        if self.content:
            payload['content'] = self.content
        if self.username:
            payload['username'] = self.username
        if self.avatar_url:
            payload['avatar_url'] = self.avatar_url
        if self.tts:
            payload['tts'] = self.tts  # Include tts in the payload
        if self.embeds:
            payload['embeds'] = self.embeds
        if self.thread_name:
            payload['thread_name'] = self.thread_name
        if self.applied_tags:
            payload['applied_tags'] = self.applied_tags
        if self.files:
            for file_data in self.files:
                files.append(('files', (file_data['filename'], open(file_data['path'], 'rb'))))

        try:
            #  Discord expects a JSON payload.  Handle the encoding explicitly.
            json_payload = json.dumps(payload)
        except TypeError as e:
            raise TypeError(f"Error constructing JSON payload: {e}")

        try:
            if files:
                response = requests.post(self.url, data=payload, files=files)
            else:
                response = requests.post(self.url, data=json_payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status()  # Raise for bad status codes (4xx or 5xx)
            return response  # Return the response object
        except requests.exceptions.RequestException as e:
            #  Include the response text in the error message for easier debugging
            error_message = f"Error sending webhook: {e}.  Response text: {response.text if hasattr(response, 'text') else 'No response text available.'}"
            raise requests.exceptions.RequestException(error_message)
class TelegramWebhook:
    """
    A class to simplify sending Telegram webhook messages.
    """
    def __init__(self, token=None):
        """
        Initializes a TelegramWebhook instance.

        Args:
            token (str, optional): The Telegram bot token. If not provided here,
                it must be set using set_token() before sending.
        """
        if token:
            self.set_token(token)
        else:
            self.token = None
        self.chat_id = None  # Chat ID is required for sending messages
        self.text = None
        self.parse_mode = None  # Optional:  HTML, Markdown, MarkdownV2

    def set_token(self, token):
        """
        Sets the Telegram bot token.

        Args:
            token (str): The Telegram bot token.

        Raises:
            TypeError: If token is not a string.
            ValueError: If token is empty.
        """
        if not isinstance(token, str):
            raise TypeError("Telegram bot token must be a string.")
        if not token:
            raise ValueError("Telegram bot token cannot be empty.")
        self.token = token
        return self

    def set_chat_id(self, chat_id):
        """
        Sets the Telegram chat ID.

        Args:
            chat_id (str or int): The Telegram chat ID.

        Raises:
            TypeError: If chat_id is not a string or an integer.
            ValueError: If chat_id is empty.
        """
        if not isinstance(chat_id, (str, int)):
            raise TypeError("Telegram chat ID must be a string or an integer.")
        if not str(chat_id):  # Check if it's empty after converting to string
            raise ValueError("Telegram chat ID cannot be empty.")
        self.chat_id = str(chat_id)  # Store it as a string for consistency
        return self

    def set_text(self, text=None):
        """
        Sets the text content of the message.

        Args:
            text (str, optional): The text content. Can be None.
        """
        if text is not None and not isinstance(text, str):
            raise TypeError("Message text must be a string or None.")
        self.text = text
        return self

    def set_parse_mode(self, parse_mode=None):
        """
        Sets the parse mode for the message (e.g., 'HTML', 'Markdown').

        Args:
            parse_mode (str, optional): The parse mode. Can be None.
        """
        if parse_mode is not None and not isinstance(parse_mode, str):
            raise TypeError("Parse mode must be a string or None.")
        if parse_mode and parse_mode not in ('HTML', 'Markdown', 'MarkdownV2'):
            raise ValueError("Invalid parse mode.  Must be 'HTML', 'Markdown', or 'MarkdownV2'.")
        self.parse_mode = parse_mode
        return self

    def send(self):
        """
        Sends the message to Telegram.

        Returns:
            requests.Response: The response object from the Telegram API.

        Raises:
            requests.exceptions.RequestException: If an error occurs during sending.
            ValueError: If the token or chat ID is not set.
            TypeError:  If there are issues constructing the request.
        """
        if not self.token:
            raise ValueError("Telegram bot token must be set before sending.")
        if not self.chat_id:
            raise ValueError("Telegram chat ID must be set before sending.")

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
        }
        if self.text:
            payload['text'] = self.text
        if self.parse_mode:
            payload['parse_mode'] = self.parse_mode

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            error_message = f"Error sending Telegram message: {e}. Response text: {response.text if hasattr(response, 'text') else 'No response text available'}"
            raise requests.exceptions.RequestException(error_message)

