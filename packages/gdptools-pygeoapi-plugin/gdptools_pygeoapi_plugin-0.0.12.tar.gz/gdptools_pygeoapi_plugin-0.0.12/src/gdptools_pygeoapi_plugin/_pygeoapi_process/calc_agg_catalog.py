"""Calc_weights_catalog_proceess."""
import json
import logging
from typing import Any
from typing import Dict
from typing import Tuple

import geopandas as gpd
import pandas as pd
from gdptools import AggGen
from gdptools import ClimRCatData
from pygeoapi.process.base import BaseProcessor

# import tempfile
# from pathlib import Path

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "run_weights_catalog",
    "title": "run area-weighted aggregation",
    "description": """Run area-weighted aggredation using  OpenDAP endpoint and
        user-defined Features""",
    "jobControlOptions": ["sync-execute", "async-execute"],
    "keywords": ["area-weighted intersections"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-CA",
        }
    ],
    "inputs": {
        "cat_dict": {
            "title": "cat_dict",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "weights": {
            "title": "weights_json_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_file": {
            "title": "shape_file_json_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_crs": {
            "title": "shape_file_crs_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_poly_idx": {
            "title": "shape_poly_idx_string",
            "schema": {
                "type": "string",
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "start_date": {
            "title": "Beginning date to pull from openDAP endpoint",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "end_date": {
            "title": "Ending date to pull from openDAP endpoint",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
    },
    "outputs": {
        "aggregated_json": {
            "title": "json records file of aggregated values",
            "schema": {"type": "object", "contentMediaType": "application/parquet"},
        }
    },
    "example": {
        "inputs": {
            "cat_dict": (
                '{"aet": {"id": "terraclim", "asset": '
                '"agg_terraclimate_aet_1958_CurrentYear_GLOBE", "URL": '
                '"http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_terraclimate_aet_1958_CurrentYear_GLOBE.nc", '  # noqa: B950
                '"type": "opendap", "varname": "aet", "variable": "aet", "description": '
                '"water_evaporation_amount", "units": "mm", "model": null, "ensemble": null, '
                '"scenario": "total", "T_name": "time", "duration": "1958-01-01/2021-12-01", '
                '"interval": "1 months", "nT": 768.0, "X_name": "lon", "Y_name": "lat", "X1": '
                '-179.97916666666666, "Xn": 179.97916666666666, "Y1": 89.97916666666667, '
                '"Yn": -89.97916666666664, "resX": 0.041666666666666664, "resY": '
                '0.041666666666666664, "ncols": 8640.0, "nrows": 4320.0, "crs": '
                '"+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs", '
                '"toptobottom": false, "tiled": ""}, "pet": {"id": "terraclim", "asset": '
                '"agg_terraclimate_pet_1958_CurrentYear_GLOBE", "URL": '
                '"http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_terraclimate_pet_1958_CurrentYear_GLOBE.nc", '  # noqa: B950
                '"type": "opendap", "varname": "pet", "variable": "pet", "description": '
                '"water_potential_evaporation_amount", "units": "mm", "model": null, '
                '"ensemble": null, "scenario": "total", "T_name": "time", "duration": '
                '"1958-01-01/2021-12-01", "interval": "1 months", "nT": 768.0, "X_name": '
                '"lon", "Y_name": "lat", "X1": -179.97916666666666, "Xn": 179.97916666666666, '
                '"Y1": 89.97916666666667, "Yn": -89.97916666666664, "resX": '
                '0.041666666666666664, "resY": 0.041666666666666664, "ncols": 8640.0, '
                '"nrows": 4320.0, "crs": "+proj=longlat +a=6378137 +f=0.00335281066474748 '
                '+pm=0 +no_defs", "toptobottom": false, "tiled": ""}}'
            ),
            "weights": (
                '{"i":{"0":2,"1":1,"2":2,"3":1},'
                '"index":{"0":0,"1":1,"2":2,"3":3},'
                '"j":{"0":3,"1":3,"2":2,"3":2},'
                '"poly_idx":{"0":"1","1":"1","2":"1","3":"1"},'
                '"wght":{'
                '"0":0.138616567,"1":0.001795472,"2":0.7689606915,"3":0.0906272694}}'
            ),
            "shape_file": (
                '{"type": "FeatureCollection", "features": ['
                '{"id": "0", "type": "Feature", "properties": {'
                '"id": 1, "poly_idx": "1"}, "geometry": {'
                '"type": "Polygon", "coordinates": [['
                "[-70.60141212297273, 41.9262774500321], "
                "[-70.57199544021768, 41.91303994279233], "
                "[-70.5867037815952, 41.87626908934851], "
                "[-70.61906213262577, 41.889506596588284], "
                "[-70.60141212297273, 41.9262774500321]"
                "]]}}]}"
            ),
            "shape_crs": "4326",
            "shape_poly_idx": "poly_idx",
            "start_date": "1980-01-01",
            "end_date": "1980-12-31",
        }
    },
}


class GDPCalcAggCatalogProcessor(BaseProcessor):  # type: ignore
    """Run area-weighted grid-to-poly aggregation."""

    def __init__(self, processor_def: dict[str, Any]):
        """Initialize Processor.

        Args:
            processor_def (_type_): _description_
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute run_weights_catalog web service."""
        cat_dict = json.loads(str(data["cat_dict"]))
        wghts = json.loads(str(data["weights"]))
        shpfile_feat = json.loads(str(data["shape_file"]))
        shp_crs = str(data["shape_crs"])
        shp_poly_idx = str(data["shape_poly_idx"])
        start_date = str(data["start_date"])
        end_date = str(data["end_date"])
        period = [start_date, end_date]

        weights = pd.DataFrame.from_dict(wghts)
        shp_file = gpd.GeoDataFrame.from_features(shpfile_feat)
        shp_file.set_crs(shp_crs, inplace=True)

        LOGGER.info(f"cat_dict: {cat_dict}  type: {type(cat_dict)}\n")
        LOGGER.info(f"weights: {weights.head()} type: {type(weights)}\n")
        LOGGER.info(f"shp_file: {shp_file.head()} type: {type(shp_file)}\n")
        LOGGER.info(f"shp_poly_idx: {shp_poly_idx} type: {type(shp_poly_idx)}\n")
        LOGGER.info(f"start_date: {start_date} type: {type(start_date)}\n")
        LOGGER.info(f"end_date: {end_date} type: {type(end_date)}\n")

        user_data = ClimRCatData(
            cat_dict=cat_dict,
            f_feature=shp_file,
            id_feature=shp_poly_idx,
            period=period,
        )
        # tempdir = tempfile.TemporaryDirectory()
        agg_gen = AggGen(
            user_data=user_data,
            stat_method="masked_mean",
            agg_engine="serial",
            agg_writer="none",
            weights=weights,
        )
        ngdf, nvals = agg_gen.calculate_agg()
        for idx, (_key, value) in enumerate(agg_gen.agg_data.items()):
            gdf = ngdf
            param_values = value.cat_param
            t_coord = param_values.T_name
            units = param_values.units
            varname = param_values.varname
            time = value.da.coords[t_coord].values

            df_key = pd.DataFrame(data=nvals[_key].values, columns=gdf.index.T.values)

            df_key.insert(0, "units", [units] * df_key.shape[0])
            df_key.insert(0, "varname", [varname] * df_key.shape[0])
            df_key.insert(0, "time", time)

            if idx == 0:
                df = df_key
            else:
                df = pd.concat([df, df_key])
        df.reset_index(inplace=True)
        return "application/json", json.loads(
            df.to_json(date_format="iso", orient="index")
        )

    def __repr__(self):  # type: ignore
        """Return representation."""
        return f"<GDPCalcWeightsCatalogProcessor> {self.name}"
