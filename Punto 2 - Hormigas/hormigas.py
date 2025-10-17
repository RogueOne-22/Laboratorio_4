import numpy as np
import matplotlib.pyplot as plt
import random
from math import sqrt
from typing import List, Tuple, Dict

# Parámetros del algoritmo
N_DRONES = 5
N_PUNTOS = 30
N_ITERACIONES = 100
EVAPORACION = 0.5
ALPHA = 1.0
BETA = 2.0
Q = 100

class Punto:
    def __init__(self, id: int, x: float, y: float, tipo: str):
        self.id = id
        self.x = x
        self.y = y
        self.tipo = tipo  # 'superviviente' o 'recurso'

class Drone:
    def __init__(self, id: int):
        self.id = id
        self.ruta = []
        self.distancia_recorrida = 0.0
        self.puntos_visitados = set()

class ACORescate:
    def __init__(self, ancho: float, alto: float):
        self.ancho = ancho
        self.alto = alto
        self.puntos = []
        self.feromonas = {}
        self.drones = [Drone(i) for i in range(N_DRONES)]
        self.mejor_ruta_global = None
        self.mejor_distancia_global = float('inf')
        self.historial_metricas = []
        
    def generar_terreno(self):
        """Genera puntos aleatorios de supervivientes y recursos"""
        self.puntos = []
        for i in range(N_PUNTOS):
            x = random.uniform(0, self.ancho)
            y = random.uniform(0, self.alto)
            tipo = 'superviviente' if random.random() > 0.3 else 'recurso'
            self.puntos.append(Punto(i, x, y, tipo))
            
        # Inicializar matriz de feromonas
        for i in range(len(self.puntos)):
            for j in range(i+1, len(self.puntos)):
                self.feromonas[(i,j)] = 1.0
                self.feromonas[(j,i)] = 1.0

    def distancia(self, p1: Punto, p2: Punto) -> float:
        """Calcula distancia euclidiana entre dos puntos"""
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def calcular_probabilidades(self, punto_actual: Punto, drones: Drone) -> List[float]:
        """Calcula probabilidades de transición a otros puntos"""
        probabilidades = []
        puntos_no_visitados = [p for p in self.puntos if p.id not in drones.puntos_visitados]
        
        if not puntos_no_visitados:
            return []
            
        for punto in puntos_no_visitados:
            feromona = self.feromonas.get((punto_actual.id, punto.id), 1.0)
            distancia = self.distancia(punto_actual, punto)
            atraccion = (feromona ** ALPHA) * ((1.0/distancia) ** BETA)
            probabilidades.append(atraccion)
            
        total = sum(probabilidades)
        return [p/total for p in probabilidades] if total > 0 else [1.0/len(probabilidades)]*len(probabilidades)

    def explorar_ruta(self, drone: Drone):
        """Explora una ruta para un drone"""
        punto_actual = random.choice(self.puntos)
        drone.ruta = [punto_actual]
        drone.puntos_visitados = {punto_actual.id}
        drone.distancia_recorrida = 0.0
        
        while len(drone.puntos_visitados) < len(self.puntos):
            puntos_no_visitados = [p for p in self.puntos if p.id not in drone.puntos_visitados]
            if not puntos_no_visitados:
                break
                
            probabilidades = self.calcular_probabilidades(punto_actual, drone)
            
            if probabilidades:
                siguiente_punto = random.choices(puntos_no_visitados, weights=probabilidades)[0]
                drone.distancia_recorrida += self.distancia(punto_actual, siguiente_punto)
                drone.ruta.append(siguiente_punto)
                drone.puntos_visitados.add(siguiente_punto.id)
                punto_actual = siguiente_punto

    def actualizar_feromonas(self):
        """Actualiza feromonas basado en las rutas encontradas"""
        # Evaporación
        for key in self.feromonas:
            self.feromonas[key] *= (1.0 - EVAPORACION)
            
        # Depositar feromonas
        for drone in self.drones:
            for i in range(len(drone.ruta)-1):
                p1, p2 = drone.ruta[i], drone.ruta[i+1]
                key = (p1.id, p2.id)
                self.feromonas[key] += Q / drone.distancia_recorrida
                self.feromonas[(key[1], key[0])] += Q / drone.distancia_recorrida

    def introducir_cambio(self):
        """Introduce cambios en el terreno (nuevos escombros)"""
        if len(self.puntos) < N_PUNTOS * 1.5:  # Límite máximo de puntos
            # Agregar nuevo punto (simulando nuevo descubrimiento)
            x = random.uniform(0, self.ancho)
            y = random.uniform(0, self.alto)
            nuevo_punto = Punto(len(self.puntos), x, y, 
                               'superviviente' if random.random() > 0.5 else 'recurso')
            self.puntos.append(nuevo_punto)
            
            # Inicializar feromonas para el nuevo punto
            for i in range(len(self.puntos)-1):
                self.feromonas[(i, nuevo_punto.id)] = 1.0
                self.feromonas[(nuevo_punto.id, i)] = 1.0

    def calcular_metricas(self, iteracion: int):
        """Calcula métricas de desempeño"""
        total_puntos = len(self.puntos)
        puntos_cubiertos = set()
        tiempo_maximo = 0
        
        for drone in self.drones:
            puntos_cubiertos.update(drone.puntos_visitados)
            if drone.distancia_recorrida > tiempo_maximo:
                tiempo_maximo = drone.distancia_recorrida
                
        cobertura = len(puntos_cubiertos) / total_puntos * 100
        
        # Encontrar mejor ruta global
        for drone in self.drones:
            if drone.distancia_recorrida < self.mejor_distancia_global:
                self.mejor_distancia_global = drone.distancia_recorrida
                self.mejor_ruta_global = drone.ruta.copy()
                
        metricas = {
            'iteracion': iteracion,
            'cobertura': cobertura,
            'tiempo_total': tiempo_maximo,
            'mejor_distancia': self.mejor_distancia_global,
            'total_puntos': total_puntos
        }
        
        self.historial_metricas.append(metricas)
        return metricas

    def ejecutar_aco(self):
        """Ejecuta el algoritmo ACO completo"""
        self.generar_terreno()
        
        for iteracion in range(N_ITERACIONES):
            # Explorar rutas
            for drone in self.drones:
                self.explorar_ruta(drone)
                
            # Actualizar feromonas
            self.actualizar_feromonas()
            
            # Calcular métricas
            metricas = self.calcular_metricas(iteracion)
            
            # Introducir cambio cada 20 iteraciones
            if iteracion % 20 == 0 and iteracion > 0:
                self.introducir_cambio()
                print(f"Iteración {iteracion}: Cambio introducido - Nuevo punto agregado")
            
            print(f"Iteración {iteracion}: Cobertura {metricas['cobertura']:.1f}%, "
                  f"Tiempo: {metricas['tiempo_total']:.2f}, "
                  f"Mejor: {metricas['mejor_distancia']:.2f}")

    def visualizar_resultados(self):
        """Visualiza los resultados del algoritmo"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Visualizar terreno y rutas
        colores = {'superviviente': 'red', 'recurso': 'blue'}
        
        for punto in self.puntos:
            ax1.scatter(punto.x, punto.y, 
                       c=colores[punto.tipo], 
                       marker='o' if punto.tipo == 'superviviente' else 's',
                       s=100, label=punto.tipo)
            
        # Mostrar mejor ruta global
        if self.mejor_ruta_global:
            x_ruta = [p.x for p in self.mejor_ruta_global]
            y_ruta = [p.y for p in self.mejor_ruta_global]
            ax1.plot(x_ruta, y_ruta, 'g-', linewidth=2, alpha=0.7, label='Mejor ruta')
            
        ax1.set_xlim(0, self.ancho)
        ax1.set_ylim(0, self.alto)
        ax1.set_title('Terreno de Rescate y Rutas de Drones')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Visualizar métricas
        iteraciones = [m['iteracion'] for m in self.historial_metricas]
        cobertura = [m['cobertura'] for m in self.historial_metricas]
        tiempos = [m['tiempo_total'] for m in self.historial_metricas]
        
        ax2.plot(iteraciones, cobertura, 'b-', label='Cobertura (%)')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('Cobertura (%)', color='b')
        ax2.tick_params(axis='y', labelcolor='b')
        ax2.grid(True, alpha=0.3)
        
        ax2_twin = ax2.twinx()
        ax2_twin.plot(iteraciones, tiempos, 'r-', label='Tiempo total')
        ax2_twin.set_ylabel('Tiempo total', color='r')
        ax2_twin.tick_params(axis='y', labelcolor='r')
        
        ax2.set_title('Métricas de Optimización')
        ax2.legend(loc='upper left')
        ax2_twin.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()

# Ejecutar la simulación
if __name__ == "__main__":
    aco = ACORescate(ancho=100, alto=100)
    aco.ejecutar_aco()
    aco.visualizar_resultados()
    
    # Mostrar resumen final
    ultima_metrica = aco.historial_metricas[-1]
    print(f"\n--- RESULTADOS FINALES ---")
    print(f"Cobertura alcanzada: {ultima_metrica['cobertura']:.1f}%")
    print(f"Tiempo total de cobertura: {ultima_metrica['tiempo_total']:.2f}")
    print(f"Mejor distancia encontrada: {ultima_metrica['mejor_distancia']:.2f}")
    print(f"Total de puntos en el mapa: {ultima_metrica['total_puntos']}")