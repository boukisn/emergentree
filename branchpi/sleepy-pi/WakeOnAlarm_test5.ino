// 
// Simple example showing how to set the RTC alarm pin to wake up the Arduino.
// Like an alarm clock the alarm is triggered at a particular time and 
// then the Arduino wakes up.
// 
// Note: this example doesn't wake up the RPi. For that add:
//
//     SleepyPi.enablePiPower(true);  
//
// after arduino wakeup. 
// 
// To test on the RPi without power cycling and using the Arduino IDE
// to view the debug messages, fit the Power Jumper or enable
// self-power
// 
// 

// **** INCLUDES *****
#include "SleepyPi2.h"
#include <Time.h>
#include <LowPower.h>
#include <PCF8523.h>
#include <Wire.h>

#define kBUTTON_POWEROFF_TIME_MS   2000
#define kBUTTON_FORCEOFF_TIME_MS   8000

#define kPI_CURRENT_THRESHOLD_MA   85

const char *monthName[12] = {
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
}; 

eTIMER_TIMEBASE  PeriodicTimer_Timebase     = eTB_MINUTE;   // e.g. Timebase set to seconds
uint8_t          PeriodicTimer_Value        = 1; 

const int LED_PIN = 13;
float supplyVoltage = 0.0;

// Globals
// ++++++++++++++++++++ Change me ++++++++++++++++++
uint8_t  WakeUp_StartHour     = 22;   // Hour in 24 hour clock
uint8_t  WakeUp_StartMinute   = 42.5;   // Minutes 
uint8_t  WakeUp_StartSecond   = 30;   // Minutes 
// ++++++++++++++++++++ End Change me ++++++++++++++++++

tmElements_t tm;

void alarm_isr()
{
    // Just a handler for the alarm interrupt.
    // You could do something here
}

void setup()
{
  // Configure "Standard" LED pin
  pinMode(LED_PIN, OUTPUT);		
  digitalWrite(LED_PIN,LOW);		// Switch off LED
  // initialize serial communication: In Arduino IDE use "Serial Monitor"
  Serial.begin(9600);
  Serial.println("Starting...");
  delay(50);

  
  SleepyPi.rtcInit(true);

  // Default the clock to the time this was compiled.
  // Comment out if the clock is set by other means
  // ...get the date and time the compiler was run
  if (getDate(__DATE__) && getTime(__TIME__)) {
      // and configure the RTC with this info
      SleepyPi.setTime(DateTime(F(__DATE__), F(__TIME__)));
  }  

  printTimeNow();
 
}

void loop() 
{
    SleepyPi.rtcClearInterrupts();
    // Allow wake up alarm to trigger interrupt on falling edge.
    attachInterrupt(0, alarm_isr, FALLING);
    
    SleepyPi.setTimer1(PeriodicTimer_Timebase, PeriodicTimer_Value);
    
    bool pi_running;

    
    // PrintRTCRegisters();   // for debug
    
    delay(500);

    // Enter power down state with ADC and BOD module disabled.
    // Wake up when wake up pin is low (which occurs when our alarm clock goes off)
    SleepyPi.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF); 
    
    // Disable external pin interrupt on wake up pin.
    detachInterrupt(0); 
    
    SleepyPi.ackTimer1();
    //SleepyPi.enablePiPower(false);
    
    supplyVoltage = SleepyPi.supplyVoltage();
    
    pi_running = SleepyPi.checkPiStatus(kPI_CURRENT_THRESHOLD_MA,false);
    if (pi_running ==false)
    {
      SleepyPi.enablePiPower(true);
      //SleepyPi.enableExtPower(true);
    }
    
    
    // Do something here
    // Example: Read sensor, data logging, data transmission.
    // Just a handler for the pin interrupt.
    digitalWrite(LED_PIN,HIGH);		// Switch on LED
    Serial.println("I've Just woken up on the Alarm!");
    Serial.println(supplyVoltage);
    printTimeNow();
    // Print the time
    DateTime now = SleepyPi.readTime();
    
    
    delay(30000);
    
    if((now.hour() == 6) && (now.minute() < 05))
    { 
      delay(10000);
      printTimeNow();
    }
    else if((now.hour() == 12) && (now.minute() < 05))
    { 
      delay(10000);
      printTimeNow();
    }
    else if((now.hour() == 18) && (now.minute() < 5))
    { 
      delay(10000);
      printTimeNow();
    }
    else if(now.hour() == 19) //&& (now.minute() < 05))
    { 
      delay(10000);
      printTimeNow();
    }
    pi_running = SleepyPi.checkPiStatus(kPI_CURRENT_THRESHOLD_MA,false);
    if (pi_running ==true)
    {
      digitalWrite(LED_PIN,LOW);
      SleepyPi.enablePiPower(false);
      //SleepyPi.enableExtPower(true);
    }
    else
    {
      digitalWrite(LED_PIN,LOW);
    }
     
    	// Switch off LED 
     
}

void printTimeNow()
{
    // Read the time
    DateTime now = SleepyPi.readTime();
    // Print out the time
    print2digits(now.hour());
    Serial.write(':');
    print2digits(now.minute());
    Serial.write('\n');

    return;
}
bool getTime(const char *str)
{
  int Hour, Min, Sec;

  if (sscanf(str, "%d:%d:%d", &Hour, &Min, &Sec) != 3) return false;
  tm.Hour = Hour;
  tm.Minute = Min;
  tm.Second = Sec;
  return true;
}

bool getDate(const char *str)
{
  char Month[12];
  int Day, Year;
  uint8_t monthIndex;

  if (sscanf(str, "%s %d %d", Month, &Day, &Year) != 3) return false;
  for (monthIndex = 0; monthIndex < 12; monthIndex++) {
    if (strcmp(Month, monthName[monthIndex]) == 0) break;
  }
  if (monthIndex >= 12) return false;
  tm.Day = Day;
  tm.Month = monthIndex + 1;
  tm.Year = CalendarYrToTm(Year);
  return true;
}

void print2digits(int number) {
  if (number >= 0 && number < 10) {
    Serial.write('0');
  }
  Serial.print(number);
}

void PrintRTCRegisters(void)
{
  
      // Debug
      uint8_t reg_value;
      reg_value = SleepyPi.rtcReadReg(PCF8523_CONTROL_1);
      Serial.print("Control 1: 0x");
      Serial.println(reg_value,HEX);
      reg_value = SleepyPi.rtcReadReg(PCF8523_CONTROL_2);
      Serial.print("Control 2: 0x");
      Serial.println(reg_value, HEX);      
      reg_value = SleepyPi.rtcReadReg(PCF8523_CONTROL_3);
      Serial.print("Control 3: 0x");
      Serial.println(reg_value,HEX); 
      
      reg_value = SleepyPi.rtcReadReg(PCF8523_SECONDS);
      Serial.print("Seconds: ");
      Serial.println(reg_value,HEX);
      reg_value = SleepyPi.rtcReadReg(PCF8523_MINUTES);
      Serial.print("Minutes: ");
      Serial.println(reg_value,HEX);  
      reg_value = SleepyPi.rtcReadReg(PCF8523_HOURS);
      Serial.print("Hours: ");
      Serial.println(reg_value,HEX);  
      reg_value = SleepyPi.rtcReadReg(PCF8523_DAYS);
      Serial.print("Days: ");
      Serial.println(reg_value,HEX);   
      reg_value = SleepyPi.rtcReadReg(PCF8523_WEEKDAYS);
      Serial.print("Week Days: ");
      Serial.println(reg_value,HEX);    
      reg_value = SleepyPi.rtcReadReg(PCF8523_MONTHS);
      Serial.print("Months: ");
      Serial.println(reg_value,HEX);  
      reg_value = SleepyPi.rtcReadReg(PCF8523_YEARS);
      Serial.print("Years: ");
      Serial.println(reg_value,HEX); 
      
      reg_value = SleepyPi.rtcReadReg(PCF8523_MINUTE_ALARM);
      Serial.print("Minute Alarm: ");
      Serial.println(reg_value,HEX);      
      reg_value = SleepyPi.rtcReadReg(PCF8523_HOUR_ALARM);
      Serial.print("Hour Alarm: ");
      Serial.println(reg_value,HEX);  
      reg_value = SleepyPi.rtcReadReg(PCF8523_DAY_ALARM);
      Serial.print("Day Alarm: ");
      Serial.println(reg_value,HEX);      
      reg_value = SleepyPi.rtcReadReg(PCF8523_WEEKDAY_ALARM);
      Serial.print("Weekday Alarm: ");
      Serial.println(reg_value,HEX); 
      
      reg_value = SleepyPi.rtcReadReg(PCF8523_OFFSET);
      Serial.print("Offset: 0x");
      Serial.println(reg_value,HEX); 
      reg_value = SleepyPi.rtcReadReg(PCF8523_TMR_CLKOUT_CTRL);
      Serial.print("TMR_CLKOUT_CTRL: 0x");
      Serial.println(reg_value,HEX);  
      reg_value = SleepyPi.rtcReadReg(PCF8523_TMR_A_FREQ_CTRL);
      Serial.print("TMR_A_FREQ_CTRL: 0x");
      Serial.println(reg_value,HEX); 
      reg_value = SleepyPi.rtcReadReg(PCF8523_TMR_A_REG);
      Serial.print("TMR_A_REG: 0x");
      Serial.println(reg_value,HEX);     
      reg_value = SleepyPi.rtcReadReg(PCF8523_TMR_B_FREQ_CTRL);
      Serial.print("TMR_B_FREQ_CTRL: 0x");
      Serial.println(reg_value,HEX);    
       reg_value = SleepyPi.rtcReadReg(PCF8523_TMR_B_REG);
      Serial.print("TMR_B_REG: 0x");
      Serial.println(reg_value,HEX);     
 
}

