from picamera2 import Picamera2
import numpy as np
import cv2
import time
import csv
from datetime import datetime, timedelta
import serial
import serial.tools.list_ports
import os
import random
import secrets
satz_liste = [
    "-angry",
   # "-std",
    "-huh",
    "-sad",
  #  "-music",
 #  "-quest"
]

#Serielle Schnittstelle 
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port, desc, hwid in sorted(ports):
        print(f"({len(available_ports) + 1}) {desc} - {port}")
        available_ports.append(port)
    return available_ports

def select_serial_port():
    available_ports = list_serial_ports()
    if not available_ports:
        print("Keine seriellen Ports gefunden.")
        return None
    choice = input("Wählen Sie einen Port aus (Nummer): ")
    try:
        index = int(choice) - 1
        if index >= 0 and index < len(available_ports):
            return available_ports[index]
        else:
            print("Ungültige Auswahl.")
            return None
    except ValueError:
        print("Bitte eine Zahl eingeben.")
        return None
    
# Laden der COCO-Klassennamen
classNames = []
classFile = "coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")


model = cv2.dnn.readNet("frozen_inference_graph.pb", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")

# Initialisieren der picamera2
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)

# Starten der Kamera
picam2.start()

# Dictionary zum Verfolgen der erkannten Objekte und deren Aufenthaltsdauer
tracked_objects = {}


csv_file = open("object_tracking.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Object ID", "Duration (seconds)", "Time"])

try:
    port = select_serial_port()
    if port:
        ser = serial.Serial(port, 9600, timeout=1)
        print(f"Verbunden mit {port}. Geben Sie 'exit' ein, um zu beenden.")
        os.system("clear")
        print("Application Programming Interfaces (API) \r\n-music: Music Interface                              \r\n-quest: QuestionMark Eye         \r\n-std: Standart Eye Mode\r\n-sad: Sad Eye\r\n-huh: Surprised Eye\r\n-angry: Angry Eye\r\n\r\nConfigs:\r\n-cnf: Config Mode\r\ndebug_on: Debug Mode\r\ndebug_off: Simple Mode                 \r\n")
        time.sleep(10)  # Warten auf die Initialisierung der seriellen Verbindung
        ser.flushInput()  # Eingabepuffer leeren
        
    while True:
        token1 = secrets.randbelow(110)
        token2 = secrets.randbelow(99)
        token3 = secrets.randbelow(100)
        token4 = secrets.randbelow(60)

        # Führen Sie eine Reihe von Operationen durch
        # Multiplikation -> Subtraktion -> Division, bleiben Sie unter 250
        # Beispiel: ((token1 * token2) - token3) / token4
        # Achten Sie darauf, Division durch Null zu vermeiden und das Ergebnis < 250 zu halten

        resultat = ((token1 * token2) - token3)
        if token4 != 0:  # Vermeiden Sie Division durch Null
            resultat /= token4

        # Stellen Sie sicher, dass das Ergebnis unter 250 bleibt
        resultat = resultat if resultat < 250 else 249
        # Erfassen eines Frames und Konvertieren in ein NumPy-Array
        frame = picam2.capture_array()
        
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Objekterkennung im Frame
        blob = cv2.dnn.blobFromImage(frame_rgb, size=(300, 300), swapRB=True)
        model.setInput(blob)
        output = model.forward()

        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > 0.5:  # Filtern von Erkennungen mit einer Zuversicht > 50%
                classId = int(detection[1])
                className = classNames[classId - 1]
               
                if className in ["person"]: 
                    box = detection[3:7] * np.array([640, 480, 640, 480])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame_rgb, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame_rgb, className.capitalize(), (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print(f"Token1: {token1}, Token2: {token2}, Token3: {token3}, Token4: {token4}, Ergebnis: {resultat}")
                    if resultat <= 60:
                        zufaelliger_satz = random.choice(satz_liste)
                        print(zufaelliger_satz)
                        ser.write((zufaelliger_satz + '\n').encode())  # '\n' als Endezeichen hinzufügen
                        ser.flush()  # Stellt sicher, dass der Befehl gesendet wird
                    else:
                        # 70% Chance, dass nichts passiert
                        print("Kein Satz ausgewählt.")
                    # Aktualisieren der erkannten Objekte und deren Aufenthaltsdauer
                    object_id = f"{className}({startX},{startY})"  
                    time.sleep(0.5)
                    if object_id not in tracked_objects:
                        tracked_objects[object_id] = {"start_time": time.time()} 
                    else:
                        tracked_objects[object_id]["duration"] = time.time() - tracked_objects[object_id]["start_time"]  # Aufenthaltsdauer aktualisieren

        # Anzeigen des Frames
        cv2.imshow("Frame", frame_rgb)
        
        # Protokollieren der erkannten Objekte und ihrer Aufenthaltsdauer
        for object_id, info in tracked_objects.items():
            duration_seconds = info["duration"] if "duration" in info else 0
            duration_formatted = str(timedelta(seconds=duration_seconds))  # Formatierung der Aufenthaltsdauer
            start_time_str = datetime.fromtimestamp(info["start_time"]).strftime("%H:%M:%S:%f")
            print(f"{object_id}: {duration_formatted}, {start_time_str}")  # Ausgabe in Konsole
            
            csv_writer.writerow([object_id, duration_formatted, start_time_str])  # Schreiben in CSV-Datei

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Freigeben der Ressourcen
    picam2.stop()
    cv2.destroyAllWindows()
    csv_file.close()  
