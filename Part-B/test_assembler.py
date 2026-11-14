#!/usr/bin/env python3
"""
Automated Test Suite for Part B Assembler
Tests assembler.py against official compare files:
- Add.asm  vs  Add.cmp
- Max.asm  vs  Max.cmp
- Rect.asm vs  Rect.cmp
- Pong.asm vs  Pong.cmp
Also validates that symbols.txt is generated as per extra feature (K mod 3 = 0).
"""

import os
import subprocess
import sys

TEST_FILES = [
    ("Add.asm", "Add.cmp"),
    ("Max.asm", "Max.cmp"),
    ("Rect.asm", "Rect.cmp"),
    ("Pong.asm", "Pong.cmp"),
]

def run_test(asm_file, cmp_file):
    base, _ = os.path.splitext(asm_file)
    hack_file = base + ".hack"
    symbols_file = "symbols.txt"

    print(f"\n[TESTING] {asm_file}...")

    # Run assembler
    cmd = [sys.executable, "assembler.py", asm_file, hack_file]
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        print(f"  [ERROR] Assembler failed with return code {res.returncode}")
        print(f"  {res.stderr.strip()}")
        return False

    if not os.path.isfile(hack_file):
        print(f"  [ERROR] Output file '{hack_file}' was not created.")
        return False

    if not os.path.isfile(symbols_file):
        print(f"  [ERROR] Extra feature 'symbols.txt' was not generated.")
        return False

    # Compare with .cmp
    with open(hack_file, "r") as f1, open(cmp_file, "r") as f2:
        out_lines = [l.strip() for l in f1 if l.strip()]
        cmp_lines = [l.strip() for l in f2 if l.strip()]

    if out_lines == cmp_lines:
        print(f"  [PASS] {hack_file} matches {cmp_file} 100% bit-for-bit!")
        print(f"         Total instructions: {len(out_lines)}")
        print(f"         symbols.txt generated ({os.path.getsize(symbols_file)} bytes)")
        return True
    else:
        print(f"  [FAIL] Output differs from {cmp_file}")
        print(f"         Generated lines: {len(out_lines)}, Expected lines: {len(cmp_lines)}")
        for i, (gen, exp) in enumerate(zip(out_lines, cmp_lines)):
            if gen != exp:
                print(f"         First mismatch at line {i+1}:")
                print(f"           Got:      {gen}")
                print(f"           Expected: {exp}")
                break
        return False


def main():
    part_b_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(part_b_dir)

    print("=" * 60)
    print(" Hack Assembler Verification Suite - Part B")
    print(" Student Roll No: 2501730142 | K = 42 | K mod 3 = 0")
    print("=" * 60)

    passed = 0
    total = len(TEST_FILES)

    for asm, cmp_f in TEST_FILES:
        if run_test(asm, cmp_f):
            passed += 1

    print("\n" + "=" * 60)
    print(f" RESULTS: {passed}/{total} tests passed successfully!")
    print("=" * 60)

    if passed == total:
        print("ALL TESTS PASSED! Your assembler is 100% compliant.")
        sys.exit(0)
    else:
        print("Some tests failed. Check the details above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
