import os
import socket
import qrcode
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from io import BytesIO
import time

# Configuration
PORT = 8000
FILE_NAME = "a.txt"
OUTPUT_FILE = "output.txt"

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

# Serveur HTTP avec traitement des POST
class CustomHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Récupération des données POST
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))

        # Extraction de la commande et écriture dans le fichier
        command = data.get('command', [''])[0]
        if command:
            with open(FILE_NAME, 'a') as file:
                file.write(command + '\n')
            print(f"Commande reçue : {command}")

        # Réponse au client
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write("Commande reçue avec succès.".encode("utf-8"))
        self.wfile.write(response.getvalue())

    def do_GET(self):
        if self.path == '/output':
            # Vérifie si le fichier output.txt existe
            if os.path.exists(OUTPUT_FILE):
                with open(OUTPUT_FILE, 'r') as file:
                    content = file.read()
            else:
                content = "Fichier en attente..."
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()

# Démarrage du serveur
if __name__ == "__main__":
    # Vérifie la présence d'index.html
    if not os.path.exists("index.html"):
        print("Erreur : fichier index.html introuvable.")
        exit(1)

    # Lancement du serveur
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{PORT}/"
    generate_qr_code(url)

    print(f"Serveur démarré sur {url}. Scannez le QR Code pour accéder.")
    with HTTPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur.")
