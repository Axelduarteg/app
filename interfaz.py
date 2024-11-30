import tkinter as tk
import customtkinter as ctk
import pywinstyles
from tkcalendar import DateEntry
from datos import datos_manager
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox


# Configuración de la ventana principal
root = ctk.CTk()
root.geometry("800x600")
root.title("Gestión de Datos")
pywinstyles.apply_style(window=root, style="aero")
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Variables de estado
pagina_actual = tk.IntVar(value=0)
sidebar_visible = tk.BooleanVar(value=True)

# Frame principal
frame_main = ctk.CTkFrame(root)
frame_main.pack(side="right", fill="both", expand=True)

# Frame de la barra lateral
frame_sidebar = ctk.CTkFrame(root, width=200)
frame_sidebar.pack(side="left", fill="y")


# Función para limpiar el frame principal
def limpiar_frame_main():
    for widget in frame_main.winfo_children():
        widget.destroy()


# Función para mostrar los detalles de un registro
def mostrar_detalles_registro(registro_id):
    registro = datos_manager.df.loc[datos_manager.df["SUBJECT_ID"] == registro_id].dropna(axis=1)
    if registro.empty:
        messagebox.showinfo("Información", f"No se encontró información para ID {registro_id}")
        return

    detalles_ventana = ctk.CTkToplevel(root)
    detalles_ventana.title(f"Detalles del Registro {registro_id}")
    detalles_ventana.geometry("400x300")
    pywinstyles.apply_style(window=detalles_ventana, style="aero")

    for columna, valor in registro.iloc[0].items():
        etiqueta = ctk.CTkLabel(detalles_ventana, text=f"{columna}: {valor}")
        etiqueta.pack(pady=5)


# Función para mostrar los registros (paginados)
def mostrar_registros():
    limpiar_frame_main()
    registros = datos_manager.obtener_registros_pagina(pagina_actual.get(), 10)
    for registro in registros:
        btn_registro = ctk.CTkButton(
            frame_main,
            text=f"ID: {registro['SUBJECT_ID']}, Nombre: {registro['Nombre']}, Apellido: {registro['Apellido']}",
            command=lambda id=registro['SUBJECT_ID']: mostrar_detalles_registro(id)
        )
        btn_registro.pack(pady=2)

    frame_botones = ctk.CTkFrame(frame_main)
    frame_botones.pack(side="bottom", fill="x")

    if pagina_actual.get() > 0:
        btn_prev = ctk.CTkButton(frame_botones, text="Anterior", command=pagina_anterior)
        btn_prev.pack(side="left", padx=10)

    total_registros = datos_manager.total_registros()
    if (pagina_actual.get() + 1) * 10 < total_registros:
        btn_next = ctk.CTkButton(frame_botones, text="Siguiente", command=pagina_siguiente)
        btn_next.pack(side="right", padx=10)


def pagina_anterior():
    if pagina_actual.get() > 0:
        pagina_actual.set(pagina_actual.get() - 1)
        mostrar_registros()


def pagina_siguiente():
    pagina_actual.set(pagina_actual.get() + 1)
    mostrar_registros()

def mostrar_formulario():
    limpiar_frame_main()
    lbl_titulo = ctk.CTkLabel(frame_main, text="Formulario", font=("Arial", 20))
    lbl_titulo.pack(pady=10)

    frame_scroll = ctk.CTkScrollableFrame(frame_main, width=600, height=400)
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    entradas = {}

    def agregar_selector(frame, campo, opciones=None, placeholder="", usar_calendario=False, comando=None):
        lbl = ctk.CTkLabel(frame, text=campo)
        lbl.pack()
        if usar_calendario:
            calendario = DateEntry(frame, selectmode="day", date_pattern="yyyy-mm-dd", width=30)
            calendario.pack(pady=5)
            return [lbl, calendario]  # Retorna una lista que contiene la etiqueta y el calendario
        elif opciones:
            var = tk.StringVar(value="No" if "Sí" in opciones and "No" in opciones else opciones[0])
            menu = ctk.CTkOptionMenu(frame, variable=var, values=opciones, command=comando)
            menu.pack(pady=5)
            return [lbl, menu]  # Retorna una lista que contiene la etiqueta y el menú
        else:
            entrada = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entrada.pack(pady=5)
            return [lbl, entrada]  # Retorna una lista que contiene la etiqueta y la entrada

    # Campos del formulario
    entradas["BIRTH_YEAR"] = agregar_selector(frame_scroll, "Año de nacimiento", usar_calendario=True)
    entradas["GENDER_FACTOR"] = agregar_selector(frame_scroll, "Sexo", ["Hombre", "Mujer"])
    entradas["RACE_FACTOR"] = agregar_selector(frame_scroll, "Raza", ["Blanco", "Negro", "Asiático", "Otro", "Desconocido"])
    entradas["ETHNICITY_FACTOR"] = agregar_selector(frame_scroll, "Origen étnico", ["Hispano", "No Hispano"])
    entradas["PAYER_FACTOR"] = agregar_selector(frame_scroll, "Cobertura", ["Sí", "No"])
    entradas["ATOPIC_MARCH_COHORT"] = agregar_selector(frame_scroll, "Cohorte", ["Sí", "No"])
    entradas["AGE_START_YEARS"] = agregar_selector(frame_scroll, "Inicio de las pruebas", usar_calendario=True)
    entradas["AGE_END_YEARS"] = agregar_selector(frame_scroll, "Fin de las pruebas", usar_calendario=True)
    entradas["SHELLFISH_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a los mariscos?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["FISH_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a al pescado?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["MILK_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a la leche?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["SOY_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a la soya?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["EGG_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a los huevos?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["WHEAT_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia al trigo?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["PEANUT_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a los manis?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["SESAME_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia al sésamo?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["TREENUT_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a los frutos secos?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["WALNUT_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a las nueces?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["PECAN_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a las nueces pecaneras?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["PISTACH_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia al pistacho?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["ALMOND_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a las almendras?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["BRAZIL_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a las nueces de brazil?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["HAZELNUT_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a las avellanas?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["CASHEW_ALLERGY"] = agregar_selector(frame_scroll, "¿Presenta alergia a los anacardos?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["ATOPIC_DERM"] = agregar_selector(frame_scroll, "¿Presenta dermatitis atopica?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["ALLERGIC_RHINITIS"] = agregar_selector(frame_scroll, "¿Presenta rinitis alérgica?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())
    entradas["ASTHMA"] = agregar_selector(frame_scroll, "¿Presenta asma?", ["Sí", "No"], comando=lambda _: mostrar_alegia_campos())

    
    # sub-campos
    keys = [
        "SHELLFISH_ALG_START", "SHELLFISH_ALG_END", "SHELLFISH_START_NUM", "SHELLFISH_END_NUM",
        "FISH_ALG_START", "FISH_ALG_END", "FISH_START_NUM", "FISH_END_NUM",
        "MILK_ALG_START", "MILK_ALG_END", "MILK_START_NUM", "MILK_END_NUM",
        "SOY_ALG_START", "SOY_ALG_END", "SOY_START_NUM", "SOY_END_NUM",
        "EGG_ALG_START", "EGG_ALG_END", "EGG_START_NUM", "EGG_END_NUM",
        "WHEAT_ALG_START", "WHEAT_ALG_END", "WHEAT_START_NUM", "WHEAT_END_NUM",
        "PEANUT_ALG_START", "PEANUT_ALG_END", "PEANUT_START_NUM", "PEANUT_END_NUM",
        "SESAME_ALG_START", "SESAME_ALG_END", "SESAME_START_NUM", "SESAME_END_NUM",
        "TREENUT_ALG_START", "TREENUT_ALG_END", "TREENUT_START_NUM", "TREENUT_END_NUM",
        "WALNUT_ALG_START", "WALNUT_ALG_END", "WALNUT_START_NUM", "WALNUT_END_NUM",
        "PECAN_ALG_START", "PECAN_ALG_END", "PECAN_START_NUM", "PECAN_END_NUM",
        "PISTACH_ALG_START", "PISTACH_ALG_END", "PISTACH_START_NUM", "PISTACH_END_NUM",
        "ALMOND_ALG_START", "ALMOND_ALG_END", "ALMOND_START_NUM", "ALMOND_END_NUM",
        "BRAZIL_ALG_START", "BRAZIL_ALG_END", "BRAZIL_START_NUM", "BRAZIL_END_NUM",
        "HAZELNUT_ALG_START", "HAZELNUT_ALG_END", "HAZELNUT_START_NUM", "HAZELNUT_END_NUM",
        "CASHEW_ALG_START", "CASHEW_ALG_END", "CASHEW_START_NUM", "CASHEW_END_NUM",
        "ATOPIC_DERM_START", "ATOPIC_DERM_END", "ATOPIC_DERM_START_NUM", "ATOPIC_DERM_END_NUM",
        "ALLERGIC_RHINITIS_START", "ALLERGIC_RHINITIS_END", "ALLERGIC_RHINITIS_START_NUM", "ALLERGIC_RHINITIS_END_NUM",
        "ASTHMA_START", "ASTHMA_END", "FIRST_ASTHMARX", "LAST_ASTHMARX", "NUM_ASTHMARX","ASTHMA_START_NUM", "ASTHMA_END_NUM"
    ]

    # Asignar None a cada clave en la lista
    for key in keys:
        entradas[key] = None
    
            
    def mostrar_alegia_campos(*args):
        # Para SHELLFISH
        if entradas["SHELLFISH_ALG_START"] is not None:
            entradas["SHELLFISH_ALG_START"][0].pack_forget()
            entradas["SHELLFISH_ALG_START"][1].pack_forget()
            entradas["SHELLFISH_ALG_START_NUM"].pack_forget()
            entradas["SHELLFISH_ALG_END"][0].pack_forget()
            entradas["SHELLFISH_ALG_END"][1].pack_forget()
            entradas["SHELLFISH_ALG_END_NUM"].pack_forget()

            entradas["SHELLFISH_ALG_START"] = None
            entradas["SHELLFISH_ALG_END"] = None
            entradas["SHELLFISH_ALG_START_NUM"] = None
            entradas["SHELLFISH_ALG_END_NUM"] = None

        if entradas["SHELLFISH_ALLERGY"][1].get() == "Sí":
            entradas["SHELLFISH_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a los mariscos al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SHELLFISH_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SHELLFISH_ALG_START_NUM"].pack(pady=5)

            entradas["SHELLFISH_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a los mariscos al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SHELLFISH_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SHELLFISH_ALG_END_NUM"].pack(pady=5)

        # Para FISH
        if entradas["FISH_ALG_START"] is not None:
            entradas["FISH_ALG_START"][0].pack_forget()
            entradas["FISH_ALG_START"][1].pack_forget()
            entradas["FISH_ALG_START_NUM"].pack_forget()
            entradas["FISH_ALG_END"][0].pack_forget()
            entradas["FISH_ALG_END"][1].pack_forget()
            entradas["FISH_ALG_END_NUM"].pack_forget()

            entradas["FISH_ALG_START"] = None
            entradas["FISH_ALG_END"] = None
            entradas["FISH_ALG_START_NUM"] = None
            entradas["FISH_ALG_END_NUM"] = None

        if entradas["FISH_ALLERGY"][1].get() == "Sí":
            entradas["FISH_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia al pescado al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["FISH_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["FISH_ALG_START_NUM"].pack(pady=5)

            entradas["FISH_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia al pescado al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["FISH_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["FISH_ALG_END_NUM"].pack(pady=5)

        # Para MILK
        if entradas["MILK_ALG_START"] is not None:
            entradas["MILK_ALG_START"][0].pack_forget()
            entradas["MILK_ALG_START"][1].pack_forget()
            entradas["MILK_ALG_START_NUM"].pack_forget()
            entradas["MILK_ALG_END"][0].pack_forget()
            entradas["MILK_ALG_END"][1].pack_forget()
            entradas["MILK_ALG_END_NUM"].pack_forget()

            entradas["MILK_ALG_START"] = None
            entradas["MILK_ALG_END"] = None
            entradas["MILK_ALG_START_NUM"] = None
            entradas["MILK_ALG_END_NUM"] = None

        if entradas["MILK_ALLERGY"][1].get() == "Sí":
            entradas["MILK_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a la leche al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["MILK_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["MILK_ALG_START_NUM"].pack(pady=5)

            entradas["MILK_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a la leche al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["MILK_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["MILK_ALG_END_NUM"].pack(pady=5)

        # Para SOY
        if entradas["SOY_ALG_START"] is not None:
            entradas["SOY_ALG_START"][0].pack_forget()
            entradas["SOY_ALG_START"][1].pack_forget()
            entradas["SOY_ALG_START_NUM"].pack_forget()
            entradas["SOY_ALG_END"][0].pack_forget()
            entradas["SOY_ALG_END"][1].pack_forget()
            entradas["SOY_ALG_END_NUM"].pack_forget()

            entradas["SOY_ALG_START"] = None
            entradas["SOY_ALG_END"] = None
            entradas["SOY_ALG_START_NUM"] = None
            entradas["SOY_ALG_END_NUM"] = None

        if entradas["SOY_ALLERGY"][1].get() == "Sí":
            entradas["SOY_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a la soya al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SOY_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SOY_ALG_START_NUM"].pack(pady=5)

            entradas["SOY_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a la soya al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SOY_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SOY_ALG_END_NUM"].pack(pady=5)
        
        # Para EGG
        if entradas["EGG_ALG_START"] is not None:
            entradas["EGG_ALG_START"][0].pack_forget()
            entradas["EGG_ALG_START"][1].pack_forget()
            entradas["EGG_ALG_START_NUM"].pack_forget()
            entradas["EGG_ALG_END"][0].pack_forget()
            entradas["EGG_ALG_END"][1].pack_forget()
            entradas["EGG_ALG_END_NUM"].pack_forget()

            entradas["EGG_ALG_START"] = None
            entradas["EGG_ALG_END"] = None
            entradas["EGG_ALG_START_NUM"] = None
            entradas["EGG_ALG_END_NUM"] = None

        if entradas["EGG_ALLERGY"][1].get() == "Sí":
            entradas["EGG_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a los huevos al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["EGG_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["EGG_ALG_START_NUM"].pack(pady=5)

            entradas["EGG_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a los huevos al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["EGG_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["EGG_ALG_END_NUM"].pack(pady=5)

        # Para WHEAT
        if entradas["WHEAT_ALG_START"] is not None:
            entradas["WHEAT_ALG_START"][0].pack_forget()
            entradas["WHEAT_ALG_START"][1].pack_forget()
            entradas["WHEAT_ALG_START_NUM"].pack_forget()
            entradas["WHEAT_ALG_END"][0].pack_forget()
            entradas["WHEAT_ALG_END"][1].pack_forget()
            entradas["WHEAT_ALG_END_NUM"].pack_forget()

            entradas["WHEAT_ALG_START"] = None
            entradas["WHEAT_ALG_END"] = None
            entradas["WHEAT_ALG_START_NUM"] = None
            entradas["WHEAT_ALG_END_NUM"] = None

        if entradas["WHEAT_ALLERGY"][1].get() == "Sí":
            entradas["WHEAT_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia al trigo al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["WHEAT_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["WHEAT_ALG_START_NUM"].pack(pady=5)

            entradas["WHEAT_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia al trigo al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["WHEAT_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["WHEAT_ALG_END_NUM"].pack(pady=5)
        
        # Para PEANUT
        if entradas["PEANUT_ALG_START"] is not None:
            entradas["PEANUT_ALG_START"][0].pack_forget()
            entradas["PEANUT_ALG_START"][1].pack_forget()
            entradas["PEANUT_ALG_START_NUM"].pack_forget()
            entradas["PEANUT_ALG_END"][0].pack_forget()
            entradas["PEANUT_ALG_END"][1].pack_forget()
            entradas["PEANUT_ALG_END_NUM"].pack_forget()

            entradas["PEANUT_ALG_START"] = None
            entradas["PEANUT_ALG_END"] = None
            entradas["PEANUT_ALG_START_NUM"] = None
            entradas["PEANUT_ALG_END_NUM"] = None

        if entradas["PEANUT_ALLERGY"][1].get() == "Sí":
            entradas["PEANUT_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a los manis al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PEANUT_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PEANUT_ALG_START_NUM"].pack(pady=5)

            entradas["PEANUT_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a los manis al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PEANUT_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PEANUT_ALG_END_NUM"].pack(pady=5)
        
        # Para SESAME
        if entradas["SESAME_ALG_START"] is not None:
            entradas["SESAME_ALG_START"][0].pack_forget()
            entradas["SESAME_ALG_START"][1].pack_forget()
            entradas["SESAME_ALG_START_NUM"].pack_forget()
            entradas["SESAME_ALG_END"][0].pack_forget()
            entradas["SESAME_ALG_END"][1].pack_forget()
            entradas["SESAME_ALG_END_NUM"].pack_forget()

            entradas["SESAME_ALG_START"] = None
            entradas["SESAME_ALG_END"] = None
            entradas["SESAME_ALG_START_NUM"] = None
            entradas["SESAME_ALG_END_NUM"] = None

        if entradas["SESAME_ALLERGY"][1].get() == "Sí":
            entradas["SESAME_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia al sésamo al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SESAME_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SESAME_ALG_START_NUM"].pack(pady=5)

            entradas["SESAME_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia al sésamo al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["SESAME_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["SESAME_ALG_END_NUM"].pack(pady=5)
        
        # Para TREENUT
        if entradas["TREENUT_ALG_START"] is not None:
            entradas["TREENUT_ALG_START"][0].pack_forget()
            entradas["TREENUT_ALG_START"][1].pack_forget()
            entradas["TREENUT_ALG_START_NUM"].pack_forget()
            entradas["TREENUT_ALG_END"][0].pack_forget()
            entradas["TREENUT_ALG_END"][1].pack_forget()
            entradas["TREENUT_ALG_END_NUM"].pack_forget()

            entradas["TREENUT_ALG_START"] = None
            entradas["TREENUT_ALG_END"] = None
            entradas["TREENUT_ALG_START_NUM"] = None
            entradas["TREENUT_ALG_END_NUM"] = None

        if entradas["TREENUT_ALLERGY"][1].get() == "Sí":
            entradas["TREENUT_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a los frutos secos al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["TREENUT_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["TREENUT_ALG_START_NUM"].pack(pady=5)

            entradas["TREENUT_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a los frutos secos al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["TREENUT_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["TREENUT_ALG_END_NUM"].pack(pady=5)
        
        # Para WALNUT
        if entradas["WALNUT_ALG_START"] is not None:
            entradas["WALNUT_ALG_START"][0].pack_forget()
            entradas["WALNUT_ALG_START"][1].pack_forget()
            entradas["WALNUT_ALG_START_NUM"].pack_forget()
            entradas["WALNUT_ALG_END"][0].pack_forget()
            entradas["WALNUT_ALG_END"][1].pack_forget()
            entradas["WALNUT_ALG_END_NUM"].pack_forget()

            entradas["WALNUT_ALG_START"] = None
            entradas["WALNUT_ALG_END"] = None
            entradas["WALNUT_ALG_START_NUM"] = None
            entradas["WALNUT_ALG_END_NUM"] = None

        if entradas["WALNUT_ALLERGY"][1].get() == "Sí":
            entradas["WALNUT_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["WALNUT_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["WALNUT_ALG_START_NUM"].pack(pady=5)

            entradas["WALNUT_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["WALNUT_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["WALNUT_ALG_END_NUM"].pack(pady=5)
        
        # Para PECAN
        if entradas["PECAN_ALG_START"] is not None:
            entradas["PECAN_ALG_START"][0].pack_forget()
            entradas["PECAN_ALG_START"][1].pack_forget()
            entradas["PECAN_ALG_START_NUM"].pack_forget()
            entradas["PECAN_ALG_END"][0].pack_forget()
            entradas["PECAN_ALG_END"][1].pack_forget()
            entradas["PECAN_ALG_END_NUM"].pack_forget()

            entradas["PECAN_ALG_START"] = None
            entradas["PECAN_ALG_END"] = None
            entradas["PECAN_ALG_START_NUM"] = None
            entradas["PECAN_ALG_END_NUM"] = None

        if entradas["PECAN_ALLERGY"][1].get() == "Sí":
            entradas["PECAN_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces pecaneras al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PECAN_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PECAN_ALG_START_NUM"].pack(pady=5)

            entradas["PECAN_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces pecaneras al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PECAN_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PECAN_ALG_END_NUM"].pack(pady=5)
        
        # Para PISTACH
        if entradas["PISTACH_ALG_START"] is not None:
            entradas["PISTACH_ALG_START"][0].pack_forget()
            entradas["PISTACH_ALG_START"][1].pack_forget()
            entradas["PISTACH_ALG_START_NUM"].pack_forget()
            entradas["PISTACH_ALG_END"][0].pack_forget()
            entradas["PISTACH_ALG_END"][1].pack_forget()
            entradas["PISTACH_ALG_END_NUM"].pack_forget()

            entradas["PISTACH_ALG_START"] = None
            entradas["PISTACH_ALG_END"] = None
            entradas["PISTACH_ALG_START_NUM"] = None
            entradas["PISTACH_ALG_END_NUM"] = None

        if entradas["PISTACH_ALLERGY"][1].get() == "Sí":
            entradas["PISTACH_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia al pistacho al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PISTACH_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PISTACH_ALG_START_NUM"].pack(pady=5)

            entradas["PISTACH_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia al pistacho al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["PISTACH_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["PISTACH_ALG_END_NUM"].pack(pady=5)
        
        # Para ALMOND
        if entradas["ALMOND_ALG_START"] is not None:
            entradas["ALMOND_ALG_START"][0].pack_forget()
            entradas["ALMOND_ALG_START"][1].pack_forget()
            entradas["ALMOND_ALG_START_NUM"].pack_forget()
            entradas["ALMOND_ALG_END"][0].pack_forget()
            entradas["ALMOND_ALG_END"][1].pack_forget()
            entradas["ALMOND_ALG_END_NUM"].pack_forget()

            entradas["ALMOND_ALG_START"] = None
            entradas["ALMOND_ALG_END"] = None
            entradas["ALMOND_ALG_START_NUM"] = None
            entradas["ALMOND_ALG_END_NUM"] = None

        if entradas["ALMOND_ALLERGY"][1].get() == "Sí":
            entradas["ALMOND_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a las almendras al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ALMOND_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ALMOND_ALG_START_NUM"].pack(pady=5)

            entradas["ALMOND_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a las almendras al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ALMOND_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ALMOND_ALG_END_NUM"].pack(pady=5)
        
        # Para BRAZIL
        if entradas["BRAZIL_ALG_START"] is not None:
            entradas["BRAZIL_ALG_START"][0].pack_forget()
            entradas["BRAZIL_ALG_START"][1].pack_forget()
            entradas["BRAZIL_ALG_START_NUM"].pack_forget()
            entradas["BRAZIL_ALG_END"][0].pack_forget()
            entradas["BRAZIL_ALG_END"][1].pack_forget()
            entradas["BRAZIL_ALG_END_NUM"].pack_forget()

            entradas["BRAZIL_ALG_START"] = None
            entradas["BRAZIL_ALG_END"] = None
            entradas["BRAZIL_ALG_START_NUM"] = None
            entradas["BRAZIL_ALG_END_NUM"] = None

        if entradas["BRAZIL_ALLERGY"][1].get() == "Sí":
            entradas["BRAZIL_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces de brazil al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["BRAZIL_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["BRAZIL_ALG_START_NUM"].pack(pady=5)

            entradas["BRAZIL_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a las nueces de brazil al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["BRAZIL_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["BRAZIL_ALG_END_NUM"].pack(pady=5)
        
        # Para HAZELNUT
        if entradas["HAZELNUT_ALG_START"] is not None:
            entradas["HAZELNUT_ALG_START"][0].pack_forget()
            entradas["HAZELNUT_ALG_START"][1].pack_forget()
            entradas["HAZELNUT_ALG_START_NUM"].pack_forget()
            entradas["HAZELNUT_ALG_END"][0].pack_forget()
            entradas["HAZELNUT_ALG_END"][1].pack_forget()
            entradas["HAZELNUT_ALG_END_NUM"].pack_forget()

            entradas["HAZELNUT_ALG_START"] = None
            entradas["HAZELNUT_ALG_END"] = None
            entradas["HAZELNUT_ALG_START_NUM"] = None
            entradas["HAZELNUT_ALG_END_NUM"] = None

        if entradas["HAZELNUT_ALLERGY"][1].get() == "Sí":
            entradas["HAZELNUT_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a las avellanas al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["HAZELNUT_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["HAZELNUT_ALG_START_NUM"].pack(pady=5)

            entradas["HAZELNUT_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a las avellanas al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["HAZELNUT_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["HAZELNUT_ALG_END_NUM"].pack(pady=5)
        
        # Para CASHEW
        if entradas["CASHEW_ALG_START"] is not None:
            entradas["CASHEW_ALG_START"][0].pack_forget()
            entradas["CASHEW_ALG_START"][1].pack_forget()
            entradas["CASHEW_ALG_START_NUM"].pack_forget()
            entradas["CASHEW_ALG_END"][0].pack_forget()
            entradas["CASHEW_ALG_END"][1].pack_forget()
            entradas["CASHEW_ALG_END_NUM"].pack_forget()

            entradas["CASHEW_ALG_START"] = None
            entradas["CASHEW_ALG_END"] = None
            entradas["CASHEW_ALG_START_NUM"] = None
            entradas["CASHEW_ALG_END_NUM"] = None

        if entradas["CASHEW_ALLERGY"][1].get() == "Sí":
            entradas["CASHEW_ALG_START"] = agregar_selector(frame_scroll, "Estado de la alergia a los anacardos al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["CASHEW_ALG_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["CASHEW_ALG_START_NUM"].pack(pady=5)

            entradas["CASHEW_ALG_END"] = agregar_selector(frame_scroll, "Estado de la alergia a los anacardos al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["CASHEW_ALG_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["CASHEW_ALG_END_NUM"].pack(pady=5)
        
        # Para DERM
        if entradas["ATOPIC_DERM_START"] is not None:
            entradas["ATOPIC_DERM_START"][0].pack_forget()
            entradas["ATOPIC_DERM_START"][1].pack_forget()
            entradas["ATOPIC_DERM_START_NUM"].pack_forget()
            entradas["ATOPIC_DERM_END"][0].pack_forget()
            entradas["ATOPIC_DERM_END"][1].pack_forget()
            entradas["ATOPIC_DERM_END_NUM"].pack_forget()

            entradas["ATOPIC_DERM_START"] = None
            entradas["ATOPIC_DERM_END"] = None
            entradas["ATOPIC_DERM_START_NUM"] = None
            entradas["ATOPIC_DERM_END_NUM"] = None

        if entradas["ATOPIC_DERM"][1].get() == "Sí":
            entradas["ATOPIC_DERM_START"] = agregar_selector(frame_scroll, "Estado de la dermatitis atopica al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ATOPIC_DERM_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ATOPIC_DERM_START_NUM"].pack(pady=5)

            entradas["ATOPIC_DERM_END"] = agregar_selector(frame_scroll, "Estado de la dermatitis atopica al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ATOPIC_DERM_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ATOPIC_DERM_END_NUM"].pack(pady=5)
        
        # Para DERM
        if entradas["ALLERGIC_RHINITIS_START"] is not None:
            entradas["ALLERGIC_RHINITIS_START"][0].pack_forget()
            entradas["ALLERGIC_RHINITIS_START"][1].pack_forget()
            entradas["ALLERGIC_RHINITIS_START_NUM"].pack_forget()
            entradas["ALLERGIC_RHINITIS_END"][0].pack_forget()
            entradas["ALLERGIC_RHINITIS_END"][1].pack_forget()
            entradas["ALLERGIC_RHINITIS_END_NUM"].pack_forget()

            entradas["ALLERGIC_RHINITIS_START"] = None
            entradas["ALLERGIC_RHINITIS_END"] = None
            entradas["ALLERGIC_RHINITIS_START_NUM"] = None
            entradas["ALLERGIC_RHINITIS_END_NUM"] = None

        if entradas["ALLERGIC_RHINITIS"][1].get() == "Sí":
            entradas["ALLERGIC_RHINITIS_START"] = agregar_selector(frame_scroll, "Estado de la rinitis alérgica al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ALLERGIC_RHINITIS_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ALLERGIC_RHINITIS_START_NUM"].pack(pady=5)

            entradas["ALLERGIC_RHINITIS_END"] = agregar_selector(frame_scroll, "Estado de la rinitis alérgica al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ALLERGIC_RHINITIS_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ALLERGIC_RHINITIS_END_NUM"].pack(pady=5)    
        
        # Para ASTHMA
        if entradas["ASTHMA_START"] is not None:
                    entradas["ASTHMA_START"][0].pack_forget()
                    entradas["ASTHMA_START"][1].pack_forget()
                    entradas["ASTHMA_START_NUM"].pack_forget()
                    entradas["ASTHMA_END"][0].pack_forget()
                    entradas["ASTHMA_END"][1].pack_forget()
                    entradas["ASTHMA_END_NUM"].pack_forget()
                    entradas["FIRST_ASTHMARX"].pack_forget()
                    entradas["LAST_ASTHMARX"].pack_forget()
                    entradas["NUM_ASTHMARX"].pack_forget()

                    entradas["ASTHMA_START"] = None
                    entradas["ASTHMA_END"] = None
                    entradas["ASTHMA_START_NUM"] = None
                    entradas["ASTHMA_END_NUM"] = None
                    entradas["FIRST_ASTHMARX"] = None
                    entradas["LAST_ASTHMARX"] = None
                    entradas["NUM_ASTHMARX"] = None
                    
        if entradas["ASTHMA"][1].get() == "Sí":
            entradas["ASTHMA_START"] = agregar_selector(frame_scroll, "Estado del asma al inicio", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ASTHMA_START_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ASTHMA_START_NUM"].pack(pady=5)

            entradas["ASTHMA_END"] = agregar_selector(frame_scroll, "Estado del asma al final", ["Leve", "Moderada", "Grave", "Intermitente", "Personalizar"])
            entradas["ASTHMA_END_NUM"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número (0-9 o personalizado)")
            entradas["ASTHMA_END_NUM"].pack(pady=5)

            entradas["FIRST_ASTHMARX"] = agregar_selector(frame_scroll, "Primer medicamento para el asma recetado", usar_calendario=True)

            entradas["LAST_ASTHMARX"] = agregar_selector(frame_scroll, "Último medicamento para el asma recetado", usar_calendario=True)

            entradas["NUM_ASTHMARX"] = ctk.CTkEntry(frame_scroll, placeholder_text="Número de medicamentos para el asma recetados")
            entradas["NUM_ASTHMARX"].pack(pady=5)
        
    def guardar():
        # Verificar si la alergia es "Sí" o "No" y ajustar los valores
        # Para SHELLFISH
        SHELLFISH_alg_start = "NA"
        SHELLFISH_alg_end = "NA"
        if entradas["SHELLFISH_ALLERGY"][1].get() == "Sí":
            start_option = entradas["SHELLFISH_ALG_START"][1].get()
            start_num = entradas["SHELLFISH_ALG_START_NUM"].get()

            end_option = entradas["SHELLFISH_ALG_END"][1].get()
            end_num = entradas["SHELLFISH_ALG_END_NUM"].get()

            SHELLFISH_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            SHELLFISH_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num

        # Para FISH
        FISH_alg_start = "NA"
        FISH_alg_end = "NA"
        if entradas["FISH_ALLERGY"][1].get() == "Sí":
            start_option = entradas["FISH_ALG_START"][1].get()
            start_num = entradas["FISH_ALG_START_NUM"].get()

            end_option = entradas["FISH_ALG_END"][1].get()
            end_num = entradas["FISH_ALG_END_NUM"].get()

            FISH_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            FISH_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num

        # Para MILK
        MILK_alg_start = "NA"
        MILK_alg_end = "NA"
        if entradas["MILK_ALLERGY"][1].get() == "Sí":
            start_option = entradas["MILK_ALG_START"][1].get()
            start_num = entradas["MILK_ALG_START_NUM"].get()

            end_option = entradas["MILK_ALG_END"][1].get()
            end_num = entradas["MILK_ALG_END_NUM"].get()

            MILK_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            MILK_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para SOY
        SOY_alg_start = "NA"
        SOY_alg_end = "NA"
        if entradas["SOY_ALLERGY"][1].get() == "Sí":
            start_option = entradas["SOY_ALG_START"][1].get()
            start_num = entradas["SOY_ALG_START_NUM"].get()

            end_option = entradas["SOY_ALG_END"][1].get()
            end_num = entradas["SOY_ALG_END_NUM"].get()

            SOY_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            SOY_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para EGG
        EGG_alg_start = "NA"
        EGG_alg_end = "NA"
        if entradas["EGG_ALLERGY"][1].get() == "Sí":
            start_option = entradas["EGG_ALG_START"][1].get()
            start_num = entradas["EGG_ALG_START_NUM"].get()

            end_option = entradas["EGG_ALG_END"][1].get()
            end_num = entradas["EGG_ALG_END_NUM"].get()

            EGG_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            EGG_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para WHEAT
        WHEAT_alg_start = "NA"
        WHEAT_alg_end = "NA"
        if entradas["WHEAT_ALLERGY"][1].get() == "Sí":
            start_option = entradas["WHEAT_ALG_START"][1].get()
            start_num = entradas["WHEAT_ALG_START_NUM"].get()

            end_option = entradas["WHEAT_ALG_END"][1].get()
            end_num = entradas["WHEAT_ALG_END_NUM"].get()

            WHEAT_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            WHEAT_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para PEANUT
        PEANUT_alg_start = "NA"
        PEANUT_alg_end = "NA"
        if entradas["PEANUT_ALLERGY"][1].get() == "Sí":
            start_option = entradas["PEANUT_ALG_START"][1].get()
            start_num = entradas["PEANUT_ALG_START_NUM"].get()

            end_option = entradas["PEANUT_ALG_END"][1].get()
            end_num = entradas["PEANUT_ALG_END_NUM"].get()

            PEANUT_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            PEANUT_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para SESAME
        SESAME_alg_start = "NA"
        SESAME_alg_end = "NA"
        if entradas["SESAME_ALLERGY"][1].get() == "Sí":
            start_option = entradas["SESAME_ALG_START"][1].get()
            start_num = entradas["SESAME_ALG_START_NUM"].get()

            end_option = entradas["SESAME_ALG_END"][1].get()
            end_num = entradas["SESAME_ALG_END_NUM"].get()

            SESAME_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            SESAME_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para TREENUT
        TREENUT_alg_start = "NA"
        TREENUT_alg_end = "NA"
        if entradas["TREENUT_ALLERGY"][1].get() == "Sí":
            start_option = entradas["TREENUT_ALG_START"][1].get()
            start_num = entradas["TREENUT_ALG_START_NUM"].get()

            end_option = entradas["TREENUT_ALG_END"][1].get()
            end_num = entradas["TREENUT_ALG_END_NUM"].get()

            TREENUT_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            TREENUT_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para WALNUT
        WALNUT_alg_start = "NA"
        WALNUT_alg_end = "NA"
        if entradas["WALNUT_ALLERGY"][1].get() == "Sí":
            start_option = entradas["WALNUT_ALG_START"][1].get()
            start_num = entradas["WALNUT_ALG_START_NUM"].get()

            end_option = entradas["WALNUT_ALG_END"][1].get()
            end_num = entradas["WALNUT_ALG_END_NUM"].get()

            WALNUT_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            WALNUT_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para PECAN
        PECAN_alg_start = "NA"
        PECAN_alg_end = "NA"
        if entradas["PECAN_ALLERGY"][1].get() == "Sí":
            start_option = entradas["PECAN_ALG_START"][1].get()
            start_num = entradas["PECAN_ALG_START_NUM"].get()

            end_option = entradas["PECAN_ALG_END"][1].get()
            end_num = entradas["PECAN_ALG_END_NUM"].get()

            PECAN_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            PECAN_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para PISTACH
        PISTACH_alg_start = "NA"
        PISTACH_alg_end = "NA"
        if entradas["PISTACH_ALLERGY"][1].get() == "Sí":
            start_option = entradas["PISTACH_ALG_START"][1].get()
            start_num = entradas["PISTACH_ALG_START_NUM"].get()

            end_option = entradas["PISTACH_ALG_END"][1].get()
            end_num = entradas["PISTACH_ALG_END_NUM"].get()

            PISTACH_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            PISTACH_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para ALMOND
        ALMOND_alg_start = "NA"
        ALMOND_alg_end = "NA"
        if entradas["ALMOND_ALLERGY"][1].get() == "Sí":
            start_option = entradas["ALMOND_ALG_START"][1].get()
            start_num = entradas["ALMOND_ALG_START_NUM"].get()

            end_option = entradas["ALMOND_ALG_END"][1].get()
            end_num = entradas["ALMOND_ALG_END_NUM"].get()

            ALMOND_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            ALMOND_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para BRAZIL
        BRAZIL_alg_start = "NA"
        BRAZIL_alg_end = "NA"
        if entradas["BRAZIL_ALLERGY"][1].get() == "Sí":
            start_option = entradas["BRAZIL_ALG_START"][1].get()
            start_num = entradas["BRAZIL_ALG_START_NUM"].get()

            end_option = entradas["BRAZIL_ALG_END"][1].get()
            end_num = entradas["BRAZIL_ALG_END_NUM"].get()

            BRAZIL_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            BRAZIL_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para HAZELNUT
        HAZELNUT_alg_start = "NA"
        HAZELNUT_alg_end = "NA"
        if entradas["HAZELNUT_ALLERGY"][1].get() == "Sí":
            start_option = entradas["HAZELNUT_ALG_START"][1].get()
            start_num = entradas["HAZELNUT_ALG_START_NUM"].get()

            end_option = entradas["HAZELNUT_ALG_END"][1].get()
            end_num = entradas["HAZELNUT_ALG_END_NUM"].get()

            HAZELNUT_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            HAZELNUT_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para CASHEW
        CASHEW_alg_start = "NA"
        CASHEW_alg_end = "NA"
        if entradas["CASHEW_ALLERGY"][1].get() == "Sí":
            start_option = entradas["CASHEW_ALG_START"][1].get()
            start_num = entradas["CASHEW_ALG_START_NUM"].get()

            end_option = entradas["CASHEW_ALG_END"][1].get()
            end_num = entradas["CASHEW_ALG_END_NUM"].get()

            CASHEW_alg_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            CASHEW_alg_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para DERM
        ATOPIC_derm_start = "NA"
        ATOPIC_derm_end = "NA"
        if entradas["ATOPIC_DERM"][1].get() == "Sí":
            start_option = entradas["ATOPIC_DERM_START"][1].get()
            start_num = entradas["ATOPIC_DERM_START_NUM"].get()

            end_option = entradas["ATOPIC_DERM_END"][1].get()
            end_num = entradas["ATOPIC_DERM_END_NUM"].get()

            ATOPIC_derm_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            ATOPIC_derm_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para DERM
        ALLERGIC_rhinitis_start = "NA"
        ALLERGIC_rhinitis_end = "NA"
        if entradas["ALLERGIC_RHINITIS"][1].get() == "Sí":
            start_option = entradas["ALLERGIC_RHINITIS_START"][1].get()
            start_num = entradas["ALLERGIC_RHINITIS_START_NUM"].get()

            end_option = entradas["ALLERGIC_RHINITIS_END"][1].get()
            end_num = entradas["ALLERGIC_RHINITIS_END_NUM"].get()

            ALLERGIC_rhinitis_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            ALLERGIC_rhinitis_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num
        
        # Para ASTHMA
        ASTHMA_start = "NA"
        ASTHMA_end = "NA"
        FIRST_asthmarx = "NA"
        LAST_asthmarx = "NA"
        NUM_astmarx = "NA"
        if entradas["ASTHMA"][1].get() == "Sí":
            start_option = entradas["ASTHMA_START"][1].get()
            start_num = entradas["ASTHMA_START_NUM"].get()

            end_option = entradas["ASTHMA_END"][1].get()
            end_num = entradas["ASTHMA_END_NUM"].get()

            ASTHMA_start = f"{['Leve', 'Moderada', 'Grave'].index(start_option)}.{start_num}" if start_option in ['Leve', 'Moderada', 'Grave'] else start_num
            ASTHMA_end = f"{['Leve', 'Moderada', 'Grave'].index(end_option)}.{end_num}" if end_option in ['Leve', 'Moderada', 'Grave'] else end_num

            FIRST_asthmarx = (lambda inicio, primer: (lambda d: d.years + d.months / 12 + d.days / 365)(relativedelta(datetime.strptime(inicio, "%Y-%m-%d"), datetime.strptime(primer, "%Y-%m-%d"))))(
            entradas["AGE_START_YEARS"][1].get(), entradas["FIRST_ASTHMARX"][1].get())

            LAST_asthmarx = (lambda inicio, primer: (lambda d: d.years + d.months / 12 + d.days / 365)(relativedelta(datetime.strptime(inicio, "%Y-%m-%d"), datetime.strptime(primer, "%Y-%m-%d"))))(
            entradas["AGE_START_YEARS"][1].get(), entradas["LAST_ASTHMARX"][1].get())

            NUM_astmarx = entradas["NUM_ASTHMARX"].get()

        # Recopilar datos para guardar en el CSV
        datos_formulario = {
            "BIRTH_YEAR": datetime.strptime(entradas["BIRTH_YEAR"][1].get(), "%Y-%m-%d").year,
            "GENDER_FACTOR": "S0 - Male" if entradas["GENDER_FACTOR"][1].get() == "Hombre" else "S1 - Female",
            "RACE_FACTOR": {"Blanco": "R0 - White", "Negro": "R1 - Black", "Asiático": "R2 - Asian or Pacific Islander", "Otro": "R3 - Other", "Desconocido": "R4 - Unknown"}[entradas["RACE_FACTOR"][1].get()],
            "ETHNICITY_FACTOR": "E1 - Hispanic" if entradas["ETHNICITY_FACTOR"][1].get() == "Hispano" else "E0 - Non-Hispanic",
            "PAYER_FACTOR": "P1 - Medicaid" if entradas["PAYER_FACTOR"][1].get() == "Sí" else "P0 - Non-Medicaid",
            "ATOPIC_MARCH_COHORT": entradas["ATOPIC_MARCH_COHORT"][1].get() == "Sí",
            "AGE_START_YEARS": (lambda nacimiento, inicio: (lambda d: d.years + d.months / 12 + d.days / 365)(relativedelta(datetime.strptime(inicio, "%Y-%m-%d"), datetime.strptime(nacimiento, "%Y-%m-%d"))))(
                entradas["BIRTH_YEAR"][1].get(), entradas["AGE_START_YEARS"][1].get()),
            "AGE_END_YEARS": (lambda nacimiento, fin: (lambda d: d.years + d.months / 12 + d.days / 365)(relativedelta(datetime.strptime(fin, "%Y-%m-%d"), datetime.strptime(nacimiento, "%Y-%m-%d"))))(
                entradas["BIRTH_YEAR"][1].get(), entradas["AGE_END_YEARS"][1].get()),
            "FIRST_ASTHMARX": FIRST_asthmarx,
            "LAST_ASTHMARX": LAST_asthmarx,
            "NUM_ASTHMARX": NUM_astmarx,

            # Asignación para SHELLFISH
            "SHELLFISH_ALG_START": SHELLFISH_alg_start,
            "SHELLFISH_ALG_END": SHELLFISH_alg_end,

            # Asignación para FISH
            "FISH_ALG_START": FISH_alg_start,
            "FISH_ALG_END": FISH_alg_end,

            # Asignación para MILK
            "MILK_ALG_START": MILK_alg_start,
            "MILK_ALG_END": MILK_alg_end,

            # Asignación para SOY
            "SOY_ALG_START": SOY_alg_start,
            "SOY_ALG_END": SOY_alg_end,  
            
            # Asignación para EGG
            "EGG_ALG_START": EGG_alg_start,
            "EGG_ALG_END": EGG_alg_end,  
            
            # Asignación para WHEAT
            "WHEAT_ALG_START": WHEAT_alg_start,
            "WHEAT_ALG_END": WHEAT_alg_end,  
            
            # Asignación para PEANUT
            "PEANUT_ALG_START": PEANUT_alg_start,
            "PEANUT_ALG_END": PEANUT_alg_end,  
            
            # Asignación para SESAME
            "SESAME_ALG_START": SESAME_alg_start,
            "SESAME_ALG_END": SESAME_alg_end,  
            
            # Asignación para TREENUT
            "TREENUT_ALG_START": TREENUT_alg_start,
            "TREENUT_ALG_END": TREENUT_alg_end,  
            
            # Asignación para WALNUT
            "WALNUT_ALG_START": WALNUT_alg_start,
            "WALNUT_ALG_END": WALNUT_alg_end,  
            
            # Asignación para PECAN
            "PECAN_ALG_START": PECAN_alg_start,
            "PECAN_ALG_END": PECAN_alg_end,  
            
            # Asignación para PISTACH
            "PISTACH_ALG_START": PISTACH_alg_start,
            "PISTACH_ALG_END": PISTACH_alg_end,  
            
            # Asignación para ALMOND
            "ALMOND_ALG_START": ALMOND_alg_start,
            "ALMOND_ALG_END": ALMOND_alg_end,  
            
            # Asignación para BRAZIL
            "BRAZIL_ALG_START": BRAZIL_alg_start,
            "BRAZIL_ALG_END": BRAZIL_alg_end,  
            
            # Asignación para HAZELNUT
            "HAZELNUT_ALG_START": HAZELNUT_alg_start,
            "HAZELNUT_ALG_END": HAZELNUT_alg_end,  
            
            # Asignación para CASHEW
            "CASHEW_ALG_START": CASHEW_alg_start,
            "CASHEW_ALG_END": CASHEW_alg_end,  
            
            # Asignación para DERM
            "ATOPIC_DERM_START": ATOPIC_derm_start,
            "ATOPIC_DERM_END": ATOPIC_derm_end,  
            
            # Asignación para DERM
            "ALLERGIC_RHINITIS_START": ALLERGIC_rhinitis_start,
            "ALLERGIC_RHINITIS_END": ALLERGIC_rhinitis_end,  

            # Asignación para ASTHMA
            "ASTHMA_START": ASTHMA_start,
            "ASTHMA_END": ASTHMA_end,
            
        }
        datos_manager.guardar_datos_csv(datos_formulario)
        
    # Guardar botón
    btn_guardar = ctk.CTkButton(frame_main, text="Guardar", command=guardar)
    btn_guardar.pack(pady=10)

# Función para mostrar los botones
def mostrar_datos():
    limpiar_frame_main()  # Limpiar el frame antes de mostrar nuevos elementos
    lbl_titulo = ctk.CTkLabel(frame_main, text="Datos", font=("Arial", 20))
    lbl_titulo.pack(pady=10)

    # Crear un frame con scroll para los botones
    frame_scroll = ctk.CTkScrollableFrame(frame_main, width=600, height=400)
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    # Botón para mostrar la información del DataFrame en un popup
    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Mostrar Información", command=lambda: messagebox.showinfo(
        "Información del DataFrame", 
        f"Primeras filas del DataFrame:\n{str(datos_manager.df.head())}\n\n"
        f"Información general sobre el DataFrame:\n{str(datos_manager.df.info())}\n\n"
        f"Estadísticas descriptivas:\n{str(datos_manager.df.describe())}"
    ))
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Frecuencia en generos", command=datos_manager.graficar_contingencia_genero_alergias)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Proporcion en generos", command=datos_manager.plot_gender_allergy_proportions)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Edad promedio", command=datos_manager.edad_promedio)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Alergias mas frecuentes", command=datos_manager.graficar_distribucion_alergias)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="diagnostico por tipo de alergia", command=datos_manager.plot_avg_age_by_allergy)
    btn_mostrar_info.pack(pady=10)
        
    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Alergias mejoran o empeoran?", command=datos_manager.graficar_mejora_empeoramiento)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Frecuencia de alergias por año de nacimiento", command=datos_manager.graficar_alergias_por_año_nacimiento)
    btn_mostrar_info.pack(pady=10)

    btn_mostrar_info = ctk.CTkButton(frame_scroll, text="Alergias sengun el payer_factor", command=datos_manager.graficar_alergias_vs_payer_factor)
    btn_mostrar_info.pack(pady=10)

# Función para alternar la visibilidad de la barra lateral
def alternar_sidebar():
    if sidebar_visible.get():
        frame_sidebar.pack_forget()
        sidebar_visible.set(False)
    else:
        frame_sidebar.pack(side="left", fill="y")
        sidebar_visible.set(True)


btn_toggle_sidebar = ctk.CTkButton(root, text="≡", width=40, height=40, command=alternar_sidebar)
btn_toggle_sidebar.place(x=10, y=10)
btn_toggle_sidebar.pack(pady=10)

btn_registros = ctk.CTkButton(frame_sidebar, text="Registros", command=mostrar_registros)
btn_registros.pack(pady=10, padx=10, fill="x")

btn_formulario = ctk.CTkButton(frame_sidebar, text="Formulario", command=mostrar_formulario)
btn_formulario.pack(pady=10, padx=10, fill="x")

btn_formulario = ctk.CTkButton(frame_sidebar, text="Datos", command=mostrar_datos)
btn_formulario.pack(pady=10, padx=10, fill="x")

mostrar_registros()

def ejecutar_interfaz():
    root.mainloop()
