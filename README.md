#  Mini Agente Lógico para la Asignación de Espacios

**Integrantes:**
- Juan Sebastián Chitiva Guerrero
- Paulina Godínez Mendoza
- Víctor Yael Méndez Alcántara · A01368475

> Proyecto para **Inteligencia Artificial (SMA0402A)** — Tecnológico de Monterrey · Semestre Ene–Jun 2026

---

##  Descripción

Webapp construida con **Streamlit** que implementa un mini agente lógico basado en **lógica de primer orden (FOL)**. El sistema razona sobre disponibilidad de espacios físicos (aulas, biblioteca, sala de reuniones, auditorio) para asignar y recomendar espacios según el tipo de solicitud, mostrando la traza de inferencia completa.

El agente no usa búsqueda heurística ni ML — toda decisión se deriva mediante **encadenamiento hacia adelante (forward chaining)** sobre una base de conocimiento explícita.

---

##  Diseño de KB V2

### Reglas nuevas

| Regla | Descripción |
|-------|-------------|
| R9  | `ReunionAccesible(g)` → `ReunionEquipo(g)` |
| R10 | `ReunionAccesible(g)` → `NecesitaAccesibilidad(g)` |
| R11 | `Asignable(s,g,t)` ∧ `NecesitaAccesibilidad(g)` ∧ `Accesible(s)` → `Recomendable(s,g,t)` |
| R12 | `Asignable(s,g,t)` ∧ `Presentacion(g)` ∧ `Centrico(s)` → `Recomendable(s,g,t)` |
| R14 | `Asignable(s,g,t)` ∧ `EstudioIndividual(g)` ∧ `Silenciosa(s)` → `Recomendable(s,g,t)` |
| R16 | `Asignable(s,g,t)` ∧ `ReunionEquipo(g)` ∧ `Colaborativo(s)` → `Recomendable(s,g,t)` |
| R17 | `Asignable(s,g,t)` ∧ `PresentacionGrande(g)` ∧ `CapacidadAlta(s)` → `Recomendable(s,g,t)` |
| R19 | `Recomendable(s,g,t)` ∧ `NecesitaAccesibilidad(g)` ∧ `Accesible(s)` → `AltamenteRecomendable(s,g,t)` |
| R20 | `Asignable(s,g,t)` ∧ `EstudioIndividual(g)` ∧ `Colaborativo(s)` → `MenosIdeal(s,g,t)` |

### Casos de prueba

| # | Caso | Slot | Tipo |
|---|------|------|------|
| 1  | EstudioIndividual en h1 | h1 | `EstudioIndividual` |
| 2  | ReunionEquipo en h2 | h2 | `ReunionEquipo` |
| 3  | Presentacion en h2 | h2 | `Presentacion` |
| 4  | PresentacionGrande en h3 | h3 | `PresentacionGrande` |
| 5  | ReunionAccesible en h2 | h2 | `ReunionAccesible` |
| 6  | ReunionAccesible en h3 | h3 | `ReunionAccesible` |
| 7  | ReunionAccesible en h4 | h4 | `ReunionAccesible` |
| 8  | ReunionAccesible en h1 | h1 | `ReunionAccesible` |
| 9  | Presentacion en h3 (céntrico) | h3 | `Presentacion` |
| 10 | Presentacion en h4 (céntrico) | h4 | `Presentacion` |
| 11 | ReunionEquipo en h3 (colaborativo) | h3 | `ReunionEquipo` |

---

##  ¿Cómo funciona?

### Representación del conocimiento

El dominio se modela con **hechos** (tuplas) y **reglas** de producción:

```python
# Hechos — estado del mundo
("Libre", "AulaA", "h1")        # AulaA está libre en h1
("Silenciosa", "Biblio1")        # Biblio1 es silenciosa
("TieneProyector", "AulaA")      # AulaA tiene proyector

# Regla — si antecedentes → consecuente
Rule(
    antecedents=(("EstudioIndividual", "?g"),),
    consequent=("RequiereSilencio", "?g"),
)
```

### Forward Chaining

El motor aplica reglas iterativamente hasta alcanzar el **punto fijo** (no se derivan hechos nuevos). Cada paso queda registrado en la **traza de inferencia** visible en la app.

### Flujo de una solicitud

```
Usuario ingresa solicitud (tipo + franja)
        ↓
Se agregan hechos transitorios: Solicita(g, t) + TipoSolicitud(g)
        ↓
Forward chaining sobre KB + hechos nuevos
        ↓
Se derivan:
  • Asignable(s, g, t)             → espacios que cumplen los requisitos
  • Recomendable(s, g, t)          → espacios con propiedades favorables
  • AltamenteRecomendable(s, g, t) → prioridad máxima (solo KB V2)
  • MenosIdeal(s, g, t)            → espacios con propiedades desfavorables (solo KB V2)
        ↓
Usuario reserva → KB se actualiza (Libre → Ocupada)
```

---

##  KB V1 vs KB V2

| Dimensión | KB V1 | KB V2 |
|-----------|-------|-------|
| Hechos base | 32 | 36 (+4 propiedades) |
| Reglas | 8 (R1–R8) | 16 (R1–R21) |
| Tipos de solicitud | 4 | 5 (`+ReunionAccesible`) |
| Predicados derivados | `Asignable`, `Recomendable` | + `NecesitaAccesibilidad`, `AltamenteRecomendable`, `MenosIdeal` |
| Mostrado en la app | Asignables + Recomendables | + Altamente recomendables + Menos ideales |
| Caso `ReunionAccesible` | ❌ No resuelto | ✅ Resuelto en 3 rondas |

**KB V2** habilita inferencia en cadena:
`ReunionAccesible → ReunionEquipo → RequiereColaboracion → Asignable → Recomendable → AltamenteRecomendable`

---

##  Espacios disponibles

| Espacio | Silenciosa | Colaborativo | Proyector | Cap. Alta | Accesible* | Céntrico* |
|---------|:----------:|:------------:|:---------:|:---------:|:----------:|:---------:|
| AulaA         |    | ✓ | ✓ |   | ✓ | ✓ |
| AulaB         | ✓  |   |   |   |   |   |
| Biblio1       | ✓  |   |   |   |   |   |
| SalaReuniones |    | ✓ | ✓ |   | ✓ | ✓ |
| AuditorioMini |    |   | ✓ | ✓ |   |   |

> \* Propiedades nuevas introducidas en KB V2.

---

##  Comparación de resultados

| Casos | KB V1 asignables | KB V2 asignables |
|-------|:----------------:|:----------------:|
| Casos 1–4 (tipos base) | 1–2 | 1–2 (igual) |
| Casos 5–8 (`ReunionAccesible`) | **0** | **1–2** |
| Casos 9–11 (franjas distintas) | 1–3 | 1–3 + más recomendables |

Los casos 5–8 son los que hacen visible la diferencia en la gráfica de la app: KB V1 no tiene reglas para `ReunionAccesible`, por lo que devuelve 0 asignables.

---

##  Estructura del proyecto

```
.
├── app.py        # Interfaz Streamlit principal
├── engine.py     # Motor de inferencia (forward chaining)
├── kb_v1.py      # Base de conocimiento versión 1 (base)
├── kb_v2.py      # Base de conocimiento versión 2 (extendida)
├── viz.py        # Visualizaciones y dataframes
├── cases.py      # Casos de prueba automáticos
├── README.md
└── reporte.pdf   # Documento de comprensión del sistema
```

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

# 2. Instalar dependencias
pip install streamlit

# 3. Correr la app
streamlit run app.py
```

> **Requisito:** Python 3.9+

---

##  Subcompetencias demostradas

- **SMA0402A** — Reconocimiento de patrones, lenguaje natural e IA
- **SEG0303A** — Efectividad en la negociación
