

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



  Each function requires the variables shown inside the function to work properly.

# GetRasterExecutor:

  Code for the GetRasterExecutor function:

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

    To run the executor function:

      raster.executr()

# GeoJsonExecutor:
  
  The GeoJsonExecutor has an execute function like the rest but also a visualize function that will save a visualization of the data and masked data to a file called data_plot.png.

  Code for the GeoJsonExecutor function:

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
  
  To run the executor and visualize function:

    geojson.execute()
    geojson.visualize()

# GetTimeseriesExecutor:

  Code for the GetTimeseriesExecutor function:

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
    
  To run the executor function:

    timeseries.execute()

# GetHeatMapExecutor:

  Code for the GetHeatmapExecutor function:

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
  
  To run the executor function:

    heatmap.execute()


# GetFindTimeExecutor:

  Code for the GetFindTimeExecutor function:
    
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

  To run the executor function:

    ft.execute()


# GetFindAreaExecutor:

  Code for the GetFindAreaExecutor function:

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

  To run the executor function:

    fa.execute()