"""
Color Manipulation and Analysis Utilities (lescolors / Les colors / The colors)

This module provides a `Color` class for working with colors in various formats.
It includes utilities for calculating adjacent and analogous colors, finding complementary
colors, converting RGB values to hexadecimal format, and extracting dominant colors
from images via a URL.

Classes:
    - Color:
        A class representing an RGB color, with methods to manipulate
        and analyze color properties such as adjacent colors, complementary color,
        and format conversions.

Functions:
    - Color.from_image(image_url: str, quality: int = 1) -> Color:
        Creates a Color object based on the dominant color in an image from a given URL.

    - Color.palette_from_image(image_url: str, num_colors: int = 5, quality: int = 1) -> list[Color]:
        Extracts a palette of dominant colors from an image URL and returns a list of Color objects.

Usage:
    This module can be used to explore color relationships, generate color schemes,
    and analyze colors from images. It is particularly useful for tasks related
    to graphic design, web development, and visual content creation.

Dependencies:
    - colorsys: A standard Python module for converting between color systems.
    - requests: A Python library for making HTTP requests.
    - colorthief: A library for grabbing the dominant color or a
                  representative color palette from an image.

Examples:
    - Creating a color object and finding analogous colors:
        red = Color([255, 0, 0])
        print(red.to_analogous())

    - Getting the complementary color of a given color:
        print(red.to_complementary())

    - Converting a color to Hex format:
        print(red.to_hex())

    - Creating a color object from an image's dominant color:
        dominant = Color.from_image('https://i.stack.imgur.com/JM4F2.png')
        print(dominant)

    - Getting a palette of dominant colors from an image:
        palette = Color.palette_from_image('https://i.stack.imgur.com/JM4F2.png')
        print(palette)
"""

import colorsys
from io import BytesIO
import requests
from colorthief import ColorThief

DEG30 = 30/360.

class Color:
    '''
    Represents a color in RGB space, with utilities for analysis and format conversion.
    
    Attributes:
        rgb (list[int]): A list containing the RGB components of the color.
        hls (tuple[float]): A tuple representing the HLS (Hue, Lightness, Saturation) values.
    '''

    def __init__(self, rgb: list[int]):
        '''
        Initializes a Color object with the given RGB values.

        Args:
            rgb (list[int]): A list containing the RGB components.
        '''
        self.rgb = rgb
        self._update_hls()

    def _update_hls(self):
        r, g, b = map(lambda x: x / 255., self.rgb)
        self.hls = colorsys.rgb_to_hls(r, g, b)

    def to_hex(self) -> str:
        '''
        Converts the RGB value of the color to hexadecimal format.

        Returns:
            str: The hex representation of the color, prefixed with "#".
        '''
        return f'#{self.rgb[0]:02x}{self.rgb[1]:02x}{self.rgb[2]:02x}'

    def to_complementary(self) -> "Color":
        '''
        Computes and returns the complementary color.

        The complementary color is found by adding 180 degrees (0.5 in hue space)
        to the hue of the original color in HSV space, and converting back to RGB.

        Returns:
            Color: A new Color object representing the complementary color.
        '''
        hsv = colorsys.rgb_to_hsv(*map(lambda x: x / 255., self.rgb))
        comp_rgb = colorsys.hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])
        comp_rgb = list(map(lambda x: int(round(x * 255)), comp_rgb))
        return Color(comp_rgb)

    def to_adjacent(self, d: float = DEG30) -> list["Color"]:
        '''
        Calculates and returns the adjacent colors on the color wheel.

        This function adjusts the hue by a given degree difference `d`
        in both the positive and negative directions.

        Args:
            d (float): The degree difference used to calculate adjacent colors
                       (default is 30 degrees, i.e., 1/12th of a full circle).

        Returns:
            list[Color]: A list of two Color objects representing the adjacent colors.
        '''
        h, l, s = self.hls
        hues = [(h + d) % 1, (h - d) % 1]
        adjacent = [
            Color(list(map(lambda x: int(round(x * 255)), colorsys.hls_to_rgb(hi, l, s))))
            for hi in hues
        ]
        return adjacent

    def to_analogous(self) -> list["Color"]:
        '''
        Computes and returns the analogous colors.

        Analogous colors are those adjacent on the color wheel.
        This uses the `to_adjacent` method with the default degree.

        Returns:
            list[Color]: A list of two Color objects representing the analogous colors.
        '''
        return self.to_adjacent()

    @staticmethod
    def from_hex(hex_color: str) -> "Color":
        '''
        Creates a Color object from a hexadecimal color string.

        Args:
            hex_color (str): A hexadecimal color string (e.g., "#ff0000").

        Returns:
            Color: A new Color object corresponding to the hex value.
        '''
        hex_color = hex_color.lstrip("#")
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return Color(rgb)

    @staticmethod
    def from_image(image_url: str, quality: int = 1) -> "Color":
        '''
        Extracts the dominant color from an image URL and creates a Color object.

        Args:
            image_url (str): The URL of the image to process.
            quality (int): An optional parameter to set the quality of extraction.
                           Lower quality values are slower but more accurate.

        Returns:
            Color: A Color object representing the dominant color of the image.
        '''
        response = requests.get(image_url, timeout=2)
        image = ColorThief(BytesIO(response.content))
        dominant_rgb = image.get_color(quality=quality)
        return Color(list(dominant_rgb))

    @staticmethod
    def palette_from_image(image_url: str, num_colors: int = 5, quality: int = 1) -> list["Color"]:
        '''
        Extracts a palette of dominant colors from an image URL.

        Args:
            image_url (str): The URL of the image to process.
            num_colors (int): Number of dominant colors to fetch (default is 5).
            quality (int): An optional parameter to set the quality of extraction.
                           Lower quality values are slower but more accurate.

        Returns:
            list[Color]: A list of Color objects representing the dominant colors.
        '''
        response = requests.get(image_url, timeout=2)
        image = ColorThief(BytesIO(response.content))
        palette = image.get_palette(color_count=num_colors, quality=quality)
        return [Color(list(color)) for color in palette]

    def __repr__(self):
        return f"Color(rgb={self.rgb}, hex='{self.to_hex()}')"

# Example usage:
# red = Color([255, 0, 0])
# print(red.to_hex())
# print(red.to_complementary())
# print(red.to_analogous())
# dominant = Color.from_image('https://i.stack.imgur.com/JM4F2.png')
# print(dominant)
# palette = Color.palette_from_image('https://i.stack.imgur.com/JM4F2.png')
# print(palette)
