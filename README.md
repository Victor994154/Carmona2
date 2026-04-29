# MINI AGENTE LÓGICO PARA LA ASIGNACIÓN

Integrantes: 
- Juan Sebastián Chitiva Guerrero
- Paulina Godínez Mendoza
- Víctor Yael Méndez Alcántara

## Descripción

Webapp construida con Streamlit que implementa un mini agente lógico basado en lógica de primer orden (FOL). El sistema razona sobre disponibilidad de espacios físicos (aulas, biblioteca, sala de reuniones, auditorio) para asignar y recomendar espacios según el tipo de solicitud, mostrando la traza de inferencia completa.
El agente no usa búsqueda heurística ni ML — toda decisión se deriva mediante encadenamiento hacia adelante (forward chaining) sobre una base de conocimiento explícita.


## DISEÑO DE KB_V2
### Reglas nuevas

### Casos nuevos
Caso 1 - EstudioIndividual en h1
Caso 2 - ReunionEquipo en h2
Caso 3 - Presentacion en h2
Caso 4 - PresentacionGrande en h3
Caso 5 - ReunionAccesible en h2
Caso 6 - Presentacion con preferencia centrica
Caso 7 - ReunionAccesible en h2 (enfoque accesibilidad)
Caso 8 - Presentacion con preferencia centrica
Caso 9 - EstudioIndividual evitando colaborativos
Caso 10 - PresentacionGrande optimizada
Caso 11 - ReunionAccesible en h1 (menos opciones)



## ¿Cómo funciona?
Representación del conocimiento
El dominio se modela con hechos (tuplas) y reglas de producción:

# Hechos — estado del mundo
("Libre", "AulaA", "h1")        # AulaA está libre en h1
("Silenciosa", "Biblio1")        # Biblio1 es silenciosa
("TieneProyector", "AulaA")      # AulaA tiene proyector

# Regla — si antecedentes → consecuente
Rule(
    antecedents=(("EstudioIndividual", "?g"),),
    consequent=("RequiereSilencio", "?g"),
)



## Forward Chaining

El motor aplica reglas iterativamente hasta alcanzar el punto fijo . Cada paso queda registrado en la traza de inferencia visible en la app.

## Flujo de una solicitud

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



## 🗃️ KB V1 vs KB V2

| Dimensión | KB V1 | KB V2 |
|-----------|-------|-------|
| Hechos base | 32 | 36 (+4 propiedades) |
| Reglas | 8 (R1–R8) | 16 (R1–R21) |
| Tipos de solicitud | 4 | 5 (+`ReunionAccesible`) |
| Predicados derivados | `Asignable`, `Recomendable` | + `NecesitaAccesibilidad`, `AltamenteRecomendable`, `MenosIdeal` |
| Mostrado en la app | Asignables + Recomendables | + Altamente recomendables + Menos ideales |
| Caso `ReunionAccesible` | ❌ No resuelto | ✅ Resuelto en 3 rondas |

## CASOS DE PRUEBA

## COMPARACIÓN DE RESULTADOS




## Estructura del proyecto


├── app.py          # Interfaz Streamlit principal
├── engine.py       # Motor de inferencia (forward chaining)
├── kb_v1.py        # Base de conocimiento versión 1 (base)
├── kb_v2.py        # Base de conocimiento versión 2 (extendida)
├── viz.py          # Visualizaciones y dataframes
├── cases.py        # Casos de prueba automáticos
├── README.md


## Subcompetencias demostradas

- SMA0402A — Reconocimiento de patrones, lenguaje natural e IA
- SEG0303A — Efectividad en la negociación
