"""Colorbased distance calculation on tiles."""

from __future__ import annotations

import os
import pathlib
import threading
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
from tqdm.contrib.concurrent import thread_map

from CDC.color_models import BaseDistance
from CDC.orthomosaic_tiler import OrthomosaicTiles, Tile


class TiledColorBasedDistance:
    """
    Calculate color based distance on tiled orthomosaic.

    Parameters
    ----------
    ortho_tiler
        An instance of :class:`~CDC.orthomosaic_tiler.OrthomosaicTiles`
    color_model
        The color model to use for distance calculations. See :mod:`~CDC.color_models`
    scale
        A scale factor to scale the calculated distances with.
    output_location
        Where output orthomosaic and tiles are saved.
    """

    def __init__(
        self,
        *,
        ortho_tiler: OrthomosaicTiles,
        color_model: BaseDistance,
        scale: float,
        output_location: pathlib.Path,
    ):
        self.ortho_tiler = ortho_tiler
        self.output_location = output_location
        self.colormodel = color_model
        self.output_scale_factor = scale
        self.ortho_tiler.divide_orthomosaic_into_tiles()

    @staticmethod
    def convertScaleAbs(image: np.ndarray, alpha: float) -> np.ndarray:
        """Scale image by alpha and take the absolute value."""
        scaled_img: np.ndarray = np.minimum(np.abs(alpha * image), 255)
        return scaled_img.astype(np.uint8)

    def process_tiles(self, save_tiles: bool = False, max_workers: int | None = os.cpu_count()) -> None:
        """
        Calculate color based distance on all tiles and save output.

        Parameters
        ----------
        save_tiles
            Save all tiles to output_location.
        max_workers
            Maximum number of threads to use for processing.
        """
        if max_workers is None:
            max_workers = 1
        read_lock = threading.Lock()
        write_lock = threading.Lock()
        process_lock = threading.Lock()
        output_filename = self.output_location.joinpath("orthomosaic.tiff")
        with rasterio.open(self.ortho_tiler.orthomosaic) as src:
            profile = src.profile
            profile["count"] = 1
            overview_factors = src.overviews(src.indexes[0])
            with rasterio.open(output_filename, "w", **profile) as dst:

                def process(tile: Tile) -> np.ndarray:
                    with read_lock:
                        img = src.read(window=tile.window_with_overlap)
                        mask_temp = src.read_masks(window=tile.window_with_overlap)
                    mask = mask_temp[0]
                    for band in range(mask_temp.shape[0]):
                        mask = mask & mask_temp[band]
                    with process_lock:  # Lock needed or running on windows crashes. see docs for further explanation.
                        distance_image = self.colormodel.calculate_distance(img)
                    distance = self.convertScaleAbs(distance_image, alpha=self.output_scale_factor)
                    output = tile.get_window_pixels(distance)
                    mask = tile.get_window_pixels(np.expand_dims(mask, 0)).squeeze()
                    if save_tiles:
                        tile.save_tile(distance, mask, self.output_location.joinpath("tiles"))
                    with write_lock:
                        dst.write(output, window=tile.window)
                        dst.write_mask(mask, window=tile.window)
                    masked_output = np.where(mask > 0, output, np.nan)
                    tile_histogram = self._calculate_tile_statistics(masked_output)
                    return tile_histogram

                tile_histograms = thread_map(process, self.ortho_tiler.tiles, max_workers=max_workers)

        self.histogram, self.mean_pixel_value = self._calculate_statistics(tile_histograms)
        with rasterio.open(output_filename, "r+") as dst:
            dst.build_overviews(overview_factors, Resampling.average)

    def _calculate_tile_statistics(self, image: np.ndarray) -> np.ndarray:
        if np.max(image) == np.min(image):
            return np.zeros(256)
        else:
            return np.histogram(image, bins=256, range=(0, 255))[0]

    def _calculate_statistics(self, tile_histograms: np.ndarray) -> tuple[np.ndarray, float]:
        image_statistics = np.zeros(256)
        for histogram in tile_histograms:
            image_statistics += histogram
        mean_divide = 0
        mean_sum = 0
        for x in range(0, 256):
            mean_sum += image_statistics[x] * x
            mean_divide += image_statistics[x]
        mean_pixel_value = mean_sum / mean_divide
        return image_statistics, mean_pixel_value

    def save_statistics(self, args: Any) -> None:
        """
        Calculate a histogram of the color based distance from all tiles.
        Save histogram in output_location/statistics with a txt file of metadata.
        """
        statistics_path = self.output_location.joinpath("statistics")
        print(f'Writing statistics to the folder "{statistics_path}"')
        # Plot histogram of pixel values
        plt.plot(self.histogram)
        plt.title("Histogram of pixel values")
        plt.xlabel("Pixel Value")
        plt.ylabel("Number of Pixels")
        histogram_filename = statistics_path.joinpath("Histogram of pixel values")
        output_directory = os.path.dirname(histogram_filename)
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        plt.savefig(histogram_filename, dpi=300)
        plt.close()
        with open(statistics_path.joinpath("statistics.txt"), "w") as f:
            f.write("Input parameters:\n")
            f.write(f" - Orthomosaic: {args.orthomosaic}\n")
            f.write(f" - Reference image: {args.reference}\n")
            f.write(f" - Annotated image: {args.annotated}\n")
            f.write(f" - Output scale factor: {args.scale}\n")
            f.write(f" - Tile sizes: {args.tile_size}\n")
            f.write(f" - Output tile location: {args.output_location}\n")
            f.write(f" - Method: {args.method}\n")
            f.write(f" - Parameter: {args.param}\n")
            f.write(f" - Date and time of execution: {datetime.now().replace(microsecond=0)}\n")
            f.write("\n\nOutput from run\n")
            f.write(" - Average color value of annotated pixels\n")
            f.write(f" - {self.colormodel.average}\n")
            f.write(" - Covariance matrix of the annotated pixels\n")
            f.write(" - " + str(self.colormodel.covariance).replace("\n", "\n   ") + "\n")
            f.write(f" - Mean pixel value: {self.mean_pixel_value}\n")
            f.write(f" - Number of tiles: {len(self.ortho_tiler.tiles)}\n")
