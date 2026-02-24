import sys
import requests
import webbrowser # <-- New library for opening the browser
from urllib.parse import urlparse
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QTextEdit)
from PyQt6.QtCore import Qt

class ShadowPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Shadow-Ping | Secure Network Tool")
        self.setGeometry(100, 100, 500, 500) # Made the window slightly taller
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0a0a0f;
            }
            QLabel {
                color: #b366ff;
                font-size: 16px;
                font-family: monospace;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #16161e;
                color: #00ffcc;
                border: 1px solid #b366ff;
                padding: 10px;
                font-size: 14px;
                font-family: monospace;
            }
            QPushButton {
                background-color: #2b1a3d;
                color: #b366ff;
                border: 2px solid #b366ff;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                font-family: monospace;
            }
            QPushButton:hover {
                background-color: #b366ff;
                color: #0a0a0f;
            }
            QTextEdit {
                background-color: #16161e;
                color: #00ffcc;
                border: 1px solid #b366ff;
                padding: 10px;
                font-size: 14px;
                font-family: monospace;
            }
        """)
        
        title = QLabel("Shadow-Ping: Target Locator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter Target IP or URL...")
        self.ip_input.returnPressed.connect(self.run_trace)
        layout.addWidget(self.ip_input)
        
        self.trace_btn = QPushButton("INITIATE TRACE")
        self.trace_btn.clicked.connect(self.run_trace)
        layout.addWidget(self.trace_btn)
        
        # --- NEW: The Map Button ---
        self.map_btn = QPushButton("VIEW TARGET ON MAP")
        self.map_btn.clicked.connect(self.open_map)
        self.map_btn.hide() # We hide this until a trace is successful
        layout.addWidget(self.map_btn)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setText("Awaiting target input...")
        layout.addWidget(self.results_display)

        # Variables to store coordinates
        self.current_lat = None
        self.current_lon = None

    def run_trace(self):
        self.map_btn.hide() # Reset the button on a new trace
        
        raw_input = self.ip_input.text().strip()
        if not raw_input:
            self.results_display.setText("Error: No target provided. Please enter an IP or URL.")
            return

        if raw_input.startswith("http://") or raw_input.startswith("https://"):
            target = urlparse(raw_input).netloc
        else:
            target = raw_input.split('/')[0]
            
        self.results_display.setText(f"Target Acquired: {target}\nInitializing trace...\nBypassing routing protocols...\n\n(API connection pending...)")
        QApplication.processEvents() 
        
        try:
            response = requests.get(f"http://ip-api.com/json/{target}")
            data = response.json()
            
            if data['status'] == 'fail':
                self.results_display.append(f"\n[TRACE FAILED]\nReason: {data.get('message', 'Invalid target or Private Network')}")
                return
                
            # Store coordinates for the map function
            self.current_lat = data.get('lat')
            self.current_lon = data.get('lon')
            
            result_text = f"""
[TRACE SUCCESSFUL]
-----------------------------------
Target    : {target}
Server IP : {data.get('query')}
ISP/Org   : {data.get('isp')} / {data.get('org')}
Location  : {data.get('city')}, {data.get('regionName')}
Country   : {data.get('country')}
Timezone  : {data.get('timezone')}
Lat/Lon   : {self.current_lat}, {self.current_lon}
-----------------------------------
Status: Coordinates Locked.
"""
            self.results_display.setText(result_text)
            
            # Reveal the Map button if coordinates exist
            if self.current_lat and self.current_lon:
                self.map_btn.show()
            
        except Exception as e:
            self.results_display.setText(f"Error connecting to trace database: {e}")

    # --- NEW: The Browser Trigger ---
    def open_map(self):
        if self.current_lat and self.current_lon:
            maps_url = f"https://www.google.com/maps/search/?api=1&query={self.current_lat},{self.current_lon}"
            webbrowser.open(maps_url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShadowPingApp()
    window.show()
    sys.exit(app.exec())