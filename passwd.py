import sys
import random
from difflib import SequenceMatcher
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox,
    QMainWindow, QAction
)

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Şifre Oluşturucu")
        self.setGeometry(100, 100, 400, 300)

        # Menü çubuğu ve yardım menüsü
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("Yardım")

        help_action = QAction("Nasıl Kullanılır?", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        # Ana pencere widget'ı
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.kelime1_input = QLineEdit()
        self.kelime1_input.setPlaceholderText("1. Kelime")

        self.kelime2_input = QLineEdit()
        self.kelime2_input.setPlaceholderText("2. Kelime")

        self.kelime3_input = QLineEdit()
        self.kelime3_input.setPlaceholderText("3. Kelime")

        self.sayi_input = QLineEdit()
        self.sayi_input.setPlaceholderText("3-4 haneli sayı")

        self.generate_button = QPushButton("Şifre Oluştur")
        self.generate_button.clicked.connect(self.generate_password)

        self.copy_button = QPushButton("Kopyala")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_password)

        self.result_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.kelime1_input)
        layout.addWidget(self.kelime2_input)
        layout.addWidget(self.kelime3_input)
        layout.addWidget(self.sayi_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.copy_button)

        central_widget.setLayout(layout)

    def generate_password(self):
        kelime1 = self.kelime1_input.text().strip()[:4]
        kelime2 = self.kelime2_input.text().strip()[:4]
        kelime3 = self.kelime3_input.text().strip()[:4]
        sayi = self.sayi_input.text().strip()

        if not sayi.isdigit() or not (3 <= len(sayi) <= 4):
            QMessageBox.warning(self, "Hatalı Giriş", "Lütfen 3-4 haneli bir sayı girin.")
            return

        sayi = sayi[:4]
        özelkarakter = random.choice("!@#$%&*")
        components = [
            kelime1.capitalize(),
            kelime2.upper(),
            kelime3.lower(),
            sayi,
            özelkarakter
        ]
        random.shuffle(components)
        password = ''.join(components)
        self.password = password

        # Sızdırılmış kontrolü
        if self.is_similar_to_leaked(password):
            QMessageBox.warning(self, "Sızdırılmış Şifre", "Bu şifre sızdırılmış olabilir! Sana yeni bir öneri şifre verdik.")
            öneri = self.generate_suggestion()
            self.password = öneri
            self.result_label.setText(f"🔐 Önerilen Şifre: {öneri}")
        else:
            self.result_label.setText(f"🔐 Oluşturulan Şifre: {password}")

        self.copy_button.setEnabled(True)

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password)
        QMessageBox.information(self, "Kopyalandı", "Şifre panoya kopyalandı.")

    def is_similar_to_leaked(self, password, threshold=0.8):
        try:
            with open("10k-most-common", "r", encoding="utf-8") as file:
                leaked_passwords = file.readlines()
            for leaked in leaked_passwords:
                similarity = SequenceMatcher(None, password, leaked.strip()).ratio()
                if similarity >= threshold:
                    return True
        except FileNotFoundError:
            QMessageBox.warning(self, "Dosya Eksik", "şifre bulunamadı güvenli!!!")
        return False

    def generate_suggestion(self):
        # Basit öneri: rastgele güçlü parola
        karakterler = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"
        return ''.join(random.choices(karakterler, k=12))

    def show_help(self):
        help_text = (
            "Bu uygulama, 3 kelime ve 3-4 haneli bir sayı alarak rastgele bir şifre oluşturur.\n\n"
            "- Her kelimenin ilk 4 harfi kullanılır.\n"
            "- Sayı 3-4 haneli olmalıdır.\n"
            "- Özel karakter otomatik eklenir.\n"
            "- 'Şifre Oluştur' ile yeni bir şifre üretilir.\n"
            "- Şifre sızdırılmışsa uyarı alırsın ve güçlü bir öneri sunulur.\n"
            "- 'Kopyala' ile şifre panoya alınır."
        )
        QMessageBox.information(self, "Yardım", help_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec_())
