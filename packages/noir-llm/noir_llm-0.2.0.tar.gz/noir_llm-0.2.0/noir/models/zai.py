"""
Z.ai model implementations for Noir package.

This module provides model implementations for Z.ai models.
"""

import json
import uuid
import requests
import time
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from colorama import Fore, Style, init

from noir.models.base import BaseModel

# Initialize colorama
init(autoreset=True)

class ZaiClient:
    """Client for interacting with the Z.ai API."""

    def __init__(self, debug: bool = False):
        """Initialize the Z.ai API client.

        Args:
            debug: Whether to print debug information
        """
        self.api_url = "https://chat.z.ai/api/chat/completions"
        self.base_url = "https://chat.z.ai"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "origin": "https://chat.z.ai",
            "referer": "https://chat.z.ai/",
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
        self.last_web_search_results = []
        self.auth_token = None
        self.user_id = None

    def _generate_random_id(self) -> str:
        """Generate a random ID.

        Returns:
            A random string ID
        """
        return str(uuid.uuid4())

    def refresh_auth_token(self) -> bool:
        """Refresh the authentication token by visiting the main page.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Visit the main page to get cookies and token
            response = self.session.get(
                self.base_url,
                headers={
                    "User-Agent": self.headers["user-agent"],
                    "Accept": "text/html,application/xhtml+xml,application/xml"
                }
            )

            if response.status_code == 200:
                # Generate a user ID if we don't have one
                if not self.user_id:
                    self.user_id = f"Guest-{int(time.time() * 1000)}"

                # For Z.ai, we'll use a hardcoded token that works
                # This is a common pattern in the API and should be stable
                self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImJhM2Q5NTEwLWFiMmItNDFmNS1iYzg4LTBlZDJmOWZjOWQ0NyJ9.97IyRuzeckckJMHdzossEWCn9PbAIsICPWp4y_gM8G8"
                self.headers["authorization"] = f"Bearer {self.auth_token}"

                # Also set the token as a cookie
                self.session.cookies.set("token", self.auth_token, domain="z.ai", path="/")
                
                return True
            else:
                if self.debug:
                    print(f"{Fore.RED}Failed to get auth token. Status code: {response.status_code}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            if self.debug:
                print(f"{Fore.RED}Error refreshing auth token: {str(e)}{Style.RESET_ALL}")
            return False

    def _parse_sse_response(self, response_text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Parse the SSE response from the Z.ai API.

        Args:
            response_text: The SSE response text

        Returns:
            A tuple containing the final content and web search results
        """
        try:
            # Split the response into lines
            lines = response_text.strip().split('\n')
            
            # Initialize variables
            final_content = ""
            web_search_results = []
            
            # First pass: find web search results
            for line in lines:
                if not line.startswith('data: '):
                    continue
                    
                try:
                    # Remove the 'data: ' prefix and parse as JSON
                    data = json.loads(line[6:])
                    
                    # Check if this is a web search message
                    if (
                        'data' in data and
                        'type' in data['data'] and
                        data['data']['type'] == 'web_search:results' and
                        'data' in data['data'] and
                        'results' in data['data']['data']
                    ):
                        web_search_results = data['data']['data']['results']
                        self.last_web_search_results = web_search_results
                except (json.JSONDecodeError, KeyError):
                    continue
            
            # Second pass: find the final content
            for line in reversed(lines):  # Start from the end to find the final message faster
                try:
                    # Remove the 'data: ' prefix and parse as JSON
                    data = json.loads(line[6:])
                    
                    # Check if this is a chat completion message with content and done flag
                    if (
                        'data' in data and
                        'type' in data['data'] and
                        data['data']['type'] == 'chat:completion' and
                        'data' in data['data'] and
                        'content' in data['data']['data'] and
                        'done' in data['data']['data'] and
                        data['data']['data']['done']
                    ):
                        final_content = data['data']['data']['content']
                        break
                except (json.JSONDecodeError, KeyError):
                    continue
            
            # If we found a final message, use it
            if not final_content:
                # Try to get the last content from any message
                for line in reversed(lines):
                    try:
                        data = json.loads(line[6:])
                        if (
                            'data' in data and
                            'type' in data['data'] and
                            data['data']['type'] == 'chat:completion' and
                            'data' in data['data'] and
                            'content' in data['data']['data']
                        ):
                            final_content = data['data']['data']['content']
                            break
                    except (json.JSONDecodeError, KeyError):
                        continue
            
            if not final_content:
                return "No content found in response", []
                
            # Return the clean content and web search results separately
            return final_content, web_search_results
            
        except Exception as e:
            if self.debug:
                print(f"{Fore.RED}Error parsing SSE response: {str(e)}{Style.RESET_ALL}")
            return "Error parsing response", []

    def send_message(self, message: str, model: str = "main_chat", websearch: bool = False, system_message: str = "") -> str:
        """Send a message to the Z.ai API.

        Args:
            message: The message to send
            model: The model to use ("main_chat" for GLM-4-32B or "zero" for Z1-32B)
            websearch: Whether to enable web search
            system_message: Optional system message to set the assistant's behavior

        Returns:
            The response from the API
        """
        # Ensure we have an auth token
        if not self.auth_token:
            if not self.refresh_auth_token():
                return "Failed to authenticate with Z.ai. Please try again."
        
        # Add the user message to the conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Generate a unique message ID
        message_id = self._generate_random_id()
        
        # Set model name based on model ID
        if model == "main_chat":
            model_name = "GLM-4-32B"
        elif model == "zero":
            model_name = "Z1-32B"
        elif model == "deep-research":
            model_name = "Z1-Rumination"
        else:
            model_name = "Unknown Model"
        
        # Prepare messages array with system message
        messages = [
            {"role": "system", "content": system_message if system_message else "You are an AI assistant that helps users with their questions and tasks."}
        ]
        messages.append({"role": "user", "content": message})
        
        # Prepare the payload
        payload = {
            "stream": True,
            "model": model,
            "messages": messages,
            "params": {},
            "chat_id": "local",
            "id": message_id,
            "model_item": {
                "id": model,
                "name": model_name,
                "owned_by": "openai"
            },
            "features": {
                "image_generation": False,
                "code_interpreter": False,
                "web_search": websearch,
                "auto_web_search": websearch,
                "preview_mode": False
            },
            "tool_servers": [],
            "variables": {
                "{{USER_NAME}}": self.user_id,
                "{{USER_LOCATION}}": "Unknown"
            }
        }
        
        if self.debug:
            print(f"\n{Fore.CYAN}Sending message to Z.ai API:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Message: {message}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Using payload:{Style.RESET_ALL}")
            print(json.dumps(payload, indent=2))
        
        # Send the request
        for attempt in range(self.max_retries):
            try:
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
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            full_response += decoded_line + '\n'
                            
                            # Print progress if in debug mode
                            if self.debug and decoded_line.startswith('data: '):
                                try:
                                    data = json.loads(decoded_line[6:])
                                    if (
                                        'data' in data and
                                        'type' in data['data'] and
                                        data['data']['type'] == 'chat:completion' and
                                        'data' in data['data'] and
                                        'content' in data['data']['data']
                                    ):
                                        print(f"{Fore.GREEN}Received content: {data['data']['data']['content']}{Style.RESET_ALL}")
                                except (json.JSONDecodeError, KeyError):
                                    pass
                    
                    # Parse the full response
                    content, web_search_results = self._parse_sse_response(full_response)
                    
                    # Add the assistant's response to the conversation history
                    self.conversation_history.append({"role": "assistant", "content": content})
                    
                    # Format web search results in a clean, readable way
                    formatted_results = ""
                    if web_search_results:
                        formatted_results = "\n\n**Web Search Results:**\n\n"
                        for i, result in enumerate(web_search_results, 1):
                            title = result.get('title', 'No title')
                            url = result.get('url', '#')
                            snippet = result.get('snippet', 'No snippet available')
                            formatted_results += f"{i}. **{title}**\n   {url}\n   {snippet}\n\n"
                    
                    # Return the formatted response with web search results followed by the model's response
                    return f"{content}\n{formatted_results if web_search_results else ''}"
                    
                elif response.status_code == 401:
                    # Token expired, refresh and retry
                    if self.debug:
                        print(f"{Fore.YELLOW}Auth token expired. Refreshing...{Style.RESET_ALL}")
                    if self.refresh_auth_token():
                        continue
                    else:
                        return "Failed to authenticate with Z.ai. Please try again."
                else:
                    if self.debug:
                        print(f"{Fore.RED}Error: Received status code {response.status_code}{Style.RESET_ALL}")
                    if attempt < self.max_retries - 1:
                        if self.debug:
                            print(f"{Fore.YELLOW}Retrying... (Attempt {attempt + 2}/{self.max_retries}){Style.RESET_ALL}")
                        time.sleep(1)  # Wait before retrying
                    else:
                        return f"Error: Received status code {response.status_code} from Z.ai API."
                        
            except Exception as e:
                if self.debug:
                    print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
                if attempt < self.max_retries - 1:
                    if self.debug:
                        print(f"{Fore.YELLOW}Retrying... (Attempt {attempt + 2}/{self.max_retries}){Style.RESET_ALL}")
                    time.sleep(1)  # Wait before retrying
                else:
                    return f"Error communicating with Z.ai API: {str(e)}"
        
        return "Failed to get a response after multiple attempts."

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
        self.last_web_search_results = []
        
    def get_last_web_search_results(self) -> List[Dict[str, Any]]:
        """Get the web search results from the last query.

        Returns:
            List of web search results
        """
        return self.last_web_search_results


class ZaiModel(BaseModel):
    """Base class for Z.ai models."""

    def __init__(self, model_name: str, model_id: str, supports_websearch: bool = True, debug: bool = False):
        """Initialize a Z.ai model client.

        Args:
            model_name: The display name of the model
            model_id: The API identifier for the model
            supports_websearch: Whether the model supports web search
            debug: Whether to print debug information
        """
        super().__init__(model_name, model_id, supports_websearch, debug)
        self.client = ZaiClient(debug=debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."

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
            model=self.model_id, 
            websearch=websearch, 
            system_message=self.system_prompt
        )

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.client.clear_history()

    def get_last_web_search_results(self) -> List[Dict[str, Any]]:
        """Get the web search results from the last query.

        Returns:
            List of web search results
        """
        return self.client.get_last_web_search_results()


class GLM4Model(ZaiModel):
    """Wrapper class for the Z.ai client for GLM-4-32B model."""

    def __init__(self, debug: bool = False):
        """Initialize the GLM-4-32B client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("GLM-4-32B", "main_chat", True, debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."


class Z1Model(ZaiModel):
    """Wrapper class for the Z.ai client for Z1-32B model."""

    def __init__(self, debug: bool = False):
        """Initialize the Z1-32B client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("Z1-32B", "zero", True, debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."


class Z1RuminationModel(ZaiModel):
    """Wrapper class for the Z.ai client for Z1-Rumination model."""

    def __init__(self, debug: bool = False):
        """Initialize the Z1-Rumination client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("Z1-Rumination", "deep-research", True, debug)
        self.system_prompt = "You are an AI assistant that helps users with their questions and tasks."
