import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy import stats
# Cargar los datos (ajusta la ruta si es necesario)
# Si tienes problemas con la ruta, prueba con una ruta relativa desde tu proyecto
# o utiliza la función os.path.abspath() para obtener la ruta absoluta

# with open('./data/diagnosis_data.json') as json_data:
    # data = json.load(json_data)
    # df = pd.DataFrame(data['recordSet'])
    # df['field']
    
df = pd.read_csv("data.csv")

# df = pd.read_json("./data/diagnosis_data.json")["recordSet"]["field"]

print(df , "aqui va la vaina")
# Visualizar las primeras filas para verificar la carga
print(df.head() , "df.headsss")
#Exploracion inicial
# Información general sobre el DataFrame
# print(df.info())
# Estadísticas descriptivas
# print(df.describe())
# Frecuencia de géneros

df.rename(columns={'GENDER_FACTOR': 'FACTOR_GENERO'}, inplace=True)
df.rename(columns={'ETHNICITY_FACTOR': 'FACTOR_RAZA'}, inplace=True)
df.rename(columns={'AGE_START_YEARS': 'EDAD_INICIO_AÑOS'}, inplace=True)
df.rename(columns={'AGE_END_YEARS': 'EDAD_FINAL_AÑOS'}, inplace=True)
df.rename(columns={'SHELLFISH_ALG_START': 'COMIENZO_ALG_MARISCOS'}, inplace=True)
df.rename(columns={'GENDER_FACTOR': 'FACTOR_GENERO'}, inplace=True)
df.rename(columns={'GENDER_FACTOR': 'FACTOR_GENERO'}, inplace=True)

print(df['FACTOR_GENERO'].value_counts() , ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<AQUI")
# Histograma de la edad al inicio del estudio
plt.hist(df['EDAD_INICIO_AÑOS'], bins=20)
plt.xlabel('Edad al inicio (años)')
plt.ylabel('Frecuencia')
plt.title('Distribución de la Edad al Inicio del Estudio')
plt.show()
#Limpieza de datos:
# Identificar columnas con valores faltantes
print(df.isnull().sum())

# Rellenar valores faltantes (ejemplo: con la media)
df['EDAD_INICIO_AÑOS'].fillna(df['EDAD_INICIO_AÑOS'].mean(), inplace=True)
# Identificar outliers usando diagramas de caja
sns.boxplot(x=df['EDAD_INICIO_AÑOS'])
plt.show()
# Eliminar outliers (si es necesario)
Q1 = df['EDAD_INICIO_AÑOS'].quantile(0.25)
Q3 = df['EDAD_INICIO_AÑOS'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['EDAD_INICIO_AÑOS'] < (Q1 - 1.5 * IQR)) | (df['EDAD_INICIO_AÑOS'] > (Q3 + 1.5 * IQR)))]
#Analisis exploratorio avanzado
#Correlaciones
# Matriz de correlación para variables numéricas
corr_matrix = df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True)
plt.show()
#Tablas de Contingencia
# Tabla de contingencia para género y tipo de alergia
pd.crosstab(df['FACTOR_GENERO'], df['COMIENZO_ALG_MARISCOS'])
# Estadísticas descriptivas para variables numéricas
numerical_stats = df.describe().T[['mean', '50%', 'std', 'min', 'max']]
numerical_stats.rename(columns={'50%': 'mediana'}, inplace=True)
print(numerical_stats)
# Frecuencias para variables categóricas
categorical_columns = df.select_dtypes(include=['object']).columns

for col in categorical_columns:
    print(f"Frecuencia de {col}:")
    print(df[col].value_counts())
    print("\n")
# Histograma de la edad al inicio del estudio
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(df['EDAD_INICIO_AÑOS'], bins=20, color='skyblue')
plt.xlabel('Edad al inicio (años)')
plt.ylabel('Frecuencia')
plt.title('Distribución de la Edad al Inicio del Estudio')

# Histograma de la edad al final del estudio (suponiendo que hay una columna 'EDAD_FINAL_AÑOS')
plt.subplot(1, 2, 2)
plt.hist(df['EDAD_FINAL_AÑOS'], bins=20, color='salmon')
plt.xlabel('Edad al final (años)')
plt.ylabel('Frecuencia')
plt.title('Distribución de la Edad al Final del Estudio')

plt.tight_layout()
plt.show()
# Gráfico de barras para prevalencia de alergias por género
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='COMIENZO_ALG_MARISCOS', hue='FACTOR_GENERO')
plt.title('Prevalencia de Alergias por Género')
plt.xlabel('Tipo de Alergia')
plt.ylabel('Frecuencia')
plt.legend(title='Género')
plt.show()

# Gráfico de barras para prevalencia de alergias por raza (ajustar según la columna correspondiente)
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='COMIENZO_ALG_MARISCOS', hue='FACTOR_RAZA')
plt.title('Prevalencia de Alergias por Raza')
plt.xlabel('Tipo de Alergia')
plt.ylabel('Frecuencia')
plt.legend(title='Raza')
plt.show()
# Tabla de contingencia para género y tipo de alergia
contingency_table = pd.crosstab(df['FACTOR_GENERO'], df['COMIENZO_ALG_MARISCOS'])
print(contingency_table)

# Prueba chi-cuadrado
chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"Chi2 Stat: {chi2_stat}, P-Value: {p_value}")
# Edad promedio al inicio del diagnóstico por tipo de alergia
average_age_by_allergy = df.groupby('COMIENZO_ALG_MARISCOS')['EDAD_INICIO_AÑOS'].mean()
print(average_age_by_allergy)

# Visualizar la relación entre edad y tipo de alergia
sns.boxplot(data=df, x='COMIENZO_ALG_MARISCOS', y='EDAD_INICIO_AÑOS')
plt.title('Edad al Inicio del Diagnóstico por Tipo de Alergia')
plt.xlabel('Tipo de Alergia')
plt.ylabel('Edad al Inicio (años)')
plt.xticks(rotation=45)
plt.show()
# Proporción de hombres y mujeres con cada tipo de alergia
proportion_gender_allergy = df.groupby(['FACTOR_GENERO', 'COMIENZO_ALG_MARISCOS']).size().unstack()
print(proportion_gender_allergy)

# Gráfico de barras para proporciones
proportion_gender_allergy.plot(kind='bar', stacked=True)
plt.title('Proporción de Género por Tipo de Alergia')
plt.xlabel('Tipo de Alergia')
plt.ylabel('Número de Casos')
plt.legend(title='Género')
plt.show()
# Prueba chi-cuadrado para evaluar asociación entre género y tipo de alergia
chi2_stat_gender, p_value_gender, dof_gender, expected_gender = stats.chi2_contingency(proportion_gender_allergy)
print(f"Chi2 Stat (Género vs Tipo de Alergia): {chi2_stat_gender}, P-Value: {p_value_gender}")
# Supongamos que tenemos columnas como 'EXPOSICION_MASCOTAS', 'HISTORIAL_FAMILIAR' etc.
df['EXPOSICION_MASCOTAS'] = df['EXPOSICION_MASCOTAS'].map({'Sí': 1, 'No': 0})
df['HISTORIAL_FAMILIAR'] = df['HISTORIAL_FAMILIAR'].map({'Sí': 1, 'No': 0})

# Regresión logística para modelar la probabilidad de desarrollar una alergia
import statsmodels.api as sm

X = df[['EDAD_INICIO_AÑOS', 'EXPOSICION_MASCOTAS', 'HISTORIAL_FAMILIAR']]
y = df['COMIENZO_ALG_MARISCOS'].map({'Sí': 1, 'No': 0})  # Ajustar según el tipo

X = sm.add_constant(X)  # Añadir constante

model = sm.Logit(y, X).fit()
print(model.summary())
# Supongamos que tenemos columnas 'TRATAMIENTO_INICIAL' y 'ESTADO_AL_FINAL'
treatment_effectiveness = df.groupby('TRATAMIENTO_INICIAL')['ESTADO_AL_FINAL'].value_counts(normalize=True).unstack()
print(treatment_effectiveness)

# Gráfico para visualizar la efectividad del tratamiento
treatment_effectiveness.plot(kind='bar', stacked=True)
plt.title('Efectividad del Tratamiento')
plt.xlabel('Tratamiento Inicial')
plt.ylabel('Proporción')
plt.legend(title='Estado al Final')
plt.show()

