import subprocess
import psutil
import time
import logging
import json
import os
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class RadminVPNManager:
    def __init__(self, config: Dict):
        self.config = config
        self.radmin_path = self.find_radmin_executable()
        self.network_name = config.get('network_name', 'MinecraftServer')
        self.auto_connect = config.get('auto_connect', True)
        self.check_interval = config.get('check_interval', 300)
        
    def find_radmin_executable(self) -> Optional[str]:
        """Find Radmin VPN executable on the system"""
        possible_paths = [
            r"C:\Program Files (x86)\Radmin VPN\RadminVPN.exe",
            r"C:\Program Files\Radmin VPN\RadminVPN.exe",
            r"C:\Users\{}\AppData\Local\Radmin VPN\RadminVPN.exe".format(os.getenv('USERNAME', '')),
            r"C:\Users\{}\AppData\Roaming\Radmin VPN\RadminVPN.exe".format(os.getenv('USERNAME', ''))
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Radmin VPN at: {path}")
                return path
        
        logger.warning("Radmin VPN executable not found in common locations")
        return None
    
    def is_radmin_running(self) -> bool:
        """Check if Radmin VPN is currently running"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and 'radmin' in proc.info['name'].lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking Radmin VPN status: {e}")
            return False
    
    def start_radmin(self) -> bool:
        """Start Radmin VPN application"""
        if not self.radmin_path:
            logger.error("Radmin VPN executable not found")
            return False
        
        try:
            if self.is_radmin_running():
                logger.info("Radmin VPN is already running")
                return True
            
            # Start Radmin VPN
            subprocess.Popen([self.radmin_path], shell=True)
            time.sleep(5)  # Wait for application to start
            
            if self.is_radmin_running():
                logger.info("Radmin VPN started successfully")
                return True
            else:
                logger.error("Failed to start Radmin VPN")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Radmin VPN: {e}")
            return False
    
    def stop_radmin(self) -> bool:
        """Stop Radmin VPN application"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'radmin' in proc.info['name'].lower():
                    proc.terminate()
                    time.sleep(2)
                    if proc.is_running():
                        proc.kill()
            
            logger.info("Radmin VPN stopped")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping Radmin VPN: {e}")
            return False
    
    def get_network_list(self) -> List[Dict]:
        """Get list of available Radmin VPN networks"""
        # This would require Radmin VPN CLI or API access
        # For now, return a placeholder
        return [
            {"name": self.network_name, "status": "available"},
            {"name": "Default Network", "status": "available"}
        ]
    
    def connect_to_network(self, network_name: str = None) -> bool:
        """Connect to a specific Radmin VPN network"""
        if not network_name:
            network_name = self.network_name
        
        try:
            if not self.is_radmin_running():
                if not self.start_radmin():
                    return False
            
            # Note: This would require Radmin VPN CLI commands
            # The actual implementation depends on Radmin VPN's command line interface
            logger.info(f"Attempting to connect to network: {network_name}")
            
            # Placeholder for actual connection logic
            # This would need to be implemented based on Radmin VPN's CLI
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to network {network_name}: {e}")
            return False
    
    def disconnect_from_network(self) -> bool:
        """Disconnect from current Radmin VPN network"""
        try:
            # Placeholder for actual disconnection logic
            logger.info("Disconnecting from Radmin VPN network")
            return True
            
        except Exception as e:
            logger.error(f"Error disconnecting from network: {e}")
            return False
    
    def get_connection_status(self) -> Dict:
        """Get current Radmin VPN connection status"""
        status = {
            "radmin_running": self.is_radmin_running(),
            "connected": False,
            "current_network": None,
            "ip_address": None
        }
        
        try:
            if status["radmin_running"]:
                # Try to get connection details
                # This would require parsing Radmin VPN status
                # For now, return basic status
                pass
                
        except Exception as e:
            logger.error(f"Error getting connection status: {e}")
        
        return status
    
    def get_network_info(self) -> Dict:
        """Get information about the current network"""
        info = {
            "network_name": self.network_name,
            "connected": False,
            "members": [],
            "ip_range": None
        }
        
        try:
            # This would require Radmin VPN API or CLI access
            # For now, return placeholder data
            pass
            
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
        
        return info
    
    def create_network(self, network_name: str, password: str = None) -> bool:
        """Create a new Radmin VPN network"""
        try:
            logger.info(f"Creating network: {network_name}")
            
            # This would require Radmin VPN CLI commands
            # Placeholder implementation
            return True
            
        except Exception as e:
            logger.error(f"Error creating network {network_name}: {e}")
            return False
    
    def join_network(self, network_name: str, password: str = None) -> bool:
        """Join an existing Radmin VPN network"""
        try:
            logger.info(f"Joining network: {network_name}")
            
            # This would require Radmin VPN CLI commands
            # Placeholder implementation
            return True
            
        except Exception as e:
            logger.error(f"Error joining network {network_name}: {e}")
            return False
    
    def setup_auto_connect(self) -> bool:
        """Setup automatic connection to the configured network"""
        if not self.auto_connect:
            return True
        
        try:
            return self.connect_to_network(self.network_name)
        except Exception as e:
            logger.error(f"Error setting up auto-connect: {e}")
            return False
    
    def monitor_connection(self) -> bool:
        """Monitor and maintain VPN connection"""
        try:
            status = self.get_connection_status()
            
            if not status["radmin_running"]:
                logger.warning("Radmin VPN is not running, attempting to start...")
                if not self.start_radmin():
                    return False
            
            if not status["connected"] and self.auto_connect:
                logger.info("Not connected to network, attempting to connect...")
                return self.connect_to_network(self.network_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Error monitoring connection: {e}")
            return False
    
    def get_network_members(self) -> List[Dict]:
        """Get list of members in the current network"""
        members = []
        
        try:
            # This would require Radmin VPN API access
            # For now, return placeholder data
            pass
            
        except Exception as e:
            logger.error(f"Error getting network members: {e}")
        
        return members
    
    def kick_member(self, member_ip: str) -> bool:
        """Kick a member from the network (if admin privileges)"""
        try:
            logger.info(f"Kicking member: {member_ip}")
            
            # This would require admin privileges and Radmin VPN CLI
            # Placeholder implementation
            return True
            
        except Exception as e:
            logger.error(f"Error kicking member {member_ip}: {e}")
            return False
    
    def get_network_statistics(self) -> Dict:
        """Get network usage statistics"""
        stats = {
            "total_members": 0,
            "online_members": 0,
            "bandwidth_usage": 0,
            "uptime": 0
        }
        
        try:
            # This would require Radmin VPN API access
            # For now, return placeholder data
            pass
            
        except Exception as e:
            logger.error(f"Error getting network statistics: {e}")
        
        return stats

# Utility functions for Radmin VPN management
def check_radmin_installation() -> bool:
    """Check if Radmin VPN is installed on the system"""
    manager = RadminVPNManager({})
    return manager.radmin_path is not None

def get_radmin_version() -> Optional[str]:
    """Get Radmin VPN version if installed"""
    try:
        manager = RadminVPNManager({})
        if manager.radmin_path:
            # This would require parsing version from executable
            return "Unknown"
        return None
    except:
        return None

def setup_radmin_for_minecraft() -> bool:
    """Setup Radmin VPN specifically for Minecraft server hosting"""
    try:
        config = {
            "network_name": "MinecraftServer",
            "auto_connect": True,
            "check_interval": 300
        }
        
        manager = RadminVPNManager(config)
        
        # Start Radmin VPN
        if not manager.start_radmin():
            return False
        
        # Connect to network
        if not manager.connect_to_network():
            return False
        
        logger.info("Radmin VPN setup completed for Minecraft server")
        return True
        
    except Exception as e:
        logger.error(f"Error setting up Radmin VPN for Minecraft: {e}")
        return False
