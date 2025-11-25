/* #include <Servo.h>

Servo servo1;  // Servomotor actual 

// Pines
const int pinServo1 = 9;
const int ledVerde = 5;
const int ledRojo = 6;

// Función para abrir y cerrar el servo
void moverServo() {
  servo1.write(90);   // Abrir compuerta
  delay(1000);
  servo1.write(0);    // Cerrar compuerta
}

// Configuración inicial
void setup() {
  Serial.begin(9600); // Comunicación serial
  servo1.attach(pinServo1);
  servo1.write(0);    // Servo en posición cerrada

  pinMode(ledVerde, OUTPUT);
  pinMode(ledRojo, OUTPUT);

  Serial.println(" Arduino listo para recibir comandos (solo V por ahora)");
}

// Bucle principal
void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    Serial.print("🔹 Comando recibido: ");
    Serial.println(comando);

    // Solo actuará el servo si el comando es 'V'
    if (comando == 'V') {
      Serial.println("🟢 Activando servomotor (Verde)");
      digitalWrite(ledVerde, HIGH);
      moverServo();
      delay(5000);
      digitalWrite(ledVerde, LOW);
    }

    // Si llega 'R', solo prende el LED rojo
    else if (comando == 'R') {
      Serial.println("🔴 Clasificación fallida: LED rojo encendido");
      digitalWrite(ledRojo, HIGH);
      delay(5000);
      digitalWrite(ledRojo, LOW);
    }

    // Si llega otro comando, simplemente lo ignora
    else {
      Serial.println("⚠️ Comando no válido (sin acción)");
    }
  }
}
 */