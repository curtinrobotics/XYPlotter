//Also assume CW is forward, ACW is backward
//Also assume BOTH will run at the EXACT SAME TIME as written

//Should Draw a square -> that is move:
//60 units RIGHT, wait 1 sec; 
//move 60 UP, wait 1 sec;
//move 60 LEFT, wait 1 sec;
//move 60 DOWN, wait 1 sec;




//make ARRAY work
//also make servos work




#include <AFMotor.h>
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

void setup() {
  Serial.begin(115200);
  
motor1.setSpeed(100);
motor2.setSpeed(100);

}

void loop() {
  
  motorStep(60, 60); //RIGHT
  delay(1000);
  
  motorStep(60, -60); //UP
  delay(1000);
  
  motorStep(-60, -60); //LEFT
  delay(1000);
  
  motorStep(-60, 60); //DOWN
  delay(1000);
  
  delay(5000);

}

void motorStep(int aStepNum, int bStepNum)
{
  int maxStep = max(abs(aStepNum), abs(bStepNum));
  float aPos = 0;
  float bPos = 0;
  float aStep = (float)aStepNum/maxStep;
  float bStep = (float)bStepNum/maxStep;
  int aActualPos = 0;
  int bActualPos = 0;
  for( int i=0; i<maxStep; i++ )
  {
    aPos = aStep*i;
    bPos = bStep*i;
    int aMove = round(aPos) - aActualPos;
    int bMove = round(bPos) - bActualPos;
    Serial.println(aMove);
    Serial.println(bMove);
    
    if( aMove > 0 )
    {
      motor1.step(aMove, FORWARD, SINGLE);
    }
    else
    {
      motor1.step(abs(aMove), BACKWARD, SINGLE);
    }
    
    if( bMove > 0 )
    {
      motor2.step(bMove, FORWARD, SINGLE);
      Serial.println("Test1");
    }
    else
    {
      motor2.step(abs(bMove), BACKWARD, SINGLE);
      Serial.println("Test2");
    }

    aActualPos += aMove;
    bActualPos += bMove;
    
  }
}
