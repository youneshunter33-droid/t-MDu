import re
import time
import random
import threading
from flask import Flask
from pyrogram import Client, filters, idle

# ====================================================
# سيرفر وهمي لإبقاء البوت شغالاً 24/7 على منصة Render
# ====================================================
app_web = Flask('')

@app_web.route('/')
def home():
    return "UserBot is Active 24/7!"

def run_web():
    app_web.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web, daemon=True).start()

# ====================================================
# البيانات الأساسية للاتصال
# ====================================================
API_ID = 33996959
API_HASH = "16775b0803fa9b9bef75507277b4af09"

STRING_SESSION = "BAIGwJ8AkjbUa5TJf8CLCTTDbNwCgAAKjjc82m1pCT8tjkikodXAsTOQg37mgEYLvTUNKs9w_PU7pLYnbGGc1EA7VUGcF2RlfSDcJ9ALIg1SZ1ohqXj2ylDQR3ifXeSRz4zdphT8GjthHPcGccAYvQgvzSIi-kdsMfwleQfvo7LWWlP4xTYpTEYUVbS_ORtLQQ9am_xetXCIu3gNQVmgySE1OG2LKGVZwXwasgPbNiICI00IWbu6ZweSjOh02YO6g4YAAr-Myi72--1k4DI50Arztc2-dI6ojPoKM_tpZ65rAPAY9RSbopej_Ljg9j0FCy1vnk-0VQeME7kHnDrDr4kUg-CSxAAAAAHZPrN1AA"

# 🔴 ضع يوزر القروب المستهدف لكلمة "راتب" هنا (مثال: "@mygroup")
TARGET_GROUP = "@mygroup"

TARGET_BOTS = [
    "@EE2Bbot",
    "@BR8bot",
    "@AnimeCloudAppbot",
    "@bobo_8bot",
    "@NA_BDBOTbot",
    "@K3Qbot",
    "@LD_Dbot"
]

app = Client(
    name="my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

lockdown_chats = set()

# ====================================================
# 1. التفاعل التلقائي بـ 🍓 على كل رسالة ترسلها أنت
# ====================================================
@app.on_message(filters.me)
def auto_react_my_messages(client, message):
    try:
        client.send_reaction(
            chat_id=message.chat.id, 
            message_id=message.id, 
            emoji="🍓"
        )
    except Exception as e:
        print(f"خطأ في التفاعل التلقائي: {e}")

# ====================================================
# 2. نظام سحب الأكواد (كود واحد عشوائي) بعد الـ 3 ساعات
# ====================================================
@app.on_message(filters.chat(TARGET_BOTS) & filters.incoming)
def process_code_message(client, message):
    text = message.text or message.caption or ""
    codes = re.findall(r'([A-Za-z0-9-_]{4,20})', text)
    if codes:
        ignored_words = ["عرض", "الاكواد", "كشط", "البوت", "مرحبا", "للحصول"]
        available_codes = [c for c in codes if c not in ignored_words]
        if available_codes:
            single_code = random.choice(available_codes)
            time.sleep(1.5)
            client.send_message(message.chat.id, f"كشط {single_code}")

def send_periodic_requests():
    interval = (3 * 3600) + (10 * 60)
    time.sleep(3)
    while True:
        for bot_username in TARGET_BOTS:
            try:
                app.send_message(bot_username, "عرض الاكواد")
                time.sleep(2)
            except Exception as e:
                print(f"خطأ أثناء طلب الأكواد: {e}")
        time.sleep(interval)

# ====================================================
# 3. إرسال كلمة (راتب) في القروب المخصص كل 15 دقيقة
# ====================================================
def send_ratib_to_single_group():
    time.sleep(10)
    while True:
        try:
            app.send_message(TARGET_GROUP, "راتب")
        except Exception as e:
            print(f"خطأ أثناء إرسال راتب: {e}")
        time.sleep(900)

# ====================================================
# 4. أوامر التحكم الخاصة بك داخل المجموعات (باي باي + بس)
# ====================================================
@app.on_message(filters.me & filters.text & filters.group)
def handle_my_commands(client, message):
    text = message.text.strip() if message.text else ""
    chat_id = message.chat.id
    
    if text == "باي باي" or text.startswith("باي باي"):
        try:
            message.edit(https://cdn.phototourl.com/free/2026-09-21-9d26771d-5821-4a34-b096-26df38336a44.jpg")
            for member in client.get_chat_members(chat_id):
                if member.user.id == client.me.id:
                    continue
                try:
                    client.ban_chat_member(chat_id, member.user.id)
                    time.sleep(0.3)
                except Exception:
                    pass
            message.edit("✅ تم تصفية القروب بنجاح!")
        except Exception as e:
            message.edit(f"❌ فشلت التصفية: {e}")

    elif text == "بس" or text.startswith("بس"):
        try:
            message.delete()
        except Exception:
            pass
        if chat_id in lockdown_chats:
            lockdown_chats.remove(chat_id)
        else:
            lockdown_chats.add(chat_id)

# ====================================================
# 5. حذف الرسائل الواردة في القروب المفعل فيه "بس"
# ====================================================
@app.on_message(filters.incoming & filters.group)
def auto_delete_incoming(client, message):
    if message.chat.id in lockdown_chats:
        try:
            message.delete()
        except Exception as e:
            print(f"خطأ في الحذف: {e}")

# ====================================================
# تشغيل البوت والمهام في الخلفية
# ====================================================
if __name__ == "__main__":
    app.start()
    print("✅ تم تشغيل البوت بنجاح سحابياً!")
    
    threading.Thread(target=send_periodic_requests, daemon=True).start()
    threading.Thread(target=send_ratib_to_single_group, daemon=True).start()
    
    idle()
