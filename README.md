# Kabuki

Kabuki is a framework for coordinating inputs and outputs on a microcontroller running Micropython such as the Pyboard.

Kabuki can do simple things like connect buttons to lights. It can also do much more complex things like animate a robot with standard R/C servos. Kabuki borrows some ideas from neural networks and function programming such as the Monad. Kabuki lets you create a web of "nodes" that influence each other. You can chain, branch, and combine calculations that transform input values into the desired output values.

**Simple Example**

Let's start with a very simple example:

```python
import kabuki
from kabuki.pyboard.inputs import UserSwitchIn
from kabuki.pyboard.outputs import LedOut

kabuki.wire_output(UserSwitchIn(), LedOut(1))
kabuki.run()
```

After the requisite imports, we wire the user switch to an LED. `UserSwitchIn` is a wrapper around the Pyboard user switch. Likewise `LedOut` wraps the Pyboard LED class. Then we call `run()` which loops indefinitely and updates the outputs. Press the button, the light comes on, let go and it goes off. Pretty simple.

**Chaining Calculations**

Supose we want to "invert" the button and light, meaning the light is on unless you press the button. We can accomplish this by simply adding a "negate" operation to the input:

```python
import kabuki
from kabuki.pyboard.inputs import UserSwitchIn
from kabuki.pyboard.outputs import LedOut

sw_in = UserSwitchIn()
inverted = sw_in.neg()
kabuki.wire_output(inverted, LedOut(1))
kabuki.run()
```

Kabuki supports the basic arithmetic operations, add, subtract, multiply, divide, absolute value, and negate, plus filtering, mapping and more.

**Declarative Programming**

If you are a programmer, you are probably most familiar with imperative style coding. You keep track of "state" (variable values) and you make decisions (if/then/else) based on that state. In declarative-style programming you say what you want and let the system figure out how to do it. With Kabuki you decide how much "weight" to give to inputs and intermediate nodes as signals pass from input to output. In the end you have a relatively simple list that "defines" the relationships between inputs and outputs. There is no state to keep track of, no messy if/then branching to trip you up.

Suppose we want to use the accelerometer to control the 4 LEDs on the Pyboard. As you tilt the board from left to right we want to cycle the lights with the angle of the board, so full tilt left lights the blue light, full tilt right lights the red light. In between lights the yellow or green accordingly. Here's how you might do it in an imperative style:

```python
import pyb

acc = pyb.Accel()
leds = [ pyb.LED(1), pyb.LED(2), pyb.LED(3), pyb.LED(4) ]

while True:
    led_states = [ 0, 0, 0, 0 ]
    y = acc.y()
    if y < 0:
        if y < -10:
            active_led = 0
        else:
            active_led = 1
    else:
        if y < 10:
            active_led = 2
        else:
            active_led = 3
    led_states[active_led] = 255
    for (led, intensity) in zip(leds, led_states):
        led.intensity(intensity)
```

I'm not the greatest Python programmer, it might be possible to accomplish the goal with fewer lines, but this should suffice to illustrate the benefits of a declarative style. You probably don't find the above particularly difficult to read but if you are familiar with the phrase "cyclomatic complexity" you'll appreciate what Kabuki can do for you. Here's the same behavior coded with Kabuki:

First the imports:

```python
import kabuki
from kabuki.pyboard.inputs import AccelIn
from kabuki.pyboard.outputs import LedOut
```

Then we create an input:

`acc_in = AccelIn()`

`AccelIn` is a wrapper around the Pyboard accelerometer class. Next we register this input with Kabuki such that it is polled with every loop:

`kabuki.poll_input(acc_in)`

Output values are determined by following the chain backwards from the output through to the inputs or literal values and then calculating forward. The accelerometer has 3 axes that can all be read with one function call. If we were using all 3 axes we would not want to ask the accelerometer for the current values 3 times in one loop. So we poll the accelerometer as one input, then we create a "node" from the `y` axis:

`acc_y = acc_in.y()`

You could then find out the value of the `y` axis of the accelerometer with `acc_y.value`. But we don't need to to do that, we want to build our network of nodes out:

```python
tilt = 30
led_1_op = acc_y.filter_above(-tilt)
led_2_op = acc_y.retain_between(-tilt, 0)
led_3_op = acc_y.retain_between(1, tilt)
led_4_op = acc_y.filter_below(tilt)
```

The accelerometer provides values from 32 to -32 on each axis. `AccelIn` uses the method `filtered_xyz()` which sums consecutive values to smooth the signal a bit. We have 4 lights, 2 will be lit when tilted to the left and the other 2 will be lit when tilted to the right. The value of 30 was chosen here by experimentation to create 4 useful ranges: greater than 30, between 0 and 30, between 0 and -30 and less than 30.

The basic idea of a neural network is to connect "nodes" and have them influence each other. While nodes can have any value that supports the operations you wish to perform, for the most part we're talking about numbers and an occasional `True` or `False`. The filter and retain operators above don't drop values from a stream but choose between the current value and zero with the expectation that zero will have no influence (or will completely supress some signal).

Values above -30 are changed to zero, values between -30 and 0 are kept (other values are changed to zero), values between 0 and 30 are kept, and values below 30 are changed to zero. These operations are then applied to the outputs:

```python
kabuki.wire_output(led_1_op, LedOut(1))
kabuki.wire_output(led_2_op, LedOut(2))
kabuki.wire_output(led_3_op, LedOut(3))
kabuki.wire_output(led_4_op, LedOut(4))
```

`LedOut` works by interpreting a zero or False value to mean "turn the light" off. Any other values will turn the light on. Finally, we kick off the main loop:

`kabuki.run()`

If the `y` axis of the accelerometer reads 8, all of the LED operators will yield a value of zero except for `led_3_op` which yields 8, therefore all LEDs will be off except LED 3 which is on. Here's the entire example:

```python
import kabuki
from kabuki.pyboard.inputs import AccelIn
from kabuki.pyboard.outputs import LedOut


acc_in = AccelIn()
kabuki.poll_input(acc_in)
acc_y = acc_in.y()

tilt = 30
led_1_op = acc_y.filter_above(-tilt)
led_2_op = acc_y.retain_between(-tilt, 0)
led_3_op = acc_y.retain_between(1, tilt)
led_4_op = acc_y.filter_below(tilt)

kabuki.wire_output(led_1_op, LedOut(1))
kabuki.wire_output(led_2_op, LedOut(2))
kabuki.wire_output(led_3_op, LedOut(3))
kabuki.wire_output(led_4_op, LedOut(4))

kabuki.run()
```

It's not a whole lot shorter but it's very easy to read and reason about. 

**Rapid Development**

If you've done any Arduino programming in C, you probably find the Pyboard development cycle a breeze. Kabuki makes things even better. Install Kabuki on your Pyboard with a special `main.py` file. Then write your node definition in the file `nodes.py`. Reboot the Pyboard and the main routine runs and reads your definition. Make a change to `nodes.py` and simply press the user switch and the new definition replaces the old and begins running right away. No need to eject/unmount and reboot the Pyboard. If your definition file crashes you'll get "police car" blinking lights much like the default Pyboard crash routine but again, just fix `nodes.py` and press the user button and you're back in business.

See the wiki for more examples and the useful operators available.


