# XBoxController Class Usage

The `XBoxController` class is a Python class that provides an interface to interact with an Xbox controller. It uses the `pygame` library to handle the controller inputs.

## Attributes

- `sticks_threshold` (float): The threshold for the stick values to trigger the callback.
- `DEBUG` (bool): A flag to enable debug mode.

## Methods

- `__init__`: Initializes the pygame library and the controller object.
- `connect`: Connects to the first controller, in case it was disconnected since initialization.
- `setCallback(key, callback)`: Sets the callback for a specific button. Possible keys are: "x", "y", "a", "b", "left_trigger", "right_trigger", "left_bumper", "right_bumper", "back", "start", "left_stick", "right_stick", "left_stick_button", "right_stick_button", "hat".
- `setCallbacks(callbacks)`: Sets the callbacks for the event listener.
- `setHz(hz)`: Sets the frequency of the event listener.
- `setDebugCallbacks()`: Sets the debug callbacks to print the events to the console.
- `runListener()`: Starts a loop that listens for events. (*NOTE: This method should be executed in a separated thread*)

## Callbacks

Callbacks are functions that are called when a specific event occurs. In the context of the `XBoxController` class, these events are button presses, stick movements, trigger pulls, and hat movements.

Here are examples of how to define callbacks for each type of event:

- Button callbacks: The callback function must accept a single parameter, which is the state of the button (0 for pressed, 1 for released). 

```python
def myCallback(x): 
  print("Button pressed" if x == 0 else "Button released")
```

- Stick callbacks: The callback function must accept two parameters, the first one is the axis (0 for x, 1 for y) and the second one is the value of the stick [-1.0, 1.0]. 

```python
def myCallback(axis, value): 
  print(f"Stick [{'y' if axis else 'x'}]: {value:.2f}")
```

- Trigger callbacks: The callback function must accept a single parameter, which is the value of the trigger [-1.0, 1.0]. 

```python
def myCallback(value): 
  print(f"Trigger: {value:.2f}")
```

- Hat callback: The callback function must accept a single parameter, which is the value of the hat (tuple of two integers [[-1, 1], [-1, 1]]). 

```python
def myCallback(value): 
  print(f"Hat: {value}")
```

## Example Usage

### Basic example

```python
# Create an instance of the XBoxController class
controller = XBoxController()

# Define a callback for the "a" button
def a_button_callback(state):
  print("A button pressed" if state == 0 else "A button released")

# Set the callback for the "a" button
controller.setCallback("a", a_button_callback)

# Start the event listener
controller.runListener()
```

> This will print "A button pressed" when the "a" button is pressed and "A button released" when it is released.

### Other examples

<details>
<summary>Advanced example</summary>

> We this code we can create a callback for the sticks, also set the speed of the event listener to 60hz and the threshold for the sticks to 0.2

```python
# Create an instance of the XBoxController class
controller = XBoxController()

# Define a callback for the "a" button
def a_button_callback(state):
  print("A button pressed" if state == 0 else "A button released")

# Define a callback for the sticks
def l_stick_callback(axis, value):
  print(f"Left Stick [{'y' if axis else 'x'}]: {value:.2f}")
def r_stick_callback(axis, value):
  print(f"Right Stick [{'y' if axis else 'x'}]: {value:.2f}")

# Define a callback for the triggers
def l_trigger_callback(value):
  print(f"Left Trigger: {value:.2f}")
def r_trigger_callback(value):
  print(f"Right Trigger: {value:.2f}")

# Define a callback for the hat
def hat_callback(value):
  print(f"Hat: {value}")

# Set the callbacks
controller.setCallback("a", a_button_callback)
controller.setCallback("left_stick", l_stick_callback)
controller.setCallback("right_stick", r_stick_callback)
controller.setCallback("left_trigger", l_trigger_callback)
controller.setCallback("right_trigger", r_trigger_callback)
controller.setCallback("hat", hat_callback)

# Set the speed of the event listener to 60hz
controller.setHz(60)
# Set the threshold for the sticks to 0.2
controller.sticks_threshold = 0.3

controller.runListener()
```
</details>


<details>
<summary>Multithreading example</summary>

> This code will run the event listener in a separate thread, so the main thread can do other stuff while the event listener is running.

```python
import threading
from xboxcontroller import XBoxController

# Define a callback for the "a" button
def a_button_callback(state):
  print("A button pressed" if state == 0 else "A button released")

# Create an instance of the XBoxController class
controller = XBoxController()

# Set the callback for the "a" button
controller.setCallback("a", a_button_callback)

# Define a function to run the event listener in a separate thread
def run_listener():
  controller.runListener()

# Start the event listener in a separate thread
listener_thread = threading.Thread(target=run_listener)
listener_thread.start()

# Do other stuff in the main thread while the event listener is running
while True:
  print("Main thread is doing other stuff...")
```

</details>


<details>
<summary>Multiprocessing example</summary>

> This code will run the event listener in a separate process, so the main process can do other stuff while the event listener is running.

```python
import multiprocessing
from xboxcontroller import XBoxController

# Define a callback for the "a" button
def a_button_callback(state):
  print("A button pressed" if state == 0 else "A button released")

# Create an instance of the XBoxController class
controller = XBoxController()

# Set the callback for the "a" button
controller.setCallback("a", a_button_callback)

# Define a function to run the event listener in a separate process
def run_listener():
  controller.runListener()

# Start the event listener in a separate process
listener_process = multiprocessing.Process(target=run_listener)
listener_process.start()

# Do other stuff in the main process while the event listener is running
while True:
  print("Main process is doing other stuff...")
```

</details>