opcodes = {
    "nop": "0000", "hlt": "0000", "sez": "0000", "clz": "0000", "sec": "0000", "clc": "0000", "cmc": "0000", "clf": "0000",
    "psh": "0001", "pop": "0001", "sic": "0001", "sdc": "0001", "trs": "0001", "tsr": "0001", "php": "0001", "plp": "0001", "rsp": "0001", "csp": "0001", "clr": "0001",
    "add": "0010", "sub": "0010", "inc": "0010", "dec": "0010",
    "cmp": "0011", "cmn": "0011", "tst": "0011", "teq": "0011",
    "ior": "0100", "nor": "0100", "xor": "0100", "xnr": "0100", "and": "0100", "nad": "0100",
    "lsl": "0101", "lsr": "0101", "rol": "0101", "ror": "0101", "sar": "0101", "flp": "0101", "pct": "0101",
    "mul": "0110", "iml": "0110", "muh": "0110", "imh": "0110",
    "div": "0111", "idv": "0111", "mod": "0111", "imd": "0111",
    "ldi": "1000",
    "mov": "1001", "mar": "1001",
    "ldr": "1010", "str": "1010",
    "rlj": "1011",
    "jmp": "1100",
    "cal": "1101", "ret": "1101",
    "inp": "1110", "out": "1110",
    "sei": "1111", "cli": "1111", "irt": "1111", "int": "1111", "wfi": "1111",  
}

subopcodes = {
    "nop": "000", "hlt": "001", "sez": "010", "clz": "011", "sec": "100", "clc": "101", "cmc": "110", "clf": "111",
    "psh": "0000", "pop": "0001", "sic": "0010", "sdc": "0011", "trs": "0100", "tsr": "0101", "php": "0110", "plp": "0111", "rsp": "1000", "csp": "1001", "clr": "1010",
    "add": "00", "sub": "01", "inc": "10", "dec": "11",
    "cmp": "00", "cmn": "01", "tst": "10", "teq": "11",
    "ior": "000", "nor": "001", "xor": "010", "xnr": "011", "and": "100", "nad": "101",
    "lsl": "000", "lsr": "001", "rol": "010", "ror": "011", "sar": "100", "flp": "101", "pct": "110",
    "mul": "00", "iml": "01", "muh": "10", "imh": "11",
    "div": "00", "idv": "01", "mod": "10", "imd": "11",
    "mov": "0", "mar": "1",
    "ldr": "0", "str": "1",
    "cal": "0", "ret": "1",
    "inp": "0", "out": "1",
    "sei": "000", "cli": "001", "irt": "010", "int": "011", "wfi": "100"
}

cond = {
    "z,": "0000", "nz,": "0001", "c,": "0010", "nc,": "0011",
    "n,": "0100", "nn,": "0101", "v,": "0110", "nv,": "0111",
    "s,": "1000", "ns,": "1001", "m,": "1010", "q,": "1011",
    "id,": "1100", "nvr,": "1101", "alw,": "1110",
}

zeroops = ["nop", "hlt", "sez", "clz", "sec", "clc", "cmc", "clf", "sic", "sdc", "php", "plp", "csp", "clr", "ret", "sei", "cli", "irt", "wfi"]
oneops = ["psh", "pop", "trs", "tsr", "rsp", "inc", "dec", "flp", "pct"]
twoops = ["add", "sub", "cmp", "cmn", "tst", "teq", "mul", "iml", "muh", "imh", "div", "idv", "mod", "imd", "ior", "nor", "xor", "xnr", "and", "nad", "lsl", "lsr", "rol", "ror", "sar", "mov"]
memory = ["mar", "ldr", "str"]
ports = ["inp", "out"]
    
def register(regstr):
    fuckyou_comma = regstr.replace(",", "")
    fuckyoutoo_r = fuckyou_comma.replace("r", "")
    this_is_number = int(fuckyoutoo_r)
    lotsofoneszeros = bin(this_is_number)[2:]
    regfr = lotsofoneszeros.zfill(4)
    return regfr

def ebvalue(ebv):
    commaB = ebv.replace(",", "")
    ebinteger = int(commaB)
    unsignedB = ebinteger & 0xFF
    ebbinary = bin(unsignedB)[2:]
    compl8bin = ebbinary.zfill(8)
    return compl8bin

def sbvalue(sbv):
    commaS = sbv.replace(",", "")
    sbinteger = int(commaS)
    unsignedS = sbinteger & 0x7F
    sbbinary = bin(unsignedS)[2:]
    compl7bin = sbbinary.zfill(7)
    return compl7bin

def fbvalue(fbv):
    commaF = fbv.replace(",", "")
    fbinteger = int(commaF)
    unsignedF = fbinteger & 0xF
    fbbinary = bin(unsignedF)[2:]
    compl4bin = fbbinary.zfill(4)
    return compl4bin

def tbvalue(tbv):
    commaT = tbv.replace(",", "")
    tbinteger = int(commaT)
    unsignedT = tbinteger & 0x3
    tbbinary = bin(unsignedT)[2:]
    compl2bin = tbbinary.zfill(2)
    return compl2bin

labels = {}
pc = 0
mcode = []

with open("text file to compile here", "r") as file:
    lines = file.readlines()

for line in lines:
    line = line.split('#')[0].strip()
    if not line:
        continue

    if line.endswith(":"):
        labels[line[:-1]] = pc
        continue
    pc += 1

print("labels:", labels)
print(" ")
for line in lines:
    line = line.split('#')[0].strip()
    if not line or line.endswith(":"):
        continue

    parts = line.split()
    code = parts[0]

    if code in zeroops:
        op = opcodes[code]
        sub = subopcodes[code]
        pad_len = 12 - len(sub)
        padding = "0" * pad_len
        final = op + sub + padding
        mcode.append(final)

    elif code in oneops:
        op = opcodes[code]
        sub = subopcodes[code]
        src = register(parts[1])
        pad_len = len(op) + len(sub) + len(src)
        padding = "0" * (16 - pad_len)
        mcode.append(op + sub + padding + src)

    elif code in twoops:
        op = opcodes[code]
        sub = subopcodes[code]
        dest = register(parts[1])
        src = register(parts[2])
        pad_len = len(op) + len(sub) + len(dest) + len(src)
        padding = "0" * (16 - pad_len)
        mcode.append(op + sub + padding + dest + src)

    elif code == "ldi":
        op = opcodes[code]
        dest = register(parts[1])
        imm = ebvalue(parts[2])
        mcode.append(op + dest + imm)

    elif code in memory:
        op = opcodes[code]
        sub = subopcodes[code]
        offset = sbvalue(parts[1])
        src = register(parts[2])
        mcode.append(op + sub + offset + src)

    elif code in ports:
        op = opcodes[code]
        sub = subopcodes[code]
        port = fbvalue(parts[1])
        src = register(parts[2])
        mcode.append(op + sub + ("0" * (16 - (len(op) + len(sub) + len(port) + len(src)))) + port + src)

    elif code == "cal":
        op = opcodes[code]
        bank = tbvalue(parts[1])
        imm = ebvalue(parts[2])
        mcode.append(op + "00" + bank + imm)

    elif code == "rlj":
        op = opcodes[code]
        port = cond[parts[1]]
        imm = ebvalue(parts[2])
        mcode.append(op + port + imm)

    elif code == "jmp":
        op = opcodes[code]
        port = cond[parts[1]]
        label = parts[2]
        addrE = labels[label]
        addrB = bin(addrE)[2:].zfill(8)
        mcode.append(op + port + addrB)

    elif code == "int":
        op = opcodes[code]
        port = fbvalue(parts[1])
        mcode.append(op + ("0" * (16 - (len(op) + len(port)))) + port)

open("F:/users/phuc/bb/output.txt", "w").write("\n".join(mcode))
