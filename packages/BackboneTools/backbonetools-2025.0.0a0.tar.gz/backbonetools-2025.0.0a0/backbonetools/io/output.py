"""
backbonetools - create, modify and visualise input and output data for the esm backbone and run backbone
Copyright (C) 2020-2025 Leonie Plaga, David Huckebrink, Christine Nowak, Jan Mutke, Jonas Finke, Silke Johanndeiter, Sophie Pathe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess as sp
from functools import partial
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gams import GamsException, GamsWorkspace
from matplotlib.colors import to_hex
from matplotlib.pyplot import get_cmap
from openpyxl import load_workbook


class BackboneResult:
    def __init__(self, path):
        ws = GamsWorkspace()
        self._path = Path(path).absolute().as_posix()
        try:
            self.gams_db = ws.add_database_from_gdx(self._path)
        except GamsException as ge:
            raise GamsException(f"Error when opening {self._path}").with_traceback(
                ge.__traceback__
            )
        except TypeError as te:
            raise TypeError(f"An error occured on {self._path}:").with_traceback(
                te.__traceback__
            )

        try:
            self.mMettings = self.gams_db.get_parameter("r_info_mSettings")
        except GamsException as ge:
            raise GamsException(
                f"Error retrieving 'r_info_mSettings' from {self._path}.\n"
                f"Please check if the file is a valid Backbone result file."
            ).with_traceback(ge.__traceback__)
        self.stepLengthInHours = self.mMettings.find_record(
            keys=["stepLengthInHours"]
        ).value
        # invest or schedule
        self.model_type = self.mMettings.first_record().keys[0]

        # allows easy access of results
        self.set_symbols_as_attribs()
        self.has_dummy_generation = not self.r_qGen_g().empty
        if self.has_dummy_generation:
            Warning(f"Model has dummy generation. ({Path(path).name})")

    def __hash__(self):
        # this is not a good hash implementation but suffices for the purpose of not loading the same file multiple times
        return hash(self.path.as_posix())

    def set_symbols_as_attribs(self):
        for symbol in self.symbols:
            # this allows to access result parameters by BackboneResult.r_emission()
            setattr(self, symbol, partial(self.param_as_df_gdxdump, symbol))

    @property
    def _backbone_path(self):
        """path to the backbone repository"""
        return Path(__file__).parent.parent.joinpath("backbone")

    @property
    def symbols(self):
        """list of all symbols in the {result_file}.gdx"""
        if hasattr(self, "_symbols"):
            return self._symbols
        # get all symbols from the gams database
        # list comprehension of gams_db raises an exception at the last index
        symbols = []
        try:
            for i, p in enumerate(self.gams_db):
                symbols.append(p.name)
        except GamsException as ge:
            if "out of range" in str(ge) and str(self.gams_db.number_symbols) in str(
                ge
            ):
                pass
            else:
                raise ge
        self._symbols = symbols
        return symbols

    def param_as_df(self, param_name, convert_time=True):
        gms_param = self.gams_db.get_parameter(param_name)
        data = [[*rec.keys, rec.value] for rec in gms_param]

        # domains have changed and now may contain sets
        domains = [x if isinstance(x, str) else x.name for x in gms_param.domains]

        columns = domains + ["Val"]
        param_df = pd.DataFrame(data=data, columns=columns)

        # converts the time column to int by omitting the first character
        if convert_time:
            if "t" in param_df.columns:
                param_df["t"] = param_df["t"].apply(lambda t: int(t[1:]))

        return param_df

    def param_as_df_gdxdump(self, param_name, encoding="1252", convert_time=True):
        """Use the 'gdxdump' GAMS utility via subprocess to convert a parameter into a pd.DataFrame.
        This is sometimes beneficial, to circumvent decoding errors
        """
        gdxdump = sp.run(
            ["gdxdump", self._path, "format", "csv", "symb", param_name], stdout=sp.PIPE
        )
        csv_data = gdxdump.stdout.decode(encoding=encoding)
        header = csv_data.partition("\n")[0]

        header = [x.strip('"') for x in header.split(",")]
        dtypes = [str if x != "Val" else float for x in header]
        dtypes = dict(zip(header, dtypes))
        df = pd.read_csv(StringIO(csv_data), dtype=dtypes, na_values="Eps")

        # converts the time column to int by omitting the first character
        if convert_time:
            if "t" in df.columns:
                df["t"] = df["t"].apply(lambda t: int(t[1:]))
        return df

    def eqn_as_df(self, eqn_name):
        gms_eqn = self.gams_db.get_equation(eqn_name)

        data = [
            [*rec.keys, rec.level, rec.marginal, rec.lower, rec.upper, rec.scale]
            for rec in gms_eqn
        ]
        columns = [x if isinstance(x, str) else x.name for x in gms_eqn.domains] + [
            "level",
            "marginal",
            "lower",
            "upper",
            "scale",
        ]

        eqn_df = pd.DataFrame(data=data, columns=columns)
        return eqn_df

    def set_as_df(self, set_name):
        gms_set = self.gams_db.get_set(set_name)
        data = [[*rec.keys] for rec in gms_set]
        domains = [x if isinstance(x, str) else x.name for x in gms_set.domains]

        set_df = pd.DataFrame(data=data, columns=domains)
        return set_df


class BackboneScenarioAnalysis:
    def __init__(self, results_dir: str = None, result_files: list = None) -> None:
        if results_dir and not result_files:
            abs_dir = Path(results_dir).resolve()
            unsorted_results = list(abs_dir.glob(r"*.gdx"))
            self.result_files = sorted(unsorted_results)
        elif not results_dir and result_files:
            self.result_files = sorted([Path(path) for path in result_files])
        else:
            raise ValueError(
                f"""One of the parameters 'results_dir' or 'result_files' must be passed.
                Received: {dict(results_dir=results_dir, result_files=result_files)}.
                """
            )

        self.bb_results = [
            BackboneResult(Path(file).as_posix()) for file in self.result_files
        ]

        # scenario names will be derived from the filenames
        self.scenarios = [
            Path(file).stem.replace("_", " ") for file in self.result_files
        ]

        # define colors as sequence:
        self.colors = self._get_n_hex_colors_from_cmap(
            "Spectral_r", len(self.result_files)
        )

        self.set_symbols_as_attribs()
        pass

    def _scenario_param(self, param_name, parallel=False):
        frames = []

        def _get_attr_df_and_set_name(result, param_name, scenario_name):
            frame = getattr(result, param_name)()
            frame["Scenario"] = scenario_name
            return frame

        if not parallel:
            for result, scenario in zip(self.bb_results, self.scenarios):
                frame = _get_attr_df_and_set_name(result, param_name, scenario)
                frames.append(frame)
        else:
            with ThreadPool(9) as p:

                param_name_list = [param_name] * len(self.bb_results)
                frames = p.starmap(
                    _get_attr_df_and_set_name,
                    zip(self.bb_results, param_name_list, self.scenarios),
                )
        return pd.concat(frames)

    def set_symbols_as_attribs(self):
        for symbol in self.bb_results[0].symbols:
            # this allows to access result parameters by BackboneResult.r_emission()
            setattr(self, symbol, partial(self._scenario_param, symbol))

    @staticmethod
    def _get_n_hex_colors_from_cmap(cmap_name, n):
        cmap = get_cmap(cmap_name)
        fracs = np.linspace(0, 1, n)
        return [to_hex(cmap(f)) for f in fracs]

    def installed_capacity(self) -> pd.DataFrame:
        frames = []
        for scen, result in zip(self.scenarios, self.bb_results):
            installed_capacity = (
                result.r_invest_unitCapacity_gnu()
                .groupby("unit")
                .sum(numeric_only=True)
            )

            installed_capacity["Scenario"] = scen

            frames.append(installed_capacity)

        scenario_df = pd.concat(frames)
        scenario_df = scenario_df.reset_index()
        return scenario_df

    def plot_installed_capacity(self, colors=None):
        if colors is None:
            colors = self.colors
        scenario_df = self.installed_capacity()
        fig = px.bar(
            scenario_df,
            x="unit",
            y="Val",
            color="Scenario",
            barmode="group",
            color_discrete_sequence=colors,
        )

        return fig

    def system_cost_composition(
        self,
    ) -> pd.DataFrame:
        frames = []
        for scen, result in zip(self.scenarios, self.bb_results):
            # print(scen, result._path)
            invest_cost = result.r_cost_unitInvestmentCost_gnu()
            invest_cost["Category"] = "Invest"
            invest_cost_sum = invest_cost.groupby("Category").sum(numeric_only=True)

            transmission_cost = result.r_cost_linkInvestmentCost_gnn()
            transmission_cost["Category"] = "Grid expansion"
            transmission_cost_sum = transmission_cost.groupby("Category").sum(
                numeric_only=True
            )

            fuel_emission_cost = result.r_cost_unitFuelEmissionCost_u()
            fuel_emission_cost["Category"] = fuel_emission_cost["node"].str.capitalize()
            fuel_emission_cost_sum = fuel_emission_cost.groupby("Category").sum(
                numeric_only=True
            )

            fom_cost = result.r_cost_unitFOMCost_gnu()
            fom_cost["Category"] = "FOM"
            fom_cost_sum = fom_cost.groupby("Category").sum(numeric_only=True)

            vom_cost = result.r_cost_unitVOMCost_gnu()
            vom_cost["Category"] = "VOM"
            vom_cost_sum = vom_cost.groupby("Category").sum(numeric_only=True)

            cost_df = pd.concat(
                [
                    invest_cost_sum,
                    fuel_emission_cost_sum,
                    fom_cost_sum,
                    vom_cost_sum,
                    transmission_cost_sum,
                ]
            )
            cost_df["Scenario"] = scen
            frames.append(cost_df)
        scenario_df = pd.concat(frames)
        scenario_df = scenario_df.reset_index()
        return scenario_df

    def plot_system_cost_composition(self):
        scenario_df = self.system_cost_composition()
        fig = px.bar(scenario_df, x="Scenario", y="Val", color="Category", width=700)
        fig.update_yaxes({"title": "annual system cost [M€]"})
        fig.update_layout(legend={"traceorder": "reversed"})
        # fig.update_traces(dict(width=[0.6] * 8))
        return fig

    def energy_provided_per_unitType(
        self, unitType_mapping: dict = None
    ) -> pd.DataFrame:
        frames = []
        for scen, result in zip(self.scenarios, self.bb_results):
            sample_df = result.r_gen_gnu()
            grouped_df = sample_df.groupby(["grid", "unit"]).sum(numeric_only=True)
            grouped_df["Scenario"] = scen
            frames.append(grouped_df)
        scenario_df = pd.concat(frames)
        return scenario_df

    def plot_energy_per_unitType(self, colors=None):
        if colors is None:
            colors = self.colors
        fig = go.Figure()

        scenario_df = self.energy_provided_per_unitType().reset_index()

        for i, scen in enumerate(self.scenarios):
            data = scenario_df.loc[scenario_df["Scenario"] == scen, :]
            x = []
            x.append(data["grid"].values)
            x.append(data["unit"].values)
            color = colors[i % len(colors)]
            fig.add_bar(x=x, y=data["Val"], name=scen, marker={"color": color})
        # fig.update_traces(colors = px.colors.sequential.RdBu[:4])
        fig.update_yaxes(title="provided energy by unit type [MWh]")
        # fig.write_image(f"{results_dir}/figures/energy_generation_by_type.svg")
        # fig.write_image(f"{results_dir}/figures/energy_generation_by_type.pdf")
        return fig

    def plot_energy_per_unitType_stacked(self, colors=None, u_name_filter=None):
        fig = go.Figure()
        scenario_df = self.energy_provided_per_unitType().reset_index()

        if u_name_filter:
            # for a birds eye view, this can be helpful for condensing unit_names
            # i.e. u_name_filter=lambda x: x.split(" ",2)[-1]
            # "DE0 0 coal" -> coal
            # "FR0 1 coal" -> coal
            scenario_df["unit"] = scenario_df["unit"].apply(u_name_filter)

        utypes = scenario_df["unit"].unique()

        for i, utype in enumerate(utypes):
            # select and aggregate data
            data = scenario_df.loc[scenario_df["unit"] == utype, :]
            data = data.groupby(["grid", "unit", "Scenario"]).sum().reset_index()

            # generate double index
            x = []
            x.append(data["grid"].values)
            x.append(data["Scenario"].values)
            color = colors[i % len(colors)]
            fig.add_bar(x=x, y=data["Val"], name=utype, marker={"color": color})
        fig.update_yaxes(title="provided energy by unit type [MWh]")
        fig.update_layout(barmode="relative")
        return fig

    def plot_priceDurationCurve(self, nodes=[], stylelist=[], colorlist=None):
        # Plot Price Duration Curve by scenarios over all or predefined nodes in the electric grid
        result = self.bb_results[0]
        marginal = result.r_balance_marginalValue_gnft()
        # extract all electric nodes from first scenario if non are given
        # grid choice has to be adapted or dropped in the code if desired
        if not nodes:
            nodes = marginal[marginal["grid"] == "elec"]["node"].drop_duplicates()
        ax_list = []
        # define list for graph's line style
        if not stylelist:
            for x in range(len(self.scenarios)):
                for element in ["-", "--", "-.", ":"]:
                    stylelist.append(element)
        # create plots by node over scenarios
        for n in nodes:
            scen_dict = {}
            for s, r in zip(self.scenarios, self.bb_results):
                marginal = r.r_balance_marginalValue_gnft()
                marginal = marginal[marginal["node"] == str(n)].sort_values("Val")
                marginal["Val"] = marginal["Val"] * -1
                price = marginal["Val"].tolist()
                scen_dict.update({str(s): price})
                t = [np.arange(0, len(price), 1)]
            df = pd.DataFrame(scen_dict, index=t)
            ax = df.plot.line(title=str(n), lw=2, style=stylelist, color=colorlist)
            ax.set_xticks([])
            ax.set_yticks(
                range(
                    min(0, int(min(price))),
                    int(max(price)),
                    round((int(max(price)) - min(0, int(min(price)))) / 10),
                )
            )
            ax.set_xlabel("hours sorted")
            ax.set_ylabel("€/MWh")
            ax.legend()
            ax_list.append(ax)
        return ax_list

    # Plot Price Duration Curve by all or predefined electric nodes over scenario
    def plot_priceDurationCurve2(self, nodes=[], stylelist=[], colorlist=None):
        result = self.bb_results[0]
        marginal = result.r_balance_marginalValue_gnft()
        # extract all electric nodes from first scenario if non are given
        # grid choice has to be adapted or dropped in the code if desired
        if not nodes:
            nodes = (
                marginal[marginal["grid"] == "elec"]["node"]
                .drop_duplicates()
                .transpose()
                .tolist()
            )
        scen_dict = {}
        ax_list = []
        # define list for graph's line style
        if not stylelist:
            for x in range(len(nodes)):
                for element in ["-", "--", "-.", ":"]:
                    stylelist.append(element)
        # create plots by nodes over scenarios
        for s, r in zip(self.scenarios, self.bb_results):
            for n in nodes:
                # result=self.bb_results[0]
                marginal = r.r_balance_marginalValue_gnft()
                marginal = marginal[marginal["node"] == str(n)].sort_values("Val")
                marginal["Val"] = marginal["Val"] * -1
                price = marginal["Val"].tolist()
                t = [np.arange(0, len(price), 1)]
                scen_dict.update({str(n): price})
                df = pd.DataFrame(scen_dict, index=t)
            ax = df.plot.line(title=str(s), style=stylelist, lw=2, color=colorlist)
            ax.set_xticks([])
            ax.set_yticks(
                range(
                    min(0, int(min(price))),
                    int(max(price)),
                    round((int(max(price)) - min(0, int(min(price)))) / 10),
                )
            )
            ax.set_xlabel("hours sorted")
            ax.set_ylabel("€/MWh")
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            ax_list.append(ax)
        return ax_list


def invest2schedule(invest_xlsx, result_gdx, schedule_xlsx_path=None):

    # # Invest 2 Schedule
    # ### read an investment result and its' input file, create a new input file

    bb_input_path = invest_xlsx
    bb_output_path = result_gdx

    if schedule_xlsx_path is None:
        schedule_xlsx_path = Path(bb_input_path).stem + "_schedule.xlsx"
        schedule_xlsx_path = Path(bb_input_path).parent.joinpath(schedule_xlsx_path)

    result = BackboneResult(bb_output_path)
    invested_capacities = result.r_invest_unitCapacity_gnu().dropna()

    wb = load_workbook(bb_input_path)
    p_gnu_io = wb["p_gnu_io"]
    p_gnu_io_values = list(p_gnu_io.values)
    p_gnu_io_df = pd.DataFrame(p_gnu_io_values[1:], columns=p_gnu_io_values[0])

    # we only put cost data, where input/output == "output"
    idx_output = p_gnu_io_df["input output"] == "output"

    output_df = p_gnu_io_df.loc[idx_output, :]
    int_idx = invested_capacities["unit"].apply(
        lambda x: output_df.index[output_df["unit"] == x][0]
    )

    # add investments to previously existing
    invest_rows = output_df.loc[int_idx, :]

    # replace eps with 0 to enable addition
    invest_rows = invest_rows.replace("eps", 0)
    invest_rows["capacity"] += invested_capacities["Val"].values

    # replace 0 with eps for backbone
    invest_rows = invest_rows.replace(0, "eps")

    # overwrite values in p_gnu_io frame
    # note that index of p_gnu_io_df and output_df is consistent
    p_gnu_io_df.loc[int_idx, "capacity"] = invest_rows["capacity"]

    p_gnu_io.delete_rows(idx=2, amount=9999)
    for tup in p_gnu_io_df.itertuples(index=False):
        # bb_indices = col_name.split("|")
        p_gnu_io.append([*tup])

    # disable investments: set max unit count to 0
    p_unit = wb["p_unit"]
    p_unit_values = list(p_unit.values)
    p_unit_df = pd.DataFrame(p_unit_values[1:], columns=p_unit_values[0])
    p_unit_df["maxUnitCount"] = 0

    p_unit.delete_rows(idx=2, amount=9999)
    for tup in p_unit_df.itertuples(index=False):
        p_unit.append([*tup])

    # Handle storages -TODO
    # Update upper limit for storages in p_gnBoundaryproperties

    storage_investments = invested_capacities.query("grid == 'storage'")
    if not storage_investments.empty:
        raise NotImplementedError(
            "Storages have been invested, but conversion to schedule is not yet implemented!"
        )

    # add investments in p_gnn
    grid_investments = result.r_invest_transferCapacity_gnn()
    grid_investments = grid_investments.set_index(["grid", "node", "node_1"])

    p_gnn_sheet = wb["p_gnn"]
    p_gnn_values = list(p_gnn_sheet.values)
    p_gnn_df = pd.DataFrame(p_gnn_values[1:], columns=p_gnn_values[0])

    # update index to enable easy merging of values
    p_gnn_df = p_gnn_df.set_index(["grid", "from node", "to node"])
    p_gnn_df.loc[grid_investments.index, "transferCap"] += grid_investments["Val"]

    # disable further investments
    p_gnn_df["transferCapInvLimit"] = "eps"

    # overwrite the sheet with updated values
    p_gnn_sheet.delete_rows(idx=2, amount=9999)
    p_gnn_df = p_gnn_df.reset_index()
    for tup in p_gnn_df.itertuples(index=False):
        p_gnn_sheet.append([*tup])

    wb.save(schedule_xlsx_path)
    return schedule_xlsx_path


if __name__ == "__main__":
    result = BackboneResult(
        "EURO_heat_retrofit_MICQP_bioShareLimrcp26_coldno_Cap_gFix_no_rtrft_results.gdx"
    )
    print(result.symbols)
    pass
