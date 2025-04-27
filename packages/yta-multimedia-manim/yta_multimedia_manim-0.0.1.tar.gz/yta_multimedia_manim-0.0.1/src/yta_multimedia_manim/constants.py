"""
TODO: Please, put some structure here and more comments
"""


MANIM_RESOURCES_FOLDER = 'resources/manim/'

DEFAULT_SCENE_SIZE = (1920, 1080)
"""
A default scene size (FullHD) defined in pixels.
This size is the same as in moviepy because this
engine works also with pixels.
"""
DEFAULT_SCENE_WIDTH = DEFAULT_SCENE_SIZE[0]
DEFAULT_SCENE_HEIGHT = DEFAULT_SCENE_SIZE[1]
DEFAULT_MANIM_SCENE_SIZE = (8, 14 + (2 / 9))
"""
The manim equivalent of an scene of 1920x1080 pixels,
adapted to be able to work with it when using the
manim engine.
"""
DEFAULT_MANIM_SCENE_WIDTH = DEFAULT_MANIM_SCENE_SIZE[0]

DEFAULT_MANIM_SCENE_HEIGHT = DEFAULT_MANIM_SCENE_SIZE[1]
# Manim core
MANDATORY_CONFIG_PARAMETER = 1
OPTIONAL_CONFIG_PARAMETER = 0

# I obtained manim dimensions from here: https://docs.manim.community/en/stable/faq/general.html#what-are-the-default-measurements-for-manim-s-scene
LEFT_MARGIN = -DEFAULT_MANIM_SCENE_WIDTH / 2
"""
The position of the left edge in a manim scene.
"""
UP_MARGIN = DEFAULT_MANIM_SCENE_HEIGHT[1] / 2
"""
The position of the top edge in a manim scene.
"""

