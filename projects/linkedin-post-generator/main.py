import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]

def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()

    with col1:
        selected_tag = st.selectbox("Title", options=fs.get_tags())

    with col2:
        selected_length = st.selectbox("Length", options=LENGTH_OPTIONS)

    with col3:
        selected_language = st.selectbox("Length", options=LANGUAGE_OPTIONS)

    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag)
        st.write(post)


if __name__ == "__main__":
    main()