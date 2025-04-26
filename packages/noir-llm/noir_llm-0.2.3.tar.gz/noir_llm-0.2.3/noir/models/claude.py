"""
Claude model implementation for Noir package.

This module provides a client for accessing Claude 3.7 models through a proxy API.
"""

import json
import time
import uuid
import requests
import random
from typing import Dict, List, Any, Tuple, Optional
from colorama import Fore, Style

from noir.models.base import BaseModel


class ClaudeClient:
    """Client for accessing Claude 3.7 models through a proxy API."""

    def __init__(self, debug: bool = False):
        """Initialize a Claude client.

        Args:
            debug: Whether to print debug information
        """
        self.base_url = "https://netwrck.com"
        self.api_url = f"{self.base_url}/api/chatpred_or"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://netwrck.com",
            "priority": "u=1, i",
            "referer": "https://netwrck.com/",
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
        self.retry_delay = 2
        self.conversation_history = []
        self.last_refresh_time = 0
        self.refresh_interval = 300  # Refresh cookies every 5 minutes
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]

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

            # Rotate user agent
            random_user_agent = random.choice(self.user_agents)
            self.headers["user-agent"] = random_user_agent

            # Visit the main page to get cookies
            response = self.session.get(
                self.base_url,
                headers={
                    "User-Agent": self.headers["user-agent"],
                    "Accept": "text/html,application/xhtml+xml,application/xml"
                }
            )

            if response.status_code == 200:
                # Set some default cookies if they don't exist
                if 'firstvisit' not in self.session.cookies:
                    self.session.cookies.set('firstvisit', 'true', domain='netwrck.com', path='/')

                # Generate random stripe IDs if they don't exist
                if '__stripe_mid' not in self.session.cookies:
                    stripe_mid = f"{uuid.uuid4()}-{uuid.uuid4().hex[:8]}"
                    self.session.cookies.set('__stripe_mid', stripe_mid, domain='netwrck.com', path='/')

                if '__stripe_sid' not in self.session.cookies:
                    stripe_sid = f"{uuid.uuid4()}-{uuid.uuid4().hex[:8]}"
                    self.session.cookies.set('__stripe_sid', stripe_sid, domain='netwrck.com', path='/')

                if 'subscribeMessageCounter' not in self.session.cookies:
                    self.session.cookies.set('subscribeMessageCounter', '1', domain='netwrck.com', path='/')

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

    def send_message(self, message: str, system_message: str = "") -> str:
        """Send a message to the Claude 3.7 model.

        Args:
            message: The message to send
            system_message: The system message to use

        Returns:
            The response from the model
        """
        # Refresh cookies before sending the message
        self.refresh_cookies()

        # Prepare the payload
        payload = {
            "query": message,
            "model_name": "anthropic/claude-3-7-sonnet-20250219",
            "context": system_message if system_message else "",
            "examples": ["hii", "Welcome! Which origin calls to you? Or do you have a different idea? Let's craft your story!)*"],
            "greeting": "An unknown multiverse phenomenon occurred, and you found yourself in a dark space. You looked around and found a source of light in a distance. You approached the light and *whoosh*....\nChoose your origin:\na) As a baby who just got birthed, your fate unknown\nb) As an amnesic stranded on an uninhabited island with mysterious ruins\nc) As an abandoned product of a forbidden experiment\nd) As a slave being sold at an auction\ne) Extremely Chaotic Randomizer\nOr, dive into your own fantasy."
        }

        # Try to send the message with retries
        for attempt in range(self.max_retries):
            try:
                if self.debug:
                    print(f"{Fore.YELLOW}Sending message to Claude 3.7 (attempt {attempt + 1}/{self.max_retries})...{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Payload: {json.dumps(payload, indent=2)}{Style.RESET_ALL}")

                # Send the request
                response = self.session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )

                if self.debug:
                    print(f"{Fore.YELLOW}Response status: {response.status_code}{Style.RESET_ALL}")

                # Check if the request was successful
                if response.status_code == 200:
                    try:
                        response_data = response.text
                        if self.debug:
                            print(f"{Fore.GREEN}Successfully received response{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}Response: {response_data[:200]}...{Style.RESET_ALL}")

                        # Store the message and response in conversation history
                        self.conversation_history.append({
                            "role": "user",
                            "content": message
                        })
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": response_data
                        })

                        # Clean up the response by removing any debug information or role-play prompts
                        # that might be included in the API response
                        if response_data.startswith('"') and response_data.endswith('"'):
                            response_data = response_data[1:-1]

                        # Handle escaped quotes and newlines
                        response_data = response_data.replace('\\n', '\n').replace('\\"', '"')

                        # Remove any references to the origin story prompt that might be in the response
                        if any(x in response_data.lower() for x in ["origin story", "choose your origin", "creative writing prompt", "multiverse phenomenon"]):
                            lines = response_data.split('\n')
                            clean_lines = []
                            skip_mode = False

                            for line in lines:
                                if any(x in line.lower() for x in ["origin story", "choose your origin", "creative writing prompt", "multiverse phenomenon", "creative fiction prompt"]):
                                    skip_mode = True
                                    continue

                                if skip_mode and line.strip() == "":
                                    skip_mode = False
                                    continue

                                if not skip_mode:
                                    clean_lines.append(line)

                            response_data = '\n'.join(clean_lines).strip()

                        # If the response is empty after cleaning, provide a default response
                        if not response_data.strip():
                            response_data = "I'm Claude, an AI assistant created by Anthropic. I'm designed to be helpful, harmless, and honest in my interactions. How can I assist you today?"

                        return response_data
                    except Exception as e:
                        if self.debug:
                            print(f"{Fore.RED}Error parsing response: {str(e)}{Style.RESET_ALL}")

                        # If we've exhausted retries, return a friendly message
                        if attempt == self.max_retries - 1:
                            return "I encountered an error processing your request. Please try again."
                else:
                    if self.debug:
                        print(f"{Fore.RED}Request failed with status code {response.status_code}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")

                    # If we get a 429 (Too Many Requests) or 403 (Forbidden), refresh cookies and retry
                    if response.status_code in [429, 403]:
                        if self.debug:
                            print(f"{Fore.YELLOW}Rate limit detected. Refreshing cookies and retrying...{Style.RESET_ALL}")

                        # Clear session and get new cookies
                        self.session = requests.Session()
                        self.refresh_cookies()

                        # Rotate user agent
                        random_user_agent = random.choice(self.user_agents)
                        self.headers["user-agent"] = random_user_agent

                        # Wait with exponential backoff
                        if attempt < self.max_retries - 1:
                            backoff_time = self.retry_delay * (2 ** attempt) * random.uniform(0.8, 1.2)
                            if self.debug:
                                print(f"{Fore.YELLOW}Waiting {backoff_time:.2f} seconds before retry...{Style.RESET_ALL}")
                            time.sleep(backoff_time)
                            continue

                    # If we've exhausted retries, return a friendly message
                    if attempt == self.max_retries - 1:
                        return "I'm currently experiencing high demand. Please try again in a moment."

            except Exception as e:
                if self.debug:
                    print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")

                # If we've exhausted retries, return a friendly message
                if attempt == self.max_retries - 1:
                    return "I encountered an error processing your request. Please try again."

                # Wait with exponential backoff before retrying
                backoff_time = self.retry_delay * (2 ** attempt) * random.uniform(0.8, 1.2)
                if self.debug:
                    print(f"{Fore.YELLOW}Waiting {backoff_time:.2f} seconds before retry...{Style.RESET_ALL}")
                time.sleep(backoff_time)

        return "Failed to get a response after multiple attempts. Please try again later."

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []


class Claude37Model(BaseModel):
    """Wrapper class for the Claude client for Claude 3.7 Sonnet model."""

    def __init__(self, debug: bool = False):
        """Initialize the Claude 3.7 Sonnet client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("Claude 3.7 Sonnet", "claude-3-7-sonnet", False, debug)
        self.client = ClaudeClient(debug=debug)
        self.system_prompt = "You are Claude, an AI assistant by Anthropic that is helpful, harmless, and honest."

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

        return self.client.send_message(message, system_message=self.system_prompt)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.client.clear_history()

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the model.

        Args:
            prompt: The system prompt to set
        """
        self.system_prompt = prompt

    def get_system_prompt(self) -> str:
        """Get the current system prompt.

        Returns:
            The current system prompt
        """
        return self.system_prompt
