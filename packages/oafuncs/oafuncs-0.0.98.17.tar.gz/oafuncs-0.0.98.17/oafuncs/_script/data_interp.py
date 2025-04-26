import importlib.util
from typing import List, Union

import numpy as np
from scipy.interpolate import griddata

from oafuncs.oa_tool import PEx

# 检查 pykdtree 是否可用
_has_pykdtree = importlib.util.find_spec("pykdtree.kdtree") is not None


def _fill_nan_nearest(arr: np.ndarray) -> np.ndarray:
    """
    用最近邻填充 NaN（只支持2D数组）
    """
    # 基础检查：如果输入为None，直接返回None
    if arr is None:
        return None

    # 确保是2D ndarray
    arr = np.asarray(arr)
    if arr.ndim != 2:
        raise ValueError(f"_fill_nan_nearest 只支持2D数组，但输入的维度是 {arr.ndim}")

    # 保存原始dtype并转为float
    orig_dtype = arr.dtype
    arr = arr.astype(float, copy=True)  # 使用copy=True确保不修改原数据

    # 检查是否有NaN需要填充
    mask = np.isnan(arr)
    if not mask.any():
        return arr.copy()

    try:
        valid = np.array(np.where(~mask)).T
        invalid = np.array(np.where(mask)).T

        # 如果有效点为空，直接返回原数据
        if valid.shape[0] == 0:
            return arr.copy()

        # 使用KDTree进行最近邻填充
        if _has_pykdtree:
            from pykdtree.kdtree import KDTree

            tree = KDTree(valid)
            _, idx = tree.query(invalid, k=1)
            filled = arr.copy()
            filled[tuple(invalid.T)] = arr[tuple(valid[idx.flatten()].T)]
        else:
            # 备用方法：使用scipy的distance_transform_edt
            from scipy.ndimage import distance_transform_edt

            idx = distance_transform_edt(mask, return_distances=False, return_indices=True)
            filled = arr[tuple(idx)]

        return filled.astype(orig_dtype)
    except Exception as e:
        import warnings

        warnings.warn(f"Error in _fill_nan_nearest: {e}, shape={arr.shape}")
        return arr.copy()  # 发生异常返回原始数据


def _data_clip(data: np.ndarray, data_min, data_max) -> np.ndarray:
    """
    将数据裁剪至 [data_min, data_max]，超出或 NaN 用最近邻填补。
    支持 1~4D。
    """
    arr = np.array(data, copy=True)  # 使用副本避免修改原数据
    ndims = arr.ndim
    if ndims != 2:
        raise ValueError(f"_data_clip 只支持1~4维数组，但输入的维度是 {ndims}")
    dtype = arr.dtype

    # 检查是否需要裁剪
    mask = np.isnan(arr) | (arr < data_min) | (arr > data_max)
    if not np.any(mask):
        return arr.astype(dtype)

    # 将超出范围的值设为NaN
    arr[mask] = np.nan

    return _fill_nan_nearest(arr).astype(dtype)



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
