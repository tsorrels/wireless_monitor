# IP_monitor

This project is a simple terminal IP traffic monitoring tool with simple a user interface and extensibility. No external dependencies.

To run in Linux (must be root):

```bash
$ sudo ./ip_monitor -i interface [-p] [Extention, ...]

```
The user must provide an interface (i.e. 'eth0'), can optionally provide the -p switch to run in permiscuous mode, and can concatenate any number of properly written extention modules that the tool will load prior to running.

A execution example would be:
```bash
$ sudo ./ip_monitor -i eth0 -p ip_whois ip_time
```


Strike 'arrow-up' and 'arrow-down' to scroll through connections. Strike 'r' to remove a connection from the state.  Stirke 'q' to quit.


## Extentions
### Model

Extending the tool is easy.  Write a module that that globally defines an Extension object named 'extension', defined in ip_extension.py. Load the modules by concatenating them only the executing command.

```python
class Extension(object):
    # must explicitly set all components; any can be an empty list
    def __init__(self, threads, hdr_extensions, data_extensions, cmd_extensions):
        self.threads = threads				# must be list
        self.header_extensions = hdr_extensions		# must be list
        self.data_extensions = data_extensions		# must be list
        self.cmd_extensions = cmd_extensions		# must be list
```


The model is a collection of 'connection' objects, defined in ip_connection.py. You can extend the model be defining a list of strings that the engine will add to the ip_connection objects as fields and make accessable.

```python
data_extensions = [ 'average_bps', ]

```

### View

The view is a series of columns with a defined string header and a matching field in the connection objects that the view will access when writing the display.

```python

class HeaderItem(object):
    def __init__(self, text, length, offset = None):
        self.text = text	# must be string
        self.length = length	# integer representing max character output for item
        self.offset = offset	# not used

```

![UI View](/doc/terminal_view.jpeg)

The UI identifies the 'current' connection with underline. Strike the up or down key to scroll and select a differrent connection. Commands executed will operate on the current connection. 

Connections that have not experienced data transfer in the last 10 seconds are displayed in grey text. 

Ensure the terminal window is sufficiently wide to display all appended header displays.
TODO: handle dynamic terminal resizing

### Controller

The control can be extended by adding CmdExtension objects, defined in cmd_extension.py. The CmdExtension object simply defines an input key and a function to execute when pressed.  The programmer must take care to not allow a collision between input keys; each key may be mapped only once throughout the entire program.


```python
class CmdExtension(object):
    def __init__(self, key, function):
        self.key = key			# must be character
        self.function = function	# must be function definition

```

The function to execute in a command extension must have the following prototype:
```python
function_def(data, state)
```
where 'data' is a string of characters from the row in the view representing the 'current connection.'  You can pass the data string to the 'find_connection' method in the state object to retreive a reference to the connection identified in the view.

```python
execute_command(data, state):
    connection = state.find_connection(data)
    with state.all_lock:
        # operate on connection
```

### Threads

Each extension also includes a member 'threads' which is a list of function definitions with the signature 
```python
function_def(state)
```
The function will likely include an infinite loop so as to continue doing work on the state (like throttling all new in-bound connections). The tool will create a new thread that calls this function and passes in the global state object.  **Locking - ** It is important to ensure your thread(s) acquire the state.all_lock lock before writing to the state or doing a time sensitive read. A simply example from the ip_time extension module follows:

```python    
def Run(state):
    while True:
        run_time(state)
        time.sleep(1)


def run_time(state):
    connections = state.all_connections
    lock = state.all_lock
    
    now = time.time()
    with lock:
        for connection in connections:
            connection.time_elapsed = format_time(now - connection.time_last)
```


### Cleanup on exit

In additional to defening a globally scoped Extension object named 'extension', modules may optionally define a globally scoped function named 'exit'.  The function signature must accept one parameter, the global state.  Upon loading the module, tool will register this cleanup function and call it prior to exiting.


### Current extensions
**ip_time** - very module that extends the model by adding the 'time_elapsed' attribute to connection objects, extends the view by adding the Time column to the UI showing the time elapsed since the last data transfer for a connection, and the controller by adding funcionality mapped to the 'R' key that 'resets' the time elapsed data for a connection to 0.  

**ip_whois** - extension that runs a whois client to resolve source IPs for all new inbound connections.

**ip_throttle** - extension that uses the Linux tc utility to throttle down all incoming traffic from new connections.  Extends the controller with the 't' key to toggle throttling a connection (Linux only).

### Extension Example Definition

A very simple example of an extension follows.  Notice the final line which defines the global variable 'extension'.

```python
import time
from ip_monitor.cmd_extension import CmdExtension
from ip_monitor.display_headers import HeaderItem
from ip_monitor.ip_extension import Extension

def format_time(time):
    returnString = ''
    if time < 60:
        returnString = str(int(time)) + 's'

    elif time < 60 * 60:
        returnString = str(int(time) / 60) + 'm'

    else:
        returnString = str(max(99, int(time) / 60 / 60)) + 'h'
            
    return returnString


def refresh_time(data, state):
    connection = state.find_connection(data)
    now = time.time() - 1
    with state.all_lock:
        connection.time_last = now


def run_time(state):
    connections = state.all_connections
    lock = state.all_lock
    now = time.time()
    with lock:
        for connection in connections:
            connection.time_elapsed = format_time(now - connection.time_last)
    
def exit(state):
    pass
    
def Run(state):
    while True:
        run_time(state)
        time.sleep(1)
    

Threads = [Run,]
Header_Extensions = [ HeaderItem('Time', 4), ]
Data_Extensions = [ 'time_elapsed', ]
Cmd_Extensions = [ CmdExtension('R', refresh_time),]

extension = Extension(Threads, Header_Extensions, Data_Extensions, Cmd_Extensions)```
```

### Logging mechanism
Debugging multithreaded applications that use the curses library is difficult.  The global state includes a member named 'logwriter' which any module can use to write any log the programmer wishes.  A module may optionally register a new log with the logwriter prior to using the logwriter.write(log_handle, text) function.  An example from ip_whois follows:
TODO: paste example


### Future ideas for extensions
Man in the Middle Module
Counter traffic module
Module to send SIGKILL to processes from this tool
Whitelist module, where only filtered traffic



#### TODO
- refactor file structure
- gracefully exit if not root
- add details view
- build module validator
