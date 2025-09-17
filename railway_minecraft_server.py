#!/usr/bin/env python3
"""
Railway Minecraft Server Manager
สร้างและจัดการ Minecraft Server บน Railway
"""

import os
import subprocess
import threading
import time
import json
import logging
from datetime import datetime
from mcstatus import JavaServer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RailwayMinecraftServer:
    def __init__(self):
        self.server_process = None
        self.server_running = False
        self.server_port = int(os.getenv('MINECRAFT_PORT', '25565'))
        self.max_ram = os.getenv('MAX_RAM', '1G')
        self.min_ram = os.getenv('MIN_RAM', '512M')
        self.server_jar = 'server.jar'
        self.world_name = os.getenv('WORLD_NAME', 'world')
        
        # Server properties
        self.server_properties = {
            'server-port': str(self.server_port),
            'online-mode': 'false',
            'enable-command-block': 'true',
            'difficulty': 'normal',
            'gamemode': 'survival',
            'max-players': '10',
            'motd': 'Railway Minecraft Server',
            'pvp': 'true',
            'spawn-protection': '0',
            'allow-nether': 'true',
            'enable-query': 'true',
            'enable-rcon': 'true',
            'rcon.port': '25575',
            'rcon.password': 'railway123'
        }
        
    def download_server_jar(self):
        """ดาวน์โหลด Minecraft Server JAR"""
        try:
            if not os.path.exists(self.server_jar):
                logger.info("Downloading Minecraft Server JAR...")
                
                # ดาวน์โหลด server JAR ล่าสุด
                import requests
                url = "https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar"
                
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(self.server_jar, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info("Minecraft Server JAR downloaded successfully!")
            else:
                logger.info("Minecraft Server JAR already exists")
                
        except Exception as e:
            logger.error(f"Failed to download server JAR: {e}")
            raise
    
    def create_eula(self):
        """สร้างไฟล์ EULA"""
        try:
            with open('eula.txt', 'w') as f:
                f.write('eula=true\n')
            logger.info("EULA accepted")
        except Exception as e:
            logger.error(f"Failed to create EULA: {e}")
            raise
    
    def create_server_properties(self):
        """สร้างไฟล์ server.properties"""
        try:
            with open('server.properties', 'w') as f:
                for key, value in self.server_properties.items():
                    f.write(f'{key}={value}\n')
            logger.info("Server properties created")
        except Exception as e:
            logger.error(f"Failed to create server properties: {e}")
            raise
    
    def start_server(self):
        """เริ่ม Minecraft Server"""
        try:
            if self.server_running:
                logger.warning("Server is already running")
                return
            
            logger.info("Starting Minecraft Server...")
            
            # คำสั่งเริ่ม server
            cmd = [
                'java',
                f'-Xmx{self.max_ram}',
                f'-Xms{self.min_ram}',
                '-jar',
                self.server_jar,
                'nogui'
            ]
            
            # เริ่ม server process
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.server_running = True
            logger.info(f"Minecraft Server started on port {self.server_port}")
            
            # เริ่ม thread สำหรับอ่าน output
            self.output_thread = threading.Thread(target=self.read_server_output)
            self.output_thread.daemon = True
            self.output_thread.start()
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    def read_server_output(self):
        """อ่าน output จาก server"""
        try:
            while self.server_running and self.server_process:
                line = self.server_process.stdout.readline()
                if line:
                    logger.info(f"[SERVER] {line.strip()}")
                else:
                    break
        except Exception as e:
            logger.error(f"Error reading server output: {e}")
    
    def stop_server(self):
        """หยุด Minecraft Server"""
        try:
            if not self.server_running or not self.server_process:
                logger.warning("Server is not running")
                return
            
            logger.info("Stopping Minecraft Server...")
            
            # ส่งคำสั่ง stop
            self.server_process.stdin.write("stop\n")
            self.server_process.stdin.flush()
            
            # รอให้ server หยุด
            self.server_process.wait(timeout=30)
            
            self.server_running = False
            self.server_process = None
            logger.info("Minecraft Server stopped")
            
        except subprocess.TimeoutExpired:
            logger.warning("Server stop timeout, force killing...")
            self.server_process.kill()
            self.server_running = False
            self.server_process = None
        except Exception as e:
            logger.error(f"Failed to stop server: {e}")
            raise
    
    def get_server_status(self):
        """ตรวจสอบสถานะ server"""
        try:
            server = JavaServer.lookup(f"localhost:{self.server_port}")
            status = server.status()
            
            return {
                'online': True,
                'version': status.version.name,
                'players_online': status.players.online,
                'players_max': status.players.max,
                'ping': status.latency,
                'motd': status.description
            }
        except Exception as e:
            return {
                'online': False,
                'error': str(e)
            }
    
    def send_server_command(self, command):
        """ส่งคำสั่งไปยัง server"""
        try:
            if not self.server_running or not self.server_process:
                return False
            
            self.server_process.stdin.write(f"{command}\n")
            self.server_process.stdin.flush()
            return True
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    def setup_server(self):
        """ตั้งค่า server"""
        try:
            logger.info("Setting up Minecraft Server...")
            
            # ดาวน์โหลด server JAR
            self.download_server_jar()
            
            # สร้างไฟล์ EULA
            self.create_eula()
            
            # สร้างไฟล์ server.properties
            self.create_server_properties()
            
            logger.info("Server setup completed!")
            
        except Exception as e:
            logger.error(f"Failed to setup server: {e}")
            raise
    
    def run_forever(self):
        """รัน server ตลอดเวลา"""
        try:
            # ตั้งค่า server
            self.setup_server()
            
            # เริ่ม server
            self.start_server()
            
            logger.info("Minecraft Server is running 24/7 on Railway!")
            logger.info(f"Server Port: {self.server_port}")
            logger.info(f"Max RAM: {self.max_ram}")
            logger.info(f"World: {self.world_name}")
            
            # รอให้ server ทำงาน
            while self.server_running:
                time.sleep(1)
                
                # ตรวจสอบว่า server ยังทำงานอยู่หรือไม่
                if self.server_process and self.server_process.poll() is not None:
                    logger.error("Server process died, restarting...")
                    self.server_running = False
                    time.sleep(5)
                    self.start_server()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping server...")
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            self.stop_server()

def main():
    """Main function"""
    print("=" * 60)
    print("Railway Minecraft Server 24/7")
    print("=" * 60)
    
    server = RailwayMinecraftServer()
    
    try:
        server.run_forever()
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
