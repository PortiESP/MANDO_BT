import pygame


class XBoxController():
  """
  A class that represents an Xbox controller and provides methods to interact with it.

  Attributes:
    - sticks_threshold (float): The threshold for the stick values to trigger the callback.
    - DEBUG (bool): A flag to enable debug mode.

  Methods:
    - __init__(): Initializes the pygame library and the controller object.
    - connect(): Connects to the first controller, in case it was disconnected since initialization.
    - setCallback(key, callback): Sets the callback for a specific button. Posible keys: ["x", "y", "a", "b", "left_trigger", "right_trigger", "left_bumper", "right_bumper", "back", "start", "left_stick", "right_stick", "left_stick_button", "right_stick_button", "hat"]
    - setCallbacks(callbacks): Sets the callbacks for the event listener.
    - setHz(hz): Sets the frequency of the event listener.
    - runListener(): Starts a loop that listens for events.
    - setDebugCallbacks(): Sets the debug callbacks to print the events to the console.

  How to define a callback:
    - Button callbacks: The callback function must accept a single parameter, which is the state of the button (0 for pressed, 1 for released). I.E.: def myCallback(x): print("Button pressed" if x == 0 else "Button released")
    - Stick callbacks: The callback function must accept two parameters, the first one is the axis (0 for x, 1 for y) and the second one is the value of the stick [-1.0, 1.0]. I.E.: def myCallback(axis, value): print(f"Stick [{"y" if axis else "x"}]: {value:.2f}")
    - Trigger callbacks: The callback function must accept a single parameter, which is the value of the trigger [-1.0, 1.0]. I.E.: def myCallback(value): print(f"Trigger: {value:.2f}")
    - Hat callback: The callback function must accept a single parameter, which is the value of the hat (tuple of two integers [[-1, 1], [-1, 1]]). I.E.: def myCallback(value): print(f"Hat: {value}")

  """

    # Button mappings
  BUTTONS = {0: "a", 1: "b", 2: "x", 3: "y", 4: "left_bumper", 5: "right_bumper", 6: "back", 7: "start", 8: "left_stick_button", 9: "right_stick_button"}
  # Axis mappings
  AXIS = {0: "left_stick_x", 1: "left_stick_y", 2: "right_stick_x", 3: "right_stick_y", 4: "left_trigger", 5: "right_trigger"}


  _controller = None  # Controller object
  _callbacks = {  # Callbacks for each button
    "x": None,
    "y": None,
    "a": None,
    "b": None,
    "left_trigger": None,
    "right_trigger": None,
    "left_bumper": None,
    "right_bumper": None,
    "back": None,
    "start": None,
    "left_stick": None,
    "right_stick": None,    
    "left_stick_button": None,
    "right_stick_button": None,    
    "hat": None
  }
  __clock = None  # Clock object for the event listener
  __hz = 20  # Frequency of the event listener
  sticks_threshold = 0.2  # Threshold for the stick values

  DEBUG = False  # Debug flag

  # Constructor
  def __init__(self):
    """
    Initializes the pygame library and the controller object.
    """

    pygame.init()

    if pygame.joystick.get_count() < 1:
      raise(IOError, "No controller detected")
    else:
      self._controller = pygame.joystick.Joystick(0)
      self._controller.init()

      self.__clock = pygame.time.Clock()


  def connect(self):
    """
    Connects to the first controller, in case it was disconnected since initialization.
    """

    if pygame.joystick.get_count() < 1:
        return False
    self._controller = pygame.joystick.Joystick(0)
    self._controller.init()

  def setCallback(self, key, callback):
    """
    Sets the callback for a specific button.

    Args:
    key (str): The name of the button.
    callback (function): The function to be called when the button is pressed.
    """

    self._callbacks[key] = callback

  def setCallbacks(self, callbacks):
    """
    Sets the callbacks for the event listener.

    Args:
    callbacks (dict): A dictionary with the callbacks for each button.
    """

    self._callbacks = callbacks

  def setHz(self, hz):
    """
    Sets the frequency of the event listener.

    Args:
    hz (int): The frequency in Hz.
    """
    self.__hz = hz

  def runListener(self):
    """
    Starts a loop that listens for events.
    """

    while (1):
      self.__clock.tick(self.__hz)

      for event in pygame.event.get():
        self.__handleEvent(event)

  def __handleEvent(self, event):
    """
    Handles a single event and triggers the appropriate callback.

    Args:
    event (pygame.event.Event): The event to be handled.
    """

    # DEBUG - Print the event details
    if self.DEBUG: 
      print(event)
      print("[DEBUG] >>> ", end="")
      if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
        print(self.BUTTONS[event.button])
      elif event.type == pygame.JOYAXISMOTION:
        print(self.AXIS[event.axis])
      elif event.type == pygame.JOYHATMOTION:
        print("hat", event.value)
      
    # PARSE EVENT - Trigger the appropriate callback
    # Pressing a button down
    if event.type == pygame.JOYBUTTONDOWN:
      if self._callbacks[self.BUTTONS[event.button]]:
        (self._callbacks[self.BUTTONS[event.button]])(0)
    # Releasing a button
    elif event.type == pygame.JOYBUTTONUP:
      if self._callbacks[self.BUTTONS[event.button]]:
        self._callbacks[self.BUTTONS[event.button]](1)
    # Moving a stick or trigger
    elif event.type == pygame.JOYAXISMOTION:
      # Left stick
      if (event.axis == 0 or event.axis == 1) and abs(event.value) > self.sticks_threshold:
        if event.axis == 0 and self._callbacks["left_stick"]: self._callbacks["left_stick"](0, event.value)
        elif event.axis == 1 and self._callbacks["left_stick"]: self._callbacks["left_stick"](1, -event.value)
      # Right stick
      elif (event.axis == 2 or event.axis == 3) and abs(event.value) > self.sticks_threshold:
        if event.axis == 2 and self._callbacks["right_stick"]: self._callbacks["right_stick"](0, event.value)
        elif event.axis == 3 and self._callbacks["right_stick"]: self._callbacks["right_stick"](1, -event.value)
      # Left trigger
      elif event.axis == 4:
        if self._callbacks["left_trigger"]: self._callbacks["left_trigger"](event.value)
      # Right trigger
      elif event.axis == 5:
        if self._callbacks["right_trigger"]: self._callbacks["right_trigger"](event.value)
    # Moving the hat
    elif event.type == pygame.JOYHATMOTION:
      if self._callbacks["hat"]: self._callbacks["hat"](event.value)


  # Debug methods
  def setDebugCallbacks(self):
    """
    Sets the debug callbacks to print the events to the console.
    """

    self.setCallbacks({
      "x": lambda x: print(f"X {"pressed" if x == 0 else "released"}"),
      "y": lambda x: print(f"Y {"pressed" if x == 0 else "released"}"),
      "a": lambda x: print(f"A {"pressed" if x == 0 else "released"}"),
      "b": lambda x: print(f"B {"pressed" if x == 0 else "released"}"),
      "left_trigger": lambda x: print(f"Left trigger: {x:.2f}"),
      "right_trigger": lambda x: print(f"Right trigger: {x:.2f}"),
      "left_bumper": lambda x: print(f"Left bumper {"pressed" if x == 0 else "released"}"),
      "right_bumper": lambda x: print(f"Right bumper {"pressed" if x == 0 else "released"}"),
      "back": lambda x: print(f"Back {"pressed" if x == 0 else "released"}"),
      "start": lambda x: print(f"Start {"pressed" if x == 0 else "released"}"),
      "left_stick": lambda axis, value: print(f"Left stick [{"y" if axis else "x"}]: {value:.2f}"),
      "right_stick": lambda axis, value: print(f"Right stick [{"y" if axis else "x"}]: {value:.2f}"),
      "left_stick_button": lambda x: print(f"Left stick button {"pressed" if x == 0 else "released"}"),
      "right_stick_button": lambda x: print(f"Right stick button {"pressed" if x == 0 else "released"}"),
      "hat": lambda x: print(f"Hat: {x}")
    })



if __name__ == "__main__":
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
      


