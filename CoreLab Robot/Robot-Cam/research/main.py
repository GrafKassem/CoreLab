from picamera2 import Picamera2
import numpy as np
import cv2

# Initialisiere picamera2
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)

# Starte die Kamera
picam2.start()

try:
    while True:
        # Erfasse ein Frame und konvertiere es in ein NumPy-Array
        frame = picam2.capture_array()
        
        # Konvertiere BGR zu RGB (wenn nötig, abhängig von der picamera2-Ausgabe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Zeige das Bild an
        cv2.imshow("Frame", frame_rgb)
        
        # Beende die Schleife mit der 'q'-Taste
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Ressourcen freigeben
    picam2.stop()
    cv2.destroyAllWindows()
