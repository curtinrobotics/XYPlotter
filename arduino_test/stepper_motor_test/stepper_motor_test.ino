int test_pin = 13;
int in1 = 2;
int in2 = 3;
int in3 = 4;
int in4 = 5;
float step_time;

void setup()
{
  Serial.begin(9600);
  pinMode(test_pin, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}

void loop()
{
  pulse(330, 1.0);
  pulse(294, 1.0);
  pulse(262, 1.0);
}

void pulse(float frequency, float duration)
{
  step_time = (1 / frequency) * 1000000;
  while(duration > 0)
  {
    digitalWrite(in1, HIGH);
    delayMicroseconds(step_time);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    delayMicroseconds(step_time);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    delayMicroseconds(step_time);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delayMicroseconds(step_time);
    digitalWrite(in4, LOW);
    duration -= (step_time/1000000)*4;
  }
}
