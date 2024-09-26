import pandas as pd

# Definir la relación de los kits y los productos que contienen
kits_contenido = {
    'CST-007AA': ['CT-011U', 'DT-123V'],
    'CST-008AA': ['CTX-145', 'DTX-199'],
    'CST-009AA': ['CTX-166', 'DTX-197'],
    'CST-011A': ['CTX-088', 'DT-124V'],
    'CST-015AA': ['CTX-064', 'DTX-099'],
    'CST-016AA': ['CTX-064', 'DTX-099L'],
    'CST-018AA': ['CTX-071', 'DT-100V'],
    'CST-019AA': ['CTX-062', 'DT-036'],
    'CST-020AA': ['CTX-062', 'DT-036V'],
    'CST-021AA': ['CTX-151', 'DTX-202'],
    'CST-022AA': ['CTX-123', 'DTX-188'],
    'CST-023AA': ['CTX-174A', 'DTX-237A'],
    'CST-024AA': ['CTX-175A', 'DTX-238A'],
    'CKT-500AU-LB': ['CDX-019A', 'DT-611U'],
    'CKT-501AA-LB': ['CDX-019A', 'DDX-041A'],
    'CKT-506AA-LB': ['CTX-160A', 'DTX-116'],
    'CKT-507AA-LB': ['CTX-160A', 'DTX-209A'],
    'CKT-508AA-LB': ['CTX-170Z', 'DTX-232A'],
    'CKT-512AA-LB': ['CTX-115A', 'DT-628'],
    'CKT-513AA-LB': ['CTX-115A', 'DTX-146'],
    'CKT-500AU-MRK': ['CDX-019A', 'DT-611U', 'TKS44-25K'],
    'CKT-507AA-MRK': ['CTX-160A', 'DTX-209A', 'TKS58-31K'],
    'CKT-507AU-MRK': ['CTX-160A', 'DT-625', 'TKS58-31K'],
    'CKT-508AA-MRK': ['CTX-170Z', 'DTX-232A', 'TKS58-50K'],
    'CKT-510AA-MRK': ['CT-011U', 'DT-123V', 'TKS50-33K'],
    'CKT-511AA-MRK': ['CTX-088', 'DT-124V', 'TKS50-31K']
}

# Leer el archivo CSV con los datos de ventas
archivo_csv = 'ventas.csv'
df = pd.read_csv(archivo_csv)

# Asegurarse de que la columna de fechas está en el formato adecuado
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

# Eliminar las columnas innecesarias
columnas_a_eliminar = ['cia', 'cobrador', 'transacciones', 'nombre_articulo', 'fuente_suministro', 'marca', 'razon_social', 'documento', 'rubro']
df = df.drop(columns=columnas_a_eliminar, errors='ignore')

# Convertir la columna 'articulo' y los códigos de los kits a minúsculas para búsqueda insensible a mayúsculas
df['articulo'] = df['articulo'].str.lower()
codigos_kits = [codigo.lower() for codigo in kits_contenido.keys()]

# Filtrar los códigos que **no pertenecen a kits**
df_no_kits = df[~df['articulo'].isin(codigos_kits)]

# Contar las ocurrencias de los códigos no kits por fecha
conteo_no_kits = df_no_kits.groupby(['fecha', 'articulo']).size().reset_index(name='Cantidad')

# Convertir el código de artículo a mayúsculas
conteo_no_kits['articulo'] = conteo_no_kits['articulo'].str.upper()

# Renombrar las columnas
conteo_no_kits.rename(columns={'articulo': 'Codigo'}, inplace=True)

# Guardar el conteo de códigos no kits en un archivo CSV
conteo_no_kits.to_csv('conteo_no_kits.csv', index=False)

print("Los resultados de los códigos no kits se han guardado en 'conteo_no_kits.csv'")
