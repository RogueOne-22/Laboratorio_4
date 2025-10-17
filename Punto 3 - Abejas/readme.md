# 🐝 Simulación de Polinización con Enjambre de Abejas (Optimización Swarm)

## 🌼 Descripción 

Este proyecto implementa una **simulación 2D de un enjambre de abejas** (o drones) en un invernadero con el objetivo de **optimizar la polinización** de flores mediante un enfoque inspirado en el **algoritmo de enjambre de abejas (Bee Colony Optimization)**.

Cada abeja representa un agente autónomo con comportamiento diferenciado y batería limitada.  
El objetivo del sistema es **maximizar la cobertura de polinización en el menor tiempo posible**, equilibrando el consumo de energía, el tiempo de vuelo y la colaboración entre tipos de abejas.

---

## 🎯 Objetivo

- Simular un enjambre inteligente de **drones/abejas** que cubra completamente un campo de flores.  
- Implementar roles de abejas:
  - **Exploradoras 🟡**: buscan nuevas flores y puntos potenciales de polinización.  
  - **Obreras 🔵**: polinizan flores activamente y priorizan las no polinizadas.  
  - **Observadoras 🔴**: permanecen cerca del panal, monitoreando la actividad general.  
- Incorporar una **gestión energética realista** con desgaste y recarga automática de batería.  
- Visualizar la simulación en **tiempo real 2D** mostrando el progreso, estado del enjambre y estadísticas.

---

## ⚙️ Características Principales

| Elemento | Descripción |
|-----------|-------------|
| 🌍 **Entorno** | Espacio bidimensional (100x100 unidades) con una base central (panal) y flores distribuidas aleatoriamente. |
| 🐝 **Tipos de abejas** | Exploradoras, obreras y observadoras, con comportamientos de búsqueda y movimiento diferenciados. |
| 🔋 **Gestión de energía** | Cada abeja tiene una batería que se consume con el movimiento y se recarga automáticamente al volver a la base. |
| 🌸 **Polinización** | Las flores se consideran polinizadas cuando una abeja entra en un radio cercano; su color cambia en la visualización. |
| ⏱️ **Panel de estado** | En la parte inferior de la animación se muestra: tiempo, flores polinizadas, fitness global, batería promedio y estado del enjambre. |
| 🔁 **Reinicio automático** | Cuando todas las flores son polinizadas, el enjambre se detiene 3 segundos y reinicia la simulación desde cero. |
| 🎨 **Visualización interactiva** | Animación continua con etiquetas y colores por tipo de abeja, y flores que cambian de color al ser polinizadas. |

---

## 🧠 Evolución del Proyecto

### 🥇 **Versión Inicial**
- Simulación básica con movimiento aleatorio.
- No existía diferenciación entre tipos de abejas.
- Sin recarga de batería ni verificación de flores polinizadas.
- La animación no mostraba métricas ni estado global.

### 🥈 **Versión Intermedia**
- Se introdujeron **roles de abejas** (exploradoras, obreras y observadoras).
- Se implementó la **detección de polinización** (flores cambian de color).
- Se añadió una **función de fitness global** basada en la cobertura.
- Se corrigió un bug que impedía la actualización visual (uso correcto de `FuncAnimation`).
- Se optimizó la lógica de movimiento hacia flores no polinizadas.

### 🥇 **Versión Final**
- Visualización completamente en **2D con panel informativo dinámico**.  
- Se agregó un **panel inferior** que muestra métricas en tiempo real:
  - Tiempo transcurrido  
  - Flores polinizadas  
  - Fitness global  
  - Batería promedio  
  - Estado del enjambre  
- Se incluyó **recarga automática** al llegar al panal.  
- Se implementó **reinicio automático** de la simulación tras completar toda la polinización.  
- Se ajustaron los valores de batería para obligar a varias recargas durante la simulación, haciendo el comportamiento más realista.  
- Se mejoró la organización visual con **colores, etiquetas y forma del panal en el centro del mapa**.
---

## 📊 Métricas en Tiempo Real

Durante la simulación podrás ver en la parte inferior:

- ⏱️ Tiempo transcurrido (segundos desde el inicio)  
- 🌼 Flores polinizadas (conteo y total)  
- 💪 Fitness global (% de polinización completada)  
- 🔋 Batería promedio (% de energía restante en el enjambre)  
- 🐝 Estado del enjambre (polinizando, recargando o reiniciando)

---

## 🔮 Posibles Mejoras Futuras

- Implementar **algoritmo de optimización de enjambre real** (Bee Colony Optimization formal).  
- Agregar un modelo 3D con vuelo vertical y trayectorias suaves.  
- Incorporar **interfaz gráfica interactiva (GUI)** con botones de pausa y reinicio.  
- Introducir **obstáculos o zonas prohibidas** dentro del invernadero.  
- Simular **flujo de néctar** y **tiempo de floración** como variables dinámicas.  
- Integrar **gráficos de rendimiento histórico** por iteración (fitness vs tiempo).  

---

## 📸 Resultado

Ejemplo del entorno generado:

///insertar video

```
🐝 Simulación de Polinización con Enjambre de Abejas
---------------------------------------------------
🟡 Exploradoras | 🔵 Obreras | 🔴 Observadoras | 🍯 Panal (Centro)
Flores 🌸 cambian de color al ser polinizadas
Panel inferior: muestra tiempo, batería, fitness y progreso global
```

---

## 👩‍💻 Autor **Paula S**  

