# 🚂 คู่มือสร้าง Minecraft Server 24/7 บน Railway

## 🎯 **Railway Minecraft Server - ครบทุกอย่างในที่เดียว!**

### **📋 สิ่งที่คุณจะได้:**
- ✅ **Minecraft Server 24/7** บน Railway
- ✅ **Auto-restart** เมื่อ server ล่ม
- ✅ **World backup** อัตโนมัติ
- ✅ **Player monitoring** แบบ real-time
- ✅ **Web interface** สำหรับจัดการ
- ✅ **Discord integration** (optional)

## 🚀 **ขั้นตอนการสร้าง**

### **1. เตรียมไฟล์**

ผมได้สร้างไฟล์ที่จำเป็นให้แล้ว:

#### **ไฟล์หลัก:**
- `railway_minecraft_server.py` - Server manager
- `railway_server_requirements.txt` - Dependencies
- `railway_server.json` - Railway config
- `Procfile` - Process definition

### **2. สร้าง GitHub Repository**

```bash
# สร้าง repository ใหม่
git init
git add .
git commit -m "Railway Minecraft Server"
git branch -M main
git remote add origin https://github.com/yourusername/railway-minecraft-server.git
git push -u origin main
```

### **3. Deploy บน Railway**

1. ไปที่ [Railway Dashboard](https://railway.app/dashboard)
2. คลิก "New Project"
3. เลือก "Deploy from GitHub repo"
4. เลือก repository ของคุณ
5. Railway จะ auto-deploy

### **4. ตั้งค่า Environment Variables**

ใน Railway Dashboard → Variables:

```bash
# Server Settings
MINECRAFT_PORT=25565
MAX_RAM=1G
MIN_RAM=512M
WORLD_NAME=railway_world

# Server Properties
SERVER_MOTD=Railway Minecraft Server
MAX_PLAYERS=10
DIFFICULTY=normal
GAMEMODE=survival
PVP=true
SPAWN_PROTECTION=0
ALLOW_NETHER=true

# Optional: Discord Integration
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

### **5. ตรวจสอบการทำงาน**

1. ไปที่ Railway Dashboard
2. คลิกที่ project ของคุณ
3. ดู logs ใน "Deployments" tab
4. Server จะเริ่มทำงานอัตโนมัติ

## 🎮 **การใช้งาน**

### **เชื่อมต่อกับ Server:**
- **IP**: Railway จะให้ public URL
- **Port**: 25565 (หรือตามที่ตั้งค่า)
- **Version**: Minecraft 1.21.8 (ล่าสุด)

### **คำสั่ง Server:**
- `/help` - ดูคำสั่งทั้งหมด
- `/list` - ดูผู้เล่นออนไลน์
- `/time set day` - เปลี่ยนเป็นกลางวัน
- `/weather clear` - เปลี่ยนเป็นอากาศดี
- `/gamemode creative` - เปลี่ยนเป็น creative mode

## 🔧 **การจัดการ Server**

### **ผ่าน Railway Dashboard:**
1. **Logs** - ดู server logs
2. **Metrics** - ดู CPU, RAM usage
3. **Variables** - แก้ไขการตั้งค่า
4. **Deployments** - ดู deployment history

### **ผ่าน Minecraft:**
- **OP Commands** - ใช้คำสั่ง admin
- **Console** - ดู server console
- **Players** - จัดการผู้เล่น

## 📊 **Monitoring & Stats**

### **Server Stats:**
- **Uptime** - เวลาทำงาน
- **Players** - จำนวนผู้เล่น
- **TPS** - Ticks per second
- **RAM Usage** - การใช้ RAM
- **CPU Usage** - การใช้ CPU

### **Auto-Monitoring:**
- **Health Check** - ตรวจสอบ server health
- **Auto-Restart** - restart เมื่อล่ม
- **Backup** - backup world อัตโนมัติ
- **Alerts** - แจ้งเตือนเมื่อมีปัญหา

## 💾 **World Management**

### **Backup System:**
- **Auto Backup** - backup ทุก 6 ชั่วโมง
- **Manual Backup** - backup ด้วยคำสั่ง
- **Restore** - restore world จาก backup
- **Download** - ดาวน์โหลด world file

### **World Settings:**
- **Seed** - ตั้งค่า world seed
- **Biomes** - เลือก biome
- **Structures** - เปิด/ปิด structures
- **Difficulty** - ตั้งค่าความยาก

## 🎯 **ข้อดีของ Railway Server**

### **✅ ข้อดี:**
- **24/7 Uptime** - ทำงานตลอดเวลา
- **Auto-Scale** - ปรับขนาดอัตโนมัติ
- **Easy Setup** - ตั้งง่าย
- **No Maintenance** - ไม่ต้องดูแล
- **Free Tier** - ฟรี $5 credit/เดือน
- **Global CDN** - เร็วทั่วโลก

### **📊 ราคา:**
- **Free**: $5 credit/เดือน
- **Pro**: $5/เดือน
- **Team**: $20/เดือน

### **🔧 Features:**
- **Auto-deploy** จาก GitHub
- **Environment variables**
- **Logs & monitoring**
- **Custom domains**
- **SSL certificates**

## 🆘 **Troubleshooting**

### **Server ไม่เริ่ม:**
1. ตรวจสอบ logs ใน Railway Dashboard
2. ตรวจสอบ Environment Variables
3. ตรวจสอบ RAM settings

### **ผู้เล่นเชื่อมต่อไม่ได้:**
1. ตรวจสอบ port settings
2. ตรวจสอบ firewall
3. ตรวจสอบ server status

### **Server ล่มบ่อย:**
1. เพิ่ม RAM allocation
2. ตรวจสอบ world size
3. ตรวจสอบ player count

## 💡 **Tips & Best Practices**

### **Performance:**
1. **ใช้ RAM ที่เหมาะสม** - 1-2GB สำหรับ 10 players
2. **ตั้งค่า spawn protection** - ป้องกัน spawn
3. **ใช้ command blocks** - สำหรับ automation
4. **Backup เป็นประจำ** - ป้องกันข้อมูลหาย

### **Security:**
1. **ตั้งค่า whitelist** - จำกัดผู้เล่น
2. **ใช้ strong passwords** - สำหรับ rcon
3. **Monitor logs** - ตรวจสอบกิจกรรม
4. **Update regularly** - อัปเดต server

### **Management:**
1. **ใช้ plugins** - เพิ่มฟีเจอร์
2. **ตั้งค่า rules** - กฎเกณฑ์ server
3. **สร้าง community** - สร้างชุมชน
4. **Monitor activity** - ตรวจสอบกิจกรรม

## 🚀 **Advanced Features**

### **Discord Integration:**
- **Server Status** - แสดงสถานะใน Discord
- **Player Notifications** - แจ้งเตือนผู้เล่นเข้า/ออก
- **Admin Commands** - คำสั่ง admin ผ่าน Discord
- **Chat Bridge** - เชื่อม chat ระหว่าง Minecraft และ Discord

### **Web Interface:**
- **Server Control** - ควบคุม server ผ่าน web
- **Player Management** - จัดการผู้เล่น
- **World Browser** - ดู world map
- **Statistics** - ดูสถิติ server

### **API Integration:**
- **REST API** - สำหรับ external tools
- **WebSocket** - สำหรับ real-time updates
- **Database** - เก็บข้อมูลผู้เล่น
- **Analytics** - วิเคราะห์ข้อมูล

## 🎉 **สรุป**

**Railway Minecraft Server เป็นวิธีที่ดีที่สุดสำหรับ:**
- **ผู้เริ่มต้น** - ตั้งง่าย ใช้งานง่าย
- **ผู้เล่นทั่วไป** - ราคาถูก มีฟีเจอร์ครบ
- **Server Owner** - ไม่ต้องดูแล server เอง
- **Developers** - มี API และ tools ครบ

**เริ่มต้นได้เลยด้วย $5 credit ฟรี!** 🚂✨
