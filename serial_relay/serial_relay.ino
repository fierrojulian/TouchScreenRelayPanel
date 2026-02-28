/*
  Mega + active-LOW relay boards (SunFounder 8ch x2)
  - Forces ALL relays OFF immediately at boot/reset (HIGH = OFF)
  - Uses a clean command map identical to your Python app:
      '0'/'1' -> relay 1 ON/OFF
      '2'/'3' -> relay 2 ON/OFF
      ...
      'Q'/'R' -> relay 14 ON/OFF
      'S'/'T' -> relay 15 ON/OFF
      'U'/'V' -> relay 16 ON/OFF
  - Ignores '\r' and '\n' so your "X\n" style sends don’t cause issues
  - Optional: 'X' turns ALL relays OFF (handy for an “All Off” button)
*/

const uint8_t relayPins[16] = {
  13, 12, 11, 10,  9,  8,  7,  6,
   5,  4,  3,  2, 22, 23, 24, 25
};

inline void relayOff(uint8_t idx) { digitalWrite(relayPins[idx], HIGH); } // ACTIVE-LOW
inline void relayOn (uint8_t idx) { digitalWrite(relayPins[idx], LOW);  } // ACTIVE-LOW

void allRelaysOff() {
  for (uint8_t i = 0; i < 16; i++) relayOff(i);
}

void setup() {
  // Set pins to OUTPUT and force relays OFF ASAP (before Serial begins)
  for (uint8_t i = 0; i < 16; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH); // OFF
  }

  Serial.begin(9600);

  // If you want to confirm boot, uncomment:
  // Serial.println("READY");
}

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    // Ignore line endings
    if (c == '\n' || c == '\r') continue;

    switch (c) {
      case '0': relayOn(0);  break;
      case '1': relayOff(0); break;

      case '2': relayOn(1);  break;
      case '3': relayOff(1); break;

      case '4': relayOn(2);  break;
      case '5': relayOff(2); break;

      case '6': relayOn(3);  break;
      case '7': relayOff(3); break;

      case '8': relayOn(4);  break;
      case '9': relayOff(4); break;

      case 'A': relayOn(5);  break;
      case 'B': relayOff(5); break;

      case 'C': relayOn(6);  break;
      case 'D': relayOff(6); break;

      case 'E': relayOn(7);  break;
      case 'F': relayOff(7); break;

      case 'G': relayOn(8);  break;
      case 'H': relayOff(8); break;

      case 'I': relayOn(9);  break;
      case 'J': relayOff(9); break;

      case 'K': relayOn(10);  break;
      case 'L': relayOff(10); break;

      case 'M': relayOn(11);  break;
      case 'N': relayOff(11); break;

      case 'O': relayOn(12);  break;
      case 'P': relayOff(12); break;

      case 'Q': relayOn(13);  break;
      case 'R': relayOff(13); break;

      case 'S': relayOn(14);  break;
      case 'T': relayOff(14); break;

      case 'U': relayOn(15);  break;
      case 'V': relayOff(15); break;

      // Optional: All OFF command (nice for safety)
      case 'X': allRelaysOff(); break;

      default:
        // Unknown command - ignore
        break;
    }
  }
}