from statsmodels.tsa.arima.model import ARIMA
import streamlit as st
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox
from pmdarima import auto_arima
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import json

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def test_stationarity_kpss(data):
    statistic, p_value, n_lags, critical_values = kpss(data)
    result = f'KPSS Statistic: {statistic}\n'
    result += f'p-value: {p_value}\n'
    result += f'num lags: {n_lags}\n'
    result += 'Critial Values:\n'
    for key, value in critical_values.items():
        result += f'   {key} : {value}\n'
    result += f'Result: The series is {"not " if p_value < 0.05 else ""}stationary'
    return result, p_value

def test_stationarity_adfuller(data):
    result = adfuller(data)
    result_str = f'ADF Statistic: {result[0]}\n'
    result_str += f'n_lags: {result[2]}\n'
    result_str += f'p-value: {result[1]}\n'
    result_str += 'Critial Values:\n'
    for key, value in result[4].items():
        result_str += f'   {key}: {value}\n'
    
    if result[1] < 0.05:
        result_str += "Data is stationary"
    else:
        result_str += "Data is not stationary"
    
    return result_str, result[1]

def main():
    # Ruta al archivo JSON de Lottie descargado localmente
    lottie_file_path = "./Animation - 1712796979757.json"  # Reemplaza con la ruta a tu archivo JSON descargado
    with open(lottie_file_path, 'r') as f:
        lottie_json = json.load(f)
    
    st_lottie(lottie_json, width='100%', height=300)
    st.title('¡FORT!')
    st.write('Selection of hyperparameters for time series')
    # Define los nombres de los autores y sus enlaces a LinkedIn
    autores = [
        {"nombre": "Mariana Andreína Paredes ", "LinkedIn": "https://www.linkedin.com/in/marianaandreinaparedesmena/"},
        {"nombre": "Yosmely Bermúdez", "LinkedIn": "https://www.linkedin.com/in/yosmely-bermudez/"}
    ]

    # Título para la sección de autores
    st.title("Authors")

    # Renderiza cada autor con un enlace a LinkedIn
    for autor in autores:
        st.markdown(f"[{autor['nombre']}]({autor['LinkedIn']})")
    # Cargar el contenido del archivo JSON
    st.write('Remember that your file must be a CSV with the date variable and the column to use for analysis.')
        # Widget para cargar un archivo CSV
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully.")
        
        df = load_data(uploaded_file)
        
        st.subheader("Table")
        st.write(df)
        
        fecha_columna = None
        
        # Inspeccionar las columnas del DataFrame
        st.write("Columnas del DataFrame cargado:")
        st.write(df.columns)
        
        # Verificar explícitamente si alguna columna es una columna de fecha
        for columna in df.columns:
            if df[columna].dtype == 'datetime64[ns]':
                fecha_columna = columna
                break
        
        if fecha_columna:
            st.write(f"Se encontró la columna de fecha: '{fecha_columna}'")
            
            result = df.set_index(fecha_columna).copy()
            st.write(f"Se estableció '{fecha_columna}' como el índice del nuevo DataFrame.")
            
            num_lags = st.number_input("Numbers of Lags para PACF y ACF:", min_value=1, max_value=50, value=10)
            
            if result is not None:
                serie = result.iloc[:, 0]  # Seleccionar una columna para el análisis de series temporales
                
                st.subheader(f"Partial Autocorrelation Plot (PACF) with {num_lags} Lags")
                fig_pacf, ax_pacf = plt.subplots()
                plot_pacf(serie, lags=num_lags, ax=ax_pacf)
                st.pyplot(fig_pacf)
                
                st.subheader(f"Autocorrelation Plot (ACF) with {num_lags} Lags")
                fig_acf, ax_acf = plt.subplots()
                plot_acf(serie, lags=num_lags, ax=ax_acf)
                st.pyplot(fig_acf)
                
                # Ejemplo de prueba de estacionariedad
                st.subheader("Initial Stationarity Tests")
                
                # Prueba de estacionariedad ADF
                adf_result = adfuller(serie)
                st.write(f"ADF Statistic: {adf_result[0]}")
                st.write(f"p-value: {adf_result[1]}")
                if adf_result[1] < 0.05:
                    st.write("Data is stationary according to ADF test.")
                else:
                    st.write("Data is not stationary according to ADF test.")
                    
                # Prueba de estacionariedad KPSS
                kpss_result = kpss(serie)
                st.write(f"KPSS Statistic: {kpss_result[0]}")
                st.write(f"p-value: {kpss_result[1]}")
                if kpss_result[1] < 0.05:
                    st.write("Data is not stationary according to KPSS test.")
                else:
                    st.write("Data is stationary according to KPSS test.")
                    
        else:
            st.write("No se encontró ninguna columna de fecha en el DataFrame cargado.")


            # Widget para seleccionar el valor de m
            m = st.selectbox("Select the value of m:", [1, 7, 30, 365])

            # Ejecutar auto_arima para sugerir los mejores hiperparámetros
            model = auto_arima(df, seasonal=True, m=m, trace=True)

            # Mostrar los hiperparámetros seleccionados por auto_arima
            st.subheader("Best hyperparameters suggested by auto_arima: ")
            st.write(f"Best ARIMA parameters: {model.order}")
            st.write(f"Best seasonal parameters: {model.seasonal_order}")

            # Widget para seleccionar los parámetros p, d, q del modelo ARIMA
            st.subheader("ARIMA Model Configuration")
            p = st.slider("p (Auto-regression order)", min_value=0, max_value=8, value=1)
            d = st.slider("d (Order of Differentiation)", min_value=0, max_value=8, value=1)
            q = st.slider("q (Moving Average Order)", min_value=0, max_value=8, value=1)

            # Crear y ajustar el modelo ARIMA con los parámetros seleccionados
            st.write(f"Training ARIMA model with p={p}, d={d}, q={q}...")
            model_arima = sm.tsa.ARIMA(df, order=(p, d, q))
            model_fit = model_arima.fit()

            # Mostrar el resumen del modelo ajustado
            st.subheader("Summary of the Adjusted ARIMA Model")
            st.text(model_fit.summary())

            # Verificar el valor de lb_pvalue para los residuos del modelo
            lb_test_result = sm.stats.acorr_ljungbox(model_fit.resid, lags=[num_lags], return_df=True)
            lb_pvalue = lb_test_result.loc[10, 'lb_pvalue']
            st.write(f"lb_pvalue value for residuals (lag={num_lags}): {lb_pvalue}")
            if lb_pvalue > 0.05:
                st.write("The residuals from the ARIMA model follow a significant pattern.")
            else:
                st.write("The residuals from the ARIMA model don't follow a significant pattern.")
if __name__ == '__main__':
    main()
