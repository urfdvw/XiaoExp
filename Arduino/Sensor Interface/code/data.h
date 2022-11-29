#define READ 1
#define VOL 2
#define REG_R 3
#define R_1K 4
#define R_10K 5
#define R_1M 6
#define R_10M 7
#define SEN_R 8
#define PHY 9
#define SCR_ORI 11
#define SCR_FIX 12
#define SCR_UP 13
#define SCR_DO 14
#define BRI_FIX 16
#define BRI_POS 17
#define BRI_INV 18
#define ALM_RE 20
#define ALM_THR 21
#define ALM_IF 22
#define ALM_F 23
#define ALM_LT 24
#define ALM_GT 25
#define ALM_ELSE 27
#define ALM_NTH 28
#define ALM_STP 29
#define TEMP_DISP 31
#define TEMP_CLB0 32
#define TEMP_CLB100 33
#define ALPHA 35
#define READ_RAW 36
#define READ_FLT 37
#define VOL_GRA 39
const char str_0[] PROGMEM = ""; //0
const char str_1[] PROGMEM = ""; //1
const char str_2[] PROGMEM = "VOLTAGE:"; //2
const char str_3[] PROGMEM = "REF R:"; //3
const char str_4[] PROGMEM = "1K"; //4
const char str_5[] PROGMEM = "10K"; //5
const char str_6[] PROGMEM = "1M"; //6
const char str_7[] PROGMEM = "10M"; //7
const char str_8[] PROGMEM = "SENSOR R:"; //8
const char str_9[] PROGMEM = ""; //9
const char str_10[] PROGMEM = "SETTINGS"; //10
const char str_11[] PROGMEM = "SCREEN ORIENTATION"; //11
const char str_12[] PROGMEM = "FIXED"; //12
const char str_13[] PROGMEM = "SENSE UP"; //13
const char str_14[] PROGMEM = "SENSE DOWN"; //14
const char str_15[] PROGMEM = "SCREEN BRIGHTNESS"; //15
const char str_16[] PROGMEM = "FIXED"; //16
const char str_17[] PROGMEM = "POS. RELATED"; //17
const char str_18[] PROGMEM = "INV. RELATED"; //18
const char str_19[] PROGMEM = "ALARM"; //19
const char str_20[] PROGMEM = "READING:"; //20
const char str_21[] PROGMEM = "THR="; //21
const char str_22[] PROGMEM = "IF:"; //22
const char str_23[] PROGMEM = "FALSE"; //23
const char str_24[] PROGMEM = "READING<THR"; //24
const char str_25[] PROGMEM = "READING>THR"; //25
const char str_26[] PROGMEM = "THEN:ALARM ON"; //26
const char str_27[] PROGMEM = "ELSE:"; //27
const char str_28[] PROGMEM = "NOTHING"; //28
const char str_29[] PROGMEM = "ALARM OFF"; //29
const char str_30[] PROGMEM = "TEMPERATURE"; //30
const char str_31[] PROGMEM = "TOGGLE DISPLAY"; //31
const char str_32[] PROGMEM = "CALIBRATE 0C"; //32
const char str_33[] PROGMEM = "CALIBRATE 100C"; //33
const char str_34[] PROGMEM = "AVERAGE"; //34
const char str_35[] PROGMEM = "NUM OF SAMPLES:"; //35
const char str_36[] PROGMEM = "RAW:"; //36
const char str_37[] PROGMEM = "AVERAGED:"; //37
const char str_38[] PROGMEM = "EXTRA"; //38
const char str_39[] PROGMEM = "VOLTAGE GRAPH"; //39
const char *const text[] PROGMEM = {str_0, str_1, str_2, str_3, str_4, str_5, str_6, str_7, str_8, str_9, str_10, str_11, str_12, str_13, str_14, str_15, str_16, str_17, str_18, str_19, str_20, str_21, str_22, str_23, str_24, str_25, str_26, str_27, str_28, str_29, str_30, str_31, str_32, str_33, str_34, str_35, str_36, str_37, str_38, str_39};
const uint8_t next_data[] PROGMEM = {0, 2, 3, 8, 5, 6, 7, 0, 9, 10, 38, 15, 13, 14, 0, 19, 17, 18, 0, 30, 21, 22, 26, 24, 25, 0, 27, 0, 29, 0, 34, 32, 33, 0, 0, 36, 37, 0, 0, 0};
const uint8_t previous_data[] PROGMEM = {0, 0, 1, 2, 0, 4, 5, 6, 3, 8, 9, 0, 0, 12, 13, 11, 0, 16, 17, 15, 0, 20, 21, 0, 23, 24, 22, 26, 0, 28, 19, 0, 31, 32, 30, 0, 35, 36, 10, 0};
const uint8_t parent_data[] PROGMEM = {0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 10, 11, 11, 11, 10, 15, 15, 15, 10, 19, 19, 19, 22, 22, 22, 19, 19, 27, 27, 10, 30, 30, 30, 10, 34, 34, 34, 0, 38};
const uint8_t child_data[] PROGMEM = {0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 0, 16, 0, 0, 0, 20, 0, 0, 23, 0, 0, 0, 0, 28, 0, 0, 31, 0, 0, 0, 35, 0, 0, 0, 39, 0};
char buffer[ 18 ];