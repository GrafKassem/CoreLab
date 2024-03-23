import serial
import serial.tools.list_ports
import time
import os
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

def main():
    port = select_serial_port()
    if port:
        ser = serial.Serial(port, 9600, timeout=1)
        print(f"Verbunden mit {port}. Geben Sie 'exit' ein, um zu beenden.")
        os.system("clear")
        print("Application Programming Interfaces (API) \r\n-music: Music Interface                              \r\n-quest: QuestionMark Eye         \r\n-std: Standart Eye Mode\r\n-sad: Sad Eye\r\n-huh: Surprised Eye\r\n-angry: Angry Eye\r\n\r\nConfigs:\r\n-cnf: Config Mode\r\ndebug_on: Debug Mode\r\ndebug_off: Simple Mode                 \r\n")
        time.sleep(25)  # Warten auf die Initialisierung der seriellen Verbindung
        ser.flushInput()  # Eingabepuffer leeren
        
        while True:
            cmd = input("Senden: ")
            if cmd.lower() == 'exit':
                break
            ser.write((cmd + '\n').encode())  # '\n' als Endezeichen hinzufügen
            ser.flush()  # Stellt sicher, dass der Befehl gesendet wird
            time.sleep(6)
            response = ser.readline().decode().strip()
            print("Antwort:", response)
        ser.close()

if __name__ == "__main__":
    main()
