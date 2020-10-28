// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//8191

//fill the screen
@SCREEN
D = A
@8191
D = D + A
@maxaddress
M = D

(STOP)
@i
M = 0
@KBD
D = M
@PRESSED
D; JGT
@UNPRESSED
D; JEQ
@STOP
0; JMP


(PRESSED)
@SCREEN
D = A
@i
A = D + M
M = -1
D = A
@maxaddress
D = M - D
@STOP
D; JEQ
@i
M = M + 1
@PRESSED
0; JMP

(UNPRESSED)
@SCREEN
D = A
@i
A = D + M
M = 0
D = A
@maxaddress
D = M - D
@STOP
D; JEQ
@i
M = M + 1
@UNPRESSED
0; JMP