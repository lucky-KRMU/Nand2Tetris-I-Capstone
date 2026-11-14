// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/CPU.tst

load CPU.hdl,
output-file CPU.out,
compare-to CPU.cmp,
output-list time%S1.4.1 inM%D1.6.1 instruction%B1.16.1 reset%B2.1.2 outM%D1.6.1 writeM%B2.1.2 addressM%D1.5.1 pc%D1.5.1;

// Initialize
set inM 0,
set reset 0,
set instruction %B0000000000000000,
tick, tock, output;

// A-instruction: @12345
set instruction %B0011000000111001,
tick, tock, output;

// D = A
set instruction %B1110110000010000,
tick, tock, output;

// A-instruction: @23456
set instruction %B0101101110100000,
tick, tock, output;

// D = D - A
set instruction %B1110010011010000,
tick, tock, output;

// A-instruction: @1000
set instruction %B0000001111101000,
tick, tock, output;

// M = D
set instruction %B1110001100001000,
tick, tock, output;

// D = M (inM = -12345)
set inM -12345,
set instruction %B1111110000010000,
tick, tock, output;

// Reset PC
set reset 1,
tick, tock, output;

// Release reset
set reset 0,
set instruction %B0000000000000001,
tick, tock, output;

// Jump test: D;JGT (D is negative, should not jump)
set instruction %B1110001100000001,
tick, tock, output;

// Jump test: D;JLT (D is negative, should jump to A=1)
set instruction %B1110001100000100,
tick, tock, output;

// Next instruction after jump
set instruction %B0000000000000010,
tick, tock, output;
