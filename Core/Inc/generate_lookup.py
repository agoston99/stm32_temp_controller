# SETUP -- DEFINE CONSTANTS HERE

bits = 12               # ADC resolution (bits)
pullup = 4700           # Pullup resistor value (Ohms)
base_temperature = 25   # Thermistor base temperature (Celsius)
thermistor = 100000     # Thermistor value at base temperature (Ohms)
beta = 3950             # Thermistor beta
file = "thermistor_lookup.h"

# ------------------------------
# SCRIPT - DO NOT MODIFY

count = 2 ** bits

resistances = []

for i in range(count):
    resistances.append(float(i) * pullup / float(count - i))

temperatures = []

import math

for i in range(count):
    if(resistances[i] == 0):
        temperatures.append(math.inf)
    else:
        value = ( 1.0 / ( (-1.0 * math.log(float(thermistor) / float(resistances[i])) / float(beta)) + ( 1.0 / (base_temperature + 273.15) ) ) ) - 273.15
        temperatures.append(value)


# import numpy as np
# x = range(count)
# import matplotlib.pyplot as plt

# plt.plot(x, resistances)
# plt.plot(x, temperatures)
# plt.show()

outputfile = open(file, "w")

outputfile.write("#ifndef INC_THERMISTOR_LOOKUP_H_\n#define INC_THERMISTOR_LOOKUP_H_\n\n#include <stdint.h>\n\nconst uint16_t thermistor_value_lookup[] = {")

cnt = 0

for value in temperatures:
    if(cnt == 0):
        cnt = 16
        outputfile.write("\n\t")
    cnt = cnt - 1
    if (value == math.inf):
        outputfile.write(str(65535) + ", ")
    else:
        val = int(round(value, 1) * 10)
        if(val > 65536):
            val = 65536
        outputfile.write(str(val) + ", ")

        

outputfile.write("\n};\n\n#endif")