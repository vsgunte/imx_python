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