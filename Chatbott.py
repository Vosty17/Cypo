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
        # In production, replace with actual API call:
        # response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
        # return response.json()[coin_id]["usd"]
        mock_prices = {
            "bitcoin": 67432.18,
            "ethereum": 3287.45,
            "cardano": 0.45
        }
        return mock_prices.get(coin_id, 0)

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
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"AI service error: {str(e)}"

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

def main():
    st.set_page_config(page_title="CryptoBuddy AI", page_icon="🤖")
    
    bot = CryptoBuddy()
    
    st.title(f"Welcome to {bot.name}!")
    st.markdown("""
    Your AI-powered cryptocurrency advisor. Get insights on:
    - 📈 Market trends
    - ♻️ Sustainable coins
    - 💰 Investment opportunities
    """)
    
    query_type = st.sidebar.selectbox(
        "What would you like to know?",
        ["Trending Cryptos", "Sustainable Picks", "Investment Advice", "Ask AI"]
    )
    
    if query_type == "Trending Cryptos":
        st.subheader("🚀 Currently Trending Cryptocurrencies")
        trending = bot.analyze_trends()
        if trending:
            for coin in trending:
                data = bot.crypto_db[coin]
                st.success(f"""
                **{coin}**
                - Price: ${data['current_price']:,.2f}
                - Market Cap: {data['market_cap'].capitalize()}
                - Trend: {data['price_trend'].capitalize()}
                """)
        else:
            st.warning("No strong trending patterns detected")
            
    elif query_type == "Sustainable Picks":
        st.subheader("🌱 Most Sustainable Cryptocurrencies")
        sustainable = bot.get_sustainable_coins()
        for coin, score in sustainable:
            st.info(f"""
            **{coin}**
            - Sustainability Score: {score*10:.1f}/10
            - Energy Use: {bot.crypto_db[coin]['energy_use'].capitalize()}
            - Current Price: ${bot.crypto_db[coin]['current_price']:,.2f}
            """)
            
    elif query_type == "Investment Advice":
        st.subheader("💼 Investment Recommendations")
        recommendations = bot.recommend_investment()
        st.balloons()
        st.success(f"""
        Based on current market data, consider these cryptocurrencies:
        {', '.join(recommendations)}
        
        *Remember: Past performance doesn't guarantee future results*
        """)
        
    elif query_type == "Ask AI":
        st.subheader("🧠 Ask CryptoBuddy AI")
        user_question = st.text_input("Ask anything about cryptocurrencies:")
        if user_question:
            with st.spinner("Analyzing market data..."):
                ai_response = bot.get_ai_insight(user_question)
                st.markdown(f"""
                <div style='background-color:#f0f2f6; padding:15px; border-radius:10px;'>
                <b>AI Analysis:</b><br>{ai_response}
                </div>
                """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    ---
    **Disclaimer**:  
    Crypto investments are risky.  
    This is not financial advice.  
    Always do your own research.
    """)

if __name__ == "__main__":
    main()