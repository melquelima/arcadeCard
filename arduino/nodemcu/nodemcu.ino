#include <Wire.h>
#include <EEPROM.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <LiquidCrystal_I2C.h>
#define SS_PIN D4       
#define RST_PIN D8      //Não conectar esse pino na placa rc522, da erro ao gravar a placa
#include <SPI.h>
#include <MFRC522.h>
#define out1  16       // Saida D0 de 0V para rele de creditos
//#define out2         // Saida D3 de 0V para led vermelho indicador de erro
#define buzzer D3

//////////////////////////// DADOS PARA PREENCHER /////////////////////////

char* rede = "LOJA 01-Oi FIBRA 2.4Ghz";     // Digite o nome da rede wifi entre "aspas"
char* senha = "loteria01"; // Digite a senha da rede wifi entre "aspas"
String token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9tYXF1aW5hIjoxLCJjb250cm9sX3N0ciI6IlhyeEVhTG83QkNRIn0.dTO0SwMCEt_y1acDqrZANRxEU5Yx5ZsM9Yjna601JA4";

/////////////////////////////////////////////////////////////////////////

LiquidCrystal_I2C lcd(0x27, 16, 2);
MFRC522 mfrc522(SS_PIN, RST_PIN);
int statuss = 0;
int out = 0;


struct responseHttp {
  int sts;
  String content;
};
struct responseHttp resp;


void setup()
{
  Serial.begin(9600);
  WiFi.begin(rede, senha);
  SPI.begin();
  mfrc522.PCD_Init();
  EEPROM.begin(512);

  lcd.begin(16,2);
  lcd.init();
  lcd.backlight();

  
  pinMode(out1, OUTPUT);
  //pinMode(out2, OUTPUT);
  
  digitalWrite(out1, HIGH);
  //digitalWrite(out2, HIGH);
  connectaWifi();
 
  
  Serial.println();
  Serial.println(EEPROM.read(10));
}

void loop() {

  String tag = "";
  connectaWifi();

  tag = readCard();
  if (tag != "") {
    validate(tag);
  }
  delay(1000);
}

void validate(String tag) {
  
  String link = "";
  Serial.println(tag);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(tag);
  link = "/validate?tag=" + tag + "&token=" + token;

  resp = httpGet(link);

  lcd.setCursor(0, 1);
  lcd.print(resp.sts);

  Serial.println(resp.sts);
  Serial.println(resp.content);

  if (resp.sts == 200) {
    credito();
  } else {
    error();
  }
}
