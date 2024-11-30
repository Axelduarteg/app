import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from faker import Faker
fake = Faker()

class DatosManager:
    def __init__(self, ruta_archivo="data.csv"):
        self.ruta_archivo = ruta_archivo
        self.columnas = [
            "SUBJECT_ID","BIRTH_YEAR","GENDER_FACTOR","RACE_FACTOR","ETHNICITY_FACTOR","PAYER_FACTOR",
            "ATOPIC_MARCH_COHORT","AGE_START_YEARS","AGE_END_YEARS","SHELLFISH_ALG_START","SHELLFISH_ALG_END",
            "FISH_ALG_START","FISH_ALG_END","MILK_ALG_START","MILK_ALG_END","SOY_ALG_START","SOY_ALG_END","EGG_ALG_START","EGG_ALG_END","WHEAT_ALG_START",
            "WHEAT_ALG_END","PEANUT_ALG_START","PEANUT_ALG_END","SESAME_ALG_START","SESAME_ALG_END","TREENUT_ALG_START","TREENUT_ALG_END",
            "WALNUT_ALG_START","WALNUT_ALG_END","PECAN_ALG_START","PECAN_ALG_END","PISTACH_ALG_START","PISTACH_ALG_END","ALMOND_ALG_START",
            "ALMOND_ALG_END","BRAZIL_ALG_START","BRAZIL_ALG_END","HAZELNUT_ALG_START","HAZELNUT_ALG_END",
            "CASHEW_ALG_START","CASHEW_ALG_END","ATOPIC_DERM_START","ATOPIC_DERM_END","ALLERGIC_RHINITIS_START","ALLERGIC_RHINITIS_END",
            "ASTHMA_START","ASTHMA_END","FIRST_ASTHMARX","LAST_ASTHMARX","NUM_ASTHMARX"
        ]
        self.df = self._cargar_datos()

    def _cargar_datos(self):
        if os.path.exists(self.ruta_archivo):
            return pd.read_csv(self.ruta_archivo)
        return pd.DataFrame(columns=self.columnas)

    def guardar_datos_csv(self, datos_formulario):
        # Agrega un nuevo registro al archivo CSV
        if self.df.empty:
            datos_formulario["SUBJECT_ID"] = 1
        else:
            datos_formulario["SUBJECT_ID"] = int(self.df["SUBJECT_ID"].max()) + 1

        nuevo_registro = pd.DataFrame([datos_formulario])
        nuevo_registro = nuevo_registro[self.columnas]
        nuevo_registro.to_csv(self.ruta_archivo, mode="a", header=not os.path.exists(self.ruta_archivo), index=False)
        self.df = pd.concat([self.df, nuevo_registro], ignore_index=True)

    def obtener_registros_pagina(self, pagina, tamanio_pagina):
        if self.df.empty:
            return []

        if tamanio_pagina <= 0 or not isinstance(tamanio_pagina, int):
            raise ValueError("El tamaño de página debe ser un entero positivo.")

        inicio = pagina * tamanio_pagina
        fin = inicio + tamanio_pagina

        registros = self.df.iloc[inicio:fin].copy()
        registros["Nombre"] = [fake.first_name() for _ in range(len(registros))]
        registros["Apellido"] = [fake.last_name() for _ in range(len(registros))]
        return registros.to_dict(orient="records")

    def total_registros(self):
        return len(self.df)

    def edad_promedio(self):
        """Representa los patrones de edad al inicio y al final del estudio."""

        # Verificar si las columnas existen en el DataFrame
        if 'AGE_START_YEARS' not in self.df.columns or 'AGE_END_YEARS' not in self.df.columns:
            print("Las columnas 'AGE_START_YEARS' o 'AGE_END_YEARS' no están presentes en el DataFrame.")
            return

        # Eliminar filas con valores nulos en las columnas de edad
        if self.df[['AGE_START_YEARS', 'AGE_END_YEARS']].isnull().sum().any():
            print("Hay valores nulos en las columnas de edad. Se eliminarán los valores nulos.")
            self.df.dropna(subset=['AGE_START_YEARS', 'AGE_END_YEARS'], inplace=True)

        # Crear una figura con subgráficos
        plt.figure(figsize=(14, 10))

        # Subgráfico 1: Histograma de las edades al inicio del estudio
        plt.subplot(2, 2, 1)
        plt.hist(self.df['AGE_START_YEARS'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribución de Edad al Inicio del Estudio')
        plt.xlabel('Edad al Inicio (años)')
        plt.ylabel('Frecuencia')

        # Subgráfico 2: Histograma de las edades al final del estudio
        plt.subplot(2, 2, 2)
        plt.hist(self.df['AGE_END_YEARS'], bins=20, color='lightgreen', edgecolor='black')
        plt.title('Distribución de Edad al Final del Estudio')
        plt.xlabel('Edad al Final (años)')
        plt.ylabel('Frecuencia')

        # Subgráfico 3: Relación entre Edad al Inicio y Edad al Final
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=self.df, x='AGE_START_YEARS', y='AGE_END_YEARS', alpha=0.6, color='orange')
        plt.title('Relación entre Edad al Inicio y Edad al Final del Estudio')
        plt.xlabel('Edad al Inicio (años)')
        plt.ylabel('Edad al Final (años)')

        # Subgráfico 4: Boxplot de Edad al Inicio y Edad al Final
        plt.subplot(2, 2, 4)
        sns.boxplot(data=self.df[['AGE_START_YEARS', 'AGE_END_YEARS']], palette='Set2')
        plt.title('Patrones de Edad al Inicio y al Final del Estudio')
        plt.xlabel('Categorías de Edad')
        plt.ylabel('Edad (años)')

        # Ajustar el espacio entre los subgráficos y mostrar la figura
        plt.tight_layout()
        plt.show()

    def graficar_distribucion_alergias(self):
        alergias = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START"
        ]
        alergias_counts = self.df[alergias].notna().sum()

        plt.figure(figsize=(12, 8))
        alergias_counts.sort_values().plot(kind='barh', color='purple')
        plt.title('Distribución de Tipos de Alergias', fontsize=16)
        plt.xlabel('Cantidad de Casos', fontsize=14)
        plt.ylabel('Tipo de Alergia', fontsize=14)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.show()

    def graficar_mejora_empeoramiento(self):
        columnas = [
            "SHELLFISH_alg_start", "SHELLFISH_ALG_END", 
            "FISH_ALG_START", "FISH_ALG_END", 
            "MILK_ALG_START", "MILK_ALG_END", 
            "SOY_ALG_START", "SOY_ALG_END", 
            "EGG_ALG_START", "EGG_ALG_END", 
            "WHEAT_ALG_START", "WHEAT_ALG_END", 
            "PEANUT_ALG_START", "PEANUT_ALG_END", 
            "SESAME_ALG_START", "SESAME_ALG_END", 
            "TREENUT_ALG_START", "TREENUT_ALG_END", 
            "WALNUT_ALG_START", "WALNUT_ALG_END", 
            "PECAN_ALG_START", "PECAN_ALG_END", 
            "PISTACH_ALG_START", "PISTACH_ALG_END", 
            "ALMOND_ALG_START", "ALMOND_ALG_END", 
            "BRAZIL_ALG_START", "BRAZIL_ALG_END", 
            "HAZELNUT_ALG_START", "HAZELNUT_ALG_END", 
            "CASHEW_ALG_START", "CASHEW_ALG_END"
        ]
        
        mejora = 0
        empeora = 0
        sin_cambio = 0

        # Calcular las métricas
        for i in range(0, len(columnas), 2):
            start_col = columnas[i]
            end_col = columnas[i + 1]
            
            # Filtrar datos no nulos
            datos = self.df[[start_col, end_col]].dropna()
            
            # Contar mejoras, empeoramientos y sin cambios
            mejora += (datos[start_col] > datos[end_col]).sum()
            empeora += (datos[start_col] < datos[end_col]).sum()
            sin_cambio += (datos[start_col] == datos[end_col]).sum()

        # Datos finales para el gráfico
        categorias = ['Mejoró', 'Empeoró', 'Sin Cambio']
        valores = [mejora, empeora, sin_cambio]

        # Graficar
        plt.figure(figsize=(8, 6))
        plt.bar(categorias, valores, color=['green', 'red', 'blue'], alpha=0.7, edgecolor='black')
        plt.title('Mejoras, Empeoramientos y Sin Cambios en las Alergias', fontsize=16)
        plt.ylabel('Cantidad de Pacientes', fontsize=14)
        plt.xlabel('Categorías', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.show()

    def graficar_alergias_por_año_nacimiento(self):
        """Genera un diagrama de barras del número de personas con alergias por año de nacimiento."""
        
        # Definir las columnas de alergias relevantes
        alergias = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START"
        ]
        
        # Crear una nueva columna para contar las alergias por persona
        self.df['ALERGIAS_PRESENTES'] = self.df[alergias].notna().sum(axis=1)
        
        # Filtrar solo las personas que tienen alguna alergia (es decir, al menos 1 alergia)
        df_con_alergias = self.df[self.df['ALERGIAS_PRESENTES'] > 0]

        # Contar el número de personas con alergias por año de nacimiento
        alergias_por_ano = df_con_alergias['BIRTH_YEAR'].value_counts().sort_index()

        # Crear gráfico de barras
        plt.figure(figsize=(12, 6))
        alergias_por_ano.plot(kind='bar', color='skyblue', edgecolor='black')

        # Configuración del gráfico
        plt.title('Número de Personas con Alergias por Año de Nacimiento', fontsize=16)
        plt.xlabel('Año de Nacimiento', fontsize=14)
        plt.ylabel('Número de Personas con Alergias', fontsize=14)
        plt.xticks(rotation=45)  # Rotar los años en el eje X para que se vean bien
        plt.grid(True, linestyle='--', alpha=0.7)

        # Mostrar el gráfico
        plt.tight_layout()
        plt.show()

    def graficar_alergias_vs_payer_factor(self):
        """Compara los casos de alergias con el PAYER_FACTOR (Medicaid vs Non-Medicaid)."""
        
        # Definir las columnas de alergias relevantes
        alergias = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START"
        ]
        
        # Crear una nueva columna para contar las alergias por persona
        self.df['ALERGIAS_PRESENTES'] = self.df[alergias].notna().sum(axis=1)
        
        # Filtrar las personas que tienen al menos una alergia
        df_con_alergias = self.df[self.df['ALERGIAS_PRESENTES'] > 0]

        # Contar el número de personas con alergias agrupadas por PAYER_FACTOR
        casos_alergias = df_con_alergias.groupby('PAYER_FACTOR')['ALERGIAS_PRESENTES'].count()

        # Crear gráfico de barras
        plt.figure(figsize=(8, 6))
        sns.barplot(x=casos_alergias.index, y=casos_alergias.values, palette='viridis')
        
        # Configuración del gráfico
        plt.title('Casos de Personas con Alergias por PAYER_FACTOR (Medicaid vs Non-Medicaid)', fontsize=16)
        plt.xlabel('PAYER_FACTOR (Medicaid vs Non-Medicaid)', fontsize=14)
        plt.ylabel('Número de Personas con Alergias', fontsize=14)
        plt.xticks(rotation=0, fontsize=12)
        plt.tight_layout()
        plt.show()

    def graficar_contingencia_genero_alergias(self):
        """Genera una tabla de contingencia y un gráfico para comparar el género con los tipos de alergias."""

        # Definir las columnas de alergias (modificar si es necesario para que coincidan con tu CSV)
        alergias = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START"
        ]

        # Verificar si la columna 'GENDER_FACTOR' existe en los datos
        if 'GENDER_FACTOR' not in self.df.columns:
            print("La columna 'GENDER_FACTOR' no está presente en el DataFrame.")
            return

        # Derretir el DataFrame para poner las alergias en una sola columna
        df_alergias = self.df.melt(id_vars=['GENDER_FACTOR'], value_vars=alergias, var_name='Tipo_Alergia', value_name='Alergia_Inicio')

        # Eliminar filas con valores nulos (si no se reporta alergia)
        df_alergias = df_alergias.dropna(subset=['Alergia_Inicio'])

        # Crear la tabla de contingencia
        tabla_contingencia = pd.crosstab(df_alergias['GENDER_FACTOR'], df_alergias['Tipo_Alergia'])

        # Graficar la tabla de contingencia como un mapa de calor
        plt.figure(figsize=(12, 8))
        sns.heatmap(tabla_contingencia, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title("Tabla de Contingencia: Género vs Tipos de Alergia")
        plt.ylabel("Género", fontsize=12)
        plt.xlabel("Tipo de Alergia", fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_gender_allergy_proportions(self):
        """Genera un gráfico de barras apiladas para ver la proporción de alergias según género."""
        
        # Definir las columnas de alergias (modificar según las columnas de alergias en tu DataFrame)
        alergias = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START"
        ]
        
        # Verificar si la columna 'GENDER_FACTOR' existe en los datos
        if 'GENDER_FACTOR' not in self.df.columns:
            print("La columna 'GENDER_FACTOR' no está presente en el DataFrame.")
            return
        
        # Derretir el DataFrame para poner las alergias en una sola columna
        df_alergias = self.df.melt(id_vars=['GENDER_FACTOR'], value_vars=alergias, var_name='Tipo_Alergia', value_name='Alergia_Inicio')
        
        # Eliminar filas con valores nulos (si no se reporta alergia)
        df_alergias = df_alergias.dropna(subset=['Alergia_Inicio'])
        
        # Crear la tabla de proporción de género por tipo de alergia
        proportion_gender_allergy = df_alergias.groupby(['GENDER_FACTOR', 'Tipo_Alergia']).size().unstack()

        # Imprimir la tabla de proporciones
        print(proportion_gender_allergy)
        
        # Graficar la proporción de género por tipo de alergia como un gráfico de barras apiladas
        proportion_gender_allergy.plot(kind='bar', stacked=True, figsize=(12, 8))
        
        # Personalización del gráfico
        plt.title('Proporción de Género por Tipo de Alergia', fontsize=16)
        plt.xlabel('Tipo de Alergia', fontsize=14)
        plt.ylabel('Número de Casos', fontsize=14)
        plt.legend(title='Género', title_fontsize='13', fontsize='11')
        plt.tight_layout()
        plt.show()

    def plot_avg_age_by_allergy(self):
        """Representa la edad promedio al inicio del diagnóstico por tipo de alergia."""

        # Definir las columnas relacionadas con las alergias
        allergy_columns = [
            "SHELLFISH_alg_start", "FISH_ALG_START", "MILK_ALG_START", "SOY_ALG_START", 
            "EGG_ALG_START", "WHEAT_ALG_START", "PEANUT_ALG_START", "SESAME_ALG_START",
            "TREENUT_ALG_START", "WALNUT_ALG_START", "PECAN_ALG_START", "PISTACH_ALG_START", 
            "ALMOND_ALG_START", "BRAZIL_ALG_START", "HAZELNUT_ALG_START", "CASHEW_ALG_START",
            "ATOPIC_DERM_START", "ALLERGIC_RHINITIS_START", "ASTHMA_START"
        ]
        
        # Seleccionar las columnas relevantes para alergias
        allergies = self.df.melt(id_vars=['AGE_START_YEARS'], value_vars=allergy_columns, 
                                var_name='Allergy_Type', value_name='Allergy_Start')
        
        # Filtrar las filas donde Allergy_Start no es nulo
        allergies = allergies.dropna(subset=['Allergy_Start'])
        
        # Calcular la edad promedio por tipo de alergia
        average_age_by_allergy = allergies.groupby('Allergy_Type')['AGE_START_YEARS'].mean()

        # Crear el gráfico de barras
        plt.figure(figsize=(12, 6))
        average_age_by_allergy.plot(kind='bar', color='skyblue')
        plt.title('Edad Promedio al Inicio del Diagnóstico por Tipo de Alergia')
        plt.xlabel('Tipo de Alergia')
        plt.ylabel('Edad Promedio al Inicio (años)')
        plt.xticks(rotation=90, ha='right')  # Rotar etiquetas en el eje X para mejorar la legibilidad
        plt.tight_layout()
        plt.show()

# Instancia global para su uso en otros módulos
datos_manager = DatosManager()
