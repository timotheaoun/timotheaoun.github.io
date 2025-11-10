import os
import socket
import qrcode
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from io import BytesIO
import threading
import time
import pyautogui
from PIL import Image, ImageDraw, ImageFont

# Configuration
PORT = 8000
IMAGE_FILE = "a.jpg"

# Génération de l'adresse IP locale
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Génération du QR Code
def generate_qr_code(url):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    print(f"QR Code généré : {url}")

# Générer une image mise à jour dynamiquement
def update_image():
    count = 0
   
class CustomHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Récupération des données POST
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))

        # Extraction des coordonnées et de l'action
        x = data.get('x', [''])[0]
        y = data.get('y', [''])[0]
        action = data.get('action', [''])[0]

        print(f"Coordonnées reçues : x={x}, y={y}, action={action}")

        # Validation et traitement des coordonnées
        if x.isdigit() and y.isdigit():
            x = int(x)
            y = int(y)

            # Exécution des actions basées sur l'événement
            if action == 'left_click':
                pyautogui.moveTo(x, y)
                pyautogui.click()
                print(f"Clic gauche à ({x}, {y})")
            elif action == 'right_click':
                pyautogui.moveTo(x, y)
                pyautogui.rightClick()
                print(f"Clic droit à ({x}, {y})")
            elif action == 'double_click':
                pyautogui.moveTo(x, y)
                pyautogui.doubleClick()
                print(f"Double clic à ({x}, {y})")
            else:
                print(f"Action inconnue : {action}")
        else:
            print("Coordonnées invalides ou manquantes")

        # Réponse au client
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write("Coordonnées reçues et action exécutée.".encode("utf-8"))
        self.wfile.write(response.getvalue())

    def do_GET(self):
        if self.path == f"/{IMAGE_FILE}":
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            with open(IMAGE_FILE, 'rb') as img:
                self.wfile.write(img.read())
        else:
            super().do_GET()

# Démarrage du serveur
if __name__ == "__main__":
    if not os.path.exists("index.html"):
        print("Erreur : fichier index.html introuvable.")
        exit(1)

    if not os.path.exists(IMAGE_FILE):
        img = Image.new('RGB', (200, 200), color=(0, 0, 0))
        img.save(IMAGE_FILE)

    threading.Thread(target=update_image, daemon=True).start()

    local_ip = get_local_ip()
    url = f"http://{local_ip}:{PORT}/"
    generate_qr_code(url)

    print(f"Serveur démarré sur {url}. Scannez le QR Code pour accéder.")
    with HTTPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur.")
