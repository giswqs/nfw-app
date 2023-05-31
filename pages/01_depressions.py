import ee
import geemap

import solara

zoom = solara.reactive(4)
center = solara.reactive([40, -100])


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_data()
        self.add_layer_manager(opened=False)
        names = ["NED 10m", "NHD-HU8 Vector"]
        self.add_inspector(names=names, visible=False, opened=True)

    def add_data(self):
        self.setCenter(-99.00, 47.01, 8)

        ned = ee.Image("USGS/3DEP/10m")
        hillshade = ee.Terrain.hillshade(ned)

        conus = ee.Geometry.BBox(-127.18, 19.39, -62.75, 51.29)

        huc8 = ee.FeatureCollection("USGS/WBD/2017/HUC08").filterBounds(conus)
        pipestem_hu8 = ee.FeatureCollection("users/giswqs/Pipestem/Pipestem_HUC8")

        style = {"color": "00000088", "fillColor": "00000000", "width": 1}

        palette = ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"]
        self.addLayer(
            ned, {'min': 0, 'max': 4000, 'palette': palette}, 'NED 10m', False
        )
        self.addLayer(hillshade, {}, "NED Hillshade", False)

        states = ee.FeatureCollection("TIGER/2018/States")
        floodplain = ee.FeatureCollection('users/giswqs/floodplain/GFP250m')

        gfplain250 = ee.Image("projects/sat-io/open-datasets/GFPLAIN250/NA")
        states = ee.FeatureCollection('users/giswqs/public/us_states')
        fp_image = gfplain250.clipToCollection(states)
        self.addLayer(fp_image, {'palette': "#002B4D"}, 'Floodplain raster', False)

        fp_style = {'fillColor': '0000ff88'}
        self.addLayer(floodplain.style(**fp_style), {}, 'Floodplain vector', False)
        self.addLayer(huc8, {}, "NHD-HU8 Vector", False)
        self.addLayer(huc8.style(**style), {}, "NHD-HU8")
        self.addLayer(
            pipestem_hu8.style(
                **{"color": "ffff00ff", "fillColor": "00000000", "width": 2}
            ),
            {},
            "Pipestem HU8",
        )

    def add_ee_data(self):
        # Add Earth Engine dataset
        dem = ee.Image('USGS/SRTMGL1_003')
        landsat7 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003').select(
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        )
        states = ee.FeatureCollection("TIGER/2018/States")

        # Set visualization parameters.
        vis_params = {
            'min': 0,
            'max': 4000,
            'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'],
        }

        # Add Earth Engine layers to Map
        self.addLayer(dem, vis_params, 'SRTM DEM', True, 0.5)
        self.addLayer(
            landsat7,
            {'bands': ['B4', 'B3', 'B2'], 'min': 20, 'max': 200, 'gamma': 2.0},
            'Landsat 7',
            False,
        )
        self.addLayer(states, {}, "US States")


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(  # type: ignore
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            scroll_wheel_zoom=True,
            add_google_map=True,
            height="800px",
        )
