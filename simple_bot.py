#!/usr/bin/env python3
"""
Simple Minecraft Server Bot
A simplified version without complex service management
"""

import discord
from discord.ext import commands
import asyncio
import json
import logging
import time
from datetime import datetime
from mcstatus import JavaServer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleMinecraftBot:
    def __init__(self):
        self.config = self.load_config()
        self.server_running = False
        self.startup_time = None
        
        # Discord bot setup with message content intent
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.config['discord']['prefix'], intents=intents)
        
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
            logger.info(f'Bot is ready to use!')
        
        @self.bot.event
        async def on_command_error(ctx, error):
            logger.error(f"Command error: {error}")
            await ctx.send(f"Error: {error}")
    
    def setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='ping')
        async def ping(ctx):
            """Test if bot is working"""
            await ctx.send("🏓 Pong! Bot is working!")
        
        @self.bot.command(name='status')
        async def server_status(ctx):
            """Get server status"""
            try:
                server_host = self.config['minecraft'].get('server_host', 'localhost')
                server_port = self.config['minecraft'].get('server_port', 25565)
                server_address = f"{server_host}:{server_port}"
                
                server = JavaServer.lookup(server_address)
                status = server.status()
                
                embed = discord.Embed(
                    title="🟢 Minecraft Server Status", 
                    color=0x00ff00
                )
                embed.add_field(name="Server", value=server_address, inline=False)
                embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
                embed.add_field(name="Version", value=status.version.name, inline=True)
                embed.add_field(name="Ping", value=f"{status.latency:.1f}ms", inline=True)
                
                if status.players.sample:
                    player_list = ", ".join([player.name for player in status.players.sample])
                    embed.add_field(name="Online Players", value=player_list, inline=False)
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                embed = discord.Embed(
                    title="🔴 Server Offline", 
                    description=f"Could not connect to server: {e}",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
        
        @self.bot.command(name='players')
        async def list_players(ctx):
            """List online players"""
            try:
                server_host = self.config['minecraft'].get('server_host', 'localhost')
                server_port = self.config['minecraft'].get('server_port', 25565)
                server_address = f"{server_host}:{server_port}"
                
                server = JavaServer.lookup(server_address)
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
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Failed to get player list: {e}")
        
        @self.bot.command(name='connect')
        async def connect_to_server(ctx, ip: str = None, port: int = None):
            """Connect to a remote Minecraft server"""
            if ip and port:
                try:
                    server = JavaServer.lookup(f"{ip}:{port}")
                    status = server.status()
                    
                    # Update config
                    self.config['minecraft']['server_host'] = ip
                    self.config['minecraft']['server_port'] = port
                    
                    with open('config.json', 'w') as f:
                        json.dump(self.config, f, indent=2)
                    
                    embed = discord.Embed(
                        title="✅ Connected to Server",
                        description=f"Successfully connected to {ip}:{port}",
                        color=0x00ff00
                    )
                    embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
                    embed.add_field(name="Version", value=status.version.name, inline=True)
                    embed.add_field(name="Ping", value=f"{status.latency:.1f}ms", inline=True)
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    await ctx.send(f"❌ Failed to connect to {ip}:{port}: {e}")
            else:
                await ctx.send("Usage: !connect <ip> <port>\nExample: !connect 26.97.108.203 5555")
        
        @self.bot.command(name='commands')
        async def help_command(ctx):
            """Show available commands"""
            embed = discord.Embed(
                title="🤖 Minecraft Server Bot Commands",
                description="Available commands:",
                color=0x0099ff
            )
            embed.add_field(name="!ping", value="Test if bot is working", inline=False)
            embed.add_field(name="!status", value="Get server status", inline=False)
            embed.add_field(name="!players", value="List online players", inline=False)
            embed.add_field(name="!connect <ip> <port>", value="Connect to a server", inline=False)
            embed.add_field(name="!commands", value="Show this help message", inline=False)
            
            await ctx.send(embed=embed)
    
    def run(self):
        """Start the bot"""
        bot_token = self.config['discord']['bot_token']
        if not bot_token or bot_token == "YOUR_DISCORD_BOT_TOKEN":
            logger.error("Please set your Discord bot token in config.json")
            return
        
        logger.info("Starting Simple Minecraft Bot...")
        self.bot.run(bot_token)

if __name__ == "__main__":
    bot = SimpleMinecraftBot()
    bot.run()
