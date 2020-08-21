"""CPU functionality."""

import sys

HLT = 0b00000001 # Hault
LDI = 0b10000010 # Load
PRN = 0b01000111 # Print
MUL = 0b10100010 # Multiply
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001 # Return
CMP = 0b10100111 # Compare
JMP = 0b01010100 # Jump to address
JEQ = 0b01010101 # Jump if equal
JNE = 0b01010110 # Jump if no flag

EFLAG = 0b001 # Equal
LFLAG = 0b011 # Less than
GFLAG = 0b010 # Greater than

class CPU:

	def __init__(self):
		self.running = True
		self.pointer = 0
		self.reg = [0] * 8
		self.memory = [0] * 256
		self.stackPointer = 0xf4
		self.reg[7] = self.stackPointer
		self.flag = None

		self.branchTable = {}
		self.branchTable[HLT] = self.handleHLT
		self.branchTable[LDI] = self.handleLDI
		self.branchTable[PRN] = self.handlePRN
		self.branchTable[MUL] = self.handleMUL
		self.branchTable[PUSH] = self.handlePUSH
		self.branchTable[POP] = self.handlePOP
		self.branchTable[CALL] = self.handleCALL
		self.branchTable[RET] = self.handleRET
		self.branchTable[CMP] = self.handleCMP
		self.branchTable[JMP] = self.handleJMP
		self.branchTable[JEQ] = self.handleJEQ
		self.branchTable[JNE] = self.handleJNE


	def load(self):
		memoryCount = 0
		file = sys.argv[1]

		try:
			with open(file) as data:
				for x, line in enumerate(data):
					line = line.split("#")
					if line[0] == '' or line[0] == '\n':
						continue
					v = int(line[0],2)

					self.memory[memoryCount] = v
					memoryCount += 1

		except FileNotFoundError:
			print("Unable to open file")
			self.running = False


	def ram_read(self, value):
		return self.memory[value]


	def ram_write(self, value, data):
		self.memory[value] = data


	def handleHLT(self, a=None, b=None):
		self.running = False


	def handleLDI(self, a, b):
		self.reg[a] = b
		self.pointer +=3


	def handlePRN(self, a, b=None):
		print(self.reg[a])
		self.pointer += 2


	def handleMUL(self, a, b):
		self.alu("MUL", a, b)
		self.pointer += 3


	def handlePUSH(self, a, b=None):
		value = self.reg[a] # Get value from register
		self.stackPointer -= 1 # Decrement stackPointer
		self.memory[self.stackPointer] = value # Store to memory (RAM)
		self.pointer += 2


	def handlePOP(self, a, b=None):
		value = self.memory[self.stackPointer] # Get value from register
		self.reg[a] = value # Store to register
		self.stackPointer += 1
		self.pointer += 2

	def handleCALL(self, a, b):
		returnCounter = self.pointer + 2
		self.stackPointer -= 1
		self.memory[self.stackPointer] = returnCounter
		self.stackPointer = self.reg[q]

	def handleRET(self, a, b):
		value = self.memory[self.stackPointer] # Get from stack
		self.pointer = value # Set to current pointer
		self.stackPointer += 1

	def handleCMP(self, a, b):
		self.alu('CMP', a, b)
		self.pointer += 3

	def handleJMP(self, a, b):
		self.pointer = self.reg[a]

	def handleJEQ(self, a, b):
		if self.flag == EFLAG:
			self.pointer = self.reg[a]
		else:
			self.pointer += 2

	def handleJNE(self, a, b):
		if self.flag != EFLAG:
			self.pointer = self.reg[a]
		else:
			self.pointer += 2



	def run(self):

		while self.running:
			instruction = self.ram_read(self.pointer)
			operand_a = self.ram_read(self.pointer + 1)
			operand_b = self.ram_read(self.pointer + 2)
			# self.trace()

			if instruction in self.branchTable:
				self.branchTable[instruction](operand_a, operand_b)
			else:
				print("Error running program instructions")
				self.running = False


	def alu(self, op, a, b):

		if op == "ADD":
			self.reg[a] += self.reg[b]
		elif op == "SUB":
			self.reg[a] -= self.reg[b]
		elif op == "MUL":
			self.reg[a] * self.reg[b]
		elif op == "DIV":
			self.reg[a] // self.reg[b]
		elif op == 'AND':
			self.reg[a] = self.reg[a] & self.reg[b]
		elif op == 'OR':
			self.reg[a] = self.reg[a] | self.reg[b]
		elif op == 'XOR':
			self.reg[a] = self.reg[a] ^ self.reg[b]
		elif op == 'NOT':
			self.reg[a] = ~self.reg[a]
		elif op == 'SHL':
			self.reg[a] = self.reg[a] << self.reg[b]
		elif op == 'SHR':
			self.reg[a] = self.reg[a] >> self.reg[b]
		elif op == "MOD":
			self.reg[a] = self.reg[a] % self.reg[b]
		elif op == "CMP":
			a = self.reg[a]
			b = self.reg[b]
			if a > b:
				self.flag = GFLAG
			elif a < b:
				self.flag = LFLAG
			else:
				self.flag = EFLAG

		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pointer,
			#self.fl,
			#self.ie,
			self.ram_read(self.pointer),
			self.ram_read(self.pointer + 1),
			self.ram_read(self.pointer + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()
