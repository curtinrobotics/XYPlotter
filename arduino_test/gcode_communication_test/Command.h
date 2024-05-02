/*
 * Command.h - Header file for Command.cpp
 */
#ifndef COMMAND_H
#define COMMAND_H

#define MAX_COMMAND_LEN 10  // Maximum number of arguments in a g-code command
#define MIN_G_COMMAND 0  // To be updated to be dynamic with gComannds enum
#define MAX_G_COMMAND 3
#define MIN_M_COMMAND 1001
#define MAX_M_COMMAND 1002

typedef enum gCommands
{
  /*
   * Enum for the types of g-codes and m-codes
   * m-code are offset by 1000 for easy conversion
   */
  G1 = 1,
  G2 = 2,
  G3 = 3,

  M1 = 1001,
  M2 = 1002
}gCommands;

class Command
{
  private:
    String commandString;
  public:
    gCommands gCode;  // Category of command
    int X;
    int Y;
    int Z;
    int A;
    int B;
    int C;

  public: Command(String inCommandString);
  public: int validateCommandString();
  private: int cmdSeparator(const String inCmdString, String* cmds);
  private: bool getArgumentParts(const String arg, char* argType, int* argValue);
};

#endif
