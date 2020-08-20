import streamlit as st
import dhlab.nbtext as nb
import pandas as pd

st.title('N-gram for alle')

words = st.sidebar.text_input('ord', "")
if words == "":
    words = "det"
    
allword = [w.strip() for w in words.split(',')]
ddk = st.sidebar.text_input('dewey', "61%")
if ddk == "":
    ddk = None

add_slider = st.sidebar.slider(
    'Select a range of values',
    1500, 2020, (1950, 2000)
)

#smooth_slider = st.sidebar.slider('glatting', 0, 8, 1)
df = pd.concat([nb.frame(nb.unigram(word, ddk = ddk, period = (add_slider[0], add_slider[1])), word) for word in allword], axis=1)
#df = df.rolling(window= smooth_slider).mean()
#df.columns =  [word]
# Råfrekvenser unigram
st.line_chart(
    df
)
#df.plot(figsize=(5,3),lw=3, alpha = .7)
#st.pyplot()
#st.write(nb.bigram('meslinger','og').plot())