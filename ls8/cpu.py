"""CPU functionality."""

import sys

# Inventory of files
"""

"""

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.opcodes = {
            0b10000010: {"name": "LDI", "operation": self.LDI},
            0b00000001: {"name": "HLT", "operation": self.HLT},
            0b01000111: {"name": "PRN", "operation": self.PRN},
        }

        self.running = False
        self.pc = 0
        self.reg = [0] * 8
        self.size = 255
        self.ram = [0] * self.size

    def load(self):
        """Load a program into memory."""

        address = 0
        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
    
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def LDI(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3
    
    def HLT(self):
        self.running = False
        self.pc += 1

    def PRN(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram[self.pc]
            
            op_func = self.opcodes[ir]["operation"]
            op_func()