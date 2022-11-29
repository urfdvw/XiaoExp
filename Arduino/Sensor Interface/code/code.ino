#include <Adafruit_FreeTouch.h>
#include <adafruit_ptc.h>
#include <samd21_ptc_component.h>

#include <Tiny4kOLED.h>

#include "data.h"

/*
 * time
 */
 
unsigned long timems;

/*
 * Touch
 */

class TouchButton {
  private:
    uint8_t _pin;
    Adafruit_FreeTouch _touch;
  public:
    TouchButton(uint8_t pin) {
      _pin = pin;
      _touch = Adafruit_FreeTouch(_pin, OVERSAMPLE_4, RESISTOR_50K, FREQ_MODE_NONE);
      _touch.begin();
    }
    bool get() {
      return _touch.measure() > 500;
    }
};

TouchButton button_left(A7);
TouchButton button_up(A8);
TouchButton button_down(A9);
TouchButton button_right(A10);

/*
 * Buttons
 */

// reading and last reading
bool cur_left = false;
bool cur_up = false;
bool cur_down = false;
bool cur_right = false;
bool last_left = false;
bool last_up = false;
bool last_down = false;
bool last_right = false;

// golbal that holds the button info
char buttons;
#define UP_EDGE 0x01
#define DOWN_EDGE 0x02
#define LEFT_EDGE 0x04
#define RIGHT_EDGE 0x08
#define UP_HOLD 0x10
#define DOWN_HOLD 0x20
#define LEFT_HOLD 0x40
#define RIGHT_HOLD 0x80

// perform the reading
unsigned long button_time;
char input() {
  buttons = 0x00;
  cur_left = button_left.get();
  cur_up = button_up.get();
  cur_down = button_down.get();
  cur_right = button_right.get();


  if(cur_down){
    Serial.print("\n button_down ");
    buttons |= DOWN_HOLD;
    if(!(last_down)){
      buttons |= DOWN_EDGE;
    }
  } else if (cur_right){
    Serial.print("\n button_right ");
    buttons |= RIGHT_HOLD;
    if(!(last_right)){
      buttons |= RIGHT_EDGE;
    }
  } else if (cur_left){
    Serial.print("\n button_left ");
    buttons |= LEFT_HOLD;
    if(!(last_left)){
      buttons |= LEFT_EDGE;
    }
  } else if (cur_up){
    Serial.print("\n button_up ");
    buttons |= UP_HOLD;
    if(!(last_up)){
      buttons |= UP_EDGE;
    }
  } else {
    button_time = timems;
  }

  if((timems - button_time) > 1500){ // if hold more than a while
    buttons >>= 4; // repeat button while hold
  }

  last_left = cur_left;
  last_right = cur_right;
  last_up = cur_up;
  last_down = cur_down;
}

/* 
 * sensors
 */

int raw;

float filtered = 0;
int alpha = 1; // filter setting
int bank[20];
int beta = 0;

float voltage;
char unit_r = 'K';
int regular_r = 0;
float sensor_r;


void initbank(){
  filtered = int(filtered);
  for(beta=0; beta<alpha; beta++){
    bank[beta] = int(filtered);
  }
  beta = 0;
}


//#define B_DEF 3820 // good value
#define B_DEF 3900
#define LOG_R25 2.3 // R25 = 10

float temp;
float B_0 = B_DEF;
float B_100 = B_DEF;
void read_sensor(){
  // sensing time
  timems = millis(); 
  // reading ex ADC
  for(int i=0; i<3; i++){
    delay(1);
    raw = analogRead(A1);
  }
  // filtering
  filtered = filtered - (float(bank[beta]) - float(raw)) / float(alpha);
  bank[beta] = raw;
  beta++;
  if (beta >= alpha){
    beta = 0;
  }
  // calculation
  voltage = filtered * 3.3 / 1024;
  sensor_r = float(regular_r) / (1023.0 - filtered) * filtered;
  if (filtered > 1022.0){
    sensor_r = 9999.99;
  }

  // temp
  // 1 / ((log(Rs) - log(R25))/B + 1/(25+273.15)) - 273.15
  if(sensor_r < 10){
    temp = 1 / ((log(sensor_r) - LOG_R25)/B_100 + 0.003354) - 273.15;
  }else{
    temp = 1 / ((log(sensor_r) - LOG_R25)/B_0 + 0.003354) - 273.15;
  }
  
  
}

void calibrate_0() {
  // (log(Rs) - log(R25)) * (1/ (1/273.15 - 1/(273.15 + 25)))
  B_0 = (log(sensor_r) - LOG_R25) * 3257.5869;
}

void calibrate_100() {
  // (log(Rs) - log(R25)) * (1/ (1/373.15 - 1/(273.15 + 25)))
  B_100 = (log(sensor_r) - LOG_R25) * (-1483.3956);
}

/*
 * parameters of other apps
 * m: menu
 * a: change_alpha
 * t: change_thr
 * f: figure
*/

char cur_app = 'm';

// alarm app parameters
int thr = 512;
int alarm_mode = 0; // 0:disable 1:lt no keep -1:gt no keep
bool alarm_not_keep = true;

// figure app
int disp_x = 0;

// screen apps
int scr_bri = 0;
int scr_ori = 0;

// temp
bool temp_disp = false;

/*
 * Menu
 */

// menu variables
int current_sel = 1;
int screen_top = 1;
int current_draw = 1;

// navigation actions
void backhome(){
  current_sel = 1;
  screen_top = 1;
}

void back() {
  if(parent_data[current_sel] != 0){
    current_sel = parent_data[current_sel];
    if(previous_data[current_sel] != 0){
      screen_top = previous_data[current_sel];
    }else{
      screen_top = current_sel;
    }
  } else {
    backhome();
  }
}

void enter (){
  if(child_data[current_sel] != 0){
    current_sel = child_data[current_sel];
    screen_top = current_sel;
  }else{
    enter_action();
  }
}

void up() {
  if(previous_data[current_sel] != 0){
    if(screen_top == current_sel){
      screen_top = previous_data[screen_top];
    }
    current_sel = previous_data[current_sel];
  }
}

void down() {
  if(next_data[current_sel] != 0){
    if(next_data[next_data[next_data[screen_top]]] == current_sel){
      screen_top = next_data[screen_top];
    }
    current_sel = next_data[current_sel];
  }
}

// value display in cases
void display_val(){
  if(current_draw == READ){
    if (alpha == 1){
      oled.print(F("RAW:"));
      oled.print(raw);
    } else {
      oled.print(F("AVERAGED:"));
      oled.print(filtered);
    }
  } else if (current_draw == READ_RAW){
    oled.print(raw);
  } else if (current_draw == READ_FLT | current_draw == ALM_RE){
    oled.print(filtered);
  } else if (current_draw == ALPHA){
    oled.print(alpha);
  } else if (current_draw == ALM_THR){
    oled.print(thr);
  } else if (current_draw == ALM_IF){
    if(alarm_mode == 0){
      oled.print(text[ALM_F]);
    } else if (alarm_mode >0) {
      oled.print(text[ALM_LT]);
    } else if (alarm_mode <0) {
      oled.print(text[ALM_GT]);
    }
  } else if (current_draw == ALM_ELSE){
    if(alarm_not_keep){
      oled.print(text[ALM_STP]);
    } else {
      oled.print(text[ALM_NTH]);
    }
  } else if (current_draw == VOL){
    oled.print(voltage);
    oled.print(F("V"));
  } else if (current_draw == REG_R){
    if(regular_r){
      oled.print(regular_r);
      oled.print(unit_r);
    }
  } else if (current_draw == SEN_R){
    if(regular_r){
      oled.print(sensor_r);
      oled.print(unit_r);
    }
  } else if (current_draw == PHY){
    if(temp_disp){
      oled.print(F("TEMP:"));
      oled.print(temp);
      oled.print(F("C"));
    } else {
      oled.print(F("-"));
    }
  }
}

// enter cases
void enter_action(){
  if(current_sel == R_1K){
    regular_r = 1;
    unit_r = 'K';
    back();
  } else if (current_sel == R_10K){
    regular_r = 10;
    unit_r = 'K';
    back();
  } else if (current_sel == R_1M){
    regular_r = 1;
    unit_r = 'M';
    back();
  } else if (current_sel == R_10M){
    regular_r = 10;
    unit_r = 'M';
    back();
  } else if (current_sel == ALPHA){
    cur_app = 'a';
  } else if (current_sel == ALM_THR){
    cur_app = 't';
  } else if (current_sel == ALM_F){
    alarm_mode = 0;
    analogWrite(A3, 0);
    back();
  } else if (current_sel == ALM_GT){
    alarm_mode = -1;
    analogWrite(A3, 0);
    back();
  } else if (current_sel == ALM_LT){
    alarm_mode = 1;
    analogWrite(A3, 0);
    back();
  } else if (current_sel == ALM_NTH){
    alarm_not_keep = false;
    back();
  } else if (current_sel == ALM_STP){
    alarm_not_keep = true;
    back();
  } else if (current_sel == VOL_GRA){
    cur_app = 'f';
    disp_x = 0;
  } else if (current_sel == BRI_FIX){
    scr_bri = 0;
    back();
  } else if (current_sel == BRI_POS){
    scr_bri = 1;
    back();
  } else if (current_sel == BRI_INV){
    scr_bri = -1;
    back();
  } else if (current_sel == SCR_FIX){
    scr_ori = 0;
    back();
  } else if (current_sel == SCR_UP){
    scr_ori = 1;
    back();
  } else if (current_sel == SCR_DO){
    scr_ori = -1;
    back();
  } else if (current_sel == TEMP_CLB0){
    calibrate_0();
    current_sel = PHY;
    screen_top = VOL;
  } else if (current_sel == TEMP_CLB100){
    calibrate_100();
    current_sel = PHY;
    screen_top = VOL;
  } else if (current_sel == TEMP_DISP){
    temp_disp = !temp_disp;
    current_sel = PHY;
    screen_top = VOL;
  }
}

void menu (){
  // react to input
  if(buttons & UP_EDGE){
    up();
  } else if (buttons & DOWN_EDGE){
    down();
  } else if (buttons & RIGHT_EDGE){
    enter();
  } else if (buttons & LEFT_EDGE){
    back();
  }

  //menu display
  current_draw = screen_top; // ref of the menu item
  for(int i=0; i<4; i++){ // for each line
    oled.setCursor(0,i);
    if(current_draw == 0){ // if empty item, clean the line
      oled.fillToEOL(0x00);
      continue;
    }
    if(current_draw == current_sel){ // if selected item, inverte disp the line
      oled.invertOutput(true);
    }
    // draw fixed content
    oled.print(text[current_draw]);
    // draw changing content
    display_val();
    // clean the rest space of the line
    oled.fillToEOL(0x00);
    // cancel invert no matter what
    oled.invertOutput(false);
    // move focus to next item
    current_draw = next_data[current_draw];
  }
  // draw and swap vram
  oled.switchFrame();
}

/*
 * other apps
*/

void set_val(int * val, int limit){
  // react to input
  if(buttons & UP_EDGE){
    *val += 1;
    if(*val > limit) {
      *val = limit;
    }
  } else if (buttons & DOWN_EDGE){
    *val -= 1;
    if(*val < 1) {
      *val = 1;
    }
  } else if (buttons & (RIGHT_EDGE | LEFT_EDGE)){
    cur_app = 'm';
  }
  
  //display
  oled.clear();
  oled.setCursor(0, 0);
  oled.print(*val);
  oled.switchFrame();
}

// a
void change_alpha(){
  set_val(&alpha, 20);
  
  // change the filter while setting alpha
  initbank();
}


// t
void change_thr(){
  set_val(&thr, 1022);
}

void oledWriteByte(char data){
  oled.startData();
  oled.sendData(data);
  oled.endData();
}

// f
void figure(){
  if (buttons & LEFT_EDGE){
    cur_app = 'm';
  }
  
  for(int i=0; i<2; i++){
    for(int j=0; j<4; j++){
      int cur = 0x00;
      int rotation = 0x01;
      for(int k=0; k<8; k++){
        if((j*8+k == (1023-int(filtered))/32) | (j*8+k == (1023-thr)/32 & alarm_mode != 0)){
          cur |= rotation;
        }
        rotation <<= 1;
      }
      oled.setCursor(disp_x, j);
      oledWriteByte(cur);
      if(disp_x < 128){
        oled.setCursor(disp_x+1, j);
      } else {
        oled.setCursor(0, j);
      }
      oledWriteByte(0xff);
    }
    oled.switchFrame();
  }
  disp_x++;
  disp_x %= 128;
  delay(50);
}

//-------------------------------------------------------------------------

void setup() {
  /* oled setup */
  oled.begin(0,0);
  oled.enableChargePump();
  oled.setRotation(1); // 0 to flip
  oled.enableZoomIn();
  oled.setFont(FONT6X8CAPS);
  oled.clear();
  oled.switchRenderFrame();
  oled.clear();
  oled.switchFrame();
  oled.on();

  /* application setup */
  // input setup
  pinMode(A2, INPUT); // X
  pinMode(A3, INPUT); // Y
  pinMode(1, OUTPUT); // Buzzer
  // input setup endB

  // filter init
  initbank();

  // init buzz
  analogWrite(A3, 1);
  delay(100);
  analogWrite(A3, 0);
  delay(100);
  analogWrite(A3, 1);
  delay(100);
  analogWrite(A3, 0);
}

void loop() {
  // sensor read
  read_sensor();
  // input read
  input();  
  
  // buzzer
  if (filtered * alarm_mode < thr * alarm_mode){
    analogWrite(A3, 1);
  } else {
    if(alarm_not_keep){
      analogWrite(A3, 0);
    }
  }

  // orientation
  if (scr_ori == 0) {
    oled.setRotation(1);
  } else {
    if (filtered * scr_ori < thr * scr_ori){
      oled.setRotation(1);
    } else {
      oled.setRotation(0);
    }
  }

  // brightness
  
  if (scr_bri == 0) {
    oled.setContrast(128);;
  } else if (scr_bri == 1) {
    oled.setContrast((1023 - filtered) / 4);
  } else {
    oled.setContrast(filtered / 4);
  }
  
  if (cur_app == 'm') {
    menu();
    return;
  } else if (cur_app == 'a'){
    change_alpha();
    return;
  } else if (cur_app == 't'){
    change_thr();
    return;
  } else if (cur_app == 'f'){
    figure();
    return;
  }
}
