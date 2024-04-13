import pygame
import colorsys
from config import *
import os


pygame.init()
text_font = pygame.font.SysFont("Formula1", 40)

base = pygame.image.load(os.path.join('img', 'base.png'))
base_width, base_height = base.get_size()
base = pygame.transform.scale(base, (base_width / 4 , base_height / 4))


steering_wheel = pygame.image.load(os.path.join('img', 'wheel.png'))
wheel_width, wheel_height = steering_wheel.get_size()
steering_wheel = pygame.transform.scale(steering_wheel, (wheel_width / 4, wheel_height / 4))


def draw_tyre_widget(window: pygame.Surface, x: int, y: int, tyre_temp: float, tyre_wear: float, as_lost_grip: bool):
    """
    Function that draw the entire tyre widget for one tyre. 

    :param window: window where the tyre widget will be drawn. 
    :param x: x coordinate of the tyre widget. 
    :param y: y coordinate of the tyre widget. 
    :param tyre_temp: temperature of the tyre in degree celsius. 
    :param tyre_wear: wear of the tyre in percent. 
    :param as_lost_grip: boolean value that is 1 if the tyre lost grip, 0 otherwise.
    """

    draw_tyre_grip_loss(window, x, y, as_lost_grip)
    draw_tyre_wear(window, x, y, tyre_wear)
    draw_tyre_temp_gauge(window, x, y, tyre_temp)


def draw_tyre_grip_loss(window: pygame.Surface, x: int, y: int, as_lost_grip: bool):
    """
    Function that draw the tyre outline representing the grip of the tyre. 

    :param window: window where the tyre grip loss indicator will be drawn. 
    :param x: x coordinate of the tyre widget. 
    :param y: y coordinate of the tyre widget. 
    :param as_lost_grip: boolean value that is 1 if the tyre lost grip, 0 otherwise.
    """
    tyre_grip_color = (205, 0, 0) if as_lost_grip else (255, 255, 255)
    pygame.draw.rect(window, tyre_grip_color, pygame.Rect(
        x, y + 45, TYRE_SLIPPED_WIDTH, TYRE_SLIPPED_HEIGHT), 5, 20)


def draw_tyre_wear(window: pygame.Surface, x: int, y: int, tyre_wear: int):
    """
    Function that draw the tyre and it's wear. 

    :param window: window where the tyre will be drawn. 
    :param x: x coordinate of the tyre widget. 
    :param y: y coordinate of the tyre widget. 
    :param tyre_wear: wear of the tyre in percent. 
    """
    # Get the color associated with the tyre wear.
    tyre_wear_color = value_to_color(
        tyre_wear, TYRE_WEAR_RANGE["MIN"], TYRE_WEAR_RANGE["MAX"], 130, 0)

    # Draw the tyre.
    pygame.draw.rect(window, tyre_wear_color, pygame.Rect(
        x + 15, y + 60, TYRE_WIDTH, TYRE_HEIGHT), 0, 10)

    # Create and center the wear text.
    wear_text = text_font.render(str(tyre_wear) + "%", True, (255, 255, 255))
    wear_x, _ = wear_text.get_size()
    window.blit(wear_text, (x + (TYRE_SLIPPED_WIDTH - wear_x) /
                2, y + (TYRE_SLIPPED_HEIGHT + 60) / 2))


def draw_tyre_temp_gauge(window: pygame.Surface, x: int, y: int, tyre_temp: int):
    """
    Function that draw the tyre temperature gauge to the tyre widget. 

    :param window: window where the gauge will be drawn. 
    :param x: x coordinate of the tyre widget. 
    :param y: y coordinate of the tyre widget. 
    :param tyre_temp: temperature of the tyre in degree celsius. 
    """

    # Get the color associated with the tyre temperature.
    tyre_temp_color = value_to_color(
        tyre_temp, TYRE_TEMP_RANGE["MIN"], TYRE_TEMP_RANGE["MAX"], 200, 20)

    # Calculate the correct gauge length according to the tyre temperature range.
    gauge_length = map_range(
        tyre_temp, TYRE_TEMP_RANGE["MIN"], TYRE_TEMP_RANGE["MAX"], 10, TYRE_SLIPPED_WIDTH)

    # Draw the gauge to the screen.
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(
        x, y + 30, TYRE_SLIPPED_WIDTH, 8), 0, 4)
    pygame.draw.rect(window, tyre_temp_color, pygame.Rect(
        x, y + 30, gauge_length, 8), 0, 4)

    # Create and center the tyre temperature text.
    temp_text = text_font.render(str(tyre_temp) + "°C", True, tyre_temp_color)
    temp_x, _ = temp_text.get_size()

    # Draw the tyre temperature text.
    window.blit(temp_text, (x + (TYRE_SLIPPED_WIDTH - temp_x) / 2, y + 2))


def draw_g_force_widget(window: pygame.Surface, x: int, y: int, lat_g_force: float, long_g_force: float):
    """
    Function that draw the G force widget. 

    :param window: window where the G force widget will be drawn. 
    :param x: x coordinate of the G force widget.
    :param y: y coordinate of the G force widget.
    :param lat_g_force: lateral G force value. 
    :param long_g_force: longitudinal G force value. 
    """

    # Draw the grid behind the G force indicator.
    pygame.draw.circle(window, (255, 255, 255), (x, y), G_FORCE_RADIUS, 2)
    pygame.draw.circle(window, (255, 255, 255), (x, y), G_FORCE_RADIUS / 1.5, 2)
    pygame.draw.circle(window, (255, 255, 255), (x, y), G_FORCE_RADIUS / 4, 2)

    # Calculate and render the G force indicator.
    mapped_lat_force = map_range(
        lat_g_force, -6, 6, -G_FORCE_RADIUS, G_FORCE_RADIUS)
    mapped_long_force = map_range(
        long_g_force, -6, 6, -G_FORCE_RADIUS, G_FORCE_RADIUS)
    pygame.draw.circle(window, (255, 0, 0), (x + mapped_lat_force, y + mapped_long_force), (G_FORCE_RADIUS / 4) - 10)

    # Parse lat and long G forces value to print it to the screen.
    g_forces = parse_g_force_data(lat_g_force, long_g_force)

    # Render each text.
    for index, coord in enumerate(G_FORCE_COORDS):
        draw_text(window, x + coord[0], y + coord[1], g_forces[index])


def draw_text(window: pygame.Surface, x: int, y: int, g_force_value: float):
    """
    Function that draw the G force text.

    :param window: window where the tyre widget will be drawn. 
    :param x: x coordinate of the G force widget.
    :param y: y coordinate of the G force widget.
    :param g_force_value: the G force value associed to the text. 
    """
    # Create and center the text.
    g_force_text = text_font.render(
        f"{g_force_value:.1f}", True, (255, 255, 255))
    text_width, text_height = g_force_text.get_size()

    # Render it.
    window.blit(g_force_text, (x - text_width / 2, y - text_height / 2))


def parse_g_force_data(lat_g_force: float, long_g_force: float) -> tuple:
    """
    Function that parse the lat and long G forces values to print them on screen. 

    :param lat_g_force: lateral G force value. 
    :param long_g_force: longitudinal G force value. 
    :return: each parsed value. 
    """

    # If the lat is negative then the left lat has a value and right lat is null.
    if lat_g_force > 0:
        left_force = 0
        right_force = lat_g_force

    # The other way around.
    else:
        left_force = abs(lat_g_force)
        right_force = 0

    # If the long is negative then the left long has a value and right long is null. 
    if long_g_force > 0:
        back_force = 0
        front_force = long_g_force

    # The other way around. 
    else:
        back_force = abs(long_g_force)
        front_force = 0

    return front_force, back_force, left_force, right_force


def value_to_color(value, value_min, value_max, hsv_min, hsv_max):
    """
    Function that generate a color than represent the value passed in. 
    :param value: value that need a color representation. 
    :param value_min: minimum interval of the value. 
    :param value_max: maximum interval of the value. 
    :param hsv_min: minimum hsv interval. 
    :param hsv_max: maximum hsv interval. 
    :return: the generated color in rgb format. 
    """

    # Map the value to the correct HSV range and generate the color.
    mapped_in_value = map_range(value, value_min, value_max, hsv_min, hsv_max)
    r, g, b = colorsys.hsv_to_rgb(mapped_in_value / 360, 1, .8)

    # Convert 0-1 rgb values  to 0-255 rgb values and remove negative values.
    r *= -255 if r < 0 else 255
    g *= -255 if g < 0 else 255
    b *= -255 if b < 0 else 255

    # return the color.
    return r, g, b


def map_range(value, in_value_min, in_value_max, out_min, out_max):
    """
    Function that map a value that is contained in a range to another range. 

    :param value: value that need to me mapped to the new range. 
    :param in_value_min: minimum interval of the current range. 
    :param in_value_max: maximum interval of the current range. 
    :param out_min: minimum interval of the new range. 
    :param out_max: maximum interval of the new range. 
    :return: new value mapped to the new range. 
    """
    # If the initial value is greater the max value, return the max out value.
    if value <= in_value_min:
        return out_min

    # Else if the initial value is lower than the min value, return the min out value.
    elif value >= in_value_max:
        return out_max

    # Map the value.
    return (value - in_value_min) * (out_max - out_min) // (in_value_max - in_value_min) + out_min



def draw_steer_widget(window: pygame.Surface, x: int, y: int, steer_angle: float):
    mapped_steering_angle = map_range(-steer_angle, -1, 1, -180, 180)

    cx_base, cy_base = base.get_rect().center
    base_x_coord, base_y_coord = x - cx_base, y - cy_base

    window.blit(base, (base_x_coord, base_y_coord))

    rotated_steering_wheel = pygame.transform.rotate(steering_wheel, mapped_steering_angle)
    cx_steer, cy_steer = rotated_steering_wheel.get_rect().center
    window.blit(rotated_steering_wheel, (x - cx_steer, y - cy_steer))