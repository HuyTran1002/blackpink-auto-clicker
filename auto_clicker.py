import sys
import os
import time
import threading
import keyboard
import pyautogui as pag
import pyscreeze
import discord
import asyncio
from discord import app_commands
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox,
    QGroupBox, QHBoxLayout, QFileDialog, QCheckBox, QToolButton, QGraphicsOpacityEffect,
    QTimeEdit, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QRect, QEasingCurve, QPoint, QTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
import random
import psutil
import subprocess
import pyperclip
from win32com.client import Dispatch
from dotenv import load_dotenv

# Thêm dòng này để chỉ rõ file .env ở cùng thư mục script
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.gitignore"))

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False

def get_config_path():
    from pathlib import Path
    return str(Path.home() / "Documents" / "config.txt")

CONFIG_FILE = get_config_path()
VALID_USERNAME = "huydeptrai"
VALID_PASSWORD = "10022000"

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    raise ValueError("⚠️ DISCORD_BOT_TOKEN missing! Set it before running.")

DISCORD_USER_ID = None

intents = discord.Intents.default()
intents.dm_messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")
    try:
        await tree.sync()
        print("✅ Slash commands synced globally.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

async def send_private_message(message):
    global DISCORD_USER_ID
    if DISCORD_USER_ID is None:
        print("⚠️ No Discord User ID set.")
        return
    user = await client.fetch_user(int(DISCORD_USER_ID))
    if user:
        await user.send(message)
        print(f"📢 Sent DM: {message}")

@tree.command(name="notify", description="Gửi tin nhắn tới user hoặc channel theo ID")
@app_commands.describe(id="ID người dùng hoặc channel", message="Nội dung tin nhắn")
async def notify(interaction: discord.Interaction, id: str, message: str):
    try:
        user = await client.fetch_user(int(id))
        if user:
            await user.send(message)
            await interaction.response.send_message(f"✅ Đã gửi tin nhắn tới user `{id}`.", ephemeral=True)
            return
    except Exception:
        pass
    try:
        channel = await client.fetch_channel(int(id))
        if channel:
            await channel.send(message)
            await interaction.response.send_message(f"✅ Đã gửi tin nhắn tới channel `{id}`.", ephemeral=True)
            return
    except Exception:
        pass
    await interaction.response.send_message("❌ Không tìm thấy user hoặc channel với ID này.", ephemeral=True)

def send_discord(message, icon=None):
    icons_notify = [
        "🌸", "✨", "🎀", "💗", "🦄", "💎", "🩷", "🎉", "💖", "🌈", "🪐", "🦋", "🌟", "🍀", "🧸", "🫧", "🫶", "🧁", "🍰", "🍭", "🍬", "🧃", "🪄", "🩰", "🥰", "😻", "🦊", "🐼", "🐧", "🐣", "🦜", "🦩"
    ]
    icons_warning = [
        "⚠️", "🚦", "😵‍💫", "😥", "😢", "😓", "😿", "🥲", "🥺", "🫠", "🛑", "🚨", "❗", "❕", "💢", "😨", "😱", "🧯", "🆘", "🔔"
    ]
    icons_success = [
        "🎉", "✅", "🥳", "😻", "💯", "🙌", "🌟", "🏆", "🥇", "🎊", "🎆", "🕺", "💃", "🫶", "🦄", "💝", "💐", "🍾", "🥂", "🎈", "🪅"
    ]
    icons_stop = [
        "🛑", "🚨", "❌", "😡", "😤", "💥", "⛔", "🚫", "🔴", "🧨", "🥵", "😠", "🛌"
    ]
    icons_click = [
        "🖱️", "🩷", "💗", "🦄", "✨", "🫰", "👆", "👇", "👉", "👈", "🖲️", "🫳", "🫴", "🖐️", "🤏"
    ]
    icons_time = [
        "⏰", "🕒", "🕰️", "⏳", "⌛", "🕞", "🕦", "🕗"
    ]

    msg_lower = message.lower()
    # Chọn icon phù hợp nội dung hoặc random nếu không xác định được
    if icon in ("🌸", None):
        icon = random.choice(icons_notify)
    elif icon == "🚦" or "không nhận được số" in msg_lower or "số thứ tự" in msg_lower:
        icon = random.choice(icons_warning)
    elif icon == "🎉" or "coming to chanh city" in msg_lower or "welcome" in msg_lower or "đã mở lại app" in msg_lower or "đã đặt hẹn giờ" in msg_lower or "bắt đầu auto clicker" in msg_lower:
        icon = random.choice(icons_success)
    elif icon == "🛑" or icon == "🚨" or "stopped" in msg_lower or "closing" in msg_lower or "dừng" in msg_lower or "tắt" in msg_lower or "huỷ" in msg_lower:
        icon = random.choice(icons_stop)
    elif icon == "🖱️" or "go to chanh city" in msg_lower or "auto timer" in msg_lower:
        icon = random.choice(icons_click)
    elif icon == "⏰" or "timeout" in msg_lower or "hẹn giờ" in msg_lower:
        icon = random.choice(icons_time)
    else:
        icon = random.choice(icons_notify)

    # Đảm bảo icon ở đầu message
    if icon and not message.startswith(icon):
        message = f"{icon} {message}"
    elif not icon:
        if not message.startswith(tuple(icons_notify + icons_warning + icons_success + icons_stop + icons_click + icons_time)):
            message = f"{random.choice(icons_notify)} {message}"
    asyncio.run_coroutine_threadsafe(send_private_message(message), client.loop)

def start_discord_bot():
    client.run(DISCORD_BOT_TOKEN)

class EnterCheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enter_callback = None

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.enter_callback:
                self.enter_callback()
        else:
            super().keyPressEvent(event)

class PasswordLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eye_btn = None

    def set_eye_btn(self, btn):
        self.eye_btn = btn

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.eye_btn:
            self.eye_btn.move(self.rect().right() - 24, (self.rect().height() - 20) // 2)

class LoginApp(QWidget):
    def toggle_password_visibility(self):
        eye_icon = QIcon(get_resource_path("images/eye.png")) if os.path.exists(get_resource_path("images/eye.png")) else (
            QIcon.fromTheme("view-password") or QIcon.fromTheme("eye") or self.style().standardIcon(self.style().SP_DialogYesButton)
        )
        eye_off_icon = QIcon(get_resource_path("images/eye-off.png")) if os.path.exists(get_resource_path("images/eye-off.png")) else (
            QIcon.fromTheme("view-hidden") or QIcon.fromTheme("eye-closed") or self.style().standardIcon(self.style().SP_DialogNoButton)
        )
        if self.toggle_pass_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_pass_btn.setIcon(eye_off_icon)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_pass_btn.setIcon(eye_icon)
            
    def __init__(self):
        super().__init__()
        self.exe_path = ""
        self.initUI()
        self.load_saved_credentials()

    def initUI(self):
        self.setWindowTitle("🖤💗 BLACKPINK Login Panel")
        self.setGeometry(500, 300, 460, 420)
        self.setWindowIcon(QIcon(get_resource_path("images/lemon.ico")))

        bg_path = get_resource_path("images/blackpink_bg.jpg")
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()

        self.old_resizeEvent = self.resizeEvent

        def resizeEvent(event):
            self.bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            if hasattr(self, 'old_resizeEvent'):
                self.old_resizeEvent(event)
        self.resizeEvent = resizeEvent

        self.setStyleSheet("""
        QWidget {
            background: transparent;
            color: #ffe4fa;
            font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
            font-size: 17px;
        }
        QLabel {
            font-size: 20px;
            color: #fff;
            font-weight: bold;
            letter-spacing: 1.5px;
            text-shadow: 2px 2px 8px #ff69b4;
        }
        QGroupBox {
            background: rgba(32,18,37,0.82);
            border: 2.5px solid #ff69b4;
            border-radius: 22px;
            margin-top: 18px;
            padding: 22px;
            font-size: 21px;
            font-weight: bold;
            color: #ff69b4;
            box-shadow: 0 6px 24px #ff69b433;
        }
        QLineEdit, QPushButton, QTimeEdit {
            background: rgba(42,24,51,0.85);
            border: 2.5px solid #ff69b4;
            border-radius: 16px;
            color: #ffe4fa;
            font-size: 17px;
            font-weight: bold;
            padding: 12px 16px;
        }
        QLineEdit:focus, QPushButton:focus, QTimeEdit:focus {
            border: 2.5px solid #fff;
            outline: none;
            background: rgba(42,24,51,1);
            color: #ffe4fa;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff69b4, stop:1 #18141c);
            color: #fff;
            border-radius: 18px;
            font-size: 19px;
            margin-top: 14px;
            letter-spacing: 2px;
            box-shadow: 0 2px 12px #ff69b488;
            transition: background 0.3s, color 0.3s;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #18141c, stop:1 #ff69b4);
            color: #ff69b4;
            border: 2.5px solid #fff;
        }
        """)

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

        self.label_chat_id = QLabel("Discord User ID:")
        group_layout.addWidget(self.label_chat_id)
        self.chat_id_input = QLineEdit(self)
        self.chat_id_input.setPlaceholderText("Enter your Discord User ID")
        group_layout.addWidget(self.chat_id_input)

        self.label_pass = QLabel("Password:")
        group_layout.addWidget(self.label_pass)
        self.password_input = PasswordLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        self.toggle_pass_btn = QToolButton(self.password_input)
        eye_icon = QIcon(get_resource_path("images/eye.png")) if os.path.exists(get_resource_path("images/eye.png")) else (
            QIcon.fromTheme("view-password") or QIcon.fromTheme("eye") or self.style().standardIcon(self.style().SP_DialogYesButton)
        )
        eye_off_icon = QIcon(get_resource_path("images/eye-off.png")) if os.path.exists(get_resource_path("images/eye-off.png")) else (
            QIcon.fromTheme("view-hidden") or QIcon.fromTheme("eye-closed") or self.style().standardIcon(self.style().SP_DialogNoButton)
        )
        self.toggle_pass_btn.setIcon(eye_icon)
        self.toggle_pass_btn.setCheckable(True)
        self.toggle_pass_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_pass_btn.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        self.toggle_pass_btn.setIconSize(QSize(20, 20))
        self.toggle_pass_btn.clicked.connect(self.toggle_password_visibility)
        self.password_input.setTextMargins(0, 0, 28, 0)
        self.toggle_pass_btn.move(self.password_input.rect().right() - 24, (self.password_input.rect().height() - 20) // 2)
        self.toggle_pass_btn.resize(20, 20)
        self.password_input.set_eye_btn(self.toggle_pass_btn)

        def update_eye_pos():
            self.toggle_pass_btn.move(self.password_input.rect().right() - 24, (self.password_input.rect().height() - 20) // 2)
        self.password_input.textChanged.connect(update_eye_pos)

        group_layout.addWidget(self.password_input)

        self.remember_pass_checkbox = EnterCheckBox("Remember password")
        group_layout.addWidget(self.remember_pass_checkbox)

        self.label_exe = QLabel("App (.exe) path:")
        group_layout.addWidget(self.label_exe)
        exe_layout = QHBoxLayout()
        self.exe_input = QLineEdit(self)
        self.exe_input.setPlaceholderText("Select .exe file to auto open")
        exe_layout.addWidget(self.exe_input)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_exe)
        exe_layout.addWidget(self.browse_btn)
        group_layout.addLayout(exe_layout)

        self.login_btn = QPushButton("Login")
        self.login_btn.setIcon(QIcon.fromTheme("dialog-ok"))
        self.login_btn.clicked.connect(self.handle_login)
        group_layout.addWidget(self.login_btn)
        self.login_btn.setDefault(True)

        self.startup_checkbox = QCheckBox("Khởi động cùng Windows")
        self.startup_checkbox.setChecked(True)  # Luôn tick mặc định
        group_layout.addWidget(self.startup_checkbox)

        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        self.setLayout(layout)

        self.username_input.returnPressed.connect(self.handle_login)
        self.chat_id_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        self.exe_input.returnPressed.connect(self.handle_login)

        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.remember_pass_checkbox.enter_callback = self.handle_login

        self.fade_in()

    def fade_in(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()
        self._fade_anim = anim

    def browse_exe(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .exe file", "", "Executable Files (*.exe)")
        if file_path:
            self.exe_input.setText(file_path)
            username = self.username_input.text().strip()
            user_id = self.chat_id_input.text().strip()
            if username and user_id:
                with open(CONFIG_FILE, "w") as file:
                    file.write(f"{username}\n{user_id}\n\n{file_path}")
        self.password_input.setFocus()

    def load_saved_credentials(self):
        global DISCORD_USER_ID
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                lines = file.readlines()
                if len(lines) >= 4:
                    self.username_input.setText(lines[0].strip())
                    self.chat_id_input.setText(lines[1].strip())
                    self.password_input.setText(lines[2].strip())
                    self.exe_input.setText(lines[3].strip())
                    DISCORD_USER_ID = lines[1].strip()
                    if lines[2].strip():
                        self.remember_pass_checkbox.setChecked(True)
                elif len(lines) >= 3:
                    self.username_input.setText(lines[0].strip())
                    self.chat_id_input.setText(lines[1].strip())
                    self.exe_input.setText(lines[2].strip())
                    DISCORD_USER_ID = lines[1].strip()

    def handle_login(self):
        global DISCORD_USER_ID
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        user_id = self.chat_id_input.text().strip()
        exe_path = self.exe_input.text().strip()
        remember_pass = self.remember_pass_checkbox.isChecked()
        startup_checked = self.startup_checkbox.isChecked()  # <-- lấy trạng thái checkbox

        try:
            if username != VALID_USERNAME or password != VALID_PASSWORD:
                self.shake_widget(self)
                return

            if not user_id:
                QMessageBox.warning(self, "Login Failed", "⚠️ Please enter a Discord User ID.")
                return

            if not exe_path or not os.path.isfile(exe_path):
                QMessageBox.warning(self, "Login Failed", "⚠️ Please select a valid .exe file.")
                return

            DISCORD_USER_ID = user_id
            with open(CONFIG_FILE, "w") as file:
                file.write(f"{username}\n{user_id}\n{password if remember_pass else ''}\n{exe_path}\n{int(startup_checked)}")

            # Xử lý khởi động cùng Windows
            if startup_checked:
                add_to_startup()
            else:
                remove_from_startup()

            self.welcome_box = QMessageBox(self)
            self.welcome_box.setWindowTitle("Login Successful")
            self.welcome_box.setText(f"✅ Welcome {username}!\nUser ID: {user_id}")
            self.welcome_box.setIcon(QMessageBox.Information)
            self.welcome_box.setStandardButtons(QMessageBox.NoButton)
            self.welcome_box.show()
            QApplication.processEvents()

            def after_welcome():
                self.welcome_box.accept()
                self.hide()
                self.auto_clicker = AutoClickerApp(exe_path=exe_path)
                self.auto_clicker.show()
                try:
                    subprocess.Popen(exe_path)
                except Exception as e:
                    QMessageBox.warning(self, "Warning", f"Không thể mở app ngoài: {e}")
                del self.welcome_box

            QTimer.singleShot(2000, after_welcome)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"⚠️ Login failed due to an error:\n{str(e)}")

    def shake_widget(self, widget):
        animation = QPropertyAnimation(widget, b"pos")
        pos = widget.pos()
        animation.setDuration(300)
        animation.setKeyValueAt(0, pos)
        animation.setKeyValueAt(0.2, pos + QPoint(-10, 0))
        animation.setKeyValueAt(0.4, pos + QPoint(10, 0))
        animation.setKeyValueAt(0.6, pos + QPoint(-10, 0))
        animation.setKeyValueAt(0.8, pos + QPoint(10, 0))
        animation.setKeyValueAt(1, pos)
        animation.start()
        self._shake_anim = animation

class RippleEffect(QLabel):
    def __init__(self, parent, x, y, color=None):
        super().__init__(parent)
        if color is None:
            color = "qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 #ffe4faAA, stop:1 #ff69b400)"
        self.setStyleSheet(f"background: {color}; border-radius: 100px;")
        self.setGeometry(x-60, y-60, 120, 120)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.show()
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(600)
        self.anim.setStartValue(QRect(x, y, 0, 0))
        self.anim.setEndValue(QRect(x-60, y-60, 120, 120))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(600)
        self.fade.setStartValue(0.6)
        self.fade.setEndValue(0)
        self.fade.start()

class AutoClickerApp(QWidget):
    set_timer_signal = pyqtSignal(int, int, int)
    cancel_timer_signal = pyqtSignal()
    set_status_signal = pyqtSignal(str, str, bool, int, object)
    minimize_signal = pyqtSignal()
    start_clicker_signal = pyqtSignal(str)  # <-- thêm dòng này

    def __init__(self, exe_path=""):
        super().__init__()
        set_auto_clicker_instance(self)
        self.exe_path = exe_path
        self.minimize_signal.connect(self.showMinimized)
        self.start_clicker_signal.connect(self.start_clicker)  # <-- thêm dòng này
        self.running = False
        self.detecting = True
        self.timeout_seconds = 0
        self.timer_set = False
        self.auto_timer = None
        self.last_timer_status = None
        self.xephang_detected = False
        self.initUI()
        set_auto_clicker_instance(self)
        self.set_timer_signal.connect(self.set_auto_timer)
        self.set_status_signal.connect(self.set_status)
        self.cancel_timer_signal.connect(self.cancel_auto_timer)

        # Sửa icon tray dùng get_resource_path
        self.tray_icon = QSystemTrayIcon(QIcon(get_resource_path("images/lemon.ico")), self)
        tray_menu = QMenu()
        restore_action = QAction("Hiện cửa sổ", self)
        quit_action = QAction("Thoát", self)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        restore_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setToolTip("BLACKPINK Auto Clicker")
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_activated)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "BLACKPINK Auto Clicker",
            "Ứng dụng đang chạy ngầm ở khay hệ thống.",
            QSystemTrayIcon.Information,
            2000
        )

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()

    def initUI(self):
        self.setWindowTitle("🖤💗 BLACKPINK Auto Clicker")
        self.setWindowIcon(QIcon(get_resource_path("images/lemon.ico")))
        self.resize(460, 420)  # Đặt kích thước trước

        bg_path = get_resource_path("images/blackpink_bg.jpg")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(bg_path).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

        self.setStyleSheet("""
        QWidget {
            background: transparent;
            color: #ffe4fa;
            font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
            font-size: 17px;
        }
        QLabel {
            font-size: 20px;
            color: #fff;
            font-weight: bold;
            letter-spacing: 1.5px;
            text-shadow: 2px 2px 8px #ff69b4;
        }
        QGroupBox {
            background: rgba(32,18,37,0.82);
            border: 2.5px solid #ff69b4;
            border-radius: 22px;
            margin-top: 18px;
            padding: 22px;
            font-size: 21px;
            font-weight: bold;
            color: #ff69b4;
            box-shadow: 0 6px 24px #ff69b433;
        }
        QLineEdit, QPushButton, QTimeEdit {
            background: rgba(42,24,51,0.85);
            border: 2.5px solid #ff69b4;
            border-radius: 16px;
            color: #ffe4fa;
            font-size: 17px;
            font-weight: bold;
            padding: 12px 16px;
        }
        QLineEdit:focus, QPushButton:focus, QTimeEdit:focus {
            border: 2.5px solid #fff;
            outline: none;
            background: rgba(42,24,51,1);
            color: #ffe4fa;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff69b4, stop:1 #18141c);
            color: #fff;
            border-radius: 18px;
            font-size: 19px;
            margin-top: 14px;
            letter-spacing: 2px;
            box-shadow: 0 2px 12px #ff69b488;
            transition: background 0.3s, color 0.3s;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #18141c, stop:1 #ff69b4);
            color: #ff69b4;
            border: 2.5px solid #fff;
        }
        """)

        layout = QVBoxLayout()
        title = QLabel("BLACKPINK AUTO CLICKER")
        title.setFont(QFont("Montserrat", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Montserrat", 18, QFont.Bold))
        self.clock_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.clock_label)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        timer_group = QGroupBox("Hẹn giờ tự động chạy")
        timer_vlayout = QVBoxLayout()

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setFixedWidth(180)
        self.time_edit.setAlignment(Qt.AlignCenter)
        timer_vlayout.addWidget(self.time_edit, alignment=Qt.AlignHCenter)

        btns_hlayout = QHBoxLayout()
        self.set_timer_btn = QPushButton("Set")
        self.set_timer_btn.setFixedWidth(110)
        self.set_timer_btn.clicked.connect(self.set_auto_timer)
        btns_hlayout.addWidget(self.set_timer_btn)

        self.cancel_timer_btn = QPushButton("Cancel")
        self.cancel_timer_btn.setFixedWidth(110)
        self.cancel_timer_btn.clicked.connect(lambda: self.cancel_auto_timer(notify=True))
        btns_hlayout.addWidget(self.cancel_timer_btn)

        timer_vlayout.addLayout(btns_hlayout)
        timer_group.setLayout(timer_vlayout)
        layout.addWidget(timer_group)

        group = QGroupBox("Main Controls")
        group_layout = QVBoxLayout()

        self.label_status = QLabel("Status: <b><span style='color:#f39c12;'>Stopped</span></b>")
        self.label_status.setFont(QFont("Montserrat", 15))
        group_layout.addWidget(self.label_status)

        self.label_timeout = QLabel("Set Timeout (seconds):")
        group_layout.addWidget(self.label_timeout)
        self.timeout_input = QLineEdit(self)
        self.timeout_input.setText("0")
        self.timeout_input.setPlaceholderText("Nhập số giây")
        self.timeout_input.setAlignment(Qt.AlignCenter)
        self.timeout_input.setStyleSheet("QLineEdit::placeholder { color: #b197b6; font-style: italic; }")
        group_layout.addWidget(self.timeout_input)

        self.label_countdown = QLabel("Timeout countdown: -")
        self.label_countdown.setFont(QFont("Montserrat", 14, QFont.Bold))
        self.label_countdown.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(self.label_countdown)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start (F1)")
        self.start_btn.setIcon(QIcon.fromTheme("media-playback-start"))
        self.start_btn.clicked.connect(self.start_clicker)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop (F2)")
        self.stop_btn.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_btn.clicked.connect(self.stop_clicker)
        btn_layout.addWidget(self.stop_btn)

        self.exit_btn = QPushButton("Exit (Esc)")
        self.exit_btn.setIcon(QIcon.fromTheme("application-exit"))
        self.exit_btn.clicked.connect(self.close_app)
        btn_layout.addWidget(self.exit_btn)

        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        self.setLayout(layout)

        keyboard.add_hotkey("f1", self.start_clicker)
        keyboard.add_hotkey("f2", self.stop_clicker)
        keyboard.add_hotkey("esc", self.close_app)

        self.start_btn.clicked.connect(lambda e=None: self.show_ripple(self.start_btn))
        self.stop_btn.clicked.connect(lambda e=None: self.show_ripple(self.stop_btn))
        self.exit_btn.clicked.connect(lambda e=None: self.show_ripple(self.exit_btn))
        self.show()

    def showEvent(self, event):
        super().showEvent(event)
        # Đặt vị trí sát phải và sát trên, không bị lẹm
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_width = self.width()
        window_height = self.height()
        x = screen_geometry.right() - window_width
        y = screen_geometry.top()
        # Đảm bảo không bị lẹm ra ngoài
        if x < screen_geometry.left():
            x = screen_geometry.left()
        if y < screen_geometry.top():
            y = screen_geometry.top()
        self.move(x, y)

    def set_status(self, text, color="#44bd32", temporary=False, duration=3000, restore_to=None):
        self.label_status.setText(f"Status: <b><span style='color:{color};'>{text}</span></b>")
        if hasattr(self, '_status_timer') and self._status_timer:
            self._status_timer.stop()
        if temporary:
            self._status_timer = QTimer(self)
            self._status_timer.setSingleShot(True)
            def restore_status():
                if restore_to == "timer" and self.last_timer_status:
                    self.set_status(self.last_timer_status, "#f39c12", temporary=False)
                elif self.running:
                    self.set_status("Running...", "#00b894", temporary=False)
                else:
                    self.set_status("Stopped", "#e17055", temporary=False)
            self._status_timer.timeout.connect(restore_status)
            self._status_timer.start(duration)

    def set_countdown(self, value):
        if value >= 0:
            color = "#ff69b4" if value <= 3 else "#ffe4fa"
            self.label_countdown.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
            self.label_countdown.setText(f"Timeout countdown: {int(value)}s")
        else:
            self.label_countdown.setText("Timeout countdown: -")

    def update_clock(self):
        now = QTime.currentTime()
        self.clock_label.setText(f"🕒 {now.toString('HH:mm:ss')}")

    def set_auto_timer(self, h=None, m=None, s=None):
        if self.running:
            self.set_status("Đang chạy rồi ní", "#e17055", temporary=True, restore_to=None)
            send_discord("Auto clicker đang chạy, không thể đặt hẹn giờ mới!", icon="⚠️")
            return
        if self.auto_timer and self.auto_timer.isActive():
            self.set_status("Đã có hẹn giờ rồi ní!", "#e17055", temporary=True, restore_to="timer")
            send_discord("Đã có lệnh hẹn giờ, hãy huỷ trước khi đặt mới!", icon="⚠️")
            return
        if h is not None and m is not None and s is not None:
            target_time = QTime(h, m, s)
            self.time_edit.setTime(target_time)
        else:
            target_time = self.time_edit.time()
        now = QTime.currentTime()
        secs = now.secsTo(target_time)
        if secs < 0:
            secs += 24 * 3600
        if self.auto_timer:
            self.auto_timer.stop()
        self.auto_timer = QTimer(self)
        self.auto_timer.setSingleShot(True)
        self.auto_timer.timeout.connect(self.auto_timer_triggered)
        self.auto_timer.start(secs * 1000)
        timer_status = f"Auto run timer set for {target_time.toString('HH:mm:ss')}"
        self.last_timer_status = timer_status
        self.set_status(timer_status, "#f39c12")
        send_discord(f"Đã đặt hẹn giờ tự động: {target_time.toString('HH:mm:ss')}", icon="⏰")

    def cancel_auto_timer(self, notify=True):
        if self.auto_timer and self.auto_timer.isActive():
            self.auto_timer.stop()
            self.auto_timer = None
            self.set_status("Auto run timer canceled", "#e17055", temporary=True, restore_to=None)
            if notify:
                send_discord("Đã huỷ hẹn giờ tự động!", icon="🚫")
            return True
        else:
            if notify:
                self.set_status("Không có lệnh hẹn giờ để huỷ!", "#e17055", temporary=True, restore_to=None)
                send_discord("Không có lệnh hẹn giờ nào để huỷ!", icon="⚠️")
            return False

    def auto_timer_triggered(self):
        self.running = False
        self.set_status("Running...", "#00b894")
        self.set_countdown(-1)
        self.auto_timer = None
        self.start_clicker(source="timer")

    def start_clicker(self, source="manual"):
        self.cancel_auto_timer(notify=False)
        if self.running:
            self.set_status("Đã chạy rồi ní!", "#e17055", temporary=True, restore_to=None)
            send_discord("Auto clicker đã chạy rồi, không thể start tiếp!", icon="⚠️")
            return
        self.show()      # <-- Đảm bảo dòng này có
        self.raise_()    # <-- Thêm dòng này để cửa sổ nổi lên trên
        self.activateWindow()  # <-- Thêm dòng này để lấy focus
        try:
            timeout_val = int(self.timeout_input.text().strip())
        except ValueError:
            timeout_val = 0
        if timeout_val < 0:
            timeout_val = 0
            self.timeout_input.setText("0")
        self.timeout_seconds = max(0, timeout_val - 2)
        self._do_start_clicker(source)

    def _do_start_clicker(self, source):
        self.running = True
        self.detecting = True
        self.set_status("Running...", "#00b894")
        self.set_countdown(-1)
        if source == "timer":
            send_discord("Go to Chanh City! (Auto Timer)", icon="🖱️")
        else:
            send_discord("Go to Chanh City!", icon="🖱️")

        try:
            self.timeout_seconds = int(self.timeout_input.text().strip())
        except ValueError:
            self.timeout_seconds = 0

        self.timeout_seconds = max(0, self.timeout_seconds - 2)

        threading.Thread(target=self.auto_click, daemon=True).start()
        threading.Thread(target=self.detect_stop_image, daemon=True).start()
        threading.Thread(target=self.detect_xephang_image, daemon=True).start()

    def detect_xephang_image(self):
        while self.detecting:
            if pag.locateCenterOnScreen(get_resource_path("images/xephang.png"), grayscale=True, confidence=0.85):
                if not self.xephang_detected:
                    self.xephang_detected = True
                    send_discord("Coming to Chanh City!", icon="🎉")
                self.running = False
                self.set_status("Stopped", "#e17055")
                self.set_countdown(-1)
                return
            time.sleep(0.5)

    def stop_clicker(self):
        # Luôn dừng timer hẹn giờ
        timer_was_active = False
        if self.auto_timer and self.auto_timer.isActive():
            self.cancel_auto_timer(notify=False)
            timer_was_active = True

        if not self.running and not timer_was_active:
            self.set_status("Fully stopped", "#e17055")
            send_discord("Auto clicker đã dừng hoàn toàn!", icon="🛑")
            self.set_countdown(-1)
            self.showNormal()
            return

        self.running = False
        self.detecting = False
        self.set_status("Fully stopped", "#e17055")
        self.set_countdown(-1)
        send_discord("Auto Clicker Stopped!!", icon="🛑")
        self.showNormal()

    def close_app(self):
        send_discord("Closing application now!!", icon="🚨")
        self.running = False
        self.detecting = False
        self.set_status("Exiting...", "#636e72")
        self.set_countdown(-1)
        # Xóa file number.txt khi tắt app
        number_file = os.path.join(os.path.expanduser("~"), "Documents", "number.txt")
        try:
            if os.path.exists(number_file):
                os.remove(number_file)
        except Exception as e:
            print(f"Không thể xóa number.txt: {e}")
        time.sleep(1.2)
        self.close()
        QApplication.quit()

    def auto_click(self):
        import re
        last_queue_number = None
        first_number_sent = False

        while self.running:
            # Nếu đã vào được thành phố thì dừng
            if pag.locateCenterOnScreen(get_resource_path("images/xephang.png"), grayscale=True, confidence=0.85):
                if not self.xephang_detected:
                    self.xephang_detected = True
                    send_discord("Coming to Chanh City!", icon="🎉")
                self.running = False
                self.set_status("Stopped", "#e17055")
                self.set_countdown(-1)
                return

            # Ưu tiên kiểm tra nút đóng trước
            loc_dong = pag.locateCenterOnScreen(get_resource_path("images/dong.png"), grayscale=True, confidence=0.85)
            if loc_dong:
                t_start = time.perf_counter()
                queue_number = double_click_and_copy_number()
                if queue_number and queue_number != last_queue_number:
                    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
                    if not first_number_sent:
                        send_discord(f"Số thứ tự của bạn là: {queue_number} ({now_str[-8:]})", icon="🚦")
                        first_number_sent = True
                    else:
                        send_discord(f"Số thứ tự của bạn là: {queue_number}", icon="🚦")
                    last_queue_number = queue_number

                pag.click(loc_dong)  # Bấm đóng
                t_end = time.perf_counter()
                elapsed = t_end - t_start

                try:
                    timeout_val = int(self.timeout_input.text().strip())
                except ValueError:
                    timeout_val = 0

                timeout_val = max(0, timeout_val - elapsed)
                if timeout_val > 0:
                    if timeout_val < 1:
                        time.sleep(timeout_val)
                    else:
                        for i in range(int(timeout_val), 0, -1):
                            if not self.running:
                                self.set_countdown(-1)
                                return
                            self.set_countdown(i)
                            time.sleep(1)
                        self.set_countdown(-1)
                        frac = timeout_val - int(timeout_val)
                        if frac > 0 and self.running:
                            time.sleep(frac)
                else:
                    self.set_countdown(-1)
                continue

            # Nếu không có nút đóng, kiểm tra nút mở
            loc_mo = pag.locateCenterOnScreen(get_resource_path("images/mo.png"), grayscale=True, confidence=0.85)
            if loc_mo:
                pag.click(loc_mo)
                time.sleep(0.01)
                continue

            # Nếu không có gì, sleep ngắn rồi lặp lại
            time.sleep(0.01)  # Giảm thời gian chờ

    def detect_stop_image(self):
        while self.detecting:
            if pag.locateCenterOnScreen(get_resource_path("images/stop.png"), grayscale=True, confidence=0.85):
                send_discord("Welcome to Chanh City!", icon="✅")
                time.sleep(2)
                self.close_app()
            time.sleep(0.5)

    def show_ripple(self, btn):
        cursor_pos = btn.mapFromGlobal(QCursor.pos())
        btn_pos = btn.mapTo(self, cursor_pos)
        RippleEffect(self, btn_pos.x(), btn_pos.y())

auto_clicker_instance = None

def set_auto_clicker_instance(instance):
    global auto_clicker_instance
    auto_clicker_instance = instance

# --- SINGLE INSTANCE CHECK (QLocalServer) ---
def is_running():
    socket = QLocalSocket()
    socket.connectToServer("BLACKPINK_AUTOCLICKER_SINGLE_INSTANCE")
    is_running = socket.waitForConnected(100)
    socket.close()
    return is_running

if is_running():
    # Đã có instance khác, thoát
    sys.exit(0)
else:
    server = QLocalServer()
    server.listen("BLACKPINK_AUTOCLICKER_SINGLE_INSTANCE")
# --- END SINGLE INSTANCE CHECK ---

# --- SLASH COMMANDS ---

@tree.command(name="start", description="Bắt đầu auto clicker")
async def start(interaction: discord.Interaction):
    if auto_clicker_instance:
        if auto_clicker_instance.running:
            auto_clicker_instance.set_status_signal.emit(
                "Đã chạy rồi ní", "#e17055", True, 3000, None
            )
            send_discord("Auto clicker đã chạy rồi, không thể start tiếp!", icon="⚠️")
            await interaction.response.send_message("⚠️ Auto clicker đã chạy rồi!", ephemeral=True)
        else:
            auto_clicker_instance.start_clicker_signal.emit("discord")
            await interaction.response.send_message("✅ Đã bắt đầu auto clicker!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="stop", description="Dừng auto clicker")
async def stop(interaction: discord.Interaction):
    if auto_clicker_instance:
        if not auto_clicker_instance.running:
            auto_clicker_instance.set_status_signal.emit(
                "Đã dừng rồi ní!", "#e17055", True, 3000, None
            )
            send_discord("Auto clicker đã dừng rồi, không thể stop tiếp!", icon="⚠️")
            await interaction.response.send_message("⚠️ Auto clicker đã dừng rồi!", ephemeral=True)
        else:
            auto_clicker_instance.stop_clicker()
            await interaction.response.send_message("🛑 Đã dừng auto clicker!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="settimeout", description="Đặt timeout (giây)")
@app_commands.describe(seconds="Số giây timeout")
async def settimeout(interaction: discord.Interaction, seconds: int):
    if auto_clicker_instance:
        if seconds < 0:
            seconds = 0
        auto_clicker_instance.timeout_input.setText(str(seconds))
        await interaction.response.send_message(f"⏱️ Timeout đã đặt thành {seconds} giây.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="settimer", description="Đặt hẹn giờ tự động (HH:MM:SS)")
@app_commands.describe(time_str="Thời gian định dạng HH:MM:SS")
async def settimer(interaction: discord.Interaction, time_str: str):
    if auto_clicker_instance:
        try:
            import re
            time_str = re.sub(r"[^\d:]", "", time_str.strip())
            h, m, s = map(int, time_str.split(":"))
            if auto_clicker_instance.auto_timer and auto_clicker_instance.auto_timer.isActive():
                auto_clicker_instance.set_status_signal.emit(
                    "Đã có hẹn giờ rồi ní!", "#e17055", True, 3000, "timer"
                )
                send_discord("Đã có lệnh hẹn giờ, hãy huỷ trước khi đặt mới!", icon="⚠️")
                await interaction.response.send_message("⚠️ Đã có lệnh hẹn giờ, hãy huỷ trước khi đặt mới!", ephemeral=True)
                return
            auto_clicker_instance.set_timer_signal.emit(h, m, s)
            await interaction.response.send_message(f"⏰ Đã đặt hẹn giờ tự động: {time_str}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Sai định dạng! Dùng HH:MM:SS\nChi tiết: {e}", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="cancel", description="Hủy hẹn giờ tự động")
async def cancel(interaction: discord.Interaction):
    if auto_clicker_instance:
        auto_clicker_instance.cancel_timer_signal.emit()
        await interaction.response.send_message("🚫 Đã huỷ hẹn giờ tự động!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="status", description="Xem trạng thái hiện tại")
async def status(interaction: discord.Interaction):
    if auto_clicker_instance:
        import re
        raw = auto_clicker_instance.label_status.text()
        clean = re.sub(r"<.*?>", "", raw)
        status_only = clean.split(":", 1)[-1].strip() if ":" in clean else clean.strip()
        await interaction.response.send_message(f"📋 Trạng thái: {status_only}", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="help", description="Hiện danh sách lệnh")
async def help_cmd(interaction: discord.Interaction):
    help_text = (
        "**BLACKPINK Auto Clicker Bot Slash Commands:**\n"
        "`/start` – Bắt đầu auto clicker\n"
        "`/stop` – Dừng auto clicker\n"
        "`/settimeout <giây>` – Đặt timeout (ví dụ: /settimeout 10)\n"
        "`/settimer <HH:MM:SS>` – Đặt hẹn giờ tự động (ví dụ: /settimer 12:34:56)\n"
        "`/cancel` – Hủy hẹn giờ tự động\n"
        "`/status` – Xem trạng thái hiện tại\n"
        "`/notify <id> <tin nhắn>` – Gửi tin nhắn riêng\n"
        "`/exit` – Tắt AutoClicker\n"
        "`/killapp` – Tắt app ngoài (.exe) đã chọn\n"
        "`/openapp` – Mở lại app ngoài (.exe) đã chọn\n"
        "`/help` – Hiện danh sách lệnh\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@tree.command(name="exit", description="Tắt AutoClicker")
async def exit_cmd(interaction: discord.Interaction):
    if auto_clicker_instance:
        await interaction.response.send_message("🔌 Đang tắt AutoClicker...", ephemeral=True)
        auto_clicker_instance.close_app()
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="killapp", description="Tắt app ngoài (.exe) đã chọn")
async def killapp(interaction: discord.Interaction):
    if auto_clicker_instance and hasattr(auto_clicker_instance, "exe_path"):
        exe_path = auto_clicker_instance.exe_path
        exe_name = os.path.basename(exe_path)
        killed = False
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and os.path.basename(proc.info['exe']).lower() == exe_name.lower():
                    proc.kill()
                    killed = True
            except Exception:
                continue
        if killed:
            await interaction.response.send_message(f"💀 Đã tắt app: `{exe_name}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ Không tìm thấy hoặc không thể tắt app: `{exe_name}`", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

@tree.command(name="openapp", description="Mở lại app ngoài (.exe) đã chọn")
async def openapp(interaction: discord.Interaction):
    if auto_clicker_instance and hasattr(auto_clicker_instance, "exe_path"):
        exe_path = auto_clicker_instance.exe_path
        if exe_path and os.path.isfile(exe_path):
            try:
                subprocess.Popen(exe_path)
                await interaction.response.send_message(f"🚀 Đã mở lại app: `{os.path.basename(exe_path)}`", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"❌ Không thể mở app: `{exe_path}`\nLỗi: {e}", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Đường dẫn file exe không hợp lệ.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Auto clicker chưa sẵn sàng.", ephemeral=True)

def remove_from_startup():
    startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    shortcut_path = os.path.join(startup_dir, "BLACKPINK Auto Clicker.lnk")
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)
        except Exception:
            pass

def add_to_startup():
    startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    # Chỉ tạo shortcut nếu đang chạy từ file exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
        shortcut_path = os.path.join(startup_dir, "BLACKPINK Auto Clicker.lnk")
        # Sửa lấy icon đúng khi chạy từ exe đóng gói
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "images", "lemon.ico")
        else:
            icon_path = os.path.join(os.path.dirname(exe_path), "images", "lemon.ico")
        if not os.path.exists(shortcut_path):
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            if os.path.exists(icon_path):
                shortcut.IconLocation = icon_path
            else:
                shortcut.IconLocation = exe_path
            shortcut.Arguments = "--minimized"
            shortcut.save()

# Thêm biến toàn cục để nhớ số chữ số
number_length = None

def double_click_and_copy_number():
    import re
    global number_length

    def try_get_number():
        time.sleep(0.01)  # Giảm thời gian chờ
        pag.hotkey('ctrl', 'c')
        time.sleep(0.01)
        copied = pyperclip.paste()
        match = re.search(r"\d{1,4}", copied)
        return match.group() if match else None

    def get_coord(length):
        if length == 2:
            return (1005, 730)
        elif length == 4:
            return (1015, 730)
        else:
            return (1009, 730)

    # Nếu chưa biết độ dài, đo lần đầu
    if number_length is None:
        pag.doubleClick(951, 730)
        number = try_get_number()
        if not number:
            return None
        number_length = len(number)

    coord = get_coord(number_length)
    fail_count = 0

    for _ in range(2):  # Chỉ thử lại tối đa 2 lần
        pag.doubleClick(*coord)
        number = try_get_number()
        if number:
            return number
        fail_count += 1

    # Nếu vẫn không lấy được, đo lại độ dài
    pag.doubleClick(951, 730)
    number = try_get_number()
    if number:
        number_length = len(number)
        coord = get_coord(number_length)
        pag.doubleClick(*coord)
        number = try_get_number()
        if number:
            return number
    number_length = None
    return None

if __name__ == "__main__":
    threading.Thread(target=start_discord_bot, daemon=True).start()
    app = QApplication(sys.argv)

    auto_login = False
    minimized = "--minimized" in sys.argv

    # Đọc config để kiểm tra tự động đăng nhập
    config_path = CONFIG_FILE
    auto_login_info = None
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            lines = [l.strip() for l in file.readlines()]
            if len(lines) >= 5:
                username, user_id, password, exe_path, startup_checked = lines[:5]
                if username and user_id and password and exe_path and os.path.isfile(exe_path):
                    auto_login_info = (username, user_id, password, exe_path)
                    auto_login = True

    if minimized and auto_login_info:
        # Gán lại DISCORD_USER_ID khi auto login
        DISCORD_USER_ID = auto_login_info[1]
        auto_clicker = AutoClickerApp(exe_path=auto_login_info[3])
        auto_clicker.hide()  # Ẩn luôn, chỉ hiện ở tray
        sys.exit(app.exec_())
    else:
        login_window = LoginApp()
        login_window.show()
        sys.exit(app.exec_())

