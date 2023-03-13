#!/usr/bin/python3

# This script generate mutation of the base gadget list
# To create a valid rop chain, we must provide gadgets to 
# 1 - write command into data section
# 2 - set rax 0xb
# 3 - set rdi to point to command
# 4 - set rsi to null
# 5 - set rdx to null
# 6 - syscall

import random

folder = "source/"

register = [ "rax" , "rbx" , "rcx" , "rdx" , "rsi" , "rdi" , "rbp" , "rsp" , "r8" , "r9" , "r10" , "r11" , "r12" , "r13" , "r14" , "r15" ]

intro = """
bits 64

SECTION .gadgets.text

gadgets:
\n
"""

popped_reg = []

def gadget_for_write_data():
    # write data into data section
    to_ret = ".StoreConstG1:\n"
    dst = random.choice(popped_reg)
    src = random.choice(popped_reg)
    while dst == src:
        src = random.choice(popped_reg)

    to_ret += "MOV QWORD [" + dst + "], " + src + "\n"
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_rax():
    # rax 0xb
    to_ret = ".LoadRAX:\n"
    # Add random preable
    to_ret += "POP RAX\n"
    popped_reg.append("rax")
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_rdi():
    # rdi address to cmd
    to_ret = ".LoadRDI:\n"
    # Add random preable
    to_ret += "POP RDI\n"
    popped_reg.append("rdi")
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_rsi():
    # rsi address to null
    to_ret = ".LoadRSI:\n"
    # Add random preable
    to_ret += "POP RSI\n"
    popped_reg.append("rsi")
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_rdx():
    # rdx address to null
    to_ret = ".LoadRDX:\n"
    # Add random preable
    to_ret += "POP RDX\n"
    popped_reg.append("rdx")
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_syscall():
    # syscall
    to_ret = ".SyscallG:\n"
    # Add random preable
    to_ret += "SYSCALL\n"
    to_ret += "RET\n\n"
    return to_ret

count = 1
def gadget_for_random_pop():
    global popped_reg
    global count
    to_ret = ".LoadSomeReg" + str(count) + ":\n"
    count += 1
    for i in range(random.randint(1, 5)):
        random_reg = random.choice(register)
        to_ret += "POP " + random_reg + "\n"
        popped_reg.append(random_reg)
    to_ret += "RET\n\n"
    return to_ret

def gadget_for_nop(num):
    to_ret = ".NopG" + str(num) + ":\n"
    to_ret += "NOP\n"
    to_ret += "RET\n\n"
    return to_ret

def popped_check():

    if ( "rax" in popped_reg and 
         "rdi" in popped_reg and 
         "rsi" in popped_reg and
         "rdx" in popped_reg):
        return True

    return False

def random_replace(text, token, replace, num_replacements):
    num_tokens = text.count(token)
    points = [0] + sorted(random.sample(range(1,num_tokens+1),num_replacements)) + [num_tokens+1]
    return replace.join(token.join(text.split(token)[i:j]) for i,j in zip(points,points[1:]))

def main():
    global popped_reg
    for i in range(3):
        popped_reg = []
        f = open(folder + "gadgets" + str(i) + ".nasm64", "w")

        to_write = intro

        while not popped_check():
            to_write += gadget_for_random_pop()

        to_write = random_replace(to_write, "RET", "CALL " + random.choice(popped_reg) + gadget_for_nop(1), 1)
        to_write += gadget_for_write_data()
        to_write += gadget_for_nop(2)
        to_write += gadget_for_syscall()

        # print(to_write)
        # print(popped_reg)
        f.write(to_write)
        f.close()


if __name__ == "__main__":
    main()

# .LoadConstG1:
# POP RAX
# RET

# .LoadConstG2:
# POP RBX
# RET

# .LoadConstG4:
# POP RDX
# RET

# .LoadConstG6:
# POP RDI
# RET

# .LoadConstG7:
# POP RSI
# RET

# .StoreMemG1:
# MOV [RAX], RBX
# RET

# .SyscallG:
# SYSCALL
# RET

# .BadGadget01:
# mov qword [rbx], r13
# pop rbx
# pop rbp
# pop r12
# pop r13
# ret