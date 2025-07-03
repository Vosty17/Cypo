
import streamlit as st
from crypto_bot import CryptoBuddy  # Your existing class
# Initialize bot
bot = CryptoBuddy()

# Sidebar filters
st.sidebar.header("🔍 Custom Search")
user_coin = st.sidebar.text_input("Enter a cryptocurrency (e.g. Bitcoin):").strip()
custom_question = st.sidebar.text_area("Ask CryptoBuddy anything:")

# Main panel
if user_coin:
    if user_coin in bot.crypto_db:
        data = bot.crypto_db[user_coin]
        st.success(f"""
        **{user_coin} Analysis**  
        💵 Price: ${data['current_price']:,.2f}  
        ♻️ Sustainability: {data['sustainability_score']*10}/10  
        📈 Trend: {data['price_trend'].capitalize()}  
        """)
    else:
        st.error(f"{user_coin} not in database. Try: {', '.join(bot.crypto_db.keys())}")

if custom_question:
    with st.spinner("🧠 Analyzing..."):
        response = bot.get_ai_insight(f"{custom_question} {user_coin}" if user_coin else custom_question)
        st.markdown(f"""
        <div style='background:#f0f2f6;padding:10px;border-radius:8px;'>
        💡 <b>AI Response:</b><br>{response}
        </div>
        """, unsafe_allow_html=True)
