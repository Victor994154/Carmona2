from __future__ import annotations

from engine import Rule
from kb_v1 import BASE_FACTS as V1_BASE_FACTS
from kb_v1 import REQUEST_TYPES as V1_REQUEST_TYPES
from kb_v1 import RULES as V1_RULES
from kb_v1 import SLOTS, SPACES


TITLE = "KB V2 - plantilla para extender V1"

# Esta lista ya incluye el nuevo tipo de solicitud para que la app lo muestre.
REQUEST_TYPES = list(V1_REQUEST_TYPES) + ["ReunionAccesible"]

# -------------------------------------------------------------------
# TODO:
# Agrega aquí los nuevos hechos de V2.
# Sugerencia mínima:
#("Accesible", "AulaA")
#("Accesible", "SalaReuniones")
#("Centrico", "AulaA")
#("Centrico", "SalaReuniones")
# -------------------------------------------------------------------
EXTRA_FACTS = {
    # Ejemplo:
    #Propiedades extra de espacios
    ("Accesible", "AulaA"),
    ("Accesible", "SalaReuniones"),
    ("Centrico", "AulaA"),
    ("Centrico", "SalaReuniones"),
}

# -------------------------------------------------------------------
# TODO:
# Agrega aquí las nuevas reglas de V2.
#
# Sugerencias mínimas:

# 1) ReunionAccesible(g) ==> ReunionEquipo(g) ----- LISTO R9
# 2) ReunionAccesible(g) ==> NecesitaAccesibilidad(g)
# 3) Asignable(s,g,t) & NecesitaAccesibilidad(g) & Accesible(s) ==> Recomendable(s,g,t)
# 4) Asignable(s,g,t) & Presentacion(g) & Centrico(s) ==> Recomendable(s,g,t)
# -------------------------------------------------------------------
EXTRA_RULES = [
    Rule(
    name="R9_reunion_accesible_es_reunion",
    antecedents=(("ReunionAccesible", "?g"),),
    consequent=("ReunionEquipo", "?g"),
    description="Una reunión accesible también es una reunión de equipo.",
    ),
    Rule(
        name="R10_reunion_necesita_accesibilidad",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("NecesitaAccesibilidad", "?g"),
        description="Una reunión accesible requiere accesibilidad.",
    ),

    Rule(
        name="R11_recomendar_accesible",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("NecesitaAccesibilidad", "?g"),
            ("Accesible", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Si necesita accesibilidad, recomendar espacios accesibles.",
    ),
    Rule(
        name="R12_recomendar_centrico_presentacion",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("Presentacion", "?g"),
            ("Centrico", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Para presentaciones, preferir espacios céntricos.",
    ),
    #Rule(
    #name="R13_no_recomendar_no_accesible",
    #antecedents=(
        #("Asignable", "?s", "?g", "?t"),
        #("NecesitaAccesibilidad", "?g"),
    #),
    #consequent=("NoIdeal", "?s", "?g", "?t"),
    #description="Espacios no accesibles no son ideales.",
    #),
    Rule(
    name="R14_priorizar_silencio",
    antecedents=(
        ("Asignable", "?s", "?g", "?t"),
        ("EstudioIndividual", "?g"),
        ("Silenciosa", "?s"),
    ),
    consequent=("Recomendable", "?s", "?g", "?t"),
    ),
    #Rule(
    #name="R15_no_recomendar_sin_proyector",
    #antecedents=(
        #("Asignable", "?s", "?g", "?t"),
        #("Presentacion", "?g"),
    #),
    #consequent=("MenosIdeal", "?s", "?g", "?t"),
    #),
    Rule(
    name="R16_priorizar_colaborativo_reunion",
    antecedents=(
        ("Asignable", "?s", "?g", "?t"),
        ("ReunionEquipo", "?g"),
        ("Colaborativo", "?s"),
    ),
    consequent=("Recomendable", "?s", "?g", "?t"),
    description="Para reuniones, preferir espacios colaborativos.",
),
    Rule(
    name="R17_priorizar_capacidad_presentacion_grande",
    antecedents=(
        ("Asignable", "?s", "?g", "?t"),
        ("PresentacionGrande", "?g"),
        ("CapacidadAlta", "?s"),
    ),
    consequent=("Recomendable", "?s", "?g", "?t"),
    description="Presentaciones grandes requieren alta capacidad.",
),
    Rule(
    name="R19_prioridad_alta_accesible",
    antecedents=(
        ("Recomendable", "?s", "?g", "?t"),
        ("NecesitaAccesibilidad", "?g"),
        ("Accesible", "?s"),
    ),
    consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
    description="Espacios accesibles tienen máxima prioridad.",
),
    Rule(
    name="R20_penalizar_no_silencioso",
    antecedents=(
        ("Asignable", "?s", "?g", "?t"),
        ("EstudioIndividual", "?g"),
        ("Colaborativo", "?s"),
    ),
    consequent=("MenosIdeal", "?s", "?g", "?t"),
    description="Espacios colaborativos no son ideales para estudio individual.",
),
]


def build_kb() -> dict:
    return {
        "title": TITLE,
        "facts": set(V1_BASE_FACTS) | set(EXTRA_FACTS),
        "rules": list(V1_RULES) + list(EXTRA_RULES),
        "spaces": list(SPACES),
        "slots": list(SLOTS),
        "request_types": list(REQUEST_TYPES),
    }
