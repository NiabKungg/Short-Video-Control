# Short-Video-Control

โปรเจคนี้ช่วยให้ผู้ใช้สามารถควบคุมการเล่นวิดีโอสั้น (เช่น ข้าม, ย้อนกลับ, และถูกใจ) โดยใช้การเคลื่อนไหวของมือที่ตรวจจับผ่านเว็บแคม ระบบนี้ใช้ **Mediapipe** สำหรับการติดตามมือและ **PyAutoGUI** เพื่อจำลองการกดแป้นพิมพ์และการคลิกเมาส์ตามการจดจำท่าทาง

## ฟีเจอร์
- **ข้ามวิดีโอ:** ทำท่าทางที่นิ้วมือ 4 และ 8 เข้าใกล้กัน
- **ย้อนกลับ (Undo):** ทำท่าทางที่นิ้วมือ 12 และ 8 เข้าใกล้กัน
- **ถูกใจวิดีโอ:** ทำท่าทางที่นิ้วมือ 4 และ 8 ห่างกันเพื่อกระตุ้นให้คลิกเมาส์สองครั้ง

## ข้อกำหนด

เพื่อรันโปรเจคนี้ คุณจะต้องมี:

- Python 3.11
- OpenCV (`opencv-python`)
- Mediapipe (`mediapipe`)
- PyAutoGUI (`pyautogui`)
- Numpy (`numpy`)

## การตั้งค่าและการใช้งาน

1. คัดลอก repository:
   ```bash
   git clone https://github.com/NiabKungg/Short-Video-Control
   cd Short-Video-Control
   ```

2. ติดตั้งแพ็กเกจที่จำเป็น:
   ```bash
   pip install -r requirements.txt
   ```

3. ดาวน์โหลดโมเดลการตรวจจับมือ:
   ```bash
   wget -q https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
   ```
   ให้แน่ใจว่าคุณมีไฟล์ `hand_landmarker.task` ในไดเรกทอรีทำงานของคุณ
   

5. รันโปรแกรม:
   ```bash
   python main.py
   ```

6. ใช้เว็บแคมเพื่อควบคุมวิดีโอ:
   - **ข้าม:** กด 'ลง' เมื่อปลายนิ้ว 4 และ 8 เข้าใกล้กัน
   - **ย้อนกลับ:** กด 'ขึ้น' เมื่อปลายนิ้ว 12 และ 8 เข้าใกล้กัน
   - **ถูกใจ:** คลิกสองครั้งเมื่อปลายนิ้ว 4 และ 8 ห่างกัน

## โครงสร้างไฟล์

```
Short-Video-Control/
│
├── main.py               # สคริปต์หลักสำหรับรันแอปพลิเคชัน
├── hand_landmarker.task   # ไฟล์โมเดลการตรวจจับมือของ Mediapipe
└── requirements.txt       # รายการแพ็กเกจที่จำเป็น
```

## การสาธิต

![example](example.gif)
