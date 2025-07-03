import os
import streamlit as st
import requests
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv()

class CryptoBuddy:
    def __init__(self):
        self.name = "CryptoBuddy AI"
        self.version = "2.0"
        self.last_updated = None
        self.crypto_db = self._initialize_crypto_db()
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.coin_icons = {
            "Bitcoin": "₿",
            "Ethereum": "Ξ",
            "Cardano": "₳",
            "Solana": "◎"
        }

    def _initialize_crypto_db(self):
        """Initialize cryptocurrency database with current prices"""
        return {
            "Bitcoin": {
                "symbol": "BTC",
                "price_trend": "rising",
                "market_cap": 1.3e12,  # in USD
                "energy_use": "high",
                "sustainability_score": 3/10,
                "current_price": self._get_live_price("bitcoin"),
                "description": "The original cryptocurrency using Proof-of-Work consensus",
                "launch_year": 2009
            },
            "Ethereum": {
                "symbol": "ETH",
                "price_trend": "stable",
                "market_cap": 400e9,  # in USD
                "energy_use": "medium",
                "sustainability_score": 6/10,
                "current_price": self._get_live_price("ethereum"),
                "description": "Smart contract platform that transitioned to Proof-of-Stake",
                "launch_year": 2015
            },
            "Cardano": {
                "symbol": "ADA",
                "price_trend": "rising",
                "market_cap": 15e9,  # in USD
                "energy_use": "low",
                "sustainability_score": 8/10,
                "current_price": self._get_live_price("cardano"),
                "description": "Research-driven Proof-of-Stake blockchain",
                "launch_year": 2017
            },
            "Solana": {
                "symbol": "SOL",
                "price_trend": "volatile",
                "market_cap": 60e9,  # in USD
                "energy_use": "medium",
                "sustainability_score": 5/10,
                "current_price": self._get_live_price("solana"),
                "description": "High-performance blockchain with hybrid consensus",
                "launch_year": 2020
            }
        }

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def _get_live_price(_self, coin_id):
        """Get live price from CoinGecko API (mock implementation)"""
        try:
            # Simulate realistic price fluctuations
            base_prices = {
                "bitcoin": 67432.18,
                "ethereum": 3287.45,
                "cardano": 0.45,
                "solana": 145.67
            }
            fluctuation = 0.995 + 0.01 * (time.time() % 10)/10
            return round(base_prices[coin_id] * fluctuation, 2)
        except Exception as e:
            st.error(f"Error getting price for {coin_id}: {str(e)}")
            return 0

    def get_ai_insight(self, question):
        """Get enhanced analysis from DeepSeek API"""
        if not self.deepseek_api_key:
            return "🔒 API key not configured - using simulated insights"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": question}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            with st.spinner("🧠 Analyzing with AI..."):
                response = requests.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=15
                )
                response.raise_for_status()
                response_data = response.json()
                
                if "choices" in response_data and response_data["choices"]:
                    return response_data["choices"][0]["message"]["content"]
                return "⚠️ No response content found"
                
        except requests.exceptions.RequestException as e:
            return f"🌐 Network error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"

    def analyze_trends(self):
        """Identify trending cryptocurrencies"""
        return sorted(
            [(coin, data) for coin, data in self.crypto_db.items() 
             if data["price_trend"] in ["rising", "volatile"]],
            key=lambda x: x[1]["market_cap"],
            reverse=True
        )

    def get_sustainable_coins(self):
        """Find eco-friendly cryptocurrencies"""
        return sorted(
            [(coin, data) for coin, data in self.crypto_db.items()],
            key=lambda x: x[1]["sustainability_score"],
            reverse=True
        )

    def recommend_investment(self, risk_profile="moderate"):
        """Generate investment recommendation based on risk profile"""
        risk_profile = risk_profile.lower()
        
        if risk_profile == "conservative":
            return [coin for coin, data in self.crypto_db.items()
                   if data["market_cap"] > 100e9]  # Large caps only
        elif risk_profile == "aggressive":
            return [coin for coin, data in self.crypto_db.items()
                   if data["price_trend"] == "rising" and data["market_cap"] < 50e9]
        else:  # moderate
            return [coin for coin, data in self.crypto_db.items()
                   if data["market_cap"] > 10e9 and data["sustainability_score"] >= 0.5]

    def refresh_data(self):
        """Refresh all cryptocurrency data"""
        self.crypto_db = self._initialize_crypto_db()
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "Data refreshed successfully!"

def display_crypto_card(coin, data, icon=""):
    """Display cryptocurrency information in a styled card"""
    trend_icons = {
        "rising": "📈",
        "stable": "➡️",
        "volatile": "🌊",
        "falling": "📉"
    }
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### {icon} {data['symbol']}")
        with col2:
            st.markdown(f"### {coin} {trend_icons.get(data['price_trend'], '')}")
        
        st.markdown(f"""
        **Price:** ${data['current_price']:,.2f}  
        **Market Cap:** ${data['market_cap']/1e9:.2f}B  
        **Sustainability:** {data['sustainability_score']*10:.1f}/10 🌱  
        **Energy Use:** {data['energy_use'].capitalize()} ⚡  
        **Launched:** {data['launch_year']}  
        """)
        
        with st.expander("ℹ️ Description"):
            st.markdown(data['description'])

def main():
    st.set_page_config(
        page_title="CryptoBuddy AI",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    bot = CryptoBuddy()
    
    # Sidebar configuration
    with st.sidebar:
        st.title(f"{bot.name} v{bot.version}")
        st.markdown("Your intelligent cryptocurrency advisor")
        
        query_type = st.selectbox(
            "Menu",
            ["📊 Market Dashboard", "🚀 Trending Coins", "🌱 Green Crypto", 
             "💼 Investment Advisor", "🧠 Ask CryptoBuddy", "ℹ️ About"]
        )
        
        if st.button("🔄 Refresh All Data", use_container_width=True):
            with st.spinner("Refreshing data..."):
                refresh_status = bot.refresh_data()
                st.toast(refresh_status, icon="✅")
        
        st.markdown("---")
        st.markdown("""
        **Disclaimer**:  
        Cryptocurrency investments are volatile.  
        This is not financial advice.  
        Always conduct your own research.
        """)
    
    # Main content area
    st.header(f"{query_type.split(' ')[1]} Overview" if " " in query_type else f"{query_type} Overview")
    
    if query_type == "📊 Market Dashboard":
        st.subheader("Real-time Cryptocurrency Data")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        cols = st.columns(4)
        for idx, (coin, data) in enumerate(bot.crypto_db.items()):
            with cols[idx % 4]:
                display_crypto_card(coin, data, bot.coin_icons.get(coin, ""))
        
        st.divider()
        st.subheader("Market Summary")
        st.markdown("""
        - **Total Market Cap:** $1.8T
        - **24h Volume:** $85B
        - **Market Sentiment:** Neutral
        """)
        
    elif query_type == "🚀 Trending Coins":
        trending = bot.analyze_trends()
        
        if trending:
            st.subheader("Currently Trending Cryptocurrencies")
            for coin, data in trending:
                display_crypto_card(coin, data, bot.coin_icons.get(coin, ""))
        else:
            st.warning("No strong trending patterns detected currently")
            
    elif query_type == "🌱 Green Crypto":
        sustainable = bot.get_sustainable_coins()
        
        st.subheader("Most Sustainable Cryptocurrencies")
        for coin, data in sustainable:
            with st.expander(f"{bot.coin_icons.get(coin, '')} {coin} - Sustainability Score: {data['sustainability_score']*10:.1f}/10", expanded=True):
                display_crypto_card(coin, data)
                
    elif query_type == "💼 Investment Advisor":
        st.subheader("Personalized Investment Recommendations")
        
        risk_profile = st.radio(
            "Your Risk Profile:",
            ["Conservative", "Moderate", "Aggressive"],
            horizontal=True,
            index=1
        )
        
        recommendations = bot.recommend_investment(risk_profile.lower())
        
        if recommendations:
            st.success(f"Based on your **{risk_profile}** risk profile:", icon="💡")
            
            cols = st.columns(len(recommendations))
            for idx, coin in enumerate(recommendations):
                data = bot.crypto_db[coin]
                with cols[idx]:
                    display_crypto_card(coin, data, bot.coin_icons.get(coin, ""))
            
            st.markdown("""
            **Investment Strategy Tips:**
            - Consider dollar-cost averaging
            - Diversify across 3-5 assets
            - Rebalance portfolio quarterly
            """)
            
    elif query_type == "🧠 Ask CryptoBuddy":
        st.subheader("AI-Powered Crypto Insights")
        
        with st.expander("💡 Sample Questions", expanded=True):
            st.markdown("""
            - What's the difference between PoW and PoS?
            - Is now a good time to invest in Bitcoin?
            - Explain Cardano's Ouroboros protocol
            - What are the risks of DeFi investments?
            """)
        
        question = st.text_input("Ask anything about cryptocurrencies:", 
                               placeholder="Type your question here...")
        
        if question:
            response = bot.get_ai_insight(question)
            st.markdown(f"""
            <div style='
                background-color:#f8f9fa;
                padding:15px;
                border-radius:10px;
                border-left:4px solid #6c757d;
                margin-top:10px;
            '>
            <strong>🤖 CryptoBuddy Analysis:</strong><br><br>
            {response}
            </div>
            """, unsafe_allow_html=True)
            
    elif query_type == "ℹ️ About":
        st.subheader("About CryptoBuddy AI")
        st.markdown(f"""
        **Version:** {bot.version}  
        **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}  
        
        CryptoBuddy AI combines real-time market data with artificial intelligence to provide:
        - Comprehensive cryptocurrency analysis
        - Sustainability ratings
        - Personalized investment guidance
        - Educational resources
        
        **Data Sources:**  
        - CoinGecko API (simulated in demo)  
        - DeepSeek AI  
        - Latest blockchain research  
        
        **Disclaimer:**  
        This application is for educational purposes only.  
        Cryptocurrency investments carry substantial risk.
        """)

if __name__ == "__main__":
    main()
