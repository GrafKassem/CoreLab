/**
   Copyright (c) Dev Berry Group www.dev-berry.com
   @author Kassem Farhat 
**/
#include <SPI.h>
#include "LCD_Driver.h"
#include "GUI_Paint.h"
#include "image.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH1106.h>
#include <Servo.h>
long randNumber;
long updateask;
Servo myservo;
// Angenommen, der Servo startet in der Mitte seines Bewegungsbereichs.
int currentPosition = 90; // Startposition in Grad, 90° für die Mitte
const int stepSize = 30; // Schrittgröße für die Bewegung
const int minPosition = 0; // Minimal mögliche Position
const int maxPosition = 180; // Maximal mögliche Position
String inputString = "";         // Ein String zum Speichern der eingehenden Daten
bool stringComplete = false;
int version = 1.13;
void serialEvent() {
    while (Serial.available()) {
        // Holt das nächste Zeichen
        char inChar = (char)Serial.read();
        // Fügt es zum Input-String hinzu
        inputString += inChar;

        // Wenn ein Zeilenende empfangen wird, markiert es das Ende des Strings
        if (inChar == '\n') {
            stringComplete = true;
        }
    }
}
void eye()
{
  Paint_Clear(WHITE); // Löscht den aktuellen Bildschirm für ein neues Zeichnen
Paint_DrawString_EN(50, 123, "CoreLab (R)",&Font16,  BLACK, GREEN);
Paint_DrawString_EN(50, 50, "Version: 1.13",&Font16,  BLACK, GREEN);
delay(4000);
Paint_Clear(CYAN);
//Paint_DrawCircle(120, 120, 115, CYAN, DOT_PIXEL_2X2, DRAW_FILL_FULL);
Paint_DrawCircle(120, 120, 75, GRAYBLUE, DOT_PIXEL_2X2, DRAW_FILL_FULL);
Paint_DrawCircle(120, 100, 35, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL);
Paint_DrawCircle(130, 90, 10, WHITE, DOT_PIXEL_2X2, DRAW_FILL_FULL);
Paint_DrawCircle(120, 120, 85, DARKGRAY, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
Paint_DrawCircle(120, 85, 15, LIGHTGRAY, DOT_PIXEL_2X2, DRAW_FILL_FULL);
}
void music()
{
   Paint_Clear(CYAN);
  Paint_DrawCircle(120, 180, 20, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL); // Kopf der Note
    Paint_DrawLine(120, 160, 120, 80, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Stiel der Note
    Paint_DrawLine(120, 80, 150, 100, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Untere Linie des Notenhalses
    Paint_DrawLine(120, 90, 160, 110, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Mittlere Linie des Notenhalses
    Paint_DrawLine(120, 100, 170, 120, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Obere Linie des Notenhalses
}
void questmark()
{
  Paint_Clear(CYAN);
Paint_DrawCircle(120, 120, 75, GRAYBLUE, DOT_PIXEL_2X2, DRAW_FILL_FULL); // Iris

    // Pupille nach oben gerichtet, um ein fragendes Aussehen zu geben
    Paint_DrawCircle(120, 105, 35, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL); // Pupille
    Paint_DrawCircle(130, 95, 10, WHITE, DOT_PIXEL_2X2, DRAW_FILL_FULL); // Glanzlicht der Pupille

    // Angehobene Augenbraue für einen fragenden Ausdruck
    Paint_DrawLine(70, 70, 170, 100, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Unterkante der Augenbraue
    Paint_DrawLine(70, 70, 120, 80, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Oberkante der Augenbraue, verbindet sich mit der Unterkante
    Paint_DrawLine(120, 80, 170, 100, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID); // Oberkante der Augenbraue, verbindet sich mit der Unterkante
}
void drawSadEye() {
    Paint_Clear(CYAN);
    // Große, unten abgesenkte Augenbrauen für einen traurigen Ausdruck
    Paint_DrawLine(70, 100, 170, 100, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(70, 100, 120, 120, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(120, 120, 170, 100, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    // Traurige Augen haben oft eine abwärts Kurve
    Paint_DrawCircle(120, 140, 20, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL);
}

void drawSkepticalEye() {
    Paint_Clear(CYAN);
    // Eine angehobene Augenbraue kann Skepsis oder Verwirrung zeigen
    Paint_DrawLine(70, 80, 170, 120, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(70, 80, 120, 90, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(120, 90, 170, 120, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    // Pupille leicht nach oben gerichtet
    Paint_DrawCircle(120, 120, 20, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL);
}

void drawAngryEye() {
    Paint_Clear(CYAN);
    // Zusammengekniffene Augenbrauen für einen wütenden Ausdruck
    Paint_DrawLine(70, 80, 170, 80, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(70, 80, 120, 60, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    Paint_DrawLine(120, 60, 170, 80, BLACK, DOT_PIXEL_2X2, LINE_STYLE_SOLID);
    // Eine kleinere Pupille könnte Wut oder Konzentration zeigen
    Paint_DrawCircle(120, 120, 15, BLACK, DOT_PIXEL_2X2, DRAW_FILL_FULL);
}

void setup()
{
  myservo.attach(2);
  Config_Init();
  LCD_Init();
  LCD_SetBacklight(1000);
  Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, BLACK);
  Paint_Clear(WHITE);
 eye();
 delay(3000);
 Serial.begin(9600);
    inputString.reserve(200);  
  
}


/**
  #############################################
  #  Application Programming Interfaces (API) #
  #############################################
**/

void loop() {

  // Verarbeitet neue Eingaben und prüft, ob eine Zeile fertig ist
    if (stringComplete) {
      //  Serial.print("You typed: ");
        //Serial.println(inputString); // Gibt die gesammelte Eingabe aus

        if (inputString.startsWith("debug_on")) {
            Serial.println("Developer Mode");
            Paint_Clear(WHITE); 
            Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, BLACK);
            Paint_DrawString_EN(50, 123, "CoreLab (R)",&Font16,  BLACK, GREEN);
            Paint_DrawString_EN(50, 50, "Version: 1.13",&Font16,  BLACK, GREEN);
            Paint_DrawString_EN(50, 150, "API Mode",&Font20,  BLACK, GREEN);
        } else if (inputString.startsWith("debug_off")) {
            eye();
        }else if(inputString.startsWith("-data")){
              Paint_Clear(WHITE); 
              Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, BLACK);
              Serial.println("Version: 1.13");
              Serial.println("Publisher: Dev Berry Group x CoreLab");
              Paint_DrawString_EN(50, 123, "OK!",&Font24,  BLACK, GREEN);
        }else if(inputString.startsWith("-cnf"))
            {
            Paint_Clear(WHITE); 
            Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, BLACK);
            Paint_DrawString_EN(50, 123, "CoreLab (R)",&Font16,  BLACK, GREEN);
            Paint_DrawString_EN(50, 50, "Version: 1.13",&Font16,  BLACK, GREEN);
            Paint_DrawString_EN(50, 150, "API Mode",&Font20,  BLACK, GREEN);
            Paint_DrawString_EN(50, 180, "Config Mode",&Font16,  BLACK, GREEN);
        }else if(inputString.startsWith("-ver")){
          Serial.println("Version 1.13");
        }else if(inputString.startsWith("-std"))
        {
          eye();
          Serial.println("OK!");
        }else if(inputString.startsWith("-music"))
        {
          music();
          Serial.println("OK!");
        }else if(inputString.startsWith("-quest"))
        {
          questmark();
          Serial.println("OK!");
        }else if(inputString.startsWith("-sad"))
        {
          drawSadEye();
          Serial.println("OK!");
        }else if(inputString.startsWith("-huh"))
        {
          drawSkepticalEye();
          Serial.println("OK!");
        }else if(inputString.startsWith("-angry"))
        {
          drawAngryEye();
          Serial.println("OK!");
        } else if(inputString.startsWith("R")) {
           myservo.write(90);
    currentPosition = 90;
    int newPosition = currentPosition + stepSize;
    if(newPosition <= maxPosition) { // Verhindert Überbewegung
      myservo.write(newPosition);
      currentPosition = newPosition; // Aktualisiere die aktuelle Position
    }
  } else if(inputString.startsWith("L")) {
     myservo.write(90);
    currentPosition = 90;
    int newPosition = currentPosition - stepSize;
    if(newPosition >= minPosition) { // Verhindert Überbewegung
      myservo.write(newPosition);
      currentPosition = newPosition; // Aktualisiere die aktuelle Position
    }
  } else if(inputString.startsWith("0")) {
    // Optional: Rückkehr zur Startposition
    myservo.write(90);
    currentPosition = 90;
  }
        
        
        else{
         Serial.println("ERR!");
        }
        inputString = "";
        stringComplete = false;
    }
}

