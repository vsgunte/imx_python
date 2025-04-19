import json
from imx_audio_system import IMXAudioSystem
from imx_audio_channel import IMXAudioChannel
from imx_audio_generator import IMXAudioGenerator
from imx_audio_track import IMXAudioTrack
from imx_audio_player import IMXAudioPlayer
from imx_network_interface import IMXNetworkInterface

class IMXConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"Failed to load config: {e}")
            return False
            
    def build_audio_system(self):
        """Build the audio system from configuration"""
        if not self.config:
            return None
            
        # Create audio system
        audio_system = IMXAudioSystem()
        
        # Add channels
        for channel_config in self.config["audio_system"]["channels"]:
            channel = IMXAudioChannel(channel_type=channel_config["type"])
            channel.set_channel_id(channel_config["channel_id"])
            channel.update_parameters(channel_config["parameters"])
            
            if channel_config["type"] == "local":
                channel.set_generator(IMXAudioGenerator())
                
            audio_system.add_channel(channel)
        
        # Create network interface
        network_config = self.config["network"]
        network_interface = IMXNetworkInterface(
            host=network_config["socket_host"],
            port=network_config["socket_port"],
            rest_base_url=network_config["rest_base_url"]
        )
        
        # Create player and load tracks
        player = IMXAudioPlayer(audio_system)
        if self.config["audio_system"]["tracks"]:
            track_config = self.config["audio_system"]["tracks"][0]  # Using first track
            track = IMXAudioTrack(
                name=track_config["name"],
                duration=track_config["duration"],
                audio_data=track_config["audio_data"]
            )
            for key, value in track_config["metadata"].items():
                track.set_metadata(key, value)
            player.set_track(track)
        
        return audio_system, network_interface, player