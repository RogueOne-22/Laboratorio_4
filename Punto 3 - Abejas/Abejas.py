import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

# -------------------- PARÁMETROS --------------------
NUM_DRONES = 40
NUM_FLORES = 80
RANGO = 100
BASE = np.array([RANGO / 2, RANGO / 2])
VELOCIDAD = 1.5
BATERIA_MAX = 80  # batería corta
RECARGA_TIEMPO = 30
RADIO_POLINIZACION = 2.0
INTERVALO_MS = 100

# -------------------- INICIALIZACIÓN --------------------
def inicializar_escenario():
    flores = np.random.rand(NUM_FLORES, 2) * RANGO
    madurez = np.random.rand(NUM_FLORES)
    polinizadas = np.zeros(NUM_FLORES, dtype=bool)

    tipos = ["obrera", "observadora", "exploradora"]
    colores = {"obrera": "orange", "observadora": "cyan", "exploradora": "magenta"}
    formas = {"obrera": "o", "observadora": "^", "exploradora": "s"}

    drones = [{
        "pos": BASE.copy(),
        "tipo": random.choice(tipos),
        "bateria": random.uniform(BATERIA_MAX * 0.5, BATERIA_MAX),
        "objetivo": random.randint(0, NUM_FLORES - 1),
        "estado": "buscando"
    } for _ in range(NUM_DRONES)]

    return flores, madurez, polinizadas, drones, colores, formas

flores, madurez, polinizadas, drones, colores, formas = inicializar_escenario()
inicio_tiempo = time.time()
ciclo_actual = 1  # contador de ciclos

# -------------------- CONFIGURAR FIGURA --------------------
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, RANGO)
ax.set_ylim(0, RANGO)
ax.set_title("🐝 Simulación de Polinización con Enjambre de Abejas (2D)")

# Base (panal)
ax.plot(BASE[0], BASE[1], "s", color="brown", markersize=10, label="Panal")

# Puntos de flores
sc_flores = ax.scatter(flores[:, 0], flores[:, 1], c='green', s=30, label="Flores")

# Drones
sc_drones = ax.scatter([], [], c=[], s=60, marker="o")

# Texto de información inferior
texto_info = ax.text(0.02, -0.08, "", transform=ax.transAxes, fontsize=10, va='top')

# Leyenda: Panal, Flores y roles de drones
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='s', color='w', markerfacecolor='brown', markersize=10, label='Panal'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Flor (no polinizada)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores['obrera'], markersize=8, label='Obrera'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores['observadora'], markersize=8, label='Observadora'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores['exploradora'], markersize=8, label='Exploradora')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.9)

# -------------------- FUNCIONES --------------------
def actualizar_drones():
    global polinizadas
    for d in drones:
        if d["estado"] == "recargando":
            d["bateria"] += 1
            if d["bateria"] >= BATERIA_MAX:
                d["estado"] = "buscando"
                d["objetivo"] = random.randint(0, NUM_FLORES - 1)
            continue

        if d["bateria"] <= 0:
            d["estado"] = "regresando"
            continue

        objetivo = flores[d["objetivo"]]
        direccion = objetivo - d["pos"]
        distancia = np.linalg.norm(direccion)

        if distancia < RADIO_POLINIZACION:
            if not polinizadas[d["objetivo"]]:
                polinizadas[d["objetivo"]] = True
            d["objetivo"] = random.randint(0, NUM_FLORES - 1)

        if d["estado"] in ["buscando", "explorando"]:
            if distancia > 0:
                d["pos"] += (direccion / distancia) * VELOCIDAD
                d["bateria"] -= 1

        if d["bateria"] < 10:
            d["estado"] = "regresando"

        if d["estado"] == "regresando":
            dir_base = BASE - d["pos"]
            dist_base = np.linalg.norm(dir_base)
            if dist_base > 1:
                d["pos"] += (dir_base / dist_base) * VELOCIDAD
            else:
                d["estado"] = "recargando"

def fitness_global():
    return np.sum(polinizadas) / NUM_FLORES

def bateria_promedio():
    return np.mean([d["bateria"] for d in drones])

def reiniciar_simulacion():
    global flores, madurez, polinizadas, drones, inicio_tiempo, ciclo_actual
    flores, madurez, polinizadas, drones, _, _ = inicializar_escenario()
    inicio_tiempo = time.time()
    ciclo_actual += 1

# -------------------- ACTUALIZACIÓN DE ANIMACIÓN --------------------
def actualizar(frame):
    global inicio_tiempo
    actualizar_drones()
    posiciones = np.array([d["pos"] for d in drones])
    colores_drones = [colores[d["tipo"]] for d in drones]

    sc_flores.set_facecolor(['yellow' if p else 'green' for p in polinizadas])
    sc_drones.set_offsets(posiciones)
    sc_drones.set_color(colores_drones)

    # Estadísticas
    tiempo_actual = time.time() - inicio_tiempo
    flores_polinizadas = np.sum(polinizadas)
    fit = fitness_global() * 100
    bateria_avg = bateria_promedio()
    estado_enjambre = "Completado" if flores_polinizadas == NUM_FLORES else "Polinizando"

    texto_info.set_text(
        f"🔁 Ciclo: {ciclo_actual}   ⏱ Tiempo: {tiempo_actual:.1f}s   🌸 Flores: {flores_polinizadas}/{NUM_FLORES}   "
        f"🏋️ Fitness: {fit:.1f}%   🔋 Batería Promedio: {bateria_avg:.1f}%   🐝 Estado: {estado_enjambre}"
    )

    # Si termina, reinicia después de 3 segundos
    if flores_polinizadas == NUM_FLORES:
        plt.pause(3)
        reiniciar_simulacion()

    return sc_drones, sc_flores, texto_info

# -------------------- ANIMACIÓN --------------------
ani = animation.FuncAnimation(fig, actualizar, interval=INTERVALO_MS)
plt.subplots_adjust(bottom=0.15)
plt.show()
