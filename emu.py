import time # not used yet just there for the fun

# m0 = addition; m1 = subtraction; m2 = bitwise; m3,4,5 shifts; m6,7 mul imul; m8 div

# subopcode spaces
ext3=[0x0, 0x4, 0x5, 0xF]
ext2=[0x2, 0x3, 0x6, 0x7]
ext1=[0x9, 0xA, 0xE, 0xD]

with open("directory of this isa formatted machine code here", "r") as file: # read from directory that have machine codes (compile it using the other one)
    mcode = [int(line, 2) for line in file.read().splitlines() if line]

pc = 0
registers = [0] * 16
ram = [0] * 256

dstack = []
dsp = 0

cstack = []
csp = 0

status = { # flags!!!!!!!!!!!!!!!
    "z": 0,
    "c": 0,
    "n": 0,
    "v": 0,
    "s": 0,
    "m": 0,
    "q": 0,
    "id": 0
}

                        #functions (fancy)

# general functions for multiplication and division

def gcalc(a, b, m):
    if m == 0: # sign calculation
        if a >= 128:
            cS = 1
        else:
            cS = 0
        if b >= 128:
            pS = 1
        else:
            pS = 0
        return(cS ^ pS)
    if m == 1: # abs
        if a >= 128:
            return(~a + 1) & 0xff
        else: return a
    if m == 2: # unconditional flip
        return(~a + 1) & 0xff


# flag functions down below

def overflow(result, a, b, m):
    if m == 0:
        return(((~(a ^ b) & (a ^ result)) & 0x80) >> 7)
    elif m == 1:
        return((((a ^ b) & (a ^ result)) & 0x80) >> 7)
    elif m == 8:
        if a == 0x80 & b == 0xff:
            return 1
        else: return 0
    elif m in (2,3,4,5):
        return 0

def negative(result, m):
    if m in (0,1,2,3,4,5):
        return((result & 0x80) >> 7)

def carry(raw, result, a, b, m):
    if m == 0:
        return ((a + b) & 0x100) >> 8
    elif m == 1:
        return (((a + ~b) + 1) & 0x100) >> 8
    elif m == 2:
        return 0

    #shifts
    elif m == 3:
        return (raw >> 8) & 1
    elif m == 4:
        if result != 0:
            ctemp = (a & (1 << (result - 1)))
            if ctemp == 0:
                return 0
            else:return 1
        else: return 0
    elif m == 5:
        shiftsT = b & 0x7
        if shiftsT !=0:
            return (result >> 7) & 1
        else:return 0
    else:return 0

def zero(result, a, m):
    if m != 7:
        return 1 if (result & 0xff)==0 else 0
    else: return 1 if (a & 0xff)==0 else 0

def sign(result, a, b, m):
    if m in (0,1):
        ovfR = overflow(result, a, b, m)
        neg = negative(result)
        return (ovfR ^ neg)
    elif m in (2,3,4,5,6,7,8):
        return 0

def mul(raw, result, m):
    if m in (0,1,2,3,4,5,8):
        return 0
    elif m == 6:
        if (raw >> 8) !=0:
            return 1
        else:
            return 0

    elif m == 7:
        p8U = (result & 0xff00) >> 8
        p8MSB = (result & 0x80) >> 7
        if p8U != 0: ovfp8U = 1
        else: ovfp8U = 0
        if p8U == 255: ovfp8U1 = 1
        else: ovfp8U1 = 0
        muloverflow = (ovfp8U & (~raw & 0x1)) | (ovfp8U1 ^ p8MSB)
        return(muloverflow)

def qn(raw, m):
    if m == 8:
        return raw
    else: return 0



def update_flag(raw, result, a, b, m):
    status["z"] = zero(result, a, m)
    status["c"] = carry(raw, result, a, b, m)
    status["n"] = negative(result, m)
    status["v"] = overflow(result, a, b, m)
    status["s"] = sign(result, a, b, m)
    status["m"] = mul(raw, result, m)
    status["q"] = qn(raw, m)
    # hey there


# flag functions up there


while True:
    if pc >= len(mcode):
        break
    instruction = mcode[pc]
    pc += 1

    code = (instruction >> 12) & 0xF


    arith_r_src2 = instruction & 0xF
    arith_r_dest = (instruction >> 4) & 0xF
    immediate = instruction & 0xff
    immreg = (instruction >> 8) & 0xf


    if code == 0x1:
        subop = (instruction >> 8) & 0xF
        if subop >= 11:
            break
    elif code in ext3:
        subop = (instruction >> 9) & 0x7
    elif code in ext2:
        subop = (instruction >> 10) & 0x3
    elif code in ext1:
        subop = (instruction >> 11) & 0x1

    if code == 0x4:
        if subop >= 6:
            break
    if code == 0x5:
        if subop >= 7:
            break
    if code == 0xF:
        if subop >= 5:
            break

    arithA = registers[arith_r_dest]
    arithB = registers[arith_r_src2]


    if code == 0x2: # basic arithmetics #yikeys #happycore #fruityaerocore #brightfutures
        if subop == 0: #add
            arithR = arithA + arithB
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithA, arithB, 0)
            registers[arith_r_dest] = arithT # /--kill yo- be nice guys totally nothing happened

        elif subop == 1: #sub
            arithR = arithA - arithB
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithA, arithB, 1)
            registers[arith_r_dest] = arithT # die/ live

        elif subop == 2: #inc
            arithR = arithB + 1
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithB, 1, 0)
            registers[arith_r_src2] = arithT # ugh #dreamcore

        elif subop == 3: #dec
            arithR = arithB - 1
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithB, 1, 1)
            registers[arith_r_src2] = arithT # yikes #a


    elif code == 0x4: # bitwise operatiosn (dumb)
        if subop == 0: #ior
            arithR = arithA | arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

        elif subop == 1: #nor
            arithR = ~(arithA | arithB)
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

        elif subop == 2: #xor
            arithR = arithA ^ arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

        elif subop == 3: #xnr
            arithR = ~(arithA ^ arithB)
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

        elif subop == 4: #and
            arithR = arithA & arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

        elif subop == 5: #nad
            arithR = ~(arithA & arithB)
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2)
            registers[arith_r_dest] = arithT

    elif code == 0x3: # comparessdjiksajfdksfhjkf (no test and set -20 points)
        if subop == 0: #cmp
            arithR = arithA - arithB
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithA, arithB, 1) # its literally just compare #bsfr

        elif subop == 1: #cmn
            arithR = arithA + arithB
            arithT = (arithR & 0xff)
            update_flag(arithR, arithT, arithA, arithB, 0) #@everyone new candidate for the most random instructions

        elif subop == 2: #tst
            arithR = arithA & arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2) #hey

        elif subop == 3: #teq
            arithR = arithA ^ arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 2) #cmp but fancier

    elif code == 0x5: # shifting sand land
        if subop == 0: #lsl
            tempshift = arithA << (arithB & 0x7)
            arithT = tempshift & 0xff #nothing to see here
            update_flag(tempshift, arithT, arithA, arithB, 3)
            registers[arith_r_dest] = arithT

        elif subop == 1: #lsr
            shiftamount = arithB & 0x7
            tempshift = arithA >> shiftamount
            arithT = tempshift & 0xff
            update_flag(tempshift, shiftamount, arithA, arithB, 4)
            registers[arith_r_dest] = arithT

        elif subop == 2: #rol
            tempshift = arithA << (arithB & 0x7)
            lowerbyte = tempshift & 0xff
            upperbyte = (tempshift & 0xff00) >> 8
            arithT = lowerbyte | upperbyte # i said nothing
            update_flag(tempshift, arithT, arithA, arithB, 3)
            registers[arith_r_dest] = arithT

        elif subop == 3: #ror
            tempshift = (arithA << 8) >> (arithB & 7)
            lowerbyte = tempshift & 0xff
            upperbyte = (tempshift & 0xff00) >> 8
            arithT = lowerbyte | upperbyte
            update_flag(tempshift, arithT, arithA, arithB, 5)
            registers[arith_r_dest] = arithT # huh HUH you see? theres nothing

        elif subop == 4: #sar
            if arithA >= 0x80:
                shiftsign = 1
            else: shiftsign = 0
            if shiftsign == 1: valA = arithA + 0xff00
            else: valA = arithA

            shiftamount = arithB & 0x7
            tempshift = valA >> shiftamount
            arithT = tempshift & 0xff
            update_flag(tempshift, shiftamount, arithA, arithB, 4)
            registers[arith_r_dest] = arithT

        elif subop == 5: #flp
            flptmp0 = ((arithB & 0x55) << 1) | ((arithB & 0xaa) >> 1)
            flptmp1 = ((flptmp0 & 0x33) << 2) | ((flptmp0 & 0xcc) >> 2)
            flptmp2 = ((flptmp1 & 0x0f) << 4) | ((flptmp1 & 0xf0) >> 4)
            registers[arith_r_src2] = flptmp2

        elif subop == 6: #pct
            pct = arithB
            pct = pct - ((pct >> 1) & 0x55)
            pct = (pct & 0x33) + ((pct >> 2) & 0x33)
            pct = (pct + (pct >> 4)) & 0x0F
            registers[arith_r_src2] = pct

    elif code == 0x6:
        if subop == 0: #mul
            arithR = arithA * arithB
            arithT = arithR & 0xff
            update_flag(arithR, arithT, arithA, arithB, 6)
            registers[arith_r_dest] = arithT

        elif subop == 1: #iml
            a = gcalc(arithA, 0, 1)
            b = gcalc(arithB, 0, 1)
            mulsign = gcalc(arithA, arithB, 0)
            mulBFN = (a * b) & 0xffff
            if mulsign == 1: mulAFN = (~mulBFN + 1) & 0xffff
            else: mulAFN = mulBFN
            mulP8 = mulAFN & 0xff
            update_flag(mulsign, mulAFN, mulP8, 0, 7)
            registers[arith_r_dest] = mulP8

        elif subop == 2: #muh
            arithR = arithA * arithB
            arithT = ((arithR & 0xff00) >> 8) & 0xff
            update_flag(arithR, arithT, arithA, arithB, 6)
            registers[arith_r_dest] = arithT

        elif subop == 3: #imh
            a = gcalc(arithA, 0, 1)
            b = gcalc(arithB, 0, 1)
            mulsign = gcalc(arithA, arithB, 0)
            mulBFN = (a * b) & 0xffff
            if mulsign == 1: mulAFN = (~mulBFN + 1) & 0xffff
            else: mulAFN = mulBFN
            mulP8 = ((mulAFN & 0xff00) >> 8) & 0xff
            update_flag(mulsign, mulAFN, mulP8, 0, 7)
            registers[arith_r_dest] = mulP8

    elif code == 0x7: #div related
        if subop == 0: #div
            if arithB == 0:
                break
            else:
                arithR = arithA // arithB
                arithT = arithR & 0xff
                update_flag(arithR, arithT, arithA, arithB, 8)
                registers[arith_r_dest] = arithT

        elif subop == 1: #idv
            a = gcalc(arithA, 0, 1)
            b = gcalc(arithB, 0, 1)
            if b == 0:
                break
            else:
                divsign = gcalc(arithA, arithB, 0)
                divbfn = (a // b) & 0xff
                if divsign == 1: divafn = gcalc(divbfn, 0, 2)
                else: divafn = divbfn
                update_flag(divsign, divafn, arithA, arithB, 8)
                registers[arith_r_dest] = divafn

        elif subop == 2: #mod
            if arithB == 0:
                break
            else:
                arithR = arithA % arithB
                arithT = arithR & 0xff
                update_flag(arithR, arithT, arithA, arithB, 2)
                registers[arith_r_dest] = arithT

        elif subop == 3: #imd
            a = gcalc(arithA, 0, 1)
            b = gcalc(arithB, 0, 1)
            if b == 0:
                break
            else:
                if arithA >= 0x80: rsign = 1
                else: rsign = 0
                modbfn = (a % b) & 0xff
                if rsign == 1: modafn = gcalc(modbfn, 0, 2)
                else: modafn = modbfn
                update_flag(0, modafn, 0, 0, 2)
                registers[arith_r_dest] = modafn

                # gosh its finally done with the math stuff