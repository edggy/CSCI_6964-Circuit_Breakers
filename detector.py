# Heuristic Detector
# Checks if file contains "clk" plus suspicious Trojan-like words.
# This avoids flagging a normal demo file just because it has clk.

detected_t1 = 0
detected_alu_t2 = 0
detected_shift_t2 = 0
detected_demo_alu = 0
detected_demo_shift = 0

suspicious_words = ['counter', 'timer', 'trigger', 'payload', 'trojan', 'delay', 'cycle']

# Check alu_simple T1
print("Checking alu_simple T1 for clk-based trojan pattern:")
found_clk = 0
found_suspicious = 0

with open('trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT1_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.split('//', 1)[0]
        lower_line = clean_line.lower()

        if 'clk' in lower_line and 'input' in lower_line:
            print("Found clk input on line", line_number)
            found_clk = 1

        if any(word in lower_line for word in suspicious_words):
            print("Found suspicious word on line", line_number)
            found_suspicious = 1

if found_clk and found_suspicious:
    detected_t1 = 1


# Check alu_simple T2
print("Checking alu_simple T2 for clk-based trojan pattern:")
found_clk = 0
found_suspicious = 0

with open('trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT2_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.split('//', 1)[0]
        lower_line = clean_line.lower()

        if 'clk' in lower_line and 'input' in lower_line:
            print("Found clk input on line", line_number)
            found_clk = 1

        if any(word in lower_line for word in suspicious_words):
            print("Found suspicious word on line", line_number)
            found_suspicious = 1

if found_clk and found_suspicious:
    detected_alu_t2 = 1


# Check shift_reg T2
print("Checking shift_reg T2 for clk-based trojan pattern:")
found_clk = 0
found_suspicious = 0

with open('trojaned_outputs/gpt-5-nano/shift_reg/shift_reg_HT2_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.split('//', 1)[0]
        lower_line = clean_line.lower()

        if 'clk' in lower_line and 'input' in lower_line:
            print("Found clk input on line", line_number)
            found_clk = 1

        if any(word in lower_line for word in suspicious_words):
            print("Found suspicious word on line", line_number)
            found_suspicious = 1

if found_clk and found_suspicious:
    detected_shift_t2 = 1


# Check demo alu_simple
print("Checking demo alu_simple for clk-based trojan pattern:")
found_clk = 0
found_suspicious = 0

with open('demo_designs/alu_simple.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.split('//', 1)[0]
        lower_line = clean_line.lower()

        if 'clk' in lower_line and 'input' in lower_line:
            print("Found clk input on line", line_number)
            found_clk = 1

        if any(word in lower_line for word in suspicious_words):
            print("Found suspicious word on line", line_number)
            found_suspicious = 1

if found_clk and found_suspicious:
    detected_demo_alu = 1


# Check demo shift_reg
print("Checking demo shift_reg for clk-based trojan pattern:")
found_clk = 0
found_suspicious = 0

with open('demo_designs/shift_reg.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.split('//', 1)[0]
        lower_line = clean_line.lower()

        if 'clk' in lower_line and 'input' in lower_line:
            print("Found clk input on line", line_number)
            found_clk = 1

        if any(word in lower_line for word in suspicious_words):
            print("Found suspicious word on line", line_number)
            found_suspicious = 1

if found_clk and found_suspicious:
    detected_demo_shift = 1


# Results
print("\nRESULTS:")

if detected_demo_alu:
    print("ALU_SIMPLE DEMO: TROJAN PATTERN FOUND ✅")
else:
    print("ALU_SIMPLE DEMO: TROJAN PATTERN NOT FOUND ❌")

if detected_demo_shift:
    print("SHIFT_REG DEMO: TROJAN PATTERN FOUND ✅")
else:
    print("SHIFT_REG DEMO: TROJAN PATTERN NOT FOUND ❌")

if detected_t1:
    print("ALU_SIMPLE T1: TROJAN PATTERN FOUND ✅")
else:
    print("ALU_SIMPLE T1: TROJAN PATTERN NOT FOUND ❌")

if detected_alu_t2:
    print("ALU_SIMPLE T2: TROJAN PATTERN FOUND ✅")
else:
    print("ALU_SIMPLE T2: TROJAN PATTERN NOT FOUND ❌")

if detected_shift_t2:
    print("SHIFT_REG T2: TROJAN PATTERN FOUND ✅")
else:
    print("SHIFT_REG T2: TROJAN PATTERN NOT FOUND ❌")

total = 5
total_found = detected_t1 + detected_alu_t2 + detected_shift_t2 + detected_demo_alu + detected_demo_shift

print("\nFound trojan patterns in", total_found, "/", total, "files")