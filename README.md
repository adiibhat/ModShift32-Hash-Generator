ModShift32 Hash Generator 🔐

A custom Python hashing algorithm (modshift32_hash) with a PyQt5 GUI.
This project demonstrates how character manipulation, modular arithmetic, and bit mixing can be combined to produce a fixed-length hash.

✨ Features

Custom ModShift32 hashing algorithm (32-character hex digest)

Side-by-side comparison with SHA-256

GUI built with PyQt5

Avalanche effect: small input change → big hash difference

Handles empty and long strings gracefully

⚙️ How the Algorithm Works
1. Input Handling

Empty strings are replaced with "empty_string" to avoid null input.

2. Initialization

Internal state (hash_value) starts at 0.

Uses a prime multiplier (31) and modular arithmetic to maintain 32-bit values.

3. Character Absorption

Each character is:

Converted to ASCII

Shifted left (0–7 bits depending on position)

Mixed into the state with multiplication and XOR operations

4. Mixing Rounds

Three nonlinear rounds of bit-shifts and XORs spread input entropy across all bits.

5. Finalization

The state is transformed into four 32-bit segments.

Each segment undergoes additional mixing, then converted to 8 hex characters.

Concatenation yields a fixed 32-character hexadecimal hash.
