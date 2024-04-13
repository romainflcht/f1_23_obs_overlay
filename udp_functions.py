from f1_23_telemetry.listener import TelemetryListener
from f1_23_telemetry.packets import PacketCarTelemetryData, PacketMotionData, PacketMotionExData, PacketCarDamageData



def fetch_telemetry(udp_listener: TelemetryListener):
    """
    Function that listen to the UDP stream sent by the F1 23 game and get car telemetry from it.
    :param: udp_listener: the UDP listener object taht listen to the UDP stream created by the game. 
    """
    packet = udp_listener.get()

    if packet is None:
        # Listening timed out, game is not focused. 
        return -1, {}
    
    # Get the player id. 
    player_id = packet.get_value("header").get("player_car_index", None)
    
    # If there is no player id, abort. 
    if player_id is None:
        return -1, {}
    
    # Motion data packet : (G Forces). 
    if isinstance(packet, PacketMotionData):
        car_motion_data = packet.get_value("car_motion_data")[player_id]
        return 0, car_motion_data
    
    # Extended motion data packet : (Wheel spin).
    if isinstance(packet, PacketMotionExData):
        car_motion_extended_data = packet.to_dict()
        return 1, car_motion_extended_data
    
    # Car telemetry data packet : (Steer angle, tyre temperature).
    elif isinstance(packet, PacketCarTelemetryData):
        car_telemetry_data = packet.get_value("car_telemetry_data")[player_id]
        return 2, car_telemetry_data
    
    # Car damage data packet : (tyre wear).
    elif isinstance(packet, PacketCarDamageData):
        car_telemetry_data = packet.get_value("car_damage_data")[player_id]
        return 3, car_telemetry_data
    
    return -1, {}
