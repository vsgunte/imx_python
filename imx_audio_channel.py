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