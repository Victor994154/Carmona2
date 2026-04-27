from __future__ import annotations

import importlib
from typing import Dict, List

from engine import run_request


MANDATORY_CASES = [
    {
        "case_name": "Caso 1 - EstudioIndividual en h1",
        "request_id": "reqA",
        "slot": "h1",
        "request_type": "EstudioIndividual",
        "expected_spaces": {"AulaB", "Biblio1"},
    },
    {
        "case_name": "Caso 2 - ReunionEquipo en h2",
        "request_id": "reqB",
        "slot": "h2",
        "request_type": "ReunionEquipo",
        "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
        "case_name": "Caso 3 - Presentacion en h2",
        "request_id": "reqC",
        "slot": "h2",
        "request_type": "Presentacion",
        "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
        "case_name": "Caso 4 - PresentacionGrande en h3",
        "request_id": "reqD",
        "slot": "h3",
        "request_type": "PresentacionGrande",
        "expected_spaces": {"AuditorioMini"},
    },
    {
    "case_name": "Caso 5 - ReunionAccesible en h2",
    "request_id": "reqE",
    "slot": "h2",
    "request_type": "ReunionAccesible",
    "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
    "case_name": "Caso 6 - Presentacion con preferencia centrica",
    "request_id": "reqF",
    "slot": "h2",
    "request_type": "Presentacion",
    "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
    "case_name": "Caso 7 - ReunionAccesible en h2 (enfoque accesibilidad)",
    "request_id": "reqG",
    "slot": "h2",
    "request_type": "ReunionAccesible",
    "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
    "case_name": "Caso 8 - Presentacion con preferencia centrica",
    "request_id": "reqH",
    "slot": "h2",
    "request_type": "Presentacion",
    "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
    "case_name": "Caso 9 - EstudioIndividual evitando colaborativos",
    "request_id": "reqI",
    "slot": "h1",
    "request_type": "EstudioIndividual",
    "expected_spaces": {"Biblio1"},
    },
    {
    "case_name": "Caso 10 - PresentacionGrande optimizada",
    "request_id": "reqJ",
    "slot": "h3",
    "request_type": "PresentacionGrande",
    "expected_spaces": {"AuditorioMini"},
    },
    {
    "case_name": "Caso 11 - ReunionAccesible en h1 (menos opciones)",
    "request_id": "reqK",
    "slot": "h1",
    "request_type": "ReunionAccesible",
    "expected_spaces": {"AulaA"},
    },
]


def run_cases(module_name: str) -> List[Dict]:
    kb_module = importlib.import_module(module_name)
    kb = kb_module.build_kb()

    results = []
    for case in MANDATORY_CASES:
        result = run_request(
            kb["facts"],
            kb["rules"],
            case["request_id"],
            case["slot"],
            case["request_type"],
        )
        spaces = {fact[1] for fact in result["assignable"]}
        ok = case["expected_spaces"].issubset(spaces)

        results.append(
            {
                "case_name": case["case_name"],
                "assignable_spaces": sorted(spaces),
                "assignable_count": len(result["assignable"]),
                "recommendable_count": len(result["recommendable"]),
                "passes_minimum_check": ok,
            }
        )
    return results


if __name__ == "__main__":
    for module_name in ["kb_v1", "kb_v2"]:
        print(f"\n=== Probando {module_name} ===")
        for row in run_cases(module_name):
            print(row)
