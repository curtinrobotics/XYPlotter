/*
 * gcode_communicaiton_test.ino - testing communication between Arduino and computer with gcode
 */

// Libraries
#include "Command.h"

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Program Start!\n");
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.write("Hello World\n");
  String str = Serial.readString();

  //int cmdSeparatorIndex = str.indexOf(' ');
  //String subStr = str.substring(0, cmdSeparatorIndex);

  if( !str.equals("") )
  {
    //Serial.write(str.c_str());
    //char* cmd = (char*) malloc(sizeof(char) * (cmdSeparatorIndex - 1));
    //int cmdCount = cmdSeparator(cmds, str);
    //for (int i = 0; i < )

    //Serial.write(subStr.c_str());
    //for (int i = 0; i < cmdCount; i++)
    //{
    //  Serial.println(cmds[i].c_str());
    //}

    //Serial.println(cmdCount);

    Command cmdObj(str);

    Serial.println(cmdObj.validateCommandString());
    Serial.println(cmdObj.X);
    Serial.println(cmdObj.Y);
    Serial.println(cmdObj.Z);
    Serial.println();

    //free(cmd);
  } 
}
