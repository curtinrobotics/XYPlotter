/*
 * Command.cpp - Object to interpret g-code commands
 */

// Libraries
#include <Arduino.h>
#include "constants.h"
#include "Command.h"

Command::Command(String inCommandString)
{
  /*
   * Creates command object based on input command string
   * :param inCommandString: String to create command off
   * :return: Command object
   */
  commandString = inCommandString;
  commandString.trim();
  X = INTMIN;
  Y = INTMIN;
  Z = INTMIN;
  A = INTMIN;
  B = INTMIN;
  C = INTMIN;
}

int Command::validateCommandString()
{
  /*
   * Validates the command string given during construction, and assigns arguments to class fields
   * :return: Number of matched arguments in command
   */
  int argumentCount = 0;
  
  // Get commnd arguments
  String cmds[MAX_COMMAND_LEN];  
  int cmdCount = cmdSeparator(commandString, cmds);

  // Get command type
  char cmdType = ' ';
  int cmdId = -1;
  if( getArgumentParts(cmds[0], &cmdType, &cmdId) )
  {
    switch( cmds[0][0] )
    {
      case 'G':
        if( MIN_G_COMMAND <= cmdId && cmdId <=  MAX_G_COMMAND )
        {
          gCode = (gCommands)cmdId;
          // TODO: create list and check commang in list (check command is valid)
          argumentCount++;
        }
        break;

      case 'M':
        if( MIN_M_COMMAND <= cmdId && cmdId <= MAX_M_COMMAND )
        {
          gCode = (gCommands)(1000 + cmdId);
          argumentCount++;        
        }
        break;
    }
  }

  // Get command parameters
  if( argumentCount == 1 )
  {
    for( int i = 1; i < cmdCount; i++ )
    {
      char cmdType = ' ';
      int cmdValue = -1;
      if( getArgumentParts(cmds[i], &cmdType, &cmdValue) )
      {
        argumentCount++;  // Assume command match
        switch( cmds[i][0] )
        {
          case 'X':
            X = cmdValue;
            break;
          case 'Y':
            Y = cmdValue;
            break;
          case 'Z':
            Z = cmdValue;
            break;
          case 'A':
            A = cmdValue;
            break;
          case 'B':
            B = cmdValue;
            break;
          case 'C':
            C = cmdValue;
            break;
          default:
            argumentCount--;  // Decrement command count if no match
            break;
        }
      }
    }
  }

  return argumentCount;
}

int Command::cmdSeparator(const String inCmdString, String* cmds)
{
  /*
   * Seperates arguments on a command, storing the result in the input array
   * :param cmds: An array of strings that the arguments will be returned to
   * :param inCmdString: Input command string that will be split
   * :return: Count of arguments found
   */
  int curIndex = 0;
  int prevIndex = -1;

  int cmdCount = 0;
  while(curIndex != -1)
  {
    curIndex = inCmdString.indexOf(' ', curIndex+1);
    cmds[cmdCount] = inCmdString.substring(prevIndex + 1, curIndex);
    prevIndex = curIndex;
    cmdCount++;
  }
  return cmdCount;
}

bool Command::getArgumentParts(const String arg, char* argType, int* argValue)
{
  /*
   * Gets the type and value of a command argument
   * :param arg: The argument to parse
   * :param argType: Pointer to the returned argument type
   * :param argValue: Pointer to the returned argument value
   * :return: True if argument if valid
   */
  *argType = arg[0];
  String argValueString = arg.substring(1, arg.length());
  *argValue = atoi(argValueString.c_str());  
  if( *argValue == 0 && !( argValueString.equals(String("0")) || argValueString.equals(String("00")) || argValueString.equals(String("000")) ) )
  {
    return false;
  }
  return true;
}
