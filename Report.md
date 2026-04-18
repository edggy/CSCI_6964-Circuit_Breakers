# Task 1. Taxonomy + safety 

## Locate the Vulnerability Definitions
Identify the four Trojan categories (T1–T4) used in this lab. 
These are defined in the `GHOST_Trojan_GPT.py` script and referenced in the `Hardware_Trojan_Insertion_Lab.ipynb` notebook.
- T1: Change Functionality: Subtly alter logic to produce incorrect results under specific conditions.
- T2: Leak Information: Design a covert data transmission mechanism that activates upon detecting a specific signal pattern.
- T3: Denial of Service: Introduce a condition that temporarily disables the module, triggered by a rare sequence of events.
- T4: Performance Degradation: Implement a continuously running shift register or accumulator to increase power consumption without affecting primary functionality.

## Taxonomy Summary
### T1: Change Functionality
Changes the intended behavior of the hardware so it produces wrong outputs, but only
when a particular condition is met. In hardware security terms, it is dangerous
because the design appears normal most of the time, which makes the malicious logic
harder to notice during ordinary testing.
#### Example:
An arithmetic module behaves normally for almost all inputs, but when it receives a rare
combination of operands, it flips one bit of the result, so the output is slightly wrong.

### T2: Leak Information
Designed to covertly expose internal data by encoding or transmitting it when a specific
trigger pattern occurs. Its main security risk is that it can quietly
turn the circuit into a hidden communication channel without visibly breaking the
primary function of the module.
#### Example:
A crypto-related module works correctly, but after a hidden trigger sequence appears on
its inputs, it starts modulating an otherwise unimportant output signal so that secret
internal data can be inferred over time.

### T3: Denial of Service
Temporarily or permanently prevents the module from operating correctly after a trigger.
From a hardware security perspective, the goal is not to corrupt outputs directly, 
but to disrupt availability and make the system unreliable or unresponsive at selected times.
#### Example:
A controller runs normally until it observes a rare sequence of control states, after
which it forces itself into a stall condition for several cycles and stops responding
to valid inputs.

### T4: Performance Degradation
Adds extra activity, such as a continuously running shift register or
accumulator, that does not change the functional outputs but wastes power or hardware
resources. It is a subtle form of attack because the circuit still appears correct
functionally, while efficiency, power use, or long-term reliability is degraded.
#### Example:
Extra hidden logic continuously toggles internal registers every clock cycle even though
those registers do not affect the module’s real outputs.

## Step 3: Define and Document Your Safety Rule
### "We will never commit API keys or secrets (such as those in the .secrets/ folder) to any public or private repository."

The `./.secrets/` directory was created and all of its contents have been added to the `.gitignore` file.

# Task 2. Single-sample analysis
## Suspected trigger condition
## Payload effect
## Where the RTL was modified
For this part, we chose to look at `demo_designs/alu_simple.v` and `trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT1_gpt-5-nano_A1.v` for the individual analysis.

# Task 3. Cross-sample comparison

# Task 4. Validation & testing
