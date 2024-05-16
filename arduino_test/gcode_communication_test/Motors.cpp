/*
 * Motors.cpp - Object to move stepper/server motors
 */

// Libraries
#include <Arduino.h>
#include <AFMotor.h>
#include "constants.h"
#include "Motors.h"

Motors::Motors()
{
  motorA = new AF_Stepper(200, 1);
  motorB = new AF_Stepper(200, 2);
  motorA->setSpeed(STEPPER_MOTOR_SPEED);
  motorB->setSpeed(STEPPER_MOTOR_SPEED);
  x = 0;
  y = 0;
  z = 0;
}

Motors::~Motors()
{
  free(motorA);
  free(motorB);
}

void Motors::move(int inX, int inY, int inZ)
{
  /*
   * Moves the gantry and head to specified absolute position (set value to INTMIN to ignore)
   * :param inX: The x position to move to
   * :param inY: The y position to move to
   * :param inZ: The z position to move to
   * :return: void
   */
  // Get the next position to move head to
  int nextX = x;
  int nextY = y;
  int nextZ = z;
  if( inX != INTMIN)
  {
    nextX = inX;
  }
  if( inY != INTMIN)
  {
    nextY = inY;
  }
  if( inZ != INTMIN )
  {
    nextZ = inZ;
  }

  // Get the relative move amount
  int relativeX = nextX - x;
  int relativeY = nextY - y;
  int relativeZ = nextZ - z;

  // Get stepper motors movement (x and y to a and b)
  int moveA = 0;
  int moveB = 0;
  // Positive X -> right
  moveA += relativeX;
  moveB += relativeX;
  // Positive Y -> forward
  moveA += relativeY;
  moveB -= relativeY;

  // Move motors
  // TODO add server motor (z) movement
  moveSteps(moveA, moveB);

  // Update motor positon
  x = nextX;
  y = nextY;
  z = nextZ;
}

void Motors::moveSteps(int aStepNum, int bStepNum)
{
  /*
   * Moves the stepper motors a and b by step number amount
   * :param aStemNum: Count to move stepper motor a by
   * :param aStemNum: Count to move stepper motor a by
   * :return: void
   */
  int maxStep = max(abs(aStepNum), abs(bStepNum));
  float aPos = 0;
  float bPos = 0;
  float aStep = (float)aStepNum/maxStep;
  float bStep = (float)bStepNum/maxStep;
  int aActualPos = 0;
  int bActualPos = 0;
  AF_Stepper motorALocal = *motorA;
  AF_Stepper motorBLocal = *motorB;
  for( int i=0; i<maxStep; i++ )
  {
    aPos = aStep*i;
    bPos = bStep*i;
    int aMove = round(aPos) - aActualPos;
    int bMove = round(bPos) - bActualPos;
    
    if( aMove > 0 )
    {
      motorALocal.step(aMove, FORWARD, SINGLE);
    }
    else
    {
      motorALocal.step(abs(aMove), BACKWARD, SINGLE);
    }
    
    if( bMove > 0 )
    {
      motorBLocal.step(bMove, FORWARD, SINGLE);
    }
    else
    {
      motorBLocal.step(abs(bMove), BACKWARD, SINGLE);
    }

    aActualPos += aMove;
    bActualPos += bMove;
  }
}



