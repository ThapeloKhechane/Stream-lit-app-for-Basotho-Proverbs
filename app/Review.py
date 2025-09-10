import streamlit as st
import json

@st.cache_data
def load_proverbs(json_path):
    """
    Load proverbs from a JSON file.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            proverbs = json.load(file)
        return proverbs
    except FileNotFoundError:
        st.error(f"File not found at {json_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"Invalid JSON file at {json_path}")
        return []

def search_proverbs(proverbs, keyword, search_in_meaning=False):
    """
    Search proverbs for a keyword in Sesotho proverb or optionally in Sesotho meaning.
    """
    keyword = keyword.lower()
    results = []
    for p in proverbs:
        proverb_text = p.get('proverb_sesotho', '').lower()
        meaning_text = p.get('meaning_sesotho', '').lower()
        if keyword in proverb_text or (search_in_meaning and keyword in meaning_text):
            results.append(p)
    return results

def main():
    st.title("Maele (Basotho Proverbs) Search Platform")

    # TODO: Update the path below to your actual JSON file location on your laptop
    json_path = r"C:\Users\Khechane\OneDrive\Desktop\AI-Proverbs-Project\data\proverbs.json"

    proverbs = load_proverbs(json_path)
    if not proverbs:
        st.stop()  # Stop if proverbs can't be loaded

    st.markdown("### Search your Maele by Sesotho keywords")
    keyword = st.text_input("Enter Sesotho keyword (maele):")
    search_in_meaning = st.checkbox("Also search in Sesotho meanings", value=True)

    if keyword:
        matches = search_proverbs(proverbs, keyword, search_in_meaning)
        if matches:
            st.success(f"Found {len(matches)} matching proverbs:")
            for idx, p in enumerate(matches, 1):
                st.markdown(f"### {idx}. {p['proverb_sesotho']}")
                st.write(f"**Tlhaloso (Sesotho Meaning):** {p['meaning_sesotho']}")
                st.write(f"**English Translation:** {p['translation_english']}")
                st.write(f"**English Meaning:** {p['meaning_english']}")
                st.markdown("---")
        else:
            st.warning("No proverbs found matching your search.")
    else:
        st.info("Please enter a keyword to search in the proverbs.")

if __name__ == "__main__":
    main()
