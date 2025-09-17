# ตัวอย่างการใช้งาน Minecraft Server Bot

## การเชื่อมต่อกับ Server ที่อยู่บน IP และ Port ที่กำหนด

### 1. การตั้งค่าผ่าน config.json

```json
{
  "minecraft": {
    "server_host": "26.97.108.203",
    "server_port": 5555,
    "server_name": "MyRemoteServer"
  }
}
```

### 2. การเชื่อมต่อผ่าน Discord Commands

```
!connect 26.97.108.203 5555
```

### 3. การตรวจสอบสถานะ

```
!status
!players
```

## ตัวอย่างการใช้งาน

### เชื่อมต่อกับ Server ระยะไกล
```
!connect 26.97.108.203 5555
```
Bot จะแสดง:
- ✅ Connected to Server
- จำนวนผู้เล่นออนไลน์
- เวอร์ชันของ Server

### ตรวจสอบสถานะ Server
```
!status
```
Bot จะแสดง:
- สถานะการเชื่อมต่อ
- จำนวนผู้เล่นออนไลน์
- เวลา uptime
- การใช้งาน RAM

### ดูรายชื่อผู้เล่น
```
!players
```
Bot จะแสดงรายชื่อผู้เล่นที่ออนไลน์

### ตัดการเชื่อมต่อ
```
!disconnect
```

## การตั้งค่า Radmin VPN

หากต้องการใช้ Radmin VPN เพื่อเชื่อมต่อกับ Server:

1. ติดตั้ง Radmin VPN
2. สร้างหรือเข้าร่วม Network
3. ตั้งค่าใน config.json:

```json
{
  "radmin_vpn": {
    "enabled": true,
    "network_name": "MinecraftServer",
    "auto_connect": true
  }
}
```

## การรัน Bot

```bash
py main.py
```

หรือใช้ไฟล์ batch:
```bash
start_bot.bat
```

## หมายเหตุ

- Bot สามารถเชื่อมต่อกับ Server ระยะไกลได้โดยไม่ต้องรัน Server เอง
- การเชื่อมต่อจะใช้ mcstatus library เพื่อตรวจสอบสถานะ
- Bot จะไม่สามารถควบคุม Server (start/stop) ได้หากเป็น Server ระยะไกล
- สามารถใช้ Radmin VPN เพื่อเชื่อมต่อกับ Network ที่มี Server อยู่
