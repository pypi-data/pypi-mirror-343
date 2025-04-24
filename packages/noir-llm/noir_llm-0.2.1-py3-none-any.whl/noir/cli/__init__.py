"""
Command-line interface for Noir package.

This module provides a command-line interface for interacting with
language models through the Noir package.
"""

import argparse
import sys
from typing import List, Optional
from colorama import Fore, Style, init

from noir import __version__
from noir.models import list_models, get_model
from noir.client import NoirClient

# Initialize colorama
init(autoreset=True)

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the Noir CLI.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="Noir - A Python package for accessing various LLM models"
    )
    
    parser.add_argument(
        "--version", "-v", action="version", 
        version=f"Noir v{__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List models command
    list_parser = subparsers.add_parser("list", help="List available models")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start an interactive chat session")
    chat_parser.add_argument(
        "--model", "-m", type=str, 
        help="Model to use for the chat session"
    )
    chat_parser.add_argument(
        "--websearch", "-w", action="store_true", 
        help="Enable web search for the chat session"
    )
    chat_parser.add_argument(
        "--system-prompt", "-s", type=str, 
        help="Set a system prompt for the chat session"
    )
    chat_parser.add_argument(
        "--debug", "-d", action="store_true", 
        help="Enable debug mode"
    )
    
    # Send message command
    send_parser = subparsers.add_parser("send", help="Send a single message")
    send_parser.add_argument(
        "message", type=str, 
        help="Message to send"
    )
    send_parser.add_argument(
        "--model", "-m", type=str, required=True, 
        help="Model to use for the message"
    )
    send_parser.add_argument(
        "--websearch", "-w", action="store_true", 
        help="Enable web search for the message"
    )
    send_parser.add_argument(
        "--system-prompt", "-s", type=str, 
        help="Set a system prompt for the message"
    )
    send_parser.add_argument(
        "--debug", "-d", action="store_true", 
        help="Enable debug mode"
    )
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    # Handle commands
    if parsed_args.command == "list":
        return handle_list_command()
    elif parsed_args.command == "chat":
        return handle_chat_command(parsed_args)
    elif parsed_args.command == "send":
        return handle_send_command(parsed_args)
    else:
        parser.print_help()
        return 0

def handle_list_command() -> int:
    """Handle the 'list' command.
    
    Returns:
        Exit code
    """
    models = list_models()
    
    print(f"\n{Fore.CYAN}Available models:{Style.RESET_ALL}")
    for i, model_id in enumerate(models, 1):
        model = get_model(model_id)
        print(f"{i}. {Fore.GREEN}{model.get_model_name()}{Style.RESET_ALL} ({model_id})")
        if model.supports_web_search():
            print(f"   {Fore.BLUE}Supports web search{Style.RESET_ALL}")
    
    return 0

def handle_chat_command(args) -> int:
    """Handle the 'chat' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    # Create client
    client = NoirClient(debug=args.debug)
    
    # Select model
    if args.model:
        if not client.select_model(args.model):
            print(f"{Fore.RED}Error: Model '{args.model}' not found.{Style.RESET_ALL}")
            return 1
    else:
        # Let the user select a model
        models = list_models()
        
        print(f"\n{Fore.CYAN}Available models:{Style.RESET_ALL}")
        for i, model_id in enumerate(models, 1):
            model = get_model(model_id)
            print(f"{i}. {Fore.GREEN}{model.get_model_name()}{Style.RESET_ALL} ({model_id})")
            if model.supports_web_search():
                print(f"   {Fore.BLUE}Supports web search{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"\n{Fore.GREEN}Select a model (1-{len(models)}): {Style.RESET_ALL}")
                index = int(choice) - 1
                if 0 <= index < len(models):
                    if not client.select_model(models[index]):
                        print(f"{Fore.RED}Error selecting model. Please try again.{Style.RESET_ALL}")
                    else:
                        break
                else:
                    print(f"{Fore.RED}Invalid selection. Please try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    
    # Set system prompt if provided
    if args.system_prompt:
        client.set_system_prompt(args.system_prompt)
    
    # Start chat loop
    print(f"\n{Fore.CYAN}Starting chat with {client.get_current_model()}. Type 'exit' or 'quit' to end the session.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Web search is {'enabled' if args.websearch else 'disabled'}.{Style.RESET_ALL}")
    
    while True:
        try:
            user_input = input(f"\n{Fore.GREEN}You: {Style.RESET_ALL}")
            
            if user_input.lower() in ["exit", "quit"]:
                print(f"\n{Fore.CYAN}Ending chat session.{Style.RESET_ALL}")
                break
            
            print(f"\n{Fore.YELLOW}Thinking...{Style.RESET_ALL}")
            response = client.send_message(user_input, websearch=args.websearch)
            
            print(f"\n{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}Chat session interrupted.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    return 0

def handle_send_command(args) -> int:
    """Handle the 'send' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    # Create client
    client = NoirClient(debug=args.debug)
    
    # Select model
    if not client.select_model(args.model):
        print(f"{Fore.RED}Error: Model '{args.model}' not found.{Style.RESET_ALL}")
        return 1
    
    # Set system prompt if provided
    if args.system_prompt:
        client.set_system_prompt(args.system_prompt)
    
    # Send message
    try:
        print(f"\n{Fore.YELLOW}Sending message to {client.get_current_model()}...{Style.RESET_ALL}")
        response = client.send_message(args.message, websearch=args.websearch)
        
        print(f"\n{Fore.BLUE}Response: {Style.RESET_ALL}{response}")
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
