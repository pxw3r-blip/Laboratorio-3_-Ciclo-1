import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Laboratorio - Análisis de CSV")

vehiculos = pd.read_csv("Electric_Vehicle_Population-2.csv")
gym = pd.read_csv("GymExerciseTracking.csv")
videojuegos = pd.read_csv("steam_store_data_2024.csv")
netflix = pd.read_csv("netflix_titles.csv")

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

f1 = st.session_state.vehiculos[
    st.session_state.vehiculos["Model Year"] < year_filtro
]

f2 = st.session_state.vehiculos[
    st.session_state.vehiculos["Base_MSRP"] < precio_filtro
]

st.write("Filtrado por año:")
st.dataframe(f1)

st.write("Filtrado por precio:")
st.dataframe(f2)


st.subheader("Gimnasio")

calorias = st.number_input("Calorías mínimas", min_value=0.0)
grasa = st.slider("Grasa máxima (%)", 0.0, 100.0)

f1 = gym[gym["Calories_Burned"] >= calorias]
f2 = gym[gym["Fat_Percentage"] <= grasa]

st.write("Por calorías:")
st.dataframe(f1)

st.write("Por grasa:")
st.dataframe(f2)


st.subheader("Videojuegos")

precio_min = st.number_input("Precio mínimo", min_value=0.0)
desc_max = st.number_input("Descuento máximo (%)", min_value=0.0)

f1 = st.session_state.videojuegos[
    st.session_state.videojuegos["price"] > precio_min
]

f2 = st.session_state.videojuegos[
    st.session_state.videojuegos["salePercentage"] < desc_max
]

st.write("Por precio:")
st.dataframe(f1)

st.write("Por descuento:")
st.dataframe(f2)

st.subheader("Netflix")

duracion = st.number_input("Duración mínima (min)", min_value=0)
anio = st.number_input("Año máximo", min_value=1900, max_value=2025)

netflix["duration_int"] = netflix["duration"].str.extract(r'(\d+)').astype(float)

f1 = netflix[netflix["duration_int"] > duracion]
f2 = netflix[netflix["release_year"] < anio]

st.write("Por duración:")
st.dataframe(f1)

st.write("Por año:")
st.dataframe(f2)