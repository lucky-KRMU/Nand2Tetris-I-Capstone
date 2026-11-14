#!/usr/bin/env python3
"""
Hack Assembler (Part B)
Nand to Tetris - I (ETCCNT301)
Student Roll No: 2501730142 (K = 42, K mod 3 = 0)
Extra Feature: Save all labels and variables with their addresses in symbols.txt
"""

import sys
import os

# Predefined symbols
PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    **{f"R{i}": i for i in range(16)},
}

# Computation codes (7 bits: a c1 c2 c3 c4 c5 c6)
COMP_TABLE = {
    # a = 0 (ALU operates on D and A)
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "1+D": "0011111",
    "A+1": "0110111",
    "1+A": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",
    # a = 1 (ALU operates on D and M)
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "1+M": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101",
}

# Destination codes (3 bits: d1 d2 d3)
DEST_TABLE = {
    "": "000",
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "AMD": "111",
    "ADM": "111",
    "MAD": "111",
    "MDA": "111",
    "DAM": "111",
    "DMA": "111",
}

# Jump codes (3 bits: j1 j2 j3)
JUMP_TABLE = {
    "": "000",
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def clean_line(raw_line: str) -> str:
    """Strip comments and surrounding whitespace."""
    comment_pos = raw_line.find("//")
    if comment_pos != -1:
        raw_line = raw_line[:comment_pos]
    return raw_line.strip().replace(" ", "")


class HackAssembler:
    def __init__(self, asm_path: str):
        self.asm_path = asm_path
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.labels = {}      # symbol -> ROM address
        self.variables = {}   # symbol -> RAM address
        self.next_var_addr = 16
        self.instructions = []

    def first_pass(self):
        """First reading: remove comments/blank lines, record label addresses."""
        rom_address = 0
        with open(self.asm_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                cleaned = clean_line(line)
                if not cleaned:
                    continue

                if cleaned.startswith("(") and cleaned.endswith(")"):
                    label = cleaned[1:-1]
                    self.symbol_table[label] = rom_address
                    self.labels[label] = rom_address
                else:
                    self.instructions.append(cleaned)
                    rom_address += 1

    def second_pass(self) -> list:
        """Second reading: translate every instruction into 16-bit binary."""
        binary_lines = []

        for inst in self.instructions:
            if inst.startswith("@"):
                # A-instruction
                val_str = inst[1:]
                if val_str.isdigit():
                    addr = int(val_str)
                else:
                    if val_str in self.symbol_table:
                        addr = self.symbol_table[val_str]
                    else:
                        addr = self.next_var_addr
                        self.symbol_table[val_str] = addr
                        self.variables[val_str] = addr
                        self.next_var_addr += 1

                binary_lines.append(f"{addr:016b}")
            else:
                # C-instruction: [dest=]comp[;jump]
                dest_part = ""
                comp_part = inst
                jump_part = ""

                if "=" in comp_part:
                    dest_part, comp_part = comp_part.split("=", 1)

                if ";" in comp_part:
                    comp_part, jump_part = comp_part.split(";", 1)

                if comp_part not in COMP_TABLE:
                    raise ValueError(f"Invalid computation instruction: '{comp_part}' in line: {inst}")
                if dest_part not in DEST_TABLE:
                    raise ValueError(f"Invalid destination: '{dest_part}' in line: {inst}")
                if jump_part not in JUMP_TABLE:
                    raise ValueError(f"Invalid jump: '{jump_part}' in line: {inst}")

                comp_bits = COMP_TABLE[comp_part]
                dest_bits = DEST_TABLE[dest_part]
                jump_bits = JUMP_TABLE[jump_part]

                binary_lines.append(f"111{comp_bits}{dest_bits}{jump_bits}")

        return binary_lines

    def save_symbols(self, symbols_path: str):
        """
        Extra Feature (K mod 3 == 0):
        Save all labels and variables with their addresses in symbols.txt.
        """
        with open(symbols_path, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("Hack Assembler Symbol Table (K mod 3 = 0)\n")
            f.write("=" * 50 + "\n\n")

            f.write("--- USER-DEFINED LABELS (ROM Addresses) ---\n")
            if self.labels:
                for label, addr in sorted(self.labels.items(), key=lambda x: x[1]):
                    f.write(f"  (LABEL) {label:<20} -> ROM[{addr}] (0x{addr:04X})\n")
            else:
                f.write("  (No user labels defined)\n")

            f.write("\n--- USER-DEFINED VARIABLES (RAM Addresses) ---\n")
            if self.variables:
                for var, addr in sorted(self.variables.items(), key=lambda x: x[1]):
                    f.write(f"  (VAR)   {var:<20} -> RAM[{addr}] (0x{addr:04X})\n")
            else:
                f.write("  (No user variables defined)\n")

            f.write("\n--- COMPLETE RESOLVED SYMBOL TABLE ---\n")
            for sym, addr in sorted(self.symbol_table.items(), key=lambda x: (x[1], x[0])):
                category = "PREDEFINED"
                if sym in self.labels:
                    category = "LABEL"
                elif sym in self.variables:
                    category = "VARIABLE"
                f.write(f"  {sym:<20} : {addr:<6} [{category}]\n")

    def assemble(self, output_path: str = None, symbols_path: str = None) -> str:
        self.first_pass()
        binary_lines = self.second_pass()

        if output_path is None:
            base, _ = os.path.splitext(self.asm_path)
            output_path = base + ".hack"

        with open(output_path, "w", encoding="utf-8") as f:
            for b in binary_lines:
                f.write(b + "\n")

        if symbols_path is None:
            out_dir = os.path.dirname(output_path) or "."
            symbols_path = os.path.join(out_dir, "symbols.txt")

        self.save_symbols(symbols_path)
        return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <source.asm> [output.hack]")
        sys.exit(1)

    asm_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isfile(asm_file):
        print(f"Error: File '{asm_file}' not found.")
        sys.exit(1)

    assembler = HackAssembler(asm_file)
    hack_file = assembler.assemble(output_path=out_file)
    print(f"Assembly successful:")
    print(f"  Source:  {asm_file}")
    print(f"  Output:  {hack_file}")
    print(f"  Symbols: symbols.txt generated successfully")


if __name__ == "__main__":
    main()
