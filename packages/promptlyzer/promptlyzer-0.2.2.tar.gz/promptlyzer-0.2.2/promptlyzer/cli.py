import argparse
import json
import os
import sys
import time
from typing import Dict, Any, List, Optional

from .client import PromptlyzerClient
from .prompt_manager import PromptManager
from .exceptions import PromptlyzerError
from .utils import prettify_json


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Promptlyzer CLI - Manage and analyze prompts from the command line"
    )
    
    parser.add_argument(
        "--api-url", 
        help="Promptlyzer API URL. Can also be set via PROMPTLYZER_API_URL env variable."
    )
    parser.add_argument(
        "--email", 
        help="Email for authentication. Can also be set via PROMPTLYZER_EMAIL env variable."
    )
    parser.add_argument(
        "--password", 
        help="Password for authentication. Can also be set via PROMPTLYZER_PASSWORD env variable."
    )
    parser.add_argument(
        "--env", 
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment (dev, staging, prod). Default: dev"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching for this operation"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    list_parser = subparsers.add_parser("list", help="List all prompts in a project (latest versions)")
    list_parser.add_argument("project_id", help="Project ID")
    
    get_parser = subparsers.add_parser("get", help="Get a specific prompt (latest version)")
    get_parser.add_argument("project_id", help="Project ID")
    get_parser.add_argument("prompt_name", help="Prompt name")
    
    monitor_parser = subparsers.add_parser("monitor", help="Monitor prompts for updates")
    monitor_parser.add_argument("project_id", help="Project ID")
    monitor_parser.add_argument(
        "--interval",
        type=int,
        default=180,
        help="Update interval in seconds (default: 180)"
    )
    monitor_parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    clear_cache_parser = subparsers.add_parser("clear-cache", help="Clear prompt cache")
    clear_cache_parser.add_argument("project_id", help="Project ID")
    clear_cache_parser.add_argument("--prompt-name", help="Optional: Prompt name to clear specific prompt cache")
    
    return parser


def prompt_updated_callback(prompt_name: str, prompt_data: Dict[str, Any], output_format: str):
    """Callback function when a prompt is updated."""
    print(f"Updated prompt: {prompt_name}")
    
    if output_format == "json":
        print(prettify_json(prompt_data))
    else:
        print(f"  Version: {prompt_data.get('current_version')}")
        if "version" in prompt_data and "content" in prompt_data["version"]:
            content = prompt_data["version"]["content"]
            print(f"  Content: {content[:100]}..." if len(content) > 100 else f"  Content: {content}")
        print()


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        client = PromptlyzerClient(
            api_url=args.api_url,
            email=args.email,
            password=args.password,
            environment=args.env
        )
        
        use_cache = not args.no_cache
        
        if args.command == "list":
            result = client.list_prompts(args.project_id, use_cache=use_cache)
            print(prettify_json(result))
        
        elif args.command == "get":
            result = client.get_prompt(args.project_id, args.prompt_name, use_cache=use_cache)
            print(prettify_json(result))
        
        elif args.command == "monitor":
            def callback(prompt_name, prompt_data):
                prompt_updated_callback(prompt_name, prompt_data, args.output)
            
            manager = PromptManager(
                client,
                args.project_id,
                update_interval=args.interval,
                on_update_callback=callback
            )
            
            print(f"Monitoring prompts in project {args.project_id} (Ctrl+C to stop)...")
            print(f"Update interval: {args.interval} seconds")
            
            # Start monitoring
            manager.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping monitor...")
                manager.stop()
        
        elif args.command == "clear-cache":
            client.clear_prompt_cache(args.project_id, args.prompt_name)
            print(f"Cache cleared for project {args.project_id}" + 
                  (f", prompt {args.prompt_name}" if args.prompt_name else ""))
    
    except PromptlyzerError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":