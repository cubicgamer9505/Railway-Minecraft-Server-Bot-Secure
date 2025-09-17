#!/usr/bin/env python3
"""
Minecraft Server Bot with Radmin VPN Integration
24/7 Automated Minecraft Server Management

This bot provides:
- Automated Minecraft server management
- Radmin VPN integration for network connectivity
- Discord bot interface for remote control
- 24/7 monitoring and auto-restart capabilities
- System health monitoring
"""

import os
import sys
import logging
import json
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minecraft_bot import MinecraftServerBot
from radmin_vpn_manager import RadminVPNManager, setup_radmin_for_minecraft
from service_manager import ServiceManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('minecraft_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MinecraftBotService:
    def __init__(self):
        self.config = self.load_config()
        self.service_manager = ServiceManager()
        self.minecraft_bot = None
        self.radmin_manager = None
        self.running = False
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("config.json not found! Please create it first.")
            return {}
        except json.JSONDecodeError:
            logger.error("Invalid JSON in config.json!")
            return {}
    
    def setup_radmin_vpn(self):
        """Setup Radmin VPN for Minecraft server"""
        if not self.config.get('radmin_vpn', {}).get('enabled', False):
            logger.info("Radmin VPN is disabled in configuration")
            return True
        
        try:
            logger.info("Setting up Radmin VPN...")
            self.radmin_manager = RadminVPNManager(self.config['radmin_vpn'])
            
            # Check if Radmin VPN is installed
            if not self.radmin_manager.radmin_path:
                logger.error("Radmin VPN is not installed or not found!")
                logger.info("Please install Radmin VPN from: https://www.radmin-vpn.com/")
                return False
            
            # Setup auto-connect
            if self.config['radmin_vpn'].get('auto_connect', True):
                if not self.radmin_manager.setup_auto_connect():
                    logger.warning("Failed to setup Radmin VPN auto-connect")
                    return False
            
            logger.info("Radmin VPN setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Radmin VPN: {e}")
            return False
    
    def setup_minecraft_bot(self):
        """Setup the Minecraft server bot"""
        try:
            logger.info("Setting up Minecraft server bot...")
            self.minecraft_bot = MinecraftServerBot()
            logger.info("Minecraft server bot setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Minecraft bot: {e}")
            return False
    
    def start(self):
        """Start the Minecraft bot service"""
        logger.info("Starting Minecraft Bot Service...")
        
        # Setup Radmin VPN first
        if not self.setup_radmin_vpn():
            logger.error("Failed to setup Radmin VPN, continuing without it...")
        
        # Setup Minecraft bot
        if not self.setup_minecraft_bot():
            logger.error("Failed to setup Minecraft bot")
            return False
        
        # Register services with service manager
        self.service_manager.register_service(
            'minecraft_bot',
            self.run_minecraft_bot
        )
        
        if self.radmin_manager:
            self.service_manager.register_service(
                'radmin_vpn',
                self.run_radmin_monitor
            )
        
        # Start all services
        self.service_manager.start_all_services()
        
        # Start monitoring
        self.service_manager.start_monitoring()
        
        self.running = True
        logger.info("Minecraft Bot Service started successfully")
        
        return True
    
    def run_minecraft_bot(self):
        """Run the Minecraft bot"""
        try:
            if self.minecraft_bot:
                self.minecraft_bot.run()
        except Exception as e:
            logger.error(f"Minecraft bot error: {e}")
            raise
    
    def run_radmin_monitor(self):
        """Monitor Radmin VPN connection"""
        try:
            while self.running and self.radmin_manager:
                self.radmin_manager.monitor_connection()
                time.sleep(self.config.get('radmin_vpn', {}).get('check_interval', 300))
        except Exception as e:
            logger.error(f"Radmin VPN monitor error: {e}")
            raise
    
    def stop(self):
        """Stop the Minecraft bot service"""
        logger.info("Stopping Minecraft Bot Service...")
        
        self.running = False
        
        # Stop all services
        self.service_manager.stop_all_services()
        self.service_manager.stop_monitoring()
        
        logger.info("Minecraft Bot Service stopped")
    
    def run_forever(self):
        """Run the service indefinitely"""
        try:
            if not self.start():
                logger.error("Failed to start service")
                return
            
            # Keep running
            while self.running:
                time.sleep(60)
                
                # Periodic health check
                health = self.service_manager.health_check()
                if health["overall_status"] != "healthy":
                    logger.warning(f"System health: {health['overall_status']}")
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Service error: {e}")
        finally:
            self.stop()

def main():
    """Main entry point"""
    print("=" * 60)
    print("Minecraft Server Bot with Radmin VPN Integration")
    print("24/7 Automated Minecraft Server Management")
    print("=" * 60)
    
    # Check if config exists
    if not os.path.exists('config.json'):
        print("\n❌ config.json not found!")
        print("Please create config.json first using the setup script.")
        print("Run: python setup.py")
        return
    
    # Create and run service
    service = MinecraftBotService()
    
    try:
        service.run_forever()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
