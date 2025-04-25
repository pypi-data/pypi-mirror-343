#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-03-30 11:16:29
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-04-25 14:23:10
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\_script\\netcdf_merge.py
Description
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""

import os
from typing import List, Optional, Union

import numpy as np
import xarray as xr

from oafuncs import pbar
import logging


def merge_nc(file_list: Union[str, List[str]], var_name: Optional[Union[str, List[str]]] = None, dim_name: Optional[str] = None, target_filename: Optional[str] = None) -> None:
    """
    Description:
        Merge variables from multiple NetCDF files along a specified dimension and write to a new file.
        If var_name is a string, it is considered a single variable; if it is a list and has only one element, it is also a single variable;
        If the list has more than one element, it is a multi-variable; if var_name is None, all variables are merged.

    Parameters:
        file_list: List of NetCDF file paths or a single file path as a string
        var_name: Name of the variable to be extracted or a list of variable names, default is None, which means all variables are extracted
        dim_name: Dimension name used for merging
        target_filename: Target file name after merging

    Example:
        merge(file_list, var_name='u', dim_name='time', target_filename='merged.nc')
        merge(file_list, var_name=['u', 'v'], dim_name='time', target_filename='merged.nc')
        merge(file_list, var_name=None, dim_name='time', target_filename='merged.nc')
    """
    from oafuncs._script.netcdf_write import save_to_nc

    if target_filename is None:
        target_filename = "merged.nc"

    # 确保目标路径存在
    target_dir = os.path.dirname(target_filename)
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if isinstance(file_list, str):
        file_list = [file_list]

    # 初始化变量名列表
    if var_name is None:
        with xr.open_dataset(file_list[0]) as ds:
            var_names = list(ds.variables.keys())
    elif isinstance(var_name, str):
        var_names = [var_name]
    elif isinstance(var_name, list):
        var_names = var_name
    else:
        raise ValueError("var_name must be a string, a list of strings, or None")

    # 初始化合并数据字典
    merged_data = {}

    for i, file in pbar(enumerate(file_list), description="Reading files", total=len(file_list)):
        with xr.open_dataset(file) as ds:
            for var in var_names:
                data_var = ds[var]
                if dim_name in data_var.dims:
                    merged_data.setdefault(var, []).append(data_var)
                elif var not in merged_data:
                    # 判断类型，时间类型用NaT填充
                    if np.issubdtype(data_var.dtype, np.datetime64):
                        merged_data[var] = data_var.fillna(np.datetime64("NaT"))
                    else:
                        merged_data[var] = data_var.fillna(0)

    for var in pbar(merged_data, description="Merging variables"):
        if isinstance(merged_data[var], list):
            # 判断类型，时间类型用NaT填充
            if np.issubdtype(merged_data[var][0].dtype, np.datetime64):
                merged_data[var] = xr.concat(merged_data[var], dim=dim_name).fillna(np.datetime64("NaT"))
            else:
                merged_data[var] = xr.concat(merged_data[var], dim=dim_name).fillna(0)

    if os.path.exists(target_filename):
        # print("Warning: The target file already exists. Removing it ...")
        logging.warning("The target file already exists. Removing it ...")
        os.remove(target_filename)

    save_to_nc(target_filename, xr.Dataset(merged_data))


# Example usage
if __name__ == "__main__":
    files_to_merge = ["file1.nc", "file2.nc", "file3.nc"]
    output_path = "merged_output.nc"
    merge_nc(files_to_merge, var_name=None, dim_name="time", target_filename=output_path)
