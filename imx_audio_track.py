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