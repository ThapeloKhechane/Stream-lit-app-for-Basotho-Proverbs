import streamlit as st
import json
import random
import os

# Path to your dataset file
JSON_PATH = os.path.join("data", "proverbs.json")

@st.cache_data  # Optional: Cache for performance
def load_proverbs(json_path):
    """
    Load proverbs from a JSON file.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            proverbs = json.load(file)
        return proverbs
    except FileNotFoundError:
        st.error(f"⚠️ File not found at {json_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"⚠️ Invalid JSON file at {json_path}")
        return []

def search_proverbs(proverbs, keyword, search_in_meaning=False):
    keyword = keyword.lower()
    results = []
    for p in proverbs:
        proverb_text = p.get('text', '').lower()
        meaning_text = p.get('meaning', '').lower()
        if keyword in proverb_text or (search_in_meaning and keyword in meaning_text):
            results.append(p)
    return results

def filter_by_category(proverbs, category):
    return [p for p in proverbs if p.get("category", "").lower() == category.lower()]

def display_proverb(proverb, language):
    if language == 'Sesotho':
        st.markdown(f"## {proverb.get('text', '')}")
        st.write(f"**Tlhaloso:** {proverb.get('meaning', 'N/A')}")
    else:  # English
        st.markdown(f"## {proverb.get('translation', 'N/A')}")
        st.write(f"**Meaning:** {proverb.get('meaning', 'N/A')}")

def main():
    st.title("📖 Maele (Basotho Proverbs) Explorer")

    # Load dataset
    proverbs = load_proverbs(JSON_PATH)
    if not proverbs:
        st.stop()

    # Language toggle
    language = st.radio("Choose language:", ("Sesotho", "English"))

    # Sidebar Navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.radio("Choose an option:", ["Search by Keyword", "Filter by Category", "Random Proverb", "Admin Interface"])

    # --- Search by Keyword ---
    if option == "Search by Keyword":
        st.subheader("🔍 Search Proverbs")
        keyword = st.text_input("Enter a Sesotho keyword (e.g., Khomo, Ntja, Tau):")
        search_in_meaning = st.checkbox("Also search in meanings", value=True)

        if keyword:
            matches = search_proverbs(proverbs, keyword, search_in_meaning)
            if matches:
                st.success(f"Found {len(matches)} matching proverbs:")
                for idx, p in enumerate(matches, 1):
                    display_proverb(p, language)
                    st.markdown("---")
            else:
                st.warning("⚠️ No proverbs found matching your search.")
        else:
            st.info("👉 Enter a keyword above to search.")

    # --- Filter by Category ---
    elif option == "Filter by Category":
        st.subheader("📂 Filter by Category")
        categories = sorted(set([p.get("category", "Uncategorized") for p in proverbs]))
        choice = st.selectbox("Select a category:", categories)

        if choice:
            filtered = filter_by_category(proverbs, choice)
            st.success(f"Found {len(filtered)} proverbs in '{choice}':")
            for idx, p in enumerate(filtered, 1):
                display_proverb(p, language)
                st.markdown("---")

    # --- Random Proverb ---
    elif option == "Random Proverb":
        st.subheader("🎲 Random Proverb of the Day")
        proverb = random.choice(proverbs)
        display_proverb(proverb, language)

    # --- Admin Interface ---
    elif option == "Admin Interface":
        st.subheader("Add a New Proverb")
        new_text = st.text_input("Proverb (Sesotho):")
        new_meaning = st.text_input("Meaning (Sesotho):")
        new_translation = st.text_input("Translation (English):")
        new_category = st.text_input("Category:")

        if st.button("Add Proverb"):
            if new_text and new_meaning and new_translation and new_category:
                # Load existing proverbs
                proverbs = load_proverbs(JSON_PATH)

                # Create a new proverb entry
                new_proverb = {
                    "text": new_text,
                    "meaning": new_meaning,
                    "translation": new_translation,
                    "category": new_category
                }

                # Append to the list and save to JSON
                proverbs.append(new_proverb)
                with open(JSON_PATH, 'w', encoding='utf-8') as file:
                    json.dump(proverbs, file, ensure_ascii=False, indent=4)

                st.success("Proverb added successfully!")
            else:
                st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
