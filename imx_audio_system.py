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