# hey there! this is work in progress
------------------------------------------------
passion project presented by who could it be wow its iconsalty or seomthing i dont know

--> the point of writing this is just to simulate a cpu of this vlie isa specifically, its not groundbreaking but its cool

(also the codes are probably poorly written please spare me)

--------------

# dependency
- pygame

-------------

# how to use

- open compiler.py
- go to line 93
- replace “file” with directory of your text asm code
- go to last line (line 187)
- replace “file” with the directory your compiled machine code will be saved at

then,

- open emu.py
- at line 12, replace file with directory of the saved compiled machine code

(debug mode at line 1 of emu.py. turn on for debug purposes, most time)



# here is the list of instructions it supports currently (mostly tested)

0x0: nop, hlt, sez, clz, sec, clc, cmc, clf

0x1: psh, pop, sic, sdc, trs, tsr, php, plp, rsp, csp, clr

0x2: add, sub, inc, dec

0x3: cmp, cmn, tst, teq

0x4: ior, nor, xor, xnr, and, nad

0x5: lsl, lsr, rol, ror, sar, flp, pct

0x6: mul, iml, muh, imh

0x7: div, idv, mod, imd

0x8: ldi

0x9: mov, mar

0xA: ldr, str

0xB: rlj

0xC: jmp

0xD: cal, ret

0xE: inp, out

0xF: sei, cli, wfi (partially)

-------------------

# formatting, syntax

0x0: [4 bit opcode] [3 bit ext opcode] [9 bit padding]

0x1: for PUSH, POP, TXS, TSX, RJSP: [4 bit opcode] [4 bit ext opcode] [4 bit padding] [4 bit reg]

0x2: [4 bit opcode] [2 bit ext opcode] [2 bit padding] [4b reg src/dest] [4b reg src2]

0x3: [4 bit opcode] [2 bit ext opcode] [2 bit padding] [4b reg src/dest] [4b reg src2]

0x4: [4 bit opcode] [3 bit ext opcode] [1 bit padding] [4b reg src/dest] [4b reg src2]

0x5: for LSL LSR ROL ROR SAR: [4 bit opcode] [3 bit ext opcode] [1 bit padding] [4b reg src/des] [4b reg src2] ; for FLP POPCNT [4 bit opcode] [3 bit ext opcode] [5 bit padding] [4b reg src/dest]

0x6: [4 bit opcode] [2 bit ext opcode] [2 bit padding] [4b reg src/dest] [4b reg src2]

0x7: [4 bit opcode] [2 bit ext opcode] [2 bit padding] [4b reg src/dest] [4b reg src2]

0x8: [4 bit opcode] [4b reg] [8 bit immediate]

0x9: for MOV: [4 bit opcode] [1 bit ext opcode] [3 bit padding] [4b reg dest] [4b reg src] ; for MRA: [4 bit opcode] [1 bit ext opcode] [7 bit offset] [4b reg src]

0xA:  [4 bit opcode] [1 bit ext opcode] [7 bit offset] [4b reg dest/src]

0xB: [4 bit opcode]  [4 bit condition] [8 bit address]

0xC: [4 bit opcode] [4 bit condition] [8 bit address]

0xD: for CAL: [4 bit opcode] [1 bit ext opcode] [1 bit padding] [2b bank address] [8 bit address]

0xE: [4 bit opcode] [1 bit ext opcode] [4b port address] [4b reg dest/src]

0xF: for SEI, CLI, IRT, WFI [4 bit opcode] [3 bit ext opcode] [9 bit padding] ; for INT [4 bit opcode] [3 bit ext opcode] [5 bit padding] [4 bit vector]


--------------

# note!
- i have wrote a basic program to demonstrate how to use, check out program.txt

-------------------

# changelog (version 11)
- added pygame functionality (dependency)
- customizable clock speed with multiplier
- real-time registers values
- native taskbar icon (windows appusermodelid)
- relative directory
- added icon.png (temporary)