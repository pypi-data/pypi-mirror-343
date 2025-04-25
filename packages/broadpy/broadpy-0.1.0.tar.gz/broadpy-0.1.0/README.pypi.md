# BRoaDpy

BRoaD API class for python.

Software development support library for BRoaD I/III in Python.

* Programming language: Python 3.9+
* License: MIT License

## What is BRoaD

BROAD is a laboratory digital signal processing device developed by Bee Beans Technologies Inc.
With BRoaD, you can easily generate, synthesize, and distribute a variety of logic signals in your lab.

There are two types of BRoaD: [BRoaD I](https://www.bbtech.co.jp/en/products/broad-1-new/) and [BRoaD III](https://www.bbtech.co.jp/en/products/broad-v3/).


## What is BRoaDpy

BRoaD allows you to design digital signals using a dedicated GUI application. The BRoaDpy API can be used, for example, to read signal processing counters configured in BRoaD from a Python program.

## How to Use
Use the `BRoaD1` class when targeting BRoaD I, and the `BRoaD3` class when targeting BRoaD III.

```
from broadpy import BRoaD1

mybroad = BRoaD1('192.168.10.16', 24, 4660) # Use the BRoaD1 or BRoaD3 class according to the device targeting.
mybroad.connect() # Initialize the connection with BRoaD.
```

Use `disconnect` to end use.


### Measure Counter
Measure Counter Logic can be controlled (Connect, Start, Stop, Disconnect)  by `broadpy`.
`connect_measure_counter` establishes a TCP connection with BRoaD, and when data is received, the functions specified by `set_counter_function` and `set_raw_function` are executed.
* `set_counter_function` : The arguments are the Measure Counter number and the measurement value.
    * If the SRC setting of Measure Counter is Gate Time, True Time, the measurement value is nsec.
    * Otherwise the measurement value is a count of the number of pulses.
* `set_raw_function` : The argument is raw data (8 bytes).

```
def sample_counter_function(id, count):
    """
    Callback function to receive decoded ID and counter value
    """
    print(f"counter {id}:{count}")

def sample_raw_function(counter_byte:bytes ):
    """
    Callback function to receive raw byte data
    """
    print(f"counter bytes : {counter_byte.hex()}")

mybroad.connect_measure_counter() # Establish a TCP connection with BRoaD.
mybroad.set_counter_function(sample_counter_function) # Specifies the function to execute when TCP data is received.
mybroad.set_raw_function(sample_raw_function) # Specifies the function to execute when TCP data is received.(raw data)
```

If the Gate setting is User Control, you can control the start and end of measurement with `start_read` and `stop_read`.
```
mybroad.start_read(0) # Start measurement Measure Counter:0.
mybroad.stop_read(0) # End measurement  MeasureCounter:0. TCP data is sent from BRoaD, and the functions specified by set_counter_function and set_raw_function are executed.
```

`disconnect_measure_counter` closes the TCP connection.

```
mybroad.disconnect_measure_counter()
```


### User Control
The User Control function of BRoaD III can be read and write to ON/OFF by `broadpy`.

```
from broadpy import BRoaD3

mybroad3 = BRoaD3('192.168.10.16', 24, 4660) # The User Control function is only available on BRoaD III.
mybroad3.connect()
mybroad3.user_control_value = mybroad3.read_user_control(0) # Read the current User Control (ON:True, OFF:False) of INPUT0 from BRoaD III.
mybroad3.user_control(0, True) # Change the User Control value of INPUT0 to ON: True, OFF: False.

```

## Version History

0.1.0 - First release.