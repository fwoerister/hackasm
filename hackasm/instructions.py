class Instruction:
    def __init__(self):
        pass

    def to_machine_code(self):
        raise NotImplementedError()


class AInstruction(Instruction):
    def __init__(self, immediate: int):
        if not 0 <= immediate <= 32767:
            raise ValueError("Immediate must be between 0 and 32767")

        self.immediate = bin(immediate)[2:]

        if len(self.immediate) < 15:
            self.immediate = '0' * (15 - len(self.immediate)) + self.immediate

        super().__init__()

    def to_machine_code(self) -> str:
        return f"0{self.immediate}"


class CInstruction(Instruction):
    def __init__(self, dest: str, comp: str, jump: str):
        self.dest = dest
        self.comp = comp
        self.jump = jump

        self.comp_translation_table = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'x': '001100',
            'y': '110000',
            '!x': '001101',
            '!y': '110001',
            '-x': '001111',
            '-y': '110011',
            'x+1': '011111',
            'y+1': '110111',
            'x-1': '001110',
            'y-1': '110010',
            'x+y': '000010',
            'x-y': '010011',
            'y-x': '000111',
            'x&y': '000000',
            'x|y': '010101',
        }

        self.jump_translation_table = {
            '': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }

        super().__init__()

    def get_dest_code(self) -> str:
        return (f"{"1" if 'A' in self.dest else "0"}"
                f"{"1" if 'D' in self.dest else "0"}"
                f"{"1" if 'M' in self.dest else "0"}")

    def get_comp_code(self) -> str:
        self.comp = self.comp.replace('D', 'x')

        if "M" in self.comp:
            self.comp = self.comp.replace('M', 'y')
            return "1" + self.comp_translation_table[self.comp]

        self.comp = self.comp.replace('A', 'y')
        return "0" + self.comp_translation_table[self.comp]

    def to_machine_code(self) -> str:
        return f"111{self.get_comp_code()}{self.get_dest_code()}{self.jump_translation_table[self.jump]}"
