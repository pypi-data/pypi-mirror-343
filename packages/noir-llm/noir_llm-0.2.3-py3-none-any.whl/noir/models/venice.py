"""
Venice model implementations for Noir package.

This module provides model implementations for Venice AI models.
"""

import json
import uuid
import requests
import time
import re
import random
from typing import Dict, List, Any, Optional, Union, Tuple
from colorama import Fore, Style, init

from noir.models.base import BaseModel

# Initialize colorama
init(autoreset=True)

class VeniceClient:
    """Client for interacting with the Venice AI API."""

    def __init__(self, debug: bool = False):
        """Initialize the Venice AI API client.

        Args:
            debug: Whether to print debug information
        """
        self.api_url = "https://outerface.venice.ai/api/inference/chat"
        self.base_url = "https://venice.ai"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "origin": "https://venice.ai",
            "referer": "https://venice.ai/",
            "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.debug = debug
        self.max_retries = 5  # Increased retries
        self.retry_delay = 2  # Base delay in seconds
        self.conversation_history = []
        self.cookies = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]

    def _generate_random_id(self) -> str:
        """Generate a random ID.

        Returns:
            A random string ID
        """
        return str(uuid.uuid4())[:8]

    def refresh_cookies(self) -> bool:
        """Refresh the cookies by visiting the main page with rotating user agents.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Rotate user agent
            user_agent = random.choice(self.user_agents)

            # Update the user agent in headers
            self.headers["user-agent"] = user_agent

            # Visit the main page to get cookies
            response = self.session.get(
                self.base_url,
                headers={
                    "User-Agent": user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache"
                },
                timeout=30
            )

            if response.status_code == 200:
                # Store cookies for later use
                self.cookies = self.session.cookies

                # Add some common cookies if they don't exist
                if '_dcid' not in dict(self.cookies):
                    dcid_value = f"dcid.{int(time.time())}.{random.randint(100000000, 999999999)}"
                    self.session.cookies.set('_dcid', dcid_value, domain='venice.ai', path='/')

                if self.debug:
                    print(f"{Fore.GREEN}Successfully refreshed cookies{Style.RESET_ALL}")
                    if self.debug:
                        print(f"{Fore.YELLOW}Cookies: {dict(self.cookies)}{Style.RESET_ALL}")

                return True
            else:
                if self.debug:
                    print(f"{Fore.RED}Failed to get cookies. Status code: {response.status_code}{Style.RESET_ALL}")
                return False

        except Exception as e:
            if self.debug:
                print(f"{Fore.RED}Error refreshing cookies: {str(e)}{Style.RESET_ALL}")
            return False

    def _parse_response(self, response_text: str) -> str:
        """Parse the response from the Venice AI API.

        Args:
            response_text: The response text

        Returns:
            The parsed content
        """
        try:
            # The response is a series of JSON objects, one per line
            lines = response_text.strip().split('\n')

            # Only print raw response in debug mode
            if self.debug:
                print(f"{Fore.YELLOW}Raw response:{Style.RESET_ALL}")
                print(response_text)

            # Combine all content parts
            full_content = ""
            for line in lines:
                try:
                    data = json.loads(line)
                    if "content" in data and "kind" in data and data["kind"] == "content":
                        full_content += data["content"]
                except json.JSONDecodeError:
                    # Only print parse errors in debug mode
                    if self.debug:
                        print(f"{Fore.RED}Failed to parse line: {line}{Style.RESET_ALL}")
                    continue

            return full_content

        except Exception as e:
            # Only print error details in debug mode
            if self.debug:
                print(f"{Fore.RED}Error parsing response: {str(e)}{Style.RESET_ALL}")
            return "Error parsing response"

    def send_message(self, message: str, model_id: str = "mistral-31-24b", system_prompt: str = "",
                   temperature: float = None, top_p: float = None, websearch: bool = False) -> str:
        """Send a message to the Venice AI API.

        Args:
            message: The message to send
            model_id: The model ID to use
            system_prompt: Optional system message to set the assistant's behavior
            temperature: Temperature parameter for the model (model-specific default if None)
            top_p: Top-p parameter for the model (model-specific default if None)
            websearch: Whether to enable web search functionality

        Returns:
            The response from the API
        """
        # Ensure we have cookies
        if not self.cookies:
            if not self.refresh_cookies():
                return "Failed to authenticate with Venice AI. Please try again."

        # Generate a random request ID
        request_id = self._generate_random_id()

        # Prepare the conversation history
        messages = []
        for msg in self.conversation_history:
            messages.append(msg)

        # Add the current message
        messages.append({"content": message, "role": "user"})

        # Set default parameters based on model
        if temperature is None:
            if model_id == "mistral-31-24b":
                temperature = 0.15
            elif model_id == "llama-3.2-3b-akash":
                temperature = 0.8
            else:
                temperature = 0.7  # Default for unknown models

        if top_p is None:
            top_p = 0.9  # Default for all models

        # Prepare the payload
        payload = {
            "requestId": request_id,
            "conversationType": "text",
            "type": "text",
            "modelId": model_id,
            "prompt": messages,
            "includeVeniceSystemPrompt": True,
            "isCharacter": False,
            "isDefault": True,
            "characterId": "",
            "id": "",
            "systemPrompt": system_prompt,
            "temperature": temperature,
            "topP": top_p,
            "textToSpeech": {
                "voiceId": "af_sky",
                "speed": 1
            },
            "clientProcessingTime": 3,
            "userId": "user_anon_1234568910",
            "webEnabled": websearch  # Use the websearch parameter to control web access
        }

        if self.debug:
            print(f"\n{Fore.CYAN}Sending message to Venice AI API:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Message: {message}{Style.RESET_ALL}")
            # Print detailed payload in debug mode
            print(f"\n{Fore.YELLOW}Using payload:{Style.RESET_ALL}")
            print(json.dumps(payload, indent=2))

        # Send the request
        for attempt in range(self.max_retries):
            try:
                # Rotate user agent for each attempt
                if attempt > 0:
                    user_agent = random.choice(self.user_agents)
                    self.headers["user-agent"] = user_agent

                # Add some randomness to the request to avoid detection
                request_id = self._generate_random_id()
                payload["requestId"] = request_id

                # Add a small random delay before each request (except the first one)
                if attempt > 0:
                    jitter = random.uniform(0.5, 1.5)
                    time.sleep(self.retry_delay * (attempt ** 1.5) * jitter)  # Exponential backoff with jitter

                # Send the request
                response = self.session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    # Parse the response
                    content = self._parse_response(response.text)

                    # Add the assistant's response to the conversation history
                    self.conversation_history.append({"role": "assistant", "content": content})

                    return content

                elif response.status_code == 401 or response.status_code == 403:
                    # Cookies might be expired, refresh and retry
                    if self.debug:
                        print(f"{Fore.YELLOW}Authentication failed. Refreshing cookies...{Style.RESET_ALL}")
                    if self.refresh_cookies():
                        continue
                    else:
                        # If we can't refresh cookies, try with a different approach
                        if attempt < self.max_retries - 1:
                            continue
                        else:
                            return "I'm having trouble connecting to the service. Please try again later."

                elif response.status_code == 429:
                    # Rate limited - implement bypass strategy
                    if self.debug:
                        print(f"{Fore.YELLOW}Rate limited. Implementing bypass strategy...{Style.RESET_ALL}")

                    # Clear session and get new cookies
                    self.session = requests.Session()
                    self.refresh_cookies()

                    # Modify the payload slightly to appear as a new request
                    payload["clientProcessingTime"] = random.randint(1, 10)
                    payload["userId"] = f"user_anon_{random.randint(1000000000, 9999999999)}"

                    # Wait with exponential backoff
                    if attempt < self.max_retries - 1:
                        backoff_time = self.retry_delay * (2 ** attempt) * random.uniform(0.8, 1.2)
                        if self.debug:
                            print(f"{Fore.YELLOW}Waiting {backoff_time:.2f} seconds before retry...{Style.RESET_ALL}")
                        time.sleep(backoff_time)
                        continue
                    else:
                        # If we've exhausted retries, return a friendly message instead of an error
                        return "I'm currently experiencing high demand. Please try again in a moment."

                else:
                    if self.debug:
                        print(f"{Fore.RED}Error: Received status code {response.status_code}{Style.RESET_ALL}")
                        if response.text:
                            print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")

                    if attempt < self.max_retries - 1:
                        if self.debug:
                            print(f"{Fore.YELLOW}Retrying... (Attempt {attempt + 2}/{self.max_retries}){Style.RESET_ALL}")
                        continue
                    else:
                        # Return a user-friendly message instead of an error
                        return "I'm having trouble connecting to the service. Please try again later."

            except Exception as e:
                if self.debug:
                    print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
                if attempt < self.max_retries - 1:
                    if self.debug:
                        print(f"{Fore.YELLOW}Retrying... (Attempt {attempt + 2}/{self.max_retries}){Style.RESET_ALL}")
                    time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    # Return a user-friendly message instead of an error
                    return "I'm having trouble connecting to the service. Please try again later."

        return "Failed to get a response after multiple attempts."

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []


class VeniceModel(BaseModel):
    """Base class for Venice AI models."""

    def __init__(self, model_name: str, model_id: str, supports_websearch: bool = False,
                 temperature: float = None, top_p: float = None, debug: bool = False):
        """Initialize a Venice AI model client.

        Args:
            model_name: The display name of the model
            model_id: The API identifier for the model
            supports_websearch: Whether the model supports web search
            temperature: Default temperature for the model
            top_p: Default top_p for the model
            debug: Whether to print debug information
        """
        super().__init__(model_name, model_id, supports_websearch, debug)
        self.client = VeniceClient(debug=debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."
        self.temperature = temperature
        self.top_p = top_p

    def send_message(self, message: str, websearch: bool = False) -> str:
        """Send a message to the model.

        Args:
            message: The message to send
            websearch: Whether to enable web search

        Returns:
            The response from the model
        """
        if websearch and not self.supports_websearch:
            if self.debug:
                print(f"{Fore.YELLOW}Warning: Web search is not supported by {self.model_name}. Ignoring websearch parameter.{Style.RESET_ALL}")
            websearch = False

        return self.client.send_message(
            message,
            model_id=self.model_id,
            system_prompt=self.system_prompt,
            temperature=self.temperature,
            top_p=self.top_p,
            websearch=websearch  # Pass the websearch parameter to the client
        )

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.client.clear_history()


class MistralModel(VeniceModel):
    """Wrapper class for the Venice AI client for Mistral-31-24B model."""

    def __init__(self, debug: bool = False):
        """Initialize the Mistral-31-24B client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__(
            model_name="Mistral-31-24B",
            model_id="mistral-31-24b",
            supports_websearch=True,  # Venice models support web search via webEnabled parameter
            temperature=0.15,
            top_p=0.9,
            debug=debug
        )
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."


class Llama32Model(VeniceModel):
    """Wrapper class for the Venice AI client for Llama-3.2-3B model."""

    def __init__(self, debug: bool = False):
        """Initialize the Llama-3.2-3B client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__(
            model_name="Llama-3.2-3B",
            model_id="llama-3.2-3b-akash",
            supports_websearch=True,  # Venice models support web search via webEnabled parameter
            temperature=0.8,
            top_p=0.9,
            debug=debug
        )
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."
