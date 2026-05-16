"""JNTUH Results API client."""

import requests
from typing import Dict
from ..config.settings import Settings


class JNTUHClient:
    """Client for fetching JNTUH academic results."""
    
    def __init__(self):
        self.api_url = Settings.JNTUH_API_URL
        self.timeout = Settings.API_TIMEOUT
    
    def fetch_results(self, hall_ticket: str) -> Dict:
        """
        Fetch academic results for a given hall ticket number.
        
        Args:
            hall_ticket: Student's hall ticket number (10 characters)
            
        Returns:
            Dictionary containing results or error information
        """
        try:
            # Validate hall ticket length (API requires exactly 10 characters)
            if len(hall_ticket) != 10:
                return {"error": "Hall ticket number must be exactly 10 characters"}
            
            # API endpoint: /api/getAcademicResult?rollNumber=XXXXXXXXXX
            url = f"{self.api_url}?rollNumber={hall_ticket}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response indicates success
                if isinstance(data, dict):
                    # Check for error in response
                    if "error" in data:
                        return {"error": data["error"]}
                    
                    # Check if data contains results (API uses lowercase keys)
                    if "details" in data or "results" in data:
                        return {"success": True, "data": data}
                    
                    # If response is empty or invalid
                    return {"error": "No results found for this hall ticket"}
                
                return {"success": True, "data": data}
                
            elif response.status_code == 422:
                return {"error": "Invalid hall ticket format. Please check and try again."}
            elif response.status_code == 404:
                return {"error": "Results not found for this hall ticket"}
            else:
                return {"error": f"Unable to fetch results. Status: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
