from picamera2 import Picamera2
import numpy as np
import cv2
import time
import csv
from datetime import datetime, timedelta

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
    while True:
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
               
                if className in ["person", "hand", "arm"]: 
                    box = detection[3:7] * np.array([640, 480, 640, 480])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame_rgb, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame_rgb, className.capitalize(), (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Aktualisieren der erkannten Objekte und deren Aufenthaltsdauer
                    object_id = f"{className}({startX},{startY})"  
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
