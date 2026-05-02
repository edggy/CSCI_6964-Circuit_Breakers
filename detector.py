#Heuristic Detector
#checks if file contains "clk" which is a common variable hardware trojans use to keep track of time
detected_t1 = 0
detected_alu_t2 = 0
detected_shift_t2 = 0
detected_demo_alu = 0
detected_demo_shift = 0

#Check alu_simple T1
print("Checking alu_simple T1 for variable 'clk':")
with open('github/CSCI_6964-Circuit_Breakers/trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT1_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        if 'clk' in line and 'input' in line:
            print("Found on line ", line_number)
            detected_t1 = 1
            break   

#Check alu_simple T2
print("Checking alu_simple T2 for variable 'clk':")
with open('github/CSCI_6964-Circuit_Breakers/trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT2_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        if 'clk' in line and 'input' in line:
            print("Found on line ", line_number)
            detected_alu_t2 = 1
            break   

#Check shift_reg T2
print("Checking shift_reg T2 for variable 'clk':")
with open('github/CSCI_6964-Circuit_Breakers/trojaned_outputs/gpt-5-nano/shift_reg/shift_reg_HT2_gpt-5-nano_A1.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        if 'clk' in line and 'input' in line:
            print("Found on line ", line_number)
            detected_shift_t2 = 1
            break   

#Check demo alu_simple
print("Checking demo alu_simple for variable 'clk':")
with open('github/CSCI_6964-Circuit_Breakers/demo_designs/alu_simple.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        if 'clk' in line and 'input' in line:
            print("Found on line ", line_number)
            detected_demo_alu= 1
            break   

#Check demo shift_reg
print("Checking shift_reg T2 for variable 'clk':")
with open('github/CSCI_6964-Circuit_Breakers/demo_designs/shift_reg.v', 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        if 'clk' in line and 'input' in line:
            print("Found on line ", line_number)
            detected_demo_shift = 1
            break   

#Results
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