# Drone Light Show 

## 📘 Resumen
Este repositorio contiene una simulación de un **show aéreo de drones** donde 40 drones forman secuencialmente tres figuras (robot → dragón → estrella) en un **bucle infinito**.  
Las figuras están definidas por **40 puntos cada una** (30 puntos de contorno + 10 de relleno) embebidos en el código — no se leen imágenes en tiempo de ejecución. La visualización es 3D (perspectiva) pero las formaciones son esencialmente 2D (plano XY) con ligera variación en Z para realismo.

---

## 🎯 Objetivos del proyecto
- Demostrar coordinación colectiva usando ideas inspiradas en **PSO (Particle Swarm Optimization)** orientadas a formar patrones visuales.  
- Generar animaciones suaves y estables evitando la convergencia masiva de los drones a un único punto.  
- Entregar un “playbook” reproducible sin dependencias de imágenes en ejecución (puntos embebidos).  
- Proveer un código fácil de ajustar para experimentar parámetros (número drones, distancia segura, velocidad, tiempos de fase).

---

## 🧠 Conceptos y diseño del algoritmo

### Representación
- **Dron** = partícula con estado `(x, y, z)` y velocidad `(vx, vy, vz)`.  
- **Figura** = conjunto de 40 objetivos `(x, y, z)` que describen contorno + relleno.  
- **Fases**:  
  - Objetivo activo (formar figura durante `T` frames)  
  - Reset (vuelan a posiciones base)  
  - Siguiente figura — ciclo infinito.

### Asignación de objetivos
- **greedy_unique_assign**: se calcula la matriz de distancias 2D entre drones y objetivos y se asigna de forma que cada objetivo quede con, idealmente, un dron (primero el dron con menor distancia mínima).  
- Alternativa sugerida: usar el **algoritmo húngaro** (`scipy.optimize.linear_sum_assignment`) para minimizar suma total de distancias (más óptimo pero requiere SciPy).

### Dinámica (PSO-like)
El paso por frame (simplificado) contiene:
1. **Cálculo del `desired`** para cada dron (su objetivo asignado).
2. **Término social**: atrae el dron hacia su objetivo — coeficiente `c2`.
3. **Término cognitivo**: en la versión simplificada usamos poca memoria cognitiva (podría ampliarse), coeficiente `c1`.
4. **Repulsión suave**: cuando dos drones están por debajo de `SAFE_DISTANCE * factor`, se aplica un empuje para separarlos (evita colisiones y apelotonamiento).
5. **Actualización de velocidad**: `v = w*v + c1*(pbest - pos) + c2*(desired - pos) + repulsion`
6. **Limitación de velocidad máxima (`MAX_SPEED`)**.
7. **Integración de posición**: `pos += v * DT`.

---

## 🧩 Formaciones implementadas

### 🐉 Dragón
Figura serpenteante generada con una curva sinusoidal en `x` y `y` con variación de altura.  
Se usa una onda `sin(t)`–`cos(t/2)` escalada para simular el cuerpo.  
Los 10 puntos de relleno agregan volumen central simulando alas o llamas.

### 🤖 Robot
Figura inspirada en un contorno tipo “robot clásico”: cuerpo rectangular, cabeza y extremidades definidas en coordenadas paramétricas.  
Contorno con 30 puntos equiespaciados y relleno centrado para densidad visual.  
Se añadieron proporciones basadas en el ejemplo de referencia (ancho:alto ≈ 1:0.6).

### ⭐ Estrella
Generada mediante coordenadas polares con radio alternante (estrella de 5 puntas).  
Contorno: vértices exteriores e interiores.  
Relleno: puntos en la región central.

![Primer intento](https://github.com/RogueOne-22/Laboratorio_4/blob/c9423d81fc051df091b791b50ca72f1fa5f7ae2a/Punto%201%20Emjambre/drone_show.gif)



https://github.com/user-attachments/assets/0c0428ee-757e-4494-92d9-a328edd38a60



---

## 🎨 Visualización

- Se usa `matplotlib` con proyección `3d`.  
- Cada dron es un punto sólido (sin líneas) del **mismo color** para uniformidad.  
- Las figuras se alternan automáticamente cada `T` iteraciones.  
- El eje `Z` tiene leve variación aleatoria para simular profundidad.  

**Parámetros clave de visualización:**
| Parámetro | Descripción | Valor por defecto |
|------------|--------------|-------------------|
| `N_DRONES` | Número de drones simulados | 40 |
| `SAFE_DISTANCE` | Distancia mínima entre drones | 5.0 |
| `MAX_SPEED` | Velocidad máxima de un dron | 40.0 |
| `MAX_ITER_PER_FORM` | Iteraciones por figura | 150 |
| `FIGURE_HOLD` | Frames que mantiene la figura | 60 |
| `DT` | Paso temporal de integración | 1.0 |

---

## ⚙️ Ciclo principal

```python
for name, targets in formations:
    swarm.reset_personal_bests()
    for i in range(MAX_ITER_PER_FORM):
        fit = swarm.step(targets)
    for _ in range(FIGURE_HOLD):
        swarm.history.append(swarm.positions.copy())
```

Cada figura ejecuta su propio bloque de iteraciones PSO.  
Se guarda el historial de posiciones para animación posterior.  
Al finalizar, el enjambre **no se reinicia al origen** sino que continúa desde su última posición (transición natural).

---

## 🧮 Fitness Function
El `fitness_formation()` mide:
1. **Proximidad a los objetivos** — drones cercanos obtienen mayor score.  
2. **Penalización por colisión** — si dos drones están muy cerca (`< SAFE_DISTANCE`), se resta puntaje.  
3. **Penalización por obstáculos** — si están dentro de un radio de obstáculo (solo si están habilitados).  
4. **Costo energético** — penaliza velocidades altas (menor consumo = mejor).  

El fitness guía la actualización del enjambre, priorizando formaciones precisas y seguras.


---

## 🚀 Mejoras implementadas
✅ Se corrigió la convergencia de drones a un solo punto.  
✅ Se añadió interpolación suave entre figuras.  
✅ Se amplió la densidad de puntos (40 drones).  
✅ Se eliminó el uso de imágenes externas — las figuras se generan algorítmicamente.  
✅ Se ajustaron las proporciones del robot y la estrella para mayor fidelidad visual.  
✅ Se simplificó la visualización (puntos sólidos del mismo color).  

---

## 💡 Posibles mejoras futuras
1. **Formaciones personalizadas:** permitir al usuario definir nuevas figuras desde coordenadas o imágenes vectoriales.  
2. **Interpolación 3D real:** transiciones con trayectorias curvas en lugar de lineales.  
3. **Simulación física realista:** incorporar gravedad, viento, y control PID.  
4. **Diferenciación visual:** colores o intensidades variables para crear degradados o secciones temáticas.  
5. **Coreografías dinámicas:** movimientos sincronizados en secuencia o con música.  
6. **Optimización global:** reemplazar el método “greedy” por el algoritmo húngaro para mejor asignación entre drones y objetivos.

---

## 🎥 Resultado
 - La animación muestra un grupo de **40 drones** desplazándose coordinadamente para recrear tres figuras distintas.  
 - Cada figura se mantiene visible unos segundos antes de transformarse suavemente en la siguiente, sin colisiones ni acumulaciones.
 


