from pathlib import Path

import polars as pl


def _parse_energy(file: str | Path, keyword: str, token_id: int) -> float:
    lines = Path(file).read_text().splitlines()

    for line in reversed(lines):
        if keyword in line:
            return float(line.split()[token_id])
    raise ValueError(f"'{keyword}' not found.")

def parse_fspe_eh(file: str | Path) -> float:
    KEYWORD = "FINAL SINGLE POINT ENERGY"
    TOKEN_ID = -1
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_zpe_eh(file: str | Path) -> float:
    KEYWORD = "Zero point energy"
    TOKEN_ID = -4
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_thermal_correction_eh(file: str | Path) -> float:
    KEYWORD = "Total thermal correction"
    TOKEN_ID = -4
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_enthalpy_eh(file: str | Path) -> float:
    KEYWORD = "Total Enthalpy"
    TOKEN_ID = -2
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_entropy_correction_eh(file: str | Path) -> float:
    KEYWORD = "Total entropy correction"
    TOKEN_ID = -4
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_gibbs_free_energy_eh(file: str | Path) -> float:
    KEYWORD = "Final Gibbs free energy"
    TOKEN_ID = -2
    return _parse_energy(file, KEYWORD, TOKEN_ID)

def parse_gibbs_correction_eh(file: str | Path) -> float:
    """For completeness - the Gibbs free energy minus the electronic energy"""
    KEYWORD = "G-E(el)"
    TOKEN_ID = -4
    return _parse_energy(file, KEYWORD, TOKEN_ID)
