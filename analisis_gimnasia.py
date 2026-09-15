import pandas as pd

# Leer el archivo Excel
archivo = "gimnasia_data_2025_2026.xlsx"

partidos = pd.read_excel(archivo, sheet_name="Partidos")
entrenadores = pd.read_excel(archivo, sheet_name="Entrenadores")

partidos_jugados = partidos[partidos["Resultado"].isin(["G", "E", "P"])].copy()

# Mostrar información básica
print("Cantidad de partidos:", len(partidos))
print("\nColumnas:")
print(partidos.columns.tolist())

print("\nPrimeros partidos:")
print(partidos.head())

# Resumen general
print("\n--- RESUMEN GENERAL ---")

pj = len(partidos_jugados)
pg = (partidos_jugados["Resultado"] == "G").sum()
pe = (partidos_jugados["Resultado"] == "E").sum()
pp = (partidos_jugados["Resultado"] == "P").sum()
puntos = partidos_jugados["Puntos"].sum()

print("Partidos:", pj)
print("Ganados:", pg)
print("Empatados:", pe)
print("Perdidos:", pp)
print("Puntos:", puntos)
print("Puntos por partido:", round(puntos / pj, 2))

# Rendimiento por entrenador

resumen_dt = partidos_jugados.groupby("DT").agg(
    PJ=("Resultado", "count"),
    PG=("Resultado", lambda x: (x == "G").sum()),
    PE=("Resultado", lambda x: (x == "E").sum()),
    PP=("Resultado", lambda x: (x == "P").sum()),
    Puntos=("Puntos", "sum"),
    GF=("GF", "sum"),
    GC=("GC", "sum")
)

resumen_dt["Puntos_por_partido"] = (
    resumen_dt["Puntos"] / resumen_dt["PJ"]
)

resumen_dt["Goles_a_favor_por_partido"] = (
    resumen_dt["GF"] / resumen_dt["PJ"]
)

resumen_dt["Goles_en_contra_por_partido"] = (
    resumen_dt["GC"] / resumen_dt["PJ"]
)

print("\n--- RENDIMIENTO POR ENTRENADOR ---")
print(resumen_dt.round(2))

# Porcentajes de resultados por entrenador
resumen_dt["Porcentaje_victorias"] = (
    resumen_dt["PG"] / resumen_dt["PJ"] * 100
)

resumen_dt["Porcentaje_empates"] = (
    resumen_dt["PE"] / resumen_dt["PJ"] * 100
)

resumen_dt["Porcentaje_derrotas"] = (
    resumen_dt["PP"] / resumen_dt["PJ"] * 100
)

print("\n--- PORCENTAJES POR ENTRENADOR ---")
print(
    resumen_dt[
        [
            "PJ",
            "PG",
            "PE",
            "PP",
            "Porcentaje_victorias",
            "Porcentaje_empates",
            "Porcentaje_derrotas",
        ]
    ].round(2)
)

import matplotlib.pyplot as plt

# Solo incluir entrenadores con al menos 5 partidos dirigidos.
# Así evitamos comparar ciclos demasiado cortos.
grafico_dt = resumen_dt[
    resumen_dt["PJ"] >= 5
].sort_values(
    "Puntos_por_partido",
    ascending=False
)

# Colores: destacamos a Pereyra y dejamos el resto en azul más suave
colores = [
    "#77D3FF" if dt == "Ariel Pereyra" else "#496A97"
    for dt in grafico_dt.index
]

# Gráfico vertical para Instagram: 1080 x 1350 píxeles
fig, ax = plt.subplots(figsize=(10.8, 13.5), facecolor="#071E45")
ax.set_facecolor("#071E45")

barras = ax.barh(
    grafico_dt.index,
    grafico_dt["Puntos_por_partido"],
    color=colores
)

ax.invert_yaxis()

# Valores al final de cada barra
for barra, valor in zip(barras, grafico_dt["Puntos_por_partido"]):
    ax.text(
        valor + 0.03,
        barra.get_y() + barra.get_height() / 2,
        f"{valor:.2f}",
        va="center",
        color="white",
        fontsize=18,
        fontweight="bold"
    )

ax.set_title(
    "Puntos por partido\nGimnasia por entrenador",
    color="white",
    fontsize=28,
    fontweight="bold",
    pad=25
)

ax.text(
    0,
    1.02,
    "Solo entrenadores con 5 o más partidos dirigidos",
    transform=ax.transAxes,
    color="#77D3FF",
    fontsize=16
)

ax.set_xlabel("Puntos por partido", color="white", fontsize=16)
ax.tick_params(colors="white", labelsize=16)

for borde in ax.spines.values():
    borde.set_visible(False)

ax.grid(axis="x", color="white", alpha=0.15)
plt.tight_layout()

plt.savefig(
    "grafico_puntos_por_dt.jpg",
    dpi=100,
    facecolor="#071E45",
    format="jpg"
)

plt.show()

# Placa: arranque de Ariel Pereyra
pereyra = resumen_dt.loc["Ariel Pereyra"]

fig, ax = plt.subplots(figsize=(10.8, 13.5), facecolor="#071E45")
ax.set_facecolor("#071E45")
ax.axis("off")

# Título
ax.text(
    0.5, 0.92,
    "ARIEL PEREYRA",
    ha="center",
    va="center",
    color="white",
    fontsize=34,
    fontweight="bold",
    transform=ax.transAxes
)

ax.text(
    0.5, 0.875,
    "SU ARRANQUE EN GIMNASIA",
    ha="center",
    va="center",
    color="#77D3FF",
    fontsize=16,
    fontweight="bold",
    transform=ax.transAxes
)

# Línea decorativa
ax.plot(
    [0.18, 0.82],
    [0.83, 0.83],
    color="#77D3FF",
    linewidth=2,
    transform=ax.transAxes
)

# Datos principales
datos = [
    (pereyra["PJ"], "PARTIDOS"),
    (pereyra["PG"], "VICTORIAS"),
    (pereyra["PE"], "EMPATE"),
    (pereyra["PP"], "DERROTAS"),
]

posiciones_y = [0.70, 0.58, 0.46, 0.34]

for (valor, etiqueta), y in zip(datos, posiciones_y):
    ax.text(
        0.5, y,
        f"{int(valor)}",
        ha="center",
        va="center",
        color="white",
        fontsize=42,
        fontweight="bold",
        transform=ax.transAxes
    )

    ax.text(
        0.5, y - 0.045,
        etiqueta,
        ha="center",
        va="center",
        color="#77D3FF",
        fontsize=16,
        fontweight="bold",
        transform=ax.transAxes
    )

# Datos destacados
ax.plot(
    [0.18, 0.82],
    [0.23, 0.23],
    color="#77D3FF",
    linewidth=2,
    transform=ax.transAxes
)

porcentaje_victorias = pereyra["Porcentaje_victorias"]
puntos_por_partido = pereyra["Puntos_por_partido"]

ax.text(
    0.5, 0.16,
    f"{porcentaje_victorias:.1f}% DE TRIUNFOS",
    ha="center",
    va="center",
    color="white",
    fontsize=25,
    fontweight="bold",
    transform=ax.transAxes
)

ax.text(
    0.5, 0.10,
    f"{puntos_por_partido:.2f} PUNTOS POR PARTIDO",
    ha="center",
    va="center",
    color="#77D3FF",
    fontsize=20,
    fontweight="bold",
    transform=ax.transAxes
)

# Pie de la placa
ax.text(
    0.5, 0.04,
    "GimnasiaData · Datos de partidos registrados desde 2025",
    ha="center",
    va="center",
    color="#AFC9DF",
    fontsize=11,
    transform=ax.transAxes
)

plt.savefig(
    "arranque_ariel_pereyra.jpg",
    dpi=100,
    facecolor="#071E45"
)

plt.show()

import matplotlib.pyplot as plt

# Fecha del primer partido dirigido por Ariel Pereyra
fecha_inicio_pereyra = partidos_jugados.loc[
    partidos_jugados["DT"] == "Ariel Pereyra",
    "Fecha"
].min()

# Separar los dos períodos
antes_pereyra = partidos_jugados[
    partidos_jugados["Fecha"] < fecha_inicio_pereyra
].copy()

con_pereyra = partidos_jugados[
    partidos_jugados["DT"] == "Ariel Pereyra"
].copy()

# Función para resumir un grupo de partidos
def resumen_periodo(datos):
    pj = len(datos)

    return {
        "Partidos": pj,
        "Puntos por partido": datos["Puntos"].sum() / pj,
        "% de victorias": (datos["Resultado"] == "G").sum() / pj * 100,
        "Goles a favor por partido": datos["GF"].sum() / pj,
        "Goles en contra por partido": datos["GC"].sum() / pj,
    }

resumen_antes = resumen_periodo(antes_pereyra)
resumen_con = resumen_periodo(con_pereyra)

# Tabla que aparecerá en la placa
filas = [
    [
        "Partidos",
        f"{resumen_antes['Partidos']}",
        f"{resumen_con['Partidos']}",
    ],
    [
        "Puntos por partido",
        f"{resumen_antes['Puntos por partido']:.2f}",
        f"{resumen_con['Puntos por partido']:.2f}",
    ],
    [
        "% de victorias",
        f"{resumen_antes['% de victorias']:.1f}%",
        f"{resumen_con['% de victorias']:.1f}%",
    ],
    [
        "Goles a favor por partido",
        f"{resumen_antes['Goles a favor por partido']:.2f}",
        f"{resumen_con['Goles a favor por partido']:.2f}",
    ],
    [
        "Goles en contra por partido",
        f"{resumen_antes['Goles en contra por partido']:.2f}",
        f"{resumen_con['Goles en contra por partido']:.2f}",
    ],
]

# Crear una placa vertical para redes
fig, ax = plt.subplots(figsize=(10.8, 13.5), facecolor="#071E45")
ax.set_facecolor("#071E45")
ax.axis("off")

ax.text(
    0.5, 0.91,
    "GIMNASIA: ANTES Y CON PEREYRA",
    ha="center",
    color="white",
    fontsize=27,
    fontweight="bold",
    transform=ax.transAxes
)

ax.text(
    0.5, 0.86,
    "Comparación de partidos registrados desde 2025",
    ha="center",
    color="#77D3FF",
    fontsize=15,
    transform=ax.transAxes
)

tabla = ax.table(
    cellText=filas,
    colLabels=["Indicador", "Antes de Pereyra", "Con Pereyra"],
    cellLoc="center",
    colLoc="center",
    bbox=[0.07, 0.27, 0.86, 0.48]
)

tabla.auto_set_font_size(False)
tabla.set_fontsize(15)

# Dar color y estilo a la tabla
for (fila, columna), celda in tabla.get_celld().items():
    celda.set_edgecolor("#77D3FF")
    celda.set_linewidth(1.2)

    if fila == 0:
        celda.set_facecolor("#16477F")
        celda.get_text().set_color("white")
        celda.get_text().set_fontweight("bold")
    else:
        celda.set_facecolor("#0C2D62")
        celda.get_text().set_color("white")

        # Destacar la columna "Con Pereyra"
        if columna == 2:
            celda.set_facecolor("#1C5B91")
            celda.get_text().set_color("#77D3FF")
            celda.get_text().set_fontweight("bold")

ax.text(
    0.5, 0.17,
    "Los promedios permiten comparar períodos\ncon distinta cantidad de partidos.",
    ha="center",
    color="white",
    fontsize=17,
    transform=ax.transAxes
)

ax.text(
    0.5, 0.08,
    "GimnasiaData",
    ha="center",
    color="#77D3FF",
    fontsize=19,
    fontweight="bold",
    transform=ax.transAxes
)

plt.savefig(
    "antes_y_con_pereyra.jpg",
    dpi=100,
    facecolor="#071E45"
)

plt.show()

# Gimnasia: rendimiento de local vs. visitante desde 2025

partidos_2025_hoy = partidos_jugados[
    pd.to_datetime(partidos_jugados["Fecha"]).dt.year >= 2025
].copy()

# Limpiar las categorías de localía
partidos_2025_hoy["Local_visitante_limpio"] = (
    partidos_2025_hoy["Local_visitante"]
    .astype("string")
    .str.strip()
    .str.lower()
    .replace({
        "l": "local",
        "v": "visitante",
    })
    .str.capitalize()
)

# Para esta comparación usamos solo local y visitante.
# Los partidos en cancha neutral quedan afuera.
partidos_localia = partidos_2025_hoy[
    partidos_2025_hoy["Local_visitante_limpio"].isin(
        ["Local", "Visitante"]
    )
].copy()

resumen_localia = partidos_localia.groupby(
    "Local_visitante_limpio"
).agg(
    PJ=("Resultado", "count"),
    PG=("Resultado", lambda x: (x == "G").sum()),
    PE=("Resultado", lambda x: (x == "E").sum()),
    PP=("Resultado", lambda x: (x == "P").sum()),
    Puntos=("Puntos", "sum"),
    GF=("GF", "sum"),
    GC=("GC", "sum"),
)

resumen_localia["Puntos_por_partido"] = (
    resumen_localia["Puntos"] / resumen_localia["PJ"]
)

resumen_localia["Porcentaje_victorias"] = (
    resumen_localia["PG"] / resumen_localia["PJ"] * 100
)

print("\n--- LOCAL VS. VISITANTE DESDE 2025 ---")
print(resumen_localia.round(2))

# Colores fijos para cada condición
colores = [
    "#77D3FF" if condicion == "Local" else "#4E74A3"
    for condicion in resumen_localia.index
]

fig, ejes = plt.subplots(
    2,
    1,
    figsize=(10.8, 13.5),
    facecolor="#071E45"
)

for ax in ejes:
    ax.set_facecolor("#071E45")

# Puntos por partido
barras_ppp = ejes[0].bar(
    resumen_localia.index,
    resumen_localia["Puntos_por_partido"],
    color=colores
)

ejes[0].set_title(
    "Puntos por partido",
    color="white",
    fontsize=23,
    fontweight="bold",
    pad=25
)

ejes[0].tick_params(colors="white", labelsize=16)
ejes[0].set_ylim(
    0,
    resumen_localia["Puntos_por_partido"].max() + 0.5
)

for barra, valor in zip(
    barras_ppp,
    resumen_localia["Puntos_por_partido"]
):
    ejes[0].text(
        barra.get_x() + barra.get_width() / 2,
        valor + 0.05,
        f"{valor:.2f}",
        ha="center",
        color="white",
        fontsize=18,
        fontweight="bold"
    )

# Porcentaje de victorias
barras_victorias = ejes[1].bar(
    resumen_localia.index,
    resumen_localia["Porcentaje_victorias"],
    color=colores
)

ejes[1].set_title(
    "Porcentaje de victorias",
    color="white",
    fontsize=23,
    fontweight="bold",
    pad=25
)

ejes[1].tick_params(colors="white", labelsize=16)
ejes[1].set_ylim(0, 100)

for barra, valor in zip(
    barras_victorias,
    resumen_localia["Porcentaje_victorias"]
):
    ejes[1].text(
        barra.get_x() + barra.get_width() / 2,
        valor + 3,
        f"{valor:.1f}%",
        ha="center",
        color="white",
        fontsize=18,
        fontweight="bold"
    )

for ax in ejes:
    for borde in ax.spines.values():
        borde.set_visible(False)

    ax.grid(axis="y", color="white", alpha=0.15)

fig.suptitle(
    "GIMNASIA: LOCAL VS. VISITANTE",
    color="white",
    fontsize=28,
    fontweight="bold",
    y=0.97
)

fig.text(
    0.5,
    0.03,
    "Partidos jugados registrados desde 2025 · GimnasiaData",
    ha="center",
    color="#77D3FF",
    fontsize=13
)

# Más espacio entre los dos gráficos
fig.subplots_adjust(
    top=0.85,
    bottom=0.11,
    hspace=0.55
)

plt.savefig(
    "gimnasia_local_vs_visitante.jpg",
    dpi=100,
    facecolor="#071E45"
)

plt.show()

# Goles a favor y en contra por DT desde 2025

grafico_goles = resumen_dt[
    resumen_dt["PJ"] >= 5
].copy()

grafico_goles["GF_por_partido"] = (
    grafico_goles["GF"] / grafico_goles["PJ"]
)

grafico_goles["GC_por_partido"] = (
    grafico_goles["GC"] / grafico_goles["PJ"]
)

# Ordenar de mayor a menor según goles a favor por partido
grafico_goles = grafico_goles.sort_values(
    "GF_por_partido",
    ascending=False
)

print("\n--- GOLES A FAVOR Y EN CONTRA POR DT ---")
print(
    grafico_goles[
        ["PJ", "GF_por_partido", "GC_por_partido"]
    ].round(2)
)

# Posiciones de las barras
posiciones = list(range(len(grafico_goles)))
ancho = 0.36

fig, ax = plt.subplots(
    figsize=(10.8, 13.5),
    facecolor="#071E45"
)

ax.set_facecolor("#071E45")

# Barras
barras_gf = ax.bar(
    [posicion - ancho / 2 for posicion in posiciones],
    grafico_goles["GF_por_partido"],
    width=ancho,
    color="#77D3FF",
    label="Goles a favor"
)

barras_gc = ax.bar(
    [posicion + ancho / 2 for posicion in posiciones],
    grafico_goles["GC_por_partido"],
    width=ancho,
    color="#C96B75",
    label="Goles en contra"
)

# Valores sobre cada barra
for barra, valor in zip(
    barras_gf,
    grafico_goles["GF_por_partido"]
):
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        valor + 0.04,
        f"{valor:.2f}",
        ha="center",
        color="white",
        fontsize=15,
        fontweight="bold"
    )

for barra, valor in zip(
    barras_gc,
    grafico_goles["GC_por_partido"]
):
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        valor + 0.04,
        f"{valor:.2f}",
        ha="center",
        color="white",
        fontsize=15,
        fontweight="bold"
    )

ax.set_xticks(posiciones)
ax.set_xticklabels(
    grafico_goles.index,
    color="white",
    fontsize=14,
    rotation=12
)

ax.tick_params(axis="y", colors="white", labelsize=14)
ax.set_ylabel(
    "Promedio de goles por partido",
    color="white",
    fontsize=16
)

ax.set_ylim(
    0,
    max(
        grafico_goles["GF_por_partido"].max(),
        grafico_goles["GC_por_partido"].max()
    ) + 0.45
)

ax.set_title(
    "GOLES A FAVOR Y EN CONTRA POR DT",
    color="white",
    fontsize=27,
    fontweight="bold",
    pad=25
)

ax.text(
    0.5,
    1.01,
    "Entrenadores de Gimnasia desde 2025 · mínimo 5 partidos",
    transform=ax.transAxes,
    ha="center",
    color="#77D3FF",
    fontsize=14
)

ax.legend(
    facecolor="#071E45",
    labelcolor="white",
    loc="upper right",
    fontsize=14
)

for borde in ax.spines.values():
    borde.set_visible(False)

ax.grid(axis="y", color="white", alpha=0.15)

fig.text(
    0.5,
    0.03,
    "GimnasiaData",
    ha="center",
    color="#77D3FF",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout(rect=[0, 0.06, 1, 0.95])

plt.savefig(
    "goles_por_dt.jpg",
    dpi=100,
    facecolor="#071E45"
)

plt.show()