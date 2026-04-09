import math
import sys
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QSizePolicy, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt


# ====================================
#   GLOBAL FLAGS
# ====================================
last_was_equals = False          # Remembers if last pressed button was "=" so new numbers overwrite previous results
is_sci_on = False                # Tracks whether scientific mode is ON or OFF
rad_deg_mode = False             # Tracks Radian/Degree toggle state (False = DEG, True = RAD)


# ====================================
#   APP + WINDOW SETUP
# ====================================
app = QApplication(sys.argv)                         # Initializes PySide6 application (required for all Qt apps)
window = QWidget()                                   # Creates main calculator window
window.setWindowTitle("YeroCalc(2.0)")               # Sets title bar text
window.setStyleSheet("background-color: #1C1C1C;")   # Gives window a dark background aesthetic


# ====================================
#   SWITCH FUNCTION (SCI MODE)
# ====================================
def toggle_switch():                                        # Handles switching between normal & scientific mode
    global is_sci_on                                        # Allows modification of global sci mode variable
    is_sci_on = not is_sci_on                               # Toggles True/False for ON/OFF

    anim = QPropertyAnimation(switchButton, b"styleSheet")  # Animation object for smooth color transitions
    anim.setDuration(250)                                   # Duration = 0.25 seconds

    if is_sci_on:                                           # When turning ON scientific mode
        switchButton.setText("ON")                          # Updates switch text
        sci_container.show()                                # Displays scientific button grid
        rad_label.show()                                    # Shows the Degrees/Radians label
        angleSwitch.show()                                  # Shows the DEG/RAD switch
        window.layout().activate()                          # Reactivates layout (ensures Qt recalculates positions)
        window.adjustSize()                                 # Adjusts window to fit new visible widgets
        switchButton.setStyleSheet("""                      
            background-color: #C83F49;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 15px;
        """)
    else:                                                   # When turning OFF scientific mode
        switchButton.setText("OFF")                         # Updates label to OFF
        sci_container.setVisible(False)                     # Hides scientific buttons
        rad_label.hide()                                    # Hides Degrees/Radians label
        angleSwitch.hide()                                  # Hides DEG/RAD switch
        window.layout().activate()                          # Refreshes layout again
        window.adjustSize()                                 # Re-sizes window down
        switchButton.setStyleSheet("""                     
            background-color: gray;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 15px;
        """)
    switchButton._anim = anim                               # Keeps animation reference alive (prevents garbage collection)


# ====================================
#   SWITCH FUNCTION (RAD N DEG)
# ====================================
def toggle_angle_mode():                                                  # Toggles between Degrees and Radians
    global rad_deg_mode                                                   # Modify global mode variable
    rad_deg_mode = not rad_deg_mode                                       # Switch True/False for mode change
               
    anim = QPropertyAnimation(switchButton, b"styleSheet")                # Prepares dummy animation (keeps smooth transition idea)
    anim.setDuration(250)                                                 # Duration 250ms
               
    if rad_deg_mode:                                                      # If toggled to RAD
        angleSwitch.setText("RAD")                                        # Updates button text to RAD
        angleSwitch.setStyleSheet("""                                     
            background-color: #C83F49;               
            color: white;               
            border: none;               
            border-radius: 12px;               
            font-size: 15px;               
        """)               
    else:                                                                 # If toggled back to DEG
        angleSwitch.setText("DEG")                                        # Updates text
        angleSwitch.setStyleSheet("""                                     
            background-color: gray;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 15px;
        """)


# ====================================
#   CUSTOM BUTTON CLASS (BOUNCY)
# ====================================
class BouncyButton(QPushButton):                                  # Extends QPushButton with custom animation behavior
    def mousePressEvent(self, event):                             # Triggered whenever button is pressed
        super().mousePressEvent(event)                            # Keeps QPushButton default press behavior
        self.animate_bounce()                                     # Adds bounce animation afterward
    
    def animate_bounce(self):                                     # Defines bounce animation
        anim = QPropertyAnimation(self, b"geometry")              # Animation acts on button geometry (size/position)
        anim.setDuration(120)                                     # Quick 0.12s animation
        anim.setEasingCurve(QEasingCurve.OutBounce)               # Gives elastic effect
        rect = self.geometry()                                    # Stores current button rectangle
        anim.setStartValue(rect)                                  # Start position same as current
        anim.setKeyValueAt(0.5, rect.adjusted(10, 10, -10, -10))  # Shrinks slightly at midpoint
        anim.setEndValue(rect)                                    # Returns to normal size
        anim.start()                                              # Starts animation
        self._anim = anim                                         # Keeps reference alive to prevent premature stop


# ====================================
#   ENTRY FIELD
# ====================================
entry = QLineEdit()                               # Creates main display for calculator and background color
entry.setStyleSheet("""                           
    background-color: #1C1C1C;
    border: none;
    color: white;
    font-size: 36px;
    padding: 10px;
""") 
                        
                        
# ====================================
#   BUTTON STYLING FUNCTIONS
# ==================================== 
def number_button(btn):                          # Style for number buttons 0–9
    btn.setStyleSheet("""
        background-color: #333333;
        color: white;
        border: none;
        font-size: 24px;
        border-radius: 20px;
        padding: 15px;
    """)

def symbol_button(btn):                         # Style for operator buttons (+, -, ×, ÷, =)
    btn.setStyleSheet("""
        background-color: #C83F49;
        color: white;
        border: none;
        font-size: 24px;
        border-radius: 20px;
        padding: 15px;
    """)

def other_button(btn):                          # Style for misc buttons (AC, %, ⌫)
    btn.setStyleSheet("""
        background-color: #838996;
        color: white;
        border: none;
        font-size: 24px;
        border-radius: 20px;
        padding: 15px;
    """)


# ====================================
#   CORE BUTTON LOGIC
# ====================================
def button_clicked(value):                                                # Handles every button click event
    global last_was_equals              
    current = entry.text()                                                # Retrieves current entry text
              
    if last_was_equals:                                                   # If last button was "="
        if value.isdigit() or value == ".":                               # Start fresh if entering number or decimal
            current = ""              
        last_was_equals = False                                           # Reset equals flag

    if current != "" and current[-1] in "+-×÷" and value in "+-×÷":       # Prevents entering two operators consecutively
        current = current[:-1] + value              
    elif current == "" and value in "+×÷":                                # Prevents leading operator
        return              
    elif current == "Error":                                              # Clears "Error" before new input
        current = value              
    elif value == "." and "." in current.split("+-×÷")[-1]:               # Prevents multiple decimals in a segment
        return              
    else:              
        current = current + value                                         # Appends the new character
              
    entry.setText(current)                                                # Updates display with new value
              
              
def clear_entry():                                                        # Clears entire entry field
    global last_was_equals              
    entry.clear()              
    last_was_equals = False              
              
              
def backspace():                                                          # Removes the last character
    current = entry.text()              
    entry.setText(current[:-1])              
              
              
def SignChange():                                                         # Toggles positive/negative sign
    current = entry.text()              
    if current.startswith("-"):              
        entry.setText(current[1:])              
    elif current != "":              
        entry.setText("-" + current)              
              
              
def normalizeExpressions(text):                                           # Converts display text into valid Python math syntax
    expr = text
    expr = expr.replace("×", "*")                                         # Replace × with *
    expr = expr.replace("÷", "/")                                         # Replace ÷ with /
    expr = expr.replace("%", "/100")                                      # Converts percent into division
    expr = expr.replace("√", "math.sqrt")                                 # Square root → math.sqrt
    expr = expr.replace("π", "math.pi")                                   # Pi constant
    expr = expr.replace("xʸ", "**")                                       # Exponentiation
    
    # --- SCIENTIFIC REPLACEMENTS ---
    if not rad_deg_mode:  # DEG mode
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        expr = expr.replace("log(", "math.log10(")
        expr = expr.replace("sin⁻¹(", "math.degrees(math.asin(")
        expr = expr.replace("cos⁻¹(", "math.degrees(math.acos(")
        expr = expr.replace("tan⁻¹(", "math.degrees(math.atan(")
    else:  # RAD mode
        expr = expr.replace("sin(", "math.sin(")
        expr = expr.replace("cos(", "math.cos(")
        expr = expr.replace("tan(", "math.tan(")
        expr = expr.replace("log(", "math.log10(")
        expr = expr.replace("sin⁻¹(", "math.asin(")
        expr = expr.replace("cos⁻¹(", "math.acos(")
        expr = expr.replace("tan⁻¹(", "math.atan(")
    return expr


def Equals():                                                             # Runs when "=" is pressed
    global last_was_equals              
    current = entry.text().strip()                                        # Clean text
    if current == "":                                                     # Ignore empty input
        return              
     
    entry.clear()                                                         # Clear before showing result
    try:              
        expression = normalizeExpressions(current)                        # Convert visible expression to Python syntax
              
        open_paren = expression.count("(")                                # Count opening parentheses
        close_paren = expression.count(")")                               # Count closing parentheses
        if open_paren > close_paren:                                      # Fix unbalanced parentheses
            expression += ")" * (open_paren - close_paren)                

        result = eval(expression, {"__builtins__": {}}, {"math": math})   # Evaluate safely using math namespace only

        # --- ROUNDING LOGIC --- #
        if isinstance(result, float):
            if result.is_integer():                                       # If float is effectively an int
                result = int(result)
                entry.setText(str(result)) 
            else:
                result = round(result, 10)                                # Round floats to 10 decimal places
                entry.setText(str(result)) 
        else:
            entry.setText(str(result))                                         
    except:              
        entry.setText("Error")                                            # Displays Error message if something fails
    last_was_equals = True                                                # Mark last key as equals pressed


# ====================================
#   BUTTON CREATION (NORMAL CALC)
# ====================================
button1 = BouncyButton("1")
button2 = BouncyButton("2")
button3 = BouncyButton("3")
button4 = BouncyButton("4")
button5 = BouncyButton("5")
button6 = BouncyButton("6")
button7 = BouncyButton("7")
button8 = BouncyButton("8")
button9 = BouncyButton("9")
button0 = BouncyButton("0")

buttonAdd = BouncyButton("+")
buttonSub = BouncyButton("-")
buttonMult = BouncyButton("×")
buttonDiv = BouncyButton("÷")
buttonEquals = BouncyButton("=")

buttonBS = BouncyButton("⌫")
buttonClear = BouncyButton("AC")
buttonDot = BouncyButton(".")
buttonPercent = BouncyButton("%")
buttonSign = BouncyButton("±")

switchButton = QPushButton("OFF")                                        # Main Scientific Mode switch
switchButton.setFixedSize(50, 25)                                        # Small pill shape size
switchButton.setStyleSheet("""                                           
    background-color: gray;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 15px;
""")


# ====================================
#   BUTTON CREATION (SCI CALC)
# ====================================
buttonSin = BouncyButton("sin")
buttonCos = BouncyButton("cos")
buttonTan = BouncyButton("tan")
buttonSinInv = BouncyButton("sin⁻¹")
buttonCosInv = BouncyButton("cos⁻¹")
buttonTanInv = BouncyButton("tan⁻¹")
buttonPara1 = BouncyButton("(")
buttonPara2 = BouncyButton(")")
buttonLog = BouncyButton("log")
buttonSqrtRoot = BouncyButton("√")
buttonXSqrt = BouncyButton("xʸ")
buttonPi = BouncyButton("π")
buttonTitle = BouncyButton("YeroCalc")

angleSwitch = QPushButton("DEG")                                       # Creates switch mode
angleSwitch.setFixedSize(50, 25)                                       # Sets size of switch and defaults OFF appearance 
angleSwitch.setStyleSheet("""
    background-color: gray;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 15px;
""")
angleSwitch.hide()                                                     # Hides switch by defualt


# ====================================
#   APPLY STYLES
# ====================================
numbers = [
    button0, button1, button2, button3, button4,
    button5, button6, button7, button8, button9,
    buttonDot, buttonSign
]

symbols = [buttonAdd, buttonSub, buttonMult, buttonDiv, buttonEquals, buttonSin, buttonCos, buttonTan, buttonSinInv, buttonCosInv, buttonTanInv, buttonPara1, buttonPara2, buttonLog, buttonSqrtRoot, buttonXSqrt, buttonPi]
others = [buttonBS, buttonClear, buttonPercent]
title = [buttonTitle]


for btn in numbers:
    number_button(btn)
for btn in symbols:
    symbol_button(btn)
for btn in others:
    other_button(btn)
for btn in title:
    other_button(btn)
                   
all_buttons = numbers + symbols + others                              # Makes 1 size for all buttons
                   
for btn in all_buttons:                     
    btn.setFixedSize(80, 65)                                          # width, height
                   

# ====================================
#   BUTTON CONNECTIONS (NORMAL CALC)
# ====================================
button1.clicked.connect(lambda: button_clicked("1"))
button2.clicked.connect(lambda: button_clicked("2"))
button3.clicked.connect(lambda: button_clicked("3"))
button4.clicked.connect(lambda: button_clicked("4"))
button5.clicked.connect(lambda: button_clicked("5"))
button6.clicked.connect(lambda: button_clicked("6"))
button7.clicked.connect(lambda: button_clicked("7"))
button8.clicked.connect(lambda: button_clicked("8"))
button9.clicked.connect(lambda: button_clicked("9"))
button0.clicked.connect(lambda: button_clicked("0"))

buttonAdd.clicked.connect(lambda: button_clicked("+"))
buttonSub.clicked.connect(lambda: button_clicked("-"))
buttonDiv.clicked.connect(lambda: button_clicked("÷"))
buttonMult.clicked.connect(lambda: button_clicked("×"))
buttonPercent.clicked.connect(lambda: button_clicked("%"))
buttonDot.clicked.connect(lambda: button_clicked("."))

buttonClear.clicked.connect(clear_entry)
buttonBS.clicked.connect(backspace)
buttonSign.clicked.connect(SignChange)
buttonEquals.clicked.connect(Equals)
entry.returnPressed.connect(Equals)                                     # Pressing Enter = same as clicking "="


# ====================================
#   BUTTON CONNECTIONS (SCI CALC)
# ====================================
buttonSin.clicked.connect(lambda: button_clicked("sin("))
buttonCos.clicked.connect(lambda: button_clicked("cos("))
buttonTan.clicked.connect(lambda: button_clicked("tan("))
buttonLog.clicked.connect(lambda: button_clicked("log("))
buttonSinInv.clicked.connect(lambda: button_clicked("sin⁻¹("))
buttonCosInv.clicked.connect(lambda: button_clicked("cos⁻¹("))
buttonTanInv.clicked.connect(lambda: button_clicked("tan⁻¹("))
buttonSqrtRoot.clicked.connect(lambda: button_clicked("√"))
buttonPi.clicked.connect(lambda: button_clicked("π"))
buttonXSqrt.clicked.connect(lambda: button_clicked("xʸ"))
buttonPara1.clicked.connect(lambda: button_clicked("("))
buttonPara2.clicked.connect(lambda: button_clicked(")"))


# ====================================
#   LAYOUT SETUP (ENTRY + SWITCHES)
# ====================================
entry_part = QVBoxLayout()
entry_part.addWidget(entry)

switch_row = QHBoxLayout()                                              # Horizontal container for both switches
switch_row.setContentsMargins(0, 0, 0, 0)
switch_row.setSpacing(20)
switch_row.setAlignment(Qt.AlignLeft)

sci_label = QLabel("Sci Mode")                                          # Left label for scientific mode
sci_label.setStyleSheet("""
    color: white;
    font-size: 12px;
    padding-right: 8px;
""")

sci_switch_layout = QHBoxLayout()                                       # Small sublayout (label + switch)
sci_switch_layout.setContentsMargins(0, 0, 0, 0)
sci_switch_layout.setSpacing(5)
sci_switch_layout.addWidget(sci_label)
sci_switch_layout.addWidget(switchButton)

rad_label = QLabel("Degrees / Radians")                                 # Right label for DEG/RAD
rad_label.setStyleSheet("""
    color: white;
    font-size: 12px;
    padding-right: 8px;
""")
rad_label.hide()

rad_switch_layout = QHBoxLayout()
rad_switch_layout.setContentsMargins(0, 0, 0, 0)
rad_switch_layout.setSpacing(5)
rad_switch_layout.addWidget(rad_label)
rad_switch_layout.addWidget(angleSwitch)

switch_row.addLayout(sci_switch_layout)                                 # Adds sci mode switch (left)
switch_row.addStretch()                                                 # Adds flexible gap between
switch_row.addLayout(rad_switch_layout)                                 # Adds DEG/RAD switch (right)
entry_part.addLayout(switch_row)                                        # Adds both under entry field


# ====================================
#   LAYOUT SETUP (NORMAL CALC)
# ====================================
row1 = QHBoxLayout()
row1.addWidget(buttonBS)
row1.addWidget(buttonClear)
row1.addWidget(buttonPercent)
row1.addWidget(buttonDiv)

row2 = QHBoxLayout()
row2.addWidget(button7)
row2.addWidget(button8)
row2.addWidget(button9)
row2.addWidget(buttonMult)

row3 = QHBoxLayout()
row3.addWidget(button4)
row3.addWidget(button5)
row3.addWidget(button6)
row3.addWidget(buttonAdd)

row4 = QHBoxLayout()
row4.addWidget(button1)
row4.addWidget(button2)
row4.addWidget(button3)
row4.addWidget(buttonSub)

row5 = QHBoxLayout()
row5.addWidget(buttonSign)
row5.addWidget(button0)
row5.addWidget(buttonDot)
row5.addWidget(buttonEquals)

normal_calc = QVBoxLayout()
normal_calc.addLayout(row1)
normal_calc.addLayout(row2)
normal_calc.addLayout(row3)
normal_calc.addLayout(row4)
normal_calc.addLayout(row5)
normal_calc.setSpacing(8)
normal_calc.setContentsMargins(8, 8, 8, 8)

normal_container = QWidget()
normal_container.setLayout(normal_calc)
normal_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)


# ====================================
#   LAYOUT SETUP (SCI CALC)
# ====================================
sci_row1 = QHBoxLayout()
sci_row1.addWidget(buttonSin)
sci_row1.addWidget(buttonCos)
sci_row1.addWidget(buttonTan)

sci_row2 = QHBoxLayout()
sci_row2.addWidget(buttonSinInv)
sci_row2.addWidget(buttonCosInv)
sci_row2.addWidget(buttonTanInv)

sci_row3 = QHBoxLayout()
sci_row3.addWidget(buttonPara1)
sci_row3.addWidget(buttonLog)
sci_row3.addWidget(buttonPara2)

sci_row4 = QHBoxLayout()
sci_row4.addWidget(buttonSqrtRoot)
sci_row4.addWidget(buttonXSqrt)
sci_row4.addWidget(buttonPi)

sci_row5 = QHBoxLayout()
sci_row5.addWidget(buttonTitle)

sci_calc = QVBoxLayout()
sci_calc.addLayout(sci_row1)
sci_calc.addLayout(sci_row2)
sci_calc.addLayout(sci_row3)
sci_calc.addLayout(sci_row4)
sci_calc.addLayout(sci_row5)
sci_calc.setSpacing(8)
sci_calc.setContentsMargins(6, 8, 6, 8)


# ====================================
#   FINAL LAYOUT (MAIN)
# ====================================
sci_container = QWidget()
sci_container.setLayout(sci_calc)
sci_container.hide()                                                    # Hidden until scientific mode activated

grids = QHBoxLayout()
grids.addWidget(normal_container)
grids.addWidget(sci_container)
grids.setSpacing(5)
grids.setContentsMargins(10, 10, 10, 10)

main_window = QVBoxLayout()
main_window.addLayout(entry_part)                                       # Entry + switches
main_window.addLayout(grids)                                            # Grids below

window.setLayout(main_window)


# ====================================
#   CONNECT SWITCHES TO FUNCTIONS
# ====================================
switchButton.clicked.connect(toggle_switch)
angleSwitch.clicked.connect(toggle_angle_mode)


# ====================================
#   RUN APP
# ====================================
window.show()
sys.exit(app.exec())                                                    # Launches the Qt event loop and runs app