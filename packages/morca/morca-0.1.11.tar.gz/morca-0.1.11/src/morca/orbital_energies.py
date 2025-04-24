from pathlib import Path

import polars as pl
from pyparsing import pyparsing_common as ppc

def parse_orbital_energies(file: str | Path) -> pl.DataFrame:
    """Parse the last ORBTIAL ENERGIES table from an ORCA output file.

    Returns a pl.DataFrame:
        restricted:   ("Id", "Occ", "Energy_Eh", "Energy_eV")
        unrestricted: ("Id", "Occ", "Energy_Eh", "Energy_eV", "Spin")
    """
    TABLE_HEADER_TO_DATA_OFFSET = 4

    lines = Path(file).read_text().splitlines()

    # Find the last occurence of ORBITAL ENERGIES
    all_occurences = [i for i, line in enumerate(lines) if line.strip() == "ORBITAL ENERGIES"]
    if len(all_occurences) == 0:
            raise ValueError("No orbital energies found")
    table_start_index = all_occurences[-1] + TABLE_HEADER_TO_DATA_OFFSET

    # Identify unrestricted calculation
    unrestricted = True if lines[table_start_index - 2].strip() == "SPIN UP ORBITALS" else False

    # Define row-parsing grammar
    _integer = ppc.integer
    _float = ppc.fnumber
    # The occupation need not be an integer, e.g. for CASSCF
    row_grammar = (_integer("Id") + _float("Occ") + _float("Energy_Eh") + _float("Energy_eV"))

    def parse_table(table_start: int) -> list:
        """Helper function for parsing an orbital energies table."""
        table_rows = []
        for line in lines[table_start:]:
            if not line.strip() or line.startswith("*"):
                break
            table_rows.append(row_grammar.parse_string(line).as_dict())
        return table_rows

    if unrestricted:
        spin_up_data = parse_table(table_start_index)
        for row in spin_up_data:
            row["Spin"] = "up"
        spin_down_data = parse_table(table_start_index + len(spin_up_data) + 3)
        for row in spin_down_data:
            row["Spin"] = "down"
        data = spin_up_data + spin_down_data
    else:
        data = parse_table(table_start_index)
    return pl.from_dicts(data)
