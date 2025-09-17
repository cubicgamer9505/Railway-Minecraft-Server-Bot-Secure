# 🚂 คู่มือตั้งค่า Minecraft Server Bot บน Railway

## 🎯 **Railway คืออะไร?**
- **Platform-as-a-Service (PaaS)** เหมือน Heroku
- **ฟรี $5 credit** ทุกเดือน
- **Auto-deploy** จาก GitHub
- **ง่ายต่อการใช้งาน**

## 📋 **ขั้นตอนการตั้งค่า**

### **1. สร้างบัญชี Railway**
1. ไปที่ [Railway.app](https://railway.app)
2. สร้างบัญชีด้วย GitHub
3. เชื่อมต่อ GitHub repository

### **2. สร้าง Project ใหม่**
1. คลิก "New Project"
2. เลือก "Deploy from GitHub repo"
3. เลือก repository ของคุณ

### **3. ตั้งค่า Environment Variables**

ใน Railway Dashboard → Variables:

```bash
# Discord Bot Settings
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_PREFIX=!

# Minecraft Server Settings
MINECRAFT_SERVER_HOST=26.97.108.203
MINECRAFT_SERVER_PORT=5555
MINECRAFT_SERVER_NAME=My Minecraft Server

# Bot Settings
LOG_LEVEL=INFO
CHECK_INTERVAL=60
```

### **4. สร้างไฟล์สำหรับ Railway**

ผมได้สร้างไฟล์ที่จำเป็นให้แล้ว:

#### **ไฟล์ที่สร้าง:**
- `railway_bot.py` - Bot สำหรับ Railway
- `railway_requirements.txt` - Dependencies
- `railway.json` - Railway configuration
- `Procfile` - Process definition

### **5. อัปโหลดไป GitHub**

```bash
# สร้าง repository ใหม่
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/minecraft-bot.git
git push -u origin main
```

### **6. Deploy บน Railway**

1. ไปที่ [Railway Dashboard](https://railway.app/dashboard)
2. คลิก "New Project"
3. เลือก "Deploy from GitHub repo"
4. เลือก repository ของคุณ
5. Railway จะ auto-deploy

### **7. ตั้งค่า Environment Variables**

ใน Railway Dashboard → Variables:

```bash
# Discord Bot Settings
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=1346692947290226802
DISCORD_PREFIX=!

# Minecraft Server Settings
MINECRAFT_SERVER_HOST=26.97.108.203
MINECRAFT_SERVER_PORT=5555
MINECRAFT_SERVER_NAME=My Minecraft Server

# Bot Settings
LOG_LEVEL=INFO
CHECK_INTERVAL=60
```

### **8. ตรวจสอบการทำงาน**

1. ไปที่ Railway Dashboard
2. คลิกที่ project ของคุณ
3. ดู logs ใน "Deployments" tab
4. Bot จะเริ่มทำงานอัตโนมัติ

## 🎯 **ข้อดีของ Railway**

### **✅ ข้อดี:**
- **ฟรี $5 credit** ทุกเดือน
- **Auto-deploy** จาก GitHub
- **24/7 uptime** อัตโนมัติ
- **Easy setup** ไม่ต้องตั้งค่า server
- **Auto-restart** เมื่อ bot ล่ม
- **Monitoring** built-in

### **📊 ราคา:**
- **Free Tier**: $5 credit/เดือน
- **Pro**: $5/เดือน
- **Team**: $20/เดือน

### **🔧 Features:**
- **Auto-deploy** จาก GitHub
- **Environment variables** management
- **Logs** และ monitoring
- **Custom domains**
- **SSL certificates**

## 🚀 **คำสั่ง Bot**

เมื่อ deploy เสร็จแล้ว Bot จะมีคำสั่ง:

- `!ping` - ทดสอบ bot
- `!status` - ตรวจสอบ server
- `!players` - ดูผู้เล่นออนไลน์
- `!info` - ข้อมูล bot
- `!railway` - ข้อมูล Railway platform

## 📱 **การใช้งาน**

1. **Bot จะทำงาน 24/7** บน Railway
2. **Auto-monitor** server status
3. **ส่งการแจ้งเตือน** เมื่อ server ล่ม/กลับมา
4. **ไม่ต้องดูแล** server เอง

## 🆘 **Troubleshooting**

### **Bot ไม่ทำงาน**
1. ตรวจสอบ Environment Variables
2. ดู logs ใน Railway Dashboard
3. ตรวจสอบ Discord Bot Token

### **Deploy ไม่สำเร็จ**
1. ตรวจสอบ `railway.json`
2. ตรวจสอบ `requirements.txt`
3. ดู error logs

### **Bot ไม่ตอบสนอง**
1. ตรวจสอบ Discord permissions
2. ตรวจสอบ Channel ID
3. ตรวจสอบ Bot Token

## 💡 **Tips**

1. **ใช้ GitHub** สำหรับ version control
2. **ตั้งค่า Environment Variables** ให้ถูกต้อง
3. **ตรวจสอบ logs** เป็นประจำ
4. **ใช้ Railway CLI** สำหรับ advanced features

**Railway เป็นตัวเลือกที่ดีมากสำหรับ Minecraft Bot!** 🚂✨
