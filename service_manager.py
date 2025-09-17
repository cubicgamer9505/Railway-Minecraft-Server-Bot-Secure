import os
import sys
import time
import logging
import subprocess
import psutil
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import signal

logger = logging.getLogger(__name__)

class ServiceManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.services = {}
        self.monitoring_active = False
        self.restart_counts = {}
        self.max_restarts = 5
        self.restart_window = 3600  # 1 hour
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_path} not found!")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {self.config_path}!")
            return {}
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop_all_services()
        sys.exit(0)
    
    def register_service(self, name: str, service_class, *args, **kwargs):
        """Register a service for management"""
        self.services[name] = {
            'class': service_class,
            'args': args,
            'kwargs': kwargs,
            'process': None,
            'thread': None,
            'last_restart': None,
            'restart_count': 0
        }
        logger.info(f"Registered service: {name}")
    
    def start_service(self, name: str) -> bool:
        """Start a specific service"""
        if name not in self.services:
            logger.error(f"Service {name} not registered")
            return False
        
        service = self.services[name]
        
        try:
            # Check if service is already running
            if service['process'] and service['process'].is_running():
                logger.info(f"Service {name} is already running")
                return True
            
            # Create and start service instance
            service_instance = service['class'](*service['args'], **service['kwargs'])
            
            # Start service in a separate thread
            service['thread'] = threading.Thread(
                target=self._run_service,
                args=(name, service_instance),
                daemon=True
            )
            service['thread'].start()
            
            logger.info(f"Service {name} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start service {name}: {e}")
            return False
    
    def _run_service(self, name: str, service_instance):
        """Run a service instance"""
        try:
            if hasattr(service_instance, 'run'):
                service_instance.run()
            elif hasattr(service_instance, 'start'):
                service_instance.start()
            else:
                logger.error(f"Service {name} has no run() or start() method")
        except Exception as e:
            logger.error(f"Service {name} crashed: {e}")
            self._handle_service_crash(name)
    
    def stop_service(self, name: str) -> bool:
        """Stop a specific service"""
        if name not in self.services:
            logger.error(f"Service {name} not registered")
            return False
        
        service = self.services[name]
        
        try:
            # Stop the service thread
            if service['thread'] and service['thread'].is_alive():
                # Send stop signal to service if it has one
                if hasattr(service.get('instance'), 'stop'):
                    service['instance'].stop()
                
                # Wait for thread to finish
                service['thread'].join(timeout=10)
                
                if service['thread'].is_alive():
                    logger.warning(f"Service {name} did not stop gracefully")
            
            service['process'] = None
            service['thread'] = None
            logger.info(f"Service {name} stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop service {name}: {e}")
            return False
    
    def restart_service(self, name: str) -> bool:
        """Restart a specific service"""
        logger.info(f"Restarting service: {name}")
        
        # Check restart limits
        if not self._can_restart(name):
            logger.error(f"Service {name} has exceeded restart limits")
            return False
        
        # Stop and start service
        self.stop_service(name)
        time.sleep(2)
        return self.start_service(name)
    
    def _can_restart(self, name: str) -> bool:
        """Check if service can be restarted based on limits"""
        service = self.services[name]
        now = datetime.now()
        
        # Reset restart count if outside restart window
        if (service['last_restart'] and 
            now - service['last_restart'] > timedelta(seconds=self.restart_window)):
            service['restart_count'] = 0
        
        # Check if restart limit exceeded
        if service['restart_count'] >= self.max_restarts:
            return False
        
        # Update restart count and timestamp
        service['restart_count'] += 1
        service['last_restart'] = now
        
        return True
    
    def _handle_service_crash(self, name: str):
        """Handle service crash and restart if needed"""
        logger.warning(f"Service {name} crashed, attempting restart...")
        
        if self._can_restart(name):
            time.sleep(5)  # Wait before restart
            self.start_service(name)
        else:
            logger.error(f"Service {name} exceeded restart limits, not restarting")
    
    def start_all_services(self):
        """Start all registered services"""
        logger.info("Starting all services...")
        
        for name in self.services:
            if not self.start_service(name):
                logger.error(f"Failed to start service: {name}")
    
    def stop_all_services(self):
        """Stop all registered services"""
        logger.info("Stopping all services...")
        
        for name in self.services:
            self.stop_service(name)
    
    def restart_all_services(self):
        """Restart all registered services"""
        logger.info("Restarting all services...")
        
        for name in self.services:
            self.restart_service(name)
    
    def get_service_status(self, name: str) -> Dict:
        """Get status of a specific service"""
        if name not in self.services:
            return {"error": "Service not found"}
        
        service = self.services[name]
        
        status = {
            "name": name,
            "running": False,
            "restart_count": service['restart_count'],
            "last_restart": service['last_restart'].isoformat() if service['last_restart'] else None,
            "can_restart": self._can_restart(name)
        }
        
        # Check if service is actually running
        if service['thread'] and service['thread'].is_alive():
            status["running"] = True
        
        return status
    
    def get_all_status(self) -> Dict:
        """Get status of all services"""
        status = {}
        for name in self.services:
            status[name] = self.get_service_status(name)
        return status
    
    def start_monitoring(self):
        """Start monitoring all services"""
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitor_services, daemon=True)
        monitor_thread.start()
        logger.info("Service monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring services"""
        self.monitoring_active = False
        logger.info("Service monitoring stopped")
    
    def _monitor_services(self):
        """Monitor services and restart if needed"""
        while self.monitoring_active:
            try:
                for name, service in self.services.items():
                    if not service['thread'] or not service['thread'].is_alive():
                        logger.warning(f"Service {name} is not running, attempting restart...")
                        if self._can_restart(name):
                            self.start_service(name)
                        else:
                            logger.error(f"Service {name} exceeded restart limits")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in service monitoring: {e}")
                time.sleep(60)
    
    def create_systemd_service(self, service_name: str = "minecraft-bot") -> str:
        """Create systemd service file for Linux"""
        current_dir = os.getcwd()
        python_path = sys.executable
        
        service_content = f"""[Unit]
Description=Minecraft Server Bot with Radmin VPN
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'minecraft')}
WorkingDirectory={current_dir}
ExecStart={python_path} {current_dir}/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_file = f"/etc/systemd/system/{service_name}.service"
        
        try:
            with open(f"{service_name}.service", 'w') as f:
                f.write(service_content)
            
            logger.info(f"Systemd service file created: {service_name}.service")
            logger.info(f"To install: sudo cp {service_name}.service /etc/systemd/system/")
            logger.info(f"To enable: sudo systemctl enable {service_name}")
            logger.info(f"To start: sudo systemctl start {service_name}")
            
            return service_file
            
        except Exception as e:
            logger.error(f"Failed to create systemd service file: {e}")
            return ""
    
    def create_windows_service(self, service_name: str = "MinecraftBot") -> str:
        """Create Windows service using NSSM (Non-Sucking Service Manager)"""
        current_dir = os.getcwd()
        python_path = sys.executable
        
        nssm_commands = f"""@echo off
echo Installing {service_name} as Windows Service...

nssm install {service_name} "{python_path}"
nssm set {service_name} AppDirectory "{current_dir}"
nssm set {service_name} AppParameters "main.py"
nssm set {service_name} DisplayName "{service_name}"
nssm set {service_name} Description "Minecraft Server Bot with Radmin VPN"
nssm set {service_name} Start SERVICE_AUTO_START

echo Service installed successfully!
echo To start: net start {service_name}
echo To stop: net stop {service_name}
echo To remove: nssm remove {service_name} confirm
"""
        
        batch_file = f"install_{service_name.lower()}_service.bat"
        
        try:
            with open(batch_file, 'w') as f:
                f.write(nssm_commands)
            
            logger.info(f"Windows service installer created: {batch_file}")
            logger.info("Note: You need to install NSSM first: https://nssm.cc/download")
            
            return batch_file
            
        except Exception as e:
            logger.error(f"Failed to create Windows service installer: {e}")
            return ""
    
    def setup_auto_start(self):
        """Setup automatic startup based on operating system"""
        if os.name == 'nt':  # Windows
            return self.create_windows_service()
        else:  # Linux/Unix
            return self.create_systemd_service()
    
    def health_check(self) -> Dict:
        """Perform comprehensive health check"""
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            },
            "overall_status": "healthy"
        }
        
        # Check each service
        for name in self.services:
            service_health = self.get_service_status(name)
            health["services"][name] = service_health
            
            if not service_health.get("running", False):
                health["overall_status"] = "unhealthy"
        
        # Check system resources
        if (health["system"]["cpu_percent"] > 90 or 
            health["system"]["memory_percent"] > 90 or 
            health["system"]["disk_percent"] > 90):
            health["overall_status"] = "warning"
        
        return health
    
    def run_forever(self):
        """Run the service manager indefinitely"""
        logger.info("Starting service manager...")
        
        # Start all services
        self.start_all_services()
        
        # Start monitoring
        self.start_monitoring()
        
        try:
            # Keep running
            while True:
                time.sleep(60)
                
                # Periodic health check
                health = self.health_check()
                if health["overall_status"] != "healthy":
                    logger.warning(f"System health: {health['overall_status']}")
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        finally:
            self.stop_all_services()
            self.stop_monitoring()
            logger.info("Service manager stopped")
