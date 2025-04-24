"""
Transport module for sending logs to Tropir API.
"""

import os
import json
import asyncio
import threading
import httpx
import traceback
import sys
from datetime import datetime
from .config import get_config

# Global httpx client for reuse
_httpx_client = None
_httpx_client_lock = threading.Lock()

def get_httpx_client():
    """
    Get or create a global httpx client for reuse.
    """
    global _httpx_client
    with _httpx_client_lock:
        if _httpx_client is None:
            _httpx_client = httpx.Client(timeout=5)
    return _httpx_client


async def send_log_async(log_data):
    """
    Sends log data to the Tropir API asynchronously.
    
    Args:
        log_data (dict): The log data to send
    """
    config = get_config()
    if not config["enabled"]:
        return
    
    try:
        # Get API key from environment variables
        api_key = os.environ.get("TROPIR_API_KEY")
        if not api_key:
            print("[TROPIR ERROR] API key not found in environment variables")
            return
            
        # Add timestamp for tracking
        log_data["timestamp"] = datetime.now().isoformat()
        
        # Enhance with URL information for HTTP requests
        request_data = log_data.get('request', {})
        if isinstance(request_data, dict):
            url = request_data.get('url')
            if url and isinstance(url, str):
                # Try to extract domain for provider detection
                if "api.openai.com" in url:
                    log_data["provider"] = "openai"
                elif "api.anthropic.com" in url:
                    log_data["provider"] = "anthropic"
                elif "openrouter.ai" in url:
                    log_data["provider"] = "openrouter"
        
        # Ensure we have all required fields
        if "provider" not in log_data:
            log_data["provider"] = "unknown"
            
        if "response" not in log_data:
            log_data["response"] = ""
            
        # Prepare the payload
        payload = {
            "api_key": api_key,
            "log_data": log_data
        }
        
        # Send the request asynchronously
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                config["api_url"],
                json=payload
            )
        
        # Check response status
        if response.status_code >= 300:
            print(f"[TROPIR ERROR] API returned error status: {response.status_code}")
    except httpx.RequestError as e:
        print(f"[TROPIR ERROR] Network error sending log: {e}")
    except json.JSONDecodeError as e:
        print(f"[TROPIR ERROR] JSON encoding error: {e}")
    except Exception as e:
        print(f"[TROPIR ERROR] Failed to send log: {e}")


def send_log(log_data):
    """
    Non-blocking wrapper for sending logs.
    For true speed improvement, this function returns immediately 
    without waiting for any async operations to complete.
    
    Args:
        log_data (dict): The log data to send
    """
    # Copy the log data to avoid modification issues
    log_data_copy = log_data.copy() if isinstance(log_data, dict) else log_data
    
    # Always use the thread approach for consistency and simplicity
    def run_in_thread():
        try:
            # Use synchronous httpx client for simplicity and reliability
            config = get_config()
            if not config["enabled"]:
                return
                
            # Get API key from environment variables
            api_key = os.environ.get("TROPIR_API_KEY")
            if not api_key:
                print("[TROPIR ERROR] API key not found in environment variables")
                return
                
            # Add timestamp for tracking
            log_data_copy["timestamp"] = datetime.now().isoformat()
            
            # Enhance with URL information for HTTP requests
            request_data = log_data_copy.get('request', {})
            if isinstance(request_data, dict):
                url = request_data.get('url')
                if url and isinstance(url, str):
                    # Try to extract domain for provider detection
                    if "api.openai.com" in url:
                        log_data_copy["provider"] = "openai"
                    elif "api.anthropic.com" in url:
                        log_data_copy["provider"] = "anthropic"
                    elif "openrouter.ai" in url:
                        log_data_copy["provider"] = "openrouter"
            
            # Ensure we have all required fields
            if "provider" not in log_data_copy:
                log_data_copy["provider"] = "unknown"
                
            if "response" not in log_data_copy:
                log_data_copy["response"] = ""
                
            # Prepare the payload
            payload = {
                "api_key": api_key,
                "log_data": log_data_copy
            }
            
            # Send the request using a reused client
            client = get_httpx_client()
            response = client.post(
                config["api_url"],
                json=payload
            )
            
            # Check response status
            if response.status_code >= 300:
                print(f"[TROPIR ERROR] API returned error status: {response.status_code}")
        except httpx.RequestError as e:
            print(f"[TROPIR ERROR] Network error sending log: {e}")
        except json.JSONDecodeError as e:
            print(f"[TROPIR ERROR] JSON encoding error: {e}")
        except Exception as e:
            print(f"[TROPIR ERROR] Failed to send log: {e}")
    
    # Start the thread with daemon=True so it doesn't block program exit
    threading.Thread(target=run_in_thread, daemon=True).start() 