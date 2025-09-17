#!/usr/bin/env python3
"""
Minecraft Server Monitor
ตรวจสอบและ restart server อัตโนมัติ
"""

import time
import json
import logging
import subprocess
import psutil
from datetime import datetime, timedelta
from mcstatus import JavaServer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self):
        self.config = self.load_config()
        self.server_host = self.config['minecraft'].get('server_host', 'localhost')
        self.server_port = self.config['minecraft'].get('server_port', 25565)
        self.check_interval = 60  # ตรวจสอบทุก 60 วินาที
        self.max_retries = 3
        self.retry_count = 0
        self.last_online = None
        self.offline_count = 0
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("config.json not found!")
            return {}
    
    def check_server_status(self):
        """ตรวจสอบสถานะ server"""
        try:
            server = JavaServer.lookup(f"{self.server_host}:{self.server_port}")
            status = server.status()
            
            self.retry_count = 0
            self.offline_count = 0
            self.last_online = datetime.now()
            
            logger.info(f"✅ Server Online - Players: {status.players.online}/{status.players.max} - Ping: {status.latency:.1f}ms")
            return True
            
        except Exception as e:
            self.offline_count += 1
            logger.warning(f"❌ Server Offline (Attempt {self.offline_count}): {e}")
            return False
    
    def send_discord_notification(self, message):
        """ส่งการแจ้งเตือนไป Discord (ถ้ามี webhook)"""
        # สามารถเพิ่ม Discord webhook ได้ที่นี่
        logger.info(f"📢 Notification: {message}")
    
    def restart_server(self):
        """Restart server (สำหรับ local server)"""
        if self.server_host == 'localhost':
            logger.info("🔄 Attempting to restart local server...")
            # เพิ่มโค้ด restart local server ได้ที่นี่
        else:
            logger.info("🔄 Remote server restart not supported")
    
    def monitor_loop(self):
        """ลูปตรวจสอบ server"""
        logger.info(f"🚀 Starting server monitor for {self.server_host}:{self.server_port}")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds")
        
        while True:
            try:
                is_online = self.check_server_status()
                
                if not is_online:
                    if self.offline_count >= self.max_retries:
                        logger.error(f"💥 Server offline for {self.offline_count} consecutive checks!")
                        self.send_discord_notification(f"Server {self.server_host}:{self.server_port} is offline!")
                        
                        # ลอง restart server
                        self.restart_server()
                        
                        # รีเซ็ต counter
                        self.offline_count = 0
                
                # รอจนกว่าจะถึงรอบถัดไป
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"💥 Monitor error: {e}")
                time.sleep(30)  # รอ 30 วินาทีก่อนลองใหม่
    
    def get_server_stats(self):
        """ดึงสถิติ server"""
        stats = {
            "host": self.server_host,
            "port": self.server_port,
            "last_check": datetime.now().isoformat(),
            "offline_count": self.offline_count,
            "last_online": self.last_online.isoformat() if self.last_online else None
        }
        
        try:
            server = JavaServer.lookup(f"{self.server_host}:{self.server_port}")
            status = server.status()
            stats.update({
                "online": True,
                "version": status.version.name,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "ping": status.latency
            })
        except:
            stats["online"] = False
        
        return stats

def main():
    """Main function"""
    print("=" * 60)
    print("Minecraft Server Monitor")
    print("24/7 Server Monitoring & Auto-Restart")
    print("=" * 60)
    
    monitor = ServerMonitor()
    
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped. Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
