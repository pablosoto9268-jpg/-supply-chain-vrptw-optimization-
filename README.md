# 🚚 Vehicle Routing & Fleet Optimization with Time Windows (VRPTW)
> **Solución práctica en Python para la optimización de rutas de transporte y distribución en logística de trinchera.**

---

## 📌 El Criterio y el Problema Operativo

En la operación logística diaria (3PL / 4PL / Flota Propia), el ruteo manual o basado únicamente en la experiencia del operador suele generar:

1. **Ineficiencia en costos de transporte:** Kilometraje excedido por falta de consolidación geográfica de entregas.
2. **Rechazos y penalizaciones por OTIF:** Entregas fuera de la ventana de recepción acordada con el cliente (Retail / CEDIS / Cliente Final).
3. **Subutilización de la capacidad:** Unidades con espacio disponible mientras otras exceden su capacidad máxima permitida.

### 🎯 Objetivo del Proyecto
Desarrollar un modelo de optimización matemática en Python utilizando la librería **Google OR-Tools** para asignar y secuenciar automáticamente los pedidos a una flota heterogénea/homogénea de vehículos, minimizando el kilometraje total recorrido y asegurando el cumplimiento estricto de:
- **Capacidad de carga por unidad** (peso / volumen).
- **Ventanas de tiempo de recepción** en los nodos de entrega.
- **Horarios operativos del centro de distribución (DEPOT).**

---

## 🛠️ Tecnologías y Librerías Utilizadas

- **Python 3.10+**
- **Google OR-Tools (`ortools.constraint_solver`):** Motor de optimización de restricciones y ruteo de vehículos.
- **Pandas / NumPy:** Procesamiento, limpieza y estructuración del Dataset de pedidos.
- **Matplotlib / Seaborn:** Visualización de las rutas generadas y distribución de carga de flota.

---

## 📐 Estructura del Repositorio

```text
├── data/
│   └── mock_deliveries.csv     # Dataset con ubicaciones, demandas y ventanas de tiempo
├── src/
│   ├── vrp_optimization.py     # Script principal del modelo de optimización
│   └── utils.py                # Cálculo de matriz de distancias y formateo de datos
├── notebooks/
│   └── VRP_Analysis.ipynb      # Libreta explicativa paso a paso para análisis de negocio
├── README.md                   # Documentación técnica del proyecto
└── requirements.txt            # Dependencias del proyecto
