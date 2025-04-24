

# Importing the executors:

  For GetRasterExecutor:

    from iharp_query_executor.get_raster_api import GetRasterExecutor

  For GeoJsonExecutor:

    from iharp_query_executor.get_geojson_executor import GeoJsonExecutor

  For GetTimeseriesExecutor:

    from iharp_query_executor.get_timeseries_api import GeoTimeseriesExecutor

  For GetHeatmapExecutor:

    from iharp_query_executor.get_heatmap_api import GeoHeatmapExecutor

  For GetFindTimeExecutor:

    from iharp_query_executor.get_find_time_api import GeoFindTimeExecutor

  For GetFindAreaExecutor:

    from iharp_query_executor.get_find_area_api import GeoFindAreaExecutor


# To use the executors:

  Each function requires the variables shown inside the function to wy.
ork properl
  For GetRasterExecutor:

    raster = GetRasterExecutor(
        variable=variable,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        temporal_resolution=temporal_resolution,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        spatial_resolution=spatial_resolution,
        aggregation=aggregation,
    )

  For GeoJsonExecutor:

    geojson = GeoJsonExecutor(
        variable=variable,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        temporal_resolution=temporal_resolution,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        spatial_resolution=spatial_resolution,
        aggregation=aggregation,
        geojson_file=geojson_file
    )

  For GetTimeseriesExecutor:

    timeseries = GetTimeseriesExecutor(
        variable=variable,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        temporal_resolution=temporal_resolution,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        aggregation=aggregation,
    )
    

  For GetHeatMapExecutor:

    heatmap = GetHeatmapExecutor(
        variable=variable,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        spatial_resolution=spatial_resolution,
        aggregation=aggregation,
    )

  For GetFindTimeExecutor:
    
    ft = GetFindTimeExecutor(
        variable=variable,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        temporal_resolution=temporal_resolution,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        aggregation=aggregation,
        filter_predicate=filter_predicate,
        filter_value=filter_value
    )


For GetFindAreaExecutor:

  fa = GetFindAreaExecutor(
      variable=variable,
      start_datetime=start_datetime,
      end_datetime=end_datetime,
      min_lat=min_lat,
      max_lat=max_lat,
      min_lon=min_lon,
      max_lon=max_lon,
      spatial_resolution=spatial_resolution,
      aggregation=aggregation,
      filter_predicate=filter_predicate,
      filter_value=filter_value
  )
