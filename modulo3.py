import pandas as pd

# Cargar los CSV con los datos
archivo_kits = 'resultados_kit_con_fecha.csv'  # Campo 2: Producto, Campo 3: Cantidad, Campo 4: Fecha
archivo_no_kits = 'conteo_no_kits.csv'         # Campo 1: fecha, Campo 2: Codigo, Campo 3: Cantidad

# Leer los archivos CSV
df_kits = pd.read_csv(archivo_kits)
df_no_kits = pd.read_csv(archivo_no_kits)

# Asegurarse de que las fechas estén en formato datetime
df_kits['Fecha'] = pd.to_datetime(df_kits['Fecha'])  # 'Fecha' mayúscula en df_kits
df_no_kits['fecha'] = pd.to_datetime(df_no_kits['fecha'])  # 'fecha' minúscula en df_no_kits

# Renombrar las columnas para estandarizar
df_kits = df_kits.rename(columns={'Producto': 'Producto', 'Cantidad': 'Frecuencia_kit', 'Fecha': 'Fecha'})
df_no_kits = df_no_kits.rename(columns={'Codigo': 'Producto', 'Cantidad': 'Frecuencia_no_kits', 'fecha': 'Fecha'})  # 'fecha' minúscula renombrada a 'Fecha'

# Agrupar por 'Producto' y 'Fecha' en ambos DataFrames para sumar las cantidades por fecha
df_kits_grouped = df_kits.groupby(['Producto', 'Fecha']).agg({'Frecuencia_kit': 'sum'}).reset_index()
df_no_kits_grouped = df_no_kits.groupby(['Producto', 'Fecha']).agg({'Frecuencia_no_kits': 'sum'}).reset_index()

# Realizar un merge entre ambos DataFrames por 'Producto' y 'Fecha'
df_merged = pd.merge(df_kits_grouped, df_no_kits_grouped, on=['Producto', 'Fecha'], how='outer')

# Sumar las frecuencias de ambos conjuntos de datos, rellenando NaN con 0
df_merged['Frecuencia_total'] = df_merged['Frecuencia_kit'].fillna(0) + df_merged['Frecuencia_no_kits'].fillna(0)

# Seleccionar las columnas relevantes
df_final = df_merged[['Producto', 'Fecha', 'Frecuencia_total']]

# Guardar el resultado en un nuevo archivo CSV
df_final.to_csv('conteo_total_producto_fecha.csv', index=False)

print("El archivo combinado con las frecuencias totales por producto y fecha se ha guardado en 'conteo_total_producto_fecha.csv'")
