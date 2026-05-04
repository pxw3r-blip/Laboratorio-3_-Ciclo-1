import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Laboratorio - Análisis de CSV")

vehiculos = pd.read_csv("assets/csv_old/Electric_Vehicle_Population-2.csv")
gym = pd.read_csv("assets/csv_old/GymExerciseTracking.csv")
videojuegos = pd.read_csv("assets/csv_old/steam_store_data_2024.csv")
netflix = pd.read_csv("assets/csv_old/netflix_titles.csv")

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

st.header("2. Ingreso de Datos")

st.subheader("Agregar Vehículo")

if "vehiculos" not in st.session_state:
    st.session_state.vehiculos = vehiculos.copy()

make = st.text_input("Marca")
model = st.text_input("Modelo")
year = st.number_input("Año", min_value=2000, max_value=2025)
price = st.number_input("Precio", min_value=0.0)

if st.button("Agregar Vehículo"):
    nuevo = pd.DataFrame([[make, model, year, price]],
                         columns=["Make", "Model", "Model Year", "Base_MSRP"])
    st.session_state.vehiculos = pd.concat([st.session_state.vehiculos, nuevo], ignore_index=True)
    st.success("Vehículo agregado")

st.subheader("Agregar Videojuego")

if "videojuegos" not in st.session_state:
    st.session_state.videojuegos = videojuegos.copy()

titulo = st.text_input("Título del juego")
precio = st.number_input("Precio juego", min_value=0.0)
descuento = st.number_input("Descuento (%)", min_value=0.0, max_value=100.0)

if st.button("Agregar Juego"):
    nuevo = pd.DataFrame([[titulo, precio, descuento]],
                         columns=["title", "price", "salePercentage"])
    st.session_state.videojuegos = pd.concat([st.session_state.videojuegos, nuevo], ignore_index=True)
    st.success("Juego agregado")

st.header("3. Filtros")


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


st.subheader("Gimnasio")

calorias = st.number_input("Calorías mínimas", min_value=0.0)
grasa = st.slider("Grasa máxima (%)", 0.0, 100.0)

gym_calorias = gym[gym["Calories_Burned"] >= calorias]
gym_grasa = gym[gym["Fat_Percentage"] <= grasa]

st.write("Por calorías:")
st.dataframe(gym_calorias)

st.write("Por grasa:")
st.dataframe(gym_grasa)


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


st.subheader("Netflix")

duracion = st.number_input("Duración mínima (min)", min_value=0)
anio = st.number_input("Año máximo", min_value=1900, max_value=2025)

netflix_duracion = netflix[netflix["duration_int"] > duracion]
netflix_anio = netflix[netflix["year_added"] < anio]

st.write("Por duración:")
st.dataframe(netflix_duracion)

st.write("Por año agregado:")
st.dataframe(netflix_anio)

st.header("4. Exploración Avanzada")
st.subheader("Vehículos Eléctricos")

def categoria_rango(x):
    if x < 100:
        return "Bajo"
    elif x <= 250:
        return "Medio"
    else:
        return "Alto"

st.session_state.vehiculos["RangoCategoria"] = st.session_state.vehiculos["Electric Range"].apply(categoria_rango)

conteo_v = st.session_state.vehiculos["RangoCategoria"].value_counts()
st.write(conteo_v)

fig, ax = plt.subplots()
conteo_v.plot(kind='bar', ax=ax)
ax.set_title("Vehículos por rango eléctrico")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado_v = st.session_state.vehiculos.groupby("RangoCategoria").agg({
    "Base_MSRP": "mean",
    "Model Year": "mean",
    "Electric Range": "std"
})

st.write(agrupado_v)

# GIMNASIO
st.subheader("Gimnasio")

def nivel_frecuencia(x):
    if x < 3:
        return "Baja"
    elif x <= 5:
        return "Moderada"
    else:
        return "Alta"

gym["NivelFrecuencia"] = gym["Workout_Frequency"].apply(nivel_frecuencia)

conteo_g = gym["NivelFrecuencia"].value_counts()
st.write(conteo_g)

fig, ax = plt.subplots()
conteo_g.plot(kind='bar', ax=ax)
ax.set_title("Frecuencia de entrenamiento")
ax.set_xlabel("Nivel")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado_g = gym.groupby("NivelFrecuencia").agg({
    "Session_Duration": "mean",
    "Experience_Level": "mean",
    "BMI": "std"
})

st.write(agrupado_g)


st.subheader("Videojuegos")

def gama_juego(x):
    if x < 10:
        return "Baja"
    elif x <= 24:
        return "Media"
    else:
        return "Alta"

st.session_state.videojuegos["GamaJuego"] = st.session_state.videojuegos["price"].apply(gama_juego)

conteo_j = st.session_state.videojuegos["GamaJuego"].value_counts()
st.write(conteo_j)

fig, ax = plt.subplots()
conteo_j.plot(kind='bar', ax=ax)
ax.set_title("Gama de videojuegos")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado_j = st.session_state.videojuegos.groupby("GamaJuego").agg({
    "price": ["mean", "std"],
    "salePercentage": "mean"
})

st.write(agrupado_j)

# NETFLIX
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

conteo_n = netflix["TipoAudiencia"].value_counts()
st.write(conteo_n)

fig, ax = plt.subplots()
conteo_n.plot(kind='bar', ax=ax)
ax.set_title("Tipo de audiencia")
ax.set_xlabel("Categoría")
ax.set_ylabel("Cantidad")
st.pyplot(fig)

agrupado_n = netflix.groupby("TipoAudiencia").agg({
    "duration_int": "mean",
    "type": lambda x: x.value_counts().idxmax()
})

st.write(agrupado_n)