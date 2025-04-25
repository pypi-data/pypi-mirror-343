import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import polars as pl
    from scipy.signal import convolve
    import altair as alt

    from morca import parse_absorption_spectrum, parse_tddft_excited_states
    from morca.broadening import create_simulated_spectrum_chart
    return (
        Path,
        alt,
        convolve,
        create_simulated_spectrum_chart,
        np,
        parse_absorption_spectrum,
        parse_tddft_excited_states,
        pl,
    )


@app.cell
def _(mo):
    file_text = mo.ui.text(
        label="Path to output file",
        value="/Users/freddy/Documents/Projects/morca/test/tddft_tpssh.out",
        full_width=True
    )
    file_text
    return (file_text,)


@app.cell
def _(Path, file_text, parse_absorption_spectrum, parse_tddft_excited_states):
    _file = Path(file_text.value)

    excited_states_df = parse_tddft_excited_states(_file)
    spectrum_df = parse_absorption_spectrum(_file)
    return excited_states_df, spectrum_df


@app.cell
def _(mo):
    fwhm_number = mo.ui.slider(label="FWHM", start=0, stop=10000, value=2000, step=100, show_value=True)
    fwhm_number
    return (fwhm_number,)


@app.cell
def _(create_simulated_spectrum_chart, mo):
    @mo.cache
    def plot(df, fwhm):
        return create_simulated_spectrum_chart(df, fwhm)
    return (plot,)


@app.cell
def _(fwhm_number, mo, plot, spectrum_df):
    _chart = plot(spectrum_df, fwhm = fwhm_number.value)
    mo.ui.altair_chart(_chart).interactive()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
