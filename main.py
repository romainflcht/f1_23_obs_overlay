from f1_23_telemetry.listener import TelemetryListener
import udp_functions
import pygame
from config import *
from graphics_functions import *


try:
    listener = TelemetryListener(host=IP_HOST, port=PORT_HOST, timeout=.1)

except OSError:
    print("[ERROR] Another program is listening to the same UDP port, try closing it and retry...")
    exit(1)

overlay_window = pygame.display.set_mode((W_WIDTH, W_HEIGHT)) 

# Window configuration.
pygame.display.set_caption('obs_f1_23_overlay')
window_icon = pygame.image.load(os.path.join('img', 'base.png'))
pygame.display.set_icon(window_icon)


if IS_OBS_OVERLAY:
    bg_color = CHROMA_KEY_COLOR
else: 
    bg_color = (0, 0, 0)


if __name__ == "__main__":
    running = True

    # Initialise car data.
    tyre_temp = [TYRE_TEMP_RANGE["MIN"] for _ in range(4)]
    tyre_wear = [TYRE_WEAR_RANGE["MIN"] for _ in range(4)]
    tyre_as_lost_grip = [0, 0, 0, 0]
    lat_g_force = 0
    long_g_force = 0
    steer_angle = 0
    

    while running:
        # Fetch UDP data from the game. 
        data_type, data = udp_functions.fetch_telemetry(listener)

        # Clear the overlay screen. 
        overlay_window.fill(bg_color)
        
        # Draw every tyre widget. 
        for index, coord in enumerate(TYRES_COORDINATES):
                    x, y = coord
                    draw_tyre_widget(overlay_window, x, y, tyre_temp[index], tyre_wear[index], tyre_as_lost_grip[index])
        
        # Draw the G forces widget. 
        draw_g_force_widget(overlay_window, TYRE_WIDGET_WIDTH / 2, TYRE_WIDGET_HEIGHT / 2, lat_g_force, long_g_force)

        # Draw steer widget.
        draw_steer_widget(overlay_window, W_WIDTH / 2, TYRE_WIDGET_HEIGHT + 150, steer_angle)

        # Draw the watermark. 
        draw_watermark(overlay_window, W_WIDTH / 2, W_HEIGHT - 10)

        # Update data from the UDP stream.
        match data_type:
            case 0:
                # Update lateral and longitudinal G forces. 
                lat_g_force = data["g_force_lateral"]
                long_g_force = data["g_force_longitudinal"]
            
            case 1:
                # Update every tyre slip ratio. 
                for index, slip_ratio in enumerate(data["m_wheelSlipRatio"]):
                    tyre_as_lost_grip[index] = 1 if slip_ratio > .1 else 0
            
            case 2: 
                # Update steer angle. 
                steer_angle = data["steer"]

                # Update every tyre temperature.
                for index, temp in enumerate(data["tyres_surface_temperature"]):
                    tyre_temp[index] = temp

            case 3: 
                # Update every tyre wear.
                for index, wear in enumerate(data["tyres_wear"]):
                    tyre_wear[index] = int(wear)

            case _:
                # Ignore all other widget.
                pass

        # Update the screen. 
        pygame.display.flip()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
    
    print("\n\ngoodbye :)")



