"""
GPT model implementation for Noir package.

This module provides a client for accessing GPT-3.5 models through a proxy API.
"""

import json
import time
import uuid
import requests
from typing import Dict, List, Any, Tuple, Optional
from colorama import Fore, Style

from noir.models.base import BaseModel


class GPTClient:
    """Client for accessing GPT-3.5 models through a proxy API."""

    def __init__(self, debug: bool = False):
        """Initialize a GPT client.

        Args:
            debug: Whether to print debug information
        """
        self.api_url = "https://chatgpt-clone-ten-nu.vercel.app/api/chat"
        self.base_url = "https://chatgpt-clone-ten-nu.vercel.app"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://chatgpt-clone-ten-nu.vercel.app",
            "referer": "https://chatgpt-clone-ten-nu.vercel.app/",
            "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.debug = debug
        self.max_retries = 3
        self.conversation_history = []
        self.last_refresh_time = 0
        self.refresh_interval = 300  # Refresh cookies every 5 minutes

    def _generate_random_id(self) -> str:
        """Generate a random ID.

        Returns:
            A random string ID
        """
        return str(uuid.uuid4())

    def refresh_cookies(self) -> bool:
        """Refresh the cookies by visiting the main page.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Only refresh if it's been more than refresh_interval seconds
            current_time = time.time()
            if current_time - self.last_refresh_time < self.refresh_interval:
                if self.debug:
                    print(f"{Fore.YELLOW}Skipping cookie refresh, last refresh was {current_time - self.last_refresh_time:.1f} seconds ago{Style.RESET_ALL}")
                return True

            if self.debug:
                print(f"{Fore.YELLOW}Refreshing cookies...{Style.RESET_ALL}")

            # Visit the main page to get cookies
            response = self.session.get(
                self.base_url,
                headers={
                    "User-Agent": self.headers["user-agent"],
                    "Accept": "text/html,application/xhtml+xml,application/xml"
                }
            )

            if response.status_code == 200:
                self.last_refresh_time = current_time
                if self.debug:
                    print(f"{Fore.GREEN}Successfully refreshed cookies{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Cookies: {self.session.cookies.get_dict()}{Style.RESET_ALL}")
                return True
            else:
                if self.debug:
                    print(f"{Fore.RED}Failed to refresh cookies. Status code: {response.status_code}{Style.RESET_ALL}")
                return False

        except Exception as e:
            if self.debug:
                print(f"{Fore.RED}Error refreshing cookies: {str(e)}{Style.RESET_ALL}")
            return False

    def _parse_stream_response(self, response_text: str) -> str:
        """Parse the streaming response from the GPT API.

        Args:
            response_text: The streaming response text

        Returns:
            The parsed content
        """
        try:
            # The response is a series of chunks, each starting with a number followed by a colon
            # Example: 0:"Hello" 0:"!" 0:" How" 0:" can" 0:" I" 0:" assist" 0:" you" 0:" today" 0:"?"

            if self.debug:
                print(f"{Fore.YELLOW}Raw response:{Style.RESET_ALL}")
                print(response_text)

            # Split by chunks and extract content
            chunks = response_text.split('0:"')
            content = ""

            for chunk in chunks:
                if not chunk:
                    continue

                # Find the end of the content (marked by ")
                end_idx = chunk.find('"')
                if end_idx != -1:
                    content += chunk[:end_idx]

            # Clean up the response
            # Remove any debug information or artifacts that might be in the response
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]

            # Remove any references to debugging or system information
            lines = content.split('\n')
            clean_lines = []
            for line in lines:
                # Skip lines that contain debug information
                if any(x in line.lower() for x in ["debug:", "system:", "debug mode", "debug information"]):
                    continue
                clean_lines.append(line)

            content = '\n'.join(clean_lines).strip()

            return content

        except Exception as e:
            if self.debug:
                print(f"{Fore.RED}Error parsing stream response: {str(e)}{Style.RESET_ALL}")
            return "Error parsing response"

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def send_message(self, message: str, model: str = "gpt-3.5-turbo", system_message: str = "") -> str:
        """Send a message to the GPT API.

        Args:
            message: The message to send
            model: The model to use (default: gpt-3.5-turbo)
            system_message: Optional system message to set the assistant's behavior

        Returns:
            The response from the API
        """
        # Ensure we have fresh cookies
        if not self.refresh_cookies():
            return "Failed to authenticate with GPT API. Please try again."

        # Prepare the messages
        messages = []

        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})

        # Add conversation history
        messages.extend(self.conversation_history)

        # Add the current message
        messages.append({"role": "user", "content": message})

        # Prepare the payload
        payload = {
            "messages": messages,
            "model": model
        }

        if self.debug:
            print(f"\n{Fore.CYAN}Sending message to GPT API:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Message: {message}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Using payload:{Style.RESET_ALL}")
            print(json.dumps(payload, indent=2))

        # Send the request
        for attempt in range(self.max_retries):
            try:
                if self.debug:
                    print(f"{Fore.YELLOW}Attempt {attempt + 1}/{self.max_retries}{Style.RESET_ALL}")

                response = self.session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    stream=True,
                    timeout=60
                )

                if response.status_code == 200:
                    # Collect the streaming response
                    full_response = ""
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            decoded_chunk = chunk.decode('utf-8')
                            full_response += decoded_chunk

                            # Print progress if in debug mode
                            if self.debug:
                                print(f"{Fore.GREEN}Received chunk: {decoded_chunk}{Style.RESET_ALL}")

                    # Parse the full response
                    content = self._parse_stream_response(full_response)

                    # Add the assistant's response to the conversation history
                    self.conversation_history.append({"role": "assistant", "content": content})

                    return content

                elif response.status_code == 401 or response.status_code == 403:
                    # Cookies might be expired, refresh and retry
                    if self.debug:
                        print(f"{Fore.YELLOW}Authentication failed. Refreshing cookies...{Style.RESET_ALL}")
                    self.last_refresh_time = 0  # Force refresh
                    if self.refresh_cookies():
                        continue
                    else:
                        # If we can't refresh cookies, try with a different approach
                        if attempt < self.max_retries - 1:
                            continue
                        else:
                            return "I'm having trouble connecting to the service. Please try again later."

                elif response.status_code == 429:
                    # Rate limited, wait and retry
                    if self.debug:
                        print(f"{Fore.YELLOW}Rate limited. Waiting before retry...{Style.RESET_ALL}")
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                    self.last_refresh_time = 0  # Force refresh
                    self.refresh_cookies()
                    continue

                else:
                    # Other error
                    if self.debug:
                        print(f"{Fore.RED}Error: {response.status_code} - {response.text}{Style.RESET_ALL}")

                    if attempt < self.max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        return f"Error: Unable to get a response from the service. Status code: {response.status_code}"

            except Exception as e:
                if self.debug:
                    print(f"{Fore.RED}Exception: {str(e)}{Style.RESET_ALL}")

                if attempt < self.max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    return f"Error: {str(e)}"

        return "Failed to get a response after multiple attempts. Please try again later."


class GPT35Model(BaseModel):
    """Wrapper class for the GPT client for GPT-3.5-Turbo model."""

    def __init__(self, debug: bool = False):
        """Initialize the GPT-3.5-Turbo client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("GPT-3.5-Turbo", "gpt-3.5-turbo", False, debug)
        self.client = GPTClient(debug=debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."

    def send_message(self, message: str, websearch: bool = False) -> str:
        """Send a message to the model.

        Args:
            message: The message to send
            websearch: Whether to enable web search (not supported)

        Returns:
            The response from the model
        """
        if websearch:
            if self.debug:
                print(f"{Fore.YELLOW}Warning: Web search is not supported by {self.model_name}. Ignoring websearch parameter.{Style.RESET_ALL}")

        return self.client.send_message(
            message,
            model=self.model_id,
            system_message=self.system_prompt
        )

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.client.clear_history()
