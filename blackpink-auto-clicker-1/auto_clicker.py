from discord.ext import commands
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox,
    QGroupBox, QHBoxLayout, QFileDialog, QCheckBox, QToolButton, QGraphicsOpacityEffect,
    QTimeEdit, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QRect, QEasingCurve, QPoint, QTime
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from win32com.client import Dispatch
import os
import sys
import asyncio
import random
import re
import threading
import time
import pyautogui as pag
import pyperclip
import psutil

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "config.txt")
VALID_USERNAME = "huydeptrai"
VALID_PASSWORD = "10022000"

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_ACTUAL_DISCORD_TOKEN")
if not DISCORD_BOT_TOKEN or DISCORD_BOT_TOKEN == "YOUR_ACTUAL_DISCORD_TOKEN":
    raise ValueError("⚠️ DISCORD_BOT_TOKEN missing! Set it before running.")

DISCORD_USER_ID = None

intents = discord.Intents.default()
intents.dm_messages = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

async def send_private_message(message):
    global DISCORD_USER_ID
    if DISCORD_USER_ID is None:
        print("⚠️ No Discord User ID set.")
        return
    user = await bot.fetch_user(int(DISCORD_USER_ID))
    if user:
        await user.send(message)
        print(f"📢 Sent DM: {message}")

@bot.command()
async def notify(ctx, id: str, *, message: str):
    try:
        user = await bot.fetch_user(int(id))
        if user:
            await user.send(message)
            await ctx.send(f"✅ Đã gửi tin nhắn tới user `{id}`.")
            return
    except Exception:
        pass
    try:
        channel = await bot.fetch_channel(int(id))
        if channel:
            await channel.send(message)
            await ctx.send(f"✅ Đã gửi tin nhắn tới channel `{id}`.")
            return
    except Exception:
        pass
    await ctx.send("❌ Không tìm thấy user hoặc channel với ID này.")

def send_discord(message, icon=None):
    icons_notify = ["🌸", "✨", "🎀", "💗", "🦄", "💎", "🩷", "🎉", "💖", "🌈", "🪐", "🦋", "🌟", "🍀", "🧸", "🫧", "🫶", "🧁", "🍰", "🍭", "🍬", "🧃", "🪄", "🩰", "🥰", "😻", "🦊", "🐼", "🐧", "🐣", "🦜", "🦩"]
    msg_lower = message.lower()
    if icon in ("🌸", None):
        icon = random.choice(icons_notify)
    if icon and not message.startswith(icon):
        message = f"{icon} {message}"
    asyncio.run_coroutine_threadsafe(send_private_message(message), bot.loop)

def start_discord_bot():
    asyncio.run(bot.start(DISCORD_BOT_TOKEN))

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🖤💗 BLACKPINK Login Panel")
        self.setGeometry(500, 300, 460, 420)
        self.setWindowIcon(QIcon(get_resource_path("images/lemon.ico")))

        layout = QVBoxLayout()
        title = QLabel("BLACKPINK AUTO CLICKER")
        title.setFont(QFont("Montserrat", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        group = QGroupBox("User Login")
        group_layout = QVBoxLayout()

        self.label_user = QLabel("Username:")
        group_layout.addWidget(self.label_user)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")
        group_layout.addWidget(self.username_input)

        self.label_pass = QLabel("Password:")
        group_layout.addWidget(self.label_pass)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        group_layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        group_layout.addWidget(self.login_btn)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username != VALID_USERNAME or password != VALID_PASSWORD:
            QMessageBox.warning(self, "Login Failed", "⚠️ Invalid username or password.")
            return

        global DISCORD_USER_ID
        DISCORD_USER_ID = self.username_input.text().strip()  # Example usage
        QMessageBox.information(self, "Login Successful", "✅ Welcome!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginApp()
    login_window.show()
    sys.exit(app.exec_())