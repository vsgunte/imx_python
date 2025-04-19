from imx_config_manager import IMXConfigManager

def main():
    # Load configuration and build system
    config_manager = IMXConfigManager("audio_config.json")
    if not config_manager.load_config():
        print("Failed to initialize system")
        return
        
    audio_system, network_interface, player = config_manager.build_audio_system()
    
    # Example usage
    print(f"Loaded {len(audio_system.get_channels())} channels")
    for channel in audio_system.get_channels():
        print(f"Channel {channel.get_channel_id()} ({channel.channel_type}): {channel.get_parameters()}")
    
    print(f"Current track: {player.get_current_track().get_name()}")
    player.play()
    
    # Example network interaction
    if network_interface.connect_socket():
        for channel in audio_system.get_channels():
            if not channel.is_remote():
                network_interface.send_socket_parameters(channel.get_channel_id(), {"active": True})
        network_interface.disconnect_socket()

if __name__ == "__main__":
    main()