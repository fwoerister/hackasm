from unittest import TestCase

from hackasm.instructions import AInstruction, CInstruction


class TestAInstruction(TestCase):
    def test_a_instruction_with_valid_immediate(self):
        instruction = AInstruction(immediate=574)
        self.assertEqual(instruction.to_machine_code(), "0000001000111110")

    def test_a_instruction_with_overflowing_immediate(self):
        self.assertRaises(ValueError, AInstruction, immediate=1000000000)

    def test_a_instruction_with_negative_immediate(self):
        self.assertRaises(ValueError, AInstruction, immediate=-1)


class TestBInstruction(TestCase):
    def test_valid_c_instruction_base_case(self):
        instruction = CInstruction("", "0", "")
        self.assertEqual(instruction.to_machine_code()[:3], "111")

    def test_memory_flag(self):
        instruction = CInstruction("", "A", "")
        self.assertEqual(instruction.to_machine_code()[3], "0")

        instruction = CInstruction("", "M", "")
        self.assertEqual(instruction.to_machine_code()[3], "1")

    def test_encoding_of_0_operation(self):
        instruction = CInstruction("A", "0", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "101010")

    def test_encoding_of_1_operation(self):
        instruction = CInstruction("A", "1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "111111")

    def test_encoding_of_minus_1_operation(self):
        instruction = CInstruction("A", "-1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "111010")

    def test_encoding_of_x_operation(self):
        instruction = CInstruction("A", "D", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "001100")

    def test_encoding_of_y_operation(self):
        instruction = CInstruction("A", "A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "110000")

    def test_encoding_of_not_x_operation(self):
        instruction = CInstruction("A", "!D", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "001101")

    def test_encoding_of_not_y_operation(self):
        instruction = CInstruction("A", "!A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "110001")

    def test_encoding_of_minus_x_operation(self):
        instruction = CInstruction("A", "-D", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "001111")

    def test_encoding_of_minus_y_operation(self):
        instruction = CInstruction("A", "-A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "110011")

    def test_encoding_of_x_plus_1_operation(self):
        instruction = CInstruction("A", "D+1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "011111")

    def test_encoding_of_y_plus_1_operation(self):
        instruction = CInstruction("A", "A+1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "110111")

    def test_encoding_of_x_minus_1_operation(self):
        instruction = CInstruction("A", "D-1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "001110")

    def test_encoding_of_y_minus_1_operation(self):
        instruction = CInstruction("A", "A-1", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "110010")

    def test_encoding_of_x_plus_y_operation(self):
        instruction = CInstruction("A", "D+A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "000010")

    def test_encoding_of_x_minus_y_operation(self):
        instruction = CInstruction("A", "D-A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "010011")

    def test_encoding_of_y_minus_x_operation(self):
        instruction = CInstruction("A", "A-D", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "000111")

    def test_encoding_of_x_and_y_operation(self):
        instruction = CInstruction("A", "D&A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "000000")

    def test_encoding_of_x_or_y_operation(self):
        instruction = CInstruction("A", "D|A", "")
        self.assertEqual(instruction.to_machine_code()[4:10], "010101")

    def test_encoding_of_destinations(self):
        instruction = CInstruction("", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "000")

        instruction = CInstruction("M", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "001")

        instruction = CInstruction("D", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "010")

        instruction = CInstruction("DM", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "011")

        instruction = CInstruction("A", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "100")

        instruction = CInstruction("AM", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "101")

        instruction = CInstruction("AD", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "110")

        instruction = CInstruction("ADM", "0", "")
        self.assertEqual(instruction.to_machine_code()[10:13], "111")

    def test_encoding_of_jumps(self):
        instruction = CInstruction("", "0", "")
        self.assertEqual(instruction.to_machine_code()[13:], "000")

        instruction = CInstruction("", "0", "JGT")
        self.assertEqual(instruction.to_machine_code()[13:], "001")

        instruction = CInstruction("", "0", "JEQ")
        self.assertEqual(instruction.to_machine_code()[13:], "010")

        instruction = CInstruction("", "0", "JGE")
        self.assertEqual(instruction.to_machine_code()[13:], "011")

        instruction = CInstruction("", "0", "JLT")
        self.assertEqual(instruction.to_machine_code()[13:], "100")

        instruction = CInstruction("", "0", "JNE")
        self.assertEqual(instruction.to_machine_code()[13:], "101")

        instruction = CInstruction("", "0", "JLE")
        self.assertEqual(instruction.to_machine_code()[13:], "110")

        instruction = CInstruction("", "0", "JMP")
        self.assertEqual(instruction.to_machine_code()[13:], "111")
