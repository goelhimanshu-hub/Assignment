import streamlit as st
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🎬 Movie & Series Watch Planner",
    page_icon="🍿",
    layout="centered"
)

# ---------------- API KEY (STREAMLIT SECRETS) ----------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center'>🎬 Movie & Series Watch Planner</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray'>Plan the perfect movie night or binge weekend 🍿</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- INPUT SECTION ----------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mood = st.selectbox(
        "🎭 Choose your mood",
        ["Thriller", "Feel-Good", "Mystery", "Romance", "Comedy", "Horror"]
    )

    time_available = st.selectbox(
        "⏱️ Time available",
        ["1–2 hours", "3–5 hours", "6+ hours", "Whole Weekend"]
    )

    platform = st.selectbox(
        "📺 Streaming platform",
        ["Netflix", "Amazon Prime", "Disney+", "Hotstar"]
    )

    generate = st.button("✨ Generate Watch Plan")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- GROQ FUNCTION ----------------
def generate_watch_plan(mood, time_available, platform):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are a movie and TV series watch planner.

Rules:
- Suggest only content available on the given platform
- Maximum 3 items
- Include watch order
- Include short synopsis (2–3 lines)
- Include snack suggestions
- Use clean markdown formatting
"""
            },
            {
                "role": "user",
                "content": f"""
Mood: {mood}
Time Available: {time_available}
Streaming Platform: {platform}
"""
            }
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content

# ---------------- OUTPUT SECTION ----------------
if generate:
    with st.spinner("🎥 Creating your personalized watch plan..."):
        result = generate_watch_plan(mood, time_available, platform)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📺 Your Watch Plan")
    st.markdown(result)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Made with ❤️ using Streamlit & Groq</div>",
    unsafe_allow_html=True
)
