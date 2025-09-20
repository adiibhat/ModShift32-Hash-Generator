import hashlib
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# --- HASHING ALGORITHM (same core logic) ---
def modshift32_hash(plaintext):
    """
    Custom hashing algorithm that produces a 32-character fixed-length hash.
    Uses character manipulation, modular arithmetic, and compression.
    """
    if not plaintext:
        plaintext = "empty_string"
    
    hash_value = 0
    prime = 31
    max_int = 2**32 - 1
    
    for i, char in enumerate(plaintext):
        ascii_val = ord(char)
        shifted_val = ascii_val << (i % 8)
        hash_value = (hash_value * prime + shifted_val) % max_int
        hash_value = (hash_value ^ (hash_value >> 16)) % max_int
    
    for _ in range(3):
        hash_value = hash_value ^ (hash_value << 13) % max_int
        hash_value = hash_value ^ (hash_value >> 7) % max_int
        hash_value = hash_value ^ (hash_value << 17) % max_int
    
    final_hash = ""
    for i in range(4):
        segment_hash = (hash_value + i * 0x9e3779b9) % max_int
        segment_hash = ((segment_hash ^ (segment_hash >> 16)) * 0x85ebca6b) % max_int
        segment_hash = ((segment_hash ^ (segment_hash >> 13)) * 0x2b2ae35) % max_int
        segment_hash = (segment_hash ^ (segment_hash >> 16)) % max_int
        final_hash += format(segment_hash, '08x')
    
    return final_hash[:32]


# --- MAIN WINDOW ---
class HashingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ModShift32 Hash Generator")
        self.setGeometry(300, 200, 700, 450)
        self.setFixedSize(700, 450)  # Optional: fixed size for simplicity

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("ModShift32 Hash Generator")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input section
        input_layout = QHBoxLayout()
        input_label = QLabel("Enter text:")
        input_label.setFont(QFont("Arial", 12))
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Courier", 11))
        self.input_field.setPlaceholderText("Type anything to hash...")
        self.input_field.returnPressed.connect(self.generate_hash)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_field)
        layout.addLayout(input_layout)

        # Generate button
        self.generate_btn = QPushButton("Generate Hash")
        self.generate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_hash)
        layout.addWidget(self.generate_btn)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Results section
        result_title = QLabel("Hash Results")
        result_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(result_title)

        # Custom Hash
        custom_label = QLabel("ModShift32 Hash (32 chars):")
        custom_label.setFont(QFont("Arial", 11))
        layout.addWidget(custom_label)

        self.custom_output = QTextEdit()
        self.custom_output.setFont(QFont("Courier", 11))
        self.custom_output.setReadOnly(True)
        self.custom_output.setFixedHeight(50)
        layout.addWidget(self.custom_output)

        # SHA-256 Hash
        sha_label = QLabel("SHA-256 Hash (first 32 chars):")
        sha_label.setFont(QFont("Arial", 11))
        layout.addWidget(sha_label)

        self.sha_output = QTextEdit()
        self.sha_output.setFont(QFont("Courier", 11))
        self.sha_output.setReadOnly(True)
        self.sha_output.setFixedHeight(50)
        layout.addWidget(self.sha_output)

        # Clear button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setFont(QFont("Arial", 11))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_fields)
        layout.addWidget(self.clear_btn)

        # Status bar
        self.statusBar().showMessage("Ready to hash your input!")

        # Set focus to input
        self.input_field.setFocus()

    def generate_hash(self):
        text = self.input_field.text()
        try:
            custom_hash = modshift32_hash(text)
            sha256_hash = hashlib.sha256(text.encode()).hexdigest()[:32]

            self.custom_output.setText(custom_hash)
            self.sha_output.setText(sha256_hash)

            self.statusBar().showMessage(f"Hashed successfully! Input length: {len(text)} characters")

        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}")

    def clear_fields(self):
        self.input_field.clear()
        self.custom_output.clear()
        self.sha_output.clear()
        self.statusBar().showMessage("All fields cleared")
        self.input_field.setFocus()


# --- RUN APPLICATION ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Clean modern style
    window = HashingApp()
    window.show()
    sys.exit(app.exec_())