
def readFile(file):
    File=open(file,'r')
    global MachineCode
    MachineCode=[]
    while True:
        inst=File.readline()
        if inst:
            _,inst=inst.split()
            inst=bin(int(inst,base=16)).replace('0b','')
            MachineCode.append(inst)
        else:
            break
    File.close()

def bintodec(binary):
    length=len(binary)
    number=int(binary[1:],base=2)
    if binary[0]=='0':
        return number
    return number-2**(length-1)

def dectobin(integer,length):
    if integer>=0:
        temp=bin(integer).replace('0b','')
        le=len(temp)
        binary='0'*(length-le)+temp
    else:
        integer+=2**(length-1)
        temp=bin(integer).replace('0b','')
        le=len(temp)
        binary='1'+'0'*(length-1-le)+temp        
    return binary


PC=0
#register File
Reg=['0'*32 for j in range(32)]

#memory
Mem=['0'*32]*4000

    
def fetch():
    global IR,PC
    IR=MachineCode[PC//4]
    PC+=4
    print("The instruction is"+str(IR))
    print("PC incremented from"+str(PC-4)+"to"+str(PC))
def decode():
    print("performing decode()")
    global rs1,rs2,rd,imm,operation
    operation=''
    opcode=IR[-7:]
    rd=IR[-12:-7]
    func3=IR[-15:-12]
    rs1=IR[-20:-15]
    rs2=IR[-25:-20]
    func7=IR[-32:-25]
    if(opcode=="0110011"):
        if(func3=="000" and func7=="0000000"):
            operation="add"
            print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="000" and func7=="0100000"):
            operation="sub"
           print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="001"):
            operation="sll"
            print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="010"):
            operation="slt"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="011"):
            operation="sltu"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="100"):
            operation="xor"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="101" and func7=="0000000"):
            operation="srl"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="101" and func7=="0100000"):
            operation="sra"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="110"):
            operation="or"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="111"):
            operation="and"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="000" and func7=="0000001"):
            operation="mul"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="100" and func7=="0000001"):
            operation="div"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
        elif(func3=="110" and func7=="0000001"):
            operation="rem"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2+"Rd: "+rd)
    elif(opcode=="0010011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="addi"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
        elif(func3=="110"):
            operation="ori"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
        elif(func3=="111"):
            operation="andi"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
    elif(opcode=="0000011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="lb"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
        elif(func3=="001"):
            operation="lh"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
        elif(func3=="010"):
            operation="lw"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
    elif(opcode=="1100111"):
        imm=func7+rs2
        if(func3=="000"):
            operation="jalr"
                        print("The operation is "+operation+". Rs1: "+rs1+"Rd: "+rd)
    elif(opcode=="0100011"):
        imm=func7+rd
        if(func3=="000"):
            operation="sb"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
        elif(func3=="001"):
            operation="sh"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
        elif(operation=="010"):
            operation="sw"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
    elif(opcode=="1100011"):
        imm=func7[0]+rd[-1]+func7[1:]+rd[0:-1]+"0"
        if(func3=="000"):
            operation="beq"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
        elif(func3=="001"):
            operation="bne"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
        elif(func3=="101"):
            operation="bge"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
        elif(func3=="100"):
            operation="blt"
                        print("The operation is "+operation+". Rs1: "+rs1+" Rs2: "+rs2)
    elif(opcode=="0010111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="auipc"
                    print("The operation is "+operation+"Rd: "+rd)
    elif(opcode=="0110111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="lui"
                    print("The operation is "+operation+"Rd: "+rd)
    elif(opcode=="1101111"):
        imm=func7[0]+rs1+func3+rs2[-1]+func7[1:]+rs2[:-1]+"0"
        operation="jal"
                    print("The operation is "+operation+"Rd: "+rd)

def execute():
    global PC,ALU_output,operation
    ALU_output=''
    arg1=int(rs1,base=2)
    arg2=int(rs2,base=2)
    if operation=="add":
        ALU_output=dectobin(bintodec(Reg[arg1])+bintodec(Reg[arg2]),32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="sub":
        ALU_output=dectobin(bintodec(Reg[arg1])-bintodec(Reg[arg2]),32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="sll":
        shif=bintodec(Reg[arg2])
        temp=Reg[arg1][shif:]+'0'*shif
        ALU_output=temp
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="slt":
        r1=bintodec(Reg[arg1])
        r2=bintodec(Reg[arg2])
        ALU_output=1 if r1<r2 else 0
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="sltu":
        ALU_output=1 if int(r1,base=2)<int(r2,base=2) else 0
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="xor":
        ALU_output=dectobin(bintodec(Reg[arg1])^bintodec(Reg[arg2]),32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="srl":
        shif=bintodec(Reg[arg2])
        temp='0'*shif+Reg[arg1][:-shif]
        ALU_output=temp
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="sra":
        shif=bintodec(Reg[arg2])
        temp='1'*shif+Reg[arg1][:-shif]
        ALU_output=temp
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="or":
        temp=bintodec(Reg[arg1])|bintodec(Reg[arg2])
        ALU_output=dectobin(temp, 32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="and":
        temp=bintodec(Reg[arg1])&bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="mul":
        temp=bintodec(Reg[arg1]) * bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="div":
        temp=bintodec(Reg[arg1]) // bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32) 
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="rem":
        temp=bintodec(Reg[arg1]) % bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+arg2+"is"+ALU_output)
    if operation=="addi":
        temp=bintodec(Reg[arg1])+bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+imm+"is"+ALU_output)
    if operation=="ori":
        temp=bintodec(Reg[arg1])|bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+imm+"is"+ALU_output)
    if operation=="andi":
        temp=bintodec(Reg[arg1])&bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+"of"+arg1+"and"+imm+"is"+ALU_output)
    if operation in ["lb","lw","lh","sb","sh","sw"]:
        temp=bintodec(Reg[rs1])+bintodec(imm)
        ALU_output=dectobin(temp,32)
        
    if operation=="jalr":
        temp=bintodec(Reg[rs1])+bintodec(imm)
        temp2=PC
        PC=temp
        ALU_output=temp2
        print(operation+"of"+arg1+"and"+imm+"is"+ALU_output)
    if operation in ["beg","bne","bge","blt","auipc"]:
        PC+=bintodec(imm)
        print(operation+"of"+arg1+"and"+arg2+"is done")
    if operation=="lui":
        ALU_output=imm
        print(operation+"is done")
    if operation=="jal":
        temp=bintodec(imm)
        temp2=PC
        PC=temp
        ALU_ouput=temp2
        print(operation+"is done")
        print("the program is executed successfully" )
def memoryAcess():
    global PC,ALU_output,operation,MDR
    if ALU_output:
        ALu_output = int(ALU_output,base=2)
        val = ALu_output%32
    else:
        return
    MDR = ''
    if operation == "lw":
        for i in range(32):
            MDR+= Mem[Alu_output//32][ALu_output%32]
    elif operation == "lh":
         for i in range(16):
            MDR+= Mem[Alu_output//32][ALu_output%32]
            ALu_output+=1
    elif operation  == "lb":
         for i in range(8):
            MDR+= Mem[Alu_output//32][ALu_output%32]
            ALu_output+=1
    elif operation  == "sb":
         if val <=24:
             contents = Mem[ALu_output//32]
             k = contents[:val] + rs2 + contents[val + 8:]
             Mem[ALu_output//32] = k
         else:
              contents1= Mem[ALu_output//32]
              contents2 = Mem[ALu_output//32+1]
              a = 32 - val 
              b = 2 * val - 32
              k1 = contents1[:val] + rs2[:a]
              k2 = rs2[-b:] + contents2[b:]
              Mem[ALu_output//32] = k1
              Mem[ALu_output//32+1] = k2
    elif operation  == "sh":
         if val <=16:
              contents = Mem[ALu_output//32]
              k = contents[:val] + rs2 + contents[val + 8:]
              Mem[ALu_output//32] = k
         else:
              contents1= Mem[ALu_output//32]
              contents2 = Mem[ALu_output//32+1]
              a = 32 - val 
              b = 2 * val - 32
              k1 = contents1[:val] + rs2[:a]
              k2 = rs2[-b:] + contents2[b:]
              Mem[ALu_output//32] = k1
              Mem[ALu_output//32+1] = k2
    elif operation  == "sw":
          if val <=0:
             contents = Mem[ALu_output//32]
             k = contents[:val] + rs2 + contents[val + 16:]
             Mem[ALu_output//32] = k
          else:
             contents1= Mem[ALu_output//32]
             contents2 = Mem[ALu_output//32+1]
             a = 32 - val 
             b = 2 * val - 32
             k1 = contents1[:val] + rs2[:a]
             k2 = rs2[-b:] + contents2[b:]
             Mem[ALu_output//32] = k1
             Mem[ALu_output//32+1] = k2
            
    else:
        return 

def writeback():  #data from memory ,#   from excute for ALU instructions ,# rd destination register 
    rd1=int(rd,base=2)
    if(operation =="add" or operation=="slt" or operation=="and" or operation =="or" or operation=="sll" or operation=="sra" or operation=="mul"):
        Reg[rd1]=ALU_output
    elif(operation== "srl" or operation=="sub" or operation=="xor" or operation=="div" or operation=="rem" or operation=="addi" or operation=="andi" or operation=="ori"):
        Reg[rd1]=ALU_output
    elif(operation=="lb" or operation=="ld" or operation=="lh" or operation=="lw"):
        Reg[rd1]=MDR
    elif(operation=="jalr" or operation=="jal"):
        Reg[rd1]=ALU_output  
    elif(operation=="lui" or operation=="auipc"):
        Reg[rd1]=ALU_output
    print("Memory write successful")

def setToStart():
    global Reg,Mem,PC,IR,rs1,rs2,rd,imm,operation,MDR,ALU_output
    Reg=['0'*32]*32
    Mem=['0'*32]*4000
    Reg[2]='01111111111111111111111111110000'
    Reg[3]='00010000000000000000000000000000'
    PC='0'
    IR=['0'*32]
    rs1=['0'*5]
    rs2=['0'*5]
    rd=['0'*5]
    imm=['0'*12]
    operation=''
    MDR=''

def storeState():
    global Reg,Mem
    f=open("store.txt","w+")
    f.write("Registers\n")
    for i in range(32):
        f.write("x"+str(i)+":"+Reg[i])         #Registers: 0000..... 0000....1 ......
        f.write("\n")            #Memory:00.000 0012.. 
    f.write("\n\n") 
    f.write("Memory: ")
    for j in range(4000):
        f.write(Mem[j])
        f.write(" ")
        f.write("\n")    
    f.close()    
       
def run_RISCVsim():
    fetch()
    decode()
    execute()
    memoryAcess()
    writeback()
