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