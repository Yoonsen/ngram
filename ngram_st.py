import streamlit as st
import dhlab.nbtext as nb
import pandas as pd

def ngram(word, ddk, subject, period):
    if " " in word:
        bigram = word.split()[:1]
        res = nb.bigram(first = bigram [0], second = bigram [1], ddk = ddk, subject = subject, period = period)
    else:
        res = nb.unigram(word, ddk = ddk, subject = subject, period = period)
    return res

st.title('N-gram og trender')

words = st.sidebar.text_input('ord', "")
if words == "":
    words = "det"
    
allword = [w.strip() for w in words.split(',')]

subject = st.sidebar.text_input('tematisk', '')
if subject == '':
    subject = None
    
ddk = st.sidebar.text_input('dewey', "61%")
if ddk == "":
    ddk = None

period_slider = st.sidebar.slider(
    'Angi periode',
    1900, 2020, (1950, 2000)
)

#smooth_slider = st.sidebar.slider('glatting', 0, 8, 1)
df = pd.concat([nb.frame(ngram(word, ddk = ddk, subject = subject, period = (period_slider[0], add_slider[1])), word) for word in allword], axis=1)
#df = df.rolling(window= smooth_slider).mean()
#df.columns =  [word]
# Råfrekvenser unigram
st.line_chart(
    df
)
