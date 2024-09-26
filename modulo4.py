import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


def cargar_datos(archivo):
    """Carga los datos desde un archivo CSV"""
    df = pd.read_csv(archivo)
    # Convertir la columna Fecha en un objeto datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df


def preparar_datos(df, producto):
    """Prepara los datos filtrando por producto y resampleando a datos mensuales"""
    # Filtrar los datos por el producto específico
    df_producto = df[df['Producto'] == producto]

    # Resamplear los datos a frecuencia mensual, sumando la frecuencia total diaria
    df_mensual = df_producto.set_index('Fecha').resample('ME').sum()

    return df_mensual['Frecuencia_total']


def entrenar_modelo(serie_temporal):
    """Entrena un modelo ARIMA usando la serie temporal"""
    modelo = ARIMA(serie_temporal, order=(5, 1, 0))
    modelo_entrenado = modelo.fit()
    return modelo_entrenado


def hacer_predicciones(modelo, serie_temporal, pasos=12):
    """Hace predicciones para los próximos 'pasos' meses"""
    predicciones = modelo.forecast(steps=pasos)

    # Crear un rango de fechas para los próximos meses
    ultima_fecha = serie_temporal.index[-1]
    fechas_futuras = pd.date_range(start=ultima_fecha, periods=pasos + 1, freq='M')[1:]

    # Devolver las predicciones con las fechas correspondientes
    predicciones.index = fechas_futuras
    return predicciones


def graficar_predicciones(serie_original, predicciones, producto):
    """Grafica las predicciones junto con la serie original"""
    plt.figure(figsize=(10, 6))
    plt.plot(serie_original, label='Frecuencia Real')
    plt.plot(predicciones.index, predicciones, label='Predicciones', linestyle='--')
    plt.legend()
    plt.title(f"Predicción de Frecuencia Total para {producto}")
    plt.show()


if __name__ == "__main__":
    # Ruta al archivo de datos
    archivo_datos = 'conteo_total_producto_fecha.csv'

    # Cargar los datos
    datos = cargar_datos(archivo_datos)

    # Agrupar por producto y calcular la frecuencia total de cada producto
    top_productos = datos.groupby('Producto')['Frecuencia_total'].sum().nlargest(5).index

    # Iterar sobre los 5 productos con mayor frecuencia total
    for producto in top_productos:
        print(f"\nProducto: {producto}")
        serie_temporal = preparar_datos(datos, producto)

        # Entrenar el modelo ARIMA para este producto
        modelo_entrenado = entrenar_modelo(serie_temporal)

        # Hacer predicciones para los siguientes 12 meses
        predicciones = hacer_predicciones(modelo_entrenado, serie_temporal, pasos=12)

        # Graficar las predicciones
        graficar_predicciones(serie_temporal, predicciones, producto)
