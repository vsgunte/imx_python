# Audio System Documentation

This document provides the complete implementation of the IMX audio system, including all Python classes, configuration file, main program, and consolidated notes. The system supports local and remote audio channels, track playback, network communication, and configuration-based initialization.

## Files and Classes

### 1. `imx_audio_system.py`

```python
class IMXAudioSystem:
    def __init__(self):
        self.channels = []

    def add_channel(self, channel):
        """Add an IMXAudioChannel to the system"""
        self.channels.append(channel)
        channel.set_parent_system(self)

    def remove_channel(self, channel):
        """Remove an IMXAudioChannel from the system"""
        if channel in self.channels:
            self.channels.remove(channel)
            channel.set_parent_system(None)

    def get_channels(self):
        """Return all channels in the system"""
        return self.channels
```

### 2. `imx_audio_channel.py`

```python
class IMXAudioChannel:
    def __init__(self, channel_type="local"):
        self.generator = None
        self.sync_detector = None
        self.parent_system = None
        self.channel_id = None
        self.channel_type = channel_type  # "local" or "remote"
        self.parameters = {
            "volume": 1.0,
            "frequency": 440.0,
            "active": False
        }

    def set_generator(self, generator):
        """Set the IMXAudioGenerator for this channel"""
        self.generator = generator

    def set_sync_detector(self, sync_detector):
        """Set the IMXAudioSyncDetector for this channel"""
        self.sync_detector = sync_detector

    def set_parent_system(self, system):
        """Set the parent IMXAudioSystem"""
        self.parent_system = system

    def get_generator(self):
        """Return the channel's generator"""
        return self.generator

    def get_sync_detector(self):
        """Return the channel's sync detector"""
        return self.sync_detector

    def set_channel_id(self, channel_id):
        """Set the channel identifier"""
        self.channel_id = channel_id

    def get_channel_id(self):
        """Return the channel identifier"""
        return self.channel_id

    def is_remote(self):
        """Check if this is a remote channel"""
        return self.channel_type == "remote"

    def update_parameters(self, parameters):
        """Update channel parameters"""
        self.parameters.update(parameters)
        # Apply parameters to generator if present and local
        if self.generator and not self.is_remote():
            if "frequency" in parameters:
                self.generator.set_sample_rate(int(parameters["frequency"]))
            if "active" in parameters:
                if parameters["active"]:
                    self.generator.start()
                else:
                    self.generator.stop()

    def get_parameters(self):
        """Return current parameters"""
        return self.parameters.copy()
```

### 3. `imx_audio_generator.py`

```python
class IMXAudioGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.is_active = False

    def generate_audio(self):
        """Generate audio data - to be implemented by subclasses"""
        pass

    def start(self):
        """Start audio generation"""
        self.is_active = True

    def stop(self):
        """Stop audio generation"""
        self.is_active = False

    def set_sample_rate(self, rate):
        """Set the sample rate for audio generation"""
        self.sample_rate = rate

    def get_sample_rate(self):
        """Return the current sample rate"""
        return self.sample_rate
```

### 4. `imx_audio_sync_detector.py`

```python
class IMXAudioSyncDetector:
    def __init__(self):
        self.detection_threshold = 0.5
        self.is_enabled = False

    def detect_sync(self, audio_data):
        """Detect synchronization points in audio data"""
        pass

    def enable(self):
        """Enable sync detection"""
        self.is_enabled = True

    def disable(self):
        """Disable sync detection"""
        self.is_enabled = False

    def set_threshold(self, threshold):
        """Set the detection threshold"""
        self.detection_threshold = threshold

    def get_system_channels(self):
        """Access all channels from the parent system"""
        if hasattr(self, 'channel') and self.channel and self.channel.parent_system:
            return self.channel.parent_system.get_channels()
        return []

    def set_channel(self, channel):
        """Set the channel this detector belongs to"""
        self.channel = channel
```

### 5. `imx_network_interface.py`

```python
import socket
import json
import requests

class IMXNetworkInterface:
    def __init__(self, host="localhost", port=5000, rest_base_url="http://localhost:8080"):
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected = False
        self.rest_base_url = rest_base_url

    # Socket methods for local channels
    def connect_socket(self):
        """Establish socket connection for local commands"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Socket connection failed: {e}")
            return False

    def disconnect_socket(self):
        """Close socket connection"""
        if self.socket:
            self.socket.close()
            self.is_connected = False

    def send_socket_parameters(self, channel_id, parameters):
        """Send parameter updates via socket for local channels"""
        if not self.is_connected:
            return False

        try:
            message = {
                "channel_id": channel_id,
                "parameters": parameters
            }
            self.socket.send(json.dumps(message).encode())
            return True
        except Exception as e:
            print(f"Failed to send socket parameters: {e}")
            return False

    def receive_socket_parameters(self):
        """Receive parameter updates from local socket"""
        if not self.is_connected:
            return None

        try:
            data = self.socket.recv(1024).decode()
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Failed to receive socket parameters: {e}")
            return None

    # REST methods for remote channels
    def send_rest_parameters(self, channel_id, parameters):
        """Send parameter updates to remote smart device via REST"""
        try:
            url = f"{self.rest_base_url}/channels/{channel_id}/parameters"
            response = requests.post(url, json=parameters)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"REST POST failed: {e}")
            return False

    def get_rest_parameters(self, channel_id):
        """Get current parameters from remote smart device via REST"""
        try:
            url = f"{self.rest_base_url}/channels/{channel_id}/parameters"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"REST GET failed: {e}")
            return None
```

### 6. `imx_audio_track.py`

```python
class IMXAudioTrack:
    def __init__(self, name, duration, audio_data=None):
        self.name = name
        self.duration = duration  # in seconds
        self.audio_data = audio_data  # Could be file path, raw data, etc.
        self.metadata = {}

    def set_audio_data(self, audio_data):
        """Set the audio data for this track"""
        self.audio_data = audio_data

    def get_audio_data(self):
        """Return the audio data"""
        return self.audio_data

    def set_metadata(self, key, value):
        """Add or update metadata"""
        self.metadata[key] = value

    def get_metadata(self):
        """Return all metadata"""
        return self.metadata.copy()

    def get_duration(self):
        """Return track duration"""
        return self.duration

    def get_name(self):
        """Return track name"""
        return self.name
```

### 7. `imx_audio_player.py`

```python
class IMXAudioPlayer:
    def __init__(self, audio_system):
        self.audio_system = audio_system
        self.current_track = None
        self.is_playing = False
        self.position = 0  # Current position in seconds

    def set_track(self, track):
        """Set the track to play"""
        self.current_track = track
        self.position = 0
        self.is_playing = False

    def play(self):
        """Start playing the current track"""
        if not self.current_track:
            return False

        self.is_playing = True
        self._update_channels()
        print(f"Playing {self.current_track.get_name()} on {len(self.audio_system.get_channels())} channels")
        return True

    def stop(self):
        """Stop playback"""
        self.is_playing = False
        self._update_channels()

    def pause(self):
        """Pause playback"""
        self.is_playing = False
        self._update_channels()

    def seek(self, position):
        """Seek to a specific position in seconds"""
        if self.current_track and 0 <= position <= self.current_track.get_duration():
            self.position = position
            return True
        return False

    def get_position(self):
        """Return current playback position"""
        return self.position

    def get_current_track(self):
        """Return the current track"""
        return self.current_track

    def _update_channels(self):
        """Update channel parameters based on playback state"""
        params = {"active": self.is_playing}
        for channel in self.audio_system.get_channels():
            if not channel.is_remote():  # Local channels only
                channel.update_parameters(params)
            # Remote channels would need network interface updates
```

### 8. `imx_config_manager.py`

```python
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
```

### 9. `main.py`

```python
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
```

### 10. `audio_config.json`

```json
{
  "audio_system": {
    "channels": [
      {
        "channel_id": "local_1",
        "type": "local",
        "parameters": {
          "volume": 0.8,
          "frequency": 440.0,
          "active": false
        }
      },
      {
        "channel_id": "remote_1",
        "type": "remote",
        "parameters": {
          "volume": 0.6,
          "frequency": 880.0,
          "active": false
        }
      }
    ],
    "tracks": [
      {
        "name": "Test Track",
        "duration": 180,
        "audio_data": "path/to/audio.wav",
        "metadata": {
          "artist": "Example Artist",
          "genre": "Test"
        }
      }
    ]
  },
  "network": {
    "socket_host": "localhost",
    "socket_port": 5000,
    "rest_base_url": "http://localhost:8080"
  }
}
```

## Notes

### System Overview

The IMX audio system is a Python-based framework for managing audio channels, tracks, and playback. It supports both local (built-in speakers) and remote (smart speakers/mics) channels, with network communication for parameter updates and a configuration system for initialization.

### Components

- **IMXAudioSystem**: Manages multiple `IMXAudioChannel` instances.
- **IMXAudioChannel**: Represents a channel (local or remote) with optional generator and sync detector.
- **IMXAudioGenerator**: Generates audio for local channels.
- **IMXAudioSyncDetector**: Detects synchronization points, accessing all system channels.
- **IMXNetworkInterface**: Handles socket (local) and REST (remote) communication.
- **IMXAudioTrack**: Represents an audio track with metadata.
- **IMXAudioPlayer**: Plays tracks on the audio system.
- **IMXConfigManager**: Loads JSON configuration to initialize the system.

### Configuration

- **File**: `audio_config.json`
- **Format**: JSON (chosen for Python support, hierarchical structure, REST compatibility).
- **Contents**: Channels, tracks, network settings.
- **Usage**: Loaded by `IMXConfigManager` on startup.
- **Note**: Hardcoded file path; consider command-line arguments for flexibility.

### Dependencies

- **Standard Library**: `socket`, `json`.
- **External**: `requests` (`pip install requests`) for REST.
- **Future**: Audio libraries (`pyaudio`, `sounddevice`), `pyyaml` or `toml` for alternative configs.

### Key Implementation Details

1. **Channel Types**:

   - Local: Built-in speakers, use `IMXAudioGenerator`, updated via sockets.
   - Remote: Smart speakers/mics, updated via REST.

2. **Network Communication**:

   - Socket: TCP, JSON-encoded for local channels (localhost:5000).
   - REST: POST/GET to `/channels/{channel_id}/parameters` for remote channels (localhost:8080).
   - Note: Requires corresponding servers; adjust REST URLs to match device API.

3. **Playback**:

   - Managed by `IMXAudioPlayer`, updates local channel parameters.
   - Remote channels need explicit network calls.
   - Playback is abstract; integrate audio library for real processing.
   - Basic position tracking; add timer/thread for real-time updates.

4. **Configuration Loading**:

   - `IMXConfigManager` builds system from JSON.
   - Loads first track only; extend for multiple tracks.
   - Basic error handling; add validation for production.

### Assumptions

- `audio_config.json` is in the same directory as `main.py`.
- Smart devices expose REST API at configured URL.
- Socket server runs on `localhost:5000`.
- `IMXAudioTrack.audio_data` is abstract (format depends on audio library).

### Considerations for Production

1. **Error Handling**:

   - Minimal; add robust validation, logging.

2. **Scalability**:

   - Support multiple tracks, dynamic loading.
   - Add `IMXAudioSyncDetector` config.
   - Ensure thread-safety for network/playback.

3. **Security**:

   - Use TLS/SSL for network.
   - Sanitize incoming data.

4. **Configuration**:

   - Dynamic file paths.
   - Support YAML/TOML if desired.

5. **Audio Processing**:

   - Integrate audio library.
   - Define `IMXAudioTrack.audio_data` format.

6. **Network**:

   - Add retry logic.
   - Use connection pooling.

### Usage Notes

- Run `main.py` to initialize from `audio_config.json`.
- Install `requests` for REST.
- Ensure socket/REST servers are running.
- System is extensible; add audio processing as needed.

### Potential Enhancements

- Multiple tracks/playlists.
- Real-time position updates.
- `IMXAudioSyncDetector` configuration.
- Dynamic channel management.
- Testing framework.

This document captures the full system as of April 18, 2025. Copy into a `.md` file for reference.
