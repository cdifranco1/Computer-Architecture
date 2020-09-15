"""CPU functionality."""

import sys

# Inventory of files
"""


"""
ALU = {"MUL", "ADD", "SUB", "CMP"}
NO_INCREMENT = {"JMP", "CALL", "RET", "JNE", "JEQ"}

# LDI = 10000010
# HLT = 1
# PRN = 1000111
# MUL = 10100010

L = 4
G = 2
E = 1

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.opcodes = {
            0b10000010: {"name": "LDI", "operation": self.LDI},
            0b00000001: {"name": "HLT", "operation": self.HLT},
            0b01000111: {"name": "PRN", "operation": self.PRN},
            0b10100010: {"name": "MUL", "operation": self.alu},
            0b10100000: {"name": "ADD", "operation": self.alu},
            0b01000101: {"name": "PUSH", "operation": self.push},
            0b01000110: {"name": "POP", "operation": self.pop},
            0b01010000: {"name": "CALL", "operation": self.call},
            0b00010001: {"name": "RET", "operation": self.ret},
            0b10100111: {"name": "CMP", "operation": self.alu},
            0b01010100: {"name": "JMP", "operation": self.jmp},
            0b01010110: {"name": "JNE", "operation": self.jne},
            0b01010101: {"name": "JEQ", "operation": self.jeq}
        }
        # `FL` bits: `00000LGE`
        self.fl = 0
        self.running = False
        self.pc = 0
        self.reg = [0] * 8
        self.size = 255
        self.ram = [0] * self.size
        self.SP = self.size - 1

    def load(self):
        """Load a program into memory."""

        #ram address is at 0
        address = 0

        if len(sys.argv) < 2:
            print(f'Usage: ls8.py filename')
        else:
            filename = sys.argv[1]

        with open(filename) as f:
            for line in f:
                x = line.split("#")[0]
                instruction = x.strip()
                if instruction == "":
                    continue

                self.ram[address] = int(instruction, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = L
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = G
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = E

        else:
            raise Exception("Unsupported ALU operation")
    
    def jmp(self):
        reg_num = self.ram[self.pc + 1]
        print(f"JUMPING to address: {self.reg[reg_num]}")
        self.pc = self.reg[reg_num]
    
    def jne(self):
        if self.fl != 1:
            self.jmp()
        else:
            self.pc += 2
    
    def jeq(self):
        if self.fl == 1:
            self.jmp()
        else:
            self.pc += 2

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def push(self):
        reg_num = self.ram[self.pc + 1]
        self.SP -= 1
        self.ram[self.SP] = self.reg[reg_num]
    
    def pop(self):
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = self.ram[self.SP]
        self.SP += 1
    
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def LDI(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
    
    def HLT(self):
        self.running = False

    def PRN(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
    
    def call(self):
        # print("RUNNING")
        # add the next location of the pc onto the stack
        self.SP -= 1
        self.ram[self.SP] = self.pc + 2
        # get register number where call address saved
        reg_num = self.ram[self.pc + 1] 

        # move PC to address saved in the register
        self.pc = self.reg[reg_num]

    def ret(self):
        self.pc = self.ram[self.SP]
        self.SP += 1

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram[self.pc]

            op_name = self.opcodes[ir]["name"]
            op_func = self.opcodes[ir]["operation"]

            if op_name in ALU:
                op_func(op_name, self.ram[self.pc + 1], self.ram[self.pc + 2])
            elif op_name in NO_INCREMENT:
                op_func()
                continue
            else:
                op_func()

            ops = ir >> 6
            self.pc += (ops + 1)