import streamlit as st
import dhlab.nbtext as nb
import pandas as pd
from PIL import Image

@st.cache(suppress_st_warning=True, show_spinner = False)
def ngram(word, ddk, subject, period):
    if " " in word:
        bigram = word.split()[:2]
        res = nb.bigram(first = bigram [0], second = bigram [1], ddk = ddk, topic = subject, period = period)
    else:
        res = nb.unigram(word, ddk = ddk, topic = subject, period = period)
    return res

@st.cache(suppress_st_warning=True, show_spinner = False)
def sumword(words, ddk, topic, period):
    wordlist =   [x.strip() for x in words.split(',')]
    # check if trailing comma, or comma in succession, if so count comma in
    if '' in wordlist:
        wordlist = [','] + [y for y in wordlist if y != '']
    ref = pd.concat([nb.unigram(w, ddk = ddk, topic = topic, period = period) for w in wordlist], axis = 1).sum(axis = 1)
    ref.columns = ["tot"]
    return ref



image = Image.open('NB-logo-no-eng-svart.png')
st.sidebar.image(image, width = 200)
st.sidebar.markdown('Se mer om å drive analytisk DH på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb), og korpusanalyse via web [her](https://beta.nb.no/korpus/)')


st.sidebar.title('Ord og bigram')

st.markdown('### Trendlinjer')

st.sidebar.header('Input')
words = st.sidebar.text_input('Fyll inn ord eller bigram adskilt med komma. Det skilles mellom store og små bokstaver', "")
if words == "":
    words = "det"

sammenlign = st.sidebar.text_input("Sammenling med summen av følgende ord - sum av komma og punktum er standard, som gir tilnærmet 10nde-del av inputordenes relativfrekvens", ".,")
 
allword = [w.strip() for w in words.split(',')][:30]

st.sidebar.header('Parametre fra metadata')
st.sidebar.subheader('Dewey')
st.sidebar.markdown("Se definisjoner av Deweys desimalkode [her](https://deweysearchno.pansoft.de/webdeweysearch/index.html)")
ddk = st.sidebar.text_input('Dewey desimalkode - skriv bare de første sifrene for eksempel 8 for alle nummer som starter med 8 som gir treff på all kodet skjønnlitteratur, se lenke til webdewey ovenfor for mulige desimalkoder', "")
if ddk == "":
    ddk = None

if ddk != None and not ddk.endswith("%"):
    ddk = ddk + "%"
st.sidebar.subheader('Temaord')
subject = st.sidebar.text_input('Temaord fra Nasjonalbibliografien - Marc21 felt 655 (stor forbokstav) eller felt 653 (liten forbokstav) - merk forskjell på urfolk og Urfolk', '')
if subject == '':
    subject = None
    
st.sidebar.subheader('Tidsperiode')
period_slider = st.sidebar.slider(
    'Angi periode - år mellom 1900 og 2014',
    1900, 2020, (1950, 2000)
)

# wrapper for nb.frame() check if dataframe is empty before assigning names to columns
def frm(x, y):
    if not x.empty:
        res = nb.frame(x, y)
    else:
        res = x
    return res

st.sidebar.header('Visning')
smooth_slider = st.sidebar.slider('Glatting', 0, 8, 3)

df = pd.concat([frm(ngram(word, ddk = ddk, subject = subject, period = (period_slider[0], period_slider[1])), word) for word in allword], axis=1)



# Råfrekvenser unigram
if sammenlign != "":
    tot = sumword(sammenlign, ddk, subject, period=(period_slider[0], period_slider[1]))
    for x in df:
        df[x] = df[x]/tot

df = df.rolling(window= smooth_slider).mean()
df.index = pd.to_datetime(df.index, format='%Y')
st.line_chart(df)

#st.line_chart(tot)