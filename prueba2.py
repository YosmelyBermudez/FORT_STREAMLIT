import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random
import time

# Colores aleatorios para cada letra
colors = ["red", "blue", "green", "orange", "purple", "pink", "yellow"]
def animated_text(text):
    # Generar un color aleatorio para cada letra del texto
    colored_text = ""
    for char in text:
        color = random.choice(colors)
        colored_text += f'<span style="color:{color};">{char}</span>'
    return colored_text

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def main():
    st.title("¡FORT!")
    st.write("Selección de Hiperparametros para el Modelo Predictivo ARIMA-SARIMA")

    text = "FORT"  # Texto que deseas animar

    # Mostrar texto animado en la aplicación
    for _ in range(3):  # Repetir la animación 5 veces
        st.markdown(f"<h1 style='text-align:center;'>{animated_text(text)}</h1>", unsafe_allow_html=True)
        time.sleep(0.5)  # Esperar medio segundo entre cada animación
    st.title('Visualización de Autocorrelación')
    st.write("Recuerde que para la serie de tiempo debe cargar un dataframe cuyo INDEX sea las fechas y la columna sea la variable a medir.")

    uploaded_file = st.file_uploader("Cargar archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        st.write("Archivo cargado con éxito.")

        df = load_data(uploaded_file)

        st.subheader("Datos del DataFrame")
        st.write(df)

        # Widget para ingresar el número de lags
        num_lags = st.number_input("Número de Lags:", min_value=1, max_value=50, value=10)

        # Visualizar gráfico de autocorrelación parcial (PACF)
        st.subheader(f"Gráfico de Autocorrelación Parcial (PACF) con {num_lags} Lags")
        fig_pacf = sm.graphics.tsa.plot_pacf(df, lags=num_lags)
        st.pyplot(fig_pacf)

        # Visualizar gráfico de autocorrelación (ACF)
        st.subheader(f"Gráfico de Autocorrelación (ACF) con {num_lags} Lags")
        fig_acf = sm.graphics.tsa.plot_acf(df, lags=num_lags)
        st.pyplot(fig_acf)

if __name__ == '__main__':
    main()
