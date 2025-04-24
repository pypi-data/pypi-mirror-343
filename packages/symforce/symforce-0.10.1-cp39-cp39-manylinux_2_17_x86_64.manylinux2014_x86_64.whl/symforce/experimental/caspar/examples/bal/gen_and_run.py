# ----------------------------------------------------------------------------
# SymForce - Copyright 2025, Skydio, Inc.
# This source code is under the Apache 2.0 license found in the LICENSE file.
# ----------------------------------------------------------------------------

from dataclasses import dataclass
from pathlib import Path

import numpy as np

import symforce

symforce.set_epsilon_to_number(float(10 * np.finfo(np.float32).eps))

import symforce.symbolic as sf
from symforce import typing as T
from symforce.experimental.caspar import CasparLibrary
from symforce.experimental.caspar import memory as mem
from symforce.experimental.caspar.examples.bal.bal_loader import load_bal


@dataclass
class Cam:
    cam_T_world: sf.Pose3
    calibration: sf.V3


class Point(sf.V3):
    pass


class Pixel(sf.V2):
    pass


def huber_norm(e: sf.Expr, k: float) -> sf.Expr:
    other = sf.sqrt(k * (2 * e * sf.sign(e) - k)) * sf.sign(e)
    return sf.Piecewise((e, e * sf.sign(e) < k), (other, True))


caslib = CasparLibrary()


@caslib.add_factor
def fac_reprojection(
    cam: T.Annotated[Cam, mem.Tunable],
    point: T.Annotated[Point, mem.Tunable],
    pixel: T.Annotated[Pixel, mem.Constant],
) -> sf.V2:
    focal_length, k1, k2 = cam.calibration
    point_cam = cam.cam_T_world * point
    d = point_cam[2]
    p = -sf.V2(point_cam[:2]) / (d + sf.epsilon() * sf.sign_no_zero(d))
    r = 1 + k1 * p.squared_norm() + k2 * p.squared_norm() ** 2
    pixel_projected = focal_length * r * p
    err = pixel_projected - pixel
    return err


out_dir = Path(__file__).resolve().parent / "generated"
caslib.generate(out_dir)
caslib.compile(out_dir)

# Can also be imported using: lib = caslib.import_lib(out_dir)
from generated import caspar_lib as lib  # type: ignore[import-not-found]

problems = {
    "medium": "venice/problem-245-198739-pre.txt.bz2",
    "large": "venice/problem-1778-993923-pre.txt.bz2",
    "huge": "final/problem-13682-4456117-pre.txt.bz2",
}
cam_ids, point_ids, camdata, pointdata, pixels = load_bal(problems["large"])

params = lib.SolverParams()
params.diag_init = 1.0
params.solver_iter_max = 100
params.pcg_iter_max = 10
params.pcg_rel_error_exit = 1e-2

solver = lib.GraphSolver(
    params,
    Cam_num_max=camdata.shape[0],
    Point_num_max=pointdata.shape[0],
    fac_reprojection_num_max=pixels.shape[0],
)

solver.set_Cam_num(camdata.shape[0])
solver.set_Cam_nodes_from_stacked_host(camdata)
solver.set_Point_nodes_from_stacked_host(pointdata)

solver.set_fac_reprojection_cam_indices_from_host(cam_ids)
solver.set_fac_reprojection_point_indices_from_host(point_ids)
solver.finish_indices()

solver.set_fac_reprojection_pixel_data_from_stacked_host(pixels)

solver.solve(print_progress=True)

pointdata_out = np.empty_like(pointdata)
solver.get_Point_nodes_to_stacked_host(pointdata_out)

mean = pointdata_out.mean(0)
points_valid_zeroed = pointdata_out - mean
eig = np.linalg.eig(points_valid_zeroed.T @ points_valid_zeroed)
rot = np.linalg.inv(eig[1])

points_opt = points_valid_zeroed @ rot.T
points_old = (pointdata - mean) @ rot.T
