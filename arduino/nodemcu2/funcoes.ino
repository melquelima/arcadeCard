void connectaWifi() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Conectando ao wifi ");
    Serial.print(rede);
    Serial.print(" Senha ");
    Serial.println(senha);
    printLcd(0, 0, "Conectando... ", true);
    if (WiFi.status() == WL_CONNECTED)
    {
      Serial.println("Conectado");
      printLcd(0, 0, "Conectado ", true);
      delay(1000);
    }
  }
}


String readCard() {
  String cont = "";

  while ( ! mfrc522.PICC_IsNewCardPresent() or !mfrc522.PICC_ReadCardSerial()) {
    delay(200);
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
  String fixedUrl = "http://www.arcadetag.com.br/api";
  HTTPClient http;

  http.setTimeout(5*1000);
  http.begin(fixedUrl + link);
  http.addHeader("Content-Type", "text/plain");
  int httpCode = http.GET();
  String resposta = http.getString();

  response.sts = httpCode;
  response.content = resposta;

  http.end();

  return response;
}

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void printLcd(int x, int y, String text, bool clr) {
  if (clr) {
    lcd.clear();
  }
  lcd.setCursor(x, y);
  lcd.print(text);
}
