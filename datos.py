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
    
    #aqui

    def rename_columns(self):
        """Renombrar las columnas para mayor claridad."""
        self.df.rename(columns={
            'GENDER_FACTOR': 'FACTOR_GENERO',
            'ETHNICITY_FACTOR': 'FACTOR_RAZA',
            'AGE_START_YEARS': 'EDAD_INICIO_AÑOS',
            'AGE_END_YEARS': 'EDAD_FINAL_AÑOS',
            'SHELLFISH_ALG_START': 'SHELLFISH_alg_start',
            'PAYER_FACTOR': 'medicacion'
        }, inplace=True)

    def display_initial_info(self):
        """Devuelve la información inicial sobre el DataFrame."""
        info = {
            "head": self.df.head(),  # Primeras filas del DataFrame
            "info": self.df.info(),  # Información sobre las columnas
            "describe": self.df.describe()  # Estadísticas descriptivas
        }
        return info

    def plot_histogram_age_start(self):
        """Muestra un histograma de la edad al inicio del estudio."""
        plt.figure(figsize=(8, 6))
        plt.hist(self.df['EDAD_INICIO_AÑOS'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Edad al inicio (años)')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de la Edad al Inicio del Estudio')
        plt.tight_layout()
        plt.show()

    def plot_missing_data(self):
        """Visualiza la distribución de valores faltantes."""
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title('Mapa de Valores Faltantes')
        plt.tight_layout()
        plt.show()

    def plot_correlation_matrix(self):
        """Muestra un gráfico de la matriz de correlaciones."""
        plt.figure(figsize=(12, 8))
        corr_matrix = self.df.corr(numeric_only=True)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, annot_kws={"size": 8}, cbar_kws={"shrink": 0.8})
        plt.title('Matriz de Correlación', fontsize=16)
        plt.tight_layout()
        plt.show()

    def plot_allergy_by_gender(self):
        """Gráfico de barras para prevalencia de alergias por género."""
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x='SHELLFISH_alg_start', hue='FACTOR_GENERO')
        plt.title('Prevalencia de Alergias por Género', fontsize=16)
        plt.xlabel('Tipo de Alergia', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.legend(title='Género', title_fontsize='13', fontsize='11')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def plot_allergy_by_race(self):
        """Gráfico de barras para prevalencia de alergias por raza."""
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x='SHELLFISH_alg_start', hue='FACTOR_RAZA')
        plt.title('Prevalencia de Alergias por Raza', fontsize=16)
        plt.xlabel('Tipo de Alergia', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.legend(title='Raza', title_fontsize='13', fontsize='11')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def plot_age_boxplot_by_allergy(self):
        """Gráfico de caja para la edad al inicio del diagnóstico por tipo de alergia."""
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.df, x='SHELLFISH_alg_start', y='EDAD_INICIO_AÑOS')
        plt.title('Edad al Inicio del Diagnóstico por Tipo de Alergia')
        plt.xlabel('Tipo de Alergia')
        plt.ylabel('Edad al Inicio (años)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_gender_allergy_proportions(self):
        """Proporción de hombres y mujeres con cada tipo de alergia."""
        proportion_gender_allergy = self.df.groupby(['FACTOR_GENERO', 'SHELLFISH_alg_start']).size().unstack()
        proportion_gender_allergy.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Proporción de Género por Tipo de Alergia')
        plt.xlabel('Tipo de Alergia')
        plt.ylabel('Número de Casos')
        plt.legend(title='Género')
        plt.tight_layout()
        plt.show()

    def plot_age_patterns(self):
        """Representa los patrones de edad al inicio y al final del diagnóstico."""
        
        # Verificar si las columnas existen
        if 'EDAD_INICIO_AÑOS' not in self.df.columns or 'EDAD_FINAL_AÑOS' not in self.df.columns:
            print("Las columnas necesarias no están presentes en el DataFrame.")
            return
        
        # Verificar si hay valores nulos en las columnas
        if self.df[['EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS']].isnull().sum().any():
            print("Hay valores nulos en las columnas de edad. Se eliminarán los valores nulos.")
            self.df.dropna(subset=['EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS'], inplace=True)

        # Crear una figura con subgráficos
        plt.figure(figsize=(14, 10))
        
        # Subgráfico 1: Histograma de las edades al inicio
        plt.subplot(2, 2, 1)
        plt.hist(self.df['EDAD_INICIO_AÑOS'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribución de Edad al Inicio del Diagnóstico')
        plt.xlabel('Edad al Inicio (años)')
        plt.ylabel('Frecuencia')
        
        # Subgráfico 2: Histograma de las edades al final
        plt.subplot(2, 2, 2)
        plt.hist(self.df['EDAD_FINAL_AÑOS'], bins=20, color='lightgreen', edgecolor='black')
        plt.title('Distribución de Edad al Final del Diagnóstico')
        plt.xlabel('Edad al Final (años)')
        plt.ylabel('Frecuencia')
        
        # Subgráfico 3: Relación entre Edad al Inicio y Edad al Final
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=self.df, x='EDAD_INICIO_AÑOS', y='EDAD_FINAL_AÑOS', alpha=0.6, color='orange')
        plt.title('Relación entre Edad al Inicio y Edad al Final')
        plt.xlabel('Edad al Inicio (años)')
        plt.ylabel('Edad al Final (años)')
        
        # Subgráfico 4: Boxplot de Edad al Inicio y Edad al Final
        plt.subplot(2, 2, 4)
        sns.boxplot(data=self.df[['EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS']], palette='Set2')
        plt.title('Patrones de Edad al Inicio y al Final')
        plt.xlabel('Categorías de Edad')
        plt.ylabel('Edad (años)')
        
        # Ajustar el espacio entre los subgráficos y mostrar la figura
        plt.tight_layout()
        plt.show()
    
    def funcion123():
        pass 
    
    #aqui

    def plot_age_patterns_by_race(self):
        """Representa los patrones de edad al inicio y al final del diagnóstico por factor de raza."""
        
        # Verificar si las columnas existen
        if 'FACTOR_RAZA' not in self.df.columns or 'EDAD_INICIO_AÑOS' not in self.df.columns or 'EDAD_FINAL_AÑOS' not in self.df.columns:
            print("Las columnas necesarias no están presentes en el DataFrame.")
            return
        
        # Verificar si hay valores nulos en las columnas
        if self.df[['FACTOR_RAZA', 'EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS']].isnull().sum().any():
            print("Hay valores nulos en las columnas. Se eliminarán los valores nulos.")
            self.df.dropna(subset=['FACTOR_RAZA', 'EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS'], inplace=True)

        # Crear una figura con subgráficos
        plt.figure(figsize=(14, 12))
        
        # Subgráfico 1: Histograma de las edades al inicio, por FACTOR_RAZA
        plt.subplot(2, 2, 1)
        sns.boxplot(data=self.df, x='FACTOR_RAZA', y='EDAD_INICIO_AÑOS', palette='Set3')
        plt.title('Distribución de Edad al Inicio del Diagnóstico por Raza')
        plt.xlabel('Factor de Raza')
        plt.ylabel('Edad al Inicio (años)')
        plt.xticks(rotation=45)
        
        # Subgráfico 2: Histograma de las edades al final, por FACTOR_RAZA
        plt.subplot(2, 2, 2)
        sns.boxplot(data=self.df, x='FACTOR_RAZA', y='EDAD_FINAL_AÑOS', palette='Set3')
        plt.title('Distribución de Edad al Final del Diagnóstico por Raza')
        plt.xlabel('Factor de Raza')
        plt.ylabel('Edad al Final (años)')
        plt.xticks(rotation=45)
        
        # Subgráfico 3: Relación entre Edad al Inicio y Edad al Final, por FACTOR_RAZA
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=self.df, x='EDAD_INICIO_AÑOS', y='EDAD_FINAL_AÑOS', hue='FACTOR_RAZA', alpha=0.6, palette='Set1')
        plt.title('Relación entre Edad al Inicio y Edad al Final por Raza')
        plt.xlabel('Edad al Inicio (años)')
        plt.ylabel('Edad al Final (años)')
        
        # Subgráfico 4: Boxplot comparando Edad al Inicio y Edad al Final por FACTOR_RAZA
        plt.subplot(2, 2, 4)
        sns.boxplot(data=self.df[['EDAD_INICIO_AÑOS', 'EDAD_FINAL_AÑOS', 'FACTOR_RAZA']], x='FACTOR_RAZA', y='EDAD_INICIO_AÑOS', hue='FACTOR_RAZA', palette='Set2')
        plt.title('Comparación de Edad al Inicio y al Final por Raza')
        plt.xlabel('Factor de Raza')
        plt.ylabel('Edad (años)')
        plt.xticks(rotation=45)
        
        # Ajustar el espacio entre los subgráficos y mostrar la figura
        plt.tight_layout()
        plt.show()

# Instancia global para su uso en otros módulos
datos_manager = DatosManager()
