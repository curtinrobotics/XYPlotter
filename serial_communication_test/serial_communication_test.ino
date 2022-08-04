int test_pin = 13;
String msg = ""; 
String serialInputMsg = "";
String serialInputChar = "";

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(test_pin, OUTPUT);
}

void loop()
{
    while( !Serial.available() );
    msg = serialRead();
    if( msg == "on" )
    {
        digitalWrite(test_pin, HIGH);
    }
    else if( msg == "off")
    {
        digitalWrite(test_pin, LOW);
    }
}

String serialRead()
{
    serialInputMsg = "";
    do
    {
        serialInputChar = Serial.readString();
        serialInputMsg = serialInputMsg + serialInputChar;
    }while( serialInputChar != "" );
    Serial.print("Message revived: ");
    Serial.println(serialInputMsg);
    return serialInputMsg;
}