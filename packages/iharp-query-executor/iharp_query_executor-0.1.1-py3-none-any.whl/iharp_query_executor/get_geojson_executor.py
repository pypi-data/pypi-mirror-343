import xarray as xr
import geopandas as gpd
import numpy as np
from shapely.vectorized import contains
import matplotlib.pyplot as plt

from .get_raster_api import GetRasterExecutor

class GeoJsonExecutor(GetRasterExecutor):
    def __init__(
        self,
        variable: str,
        start_datetime: str,
        end_datetime: str,
        temporal_resolution: str,
        spatial_resolution: float,
        aggregation,
        geojson_file,
        min_lat: float = None,
        max_lat: float = None,
        min_lon: float = None,
        max_lon: float = None,
    ):
        super().__init__(
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
        self.geojson_file = geojson_file
        self.gdf = self._load_geojson()
        self.polygon = self.gdf.geometry.iloc[0]
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = self.polygon.bounds

    def _load_geojson(self):
        with open(self.geojson_file, 'r') as file:
            gdf = gpd.read_file(file)
        return gdf

    def _extract_coordinates(self, geojson_data):
        coords = []
        coords.extend(geojson_data["coordinates"])
        return coords
    
    def _create_boudning_box(self, coordinates):
        longs = []
        lats = []
        for coord in coordinates:
            longs.append(coord[0])
            lats.append(coord[1])
        return min(longs), min(lats), max(longs), max(lats)
    
    def _mask_raster_data(self, raster, polygon):
        lons = raster["longitude"].values
        lats = raster["latitude"].values
        mesh_lons, mesh_lats = np.meshgrid(lons, lats) # maybe add indexing='ij'
        points = np.vstack((mesh_lons.ravel(), mesh_lats.ravel())).T

        mask = contains(polygon, points[:, 0], points[:, 1])
        
        mask = np.array(mask)
        
        mask = mask.reshape(mesh_lons.shape)
        mask_da = xr.DataArray(mask, dims=["latitude", "longitude"], coords={"latitude": lats, "longitude": lons})

        masked_data = raster.where(mask_da, drop=False)

        return masked_data
    
    def visualize(self):

        raster = GetRasterExecutor(
            variable=self.variable,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            temporal_resolution=self.temporal_resolution,
            min_lat=self.min_lat,
            max_lat=self.max_lat,
            min_lon=self.min_lon,
            max_lon=self.max_lon,
            spatial_resolution=self.spatial_resolution,
            aggregation=self.aggregation
        )

        original_data = raster.execute()
        masked_raster = self._mask_raster_data(original_data, self.polygon)


        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        plt1 = axs[0].pcolormesh(original_data.longitude, original_data.latitude, original_data.t2m.isel(valid_time=0))
        axs[0].set_title("Original Raster Data")
        fig.colorbar(plt1, ax=axs[0])

        plt2 = axs[1].pcolormesh(masked_raster.longitude, masked_raster.latitude, masked_raster.t2m.isel(valid_time=0), cmap="binary") 
        axs[1].set_title("Mask")
        fig.colorbar(plt2, ax=axs[1])

        plt3 = axs[2].pcolormesh(masked_raster.longitude, masked_raster.latitude, masked_raster.t2m.isel(valid_time=0))
        axs[2].set_title("Masked Data")
        fig.colorbar(plt3, ax=axs[2])

        for ax in axs:
            x, y = self.polygon.exterior.xy
            ax.plot(x, y, color="red")
        plt.tight_layout()
        plt.savefig("data_plot.png")
        plt.show()
        plt.close()
    
    def execute(self):

        raster = GetRasterExecutor(
            variable=self.variable,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            temporal_resolution=self.temporal_resolution,
            min_lat=self.min_lat,
            max_lat=self.max_lat,
            min_lon=self.min_lon,
            max_lon=self.max_lon,
            spatial_resolution=self.spatial_resolution,
            aggregation=self.aggregation
        )
        original_data = raster.execute()
        masked_data = self._mask_raster_data(original_data, self.polygon)
        # print(masked_data)
        #self._visualize_mask()
        original_count = np.sum(~np.isnan(original_data.t2m.values))
        masked_count = np.sum(~np.isnan(masked_data.t2m.values))
        
        if original_count == masked_count:
            print("Mask Failed: Same number of valid points before and after masking")
        else:
            print(f"Mask Succeeded: Reduced from {original_count} to {masked_count} points")
        # masked_data = masked_data.dropna(dim="valid_time")
        # fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        # axes_flat = axs.flatten()

        # for i in range(4):
        #     im = axes_flat[i].pcolormesh(masked_data.longitude, masked_data.latitude, masked_data["t2m"][i,:,:])
        #     axes_flat[i].set_title(f'Slice {i}')
            
        # fig.colorbar(im, ax=axes_flat[0])
        # fig.colorbar(im, ax=axes_flat[1])
        # fig.colorbar(im, ax=axes_flat[2])
        # fig.colorbar(im, ax=axes_flat[3])
        # plt.tight_layout()
        # plt.show()
        return masked_data
        