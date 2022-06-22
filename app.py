
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px




#Muestra el titulo 
st.title ("análisis de sentimiento de tweet sobre aerolíneas Estadounidenses")
# Muestra un titulo en la barra lateral
st.sidebar.title("análisis de sentimiento de tweet sobre aerolíneas Estadounidenses")
#subtitulo en el panel
st.markdown ("dashboard")
#subtitulo en la barra lateral
st.sidebar.markdown("análisis de sentimiento de tweet sobre aerolíneas Estadounidenses")

#Funcion que permite leer la base de datos.
def load_data():
    data = pd.read_csv("data/Tweets.csv", encoding="UTF-8")
    #Convertir argumento a fecha y hora.
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

#Método a utilizar para rellenar huecos en serie
data = data.fillna(method='ffill')
#muestra un subtitulo en la barra antes del radio button
st.sidebar.subheader("show random tweet")
#Crea el radio button
random_tweet = st.sidebar.radio('sentimiento', ('positive','neutral','negative'))
#este permite tomar una tweet aleatorio elegido en el radio button
st.sidebar.markdown(data.query('airline_sentiment  == @random_tweet')[["text"]].sample(n=1).iat[0,0])
#subtitulo en la barra lateral
st.sidebar.markdown('### Numbero de tweets por sentimiento')
#este muestra los graficos que puede seleccionar
select = st.sidebar.selectbox('visualizacion tipo', ['Histograma','Grafica circular','Grafica de lineas' ], key='1')

#contabiliza los tweets por sentimiento
sentiment_count = data['airline_sentiment'].value_counts()
#muestra el sentimiento y contador total
st.write(sentiment_count)
#Permite evaluar lo sentimientos y la cantidad de tweets
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets':sentiment_count.values})

#Este metodo permite elegir entre tres diferentes opciones de graficos (Histograma, Grafica de lineas y pie)
if st.sidebar.checkbox("Hide", True):
    st.markdown("### Numeros of tweets by sentiment")
    if select == "Histograma":
        fig = px.bar(sentiment_count, x= 'Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
        
    elif select == 'Grafica de lineas':
        fig = px.line(sentiment_count, x='Sentiment', y='Tweets')
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Tweets', names = 'Sentiment')
        st.plotly_chart(fig)
#Este pone un subitulo en la barra lateral
st.sidebar.subheader("Cuando y donde los usuarios tweetiaron?")
#Muestra las horas en una barra lateral
hour = st.sidebar.slider("Hour of day", 0, 23)
#modifica el mapa dependiendo la hora
modified_data=data[data['tweet_created'].dt.hour == hour]

#Permite cerrar la visualizacion
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("### Locacion de los tweet basado en el tiempo y dia")
    st.markdown("%i tweets entre %i:00 y %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Mostar data", False):
        st.write(modified_data)

st.sidebar.subheader("Desglose de tweets por sentimiento")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key=0)

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x= 'airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
    facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)


