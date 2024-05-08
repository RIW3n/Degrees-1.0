int p_w_m = 1000;
int p_w_ms = 1020;
int pwtrl = 220;
int pwmrl = 1000;
int pwmrls = 1035;
int fl_1 = 31;
int fl_2 = 33;
int bl_3 = 35;
int bl_4 = 37;
int l_ena = 8;
int l_enb = 9;

int fr_1 = 39;
int fr_2 = 41;
int br_3 = 43;
int br_4 = 45;
int r_ena = 10;
int r_enb = 11;


int vcc_1 = 22;
int gnd_1 = 24;
int vcc_2 = 36;
int gnd_2 = 38;
int vcc_3 = 28;
int gnd_3 = 30;
int vcc_4 = 32;
int gnd_4 = 34;

volatile float dr = 0.0000;
volatile float dl = 0.0000;


float wd = 59.00000;
float mc = 9.700000;

float d = 0.00000;
float tita = 0.0;
float x = 0.0;
float y = 0.0;
float theta = 0.0;


int tot_no_rev = 660;


const int fl_c1 = 21;
const int fl_c2 = 4;

const int fr_c1 = 19;
const int fr_c2 = 7;

const int bl_c1 = 2;
const int bl_c2 = 5;

const int br_c1 = 3;
const int br_c2 = 6;



void setup() {
  // put your setup code here, to run once:
   pinMode(fl_1, OUTPUT);
   pinMode(fl_2, OUTPUT);
   pinMode(bl_3,OUTPUT);
   pinMode(bl_4, OUTPUT);
   pinMode(l_ena, OUTPUT);
   pinMode(l_enb,OUTPUT);


   pinMode(fr_1, OUTPUT);
   pinMode(fr_2, OUTPUT);
   pinMode(br_3,OUTPUT);
   pinMode(br_4, OUTPUT);
   pinMode(r_ena, OUTPUT);
   pinMode(r_enb,OUTPUT);

   Serial.begin(9600);
   
    pinMode(vcc_1,OUTPUT);
    pinMode(gnd_1,OUTPUT);
    pinMode(vcc_2,OUTPUT);
    pinMode(gnd_2,OUTPUT);
    pinMode(vcc_3,OUTPUT);
    pinMode(gnd_3,OUTPUT);
    pinMode(vcc_4,OUTPUT);
    pinMode(gnd_4,OUTPUT);

    pinMode(bl_c1, INPUT);
    pinMode(br_c2, INPUT);
    pinMode(br_c1, INPUT);
    pinMode(bl_c2, INPUT);

    digitalWrite(vcc_1,HIGH);
    digitalWrite(gnd_1,LOW);
    digitalWrite(vcc_2,HIGH);
    digitalWrite(gnd_2,LOW);
    digitalWrite(vcc_3,HIGH);
    digitalWrite(gnd_3,LOW);
    digitalWrite(vcc_4,HIGH);
    digitalWrite(gnd_4,LOW);

    
    
   attachInterrupt(digitalPinToInterrupt(bl_c1), dltick, CHANGE);
   attachInterrupt(digitalPinToInterrupt(br_c1), drtick, CHANGE);
  
   
}

void loop() {
  // put your main code here, to run repeatedly
  localize();
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(theta);
if (Serial.available() > 0) {
    
    char command = Serial.read();
    executeCommand(command);
  }
}

void executeCommand(char command) {
  switch (command) {
    case 'F':
      move_forward();
      break;
    case 'B':
      move_backward();
      break;
    case 'L':
      move_left();
      break;
    case 'U':
      turnleft();
      break;
    case 'W':
      turnright();
      break;
    case 'R':
      move_right();
      break;
    case 'S':
      stop_mec();
      break;
    default:
      stop_mec();
  }

}

void move_forward(){
  analogWrite(l_ena, p_w_m);
  analogWrite(l_enb, p_w_m);
  digitalWrite(fl_1,LOW);
  digitalWrite(fl_2, HIGH);
  
  digitalWrite(bl_3,HIGH);
  digitalWrite(bl_4, LOW);



  analogWrite(r_ena, p_w_m);
  analogWrite(r_enb, p_w_m);
  digitalWrite(fr_1,LOW);
  digitalWrite(fr_2, HIGH);
  
  digitalWrite(br_3,HIGH);
  digitalWrite(br_4, LOW);
  
}

void move_backward(){
  analogWrite(l_ena, p_w_ms);
  analogWrite(l_enb, p_w_m);
  digitalWrite(fl_1,HIGH);
  digitalWrite(fl_2, LOW);
  
  digitalWrite(bl_3,LOW);
  digitalWrite(bl_4, HIGH);



  analogWrite(r_ena, p_w_m);
  analogWrite(r_enb, p_w_m);
  digitalWrite(fr_1,HIGH);
  digitalWrite(fr_2, LOW);
  
  digitalWrite(br_3,LOW);
  digitalWrite(br_4, HIGH);
  
}

void move_right(){
  analogWrite(l_ena, pwmrls);
  analogWrite(l_enb, pwmrl);
  digitalWrite(fl_1,HIGH);
  digitalWrite(fl_2, LOW);
  
  digitalWrite(bl_3,HIGH);
  digitalWrite(bl_4, LOW);



  analogWrite(r_ena, pwmrl);
  analogWrite(r_enb, pwmrl);
  digitalWrite(fr_1,HIGH);
  digitalWrite(fr_2, LOW);
  
  digitalWrite(br_3,HIGH);
  digitalWrite(br_4, LOW);
  
}


void move_left(){
  analogWrite(l_ena, pwmrls);
  analogWrite(l_enb, pwmrl);
  digitalWrite(fl_1,LOW);
  digitalWrite(fl_2, HIGH);
  
  digitalWrite(bl_3,LOW);
  digitalWrite(bl_4, HIGH);



  analogWrite(r_ena, pwmrl);
  analogWrite(r_enb, pwmrl);
  digitalWrite(fr_1,LOW);
  digitalWrite(fr_2, HIGH);
  
  digitalWrite(br_3,LOW);
  digitalWrite(br_4, HIGH);
  
}


void stop_mec(){
  analogWrite(l_ena, 100);
  analogWrite(l_enb, 100);
  digitalWrite(fl_1,LOW);
  digitalWrite(fl_2, LOW);
  
  digitalWrite(bl_3,LOW);
  digitalWrite(bl_4, LOW);



  analogWrite(r_ena, 100);
  analogWrite(r_enb, 100);
  digitalWrite(fr_1,LOW);
  digitalWrite(fr_2, LOW);
  
  digitalWrite(br_3,LOW);
  digitalWrite(br_4, LOW);
  
}

void dltick() {
  if (digitalRead(bl_c1) == digitalRead(bl_c2)) {
   
  
    dl += 0.07262384;
  } else {
    dl -= 0.07262384;
  }
}

void drtick() {
  if (digitalRead(br_c1) == digitalRead(br_c2)) {
    dr -= 0.046172;
  } else {
    dr += 0.046172;
  }
}

void localize (){


d = (dr+dl)/2;
tita = (dr-dl)/wd;
theta += tita;
x = x + d*sin(theta);
y = y + d*cos(theta);

dr = 0;
dl = 0;
Serial.print(x);
Serial.print(",");
Serial.print(y);
Serial.print(",");
Serial.println(theta);
}


void test(){
  
  analogWrite(l_ena,200);
  analogWrite(l_enb,200);
  digitalWrite(fl_1,HIGH);
  digitalWrite(fl_2,LOW);
}

void test2(){
  analogWrite(l_enb,100);
  analogWrite(l_ena,100);
  digitalWrite(bl_3,HIGH);
  digitalWrite(bl_4,LOW);
}

void test3(){
  analogWrite(r_ena, 200);
  analogWrite(r_enb, 200);

  digitalWrite(br_3,HIGH);
  digitalWrite(br_4,LOW);
}

void turnright() {
  analogWrite(l_enb,pwtrl);
  analogWrite(l_ena,pwtrl);
  digitalWrite(bl_3,HIGH);
  digitalWrite(bl_4,LOW);

  analogWrite(r_ena, pwtrl);
  analogWrite(r_enb, pwtrl);
  digitalWrite(fr_1,HIGH);
  digitalWrite(fr_2, LOW);

  
}

void turnleft() {
  analogWrite(l_enb,pwtrl);
  analogWrite(l_ena,pwtrl);
  digitalWrite(bl_3,LOW);
  digitalWrite(bl_4,HIGH);

  analogWrite(r_ena, pwtrl);
  analogWrite(r_enb, pwtrl);
  digitalWrite(fr_1,LOW);
  digitalWrite(fr_2, HIGH);

  
}