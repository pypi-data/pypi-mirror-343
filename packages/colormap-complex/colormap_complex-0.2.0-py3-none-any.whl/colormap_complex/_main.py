from pathlib import Path
from typing import Any, Literal, Protocol, TypeVar

import colour
import numpy as np
from numpy.typing import NDArray

TBase = TypeVar("TBase", bound=Any)
ColormapType = Literal[
    "oklab",
    "oklch",
    "prolab",
    "prolch",
    "hsv",
    "ycbcr",
    "bremm",
    "cubediagonal",
    "schumann",
    "steiger",
    "teulingfig2",
    "ziegler",
]
ALL_COLORMAPS: list[ColormapType] = [
    "oklab",
    "oklch",
    "prolab",
    "prolch",
    "hsv",
    "ycbcr",
    "bremm",
    "cubediagonal",
    "schumann",
    "steiger",
    "teulingfig2",
    "ziegler",
]
_CACHED_COLORMAPS: list[ColormapType] = [
    "bremm",
    "cubediagonal",
    "schumann",
    "steiger",
    "teulingfig2",
    "ziegler",
]


def interpnd(base: NDArray[TBase], *indices: NDArray[np.number]) -> NDArray[TBase]:
    """
    Interpolate a n-dimensional array.

    Parameters
    ----------
    base : NDArray[TBase]
        Array of shape B.
    indices : NDArray[np.number]
        Array of shape I.

    Returns
    -------
    NDArray[TBase]
        Interpolated array of shape (*I, B.shape[len(I):]).

    """
    indices_0 = tuple(np.floor(indices_i).astype(np.int32) for indices_i in indices)
    indices_1 = tuple(np.ceil(indices_i).astype(np.int32) for indices_i in indices)
    indices_p = np.prod(
        np.stack(indices, axis=0) - np.stack(indices_0, axis=0),
        axis=0,
    )[(...,) + (None,) * (base.ndim - len(indices))]
    return base[indices_0] * (1 - indices_p) + base[indices_1] * indices_p


class Colormap(Protocol):
    """Colormap protocol."""

    __name__: str

    def __call__(
        self,
        x: NDArray[np.number],
        y: NDArray[np.number],
        /,
        *,
        scale: bool = False,
    ) -> NDArray[np.number]:
        """
        Colormap function.

        Parameters
        ----------
        x : NDArray[np.number]
            Array of shape (...,)
        y : NDArray[np.number]
            Array of shape (...,)
        scale : bool
            Whether to scale the input to the range [0, 1].

        Returns
        -------
        NDArray[np.number]
            Colormap of shape (..., 3).
            The colormap is in the range [0, 1].
            If colormap is cyclic, x axis corresponds to the cyclic
            dimension.

        """


def colormap(
    *,
    type: Literal[
        "oklab",
        "oklch",
        "prolab",
        "prolch",
        "hsv",
        "ycbcr",
        "bremm",
        "cubediagonal",
        "schumann",
        "steiger",
        "teulingfig2",
        "ziegler",
    ] = "bremm",
    cut_outbound: bool = True,
    clip: bool = True,
) -> Colormap:
    """
    2D colormap function.

    Parameters
    ----------
    type : Literal['oklab', 'oklch', 'prolab', 'prolch', 'hsv', 'ycbcr',
        'bremm', 'cubediagonal', 'schumann', 'steiger', 'teulingfig2', 'ziegler']
        Type of colormap.
    cut_outbound : bool
        If using CIE XYZ, cut colors that are out of bounds
        for the sRGB color space.
    clip : bool
        Whether to clip the output to the range [0, 1].

    Returns
    -------
    Colrmap
        Colormap function.

    """
    if type not in ALL_COLORMAPS:
        raise ValueError(f"Unknown colormap: {type}. Available colormaps: {ALL_COLORMAPS}")
    if type in _CACHED_COLORMAPS:
        file = Path(__file__).parent / "data" / f"{type}.npy"
        if not file.exists():
            raise FileNotFoundError("Colormap file not found.")
        colormap = np.load(file) / 255
        # 512 x 512 x 3

    def inner(
        x: NDArray[np.number], y: NDArray[np.number], /, *, scale: bool = False
    ) -> NDArray[np.number]:
        if scale:
            xmin = np.min(x)
            xmax = np.max(x)
            ymin = np.min(y)
            ymax = np.max(y)
            x = (x - xmin) / (xmax - xmin)
            y = (y - ymin) / (ymax - ymin)
        x, y = np.broadcast_arrays(x, y)
        if type == "hsv":
            srgb = colour.HSL_to_RGB(np.stack([x, np.ones_like(x), 0.3 + 0.6 * y], axis=-1))
        elif type == "ycbcr":
            srgb = colour.YCbCr_to_RGB(np.stack([np.ones_like(x) * 0.5, x, y], axis=-1))
        elif type in ["oklab", "oklch", "prolab", "prolch"]:
            if type == "oklab":
                xyz = colour.Oklab_to_XYZ(
                    np.stack(
                        [0.7 * np.ones_like(x), 0.1 * (2 * x - 1), 0.14 * (2 * y - 1)],
                        axis=-1,
                    )
                )
            elif type == "oklch":
                # too black -> invisible, too bright -> out of bounds
                xyz = colour.Oklab_to_XYZ(
                    np.stack(
                        [
                            0.3 + 0.45 * y,
                            0.1 * np.cos(2 * np.pi * x),
                            0.1 * np.sin(2 * np.pi * x),
                        ],
                        axis=-1,
                    )
                )
            elif type == "prolab":
                xyz = colour.ProLab_to_XYZ(
                    np.stack(
                        [75 * np.ones_like(x), 15 * (2 * x - 1), 20 * (2 * y - 1)],
                        axis=-1,
                    )
                )
            elif type == "prolch":
                # too black -> invisible, too bright -> out of bounds
                xyz = colour.ProLab_to_XYZ(
                    np.stack(
                        [
                            20 + 70 * y,
                            17 * np.cos(2 * np.pi * x),
                            17 * np.sin(2 * np.pi * x),
                        ],
                        axis=-1,
                    )
                )
            srgb = colour.XYZ_to_sRGB(xyz)
            if cut_outbound:
                srgb[(np.abs(srgb) > 1).any(axis=-1)] = 0
        elif type in _CACHED_COLORMAPS:
            return interpnd(
                colormap,
                x * (colormap.shape[0] - 1),
                y * (colormap.shape[1] - 1),
            )
        else:
            raise AssertionError()
        if clip:
            srgb = np.clip(srgb, 0, 1)
        return srgb

    inner.__name__ = type
    inner.__doc__ = f"Colormap function of type {type}."
    return inner
