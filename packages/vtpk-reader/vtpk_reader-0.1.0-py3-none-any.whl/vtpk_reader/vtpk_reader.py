from __future__ import annotations

import copy
import gzip
import json
import struct
import zipfile
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Callable, Iterable

import mapbox_vector_tile
import pyproj
import shapely


class VtpkError(Exception):
    pass


class Qttl(Enum):
    NW = 0
    NE = 1
    SW = 2
    SE = 3


class TileIndexTile:
    def __init__(
        self,
        parent: TileIndexTile | None,
        level: int,
        x: int,
        y: int,
        child_nw: TileIndexTile | None,
        child_ne: TileIndexTile | None,
        child_sw: TileIndexTile | None,
        child_se: TileIndexTile | None,
    ):
        self.parent = parent
        self.level = level
        assert self.level is not None
        self.x = x
        assert self.x is not None
        self.y = y
        assert self.y is not None
        self.index: int | None = None
        self.children = {
            qttl: child
            for qttl, child in {
                Qttl.NW: child_nw,
                Qttl.NE: child_ne,
                Qttl.SW: child_sw,
                Qttl.SE: child_se,
            }.items()
            if child is not None
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(L{self.level:02}:{self.x},{self.y})"

    @staticmethod
    def from_data(data, parent: TileIndexTile | None, level: int, x: int, y: int) -> TileIndexTile | None:
        if data == 0:
            return None
        elif data == 1:
            return TileIndexTile(
                parent=parent,
                level=level,
                x=x,
                y=y,
                child_nw=None,
                child_ne=None,
                child_sw=None,
                child_se=None,
            )
        elif isinstance(data, list):
            return TileIndexTile.from_list(data=data, level=level, x=x, y=y, grand_parent=parent)
        else:
            raise VtpkError("Unknown tilemap tile value {data}")

    @staticmethod
    def _make_parent_tile(
        parent_factory: Callable,
        level: int,
        parent_x: int,
        parent_y: int,
        children_data: list,
    ):
        assert len(children_data) == 4
        assert level is not None
        children = [
            TileIndexTile.from_data(
                data=datum,
                parent=None,
                level=level + 1,
                x=parent_x * 2 + (idx % 2),
                y=parent_y * 2 + (int(idx / 2)),
            )
            for idx, datum in enumerate(children_data)
        ]
        parent = parent_factory(children)
        for idx, child in enumerate(children):
            if child is not None:
                child.parent = parent
                child.index = idx
        return parent

    @classmethod
    def from_list(cls, data: list, level: int, x: int, y: int, grand_parent: TileIndexTile | None = None):
        return cls._make_parent_tile(
            parent_factory=lambda children: cls(grand_parent, level, x, y, *children),
            level=level,
            parent_x=x,
            parent_y=y,
            children_data=data,
        )


class TileIndexRoot(TileIndexTile):
    def __init__(self, nw, ne, sw, se):
        super().__init__(
            parent=None,
            level=0,
            x=0,
            y=0,
            child_nw=nw,
            child_ne=ne,
            child_sw=sw,
            child_se=se,
        )
        self.level = 0

    @classmethod
    def from_list(cls, data: list, *_):
        return cls._make_parent_tile(
            parent_factory=lambda children: cls(*children), level=0, parent_x=0, parent_y=0, children_data=data
        )


class TileIndex:
    """
    Class represending the quad tile tree stored in p12/tilemap/root.json in .vtpk vector tile caches
    """

    def __init__(self, index_data):
        self.root_tile = TileIndexRoot.from_list(index_data)


@dataclass
class TileIndexRecord:
    file_offset: int
    data_size: int


class TileBundleFile:
    """
    Class for reading .bundle files inside .vtpk packages
    """

    def __init__(self, bundle_stream):
        self.tiles = {}
        self.bundle_stream = bundle_stream
        (
            version,
            record_count,
            max_tile_size,
            offset_byte_count,
            slack_space,
            file_size,
            user_header_offset,
            user_header_size,
            legacy1,
            legacy2,
            legacy3,
            legacy4,
            index_size,
        ) = struct.unpack("iiiiqqqiiiiii", self.bundle_stream.read(64))
        assert version == 3
        assert index_size == 131072

        tile_index = struct.unpack("q" * 128 * 128, self.bundle_stream.read(8 * 128 * 128))
        for idx, tile_idx_record in enumerate(list(tile_index)):
            m = 2**40
            tile_offset = tile_idx_record % m
            tile_size = int(tile_idx_record / m)
            if tile_size > 0:
                tile_row = int(idx / 128)
                tile_column = int(idx % 128)
                self.tiles[(tile_row, tile_column)] = TileIndexRecord(tile_offset, tile_size)

    def read_tile_features(self, row, column):
        tile_index_record = self.tiles[(row, column)]
        self.bundle_stream.seek(tile_index_record.file_offset, 0)
        return mapbox_vector_tile.decode(
            gzip.decompress(self.bundle_stream.read(tile_index_record.data_size)),
            default_options={
                "y_coord_down": True,
            },
        )


class Vtpk:
    def __init__(self, file_path):
        self.compressed = zipfile.ZipFile(file_path, "r")
        try:
            with self.compressed.open("p12/tilemap/root.json") as tilemap_root_json:
                self.root_tile = TileIndexRoot.from_list(json.loads(tilemap_root_json.read())["index"])
            with self.compressed.open("p12/root.json") as root_properties_json:
                self.root_properties = json.loads(root_properties_json.read())
            self.lod_resolutions = {}
            for lod_info in self.root_properties["tileInfo"]["lods"]:
                self.lod_resolutions[lod_info["level"]] = lod_info["resolution"]
            self._crs = pyproj.CRS(self.root_properties["tileInfo"]["spatialReference"]["latestWkid"])
            for axis in self._crs.axis_info:
                if axis.direction.upper() in {"EAST", "WEST"}:
                    self.x_axis = axis
                elif axis.direction.upper() in {"NORTH", "SOUTH"}:
                    self.y_axis = axis
                else:
                    raise VtpkError(f"Unrecognized axis direction ${axis.direction}")
        except KeyError as e:
            raise VtpkError(
                "Didn't find an expected file in zip archive. Maybe this is not an Esri Vector Tile Package file?"
            ) from e

    @property
    def crs(self) -> pyproj.CRS:
        return self._crs

    @property
    def min_lod(self) -> int:
        return self.root_properties["minLOD"]

    @property
    def max_lod(self) -> int:
        return self.root_properties["maxLOD"]

    @cached_property
    def x_size(self) -> float:
        return self.root_properties["fullExtent"]["xmax"] - self.root_properties["fullExtent"]["xmin"]

    @cached_property
    def y_size(self) -> float:
        return self.root_properties["fullExtent"]["ymax"] - self.root_properties["fullExtent"]["ymin"]

    @cached_property
    def _y_sign(self) -> int:
        if self.y_axis.direction.upper() == "SOUTH":
            return 1
        elif self.y_axis.direction.upper() == "NORTH":
            return -1
        else:
            raise VtpkError(f"Unrecognized axis direction ${self.y_axis.direction}")

    def _tile_coord_xform_function(
        self, tile: TileIndexTile, tile_extent: int
    ) -> Callable[[float, float], tuple[float, float]]:
        """
        Returns a function to transform coords from tile-internal coordinate system
        to the coords in the CRS specified in this file
        """
        tile_cols = self.root_properties["tileInfo"]["cols"]
        tile_rows = self.root_properties["tileInfo"]["rows"]
        tile_resolution = self.lod_resolutions[tile.level]
        tile_origin_x = self.root_properties["tileInfo"]["origin"]["x"] + tile_resolution * tile_cols * tile.x
        tile_origin_y = (
            self.root_properties["tileInfo"]["origin"]["y"] + tile_resolution * tile_rows * tile.y * self._y_sign
        )
        y_sign = self._y_sign

        def xform_coord(x: float, y: float) -> tuple[float, float]:
            result = (
                tile_origin_x + x / tile_extent * tile_cols * tile_resolution,
                tile_origin_y + y / tile_extent * tile_rows * tile_resolution * y_sign,
            )
            return result

        return xform_coord

    def tile_bounds(self, tile: TileIndexTile) -> tuple[float, float, float, float]:
        xform = self._tile_coord_xform_function(tile, 1)
        minx, miny = xform(0, 0)
        maxx, maxy = xform(1, 1)
        return (minx, miny, maxx, maxy)

    def _get_tiles(
        self, tile: TileIndexTile, lods: Iterable[int], bound_box: shapely.Polygon | None
    ) -> Iterable[TileIndexTile]:
        tile_bounds = self.tile_bounds(tile)
        if bound_box is not None:
            intersection = shapely.box(*tile_bounds).intersection(bound_box)
            proceed = intersection is not None and not intersection.is_empty
        else:
            proceed = True
        if proceed:
            result = {tile} if tile.level in lods else set()
            result |= {tile for child in tile.children.values() for tile in self._get_tiles(child, lods, bound_box)}
            return result
        else:
            return []

    def _check_lods(self, lods: Iterable[int]):
        for lod in lods:
            if lod < self.min_lod or lod > self.max_lod:
                raise VtpkError(f"LOD {lod} is out of range (min is {self.min_lod}, max {self.max_lod})")

    def get_tiles(self, lods: Iterable[int], bound_box: shapely.Polygon | None):
        self._check_lods(lods)
        return self._get_tiles(self.root_tile, lods, bound_box)

    def _tile_raw_features(self, tile: TileIndexTile):
        tile_file_c = int(tile.x / 128) * 128
        tile_file_r = int(tile.y / 128) * 128
        bundle_filename = f"p12/tile/L{tile.level:02}/R{tile_file_r:04x}C{tile_file_c:04x}.bundle"
        with self.compressed.open(bundle_filename) as bundle_file_stream:
            bundle_file = TileBundleFile(bundle_file_stream)
            tile_in_file_c = tile.x % 128
            tile_in_file_r = tile.y % 128
            return bundle_file.read_tile_features(tile_in_file_r, tile_in_file_c)

    def tile_features(self, tile: TileIndexTile):
        feature_dict = self._tile_raw_features(tile)

        def convert_feature(feature, extent):
            shapely_geometry = shapely.ops.transform(
                self._tile_coord_xform_function(tile, extent),
                shapely.geometry.shape(feature["geometry"]),
            )
            updated_feature = copy.deepcopy(feature)
            updated_feature["geometry"] = shapely_geometry
            return updated_feature

        def convert_featureset(featureset):
            feature_list = featureset["features"]
            extent = featureset["extent"]
            featureset["features"] = [convert_feature(feature, extent) for feature in feature_list]
            return featureset

        return {key: convert_featureset(val) for key, val in feature_dict.items()}
