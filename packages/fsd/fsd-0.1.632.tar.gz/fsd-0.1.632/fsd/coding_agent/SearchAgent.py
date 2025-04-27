import os
import aiohttp
import sys
import asyncio


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class SearchAgent:
    def __init__(self):
        self.model = "sonar"  # Default model

    async def get_search_plan(self, queries):
        """
        Process multiple search queries concurrently using Perplexity API.
        
        Args:
            queries (list): List of search queries to process.
            
        Returns:
            list: List of search results corresponding to each query.
        """
        if not queries:
            return []
            
        logger.info(f"#### `SnowX` is processing {len(queries)} search queries")
        tasks = [self._process_query(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        return results
        
    async def _process_query(self, query):
        """
        Process a single search query using Perplexity API.
        
        Args:
            query (str): The search query to process.
            
        Returns:
            dict: The search result.
        """
        logger.info(f"#### `SnowX` is searching: {query}")
        
        try:
            result = await self._search_perplexity(query)
            logger.info(f"#### `SnowX` search completed: {query}")
            return result
        except Exception as e:
            logger.error(f"#### `SnowX` search failed for query '{query}': {str(e)}")
            return {"query": query, "error": str(e), "result": None}
    
    async def _search_perplexity(self, query):
        """
        Make a request to the Perplexity API.
        
        Args:
            query (str): The search query.
            
        Returns:
            dict: The API response.
        """
        messages = [
            {
                "role": "system",
                "content": "You are a specialized real-time data collection agent focused on gathering maximum quantitative information, statistics, and factual data. Your primary mission is to collect as much valuable data as possible."
            },
            {
                "role": "user",
                "content": f"Today is {self._get_current_date()}. Focus on the most recent and up-to-date information available. I need the latest news, developments, and data on this topic: {query}"
            }
        ]
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    "https://api.snowx.io/api/perplexity/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "return_images": True,
                        "web_search_options": {
                            "search_context_size": "high"
                        }
                    },
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Perplexity API error: {error_text}")
                        return {"query": query, "error": f"API returned status {response.status}", "result": None}
                    
                    response_data = await response.json()
                    content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    citations = response_data.get("citations", [])
                    images = response_data.get("images", [])
                    
                    return {
                        "query": query,
                        "result": content,
                        "citations": citations,
                        "images": images,
                        "response": response_data
                    }
            except Exception as e:
                logger.error(f"Error making request to Perplexity API: {str(e)}")
                return {"query": query, "error": str(e), "result": None}
    
    def _get_current_date(self):
        """Get the current date in a formatted string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")



