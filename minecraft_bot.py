import discord
from discord.ext import commands, tasks
import asyncio
import subprocess
import psutil
import json
import logging
import time
import os
import schedule
from mcstatus import JavaServer
import requests
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MinecraftServerBot:
    def __init__(self):
        self.config = self.load_config()
        self.server_process = None
        self.server_running = False
        self.last_restart = None
        self.startup_time = None
        
        # Discord bot setup
        intents = discord.Intents.default()
        intents.message_content = True
        # Disable privileged intents to avoid permission issues
        intents.guilds = False
        intents.members = False
        intents.presences = False
        self.bot = commands.Bot(command_prefix=self.config['discord']['prefix'], intents=intents)
        
        # Setup bot events and commands
        self.setup_events()
        self.setup_commands()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("config.json not found!")
            return {}
        except json.JSONDecodeError:
            logger.error("Invalid JSON in config.json!")
            return {}
    
    def setup_events(self):
        """Setup Discord bot events"""
        @self.bot.event
        async def on_ready():
            logger.info(f'{self.bot.user} has connected to Discord!')
            self.monitor_server.start()
            self.health_check.start()
            if self.config['radmin_vpn']['enabled']:
                self.radmin_vpn_check.start()
        
        @self.bot.event
        async def on_command_error(ctx, error):
            logger.error(f"Command error: {error}")
            await ctx.send(f"Error: {error}")
    
    def setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='start')
        async def start_server(ctx):
            """Start the Minecraft server"""
            if self.server_running:
                await ctx.send("Server is already running!")
                return
            
            try:
                await self.start_minecraft_server()
                await ctx.send("✅ Minecraft server started successfully!")
            except Exception as e:
                logger.error(f"Failed to start server: {e}")
                await ctx.send(f"❌ Failed to start server: {e}")
        
        @self.bot.command(name='stop')
        async def stop_server(ctx):
            """Stop the Minecraft server"""
            if not self.server_running:
                await ctx.send("Server is not running!")
                return
            
            try:
                await self.stop_minecraft_server()
                await ctx.send("✅ Minecraft server stopped successfully!")
            except Exception as e:
                logger.error(f"Failed to stop server: {e}")
                await ctx.send(f"❌ Failed to stop server: {e}")
        
        @self.bot.command(name='restart')
        async def restart_server(ctx):
            """Restart the Minecraft server"""
            try:
                await self.restart_minecraft_server()
                await ctx.send("✅ Minecraft server restarted successfully!")
            except Exception as e:
                logger.error(f"Failed to restart server: {e}")
                await ctx.send(f"❌ Failed to restart server: {e}")
        
        @self.bot.command(name='status')
        async def server_status(ctx):
            """Get server status"""
            status = await self.get_server_status()
            embed = discord.Embed(title="Minecraft Server Status", color=0x00ff00 if self.server_running else 0xff0000)
            embed.add_field(name="Status", value="🟢 Online" if self.server_running else "🔴 Offline", inline=False)
            embed.add_field(name="Uptime", value=status.get('uptime', 'N/A'), inline=True)
            embed.add_field(name="Players", value=f"{status.get('players_online', 0)}/{status.get('max_players', 0)}", inline=True)
            embed.add_field(name="RAM Usage", value=status.get('ram_usage', 'N/A'), inline=True)
            embed.add_field(name="Last Restart", value=status.get('last_restart', 'N/A'), inline=False)
            await ctx.send(embed=embed)
        
        @self.bot.command(name='players')
        async def list_players(ctx):
            """List online players"""
            if not self.server_running:
                await ctx.send("Server is not running!")
                return
            
            try:
                players = await self.get_online_players()
                if players:
                    player_list = "\n".join([f"• {player}" for player in players])
                    embed = discord.Embed(title="Online Players", description=player_list, color=0x00ff00)
                else:
                    embed = discord.Embed(title="Online Players", description="No players online", color=0xffaa00)
                await ctx.send(embed=embed)
            except Exception as e:
                logger.error(f"Failed to get players: {e}")
                await ctx.send(f"❌ Failed to get player list: {e}")
        
        @self.bot.command(name='backup')
        async def create_backup(ctx):
            """Create a server backup"""
            try:
                await self.create_server_backup()
                await ctx.send("✅ Server backup created successfully!")
            except Exception as e:
                logger.error(f"Failed to create backup: {e}")
                await ctx.send(f"❌ Failed to create backup: {e}")
        
        @self.bot.command(name='connect')
        async def connect_to_server(ctx, ip: str = None, port: int = None):
            """Connect to a remote Minecraft server"""
            if ip and port:
                # Update server connection
                self.config['minecraft']['server_host'] = ip
                self.config['minecraft']['server_port'] = port
                
                # Save config
                with open('config.json', 'w') as f:
                    json.dump(self.config, f, indent=2)
                
                # Test connection
                try:
                    server = JavaServer.lookup(f"{ip}:{port}")
                    status = server.status()
                    embed = discord.Embed(
                        title="✅ Connected to Server",
                        description=f"Successfully connected to {ip}:{port}",
                        color=0x00ff00
                    )
                    embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
                    embed.add_field(name="Version", value=status.version.name, inline=True)
                    await ctx.send(embed=embed)
                    
                    # Mark as running
                    self.server_running = True
                    self.startup_time = datetime.now()
                    
                except Exception as e:
                    await ctx.send(f"❌ Failed to connect to {ip}:{port}: {e}")
            else:
                await ctx.send("Usage: !connect <ip> <port>\nExample: !connect 26.97.108.203 5555")
        
        @self.bot.command(name='disconnect')
        async def disconnect_from_server(ctx):
            """Disconnect from current server"""
            if self.server_running:
                self.server_running = False
                await ctx.send("✅ Disconnected from server")
            else:
                await ctx.send("❌ Not connected to any server")
    
    async def start_minecraft_server(self):
        """Start the Minecraft server or connect to remote server"""
        if self.server_running:
            return
        
        server_host = self.config['minecraft'].get('server_host', 'localhost')
        
        # If connecting to remote server, just mark as running
        if server_host != 'localhost':
            self.server_running = True
            self.startup_time = datetime.now()
            logger.info(f"Connected to remote Minecraft server at {server_host}:{self.config['minecraft'].get('server_port', 25565)}")
            return
        
        # Local server startup
        server_path = self.config['minecraft']['server_path']
        max_ram = self.config['minecraft']['max_ram']
        min_ram = self.config['minecraft']['min_ram']
        
        # Java command to start the server
        cmd = [
            'java',
            f'-Xmx{max_ram}',
            f'-Xms{min_ram}',
            '-jar',
            server_path,
            'nogui'
        ]
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(server_path)
            )
            
            self.server_running = True
            self.startup_time = datetime.now()
            logger.info("Minecraft server started successfully")
            
            # Wait a bit for server to fully start
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    async def stop_minecraft_server(self):
        """Stop the Minecraft server gracefully"""
        if not self.server_running:
            return
        
        server_host = self.config['minecraft'].get('server_host', 'localhost')
        
        # If connecting to remote server, just mark as not running
        if server_host != 'localhost':
            self.server_running = False
            logger.info(f"Disconnected from remote Minecraft server at {server_host}:{self.config['minecraft'].get('server_port', 25565)}")
            return
        
        # Local server shutdown
        if not self.server_process:
            return
        
        try:
            # Send stop command to server
            self.server_process.stdin.write("stop\n")
            self.server_process.stdin.flush()
            
            # Wait for process to terminate
            self.server_process.wait(timeout=30)
            
            self.server_running = False
            self.server_process = None
            logger.info("Minecraft server stopped successfully")
            
        except subprocess.TimeoutExpired:
            # Force kill if graceful stop fails
            self.server_process.kill()
            self.server_running = False
            self.server_process = None
            logger.warning("Server was force killed after timeout")
        except Exception as e:
            logger.error(f"Failed to stop server: {e}")
            raise
    
    async def restart_minecraft_server(self):
        """Restart the Minecraft server"""
        if self.server_running:
            await self.stop_minecraft_server()
            await asyncio.sleep(5)
        
        await self.start_minecraft_server()
        self.last_restart = datetime.now()
        logger.info("Minecraft server restarted")
    
    async def get_server_status(self):
        """Get comprehensive server status"""
        status = {
            'uptime': 'N/A',
            'players_online': 0,
            'max_players': 0,
            'ram_usage': 'N/A',
            'last_restart': 'N/A'
        }
        
        if self.server_running and self.startup_time:
            uptime = datetime.now() - self.startup_time
            status['uptime'] = str(uptime).split('.')[0]  # Remove microseconds
        
        if self.last_restart:
            status['last_restart'] = self.last_restart.strftime("%Y-%m-%d %H:%M:%S")
        
        # Get RAM usage
        if self.server_process:
            try:
                process = psutil.Process(self.server_process.pid)
                ram_mb = process.memory_info().rss / 1024 / 1024
                status['ram_usage'] = f"{ram_mb:.1f} MB"
            except:
                pass
        
        # Try to get player count from server
        try:
            server_host = self.config['minecraft'].get('server_host', 'localhost')
            server_port = self.config['minecraft'].get('server_port', 25565)
            server_address = f"{server_host}:{server_port}"
            server = JavaServer.lookup(server_address)
            status_info = server.status()
            status['players_online'] = status_info.players.online
            status['max_players'] = status_info.players.max
        except:
            pass
        
        return status
    
    async def get_online_players(self):
        """Get list of online players"""
        try:
            server_host = self.config['minecraft'].get('server_host', 'localhost')
            server_port = self.config['minecraft'].get('server_port', 25565)
            server_address = f"{server_host}:{server_port}"
            server = JavaServer.lookup(server_address)
            status = server.status()
            if status.players.sample:
                return [player.name for player in status.players.sample]
            return []
        except:
            return []
    
    async def create_server_backup(self):
        """Create a backup of the server world"""
        backup_path = self.config['minecraft']['backup_path']
        server_dir = os.path.dirname(self.config['minecraft']['server_path'])
        
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_full_path = os.path.join(backup_path, backup_name)
        
        # Create backup using tar (Windows) or zip
        import shutil
        shutil.make_archive(backup_full_path, 'zip', server_dir)
        
        logger.info(f"Backup created: {backup_name}.zip")
    
    @tasks.loop(seconds=30)
    async def monitor_server(self):
        """Monitor server health and auto-restart if needed"""
        if not self.config['minecraft']['auto_restart']:
            return
        
        if self.server_running and self.server_process:
            # Check if process is still running
            if self.server_process.poll() is not None:
                logger.warning("Server process died, attempting restart...")
                self.server_running = False
                await self.restart_minecraft_server()
                return
            
            # Check if server has been running too long (restart interval)
            if self.startup_time:
                uptime = datetime.now() - self.startup_time
                restart_interval = timedelta(seconds=self.config['minecraft']['restart_interval'])
                
                if uptime > restart_interval:
                    logger.info("Server uptime exceeded restart interval, restarting...")
                    await self.restart_minecraft_server()
    
    @tasks.loop(seconds=60)
    async def health_check(self):
        """Perform health checks on the server"""
        if not self.server_running:
            return
        
        try:
            # Check if server is responding
            server_host = self.config['minecraft'].get('server_host', 'localhost')
            server_port = self.config['minecraft'].get('server_port', 25565)
            server_address = f"{server_host}:{server_port}"
            server = JavaServer.lookup(server_address)
            server.status()
        except:
            logger.warning("Server health check failed - server not responding")
            # Could implement auto-restart here if needed
    
    @tasks.loop(seconds=300)
    async def radmin_vpn_check(self):
        """Check Radmin VPN connection status"""
        if not self.config['radmin_vpn']['enabled']:
            return
        
        try:
            # Check if Radmin VPN is running
            for proc in psutil.process_iter(['pid', 'name']):
                if 'radmin' in proc.info['name'].lower():
                    logger.info("Radmin VPN is running")
                    return
            
            logger.warning("Radmin VPN is not running")
            # Could implement auto-start here if needed
            
        except Exception as e:
            logger.error(f"Radmin VPN check failed: {e}")
    
    def run(self):
        """Start the bot"""
        bot_token = self.config['discord']['bot_token']
        if not bot_token or bot_token == "YOUR_DISCORD_BOT_TOKEN":
            logger.error("Please set your Discord bot token in config.json")
            return
        
        self.bot.run(bot_token)

if __name__ == "__main__":
    bot = MinecraftServerBot()
    bot.run()
