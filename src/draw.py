import cv2

# Color list options
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_MAROON = (0, 0, 128)
COLOR_AQUA = (255, 255, 0)
COLOR_NAVY = (128, 0, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_MAGENTA = (255, 0, 255)
COLOR_VIOLET = (226, 43, 138)
COLOR_SNOW = (250, 250, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_SILVER = (192, 192, 192)
COLOR_SMOKE = (245, 245, 245)

# Font style options
SANS_SERIF_REGULAR = cv2.FONT_HERSHEY_SIMPLEX
SANS_SERIF_SMALL = cv2.FONT_HERSHEY_PLAIN
SANS_SERIF_NORMAL = cv2.FONT_HERSHEY_DUPLEX
SERIF_REGULAR = cv2.FONT_HERSHEY_COMPLEX
SERIF_NORMAL = cv2.FONT_HERSHEY_TRIPLEX
SERIF_SMALL = cv2.FONT_HERSHEY_COMPLEX_SMALL
HAND_WRITING_REGULAR = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
HAND_WRITING_NORMAL = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
ITALIC = cv2.FONT_ITALIC

# Font weight options
TEXT_WEIGHT_REGULAR = 1
TEXT_WEIGHT_MEDIUM = 2
TEXT_WEIGHT_HARD = 3
TEXT_WEIGHT_BOLD = 4

# Font size options
TEXT_SIZE_SMALL = 0.7
TEXT_SIZE_REGULAR = 1
TEXT_SIZE_NORMAL = 1.3
TEXT_SIZE_MEDIUM = 1.5
TEXT_SIZE_LARGE = 2

# Font weight options
THICK_WEIGHT_REGULAR = 1
THICK_WEIGHT_MEDIUM = 2
THICK_WEIGHT_HARD = 3
THICK_WEIGHT_BOLD = 4


class Draw:
    def __init__(self, canvas):
        self.canvas = canvas

        self.x_center = int(self.canvas.shape[0] / 2)
        self.y_center = int(self.canvas.shape[1] / 2)

    def Text(self,
             text: str,
             x: int = 0,
             y: int = 0,
             font: int = SANS_SERIF_NORMAL,
             font_size: float = TEXT_SIZE_NORMAL,
             font_weight: int = TEXT_WEIGHT_MEDIUM,
             color: tuple = COLOR_BLACK):

        return cv2.putText(self.canvas,
                           text,
                           (self.x_center + x, self.y_center + y),
                           font,
                           font_size,
                           color,
                           font_weight)

    def Circle(self,
               x: int = 0,
               y: int = 0,
               rad: int = 2,
               color: tuple = COLOR_BLACK,
               thick: int =THICK_WEIGHT_MEDIUM
               ):

        return cv2.circle(self.canvas,
                          (self.x_center + x, self.y_center + y),
                          rad,
                          color,
                          thick)



