## **Lognotify** — module for colorful logging

### **Supported features**
#### **Predefined log levels:**
- **info** or **note** — informational messages
- **warning** — warnings
- **error** — errors
- **debug** — debugging messages
- **critical** — critical errors
- **custom** — custom log level

#### **Formatting options:**
- **Text and level (label) colors:**
    - `black, red, green, yellow, blue, magenta, cyan, white`
    - Additional: `light-*`, `dim-*` (e.g., `light-red`, `dim-blue`)
- **Background colors:**
    - Same as text colors
- **Text case options:**
    - `upper` — ALL UPPERCASE
    - `lower` — all lowercase
    - `capitalize` — First letter uppercase
    - `title` — Each Word Capitalized
- **Works on Windows and Linux**

### **Usage examples**
```python
from lognotify import info, note, warning, error, debug, critical, custom

print(info(text="System is running"))
print(note(text="System is running"))
print(warning(text="Potential issues ahead"))
print(error(text="An error occurred!"))
print(debug(text="Debugging info"))
print(critical(text="Critical failure!"))
print(custom(text="Custom log message", log_level="ALERT", text_color="magenta", letter_color="red", text_back="black", letter_back="white", text_case="title", letter_case="upper")
```

### **Install**

##### With PyPi
```python
pip install lognotify
```

##### With Source
```bash
git clone https://github.com/411Gamer/lognotify.git
cd lognotify
python3 setup.py install
```

