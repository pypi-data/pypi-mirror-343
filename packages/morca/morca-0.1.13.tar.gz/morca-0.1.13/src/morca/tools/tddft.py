import marimo

__generated_with = "0.12.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from pathlib import Path
    import subprocess

    import pyparsing as pp
    import polars as pl
    import altair as alt
    import cotwo as co
    return Path, alt, co, pl, pp, subprocess


@app.cell
def _(pl, pp):
    def parse_tddft_spectrum(
        text: str,
        header: str = "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS",
    ) -> pl.DataFrame:
        header_phrase = header
        lines = text.splitlines()

        # Locate the header line index that contains the header phrase.
        header_idx = None
        for i, line in enumerate(lines):
            if header_phrase in line:
                header_idx = i
                break
        if header_idx is None:
            raise ValueError("Absorption table header not found.")

        # Collect lines starting from the header until the first empty line after the header block.
        table_lines = []
        # Start from header_idx and skip a couple of lines if needed (to bypass dashed header lines).
        for line in lines[header_idx:]:
            # Stop when we hit an empty line (or a line that is only whitespace)
            if line.strip() == "":
                break
            table_lines.append(line)

        # Join the collected lines into a block of text.
        table_block = "\n".join(table_lines)

        # Define a numeric pattern (with optional exponential part)
        number = pp.Regex(r"[-+]?[0-9]*\.?[0-9]+(?:[Ee][-+]?[0-9]+)?")

        # Define the transition identifier pattern (e.g., "0-2A -> 1-2A")
        transition = pp.Regex(r"\S+\s*->\s*\S+")

        # Define the row grammar: transition followed by 8 numbers
        row = (
            transition("Transition")
            + number("Energy_eV")
            + number("Energy_cm")
            + number("Wavelength_nm")
            + number("fosc")
            + number("D2")
            + number("DX")
            + number("DY")
            + number("DZ")
        )

        # Prepare a list for storing parsed rows
        rows = []

        # Use scanString to find all matching rows in the input text
        for tokens, start, end in row.scanString(table_block):
            # Convert numeric tokens to float and build a dictionary for the row
            row_dict = {
                # "Transition": int(tokens["Transition"].split("->")[1].strip().split("-")[0]),
                "Transition": tokens["Transition"],
                "Energy_eV": float(tokens["Energy_eV"]),
                "Energy_cm": float(tokens["Energy_cm"]),
                "Wavelength_nm": float(tokens["Wavelength_nm"]),
                "fosc": float(tokens["fosc"]),
                "D2": float(tokens["D2"]),
                "DX": float(tokens["DX"]),
                "DY": float(tokens["DY"]),
                "DZ": float(tokens["DZ"]),
            }
            rows.append(row_dict)

        # Create a Polars DataFrame from the extracted rows
        df = pl.DataFrame(rows)
        return df
    return (parse_tddft_spectrum,)


@app.cell
def _(mo):
    file_text = mo.ui.text(placeholder="Path to ORCA output file", full_width=True)
    file_text
    return (file_text,)


@app.cell
def _(Path, file_text, mo):
    mo.stop(not file_text.value)

    file = Path(file_text.value)
    assert file.exists(), f"File {file} not found"
    return (file,)


@app.cell(hide_code=True)
def _(pl, pp):
    def parse_tddft_excited_states(text: str) -> pl.DataFrame:
        """
        Parse the TD-DFT excited states from the provided text.

        The parser extracts the following for each state:
          - State number
          - Energy in atomic units (E_au)
          - Energy in electron volts (E_eV)
          - Energy in cm⁻¹ (E_cm)
          - <S**2> value (S2)
          - Multiplicity (Mult)

        Each state is followed by one or more transition lines with:
          - Transition (e.g., "83b -> 89b")
          - Weight

        Returns
        -------
        pl.DataFrame
            A DataFrame with columns:
            "State", "E_au", "E_eV", "E_cm", "S2", "Mult", "Transition", "Weight"
        """
        # Define number pattern (float numbers, with optional exponential notation)
        number = pp.Regex(r"[-+]?[0-9]*\.?[0-9]+(?:[Ee][-+]?[0-9]+)?")

        # Pattern for the state header line:
        # Example:
        # STATE  1:  E=   0.030330 au      0.825 eV     6656.7 cm**-1 <S**2> =   0.865312 Mult 2
        state_header = (
            pp.Suppress("STATE")
            + pp.Word(pp.nums)("State")
            + pp.Suppress(":")
            + pp.Suppress("E=")
            + number("E_au")
            + pp.Suppress("au")
            + number("E_eV")
            + pp.Suppress("eV")
            + number("E_cm")
            + pp.Suppress("cm**-1")
            + pp.Suppress("<S**2>")
            + pp.Suppress("=")
            + number("S2")
            + pp.Suppress("Mult")
            + pp.Word(pp.nums)("Mult")
        )

        # Pattern for transition lines:
        # Example:
        #     83b ->  89b  :     0.050639
        transition_line = (
            pp.Optional(pp.White(" \t"))
            + pp.Regex(r"\S+\s*->\s*\S+")("Transition")
            + pp.Suppress(":")
            + number("Weight")
        )

        # Prepare list for rows
        rows = []
        current_state_info = {}

        # Split the input text into lines for sequential parsing
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                # Try to parse a state header
                result = state_header.parseString(line)
                # Store current state info; convert numbers to float/int as needed.
                current_state_info = {
                    "State": int(result["State"]),
                    "E_au": float(result["E_au"]),
                    "E_eV": float(result["E_eV"]),
                    "E_cm": float(result["E_cm"]),
                    "S2": float(result["S2"]),
                    "Mult": int(result["Mult"]),
                }
            except pp.ParseException:
                # If not a state header, try to parse a transition line.
                try:
                    trans_result = transition_line.parseString(line)
                    row = {
                        "State": current_state_info.get("State"),
                        "E_au": current_state_info.get("E_au"),
                        "E_eV": current_state_info.get("E_eV"),
                        "E_cm": current_state_info.get("E_cm"),
                        "S2": current_state_info.get("S2"),
                        "Mult": current_state_info.get("Mult"),
                        "Transition": trans_result["Transition"],
                        "Weight": float(trans_result["Weight"]),
                    }
                    rows.append(row)
                except pp.ParseException:
                    # If the line matches neither, we skip it.
                    continue

        # Create and return a Polars DataFrame
        df = pl.DataFrame(rows)
        return df
    return (parse_tddft_excited_states,)


@app.cell
def _(
    Path,
    alt,
    co,
    parse_tddft_excited_states,
    parse_tddft_spectrum,
    pl,
    subprocess,
):
    class Tddft:
        def __init__(self, file: str | Path) -> None:
            self.file = Path(file)
            assert file.exists()

            self.spectrum: pl.DataFrame = parse_tddft_spectrum(
                self.file.read_text()
            )
            self.excited_states: pl.DataFrame = parse_tddft_excited_states(
                self.file.read_text()
            )
            self.molecule = co.Molecule.from_file(self.file)

            for line in self.file.read_text().splitlines():
                if "Tamm-Dancoff approximation     ... deactivated" in line:
                    self.tda = False
                    break
            else:
                self.tda = True

        def plot_spectrum(self, unit: str = "Wavelength_nm") -> alt.Chart:
            return (
                alt.Chart(self.spectrum)
                .mark_bar()
                .encode(
                    x=unit,
                    y=alt.Y("fosc"),
                    color=alt.Color("Transition:N").scale(scheme="viridis"),
                )
            )

        def _get_state_vector(self, state: int) -> int:
            return state if self.tda else 2 * state - 1

        def create_difference_density(self, state: int, grid: int = 60) -> Path:
            state_vector = self._get_state_vector(state)
            gbw_file = self.file.with_suffix(".gbw")
            assert gbw_file.exists(), f"Can't find {gbw_file}"
            cis_file = self.file.with_suffix(".cis")
            assert cis_file.exists(), f"Can't find {cis_file}"

            diffdens_file = self.file.with_suffix(f".cisdp{state_vector:02d}.cube")

            if diffdens_file.exists():
                return diffdens_file

            instruction_set = (
                f"4\n{grid}\n5\n7\n6\nn\n{cis_file.resolve()}\n{state_vector}\n12\n"
            )
            result = subprocess.run(
                ["orca_plot", gbw_file, "-i"],
                text=True,
                input=instruction_set,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if not diffdens_file.exists():
                print(f"orca_plot stdout: {result.stdout}")
                print(f"orca_plot stderr: {result.stderr}")
                raise FileNotFoundError(
                    "Failed to create density file. Check what orca_plot is doing."
                )

            return diffdens_file

        def create_molecular_orbital(self, id: str, grid: int = 60) -> Path:
            """Give spin as 'a' or 'b' for now"""
            gbw_file = self.file.with_suffix(".gbw")
            assert gbw_file.exists(), f"Can't find {gbw_file}"

            id = id.strip()

            density_file = self.file.with_suffix(f".mo{id}.cube")

            if density_file.exists():
                return density_file

            instruction_set = f"4\n{grid}\n5\n7\n3\n{1 if 'b' in id else 0}\n2\n{id[:-1]}\n11\n12\n"
            result = subprocess.run(
                ["orca_plot", gbw_file, "-i"],
                text=True,
                input=instruction_set,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if not density_file.exists():
                print(f"orca_plot stdout: {result.stdout}")
                print(f"orca_plot stderr: {result.stderr}")
                raise FileNotFoundError(
                    "Failed to create density file. Check what orca_plot is doing."
                )

            return density_file
    return (Tddft,)


@app.cell
def _(Tddft, file, mo):
    t = Tddft(file)
    tddft_spectrum = mo.ui.altair_chart(
        t.plot_spectrum(), chart_selection="point", legend_selection=True
    )
    tddft_spectrum
    return t, tddft_spectrum


@app.cell
def _(mo, t, tddft_spectrum):
    mo.stop(tddft_spectrum.value.is_empty())

    state = int(tddft_spectrum.value["Transition"][0].split()[-1].split("-")[0])
    print(f"State: {state}")

    with mo.status.spinner(
        title="Generating difference density..",
        subtitle="This might take up to a minute",
    ) as _spinner:
        _diffdens = t.create_difference_density(state, grid=60)

    fig = t.molecule.create_fig_with_isosurface(
        _diffdens, isovalue=0.0025, colors=("#CCBE00", "#CC0022")
    )
    return fig, state


@app.cell
def _(fig, mo, pl, state, t, tddft_spectrum):
    _state: pl.DataFrame = tddft_spectrum.value

    _excited_states = t.excited_states.filter(pl.col("State") == state)
    orbital_transitions_df = _excited_states.select(
        ["Transition", "Weight", "Mult"]
    ).sort(by="Weight", descending=True)

    orbital_transitions = mo.ui.table(
        orbital_transitions_df, label="Orbital Transitions", selection="single"
    )

    mo.hstack(
        [
            mo.ui.plotly(fig),
            mo.vstack(
                [
                    f"State {state}",
                    f"Energy {_state['Energy_cm'][0]} 1/cm",
                    f"Wavelength {_state['Wavelength_nm'][0]} nm",
                    f"<S**2> {_excited_states['S2'][0]:.4f}",
                    orbital_transitions,
                ]
            ),
        ],
        justify="start",
    )
    return orbital_transitions, orbital_transitions_df


@app.cell
def _(mo, orbital_transitions, t, tddft_spectrum):
    mo.stop(tddft_spectrum.value.is_empty())

    mo.stop(orbital_transitions.value.is_empty())

    _from_orb, _to_orb = orbital_transitions.value["Transition"][0].split("->")

    with mo.status.spinner(
        title="Generating molecular orbital..",
    ) as _spinner:
        from_orb = t.create_molecular_orbital(_from_orb)
        to_orb = t.create_molecular_orbital(_to_orb)

    mo.hstack(
        [
            mo.ui.plotly(
                t.molecule.create_fig_with_isosurface(from_orb, isovalue=0.05),
                label="Donor orbital",
            ),
            mo.ui.plotly(
                t.molecule.create_fig_with_isosurface(to_orb, isovalue=0.05),
                label="Acceptor orbital",
            ),
        ],
        justify="start",
    )
    return from_orb, to_orb


@app.cell
def _(mo, pl, t):
    # Order the states by weight of orbital contribution

    _df = t.spectrum.rename({"Transition": "State"})
    _df = _df.with_columns(
        pl.col("State").str.extract(r"->\s*(\d+)", 1).cast(pl.Int64)
    ).drop(["D2", "DX", "DY", "DZ"])

    _orb_df = t.excited_states.drop(["E_au", "E_eV", "E_cm"])
    _orb_df = _orb_df.with_columns(
        [
            pl.col("Transition")
            .map_elements(
                lambda s: s.strip().replace(" ", "").split("->")[0],
                return_dtype=pl.String,
            )
            .alias("From Orbital"),
            pl.col("Transition")
            .map_elements(
                lambda s: s.strip().replace(" ", "").split("->")[1],
                return_dtype=pl.String,
            )
            .alias("To Orbital"),
        ]
    )
    _df = _df.join(_orb_df, on="State")
    _df = _df.select(
        [
            "State",
            "From Orbital",
            "To Orbital",
            "Weight",
            "Mult",
            "S2",
            "Wavelength_nm",
            "Energy_cm",
            "Energy_eV",
            "fosc",
        ]
    )
    data = _df
    mo.ui.data_explorer(_df)
    return (data,)


@app.cell
def _(data, mo):
    mo_dropdown = mo.ui.dropdown(
        label="Select acceptor orbital to filter for:",
        options=data["To Orbital"].sort(descending=True),
    )
    mo_dropdown
    return (mo_dropdown,)


@app.cell
def _(data, mo, mo_dropdown, pl):
    mo.stop(not mo_dropdown.value)
    _mo = mo_dropdown.value

    data.filter(pl.col("To Orbital") == _mo).sort(by="Weight", descending=True)
    return


if __name__ == "__main__":
    app.run()
