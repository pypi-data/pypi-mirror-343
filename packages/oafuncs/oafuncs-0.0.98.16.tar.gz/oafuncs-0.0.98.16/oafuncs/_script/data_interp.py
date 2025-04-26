import importlib.util
from typing import List, Union

import numpy as np
from oafuncs.oa_tool import PEx
from scipy.interpolate import griddata

_has_pykdtree = importlib.util.find_spec("pykdtree.kdtree") is not None


def _fill_nan_nearest(arr):
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


def _data_clip(data, data_min, data_max):
    """
    对data进行范围裁剪，超出范围的点设为nan，并用fill_nan_nearest填充，最后再次填充极端nan。
    """
    arr = np.asarray(data)
    mask = np.isnan(arr) | (arr < data_min) | (arr > data_max)
    if np.any(mask):
        arr = np.where(mask, np.nan, arr)
        arr = _fill_nan_nearest(arr)
    if np.any(np.isnan(arr)):
        arr = _fill_nan_nearest(arr)
    return arr


def _interp_single_worker(*args):
    """
    用于PEx并行的单slice插值worker，参数为(t, z, source_data, origin_points, target_points, interpolation_method, target_shape)
    """
    data_slice, origin_points, target_points, interpolation_method, target_shape = args

    # 过滤掉包含 NaN 的点
    valid_mask = ~np.isnan(data_slice.ravel())
    valid_data = data_slice.ravel()[valid_mask]
    valid_points = origin_points[valid_mask]

    if len(valid_data) < 10:  # 如果有效数据太少，用均值填充
        return np.full(target_shape, np.nanmean(data_slice))

    # 使用有效数据进行插值
    result = griddata(valid_points, valid_data, target_points, method=interpolation_method)
    result = result.reshape(target_shape)

    # 第二步：用data_clip裁剪并填充
    data_min, data_max = np.nanmin(data_slice), np.nanmax(data_slice)
    result = _data_clip(result, data_min, data_max)

    return result


def interp_2d_func(
    target_x_coordinates: Union[np.ndarray, List[float]],
    target_y_coordinates: Union[np.ndarray, List[float]],
    source_x_coordinates: Union[np.ndarray, List[float]],
    source_y_coordinates: Union[np.ndarray, List[float]],
    source_data: np.ndarray,
    interpolation_method: str = "cubic",
) -> np.ndarray:
    """
    Perform 2D interpolation on the last two dimensions of a multi-dimensional array.

    Args:
        target_x_coordinates (Union[np.ndarray, List[float]]): Target grid's x-coordinates.
        target_y_coordinates (Union[np.ndarray, List[float]]): Target grid's y-coordinates.
        source_x_coordinates (Union[np.ndarray, List[float]]): Original grid's x-coordinates.
        source_y_coordinates (Union[np.ndarray, List[float]]): Original grid's y-coordinates.
        source_data (np.ndarray): Multi-dimensional array with the last two dimensions as spatial.
        interpolation_method (str, optional): Interpolation method. Defaults to "cubic".
            >>> optional: 'linear', 'nearest', 'cubic', 'quintic', etc.
        use_parallel (bool, optional): Enable parallel processing. Defaults to True.

    Returns:
        np.ndarray: Interpolated data array.

    Raises:
        ValueError: If input shapes are invalid.

    Examples:
        >>> target_x_coordinates = np.array([1, 2, 3])
        >>> target_y_coordinates = np.array([4, 5, 6])
        >>> source_x_coordinates = np.array([7, 8, 9])
        >>> source_y_coordinates = np.array([10, 11, 12])
        >>> source_data = np.random.rand(3, 3)
        >>> result = interp_2d(target_x_coordinates, target_y_coordinates, source_x_coordinates, source_y_coordinates, source_data)
        >>> print(result.shape)  # Expected output: (3, 3)
    """
    if len(target_y_coordinates.shape) == 1:
        target_x_coordinates, target_y_coordinates = np.meshgrid(target_x_coordinates, target_y_coordinates)
    if len(source_y_coordinates.shape) == 1:
        source_x_coordinates, source_y_coordinates = np.meshgrid(source_x_coordinates, source_y_coordinates)

    if source_x_coordinates.shape != source_data.shape[-2:] or source_y_coordinates.shape != source_data.shape[-2:]:
        raise ValueError("[red]Shape of source_data does not match shape of source_x_coordinates or source_y_coordinates.[/red]")

    target_points = np.column_stack((np.array(target_x_coordinates).ravel(), np.array(target_y_coordinates).ravel()))
    origin_points = np.column_stack((np.array(source_x_coordinates).ravel(), np.array(source_y_coordinates).ravel()))

    data_dims = len(source_data.shape)
    # Ensure source_data is 4D for consistent processing (t, z, y, x)
    if data_dims < 2:
        raise ValueError(f"[red]Source data must have at least 2 dimensions, but got {data_dims}.[/red]")
    elif data_dims > 4:
        # Or handle cases with more than 4 dimensions if necessary
        raise ValueError(f"[red]Source data has {data_dims} dimensions, but this function currently supports only up to 4.[/red]")

    # Reshape to 4D by adding leading dimensions of size 1 if needed
    num_dims_to_add = 4 - data_dims
    new_shape = (1,) * num_dims_to_add + source_data.shape
    new_src_data = source_data.reshape(new_shape)

    t, z, y, x = new_src_data.shape

    params = []
    target_shape = target_y_coordinates.shape
    for t_index in range(t):
        for z_index in range(z):
            params.append((new_src_data[t_index, z_index], origin_points, target_points, interpolation_method, target_shape))

    with PEx() as excutor:
        result = excutor.run(_interp_single_worker, params)

    return np.squeeze(np.array(result).reshape(t, z, *target_shape))
