# 🧠 Sistema de Rescate con Drones usando Algoritmo ACO 
![Python](https://img.shields.io/badge/Python-3.7%2B-blue) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-orange) ![Numpy](https://img.shields.io/badge/Numpy-1.21%2B-green)

  Un sistema de optimización de rutas de rescate que utiliza el algoritmo de colonia de hormigas (ACO) para coordinar drones en la búsqueda de supervivientes y recursos en zonas de desastre.

## 📋 Descripción del Proyecto

* Este proyecto simula un escenario post-terremoto donde 10 drones (que actúan como hormigas en el algoritmo ACO) colaboran para encontrar supervivientes y recursos de manera eficiente.
--
## ✨ Características Principales
--
🤖 Algoritmo ACO Adaptado

    10 drones coordinados que actúan como hormigas

    Sistema de feromonas que se evapora y actualiza dinámicamente

    Función de fitness que minimiza el tiempo total de cobertura

    Probabilidades de transición basadas en feromonas y distancia

🗺️ Simulación de Terreno

    Puntos de interés aleatorios: supervivientes (70%) y recursos (30%)

    Cambios dinámicos: nuevos puntos aparecen cada 10 iteraciones

    Terreno adaptable de 100x100 unidades

    Métrica de cobertura en tiempo real

📊 Sistema de Visualización

    Animación en tiempo real del proceso de exploración

    Rastros de feromonas representados como puntos amarillos

    Efectos de estela en las rutas de los drones

    Múltiples paneles de métricas y resultados

# 🔧 Cambios y Mejoras Implementadas
  * Visualización de Feromonas como Puntos:
     Las feromonas ahora se representan como puntos discretos en lugar de nubes continuas, mejorando la claridad visual.
  
  * Tamaños de Elementos Optimizados:
     Drones (60px) y feromonas (3-15px) más pequeños para reducir superposición y mejorar la distribución espacial.
    
  * Efecto de Estela en Rutas  
     Implementación de rutas con efecto de estela que muestra la dirección y antigüedad del movimiento.
    
  *  Leyenda Unificada y Compacta
     Leyenda compacta con elementos más pequeños y solo los primeros 3 drones para evitar saturación.
     
  *  Representación Mejorada de la Mejor Ruta
     La mejor ruta global ahora se muestra con waypoints y flechas que indican dirección, facilitando el análisis.
--
## Parámetros configurables

Ejemplo de parámetros en el archivo principal (`aco_rescate_drones.py`):

```python
N_DRONES = 10           # Número de drones
N_PUNTOS = 30           # Puntos iniciales en el mapa
N_ITERACIONES = 50      # Iteraciones del algoritmo
EVAPORACION = 0.3       # Tasa de evaporación de feromonas
ALPHA = 1.0             # Peso de las feromonas
BETA = 2.0              # Peso de la distancia inversa
Q = 100                 # Constante de deposición
```

## 📈 Métricas y resultados

El sistema genera cuatro tipos de visualizaciones:

- Animación en tiempo real: muestra la exploración progresiva con feromonas y rutas
- Mapa final: terreno completo con la mejor ruta encontrada
- Evolución de métricas: cobertura (%) vs tiempo de operación
- Análisis por drone: cobertura individual y eficiencia de rutas

### Ejemplo de salida


https://github.com/user-attachments/assets/230e8a2f-f0f3-413f-bb9d-d51a76e6836e


<video controls src="https://github.com/RogueOne-22/Laboratorio_4/blob/c9423d81fc051df091b791b50ca72f1fa5f7ae2a/Punto%202%20-%20Hormigas/Grabaci%C3%B3n%20de%20pantalla%202025-10-17%20093909.mp4" title="Ejemplo final"></video>

![Ejemplo final](https://github.com/RogueOne-22/Laboratorio_4/blob/e4153f7811e72b6391f07868de00954c721a8a84/Punto%202%20-%20Hormigas/Grabaci%C3%B3n%20de%20pantalla%202025-10-17%20094746.mp4)

Luego de cerrar la simulación se genera una nueva imagen mosntrado el resumen.

![REsultados](https://github.com/RogueOne-22/Laboratorio_4/blob/c9423d81fc051df091b791b50ca72f1fa5f7ae2a/Punto%202%20-%20Hormigas/Captura%20de%20pantalla%202025-10-17%20095221.png)

```text
Iteración 25: Cobertura 76.7%, Tiempo: 145.32
Iteración 25: Nuevo punto descubierto!
...
--- RESULTADOS FINALES ---
Cobertura alcanzada: 92.3%
Tiempo total de cobertura: 183.45
Mejor distancia encontrada: 156.78
Total de puntos en el mapa: 34
```

## 🎨 Convenciones visuales

| Elemento        | Símbolo | Color   |
|----------------|:-------:|:-------:|
| Supervivientes | ●       | Rojo    |
| Recursos       | ■       | Azul    |
| Drones         | ▲       | Verde   |
| Feromonas      | •       | Amarillo|
| Mejor Ruta     | →       | Verde   |

## 🔄 Flujo del algoritmo

1. Inicialización: generar terreno y inicializar feromonas
2. Exploración: cada drone elige rutas basadas en probabilidades
3. Actualización: evaporar y depositar feromonas
4. Adaptación: introducir nuevos puntos de interés
5. Métricas: calcular cobertura y eficiencia
6. Visualización: actualizar animación y gráficas

## 💡 Aplicaciones prácticas

- Rescate en desastres: optimización de búsqueda en áreas extensas
- Logística: rutas de entrega y distribución
- Agricultura: monitoreo de cultivos con drones
- Vigilancia: cobertura eficiente de áreas de seguridad

## 🛠️ Posibles mejoras futuras

- Implementación de obstáculos dinámicos
- Drones con diferentes capacidades y velocidades
- Comunicación directa entre drones
- Optimización multi-objetivo
- Integración con datos GIS reales
