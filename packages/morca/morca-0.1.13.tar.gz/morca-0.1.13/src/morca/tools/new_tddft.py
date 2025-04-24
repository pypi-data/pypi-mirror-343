import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from pathlib import Path

    import numpy as np
    import polars as pl
    from scipy.signal import convolve
    import altair as alt

    from morca import parse_absorption_spectrum, parse_tddft_excited_states
    return (
        Path,
        alt,
        convolve,
        mo,
        np,
        parse_absorption_spectrum,
        parse_tddft_excited_states,
        pl,
    )


@app.cell
def _(Path):
    file = Path("/Users/freddy/Documents/Projects/morca/test/tddft_tpssh.out")
    return (file,)


@app.cell
def _(file, parse_absorption_spectrum, parse_tddft_excited_states):
    excited_states_df = parse_tddft_excited_states(file)
    spectrum_df = parse_absorption_spectrum(file)
    print(spectrum_df.schema)
    return excited_states_df, spectrum_df


@app.cell
def _():
    # # Define gaussian broadening functions

    # # Step 1: Define the broadening function (Gaussian in this case)
    # def gaussian(x, fwhm):
    #     """Gaussian function used for spectral broadening.

    #     Args:
    #         x: The wavelength or frequency values relative to the center.
    #         fwhm: The full width at half maximum (FWHM) of the Gaussian.

    #     Returns:
    #         Array of Gaussian function values.
    #     """
    #     sigma = fwhm / (
    #         2 * np.sqrt(2 * np.log(2))
    #     )  # Convert FWHM to standard deviation

    #     if sigma == 0:
    #         return np.zeros_like(x)

    #     return np.exp(-(x**2) / (2 * sigma**2))


    # def apply_gaussian_filter(
    #     df, energy_col, intensity_col, fwhm, interpolation_factor=5
    # ):
    #     """Apply spectral broadening to a Polars DataFrame with spectral data.

    #     Args:
    #         df: The input Polars DataFrame containing spectral data.
    #         energy_col: The column name containing energy or frequency values.
    #         intensity_col: The column name containing intensity values.
    #         fwhm: Full width at half maximum (FWHM) for the broadening.
    #         interpolation_factor: Factor by which to increase the number of data points for smoothing.

    #     Returns:
    #         A new Polars DataFrame with the broadened and smoothed spectrum.
    #     """
    #     # Extract data from the Polars DataFrame
    #     energies = df[energy_col].to_numpy()
    #     intensities = df[intensity_col].to_numpy()

    #     # Step 1: Interpolate the data to add more points (smoothing)
    #     new_energies = np.linspace(
    #         energies.min(), energies.max(), len(energies) * interpolation_factor
    #     )

    #     # Step 2: Create an array of zeros for the new intensities (zero padding)
    #     new_intensities = np.zeros_like(new_energies)

    #     # Step 3: Map original intensities to the nearest points on the new energy grid
    #     interpolated_indices = np.searchsorted(new_energies, energies)
    #     for i, idx in enumerate(interpolated_indices):
    #         if idx < len(new_energies):
    #             new_intensities[idx] = intensities[
    #                 i
    #             ]  # Map original intensities to new grid

    #     # Step 4: Create a energy grid relative to the center of the spectrum
    #     delta_energies = new_energies - np.mean(new_energies)

    #     # Step 5: Create the Gaussian kernel for broadening
    #     gaussian_kernel = gaussian(delta_energies, fwhm)

    #     # Step 6: Convolve the interpolated intensity with the Gaussian broadening kernel
    #     broadened_intensities = convolve(
    #         new_intensities, gaussian_kernel, mode="same"
    #     )

    #     # Step 7: Normalize the result to maintain the total intensity
    #     # broadened_intensities /= np.max(broadened_intensities)

    #     # Step 8: Create a new Polars DataFrame with broadened spectrum
    #     broadened_df = pl.DataFrame(
    #         {energy_col: new_energies, intensity_col: broadened_intensities}
    #     )

    #     return broadened_df
    return


@app.cell
def _(np):
    from scipy.interpolate import interp1d


    def gaussian(x: np.ndarray, fwhm: float) -> np.ndarray:
        """
        Gaussian function used for spectral broadening.

        Parameters
        ----------
        x : np.ndarray
            Energy/frequency offset relative to center.
        fwhm : float
            Full width at half maximum (FWHM) of the Gaussian.

        Returns
        -------
        np.ndarray
            Gaussian values evaluated at x.
        """
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        if sigma == 0:
            return np.zeros_like(x)
        return np.exp(-(x**2) / (2 * sigma**2))
    return gaussian, interp1d


@app.cell
def _(mo):
    fwhm_number = mo.ui.number(start=0, stop=10000, value=2000, step=100)
    fwhm_number
    return (fwhm_number,)


@app.cell
def _():
    # _simulated_spectrum = apply_gaussian_filter(
    #     spectrum_df, "energy_cm", "fosc", fwhm_number.value
    # )

    # sim_chart = (
    #     alt.Chart(_simulated_spectrum)
    #     .mark_line()
    #     .encode(
    #         x="energy_cm",
    #         y="fosc",
    #     )
    # )
    # sim_chart
    return


@app.cell
def _(alt, spectrum_df):
    bar_chart = (
        alt.Chart(spectrum_df)
        .mark_bar()
        .encode(x="energy_cm", y="fosc", tooltip="to_state", color="to_mult:N")
    )
    bar_chart
    return (bar_chart,)


@app.cell
def _():
    # sim_chart + bar_chart
    return


@app.cell
def _():
    # # plot a gaussian for each transition
    # def plot_gaussian(energy, fwhm, intensity):
    #     """Plot a Gaussian function for each transition.

    #     Args:
    #         energy: The energy value for the transition.
    #         fwhm: Full width at half maximum (FWHM) for the Gaussian.
    #         intensity: The intensity value for the transition.
    #         color: Color for the Gaussian plot.
    #     """
    #     x = np.linspace(energy - 2 * fwhm, energy + 2 * fwhm, 100)
    #     y = intensity * gaussian(x - energy, fwhm)
    #     return x, y


    # charts = []
    # dfs = []
    # for row in spectrum_df.iter_rows(named=True):
    #     energy = row["energy_cm"]
    #     fwhm = fwhm_number.value
    #     intensity = row["fosc"]

    #     # Call the Gaussian plotting function.
    #     x, y = plot_gaussian(energy, fwhm, intensity)
    #     df = pl.DataFrame({"to_state": row["to_state"], "energy_cm": x, "fosc": y})
    #     df = df.filter(pl.col("fosc") != 0)
    #     dfs.append(df)

    #     # Create an Altair chart.
    #     # In this simple example, we encode x and y as lists of values.
    #     chart = (
    #         alt.Chart(df)
    #         .mark_area(opacity=0.3)
    #         .encode(x="energy_cm", y="fosc", color="to_state:N")
    #     )
    #     charts.append(chart)
    return


@app.cell
def _(alt, fwhm_number, gaussian, np, pl, spectrum_df):
    # import numpy as np
    # import polars as pl
    # import altair as alt

    # 1) pick a common energy grid *once*
    fwhm = fwhm_number.value
    # extend range a bit beyond your transitions:
    emin = spectrum_df.select(pl.col("energy_cm")).min().item() - 2 * fwhm
    emax = spectrum_df.select(pl.col("energy_cm")).max().item() + 2 * fwhm
    grid = np.linspace(emin, emax, 500)  # tweak resolution here


    # 2) helper: return y-array for a single transition
    def gaussian_line(energy0: float, fwhm: float, intensity: float) -> np.ndarray:
        """
        energy0 : center energy (cm⁻¹)
        fwhm    : full width at half max
        intensity: peak height
        """
        return intensity * gaussian(grid - energy0, fwhm)


    # 3) build per-transition DataFrames and accumulate the y‑arrays
    dfs = []
    all_ys = []
    for row in spectrum_df.iter_rows(named=True):
        y = gaussian_line(row["energy_cm"], fwhm, row["fosc"])
        all_ys.append(y)

        df_line = pl.DataFrame(
            {
                "to_state": [row["to_state"]] * grid.size,
                "energy_cm": grid,
                "intensity_cm1": y,
            }
        ).filter(pl.col("intensity_cm1") > 0)
        dfs.append(df_line)

    # 4) sum up all y‑arrays into one spectrum
    total_y = np.sum(all_ys, axis=0)
    spectrum_total = pl.DataFrame({"energy_cm": grid, "intensity_cm1": total_y})

    # 5) plot total spectrum alongside individual areas
    base = (
        alt.Chart(spectrum_total)
        .mark_line()
        .encode(x="energy_cm", y="intensity_cm1")
        .properties(title="Simulated Spectrum")
    )

    overlays = [
        alt.Chart(df)
        .mark_area(opacity=0.3)
        .encode(
            x="energy_cm",
            y="intensity_cm1",
            color=alt.Color("to_state:N").scale(
                scheme="category20", domain=range(0, 128)
            ),
        )
        for df in dfs
    ]

    final_chart = alt.layer(*overlays, base).resolve_scale(color="independent")
    final_chart
    return (
        all_ys,
        base,
        df_line,
        dfs,
        emax,
        emin,
        final_chart,
        fwhm,
        gaussian_line,
        grid,
        overlays,
        row,
        spectrum_total,
        total_y,
        y,
    )


@app.cell
def _(dfs):
    dfs[9]
    return


@app.cell
def _(alt, charts):
    # Combine all chartsinto one
    combined_chart = alt.layer(*charts)
    combined_chart
    return (combined_chart,)


@app.cell
def _(alt):
    x_brush = alt.selection_interval(encodings=["x"])
    return (x_brush,)


@app.cell
def _(area_charts, mo, sim_df_chart, x_brush):
    # cc = sim_chart + states_chart + bar_chart
    # cc = states_chart
    cc = area_charts[0] + sim_df_chart
    for c in area_charts[1:]:
        cc += c
    ccc = mo.ui.altair_chart(cc.add_params(x_brush))
    ccc
    return c, cc, ccc


@app.cell
def _(dfs, pl):
    # Merge all spectra
    _all_df = pl.concat(dfs)

    # Define new energy grid for interpolation
    _min_x = _all_df["energy_cm"].min()
    _max_x = _all_df["energy_cm"].max()
    return


@app.cell
def _(sim_df_chart):
    sim_df_chart
    return


@app.cell
def _(ccc, combined_df, pl):
    _sel = ccc.apply_selection(combined_df)
    _fosc_sum = _sel["fosc"].sum()
    _sel = (
        _sel.group_by("to_state")
        .agg([pl.col("fosc").sum().truediv(_fosc_sum).alias("weight")])
        .sort("weight", descending=True)
    )

    sel = _sel
    return (sel,)


@app.cell
def _():
    # now that i can get a selection, i can compute the excited states ratio under a certain feature

    # we can use this data to maybe shade the sim_chart line
    return


@app.cell
def _(alt, dfs, pl):
    combined_df = pl.concat(dfs).sort(["to_state", "energy_cm"])

    states_chart = (
        alt.Chart(combined_df)
        .mark_line(opacity=0.9, interpolate="natural")
        .encode(
            x="energy_cm",
            y="fosc",
            color="to_state:N",
            # opacity=alt.condition(x_brush, alt.value(1), alt.value(0.2)),
        )
    )
    return combined_df, states_chart


@app.cell
def _(alt, dfs):
    area_charts = []

    for _df in dfs:
        if _df.is_empty():
            continue

        area_charts.append(
            alt.Chart(_df)
            .mark_area(opacity=0.3, interpolate="natural", line=True)
            .encode(
                x="energy_cm",
                y="fosc",
                color="to_state:N",
            )
        )
    return (area_charts,)


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
