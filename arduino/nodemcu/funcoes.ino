
void error() {
  mario2();
  //digitalWrite(out2, LOW);
  //delay(500);
  //digitalWrite(out2, HIGH);
}


void connectaWifi() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Conectando ao wifi ");
    Serial.print(rede);
    Serial.print(" Senha ");
    Serial.println(senha);
    if (WiFi.status() == WL_CONNECTED)
    {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Conectado");
      Serial.println("Conectado");
      
    }
  }
}


String readCard() {
  String cont = "";


  if ( ! mfrc522.PICC_IsNewCardPresent() or !mfrc522.PICC_ReadCardSerial()) {
    return "";
  }

  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cont.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  cont.toUpperCase();
  return cont;
 
}
   
void credito() {
  digitalWrite(out1, LOW);
  //tone(buzzer, 100, 1000);
  delay(300);           // Tempo em ms que o relê fica acionado para gerar o credito
  digitalWrite(out1, HIGH);
  mario1();

}

  struct responseHttp httpGet(String link) {
  struct responseHttp response;
  String fixedUrl = "http://201.27.119.72:5000/api";
  HTTPClient http;

  http.begin(fixedUrl + link);
  http.addHeader("Content-Type", "text/plain");
  int httpCode = http.GET();
  String resposta = http.getString();

  response.sts = httpCode;
  response.content = resposta;

  http.end();

  return response;
 
}
