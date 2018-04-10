/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include "PongGame.h"
#include "LEDMatrix.h"

using namespace std;
using namespace hw4;

const int nrow = 8;
const int ncol = 8;
unsigned long prevMilli=0;
PongGame pongGame(nrow, ncol);
int* buffer = new int[nrow*ncol];

LEDMatrix ledMat(2,3,4,5);
/***********CHANGE THESE*********************/



void setup(){
    pongGame.start(millis());
    pinMode(8, INPUT);
    pinMode(9, INPUT);
    pinMode(10, INPUT);
    pinMode(11, INPUT);
    pinMode(12, INPUT);
    Serial.begin(9600);
}

void drawScreen(int* buffer){
    int tem[8] = {
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000
    };
    for(int irow=0; irow<nrow; irow++){
        int toMove =7;
        for(int icol=0; icol<ncol; icol++){
            int buff = buffer[irow*ncol + icol];
          
            if(buff==0){
              tem[irow] = tem[irow] | (0<<toMove);
            } else{
              tem[irow]  = tem[irow] | (1<<toMove);
            }

            toMove=toMove-1;

        }
    }
    ledMat.writeData(tem);
}

char getInput(){
    int reset = digitalRead(8);
    int _1upKey = digitalRead(11);
    int _1downKey = digitalRead(12);
    int _2upKey = digitalRead(9);
    int _2downKey = digitalRead(10);
//    Serial.println("GETINPUT");
    if(reset){
      Serial.println("reset");
      return ' ';
    }
    else if (_1upKey){
      Serial.println("player1 Goes Up");
      return 'a';
    }
    else if (_1downKey){
      Serial.println("Player1 Goes down");
      return 'b';
    }
    else if (_2upKey){
      Serial.println("Player2 Goes Up");
      return 'c';
    }
    else if (_2downKey){
      Serial.println("Player 2 Goes Down");
      return 'd';
    }
    else{
      return 'q';
    }
}

void processInput(unsigned long tick){ //You will need to change this
    if(tick -prevMilli >70){
        
        char ch=getInput();
        prevMilli=tick;
 
        switch(ch){
            case 'a':
              
                pongGame.movePad(Player::PLAYER_ONE, PadDirection::UP);
                
                break;
            case 'b':
                pongGame.movePad(Player::PLAYER_ONE, PadDirection::DOWN);
                break;
            case ' ':
                pongGame.reset();
                pongGame.start(tick);
                break;
            case 'c':
                pongGame.movePad(Player::PLAYER_TWO, PadDirection::UP);
                break;
            case 'd':
                pongGame.movePad(Player::PLAYER_TWO, PadDirection::DOWN);
                break;
            case 'q':
                break;
            }
            
    }
}

void loop(){
    const unsigned long tick = millis();
    processInput(tick);
    pongGame.update(tick);
    ledMat.update();
    if(pongGame.isDirty()){


        pongGame.paint(buffer);
        drawScreen(buffer);
    }
    
}




