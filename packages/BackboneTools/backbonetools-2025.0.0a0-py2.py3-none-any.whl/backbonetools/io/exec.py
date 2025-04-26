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

import os
import subprocess as sp
from glob import glob
from multiprocessing.pool import ThreadPool
from pathlib import Path

from backbonetools.io.input import BackboneInput
from backbonetools.io.output import BackboneResult


def run_backbone(
    input_dir,
    input_file_gdx,
    output_dir,
    output_file=None,
    backbone_dir=None,
    **kwargs,
):
    """runs Backbone with the specified arguments

    Args:
        input_dir (str): Path to the input directory for Backbone to read configurations (e.g. `investInit.gms`)
        input_file_gdx (str): Path to the Backbone input file
        output_dir (str): Path to the output directory, where results shall be written
        output_file (str): Name of the Backbone result file
        backbone_dir (str, optional): Path to the Backbone Framework. Defaults to the path of the submodule in this repository.
    """

    # if not specified, derive from input_file_gdx
    if not output_file:
        output_file = Path(input_file_gdx).stem + "_result.gdx"

    # if not specified, set backbone_dir to submodule path
    if not backbone_dir:
        backbone_dir = Path(__file__).parent.parent.joinpath("backbone")

    # keyword arguments are parsed into backbone suitable form
    # e.g. dict(maxTotalCost=42) will be passed as "--maxTotalCost=42" to backbone
    keyword_args = [f"--{k}={v}" for k, v in kwargs.items()]

    # spaces in file names don't work through subprocesses
    contain_spaces = [
        " " in str(file_or_dir)
        for file_or_dir in [input_dir, input_file_gdx, output_dir, output_file]
    ]
    if any(contain_spaces):
        raise ValueError(
            "Passing paths with spaces via subprocess to Gams is not supported yet."
        )

    # absolute paths are better for gams
    input_dir = Path(input_dir).absolute().as_posix()
    input_file_gdx = Path(input_file_gdx).absolute().as_posix()
    output_dir = Path(output_dir).absolute().as_posix()

    Path(input_dir).mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)

    process_output = sp.run(
        [
            "gams",
            "Backbone.gms",
            f"--input_dir={input_dir}",
            f"--input_file_gdx={input_file_gdx}",
            f"--output_dir={output_dir}",
            f"--output_file={output_file}",
            *keyword_args,
        ],
        cwd=backbone_dir,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        # text= True
    )

    # stdout, stderr = process_output.communicate()
    # write terminal output to a file
    open(f"{output_dir}/{Path(output_file).stem}_terminal.log", "w").write(
        process_output.stdout.decode()
    )
    open(f"{output_dir}/{Path(output_file).stem}_error.log", "w").write(
        process_output.stderr.decode()
    )
    print("finished", output_file)
    return Path(output_dir).joinpath(output_file).absolute()


def sensitivity(
    input_file_gdx,
    bb_input_dir,
    output_dir=None,
    parallel=True,
    param="CO2",
    percentages=[0.05, 0.1, 0.2, 0.4, 0.8],
):
    if param != "CO2":
        raise NotImplementedError(
            f"sensitivity not yet implemented for parameters other than {param}."
        )

    sensitivity_dir = Path(input_file_gdx).parent
    sensitivity_input_dir = f"{sensitivity_dir}/{param}_inputs"
    if not output_dir:
        sensitivity_output_dir = f"{sensitivity_dir}/{param}_outputs"
    else:
        sensitivity_output_dir = output_dir

    # create directories
    Path(sensitivity_input_dir).mkdir(exist_ok=True)
    Path(sensitivity_output_dir).mkdir(exist_ok=True)

    bb_in = BackboneInput(input_file_gdx)
    bb_opt_fn = bb_in._path.stem + f"_100{param}_result.gdx"

    # run first optimisation i.e. 100% of `param`
    bb_out_path = run_backbone(
        bb_input_dir,
        input_file_gdx=bb_in._path,
        output_dir=sensitivity_output_dir,
        output_file=bb_opt_fn,
    )

    # from scripts.results import BackboneResult
    bb_result = BackboneResult(bb_out_path)
    bb_result.r_emission()

    emission_lims = bb_result.r_emission()["Val"].values * percentages
    # percentages,emission_lims

    for percentage, em_lim in zip(percentages, emission_lims):
        new_db = bb_in.update_gams_parameter_in_db(
            "p_groupPolicyEmission",
            ["emission group", "emissionCap", "CO2"],
            value=em_lim,
        )
        out_fn = Path(bb_in._path).stem + f"_{percentage*100:02.0f}{param}"
        Path(sensitivity_input_dir).mkdir(exist_ok=True)
        new_db.export(f"{sensitivity_input_dir}/{out_fn}.gdx")

    input_files = list(glob(f"{sensitivity_input_dir}/*.gdx"))
    result_paths = []

    if parallel:
        threads = os.cpu_count() - 1
        with ThreadPool(threads) as pool:
            jobs = []
            for file in input_files:
                job = pool.apply_async(
                    run_backbone, (bb_input_dir, file, sensitivity_output_dir)
                )
                jobs.append(job)
            result_paths = [job.get() for job in jobs]
    else:
        for file in input_files:
            path = run_backbone(bb_input_dir, file, sensitivity_output_dir)
            result_paths.append(path)

    return result_paths
