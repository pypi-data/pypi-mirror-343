#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-04-26 11:54:21
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-04-26 11:54:22
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\_script\\data_interp_geo.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""

import importlib.util
from typing import List, Union

import numpy as np
from scipy.interpolate import RectBivariateSpline

from oafuncs.oa_tool import PEx

_has_pykdtree = importlib.util.find_spec("pykdtree.kdtree") is not None


def fill_nan_nearest(arr):
    """用最近邻插值填充 NaN，优先用pykdtree加速"""
    mask = np.isnan(arr)
    if not mask.any():
        return arr
    if _has_pykdtree:
        from pykdtree.kdtree import KDTree

        valid_idx = np.array(np.where(~mask)).T
        nan_idx = np.array(np.where(mask)).T
        if len(valid_idx) == 0:
            # 全是nan，直接返回
            return arr
        tree = KDTree(valid_idx)
        dist, idx = tree.query(nan_idx, k=1)
        filled = arr.copy()
        # idx shape: (n_nan, 1)，valid_idx shape: (n_valid, ndim)
        # valid_idx[idx].T shape: (ndim, n_nan)
        filled[tuple(nan_idx.T)] = arr[tuple(valid_idx[idx.flatten()].T)]
        return filled
    else:
        from scipy.ndimage import distance_transform_edt

        idx = distance_transform_edt(mask, return_distances=False, return_indices=True)
        return arr[tuple(idx)]


def _interp_single_worker(*args):
    """
    单slice插值worker，参数为(data_slice, sx, sy, tx, ty, interpolation_method, data_min, data_max)
    """
    # 兼容PEx调用方式：args为tuple或list
    if len(args) == 1 and isinstance(args[0], (tuple, list)):
        args = args[0]
    data_slice, sx, sy, tx, ty, interpolation_method, data_min, data_max = args
    # 处理nan
    if np.isnan(data_slice).any():
        mask = np.isnan(data_slice)
        if mask.any():
            data_slice = fill_nan_nearest(data_slice)
    x1d = np.unique(sx[0, :])
    y1d = np.unique(sy[:, 0])
    if sx.shape != (len(y1d), len(x1d)) or sy.shape != (len(y1d), len(x1d)):
        from scipy.interpolate import griddata

        grid_points = np.column_stack((sx.ravel(), sy.ravel()))
        grid_values = data_slice.ravel()
        data_slice = griddata(grid_points, grid_values, (x1d[None, :], y1d[:, None]), method="linear")
    if interpolation_method == "linear":
        kx = ky = 1
    else:
        kx = ky = 3
    interp_func = RectBivariateSpline(y1d, x1d, data_slice, kx=kx, ky=ky)
    out = interp_func(ty[:, 0], tx[0, :])
    # 优化裁剪逻辑：超出范围的点设为nan，再用fill_nan_nearest填充
    arr = np.asarray(out)
    mask = np.isnan(arr) | (arr < data_min) | (arr > data_max)
    if np.any(mask):
        arr = np.where(mask, np.nan, arr)
        arr = fill_nan_nearest(arr)
    # 最后再填充nan（极端情况）
    if np.any(np.isnan(arr)):
        arr = fill_nan_nearest(arr)
    return arr


def interp_2d_geo(
    target_x_coordinates: Union[np.ndarray, List[float]],
    target_y_coordinates: Union[np.ndarray, List[float]],
    source_x_coordinates: Union[np.ndarray, List[float]],
    source_y_coordinates: Union[np.ndarray, List[float]],
    source_data: np.ndarray,
    interpolation_method: str = "cubic",
) -> np.ndarray:
    """
    更平滑的二维插值，采用RectBivariateSpline实现bicubic效果，接口与interp_2d兼容。
    支持输入2D/3D/4D数据，最后两维为空间。
    interpolation_method: "cubic"（默认，bicubic），"linear"（双线性）
    插值后自动裁剪并用最近邻填充超限和NaN，范围取原始数据的nanmin/nanmax
    """
    # 保证输入为ndarray
    tx = np.asarray(target_x_coordinates)
    ty = np.asarray(target_y_coordinates)
    sx = np.asarray(source_x_coordinates)
    sy = np.asarray(source_y_coordinates)
    data = np.asarray(source_data)

    if ty.ndim == 1:
        tx, ty = np.meshgrid(tx, ty)
    if sy.ndim == 1:
        sx, sy = np.meshgrid(sx, sy)

    if sx.shape != data.shape[-2:] or sy.shape != data.shape[-2:]:
        raise ValueError("Shape of source_data does not match shape of source_x_coordinates or source_y_coordinates.")

    data_dims = data.ndim
    if data_dims < 2:
        raise ValueError("Source data must have at least 2 dimensions.")
    elif data_dims > 4:
        raise ValueError("Source data has more than 4 dimensions, not supported.")

    num_dims_to_add = 4 - data_dims
    new_shape = (1,) * num_dims_to_add + data.shape
    data4d = data.reshape(new_shape)
    t, z, ny, nx = data4d.shape

    data_min, data_max = np.nanmin(data), np.nanmax(data)
    target_shape = ty.shape

    # 并行参数准备
    params = []
    for ti in range(t):
        for zi in range(z):
            params.append((data4d[ti, zi], sx, sy, tx, ty, interpolation_method, data_min, data_max))

    with PEx() as excutor:
        result = excutor.run(_interp_single_worker, params)

    result = np.array(result).reshape(t, z, *target_shape)
    result = np.squeeze(result)
    return result
