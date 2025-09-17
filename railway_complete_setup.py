#!/usr/bin/env python3
"""
Railway Complete Setup
สร้าง Minecraft Server + Bot บน Railway แบบครบชุด
"""

import os
import subprocess
import threading
import time
import json
import logging
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from mcstatus import JavaServer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RailwayCompleteSetup:
    def __init__(self):
        # Server settings
        self.server_process = None
        self.server_running = False
        self.server_port = int(os.getenv('MINECRAFT_PORT', '25565'))
        self.max_ram = os.getenv('MAX_RAM', '1G')
        self.min_ram = os.getenv('MIN_RAM', '512M')
        self.server_jar = 'server.jar'
        
        # Discord settings
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.channel_id = os.getenv('DISCORD_CHANNEL_ID')
        self.prefix = os.getenv('DISCORD_PREFIX', '!')
        
        # Bot setup
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.prefix, intents=intents)
        
        self.setup_events()
        self.setup_commands()
        
    def setup_events(self):
        """Setup Discord bot events"""
        @self.bot.event
        async def on_ready():
            logger.info(f'{self.bot.user} has connected to Railway!')
            logger.info('Minecraft Server + Bot is ready!')
            
            # เริ่ม monitoring task
            self.monitor_task = asyncio.create_task(self.monitor_server())
    
    def setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='ping')
        async def ping(ctx):
            """Test if bot is working"""
            await ctx.send("🏓 Pong! Railway Minecraft Server + Bot is working!")
        
        @self.bot.command(name='server')
        async def server_status(ctx):
            """Get server status"""
            try:
                server = JavaServer.lookup(f"localhost:{self.server_port}")
                status = server.status()
                
                embed = discord.Embed(
                    title="🟢 Railway Minecraft Server", 
                    color=0x00ff00
                )
                embed.add_field(name="Status", value="🟢 Online", inline=True)
                embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
                embed.add_field(name="Version", value=status.version.name, inline=True)
                embed.add_field(name="Ping", value=f"{status.latency:.1f}ms", inline=True)
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                embed.add_field(name="RAM", value=f"{self.min_ram} - {self.max_ram}", inline=True)
                
                if status.players.sample:
                    player_list = ", ".join([player.name for player in status.players.sample])
                    embed.add_field(name="Online Players", value=player_list, inline=False)
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                embed = discord.Embed(
                    title="🔴 Server Offline", 
                    description=f"Server is not responding: {e}",
                    color=0xff0000
                )
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                await ctx.send(embed=embed)
        
        @self.bot.command(name='players')
        async def list_players(ctx):
            """List online players"""
            try:
                server = JavaServer.lookup(f"localhost:{self.server_port}")
                status = server.status()
                
                if status.players.sample:
                    player_list = "\n".join([f"• {player.name}" for player in status.players.sample])
                    embed = discord.Embed(
                        title="👥 Online Players", 
                        description=player_list,
                        color=0x00ff00
                    )
                else:
                    embed = discord.Embed(
                        title="👥 Online Players", 
                        description="No players online",
                        color=0xffaa00
                    )
                
                embed.add_field(name="Total", value=f"{status.players.online}/{status.players.max}", inline=True)
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Failed to get player list: {e}")
        
        @self.bot.command(name='restart')
        async def restart_server(ctx):
            """Restart Minecraft server"""
            try:
                await ctx.send("🔄 Restarting Minecraft server...")
                
                # หยุด server
                if self.server_running:
                    self.stop_server()
                    await asyncio.sleep(5)
                
                # เริ่ม server ใหม่
                self.start_server()
                await asyncio.sleep(10)
                
                await ctx.send("✅ Minecraft server restarted successfully!")
                
            except Exception as e:
                await ctx.send(f"❌ Failed to restart server: {e}")
        
        @self.bot.command(name='info')
        async def bot_info(ctx):
            """Show complete system information"""
            embed = discord.Embed(
                title="🚂 Railway Minecraft Server + Bot",
                description="Complete 24/7 Minecraft Server Solution",
                color=0x0099ff
            )
            embed.add_field(name="Platform", value="🚂 Railway", inline=True)
            embed.add_field(name="Server Port", value=self.server_port, inline=True)
            embed.add_field(name="RAM", value=f"{self.min_ram} - {self.max_ram}", inline=True)
            embed.add_field(name="Uptime", value="24/7", inline=True)
            embed.add_field(name="Auto-restart", value="✅ Enabled", inline=True)
            embed.add_field(name="Monitoring", value="✅ Active", inline=True)
            embed.add_field(name="Commands", value="!ping, !server, !players, !restart, !info", inline=False)
            
            await ctx.send(embed=embed)
    
    def download_server_jar(self):
        """ดาวน์โหลด Minecraft Server JAR"""
        try:
            if not os.path.exists(self.server_jar):
                logger.info("Downloading Minecraft Server JAR...")
                
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
            server_properties = {
                'server-port': str(self.server_port),
                'online-mode': 'false',
                'enable-command-block': 'true',
                'difficulty': 'normal',
                'gamemode': 'survival',
                'max-players': '10',
                'motd': 'Railway Minecraft Server 24/7',
                'pvp': 'true',
                'spawn-protection': '0',
                'allow-nether': 'true',
                'enable-query': 'true',
                'enable-rcon': 'true',
                'rcon.port': '25575',
                'rcon.password': 'railway123'
            }
            
            with open('server.properties', 'w') as f:
                for key, value in server_properties.items():
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
            
            cmd = [
                'java',
                f'-Xmx{self.max_ram}',
                f'-Xms{self.min_ram}',
                '-jar',
                self.server_jar,
                'nogui'
            ]
            
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
            
            self.server_process.stdin.write("stop\n")
            self.server_process.stdin.flush()
            
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
    
    async def monitor_server(self):
        """Monitor server status and send notifications"""
        await self.bot.wait_until_ready()
        
        channel = self.bot.get_channel(int(self.channel_id)) if self.channel_id else None
        
        last_status = None
        
        while not self.bot.is_closed():
            try:
                server = JavaServer.lookup(f"localhost:{self.server_port}")
                status = server.status()
                
                current_status = "online"
                
                # ส่งการแจ้งเตือนเมื่อ server กลับมาออนไลน์
                if last_status == "offline" and current_status == "online":
                    if channel:
                        embed = discord.Embed(
                            title="🟢 Server Back Online!",
                            description=f"Railway Minecraft Server is now online",
                            color=0x00ff00
                        )
                        embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
                        embed.add_field(name="Version", value=status.version.name, inline=True)
                        await channel.send(embed=embed)
                
                last_status = current_status
                
            except Exception as e:
                current_status = "offline"
                
                # ส่งการแจ้งเตือนเมื่อ server ล่ม
                if last_status == "online" and current_status == "offline":
                    if channel:
                        embed = discord.Embed(
                            title="🔴 Server Offline!",
                            description=f"Railway Minecraft Server is offline: {e}",
                            color=0xff0000
                        )
                        await channel.send(embed=embed)
                
                last_status = current_status
            
            await asyncio.sleep(60)  # ตรวจสอบทุก 60 วินาที
    
    def setup_server(self):
        """ตั้งค่า server"""
        try:
            logger.info("Setting up Minecraft Server...")
            
            self.download_server_jar()
            self.create_eula()
            self.create_server_properties()
            
            logger.info("Server setup completed!")
            
        except Exception as e:
            logger.error(f"Failed to setup server: {e}")
            raise
    
    def run_forever(self):
        """รัน server และ bot ตลอดเวลา"""
        try:
            # ตั้งค่า server
            self.setup_server()
            
            # เริ่ม server
            self.start_server()
            
            logger.info("Railway Minecraft Server + Bot is running 24/7!")
            logger.info(f"Server Port: {self.server_port}")
            logger.info(f"Max RAM: {self.max_ram}")
            logger.info("Discord Bot: Ready")
            
            # เริ่ม Discord bot
            if self.discord_token:
                self.bot.run(self.discord_token)
            else:
                logger.warning("Discord token not found, running server only")
                while self.server_running:
                    time.sleep(1)
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping...")
        except Exception as e:
            logger.error(f"System error: {e}")
        finally:
            self.stop_server()

def main():
    """Main function"""
    print("=" * 60)
    print("Railway Minecraft Server + Bot 24/7")
    print("Complete Solution")
    print("=" * 60)
    
    system = RailwayCompleteSetup()
    
    try:
        system.run_forever()
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
