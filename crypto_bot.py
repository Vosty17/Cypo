
import os
import streamlit as st
import requests
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

class CryptoBuddy:
    def __init__(self):
        self.name = "CryptoBuddy AI"
        self.last_updated = None
        self.crypto_db = self._initialize_crypto_db()
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

    def _initialize_crypto_db(self):
        """Initialize cryptocurrency database with current prices"""
        return {
            "Bitcoin": {
                "symbol": "BTC",
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3/10,
                "current_price": self._get_live_price("bitcoin"),
                "description": "The first and most well-known cryptocurrency using Proof-of-Work"
            },
            "Ethereum": {
                "symbol": "ETH",
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6/10,
                "current_price": self._get_live_price("ethereum"),
                "description": "Smart contract platform that transitioned to Proof-of-Stake"
            },
            "Cardano": {
                "symbol": "ADA",
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8/10,
                "current_price": self._get_live_price("cardano"),
                "description": "Proof-of-Stake blockchain focused on sustainability"
            },
            "Solana": {
                "symbol": "SOL",
                "price_trend": "volatile",
                "market_cap": "medium",
                "energy_use": "medium",
                "sustainability_score": 5/10,
                "current_price": self._get_live_price("solana"),
                "description": "High-performance blockchain with hybrid consensus model"
            }
        }

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def _get_live_price(_self, coin_id):
        """Get live price from CoinGecko API (mock implementation)"""
        try:
            # Mock prices with slight variations to simulate real market
            mock_prices = {
                "bitcoin": 67432.18 * (0.995 + 0.01 * (time.time() % 10)/10,
                "ethereum": 3287.45 * (0.995 + 0.01 * (time.time() % 10)/10,
                "cardano": 0.45 * (0.995 + 0.01 * (time.time() % 10)/10,
                "solana": 145.67 * (0.995 + 0.01 * (time.time() % 10)/10
            }
            return round(mock_prices.get(coin_id, 0), 2)
        except Exception as e:
            print(f"Error getting price for {coin_id}: {str(e)}")
            return 0

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_ai_insight(_self, question):
        """Get enhanced analysis from DeepSeek API"""
        if not _self.deepseek_api_key:
            return "🔒 API key not configured - using simulated insights"
            
        headers = {
            "Authorization": f"Bearer {_self.deepseek_api_key}",
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
            response.raise_for_status()
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            elif "output" in response_data:
                return response_data["output"]
            else:
                return "⚠️ Received unexpected API response format"
                
        except requests.exceptions.RequestException as e:
            return f"🌐 Network error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"

    def analyze_trends(self):
        """Identify trending cryptocurrencies"""
        return [coin for coin in self.crypto_db 
               if self.crypto_db[coin]["price_trend"] in ["rising", "volatile"]]

    def get_sustainable_coins(self):
        """Find eco-friendly cryptocurrencies"""
        return sorted(
            [(coin, data["sustainability_score"]) 
             for coin, data in self.crypto_db.items()],
            key=lambda x: x[1],
            reverse=True
        )

    def recommend_investment(self, risk_profile="moderate"):
        """Generate investment recommendation based on risk profile"""
        risk_profile = risk_profile.lower()
        
        if risk_profile == "conservative":
            return [coin for coin in self.crypto_db
                   if self.crypto_db[coin]["market_cap"] == "high"]
        elif risk_profile == "aggressive":
            return [coin for coin in self.crypto_db
                   if self.crypto_db[coin]["price_trend"] == "rising"]
        else:  # moderate
            return [coin for coin in self.crypto_db
                   if (self.crypto_db[coin]["price_trend"] in ["rising", "stable"] and
                      self.crypto_db[coin]["market_cap"] in ["high", "medium"])]

    def refresh_data(self):
        """Refresh all cryptocurrency data"""
        self.crypto_db = self._initialize_crypto_db()
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "Data refreshed successfully!"

def display_crypto_card(coin, data):
    """Helper function to display cryptocurrency information in a card"""
    trend_color = {
        "rising": "🟢",
        "stable": "🟡",
        "volatile": "🟠",
        "falling": "🔴"
    }.get(data["price_trend"], "⚪")
    
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.subheader(f"{data['symbol']}")
        with col2:
            st.subheader(f"{coin} {trend_color}")
        
        st.markdown(f"""
        **Price:** ${data['current_price']:,.2f}  
        **Market Cap:** {data['market_cap'].capitalize()}  
        **Sustainability:** {data['sustainability_score']*10:.1f}/10 ({data['energy_use'].capitalize()} energy)  
        *{data['description']}*
        """)
        st.divider()

def main():
    st.set_page_config(
        page_title="CryptoBuddy AI",
        page_icon="🤖",
        layout="wide"
    )
    
    bot = CryptoBuddy()
    
    # Sidebar configuration
    with st.sidebar:
        st.title("CryptoBuddy AI")
        st.markdown("Your personal cryptocurrency advisor")
        
        query_type = st.selectbox(
            "What would you like to know?",
            ["Market Overview", "Trending Cryptos", "Sustainable Picks", 
             "Investment Advice", "Ask AI", "About"]
        )
        
        if st.button("🔄 Refresh Data"):
            refresh_status = bot.refresh_data()
            st.toast(refresh_status)
        
        st.markdown("""
        ---
        **Disclaimer**:  
        Cryptocurrency investments are highly volatile and risky.  
        This application provides informational insights only.  
        Always conduct your own research before making financial decisions.
        """)
    
    # Main content area
    if query_type == "Market Overview":
        st.header("📊 Cryptocurrency Market Overview")
        st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        cols = st.columns(4)
        for idx, (coin, data) in enumerate(bot.crypto_db.items()):
            with cols[idx % 4]:
                with st.container(border=True):
                    st.markdown(f"**{coin} ({data['symbol']})**")
                    st.markdown(f"${data['current_price']:,.2f}")
                    st.progress(data['sustainability_score'], 
                               text=f"Sustainability: {data['sustainability_score']*10:.1f}/10")
        
        st.divider()
        st.subheader("Detailed View")
        selected_coin = st.selectbox("Select cryptocurrency", list(bot.crypto_db.keys()))
        display_crypto_card(selected_coin, bot.crypto_db[selected_coin])
        
    elif query_type == "Trending Cryptos":
        st.header("🚀 Trending Cryptocurrencies")
        trending = bot.analyze_trends()
        
        if trending:
            for coin in trending:
                display_crypto_card(coin, bot.crypto_db[coin])
        else:
            st.warning("No strong trending patterns detected currently")
            
    elif query_type == "Sustainable Picks":
        st.header("🌱 Sustainable Cryptocurrencies")
        sustainable = bot.get_sustainable_coins()
        
        for coin, score in sustainable:
            data = bot.crypto_db[coin]
            with st.expander(f"{coin} ({data['symbol']}) - Sustainability Score: {score*10:.1f}/10"):
                st.markdown(f"""
                **Current Price:** ${data['current_price']:,.2f}  
                **Energy Use:** {data['energy_use'].capitalize()}  
                **Market Cap:** {data['market_cap'].capitalize()}  
                **Description:** {data['description']}
                """)
                
    elif query_type == "Investment Advice":
        st.header("💼 Personalized Investment Recommendations")
        
        risk_profile = st.radio(
            "Select your risk profile:",
            ["Conservative", "Moderate", "Aggressive"],
            horizontal=True
        )
        
        recommendations = bot.recommend_investment(risk_profile.lower())
        
        if recommendations:
            st.balloons()
            st.success("Based on your risk profile, consider these cryptocurrencies:")
            
            cols = st.columns(len(recommendations))
            for idx, coin in enumerate(recommendations):
                data = bot.crypto_db[coin]
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"**{coin} ({data['symbol']})**")
                        st.markdown(f"${data['current_price']:,.2f}")
                        st.markdown(f"*{data['price_trend'].capitalize()} trend*")
            
            st.markdown("""
            ---
            **Remember**:  
            - Diversify your investments  
            - Only invest what you can afford to lose  
            - Consider dollar-cost averaging strategy  
            """)
            
    elif query_type == "Ask AI":
        st.header("🧠 Ask CryptoBuddy AI")
        
        with st.expander("💡 Sample questions"):
            st.markdown("""
            - What's the difference between Bitcoin and Ethereum?
            - Should I invest in Cardano right now?
            - Explain Proof-of-Stake vs Proof-of-Work
            - What are the risks of investing in cryptocurrencies?
            """)
        
        user_question = st.text_input("Ask anything about cryptocurrencies:", 
                                    placeholder="Type your question here...")
        
        if user_question:
            with st.spinner("Analyzing market data and preparing insights..."):
                ai_response = bot.get_ai_insight(user_question)
                
                st.markdown(f"""
                <div style='background-color:#f0f2f6; padding:15px; border-radius:10px;'>
                <b>🤖 CryptoBuddy AI Analysis:</b><br><br>
                {ai_response}
                </div>
                """, unsafe_allow_html=True)
                
    elif query_type == "About":
        st.header("ℹ️ About CryptoBuddy AI")
        st.markdown("""
        CryptoBuddy AI is your intelligent cryptocurrency advisor that provides:
        
        - Real-time market insights
        - Sustainability analysis
        - Personalized investment recommendations
        - AI-powered Q&A about cryptocurrencies
        
        **Features**:
        - Market overview with current prices
        - Trending cryptocurrencies identification
        - Eco-friendly crypto recommendations
        - Risk-adjusted investment suggestions
        - AI-powered question answering
        
        **Technology Stack**:
        - Python with Streamlit for the web interface
        - DeepSeek AI for natural language processing
        - CoinGecko API for cryptocurrency data (simulated in this demo)
        
        *Note: This is a demonstration application. Prices and insights are simulated.*
        """)

if __name__ == "__main__":
    main()
