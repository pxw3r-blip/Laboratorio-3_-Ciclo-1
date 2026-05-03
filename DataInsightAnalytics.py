import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Laboratorio - Análisis de CSV")

# =========================
# CARGA DE DATOS
# =========================

vehiculos = pd.read_csv("Electric_Vehicle_Population-2.csv")
gym = pd.read_csv("GymExerciseTracking.csv")
videojuegos = pd.read_csv("steam_store_data_2024.csv")
netflix = pd.read_csv("netflix_titles.csv")

# =========================
# SESSION STATE
# =========================

if "vehiculos" not in st.session_state:
    st.session_state.vehiculos = vehiculos.copy()

if "videojuegos" not in st.session_state:
    st.session_state.videojuegos = videojuegos.copy()

# =========================
# 1. EXPLORACIÓN
# =========================

def explorar(df, nombre):
    st.subheader(f"Exploración: {nombre}")
    st.write("Dimensiones:", df.shape)
    st.write("Columnas:")
    st.write(df.columns.tolist())
    st.write("Primeras 6 filas:")
    st.dataframe(df.head(6))
    st.write("Estadísticas:")
    st.dataframe(df.describe())

st.header("1. Exploración de Datos")

explorar(vehiculos, "Vehículos Eléctricos")
explorar(gym, "Gimnasio")
explorar(videojuegos, "Videojuegos")
explorar(netflix, "Netflix")

# =========================
# 2. INGRESO DE DATOS
# =========================

st.header("2. Ingreso de Datos")

# Vehículos
st.subheader("Agregar Vehículo")

make = st.text_input("Marca")
model = st.text_input("Modelo")
year = st.number_input("Año", min_value=2000, max_value=2025)
price = st.number_input("Precio", min_value=0.0)

if st.button("Agregar Vehículo"):
    nuevo = pd.DataFrame([[make, model, year, price]],
                         columns=["Make", "Model", "Model Year", "Base_MSRP"])
    st.session_state.vehiculos = pd.concat([st.session_state.vehiculos, nuevo], ignore_index=True)
    st.success("Vehículo agregado")

# Videojuegos
st.subheader("Agregar Videojuego")

titulo = st.text_input("Título del juego")
precio = st.number_input("Precio juego", min_value=0.0)
descuento = st.number_input("Descuento (%)", min_value=0.0, max_value=100.0)

if st.button("Agregar Juego"):
    nuevo = pd.DataFrame([[titulo, precio, descuento]],
                         columns=["title", "price", "salePercentage"])
    st.session_state.videojuegos = pd.concat([st.session_state.videojuegos, nuevo], ignore_index=True)
    st.success("Juego agregado")

# =========================
# 3. FILTROS
# =========================

st.header("3. Filtros")

# Vehículos
st.subheader("Vehículos Eléctricos")

year_filtro = st.slider("Año máximo", 2000, 2025, 2015)
precio_filtro = st.number_input("Precio máximo", 0.0, 845000.0)

vehiculos_year = st.session_state.vehiculos[
    st.session_state.vehiculos["Model Year"] < year_filtro
]

vehiculos_precio = st.session_state.vehiculos[
    st.session_state.vehiculos["Base_MSRP"] < precio_filtro
]

st.write("Filtrado por año:")
st.dataframe(vehiculos_year)

st.write("Filtrado por precio:")
st.dataframe(vehiculos_precio)

# Gimnasio
st.subheader("Gimnasio")

calorias = st.number_input("Calorías mínimas", min_value=0.0)
grasa = st.slider("Grasa máxima (%)", 0.0, 100.0)

gym_calorias = gym[gym["Calories_Burned"] >= calorias]
gym_grasa = gym[gym["Fat_Percentage"] <= grasa]

st.write("Por calorías:")
st.dataframe(gym_calorias)

st.write("Por grasa:")
st.dataframe(gym_grasa)

# Videojuegos
st.subheader("Videojuegos")

precio_min = st.number_input("Precio mínimo", min_value=0.0)
desc_max = st.number_input("Descuento máximo (%)", min_value=0.0)

juegos_precio = st.session_state.videojuegos[
    st.session_state.videojuegos["price"] > precio_min
]

juegos_descuento = st.session_state.videojuegos[
    st.session_state.videojuegos["salePercentage"] < desc_max
]

st.write("Por precio:")
st.dataframe(juegos_precio)

st.write("Por descuento:")
st.dataframe(juegos_descuento)

# Netflix
st.subheader("Netflix")

duracion = st.number_input("Duración mínima (min)", min_value=0)
anio = st.number_input("Año máximo", min_value=1900, max_value=2025)

netflix["duration_int"] = netflix["duration"].str.extract(r'(\d+)').astype(float)
netflix["date_added"] = pd.to_datetime(netflix["date_added"], errors='coerce')
netflix["year_added"] = netflix["date_added"].dt.year

netflix_duracion = netflix[netflix["duration_int"] > duracion]
netflix_anio = netflix[netflix["year_added"] < anio]

st.write("Por duración:")
st.dataframe(netflix_duracion)

st.write("Por año agregado:")
st.dataframe(netflix_anio)

# =========================
# 4. EXPLORACIÓN AVANZADA
# =========================

st.header("4. Exploración Avanzada")

# ---------- VEHÍCULOS ----------
st.subheader("Vehículos Eléctricos")

def categoria_rango(x):
    if x < 100:
        return "Bajo"
    elif x <= 250:
        return "Medio"
    else:
        return "Alto"

st.session_state.vehiculos["RangoCategoria"] = st.session_state.vehiculos["Electric Range"].apply(categoria_rango)

conteo = st.session_state.vehiculos["RangoCategoria"].value_counts()
st.write(conteo)

fig, ax = plt.subplots()
conteo.plot(kind='bar', ax=ax)
ax.set_title("Vehículos por rango eléctrico")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado = st.session_state.vehiculos.groupby("RangoCategoria").agg({
    "Base_MSRP": "mean",
    "Model Year": "mean",
    "Electric Range": "std"
})

st.write(agrupado)

# ---------- GIMNASIO ----------
st.subheader("Gimnasio")

def nivel_frecuencia(x):
    if x < 3:
        return "Baja"
    elif x <= 5:
        return "Moderada"
    else:
        return "Alta"

gym["NivelFrecuencia"] = gym["Workout_Frequency"].apply(nivel_frecuencia)

conteo = gym["NivelFrecuencia"].value_counts()
st.write(conteo)

fig, ax = plt.subplots()
conteo.plot(kind='bar', ax=ax)
ax.set_title("Frecuencia de entrenamiento")
ax.set_xlabel("Nivel")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado = gym.groupby("NivelFrecuencia").agg({
    "Session_Duration": "mean",
    "Experience_Level": "mean",
    "BMI": "std"
})

st.write(agrupado)

# ---------- VIDEOJUEGOS ----------
st.subheader("Videojuegos")

def gama_juego(x):
    if x < 10:
        return "Baja"
    elif x <= 24:
        return "Media"
    else:
        return "Alta"

st.session_state.videojuegos["GamaJuego"] = st.session_state.videojuegos["price"].apply(gama_juego)

conteo = st.session_state.videojuegos["GamaJuego"].value_counts()
st.write(conteo)

fig, ax = plt.subplots()
conteo.plot(kind='bar', ax=ax)
ax.set_title("Gama de videojuegos")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado = st.session_state.videojuegos.groupby("GamaJuego").agg({
    "price": ["mean", "std"],
    "salePercentage": "mean"
})

st.write(agrupado)

# ---------- NETFLIX ----------
st.subheader("Netflix")

def tipo_audiencia(x):
    if x in ["G", "TV-Y", "TV-G", "TV-Y7", "TV-Y7-FV"]:
        return "Niños"
    elif x in ["PG", "TV-PG"]:
        return "Adolescentes"
    elif x in ["PG-13", "TV-14"]:
        return "Adultos Jóvenes"
    else:
        return "Adultos"

netflix["TipoAudiencia"] = netflix["rating"].apply(tipo_audiencia)

conteo = netflix["TipoAudiencia"].value_counts()
st.write(conteo)

fig, ax = plt.subplots()
conteo.plot(kind='bar', ax=ax)
ax.set_title("Tipo de audiencia")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado = netflix.groupby("TipoAudiencia").agg({
    "duration_int": "mean",
    "type": lambda x: x.value_counts().idxmax()
})

st.write(agrupado)