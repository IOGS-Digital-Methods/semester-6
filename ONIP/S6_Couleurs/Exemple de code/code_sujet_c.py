# %%
__author__ = "Corentin Nannini"

import skimage.color
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum
import matplotlib
import scipy.linalg

#  colour-science package only used for CIE 1931 diagram construction
import colour


class ColorSpace(Enum):
    """Enumeration Base class restrict the possible values
    This simplifies the use of the class and the attributes available
    (in this case, color spaces) thanks to the IDE.
    """

    RGB = 1
    Lab = 2
    XYZ = 3


class Color:
    """The `Color` class represents a color in different color spaces (XYZ, Lab, RGB) and provides methods to convert between them."""

    def __init__(
        self,
        color_coordinates: np.ndarray | list,
        colorspace: ColorSpace,
        illuminant="D65",
    ) -> None:
        """Constructor of Color Class

        Args:
            color_coordinates (np.ndarray | list): should be float arraylike with 3 components
            colorspace (ColorSpace): Specify the ColorSpace in which color_coordinates is expressed
            illuminant (str, optional): Ony usefull if the color space is Lab. Defaults to "D65".
        """
        if isinstance(color_coordinates, (list, tuple)):
            color_coordinates = np.array(color_coordinates)

        assert len(color_coordinates) == 3, f"{color_coordinates = } is not size 3"

        if colorspace is ColorSpace.XYZ:
            self.xyz_coordinates = color_coordinates
        elif colorspace is ColorSpace.Lab:
            self.xyz_coordinates = skimage.color.lab2xyz(
                color_coordinates, illuminant=illuminant
            )
        elif colorspace is ColorSpace.RGB:
            self.xyz_coordinates = skimage.color.rgb2xyz(color_coordinates)

    def to_lab(self, illuminant="D65") -> np.ndarray:
        return skimage.color.xyz2lab(self.xyz_coordinates, illuminant=illuminant)

    def to_rgb(self) -> np.ndarray:
        return skimage.color.xyz2rgb(self.xyz_coordinates)

    def __repr__(self) -> str:
        (x, y, z) = self.xyz_coordinates
        return f"Color (X, Y, Z) = {x:.3}, {y:.3}, {z:.3}"


@dataclass
class ColorPatch:
    """ColorPatch class represents a color patch with a name, coordinates, and color.

    Example :
    >>> patch = ColorPatch('B4', [1, 3], Color([.3, .2, .5], ColorSpace.RGB))
    >>> print(patch)
        ColorPatche B4 located at [1, 3] - XYZ == 0.0807, 0.0547, 0.209
    """

    name: str
    xy: tuple[int, int]
    color: Color

    def __repr__(self) -> str:
        (x, y, z) = self.color.xyz_coordinates
        return f"ColorPatch {self.name} located at {self.xy} - XYZ == {x:.3}, {y:.3}, {z:.3}"

    def __post_init__(self):
        """
        If no name are provided to the constructor (name = '')
        The name will be automatically determined with the xy-coordinates
        """
        if self.name == "":
            self.name = f"{chr(ord('a')+self.xy[0]).upper()}{self.xy[1]+1}"


### Geometry classes
class Quadrilateral:
    """
    Represents a quadrilateral shape defined by four points in a 2D coordinate system.
    """

    def __init__(self, p1, p2, p3, p4):
        """
        all points are arraylike : [x, y]. Order has no importance.
        .      P1     P2
        y       x----x
        ∟x     /     │
        .     /      │
        .    /       │
        .   x--------x
        .   P4       P3
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def to_numpy(self):
        """Return numpy array of the coordinates"""
        return np.array([self.p1, self.p2, self.p3, self.p4])

    def plot(self, ax=None, invert_p3_p4=False):
        """Plot the quadrilateral in an ax
        Args:
            ax (_type_, optional): ax in which we want to draw the quadrilateral.
            If none, we take the current Axe. Defaults to None.
            invert_p3_p4 (bool, optional): If we want to invert last points.
            To change between Z or ⫎ configuration. Defaults to False.
        """
        if ax is None:
            ax = plt.gca()

        # add redundancy on the last point to close the loop
        round_path = np.vstack((self.to_numpy(), self.p1))

        if invert_p3_p4:
            round_path[2, :], round_path[3, :] = (
                round_path[3, :].copy(),
                round_path[2, :].copy(),
            )

        # adding a marker on the first point to locate it visually
        first_point = ax.plot(*self.p1, "+")
        ax.plot(round_path[:, 0], round_path[:, 1], color=first_point[0].get_c())

    def __repr__(self) -> str:
        return f"Quadrilateral object : \n{self.to_numpy()}"


class Rectangle(Quadrilateral):
    """
    The `Rectangle` class represents a rectangle shape and provides methods for manipulating and cropping rectangles in images.
    - Inherit from Quadrilateral
    """

    def __init__(self, xy, w, h):
        """Restrict the use of quadrilateral to only aligned point

        Args:
            xy (_type_): top=left point of the rectangle
            w (_type_): width of the rectangle
            h (_type_): heigh of the rectangle
        """
        p2 = [xy[0] + w, xy[1]]
        p3 = [xy[0] + w, xy[1] + h]
        p4 = [xy[0], xy[1] + h]
        self.h = h
        self.w = w
        super().__init__(xy, p2, p3, p4)

    def to_z_config(self):
        """
        Ensure the Z configuration by swapping last points
        """
        if self.p2[0] == self.p3[0]:
            self.p3, self.p4 = self.p4, self.p3
        return self

    def to_clockwise_config(self):
        """
        Ensure the clockwise configuration by swapping last points
        """
        if self.p2[0] == self.p4[0]:
            self.p3, self.p4 = self.p4, self.p3
        return self

    def shrink(self, factor):
        """
        Reduce the size of the rectangle by a factor
        """

        # Calculate the center of the rectangle
        cx = (self.p1[0] + self.p3[0]) / 2
        cy = (self.p1[1] + self.p3[1]) / 2

        # Create new points for the shrunken rectangle
        self.p1 = [cx + factor * (self.p1[0] - cx), cy + factor * (self.p1[1] - cy)]
        self.p2 = [cx + factor * (self.p2[0] - cx), cy + factor * (self.p2[1] - cy)]
        self.p3 = [cx + factor * (self.p3[0] - cx), cy + factor * (self.p3[1] - cy)]
        self.p4 = [cx + factor * (self.p4[0] - cx), cy + factor * (self.p4[1] - cy)]
        self.h = self.p4[1] - self.p1[1]
        self.h = self.p2[0] - self.p1[0]

        return self

    def crop(self, img) -> np.ndarray:
        """
        Crop an image with the parameters of the rectangle
        """
        img_crop = img[
            int(np.ceil(self.p1[1])) : int(np.floor(self.p4[1])),
            int(np.ceil(self.p1[0])) : int(np.floor(self.p2[0])),
            :,
        ]
        return img_crop

    def mean_color_crop(self, img) -> np.ndarray:
        """
        Crop an image and return the mean color.
        """
        img_crop = self.crop(img)
        return np.mean(img_crop, axis=(0, 1))


class RectangleGrid:
    """
    The `RectangleGrid` class represents a grid of rectangles on a canvas, with the ability to shrink each rectangle by a given parameter and plot the grid
    """

    def __init__(
        self,
        canva: Rectangle,
        columns: int,
        lines: int,
        shrink_parameter: float,
    ) -> None:

        self.rectangles: list[Rectangle] = []
        self.patch_coordinates: list[list[int, int]] = []
        self.lines = lines
        self.columns = columns

        size_patch_h = canva.h / lines
        size_patch_w = canva.w / columns

        for i in range(lines):
            for j in range(columns):
                self.patch_coordinates.append([j, i])

                rect_ij = Rectangle(
                    [j * size_patch_w, i * size_patch_h], size_patch_w, size_patch_h
                )  # maybe add the first point of the canva...
                self.rectangles.append(rect_ij.shrink(shrink_parameter))

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        for rect in self.rectangles:
            rect.plot(ax=ax)


### ColorChecker classes
class ColorCheckerSGBaseClass:
    """Base class for the color checker. Provide some methods (len(), iteration feature)
    and initialize the patches attribute
    """

    patches: list[ColorPatch] = []

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        ax.invert_yaxis()
        for ptch in self:
            rect = matplotlib.patches.Rectangle(
                ptch.xy, 1, 1, color=ptch.color.to_rgb()
            )
            ax.add_artist(rect)

        ax.set_xticks(
            np.arange(14) + 0.5,
            labels=[chr(value).upper() for value in range(ord("a"), ord("n") + 1)],
        )
        ax.set_yticks(
            np.arange(10) + 0.5, labels=[str(value + 1) for value in range(10)]
        )

        ax.set_xlim(0, 14)
        ax.set_ylim(10, 0)

    @staticmethod
    def _convertNameToCoordinates(name: str):
        letter_num = ord(name[0]) - 65
        return (letter_num, np.int64(name[1:]) - 1)

    def __len__(self):
        return len(self.patches)

    """ iter and next __method__ are used to custimize the iteration of a ColorChecker object"""

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.patches):
            patch = self.patches[self.current_index]
            self.current_index += 1
            return patch
        raise StopIteration

    @property
    def patches_names(self):
        return [ptch.name for ptch in self]

    @property
    def color_as_dict(self):
        return {ptch.name: ptch.color for ptch in self}

    def get_color_by_patch_name(self, name):
        return self.color_as_dict.get(name, None)


class ColorCheckerSGReference(ColorCheckerSGBaseClass):
    TXT_LAB_DATA = r"ColorCheckerSG_After_Nov2014.txt"

    def __init__(self) -> None:
        patches_data = np.loadtxt(self.TXT_LAB_DATA, dtype=str)
        self.patches: list[ColorPatch] = []
        for patch_data in patches_data:
            color_data = tuple(np.float64(patch_data[1:]))
            self.patches.append(
                ColorPatch(
                    patch_data[0],
                    self._convertNameToCoordinates(patch_data[0]),
                    Color(color_data, ColorSpace.Lab),  # , illuminant="D50"),
                )
            )


class ColorCheckerSGMeasure(ColorCheckerSGBaseClass):
    CC_RATIO = 14 / 10
    IMG_SIZE = 1000
    LINE_NO = 10
    COL_NO = 14

    def __init__(self, image_path: str, corners: Quadrilateral) -> None:

        self.img = cv.imread(image_path)[..., ::-1]
        self.corners = corners
        assert (
            self.img is not None
        ), "file could not be read, check with os.path.exists()"

    def process(self):
        # define finale undistorded image canva
        self.dest_rectangle = Rectangle(
            [0, 0], self.IMG_SIZE * self.CC_RATIO, self.IMG_SIZE
        )
        pts2 = np.float32(self.dest_rectangle.to_z_config().to_numpy())

        # Undistord the image
        try:
            M = cv.getPerspectiveTransform(np.float32(corners.to_numpy()), pts2)
            self.undistord_image = cv.warpPerspective(self.img, M, (1400, 1000))
        except:
            self.plot_roi()
            raise Exception("Cannot perform image transofrmation")

        self.grid = RectangleGrid(self.dest_rectangle, 14, 10, 0.5)
        for i in range(self.grid.lines):
            for j in range(self.grid.columns):
                patch_rect = self.grid.rectangles[i * self.grid.columns + j]
                self.patches.append(
                    ColorPatch(
                        "",  # we want to automatically fill the name with the xz coordinates
                        [j, i],
                        Color(
                            patch_rect.mean_color_crop(self.undistord_image) / 255,
                            ColorSpace.RGB,
                        ),
                    )
                )

    def plot_roi(self):
        plt.imshow(self.img)
        self.corners.plot(invert_p3_p4=True)
        plt.show()

    def plot_patches(self):
        plt.imshow(self.undistord_image)
        self.grid.plot()
        plt.show()


class ColorCorrection:
    def __init__(
        self,
        measure_color_checker: ColorCheckerSGMeasure,
        ref_color_checker: ColorCheckerSGReference,
        correction_order: int = 2,
    ) -> None:
        assert set(measure_color_checker.patches_names) == set(
            ref_color_checker.patches_names
        ), "The two input ColorChecker should have the same size"

        self.cc_measure = measure_color_checker
        self.cc_ref = ref_color_checker
        self.patches_names = measure_color_checker.patches_names
        self.correction_order = correction_order

        Lab_ref, Lab_meas = [], []
        for name in self.patches_names:
            Lab_ref.append(self.cc_ref.get_color_by_patch_name(name).to_lab())
            Lab_meas.append(self.cc_measure.get_color_by_patch_name(name).to_lab())

        self.Lab_ref = np.array(Lab_ref)
        self.Lab_meas = np.array(Lab_meas)

        self.S_ref = np.sqrt(self.Lab_ref[:, 1] ** 2 + self.Lab_ref[:, 2] ** 2)
        self.S_meas = np.sqrt(self.Lab_meas[:, 1] ** 2 + self.Lab_meas[:, 2] ** 2)

    def plot_Lab_meas_vs_ref(self):
        fig, axes = plt.subplots(1, 2)

        axes[0].scatter(self.Lab_ref[:, 0], self.Lab_meas[:, 0], marker="+")
        axes[0].set_xlim(0, 100)
        axes[0].set_ylim(0, 100)
        axes[0].set_xlabel("L* reference")
        axes[0].set_ylabel("L* measured")

        axes[1].scatter(self.S_ref, self.S_meas, marker="+")
        axes[1].set_xlim(0, 120)
        axes[1].set_ylim(0, 120)
        axes[1].set_xlabel("Saturation reference")
        axes[1].set_ylabel("Saturation measured")

    def plot_both_colorchecker(self):
        fig, axes = plt.subplots(2, 1)

        self.cc_measure.plot(ax=axes[1])
        self.cc_ref.plot(ax=axes[0])

        for ax in axes:
            ax.set_aspect("equal", "box")

    def cie_xy_delta_color(self):
        """
        Plot a cie 1931 xy diagram with for each patch a line from the theoretical
        xy coordinates to the measured one on the image
        """
        fig, ax = plt.subplots()
        xyz_ref, xyz_meas = [], []

        #### construction of the CIE 1931 xy border diagram ####
        # TOTALLY OPTIONAL
        wavelength = np.linspace(
            425, 640, 1000
        )  # this range is abitrary, but works well
        XYZ_border_CIE = colour.wavelength_to_XYZ(wavelength)

        # for pink line which do not correspond to any color, we interpolate extremes values of the prevbious curve
        short_wl, long_wl = XYZ_border_CIE[0], XYZ_border_CIE[-1]
        pink_line = np.array(
            [
                short_wl * alpha + long_wl * (1 - alpha)
                for alpha in np.linspace(0, 1, 1000)
            ]
        )
        XYZ_border_CIE = np.vstack((XYZ_border_CIE, pink_line))

        # compute xy coordinates with Grassmann formula
        x_border = XYZ_border_CIE[:, 0] / np.sum(XYZ_border_CIE, axis=1)
        y_border = XYZ_border_CIE[:, 1] / np.sum(XYZ_border_CIE, axis=1)
        display_colors = skimage.color.convert_colorspace(XYZ_border_CIE, "XYZ", "RGB")
        ax.scatter(x_border, y_border, c=display_colors, marker=".")

        # plot of lines
        for name in self.patches_names:
            XYZ_ref = self.cc_ref.get_color_by_patch_name(name).xyz_coordinates
            XYZ_meas = self.cc_measure.get_color_by_patch_name(name).xyz_coordinates
            RGB_color = self.cc_ref.get_color_by_patch_name(name).to_rgb()
            x_ref, y_ref = XYZ_ref[:2] / np.sum(XYZ_ref)
            x_meas, y_meas = XYZ_meas[:2] / np.sum(XYZ_meas)
            # ax.arrow(x_ref, y_ref, x_meas - x_ref, y_meas - y_ref, color=RGB_color)
            ax.annotate(
                "",
                xy=(x_meas, y_meas),
                xytext=(x_ref, y_ref),
                arrowprops=dict(arrowstyle="->", color=RGB_color),
            )
        ax.set_xlim(-0.01, 0.73)
        ax.set_ylim(0, 0.85)
        ax.set_aspect("equal", "box")
        ax.set_ylabel("y")
        ax.set_xlabel("x")
        ax.set_title("xy CIE 1931 diagram")

    def compute_correction_matrix(self):
        W_ref = np.array(
            [
                self.cc_ref.get_color_by_patch_name(name).xyz_coordinates
                for name in self.patches_names
            ]
        )

        if self.correction_order == 1:
            W_meas_n_th_order = np.zeros([len(self.cc_measure), 4])
            for i, name in enumerate(self.patches_names):
                X, Y, Z = self.cc_measure.get_color_by_patch_name(name).xyz_coordinates
                W_meas_n_th_order[i] = np.array([1, X, Y, Z])
        if self.correction_order == 2:
            W_meas_n_th_order = np.zeros([len(self.cc_measure), 10])
            for i, name in enumerate(self.patches_names):
                X, Y, Z = self.cc_measure.get_color_by_patch_name(name).xyz_coordinates
                W_meas_n_th_order[i] = np.array(
                    [1, X, Y, Z, X**2, X * Y, X * Z, Y**2, Y * Z, Z**2]
                )
        if self.correction_order == 3:
            W_meas_n_th_order = np.zeros([len(self.cc_measure), 20])
            for i, name in enumerate(self.patches_names):
                X, Y, Z = self.cc_measure.get_color_by_patch_name(name).xyz_coordinates
                W_meas_n_th_order[i] = np.array(
                    [
                        1,
                        X,
                        Y,
                        Z,
                        X**2,
                        X * Y,
                        X * Z,
                        Y**2,
                        Y * Z,
                        Z**2,
                        X**3,
                        X**2 * Y,
                        X**2 * Z,
                        X * Y**2,
                        X * Y * Z,
                        X * Z**2,
                        Y**3,
                        Y**2 * Z,
                        Y * Z**2,
                        Z**3,
                    ]
                )

        res = scipy.linalg.lstsq(W_meas_n_th_order, W_ref)
        self.U = res[0]

    def correct_img(self, plot: bool = True):
        assert hasattr(self, "U"), "Class has not correction matrix calculated for now"

        XYZ_img = skimage.color.rgb2xyz(self.cc_measure.img)
        X, Y, Z = np.split(XYZ_img, 3, axis=2)

        if self.correction_order == 1:
            n_th_order_image = np.stack(
                (np.ones_like(X), X, Y, Z),
                axis=2,
            ).squeeze()

        if self.correction_order == 2:
            n_th_order_image = np.stack(
                (np.ones_like(X), X, Y, Z, X**2, X * Y, X * Z, Y**2, Y * Z, Z**2),
                axis=2,
            ).squeeze()

        if self.correction_order == 3:
            n_th_order_image = np.stack(
                (
                    np.ones_like(X),
                    X,
                    Y,
                    Z,
                    X**2,
                    X * Y,
                    X * Z,
                    Y**2,
                    Y * Z,
                    Z**2,
                    X**3,
                    X**2 * Y,
                    X**2 * Z,
                    X * Y**2,
                    X * Y * Z,
                    X * Z**2,
                    Y**3,
                    Y**2 * Z,
                    Y * Z**2,
                    Z**3,
                ),
                axis=2,
            ).squeeze()

        corrected_XYZ_img = np.dot(n_th_order_image, self.U)

        self.corrected_rgb_img = skimage.color.xyz2rgb(corrected_XYZ_img)
        if plot:
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(self.cc_measure.img)
            axes[1].imshow(self.corrected_rgb_img)

            axes[0].set_title("Image détériorée")
            axes[1].set_title("Image corrigée")

            for ax in axes:
                ax.set_aspect("equal", "box")
                ax.axis("off")

            fig.set_size_inches(12, 16)


# creation of CC measurement from image
image_path = r"ColorCheckerSG_VeryAltered.jpg"
corners = Quadrilateral([319, 208], [2051, 109], [412, 1353], [2081, 1381])

cc_meas = ColorCheckerSGMeasure(image_path, corners)
cc_meas.process()
cc_meas.plot_roi()
cc_meas.plot_patches()
cc_meas.plot()

# creation of CC reference from constructor values
cc_ref = ColorCheckerSGReference()
cc_ref.plot()

# correction process
color_corr = ColorCorrection(cc_meas, cc_ref, 3)
color_corr.compute_correction_matrix()
color_corr.correct_img()
color_corr.plot_both_colorchecker()
color_corr.plot_Lab_meas_vs_ref()
color_corr.cie_xy_delta_color()
