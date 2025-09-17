# Minecraft Server Bot with Radmin VPN Integration

A comprehensive 24/7 automated Minecraft server management bot with Radmin VPN integration for seamless network connectivity.

## Features

### 🎮 Minecraft Server Management
- **Automated Server Control**: Start, stop, restart Minecraft servers
- **Auto-Restart**: Configurable automatic server restarts
- **Backup System**: Automated world backups
- **Player Management**: Monitor online players
- **Resource Monitoring**: Track RAM usage and server performance

### 🌐 Radmin VPN Integration
- **Network Management**: Automatic Radmin VPN connection
- **Connection Monitoring**: Continuous VPN status monitoring
- **Auto-Reconnect**: Automatic reconnection on network issues
- **Network Statistics**: Monitor network usage and members

### 🤖 Discord Bot Interface
- **Remote Control**: Control server from Discord
- **Real-time Status**: Live server status updates
- **Player Commands**: List online players
- **Admin Commands**: Full server management through Discord

### 📊 24/7 Monitoring
- **Health Checks**: Continuous system health monitoring
- **Auto-Recovery**: Automatic service recovery
- **Logging**: Comprehensive logging system
- **Service Management**: Process monitoring and management

## Installation

### Prerequisites
- Python 3.7 or higher
- Java (for Minecraft server)
- Radmin VPN (optional)
- Discord Bot Token

### Quick Setup

1. **Clone or download the project files**

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Follow the interactive setup**:
   - Configure Minecraft server path
   - Set up Discord bot token
   - Configure Radmin VPN (optional)
   - Set monitoring preferences

4. **Start the bot**:
   ```bash
   python main.py
   ```

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create configuration file** (`config.json`):
   ```json
   {
     "minecraft": {
       "server_path": "C:\\Minecraft\\server.jar",
       "server_name": "MyMinecraftServer",
       "max_ram": "4G",
       "min_ram": "2G",
       "auto_restart": true,
       "restart_interval": 86400,
       "backup_interval": 3600,
       "backup_path": "C:\\Minecraft\\backups"
     },
     "discord": {
       "bot_token": "YOUR_DISCORD_BOT_TOKEN",
       "admin_channel_id": "YOUR_ADMIN_CHANNEL_ID",
       "prefix": "!"
     },
     "radmin_vpn": {
       "enabled": true,
       "network_name": "MinecraftServer",
       "auto_connect": true,
       "check_interval": 300
     },
     "monitoring": {
       "log_file": "server_bot.log",
       "max_log_size": 10485760,
       "backup_count": 5,
       "health_check_interval": 60
     }
   }
   ```

## Configuration

### Minecraft Server Settings
- `server_path`: Path to your Minecraft server JAR file (for local servers)
- `server_host`: IP address of the Minecraft server (e.g., "26.97.108.203" or "localhost")
- `server_port`: Port of the Minecraft server (e.g., 5555 or 25565)
- `max_ram`/`min_ram`: Memory allocation for the server (local servers only)
- `auto_restart`: Enable automatic server restarts
- `restart_interval`: Time between restarts (seconds)
- `backup_interval`: Time between backups (seconds)

### Discord Bot Settings
- `bot_token`: Your Discord bot token
- `admin_channel_id`: Channel ID for admin commands
- `prefix`: Command prefix for Discord commands

### Radmin VPN Settings
- `enabled`: Enable Radmin VPN integration
- `network_name`: Name of your Radmin VPN network
- `auto_connect`: Automatically connect to network
- `check_interval`: VPN status check interval

## Discord Commands

| Command | Description |
|---------|-------------|
| `!start` | Start the Minecraft server |
| `!stop` | Stop the Minecraft server |
| `!restart` | Restart the Minecraft server |
| `!status` | Get server status and information |
| `!players` | List online players |
| `!backup` | Create a server backup |
| `!connect <ip> <port>` | Connect to a remote Minecraft server |
| `!disconnect` | Disconnect from current server |

## Radmin VPN Setup

1. **Download and install Radmin VPN**:
   - Visit: https://www.radmin-vpn.com/
   - Download and install the software

2. **Create or join a network**:
   - Create a new network or join an existing one
   - Note the network name for configuration

3. **Configure the bot**:
   - Set `radmin_vpn.enabled` to `true`
   - Set the correct `network_name`
   - Enable `auto_connect` for automatic connection

## Running as a Service

### Windows Service
1. Install NSSM (Non-Sucking Service Manager)
2. Run the generated batch file: `install_minecraftbot_service.bat`
3. Start the service: `net start MinecraftBot`

### Linux Systemd Service
1. Copy the service file: `sudo cp minecraft-bot.service /etc/systemd/system/`
2. Enable the service: `sudo systemctl enable minecraft-bot`
3. Start the service: `sudo systemctl start minecraft-bot`

## File Structure

```
minecraft-bot/
├── main.py                 # Main entry point
├── minecraft_bot.py        # Minecraft server management
├── radmin_vpn_manager.py   # Radmin VPN integration
├── service_manager.py      # Service management and monitoring
├── setup.py               # Setup script
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── logs/                 # Log files directory
```

## Troubleshooting

### Common Issues

1. **Server won't start**:
   - Check Java installation
   - Verify server JAR path
   - Check available RAM

2. **Discord bot not responding**:
   - Verify bot token
   - Check channel ID
   - Ensure bot has proper permissions

3. **Radmin VPN issues**:
   - Verify Radmin VPN installation
   - Check network name
   - Ensure network is accessible

4. **Permission errors**:
   - Run as administrator (Windows)
   - Check file permissions
   - Verify directory access

### Logs
Check the log file (`server_bot.log`) for detailed error information and debugging.

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify configuration settings
3. Ensure all prerequisites are installed
4. Check Discord bot permissions

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
