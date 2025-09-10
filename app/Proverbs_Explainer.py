import streamlit as st
import json
import random

# --- Load the proverbs dataset ---
@st.cache_data
def load_proverbs(file_path=r"C:\Users\Khechane\Desktop\AI-Proverbs-Project\data\proverbs.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Find and explain a proverb ---
def explain_proverb(user_input, proverbs):
    user_input = user_input.strip().lower()

    # Exact Sesotho match
    for item in proverbs:
        if user_input in item["proverb"].lower():
            return item

    # English translation or meaning keywords
    for item in proverbs:
        if (user_input in item["translation"].lower()) or (user_input in item["meaning"].lower()):
            return item

    # Fallback: random proverb
    return random.choice(proverbs)

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="Sesotho Proverbs Explainer", page_icon="📜")
    st.title("📜 Sesotho Proverbs Explainer")
    st.caption("Preserving 🇱🇸 Basotho wisdom through technology.")

    proverbs = load_proverbs()

    user_input = st.text_input("🔍 Enter a keyword, a Sesotho proverb, or an English phrase")

    if user_input:
        result = explain_proverb(user_input, proverbs)

        if user_input.lower() not in result["proverb"].lower() \
           and user_input.lower() not in result["translation"].lower() \
           and user_input.lower() not in result["meaning"].lower():
            st.warning("🙁 Proverb not found. Here's a random one to reflect on:")

        st.markdown("### 📖 Proverb")
        st.markdown(f"**Sesotho:** {result['proverb']}")
        st.markdown(f"**Translation:** {result['translation']}")
        st.markdown(f"**Meaning:** {result['meaning']}")

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit | [streamlit.io](https://streamlit.io)")

if __name__ == "__main__":
    main()
