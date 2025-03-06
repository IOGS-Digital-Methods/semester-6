# %%
__author__ = "Corentin Nannini"
__date__ = "2024-12-26"

import skimage.color
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


class Color:
    """The `Color` class represents a color in different color spaces
    (XYZ, Lab, RGB) and provides methods to convert spaces."""

    def __init__(
        self,
        color_coordinates: np.ndarray | list | tuple,
        colorspace: str,
        illuminant="D65",
    ) -> None:
        """
        The color is represented in the XYZ color space. If the color is provided in another color space,
        it is converted to XYZ. Anyway, the values of the color should be between 0 and 1. For 8 bit images,
        the values should be divided by 255.

        Args:
            color_coordinates (np.ndarray | list): should be float arraylike with 3 components
            colorspace (str): Specify the color space in which color_coordinates is expressed.
                accepted values are "XYZ", "Lab", "RGB"
            illuminant (str, optional): Ony useful if the color space is Lab. Defaults to "D65".
            Not recommended to change this value.
        """

        # the provided coordinates is stored as a numpy array
        if isinstance(color_coordinates, (list, tuple)):
            color_coordinates = np.array(color_coordinates)

        # check if the color coordinates are of the right size (3)
        assert len(color_coordinates) == 3, f"{color_coordinates = } is not size 3"

        # check if the color space is valid
        if colorspace.casefold() == "xyz":
            self.xyz_coordinates = color_coordinates
        elif colorspace.casefold() == "lab":
            self.xyz_coordinates = skimage.color.lab2xyz(
                color_coordinates, illuminant=illuminant
            )
        elif colorspace.casefold() == "rgb":
            self.xyz_coordinates = skimage.color.rgb2xyz(color_coordinates)

    def to_lab(self, illuminant="D65") -> np.ndarray:
        return skimage.color.xyz2lab(self.xyz_coordinates, illuminant=illuminant)

    def to_rgb(self) -> np.ndarray:
        """Convert to color to RGB color space, this conveniently allows to display the color."""
        return skimage.color.xyz2rgb(self.xyz_coordinates)

    def __repr__(self) -> str:
        (x, y, z) = self.xyz_coordinates
        return f"Color (X, Y, Z) = {x:.3}, {y:.3}, {z:.3}"


if __name__ == "__main__":
    # example of use
    c1 = Color([0.5, 0.5, 0.5], "XYZ")
    print(c1)


class PerspectiveRemover:
    """Allow to remove distortion caused by the perspective in an image"""

    def __init__(self, image: np.ndarray, corners_colorchecker: np.ndarray) -> None:
        """
        Args:
            image (np.ndarray): Array of the image, of size [l, w, 3]
            corners_colorchecker (np.ndarray): coordinates of the corners of the colorchecker in the image
                Should be given in the following order (z-order): top-left, top-right, bottom-left, bottom-right
                Example : np.array([[319, 208], [2051, 109], [412, 1353], [2081, 1381]])
        """
        self.image = image
        self.corners = np.float32(corners_colorchecker)
        self.final_image_size = (
            1400,
            1000,
        )  # size of the final image, only valid for the colorchecker SG

    def remove_distortion(self) -> None:
        """Remove the image's distortion according to the corners of the colorchecker"""
        dest = np.array(
            [
                [0, 0],
                [self.final_image_size[0], 0],
                [0, self.final_image_size[1]],
                [self.final_image_size[0], self.final_image_size[1]],
            ],
            np.float32,
        )

        M = cv.getPerspectiveTransform(self.corners, dest)
        self.undistorted_image = cv.warpPerspective(self.image, M, (1400, 1000))
        return self.undistorted_image

    def plot(self):
        """
        Method to display the image with the corners of the colorchecker.
        Can be useful to check if the corners are well placed.
        """
        plt.imshow(self.image)
        plt.plot(self.corners[:, 0], self.corners[:, 1], "+")
        for i, txt in enumerate(["1", "2", "3", "4"]):
            offset = 20
            plt.text(
                self.corners[i, 0] + offset,
                self.corners[i, 1] + offset,
                txt,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5),
            )
        plt.gca().set_aspect("equal")
        plt.show()


if __name__ == "__main__":
    # Example of use
    img = cv.imread("ColorCheckerSG_Altered.jpg").astype(np.float32) / 255.0

    perspective = PerspectiveRemover(
        img, np.array([[319, 208], [2051, 109], [412, 1353], [2081, 1381]])
    )
    perspective.plot()

    undistorted_image = perspective.remove_distortion()
    plt.imshow(undistorted_image)


class Rectangle:
    """
    The `Rectangle` class represents a rectangle shape and provides methods for
    manipulating and cropping images.
    """

    def __init__(self, xy: list | np.ndarray, w: float, h: float) -> None:
        """Define a rectangle using the top-left point and the width and height.
        It generates the 4 points of the rectangle (p1, p2, p3, p4).

        all points are arraylike : [x, y].
        .       p1      p2
        . (xy)  x--------x
        .       │   w    │
        .     h │        │
        .       │        │
        .       x--------x
        .       p4       p3

        Args:
            xy (list or array): top=left point of the rectangle
            w (float): width of the rectangle
            h (float): heigh of the rectangle
        """
        self.h = h
        self.w = w

        xy = np.array(xy)
        p2 = np.array([xy[0] + w, xy[1]])
        p3 = np.array([xy[0] + w, xy[1] + h])
        p4 = np.array([xy[0], xy[1] + h])

        self.p1 = xy
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def to_numpy(self):
        """Return numpy array of the coordinates"""
        return np.array([self.p1, self.p2, self.p3, self.p4])

    def shrink(self, factor):
        """
        Reduce the size of the rectangle by a factor, for the center of the rectangle.
        if the factor is 1, the rectangle will not change.
                ... below 1, the rectangle will shrink
                ... above 1, the rectangle will expand
        """

        # Calculate the center of the rectangle
        cx = (self.p1[0] + self.p3[0]) / 2
        cy = (self.p1[1] + self.p3[1]) / 2
        center = np.array([cx, cy])

        # Create new points for the shrunken rectangle
        self.p1 = center + factor * (self.p1 - center)
        self.p2 = center + factor * (self.p2 - center)
        self.p3 = center + factor * (self.p3 - center)
        self.p4 = center + factor * (self.p4 - center)
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

    def plot(self, ax=None):
        """Plot the rectangle in an ax
        Args:
            ax (_type_, optional): ax in which we want to draw the quadrilateral.
            If none, we take the current Axe. Defaults to None.
        """
        if ax is None:
            ax = plt.gca()

        # add redundancy on the last point to close the loop
        round_path = np.vstack((self.to_numpy(), self.p1))

        # adding a marker on the first point to locate it visually
        first_point = ax.plot(*self.p1, "+")
        ax.plot(round_path[:, 0], round_path[:, 1], color=first_point[0].get_c())


if __name__ == "__main__":
    # Example of use
    rect = Rectangle([30, 30], 100, 100)
    rect.plot()
    plt.imshow(undistorted_image)
    plt.show()

    cropped_image = rect.crop(undistorted_image)
    plt.imshow(cropped_image)
    plt.show()


"""
Coordinates for the images in the dataset.
The coordinates are in the format of (x1, y1), (x2, y2), (x3, y3), (x4, y4)
where (x1, y1) is the top-left corner, (x2, y2) is the top-right corner,
(x3, y3) is the bottom-left corner, and (x4, y4) is the bottom-right corner.
"""

coordinates = {
    "CC_image": ([319, 208], [2051, 109], [412, 1353], [2081, 1381]),
    "APC_0007.jpg": ([1287, 1450], [1839, 1454], [1280, 1838], [1835, 1851]),
    "APC_0010.jpg": ([646, 1850], [2083, 1809], [718, 3028], [2160, 2771]),
    "APC_0012.jpg": ([327, 1165], [1889, 1200], [338, 2274], [1876, 2205]),
    "APC_0020.jpg": ([1003, 1682], [2070, 1723], [940, 2477], [2045, 2506]),
}

# %%
