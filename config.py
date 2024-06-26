IP_HOST = "localhost"
PORT_HOST = 20888

# OBS SETTINGS
IS_OBS_OVERLAY = 1
CHROMA_KEY_COLOR = (180, 0, 255)

# WIDOW SIZE
W_WIDTH = 355
W_HEIGHT = 1000

# TYRE WIDGET SIZE (spacing between tyres).
TYRE_WIDGET_WIDTH = W_WIDTH
TYRE_WIDGET_HEIGHT = 670

# RANGE VALUE FOR TYRE TEMPERATURE AND TYRE WEAR. 
TYRE_TEMP_RANGE = {"MIN": 70, "MAX": 120} # IN DEGRES CELSIUS.
TYRE_WEAR_RANGE = {"MIN": 0, "MAX": 100}  # IN PERCENT.

# SIZE OF THE TYRE SLIPPED INDICATOR. 
TYRE_SLIPPED_WIDTH = 110
TYRE_SLIPPED_HEIGHT = 160

# SIZE OF THE TYRE WEAR INDICATOR. 
TYRE_WIDTH = 80
TYRE_HEIGHT = 130

# COORDINATE OF EVERY TYRES. (RL, RR, FL, FR).
TYRES_COORDINATES = (
    (0, TYRE_WIDGET_HEIGHT - TYRE_SLIPPED_HEIGHT - 45),
    (TYRE_WIDGET_WIDTH - TYRE_SLIPPED_WIDTH, TYRE_WIDGET_HEIGHT - TYRE_SLIPPED_HEIGHT - 45), 
    (0, 0), 
    (TYRE_WIDGET_WIDTH - TYRE_SLIPPED_WIDTH, 0),
)

# COORDINATE OF G FORCE TEXTS.
G_FORCE_RADIUS = 90
G_FORCE_COORDS = (
    (0, G_FORCE_RADIUS + 15),
    (0, -G_FORCE_RADIUS - 10),
    (-G_FORCE_RADIUS - 20, 0),
    (G_FORCE_RADIUS + 20, 0),
)
