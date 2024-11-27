import pandas as pd
from faker import Faker
import os

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


# Instancia global para su uso en otros módulos
datos_manager = DatosManager()
