#!/usr/bin/env python3
"""
Railway Minecraft Server Bot
Bot สำหรับ Railway platform
"""

import os
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RailwayMinecraftBot:
    def __init__(self):
        # ใช้ environment variables จาก Railway
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.channel_id = os.getenv('DISCORD_CHANNEL_ID')
        self.prefix = os.getenv('DISCORD_PREFIX', '!')
        
        self.server_host = os.getenv('MINECRAFT_SERVER_HOST', '26.97.108.203')
        self.server_port = int(os.getenv('MINECRAFT_SERVER_PORT', '5555'))
        self.server_name = os.getenv('MINECRAFT_SERVER_NAME', 'My Minecraft Server')
        
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '60'))
        
        # Discord bot setup
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
            logger.info(f'Bot is ready to use!')
            
            # เริ่ม monitoring task
            self.monitor_task = asyncio.create_task(self.monitor_server())
        
        @self.bot.event
        async def on_command_error(ctx, error):
            logger.error(f"Command error: {error}")
            await ctx.send(f"Error: {error}")
    
    def setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='ping')
        async def ping(ctx):
            """Test if bot is working"""
            await ctx.send("🏓 Pong! Bot is working on Railway!")
        
        @self.bot.command(name='status')
        async def server_status(ctx):
            """Get server status"""
            try:
                server_address = f"{self.server_host}:{self.server_port}"
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
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                
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
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                await ctx.send(embed=embed)
        
        @self.bot.command(name='players')
        async def list_players(ctx):
            """List online players"""
            try:
                server_address = f"{self.server_host}:{self.server_port}"
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
                embed.add_field(name="Platform", value="🚂 Railway", inline=True)
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Failed to get player list: {e}")
        
        @self.bot.command(name='info')
        async def bot_info(ctx):
            """Show bot information"""
            embed = discord.Embed(
                title="🤖 Railway Minecraft Bot",
                description="Minecraft Server Bot running on Railway",
                color=0x0099ff
            )
            embed.add_field(name="Platform", value="🚂 Railway", inline=True)
            embed.add_field(name="Server", value=f"{self.server_host}:{self.server_port}", inline=True)
            embed.add_field(name="Uptime", value="24/7", inline=True)
            embed.add_field(name="Commands", value="!ping, !status, !players, !info", inline=False)
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name='railway')
        async def railway_info(ctx):
            """Show Railway specific information"""
            embed = discord.Embed(
                title="🚂 Railway Platform Info",
                description="Bot is running on Railway platform",
                color=0x00d4aa
            )
            embed.add_field(name="Platform", value="Railway", inline=True)
            embed.add_field(name="Auto-deploy", value="✅ Enabled", inline=True)
            embed.add_field(name="Uptime", value="24/7", inline=True)
            embed.add_field(name="Monitoring", value="✅ Active", inline=True)
            
            await ctx.send(embed=embed)
    
    async def monitor_server(self):
        """Monitor server status and send notifications"""
        await self.bot.wait_until_ready()
        
        channel = self.bot.get_channel(int(self.channel_id)) if self.channel_id else None
        
        last_status = None
        
        while not self.bot.is_closed():
            try:
                server_address = f"{self.server_host}:{self.server_port}"
                server = JavaServer.lookup(server_address)
                status = server.status()
                
                current_status = "online"
                
                # ส่งการแจ้งเตือนเมื่อ server กลับมาออนไลน์
                if last_status == "offline" and current_status == "online":
                    if channel:
                        embed = discord.Embed(
                            title="🟢 Server Back Online!",
                            description=f"Server {server_address} is now online",
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
                            description=f"Server {server_address} is offline: {e}",
                            color=0xff0000
                        )
                        await channel.send(embed=embed)
                
                last_status = current_status
            
            # รอจนกว่าจะถึงรอบถัดไป
            await asyncio.sleep(self.check_interval)
    
    def run(self):
        """Start the bot"""
        if not self.discord_token:
            logger.error("DISCORD_BOT_TOKEN not found in environment variables!")
            return
        
        logger.info("Starting Railway Minecraft Bot...")
        logger.info(f"Server: {self.server_host}:{self.server_port}")
        logger.info(f"Platform: Railway")
        
        self.bot.run(self.discord_token)

if __name__ == "__main__":
    bot = RailwayMinecraftBot()
    bot.run()
