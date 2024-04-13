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
    

    uploaded_file = st.file_uploader("Load CSV file", type=['csv'])
    st.write('Remember that your file must be a CSV with the date variable and the column to use for analysis.')
    
    if uploaded_file is not None:
        st.write("File uploaded successfully.")

        df = load_data(uploaded_file)

        st.subheader("Table")
        st.write(df)

        
        # Variable para almacenar el nombre de la columna de fecha (si se encuentra)
        fecha_columna = None
        # Variable para almacenar el nuevo DataFrame con la columna de fecha como índice
        result = None

        # Iterar sobre las columnas del DataFrame
        for columna in df.columns:
            # Verificar si la columna es de tipo fecha
            if pd.api.types.is_datetime64_any_dtype(df[columna]):
                fecha_columna = columna
                break  # Detener la iteración después de encontrar la primera columna de fecha
        
        # Si se encontró una columna de fecha
        if fecha_columna:
            # Crear un nuevo DataFrame con la columna de fecha como índice
            result = df.set_index(fecha_columna).copy()
            print(f"Se estableció '{fecha_columna}' como el índice del nuevo DataFrame.")
        

        # Widget para ingresar el número de lags
        num_lags = st.number_input("Numbers of Lags para PACF y ACF:", min_value=1, max_value=50, value=10)

        # Visualizar gráfico de autocorrelación parcial (PACF)
        st.subheader(f"Partial Autocorrelation Plot (PACF) with {num_lags} Lags")
        fig_pacf, ax_pacf = plt.subplots()
        plot_pacf(result.values, lags=num_lags, ax=ax_pacf)
        st.pyplot(fig_pacf)

        # Visualizar gráfico de autocorrelación (ACF)
        st.subheader(f"Autocorrelation Plot (ACF) with {num_lags} Lags")
        fig_acf, ax_acf = plt.subplots()
        plot_acf(result.values, lags=num_lags, ax=ax_acf)
        st.pyplot(fig_acf)

        # Pruebas de estacionariedad inicial
        st.subheader("Initial Stationarity Tests")

        # Ejecutar prueba KPSS inicial
        st.write("### Initial KPSS Test")
        kpss_result, kpss_p_value = test_stationarity_kpss(result.iloc[:, 0])  # Seleccionar una columna del DataFrame para la prueba
        st.write(kpss_result)

        # Ejecutar prueba ADF inicial
        st.write("### Initial ADF Test")
        adf_result, adf_p_value = test_stationarity_adfuller(result.iloc[:, 0])  # Seleccionar una columna del DataFrame para la prueba
        st.write(adf_result)

        if kpss_p_value < 0.05 or adf_p_value >= 0.05:
            st.subheader("Differential Transformation")

            # Aplicar diferenciación
            diff_df = result.diff().dropna()  # Aplicar diff() y eliminar NaN

            st.subheader("Data Transformed by Differentiation")
            st.write(diff_df)

            # Pruebas de estacionariedad después de la diferenciación
            st.subheader("Stationarity Tests After Differentiation")

            # Ejecutar prueba KPSS después de la diferenciación
            st.write("### KPSS Test After Differentiation")
            kpss_result_diff, kpss_p_value_diff = test_stationarity_kpss(diff_df.iloc[:, 0])
            st.write(kpss_result_diff)

            # Ejecutar prueba ADF después de la diferenciación
            st.write("### ADF Test After Differentiation")
            adf_result_diff, adf_p_value_diff = test_stationarity_adfuller(diff_df.iloc[:, 0])
            st.write(adf_result_diff)

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
