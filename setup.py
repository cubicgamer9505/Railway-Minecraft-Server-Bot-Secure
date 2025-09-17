#!/usr/bin/env python3
"""
Setup script for Minecraft Server Bot with Radmin VPN Integration
This script helps configure the bot for first-time use.
"""

import os
import json
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("Minecraft Server Bot Setup")
    print("24/7 Automated Minecraft Server Management")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def create_config():
    """Create configuration file interactively"""
    print("\n⚙️  Creating configuration file...")
    
    config = {
        "minecraft": {},
        "discord": {},
        "radmin_vpn": {},
        "monitoring": {}
    }
    
    # Minecraft server configuration
    print("\n🎮 Minecraft Server Configuration:")
    config["minecraft"]["server_path"] = input("Server JAR path (e.g., C:\\Minecraft\\server.jar): ").strip()
    config["minecraft"]["server_name"] = input("Server name (default: MyMinecraftServer): ").strip() or "MyMinecraftServer"
    config["minecraft"]["server_host"] = input("Server IP address (e.g., 26.97.108.203 or localhost): ").strip() or "localhost"
    config["minecraft"]["server_port"] = int(input("Server port (e.g., 5555 or 25565): ").strip() or "25565")
    config["minecraft"]["max_ram"] = input("Maximum RAM (e.g., 4G): ").strip() or "4G"
    config["minecraft"]["min_ram"] = input("Minimum RAM (e.g., 2G): ").strip() or "2G"
    config["minecraft"]["auto_restart"] = input("Auto-restart server? (y/n, default: y): ").strip().lower() != 'n'
    config["minecraft"]["restart_interval"] = int(input("Restart interval in seconds (default: 86400 = 24h): ").strip() or "86400")
    config["minecraft"]["backup_interval"] = int(input("Backup interval in seconds (default: 3600 = 1h): ").strip() or "3600")
    config["minecraft"]["backup_path"] = input("Backup directory (default: C:\\Minecraft\\backups): ").strip() or "C:\\Minecraft\\backups"
    
    # Discord bot configuration
    print("\n🤖 Discord Bot Configuration:")
    config["discord"]["bot_token"] = input("Discord bot token: ").strip()
    config["discord"]["admin_channel_id"] = input("Admin channel ID: ").strip()
    config["discord"]["prefix"] = input("Command prefix (default: !): ").strip() or "!"
    
    # Radmin VPN configuration
    print("\n🌐 Radmin VPN Configuration:")
    config["radmin_vpn"]["enabled"] = input("Enable Radmin VPN? (y/n, default: y): ").strip().lower() != 'n'
    if config["radmin_vpn"]["enabled"]:
        config["radmin_vpn"]["network_name"] = input("Network name (default: MinecraftServer): ").strip() or "MinecraftServer"
        config["radmin_vpn"]["auto_connect"] = input("Auto-connect to network? (y/n, default: y): ").strip().lower() != 'n'
        config["radmin_vpn"]["check_interval"] = int(input("Connection check interval in seconds (default: 300): ").strip() or "300")
    
    # Monitoring configuration
    print("\n📊 Monitoring Configuration:")
    config["monitoring"]["log_file"] = input("Log file name (default: server_bot.log): ").strip() or "server_bot.log"
    config["monitoring"]["max_log_size"] = int(input("Max log size in bytes (default: 10485760 = 10MB): ").strip() or "10485760")
    config["monitoring"]["backup_count"] = int(input("Number of log backups (default: 5): ").strip() or "5")
    config["monitoring"]["health_check_interval"] = int(input("Health check interval in seconds (default: 60): ").strip() or "60")
    
    # Save configuration
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("\n✅ Configuration saved to config.json!")
        return True
    except Exception as e:
        print(f"\n❌ Failed to save configuration: {e}")
        return False

def check_radmin_vpn():
    """Check if Radmin VPN is installed"""
    print("\n🔍 Checking for Radmin VPN installation...")
    
    possible_paths = [
        r"C:\Program Files (x86)\Radmin VPN\RadminVPN.exe",
        r"C:\Program Files\Radmin VPN\RadminVPN.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Radmin VPN found at: {path}")
            return True
    
    print("❌ Radmin VPN not found!")
    print("Please download and install Radmin VPN from: https://www.radmin-vpn.com/")
    return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    try:
        # Create backup directory
        backup_path = input("Backup directory path (default: C:\\Minecraft\\backups): ").strip() or "C:\\Minecraft\\backups"
        os.makedirs(backup_path, exist_ok=True)
        print(f"✅ Created backup directory: {backup_path}")
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        print("✅ Created logs directory")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    print("\n🚀 Creating startup scripts...")
    
    if platform.system() == "Windows":
        # Windows batch file
        batch_content = """@echo off
echo Starting Minecraft Server Bot...
py main.py
pause
"""
        try:
            with open("start_bot.bat", "w") as f:
                f.write(batch_content)
            print("✅ Created start_bot.bat")
        except Exception as e:
            print(f"❌ Failed to create Windows startup script: {e}")
    
    else:
        # Linux/Unix shell script
        shell_content = """#!/bin/bash
echo "Starting Minecraft Server Bot..."
python3 main.py
"""
        try:
            with open("start_bot.sh", "w") as f:
                f.write(shell_content)
            os.chmod("start_bot.sh", 0o755)
            print("✅ Created start_bot.sh")
        except Exception as e:
            print(f"❌ Failed to create Unix startup script: {e}")

def create_discord_bot():
    """Guide user through Discord bot creation"""
    print("\n🤖 Discord Bot Setup Guide:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Click 'New Application' and give it a name")
    print("3. Go to the 'Bot' section")
    print("4. Click 'Add Bot'")
    print("5. Copy the bot token and paste it in the configuration")
    print("6. Enable 'Message Content Intent' in the Bot section")
    print("7. Go to 'OAuth2' > 'URL Generator'")
    print("8. Select 'bot' scope and 'Administrator' permissions")
    print("9. Use the generated URL to invite the bot to your server")
    print("10. Get the channel ID by right-clicking on a channel and selecting 'Copy ID'")
    print()

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📖 Usage Instructions:")
    print("1. Make sure your Minecraft server JAR file is in the specified path")
    print("2. Configure your Discord bot token and channel ID")
    print("3. If using Radmin VPN, make sure it's installed and configured")
    print("4. Run the bot using: python main.py")
    print("5. Use Discord commands to control the server:")
    print("   - !start - Start the Minecraft server")
    print("   - !stop - Stop the Minecraft server")
    print("   - !restart - Restart the Minecraft server")
    print("   - !status - Get server status")
    print("   - !players - List online players")
    print("   - !backup - Create a server backup")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create configuration
    if not create_config():
        return
    
    # Check Radmin VPN
    check_radmin_vpn()
    
    # Create directories
    create_directories()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Show Discord bot setup guide
    create_discord_bot()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n🎉 Setup completed successfully!")
    print("You can now run the bot using: python main.py")
    print("Or use the startup script: start_bot.bat (Windows) or start_bot.sh (Linux)")

if __name__ == "__main__":
    main()
