#-----------------------------------------------------------------------
# Name:        gistools (huff package)
# Purpose:     GIS tools
# Author:      Thomas Wieland 
#              ORCID: 0000-0001-5168-9846
#              mail: geowieland@googlemail.com              
# Version:     1.0.0
# Last update: 2025-04-25 18:16
# Copyright (c) 2025 Thomas Wieland
#-----------------------------------------------------------------------


import geopandas as gp 


def overlay_difference(
    polygon_gdf: gp.GeoDataFrame, 
    sort_col: str = None,
    ):

    if sort_col is not None:
        polygon_gdf = polygon_gdf.sort_values(by=sort_col).reset_index(drop=True)
    else:
        polygon_gdf = polygon_gdf.reset_index(drop=True)

    new_geometries = []
    new_data = []

    for i in range(len(polygon_gdf) - 1, 0, -1):
        current_polygon = polygon_gdf.iloc[i].geometry
        previous_polygon = polygon_gdf.iloc[i - 1].geometry
        difference_polygon = current_polygon.difference(previous_polygon)

        if difference_polygon.is_empty or not difference_polygon.is_valid:
            continue

        new_geometries.append(difference_polygon)
        new_data.append(polygon_gdf.iloc[i].drop("geometry"))

    inner_most_polygon = polygon_gdf.iloc[0].geometry
    if inner_most_polygon.is_valid:
        new_geometries.append(inner_most_polygon)
        new_data.append(polygon_gdf.iloc[0].drop("geometry"))

    polygon_gdf_difference = gp.GeoDataFrame(
        new_data, geometry=new_geometries, crs=polygon_gdf.crs
    )

    return polygon_gdf_difference