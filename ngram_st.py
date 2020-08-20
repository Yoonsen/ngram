import streamlit as st
import dhlab.nbtext as nb
import pandas as pd

@st.cache(suppress_st_warning=True)
def ngram(word, ddk, subject, period):
    if " " in word:
        bigram = word.split()[:2]
        res = nb.bigram(first = bigram [0], second = bigram [1], ddk = ddk, topic = subject, period = period)
    else:
        res = nb.unigram(word, ddk = ddk, topic = subject, period = period)
    return res

@st.cache(suppress_st_warning=True)
def sumword(words, ddk, topic, period):
    wordlist =   [x.strip() for x in words.split(',')]
    ref = pd.concat([nb.unigram(w, ddk = ddk, topic = topic, period = period) for w in wordlist], axis = 1).sum(axis = 1)
    ref.columns = ["tot"]
    return ref

st.title('Bruksutvikling ord og bigram')

words = st.sidebar.text_input('ord', "")
if words == "":
    words = "det"

sammenlign = st.sidebar.text_input("sammenling med summen av følgende ord", ".")
 
allword = [w.strip() for w in words.split(',')]

subject = st.sidebar.text_input('tematisk', '')
if subject == '':
    subject = None
    
ddk = st.sidebar.text_input('dewey', "")
if ddk == "":
    ddk = None
    
if ddk != None and not ddk.endswith("%"):
    ddk = ddk + "%"

period_slider = st.sidebar.slider(
    'Angi periode',
    1900, 2020, (1950, 2000)
)


if sammenlign == "":
    tot = pd.DataFrame()
    tot.columns = ["tot"]
else:
    tot = sumword(sammenlign, ddk, subject, period=(period_slider[0], period_slider[1]))

smooth_slider = st.sidebar.slider('glatting', 0, 8, 3)

df = pd.concat([nb.frame(ngram(word, ddk = ddk, subject = subject, period = (period_slider[0], period_slider[1])), word) for word in allword], axis=1)

df = df.rolling(window= smooth_slider).mean()

# Råfrekvenser unigram
for x in df:
    df[x] = df[x]/tot

st.line_chart(df)

#st.line_chart(tot)