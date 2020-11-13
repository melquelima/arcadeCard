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

char* rede = "Menezes apolinario";     // Digite o nome da rede wifi entre "aspas"
char* senha = "melque01"; // Digite a senha da rede wifi entre "aspas"
String token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9tYXF1aW5hIjo5LCJjb250cm9sX3N0ciI6InNPN2JacEVrVXd3In0.n3iRxd8GLZ45Yyx9kldbLlFGAb1a3zgV7frjnIF8VfM";

/////////////////////////////////////////////////////////////////////////
LiquidCrystal_I2C lcd(0x3F, 16, 2);
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

 lcd.init();   // INICIALIZA O DISPLAY LCD
 lcd.backlight(); // HABILITA O BACKLIGHT (LUZ DE FUNDO) 

  pinMode(out1, OUTPUT);
  //pinMode(out2, OUTPUT);

  digitalWrite(out1, HIGH);

  
  //digitalWrite(out2, HIGH);
  connectaWifi();
  //Serial.println();
  //Serial.println(EEPROM.read(10));

}

void loop() {
  printLcd(0, 0, "Passe o cartao!", true);
  
  String tag = "";
  connectaWifi();

  tag = readCard();
  if (tag != "") {
    printLcd(0, 0, "Validando...", true);
    validate(tag);
  }
}

void validate(String tag) {

  String link = "";
  Serial.println(tag);
  link = "/validate?tag=" + tag + "&token=" + token;

  resp = httpGet(link);

  Serial.println(resp.sts);
  Serial.println(resp.content);

  if (resp.sts == 200) {
    String nome = getValue(resp.content, '\n', 0);
    String text = getValue(resp.content, '\n', 1);
  
    printLcd(0, 0, nome, true);
    printLcd(0, 1, text, false);
    credito();
  } else {
    printLcd(0, 0, "=====ERROR=====", true);
    printLcd(0, 1, resp.content, false);
    mario2();
    delay(1000);
  }
}
