void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

#define INTMIN 0x8000

#define MIN_G_COMMAND 0
#define MAX_G_COMMAND 3
#define MIN_M_COMMAND 1001
#define MAX_M_COMMAND 1002
typedef enum gCommands
{
  G1 = 1,
  G2 = 2,
  G3 = 3,

  M1 = 1001,
  M2 = 1002
};

class Command
{
  private:
    String commandString;
  public:
    gCommands gCode; // Category of command
    int X;
    int Y;
    int Z;
    int A;
    int B;
    int C;

    Command(String inCommandString)
    {
      commandString = inCommandString;
      X = INTMIN;
      Y = INTMIN;
      Z = INTMIN;
      A = INTMIN;
      B = INTMIN;
      C = INTMIN;
    }

    int cmdSeparator(String * cmds, String inCmdString)
    {
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

    // Returns true if command string is valid
    bool validateCommandString()
    {
      bool isValid = true;
      String cmds[10];
      int cmdCount = cmdSeparator(cmds, commandString);

      String cmdIdString = cmds[0].substring(1, cmds[0].length());
      int cmdID = atoi(cmdIdString.c_str());
      if (cmdID == 0 && !( cmdIdString.equals("0") ||  cmdIdString.equals("00") || cmdIdString.equals("000"))) 
      {
        isValid = false;
      }

      // Get command type
      switch (cmds[0][0])
      {
        case 'G':
          if ( MIN_G_COMMAND <= cmdID && cmdID <=  MAX_G_COMMAND)
          {
            gCode = cmdID;
            // TODO: create list and check commang in list (check command is valid)
          }
          else
          {
            isValid = false;
          }
          break;

        case 'M':
          if ( MIN_M_COMMAND <= cmdID && cmdID <= MAX_M_COMMAND) 
          {
            gCode = 1000 + cmdID;
          }
          else
          {
            isValid = false;
          }
          break;

        default:
          isValid = false;
          break;
      }

      // Get command parameters
      for (int i = 1; i < cmdCount; i++)
      {
        String cmdValueString = cmds[i].substring(1, cmds[i].length());
        int cmdValue = atoi(cmdValueString.c_str());
        if (cmdValue == 0 && !( cmdValueString.equals("0") ||  cmdValueString.equals("00") || cmdValueString.equals("000"))) 
        {
          isValid = false;
        }

        switch (cmds[i][0])
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
            isValid = false;
            break;

        }
      }
      
      //caseTest(cmd[0]);
      return isValid;
    }
};

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.write("Hello World\n");
  String cmds[10];
  String str = Serial.readString();

  //int cmdSeparatorIndex = str.indexOf(' ');
  //String subStr = str.substring(0, cmdSeparatorIndex);

  if (!str.equals(""))
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
    Serial.println(cmdObj.Z == INTMIN);

    //free(cmd);
  } 
}
