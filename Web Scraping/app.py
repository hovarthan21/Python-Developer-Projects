import streamlit as st
from utils import scrape_headings, scrape_content

st.set_page_config(page_title="Web Scraper App", page_icon="🕵️‍♂️", layout="wide")

if 'history' not in st.session_state:
    st.session_state['history'] = []

    
st.title("🕵️‍♂️ Web Scraper App")
st.markdown("Enter a website URL to scrape headings and content.")

tab1, tab2 = st.tabs(["Scrape", "History"])

with tab1:
    url = st.text_input("Enter Website URL:", "")
    if st.button("Scrape Website"):
        if url:
            st.session_state['history'].append(url)

            st.subheader("Headings:")
            headings = scrape_headings(url)
            if headings:
                for h in headings:
                    st.write(h)
            else:
                st.write("No headings found.")

            st.subheader("Content:")
            content = scrape_content(url)
            if content:
                for c in content:
                    st.write(c)
            else:
                st.write("No content found.")
        else:
            st.warning("Please enter a valid URL.")

with tab2:
    st.subheader("📌 Scraping History")
    if st.session_state['history']:
        for i, h_url in enumerate(reversed(st.session_state['history']), start=1):
            st.write(f"{i}. {h_url}")
        
        if st.button("Clear History"):
            st.session_state['history'] = []
            st.success("History cleared!")
    else:
        st.info("No history available.")
