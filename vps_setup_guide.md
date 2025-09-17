# 🚀 คู่มือตั้งค่า Minecraft Server 24/7 บน VPS

## 📋 **ขั้นตอนการตั้งค่า VPS**

### **1. เลือก VPS Provider**

#### **Oracle Cloud (แนะนำ - ฟรี)**
- ไปที่: https://cloud.oracle.com/
- สร้างบัญชีฟรี
- สร้าง VM Instance (Always Free)
- Specs: 1 OCPU, 1GB RAM, 50GB Storage

#### **AWS EC2 (ฟรี 12 เดือน)**
- ไปที่: https://aws.amazon.com/
- สร้าง EC2 Instance
- เลือก t2.micro (ฟรี)

#### **DigitalOcean ($5/เดือน)**
- ไปที่: https://digitalocean.com/
- สร้าง Droplet
- เลือก Basic Plan $5/เดือน

### **2. ติดตั้ง Java และ Minecraft Server**

```bash
# อัปเดตระบบ
sudo apt update && sudo apt upgrade -y

# ติดตั้ง Java
sudo apt install openjdk-17-jdk -y

# สร้างโฟลเดอร์สำหรับ server
mkdir minecraft-server
cd minecraft-server

# ดาวน์โหลด Minecraft Server
wget https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar

# ตั้งชื่อไฟล์
mv server.jar minecraft_server.jar

# รัน server ครั้งแรก
java -Xmx1G -Xms1G -jar minecraft_server.jar nogui
```

### **3. ตั้งค่า Server**

```bash
# แก้ไข eula.txt
echo "eula=true" > eula.txt

# แก้ไข server.properties
nano server.properties
```

**การตั้งค่าสำคัญ:**
```
server-port=25565
online-mode=false
enable-command-block=true
difficulty=normal
gamemode=survival
max-players=20
```

### **4. สร้าง Systemd Service**

```bash
# สร้างไฟล์ service
sudo nano /etc/systemd/system/minecraft.service
```

**เนื้อหาไฟล์:**
```ini
[Unit]
Description=Minecraft Server
After=network.target

[Service]
Type=simple
User=minecraft
WorkingDirectory=/home/minecraft/minecraft-server
ExecStart=/usr/bin/java -Xmx1G -Xms1G -jar minecraft_server.jar nogui
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **5. เปิดใช้งาน Service**

```bash
# สร้าง user
sudo useradd -m minecraft
sudo chown -R minecraft:minecraft /home/minecraft/minecraft-server

# เปิดใช้งาน service
sudo systemctl enable minecraft
sudo systemctl start minecraft

# ตรวจสอบสถานะ
sudo systemctl status minecraft
```

### **6. ตั้งค่า Firewall**

```bash
# เปิด port 25565
sudo ufw allow 25565

# เปิดใช้งาน firewall
sudo ufw enable
```

### **7. อัปโหลด Bot ไป VPS**

```bash
# อัปโหลดไฟล์ bot
scp -r /path/to/bot user@your-vps-ip:/home/user/

# SSH เข้า VPS
ssh user@your-vps-ip

# ติดตั้ง Python dependencies
cd bot
pip3 install -r requirements.txt

# รัน bot
python3 simple_bot.py
```

### **8. ใช้ Screen/Tmux สำหรับ 24/7**

```bash
# ติดตั้ง screen
sudo apt install screen -y

# สร้าง session ใหม่
screen -S minecraft-bot

# รัน bot
python3 simple_bot.py

# กด Ctrl+A แล้วกด D เพื่อ detach
# กลับมาใช้: screen -r minecraft-bot
```

## 🔧 **การบำรุงรักษา**

### **Backup Server**
```bash
# สร้างสคริปต์ backup
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz world/
```

### **Auto Backup**
```bash
# เพิ่มใน crontab
crontab -e

# Backup ทุก 6 ชั่วโมง
0 */6 * * * /home/minecraft/backup.sh
```

## 📊 **การตรวจสอบ**

### **ตรวจสอบ Server Status**
```bash
# ดู log
sudo journalctl -u minecraft -f

# ตรวจสอบ RAM
free -h

# ตรวจสอบ Disk
df -h
```

### **ตรวจสอบ Bot Status**
```bash
# ดู process
ps aux | grep python

# ดู log
tail -f simple_bot.log
```

## 💡 **Tips**

1. **ใช้ VPS ที่มี RAM อย่างน้อย 1GB**
2. **ตั้งค่า swap file สำหรับ RAM เพิ่มเติม**
3. **ใช้ CloudFlare สำหรับ DDoS Protection**
4. **Backup ข้อมูลเป็นประจำ**
5. **อัปเดตระบบเป็นประจำ**

## 🆘 **Troubleshooting**

### **Server ไม่เริ่ม**
```bash
# ตรวจสอบ log
sudo journalctl -u minecraft -n 50

# ตรวจสอบ Java
java -version

# ตรวจสอบ port
netstat -tlnp | grep 25565
```

### **Bot ไม่ทำงาน**
```bash
# ตรวจสอบ dependencies
pip3 list | grep discord

# ตรวจสอบ config
cat config.json

# รันแบบ debug
python3 -u simple_bot.py
```
