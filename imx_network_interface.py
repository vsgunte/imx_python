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