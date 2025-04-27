import os
import warnings

import netCDF4 as nc
import numpy as np
import xarray as xr

warnings.filterwarnings("ignore", category=RuntimeWarning)


def _nan_to_fillvalue(ncfile):
    """
    将 NetCDF 文件中所有变量的 NaN 和掩码值替换为其 _FillValue 属性（若无则自动添加 _FillValue=-32767 并替换）。
    同时处理掩码数组中的无效值。
    仅对数值型变量（浮点型、整型）生效。
    """
    with nc.Dataset(ncfile, "r+") as ds:
        for var_name in ds.variables:
            var = ds.variables[var_name]
            # 只处理数值类型变量 (f:浮点型, i:有符号整型, u:无符号整型)
            if var.dtype.kind not in ["f", "i", "u"]:
                continue

            # 读取数据
            arr = var[:]

            # 确定填充值
            if "_FillValue" in var.ncattrs():
                fill_value = var.getncattr("_FillValue")
            else:
                fill_value = -32767
                try:
                    var.setncattr("_FillValue", fill_value)
                except Exception:
                    # 某些变量可能不允许动态添加 _FillValue
                    continue

            # 处理掩码数组
            if hasattr(arr, "mask"):
                # 如果是掩码数组，将掩码位置的值设为 fill_value
                if np.any(arr.mask):
                    # 转换为普通数组，掩码位置填入 fill_value
                    arr = np.ma.filled(arr, fill_value=fill_value)

            # 处理剩余NaN值
            if np.any(np.isnan(arr)):
                arr = np.nan_to_num(arr, nan=fill_value, posinf=fill_value, neginf=fill_value)

            # 写回变量
            var[:] = arr


def _numpy_to_nc_type(numpy_type):
    """将 NumPy 数据类型映射到 NetCDF 数据类型"""
    numpy_to_nc = {
        "float32": "f4",
        "float64": "f8",
        "int8": "i1",
        "int16": "i2",
        "int32": "i4",
        "int64": "i8",
        "uint8": "u1",
        "uint16": "u2",
        "uint32": "u4",
        "uint64": "u8",
    }
    numpy_type_str = str(numpy_type) if not isinstance(numpy_type, str) else numpy_type
    return numpy_to_nc.get(numpy_type_str, "f4")


def _calculate_scale_and_offset(data, n=16):
    """
    计算数值型数据的 scale_factor 与 add_offset，
    将数据映射到 [0, 2**n - 1] 的范围。
    同时处理数据中的 NaN 值。
    """
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")

    # 先处理数据中的 NaN 和无穷值
    clean_data = np.nan_to_num(data, nan=-32767, posinf=np.finfo(float).max, neginf=np.finfo(float).min)

    # 计算有效值的最小最大值（排除填充值）
    valid_mask = clean_data != -32767
    if np.any(valid_mask):
        data_min = np.min(clean_data[valid_mask])
        data_max = np.max(clean_data[valid_mask])
    else:
        # 全都是填充值的情况，使用默认范围
        data_min, data_max = 0, 1

    if data_max == data_min:
        scale_factor = 1.0
        add_offset = data_min
    else:
        scale_factor = (data_max - data_min) / (2**n - 1)
        add_offset = data_min + 2 ** (n - 1) * scale_factor
    return scale_factor, add_offset


def _data_to_scale_offset(data, scale, offset):
    """
    将数据转换为 scale_factor 和 add_offset 的形式。
    此处同时替换 NaN、正无穷和负无穷为填充值 -32767，
    以确保转换后的数据可安全转为 int16。
    """
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")

    # 先计算转换后的数据
    result = np.around((data - offset) / scale)
    # 替换 NaN, 正负无穷（posinf, neginf）为 -32767
    result = np.nan_to_num(result, nan=-32767, posinf=-32767, neginf=-32767)
    result = np.clip(result, -32767, 32767)  # 限制范围在 int16 的有效范围内
    result = np.where(np.isfinite(result), result, -32767)  # 替换无效值为 -32767
    new_data = result.astype(np.int16)
    return new_data


def save_to_nc(file, data, varname=None, coords=None, mode="w", scale_offset_switch=True, compile_switch=True):
    """
    保存数据到 NetCDF 文件，支持 xarray 对象（DataArray 或 Dataset）和 numpy 数组。

    仅对数据变量中数值型数据进行压缩转换（利用 scale_factor/add_offset 转换后转为 int16），
    非数值型数据以及所有坐标变量将禁用任何压缩，直接保存原始数据。

    参数：
      - file: 保存文件的路径
      - data: xarray.DataArray、xarray.Dataset 或 numpy 数组
      - varname: 变量名（仅适用于传入 numpy 数组或 DataArray 时）
      - coords: 坐标字典（numpy 数组分支时使用），所有坐标变量均不压缩
      - mode: "w"（覆盖）或 "a"（追加）
      - scale_offset_switch: 是否对数值型数据变量进行压缩转换
      - compile_switch: 是否启用 NetCDF4 的 zlib 压缩（仅针对数值型数据有效）
    """
    # 处理 xarray 对象（DataArray 或 Dataset）的情况
    if isinstance(data, (xr.DataArray, xr.Dataset)):
        encoding = {}  # 用于保存数据变量的编码信息

        if isinstance(data, xr.DataArray):
            if data.name is None:
                data = data.rename("data")
            varname = data.name if varname is None else varname
            # 判断数据是否为数值型
            if np.issubdtype(data.values.dtype, np.number) and scale_offset_switch:
                scale, offset = _calculate_scale_and_offset(data.values)
                new_values = _data_to_scale_offset(data.values, scale, offset)
                # 生成新 DataArray，保留原坐标和属性，同时写入转换参数到属性中
                new_da = data.copy(data=new_values)
                new_da.attrs["scale_factor"] = float(scale)
                new_da.attrs["add_offset"] = float(offset)
                encoding[varname] = {
                    "zlib": compile_switch,
                    "complevel": 4,
                    "dtype": "int16",
                    "_FillValue": -32767,
                }
                new_da.to_dataset(name=varname).to_netcdf(file, mode=mode, encoding=encoding)
            else:
                data.to_dataset(name=varname).to_netcdf(file, mode=mode)
            _nan_to_fillvalue(file)  # 替换 NaN 为 _FillValue
            return

        else:
            # 处理 Dataset 的情况，仅处理 data_vars 数据变量，坐标变量保持原样
            new_vars = {}
            encoding = {}
            for var in data.data_vars:
                da = data[var]
                if np.issubdtype(np.asarray(da.values).dtype, np.number) and scale_offset_switch:
                    scale, offset = _calculate_scale_and_offset(da.values)
                    new_values = _data_to_scale_offset(da.values, scale, offset)
                    new_da = xr.DataArray(new_values, dims=da.dims, coords=da.coords, attrs=da.attrs)
                    new_da.attrs["scale_factor"] = float(scale)
                    new_da.attrs["add_offset"] = float(offset)
                    new_vars[var] = new_da
                    encoding[var] = {
                        "zlib": compile_switch,
                        "complevel": 4,
                        "dtype": "int16",
                        "_FillValue": -32767,
                    }
                else:
                    new_vars[var] = da
            new_ds = xr.Dataset(new_vars, coords=data.coords)
            if encoding:
                new_ds.to_netcdf(file, mode=mode, encoding=encoding)
            else:
                new_ds.to_netcdf(file, mode=mode)
        _nan_to_fillvalue(file)  # 替换 NaN 为 _FillValue
        return

    # 处理纯 numpy 数组情况
    if mode == "w" and os.path.exists(file):
        os.remove(file)
    elif mode == "a" and not os.path.exists(file):
        mode = "w"
    data = np.asarray(data)
    is_numeric = np.issubdtype(data.dtype, np.number)
    try:
        with nc.Dataset(file, mode, format="NETCDF4") as ncfile:
            # 坐标变量直接写入，不做压缩
            if coords is not None:
                for dim, values in coords.items():
                    if dim not in ncfile.dimensions:
                        ncfile.createDimension(dim, len(values))
                        var_obj = ncfile.createVariable(dim, _numpy_to_nc_type(np.asarray(values).dtype), (dim,))
                        var_obj[:] = values

            dims = list(coords.keys()) if coords else []
            if is_numeric and scale_offset_switch:
                scale, offset = _calculate_scale_and_offset(data)
                new_data = _data_to_scale_offset(data, scale, offset)
                var = ncfile.createVariable(varname, "i2", dims, fill_value=-32767, zlib=compile_switch)
                var.scale_factor = scale
                var.add_offset = offset
                # Ensure no invalid values in new_data before assignment
                var[:] = new_data
            else:
                # 非数值型数据，禁止压缩
                dtype = _numpy_to_nc_type(data.dtype)
                var = ncfile.createVariable(varname, dtype, dims, zlib=False)
                var[:] = data
        _nan_to_fillvalue(file)  # 替换 NaN 为 _FillValue
    except Exception as e:
        raise RuntimeError(f"netCDF4 保存失败: {str(e)}") from e


# 测试用例
if __name__ == "__main__":
    # --------------------------------
    # dataset
    file = r"F:\roms_rst.nc"
    ds = xr.open_dataset(file)
    outfile = r"F:\roms_rst_test.nc"
    save_to_nc(outfile, ds)
    ds.close()
    # --------------------------------
    # dataarray
    data = np.random.rand(4, 3, 2)
    coords = {"x": np.arange(4), "y": np.arange(3), "z": np.arange(2)}
    varname = "test_var"
    data = xr.DataArray(data, dims=("x", "y", "z"), coords=coords, name=varname)
    outfile = r"F:\test_dataarray.nc"
    save_to_nc(outfile, data)
    # --------------------------------
    # numpy array
    data = np.random.rand(4, 3, 2)
    coords = {"x": np.arange(4), "y": np.arange(3), "z": np.arange(2)}
    varname = "test_var"
    outfile = r"F:\test_numpy.nc"
    save_to_nc(outfile, data, varname=varname, coords=coords)
    # --------------------------------
