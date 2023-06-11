
import streamlit  as st


st.title("About Me 👽 ")

        
st.write("HEllO if you like this do check out my Socials 👨‍💻 ")

st.write("My name is Dame Rajee")
st.write("I am 18 years old and an AI and ML enthusiast I LOVE SPACE AND PHYSICS AS WELL 🧑‍🚀 ")

st.title("Socials") 

SOCIAL_MEDIA = {
    "Medium ": "https://medium.com/@doss72180 🎃 ",
    "LinkedIn": "https://www.linkedin.com/in/dame-rajee-9b6977231/",
    "GitHub": "https://github.com/dame-cell",
    "Twitter": "https://twitter.com/damerajee44", 
}  

st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

