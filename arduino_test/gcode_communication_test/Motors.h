/*
 * Motor.h - Header file for Motors.cpp
 */
#ifndef MOTORS_H
#define MOTORS_H

#include <AFMotor.h>

#define STEPPER_MOTOR_SPEED 100  // Arbitrary number on speed (higher is faster)

class Motors
{
  private:
    AF_Stepper* motorA;  // Motors
    AF_Stepper* motorB;
    int x;  // Position of motors
    int y;
    int z;
  public:

  public: Motors();
  public: ~Motors();
  public: void move(int inX, int inY, int inZ);
  private: void moveSteps(int aStepNum, int bStepNum);
};

#endif
