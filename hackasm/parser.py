import re

from collections.abc import Iterable

from hackasm.instructions import AInstruction, CInstruction, Instruction

A_INSTRUCTION_REGEX = r'^@([a-zA-Z._$:][a-zA-Z0-9._$:]*|\d+)$'

DEST_REGEX = r'[ADM]{1,3}='
COMP_REGEX = r'0|1|-1|D|[AM]|!D|![AM]|-D|-[AM]|D+1|[AM]+1|D-1|[AM]-1|D+[AM]|D-[AM]|[AM]-D|D&[AM]|D\|[AM]'
JUMP_REGEX = r'JGT|JEQ|JGE|JLT|JNE|JLE|JMP'

C_INSTRUCTION_REGEX = rf'^({DEST_REGEX})?({COMP_REGEX})(;{JUMP_REGEX})?'


class Parser:
    def __init__(self, src_file_name: str):
        self.file = src_file_name
        self.next_var_address = 0x0010
        self.symbols = {
            'R0': 0x0000,
            'R1': 0x0001,
            'R2': 0x0002,
            'R3': 0x0003,
            'R4': 0x0004,
            'R5': 0x0005,
            'R6': 0x0006,
            'R7': 0x0007,
            'R8': 0x0008,
            'R9': 0x0009,
            'R10': 0x000A,
            'R11': 0x000B,
            'R12': 0x000C,
            'R13': 0x000D,
            'R14': 0x000E,
            'R15': 0x000F,
            'SP': 0x0000,
            'LCL': 0x0001,
            'ARG': 0x0002,
            'THIS': 0x0003,
            'THAT': 0x0004,
            'SCREEN': 0x4000,
            'KBD': 0x6000,
        }

        self.parse_symbols()

    def parse_symbols(self):
        with open(self.file, 'r') as source:
            line_count = 0
            for line in source:
                line = line.strip()

                if not line or line.startswith('//'):
                    continue

                if line.startswith('(') and line.endswith(')'):
                    symbol = line[1:-1]
                    if symbol not in self.symbols:
                        self.symbols[symbol] = line_count
                else:
                    line_count += 1

    def get_parsed_instructions(self) -> Iterable[Instruction]:
        with open(self.file, 'r') as source:
            line_nr = -1
            for line in source:
                line_nr += 1

                # ignore leading and trailing spaces
                line = line.strip()

                # ignore comments and empty lines
                if not line or line.startswith('//') or (line.startswith('(') and line.endswith(')')):
                    continue

                # convert to A instruction
                if re.match(A_INSTRUCTION_REGEX, line):
                    yield self.to_a_instruction(line)
                # convert to C instruction
                elif re.match(C_INSTRUCTION_REGEX, line):
                    yield self.to_c_instruction(line)
                else:
                    raise Exception(f"Invalid syntax at line {line_nr}: {line}")

    @staticmethod
    def to_c_instruction(line):
        groups = re.findall(C_INSTRUCTION_REGEX, line)[0]
        dest = groups[0][:-1] if groups[0] else ''
        comp = groups[1]
        jump = groups[2][1:] if groups[2] else ''
        return CInstruction(dest, comp, jump)

    def to_a_instruction(self, line):
        if line[1:].isdigit():
            immediate = int(line[1:])

            if 0 <= immediate <= 0x7FFF:
                return AInstruction(immediate)
            else:
                raise Exception("Immediate out of range.")
        else:
            symbol = line[1:]

            if symbol in self.symbols:
                return AInstruction(self.symbols[symbol])
            else:
                variable_address = self.next_var_address
                self.symbols[symbol] = variable_address
                self.next_var_address += 1
                return AInstruction(variable_address)
