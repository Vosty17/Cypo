
import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CryptoBuddy:
    def __init__(self):
        self.name = "CryptoBuddy AI"
        self.crypto_db = {
            "Bitcoin": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3/10,
                "current_price": self._get_live_price("bitcoin")
            },
            "Ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6/10,
                "current_price": self._get_live_price("ethereum")
            },
            "Cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8/10,
                "current_price": self._get_live_price("cardano")
            }
        }
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

    def _get_live_price(self, coin_id):
        """Get live price from CoinGecko API (mock implementation)"""
        try:
            # In production, replace with actual API call:
            # response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
            # return response.json()[coin_id]["usd"]
            mock_prices = {
                "bitcoin": 67432.18,
                "ethereum": 3287.45,
                "cardano": 0.45
            }
            return mock_prices.get(coin_id, 0)
        except Exception as e:
            print(f"Error getting price for {coin_id}: {str(e)}")
            return 0

    def get_ai_insight(self, question):
        """Get enhanced analysis from DeepSeek API"""
        if not self.deepseek_api_key:
            return "API key not configured"
            
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": question}],
                    "temperature": 0.7
                },
                headers=headers,
                timeout=10
            )
            response.raise_for_status()  # Raises exception for 4XX/5XX errors
            response_data = response.json()
            
            # Handle the response based on DeepSeek's actual structure
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            elif "output" in response_data:  # Alternative structure
                return response_data["output"]
            else:
                return f"Unexpected API response format: {response_data}"
                
        except requests.exceptions.RequestException as e:
            return f"API request failed: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def analyze_trends(self):
        """Identify trending cryptocurrencies"""
        return [coin for coin in self.crypto_db 
               if self.crypto_db[coin]["price_trend"] == "rising"]

    def get_sustainable_coins(self):
        """Find eco-friendly cryptocurrencies"""
        return sorted(
            [(coin, data["sustainability_score"]) 
             for coin, data in self.crypto_db.items()],
            key=lambda x: x[1],
            reverse=True
        )

    def recommend_investment(self):
        """Generate investment recommendation"""
        profitable = [
            coin for coin in self.crypto_db
            if (self.crypto_db[coin]["price_trend"] == "rising" and
                self.crypto_db[coin]["market_cap"] in ["high", "medium"])
        ]
        return profitable or list(self.crypto_db.keys())

# Rest of the code remains the same...
