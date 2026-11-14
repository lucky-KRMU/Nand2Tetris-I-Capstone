// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/Memory.tst

load Memory.hdl,
output-file Memory.out,
compare-to Memory.cmp,
output-list time%S1.4.1 in%D1.6.1 load%B2.1.2 address%B1.15.1 out%D1.6.1;

// Initial values
set in -1,
set load 0,
set address 0,
eval,
output;

tick,
tock,
output;

// Test RAM[0] = 333
set in 333,
set load 1,
set address 0,
eval,
output;

tick,
tock,
output;

// Read RAM[0]
set in -1,
set load 0,
set address 0,
eval,
output;

tick,
tock,
output;

// Test RAM[16383] = 444
set in 444,
set load 1,
set address 16383,
eval,
output;

tick,
tock,
output;

// Read RAM[16383]
set in -1,
set load 0,
set address 16383,
eval,
output;

tick,
tock,
output;

// Test Screen[0] = 555 (address 16384)
set in 555,
set load 1,
set address 16384,
eval,
output;

tick,
tock,
output;

// Read Screen[0]
set in -1,
set load 0,
set address 16384,
eval,
output;

tick,
tock,
output;

// Test Screen[8191] = 666 (address 24575)
set in 666,
set load 1,
set address 24575,
eval,
output;

tick,
tock,
output;

// Read Screen[8191]
set in -1,
set load 0,
set address 24575,
eval,
output;

tick,
tock,
output;

// Test Keyboard (address 24576)
// Note: cannot write to keyboard
set in 777,
set load 1,
set address 24576,
eval,
output;

tick,
tock,
output;

// Read Keyboard
set in -1,
set load 0,
set address 24576,
eval,
output;

tick,
tock,
output;
