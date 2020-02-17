def csum(command):  
    checksum = 0
    for i in range(25):     
        checksum = checksum + command[i]                    
    return (0xFF & checksum)                    
    
def command(command, serial):                          
    command[0] = 0xAA
    command[25] = csum(command)
    serial.write(command)                        
    resp = serial.read(26)
    if resp[2] == 0x12:
        if resp[3] == 0x80:
            """Success"""
            return
        elif resp[3] == 0x90:
            raise Exception('Checksum Error')
        elif resp[3] == 0xA0:
            raise Exception('Parameter Incorrect')
        elif resp[3] == 0xB0:
            raise Exception('Unrecognized Command')
        elif resp[3] == 0xC0:
            raise Exception('Invalid Command')
            
        print("Command Sent:\t\t",end=' ')
        printCmd(command)
            
        print("Reponse Received:\t",end=' ')    
        printCmd(resp)
    else:
        return resp
    
def printCmd(buff):
    x = " "        
    for y in range(len(buff)):
        x+=" "
        x+=hex(buff[y]).replace('0x','')   
    print(x)
    
def remoteMode(state, serial):
    """Remote Mode"""
    cmd = [0] * 26
    cmd[2] = 0x20
    if bool(state):
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)
    
def inputOn(state, serial):
    """Input On. state = True or False"""
    cmd = [0] * 26
    cmd[2] = 0x21
    if bool(state):
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)
    
def setMaxVoltage(voltage, serial):
    value = int(voltage * 1000)
    """Set Max Voltage"""
    cmd = [0] * 26
    cmd[2] = 0x22
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)
    
def readMaxVoltage(serial):
    """Read Max Voltage"""
    cmd = [0] * 26
    cmd[2] = 0x23
    resp = command(cmd, serial)
    voltage = resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24)
    return voltage/1000.00
    

def setMaxCurrent(current, serial):
    value = int(current * 10000)
    """Set max input current: %f & current"""
    cmd = [0] * 26
    cmd[2] = 0x24
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)

def readMaxCurrent(serial):
    """Read the max setup input current."""
    cmd = [0] * 26
    cmd[2] = 0x25
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/10000.00
    
def setMaxPower(power, serial):
    """Set max input power. Unit = W, Resolution 1mW"""
    value = int(power*1000)
    cmd = [0] * 26
    cmd[2] = 0x26
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)
 

def readMaxPower(serial):
    """Read the max setup input power."""
    cmd = [0] * 26
    cmd[2] = 0x27
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00

def setMode(mode, serial):
    """Set operation mode. CC(0)/CV(1)/CW(2)/CR(3)"""
    if mode not in range(0,3):
        raise Exception(("setMode mode=%d: Operation mode not in range 0-3 (cc=0, cv=1, cp=2, cr=3)" % mode).format())
    cmd = [0] * 26
    cmd[2] = 0x28
    cmd[3] = mode
    command(cmd, serial)

def readMode(serial):
    """Read the operation mode."""
    cmd = [0] * 26
    cmd[2] = 0x29
    resp = command(cmd, serial)
    return resp[3]

def setCCCurrent(current, serial):
    """Set CC mode current value"""
    value = int(current*10000)
    cmd = [0] * 26
    cmd[2] = 0x2A
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    resp = command(cmd, serial)
    

def readCCCurrent(serial):
    """Read CC mode current value"""
    cmd = [0] * 26
    cmd[2] = 0x2B
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/10000.00

def setCVVoltage(voltage, serial):
    """Set CV mode voltage value"""
    value = int(voltage * 1000)
    cmd = [0] * 26
    cmd[2] = 0x2C
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)
    
def readCVVoltage(serial):
    """Read CV mode voltage value"""
    cmd = [0] * 26
    cmd[2] = 0x2D
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00

def setCWPower(power, serial):
    """Set CW mode watt value"""
    value = int(power * 1000)
    cmd = [0] * 26
    cmd[2] = 0x2E
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)
    
def readCWPower(serial):
    """Read CW mode watt value"""
    cmd = [0] * 26
    cmd[2] = 0x2F
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00

def setCRResistance(resistance, serial):
    """Set CR mode resistance value"""
    value = int(resistance * 1000)
    cmd = [0] * 26
    cmd[2] = 0x30
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)
    
def readCRResistance(serial):
    """Read CR mode resistance value"""
    cmd = [0] * 26
    cmd[2] = 0x31
    resp = command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00
    
def setCCTransient(aCurrent, bCurrent, aTime, bTime, mode, serial):
    """Set CC mode transient current and timer parameter.
    aCurrent - current in Amps
    bCurrent - current in Amps
    aTime - A level time in milliseconds
    bTime - B level time in milliseconds
    mode - 1 = Continuous, 2 = Pulse, 3 = Toggled """
    aCurr = int(aCurrent*10000)
    aT = int(aTime*10)
    bCurr = int(bCurrent*10000)
    bT = int(bTime*10)
    print(aCurr)
    cmd = [0] * 26
    cmd[2] = 0x32
    cmd[3] = aCurr & 0xFF
    cmd[4] = (aCurr >> 8) & 0xFF
    cmd[5] = (aCurr >> 16) & 0xFF
    cmd[6] = (aCurr >> 24) & 0xFF
    cmd[7] = aT & 0xFF
    cmd[8] = (aT >> 8) & 0xFF
    cmd[9] = bCurr & 0xFF
    cmd[10] = (bCurr >> 8) & 0xFF
    cmd[11] = (bCurr >> 16) & 0xFF
    cmd[12] = (bCurr >> 24) & 0xFF
    cmd[13] = bT & 0xFF
    cmd[14] = (bT >> 8) & 0xFF
    cmd[15] = mode
    command(cmd, serial)
    

def readCCTransient(serial):
    """Read CC mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x33
    resp = command(cmd, serial)
    return resp
    
def setCV(aVoltage, bVoltage, aTime, bTime, mode, serial):
    """Set CV mode transient current and timer parameter.
    aVoltage - Voltage in Volts
    bVoltage - Voltage in Volts
    aTime - A level time in milliseconds
    bTime - B level time in milliseconds
    mode - 1 = Continuous, 2 = Pulse, 3 = Toggled """
    aVolt = int(aVoltage*10000)
    aT = int(aTime*10)
    bVolt = int(aVoltage*10000)
    bT = int(bTime*10)
    cmd = [0] * 26
    cmd[2] = 0x34
    cmd[3] = aVolt & 0xFF
    cmd[4] = (aVolt >> 8) & 0xFF
    cmd[5] = (aVolt >> 16) & 0xFF
    cmd[6] = (aVolt >> 24) & 0xFF
    cmd[7] = aT & 0xFF
    cmd[8] = (aT >> 8) & 0xFF
    cmd[9] = bVolt & 0xFF
    cmd[10] = (bVolt >> 8) & 0xFF
    cmd[11] = (bVolt >> 16) & 0xFF
    cmd[12] = (bVolt >> 24) & 0xFF
    cmd[13] = bT & 0xFF
    cmd[14] = (bT >> 8) & 0xFF
    cmd[15] = mode
    command(cmd, serial)

def readCVTransient(serial):
    """Read CV mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x35
    resp = command(cmd, serial)
    return resp

def setCWTransient(aPower, bPower, aTime, bTime, mode, serial):
    """Set CW mode transient current and timer parameter.
    aPower - Power in Watts
    bPower - Power in Watts
    aTime - A level time in milliseconds
    bTime - B level time in milliseconds
    mode - 1 = Continuous, 2 = Pulse, 3 = Toggled """
    aPow = int(aPower*100)
    aT = int(aTime*10)
    bPow = int(bPower*100)
    bT = int(bTime*10)
    cmd = [0] * 26
    cmd[2] = 0x36
    cmd[3] = aPow & 0xFF
    cmd[4] = (aPow >> 8) & 0xFF
    cmd[5] = (aPow >> 16) & 0xFF
    cmd[6] = (aPow >> 24) & 0xFF
    cmd[7] = aT & 0xFF
    cmd[8] = (aT >> 8) & 0xFF
    cmd[9] = bPow & 0xFF
    cmd[10] = (bPow >> 8) & 0xFF
    cmd[11] = (bPow >> 16) & 0xFF
    cmd[12] = (bPow >> 24) & 0xFF
    cmd[13] = bT & 0xFF
    cmd[14] = (bT >> 8) & 0xFF
    cmd[15] = mode
    command(cmd, serial)

def readCWTransient(serial):
    """Read CW mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x37
    resp = command(cmd, serial)
    return resp

def setCRTransient(aResistance, bResistance, aTime, bTime, mode, serial):
    """Set CW mode transient current and timer parameter.
    aPower - Resistance in Ohms
    bPower - Resistance in Ohms
    aTime - A level time in milliseconds
    bTime - B level time in milliseconds
    mode - 1 = Continuous, 2 = Pulse, 3 = Toggled """
    aRes = int(aResistance*1)
    aT = int(aTime*10)
    bRes = int(bResistance*1)
    bT = int(bTime*10)
    cmd = [0] * 26
    cmd[2] = 0x38
    cmd[3] = aRes & 0xFF
    cmd[4] = (aRes >> 8) & 0xFF
    cmd[5] = (aRes >> 16) & 0xFF
    cmd[6] = (aRes >> 24) & 0xFF
    cmd[7] = aT & 0xFF
    cmd[8] = (aT >> 8) & 0xFF
    cmd[9] = bRes & 0xFF
    cmd[10] = (bRes >> 8) & 0xFF
    cmd[11] = (bRes >> 16) & 0xFF
    cmd[12] = (bRes >> 24) & 0xFF
    cmd[13] = bT & 0xFF
    cmd[14] = (bT >> 8) & 0xFF
    cmd[15] = mode
    command(cmd, serial)

def readCRTransient(serial):
    """Read CR mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x39
    resp = command(cmd, serial)
    return resp

def setCCList(serial):
    """Set the list operation mode (CC)"""
    cmd = [0] * 26
    cmd[2] = 0x3A
    cmd[3] = 0
    command(cmd, serial)

def readCCList(serial):
    """Read the list operation mode."""
    cmd = [0] * 26
    cmd[2] = 0x3B
    resp = command(cmd, serial)
    return resp

def setListRepeat(repeat, serial):
    """Set the list repeat mode (ONCE/REPEAT)
    (repeat) - 0=Once, 1-65534 or 65535 = forever"""
    cmd = [0] * 26
    cmd[2] = 0x3C
    cmd[3] = repeat #this should be 2 bytes... I think (Ryan)
    command(cmd, serial)

def readListRepeat(serial):
    """Read the list repeat mode."""
    cmd = [0] * 26
    cmd[2] = 0x3D
    resp = command(cmd, serial)
    return resp

def setListStepCount(stepCount, serial):
    """Set list steps counts.
    (stepCount) = number of steps"""
    cmd = [0] * 26
    cmd[2] = 0x3E
    cmd[3] = stepCount & 0xFF
    cmd[4] = (stepCount >> 8) & 0xFF
    command(cmd, serial)

def readListStepCount(serial):
    """Read list steps counts"""
    cmd = [0] * 26
    cmd[2] = 0x3F
    resp = command(cmd, serial)
    return resp

def setStepTime(stepNumber, current, time, serial):
    """Set one of the step's current and time values.
    stepNumer - (1-84)
    current - in Amps
    time - in milliseconds
    """
    curr = int(current*10000)
    cmd = [0] * 26
    cmd[2] = 0x40
    cmd[3] = stepNumber & 0xFF
    cmd[4] = (stepNumber >> 8) & 0xFF
    cmd[5] = bCurr & 0xFF
    cmd[6] = (bCurr >> 8) & 0xFF
    cmd[7] = (bCurr >> 16) & 0xFF
    cmd[8] = (bCurr >> 24) & 0xFF
    cmd[9] = time & 0xFF
    cmd[10] = (time >> 8) & 0xFF
    command(cmd, serial)

def readStepTime(serial):
    """Read one of the step's current and time values."""
    cmd = [0] * 26
    cmd[2] = 0x41
    resp = command(cmd, serial)
    return resp

def saveListFile(location, serial):
    """Save list file in appointed area.
    location - 1-7"""
    cmd = [0] * 26
    cmd[2] = 0x4C
    cmd[3] = location
    command(cmd, serial)

def recallListFile(location, serial):
    """Recall the list file from the appointed area.
    (location) - 1-7"""
    cmd = [0] * 26
    cmd[2] = 0x4D
    return command(cmd, serial)
    
def setTimer(time, serial):
    """Set timer value of FOR LOAD ON
    (time) - seconds"""
    cmd = [0] * 26
    cmd[2] = 0x50
    cmd[3] = time & 0xFF
    cmd[4] = (time >> 8) & 0xFF
    command(cmd, serial)

def readTimer(serial):
    """Read timer value of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x51
    resp = command(cmd, serial)
    return resp

def setTimerState(state, serial):
    """Disable/Enable timer of FOR LOAD ON
    (state) - Boolean True/False"""
    cmd = [0] * 26
    cmd[2] = 0x52
    if state:
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)
    

def readTimerState(serial):
    """Read timer state of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x53
    resp = command(cmd, serial)
    return resp

def setAddress(address, serial):
    """Set communication address
    (address) - 0-31"""
    cmd = [0] * 26
    cmd[2] = 0x54
    cmd[3] = address
    command(cmd, serial)

def setEnableLocalButton(state, serial):
    """Enable/Disable LOCAL control button.
    (state) - Boolean True/False"""
    cmd = [0] * 26
    cmd[2] = 0x55
    if state:
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)

def setEnableRemoteSense(state, serial):
    """Enable/Disable remote sense mode.
    (state) - Boolean True/False"""
    cmd = [0] * 26
    cmd[2] = 0x56
    if state:
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)

def readEnableRemoteSense(serial):
    """Read the state of remote sense mode."""
    cmd = [0] * 26
    cmd[2] = 0x57
    resp = command(cmd, serial)
    return resp

def setTriggerSource(source, serial):
    """Set trigger source.
    source - 0 = manual, 1 = external, 2 = bus, 3 = hold"""
    cmd = [0] * 26
    cmd[2] = 0x58
    cmd[3] = source
    command(cmd, serial)

def readTriggerSource(serial):
    """Read trigger source."""
    cmd = [0] * 26
    cmd[2] = 0x59
    resp = command(cmd, serial)
    return resp

def trigger(serial):
    """Sending a trigger signal to trigging the electronic load."""
    cmd = [0] * 26
    cmd[2] = 0x5A
    command(cmd, serial)

def saveUserSettings(location, serial):
    """Saving user's setting value in appointed memory area for recall."""
    cmd = [0] * 26
    cmd[2] = 0x5B
    cmd[3] = location
    command(cmd, serial)

def recallUserSettings(location, serial):
    """Recall user's setting value in appointed memory area."""
    cmd = [0] * 26
    cmd[2] = 0x5C
    cmd[3] = location
    command(cmd, serial)

def setFunctionMode(function, serial):
    """Set (function):
    function - 0=fixed, 1=short, 2=transient, 3=list, 4=battery"""
    cmd = [0] * 26
    cmd[2] = 0x5D
    cmd[3] = function
    command(cmd, serial)

def readFunctionMode(serial):
    """Read the function mode."""
    cmd = [0] * 26
    cmd[2] = 0x5E
    resp = command(cmd, serial)
    return resp

def readInputLevels(serial):
    """Read input voltage, current, power and relative state"""
    cmd = [0] * 26
    cmd[2] = 0x5F
    resp = command(cmd, serial)
    return resp

def readMaxSettings(serial):
    """Read the information of E-Load (rated current/voltage, min voltage, max power, max resistance, min resistance)"""
    cmd = [0] * 26
    cmd[2] = 0x01
    resp = command(cmd, serial)
    return resp

def readStatusRegister(serial):
    """Read the status register
    0 - Reverse Voltage
    1 - Over Voltage
    2 - Over Current
    3 - Over Power
    4 - Over Temp
    5 - Remote Sense Wire Disconnected
    6 - Constant Current
    7 - Constant Voltage
    8 - Constant Power
    9 - Constant Resistance
    10 - Pass Autotest
    11 - Fail Autotest
    12 - Autotest Complete """
    cmd = [0] * 26
    cmd[2] = 0x00
    resp = command(cmd, serial)
    return resp

def readMaxMinInfo(serial):
    """Set hardware OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x01
    resp = command(cmd, serial)
    return resp

def setOPP(power, serial):
    """Set hardware OPP point"""
    powLim = int(power * 1000) #check this...
    cmd = [0] * 26
    cmd[2] = 0x02
    cmd[3] = powLim & 0xFF
    cmd[4] = (powLim >> 8) & 0xFF
    cmd[4] = (powLim >> 16) & 0xFF
    cmd[4] = (powLim >> 24) & 0xFF
    command(cmd, serial)

def readOPP(serial):
    """Read hardware OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x03
    resp = command(cmd, serial)
    return resp

def setOCP(current, serial):
    """Set software OCP point
    (current) - current limit in Amps"""
    currLim = int(current * 1000) #check this...
    cmd = [0] * 26
    cmd[2] = 0x80
    cmd[3] = currLim & 0xFF
    cmd[4] = (currLim >> 8) & 0xFF
    cmd[4] = (currLim >> 16) & 0xFF
    cmd[4] = (currLim >> 24) & 0xFF
    command(cmd, serial)

def readOCP(serial):
    """Read software OCP point"""
    cmd = [0] * 26
    cmd[2] = 0x81
    resp = command(cmd, serial)
    return resp

def setOCPDelay(serial):
    """Set OCP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x82

def readOCPDelay(serial):
    """Read OCP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x83
    resp = command(cmd, serial)
    return resp

def setEnableOCP(state, serial):
    """Enable/disable OCP function
    (state) - Boolean True/False = On/off"""
    cmd = [0] * 26
    cmd[2] = 0x84
    if state:
        cmd[3] = 1
    else:
        cmd[3] = 0
    command(cmd, serial)

def readEnableOCP(serial):
    """Read the state of OCP function"""
    cmd = [0] * 26
    cmd[2] = 0x85
    resp = command(cmd, serial)
    return resp

def setSoftOPP(power, serial):
    """Set software OPP point
    (power) - power limit in Watts"""
    plim = int(power * 10000)#check this...
    cmd = [0] * 26
    cmd[2] = 0x86
    cmd[3] = plim & 0xFF
    cmd[4] = (plim >> 8) & 0xFF
    cmd[4] = (plim >> 16) & 0xFF
    cmd[4] = (plim >> 24) & 0xFF
    command(cmd, serial)

def readSoftOPP(serial):
    """Read software OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x87
    resp = command(cmd, serial)
    return resp

def setSoftOPPDelay(delay, serial):
    """Set software OPP delay time
    (delay) - time in milliseconds""" #check this...
    cmd = [0] * 26
    cmd[2] = 0x88
    cmd[3] = int(delay)
    command(cmd, serial)

def readSoftOPPDelay(serial):
    """Read software OPP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x89
    resp = command(cmd, serial)
    return resp

def setFirstMeasuredPoint(serial):
    """Set the first measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8A

def readFirstMeasuredPoint(serial):
    """Read the first measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8B
    resp = command(cmd, serial)
    return resp

def setSecondMeasuredPoint(serial):
    """Set the second measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8C

def readSecondMeasuredPoint(serial):
    """Read the second measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8D
    resp = command(cmd, serial)
    return resp

def setVdCRLED(serial):
    """Set Vd value of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x8E

def readVdCRLED(serial):
    """Read Vd value of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x8F
    resp = command(cmd, serial)
    return resp

def clearProtect(serial):
    """Clear the protection state"""
    cmd = [0] * 26
    cmd[2] = 0x90

def setEnableAutorange(serial):
    """Enable/disable voltage autorange function"""
    cmd = [0] * 26
    cmd[2] = 0x91

def readEnableAutorange(serial):
    """Read the state of voltage autorange"""
    cmd = [0] * 26
    cmd[2] = 0x92
    resp = command(cmd, serial)
    return resp

def setEnableCRLED(serial):
    """Enable/disable CR-LED function"""
    cmd = [0] * 26
    cmd[2] = 0x93

def readCRLEDState(serial):
    """Read the state of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x94
    resp = command(cmd, serial)
    return resp

def forceTrigger(serial):
    """Provide a trigger signal, nomatter what the current trigger source it is."""
    cmd = [0] * 26
    cmd[2] = 0x9D
    
def readTimer(serial):
    """Read related information of E-load (working time, the rest time of the timer)"""
    cmd = [0] * 26
    cmd[2] = 0xA0
    resp = command(cmd, serial)
    return resp
        
def readInfo(serial):
    """Read related information of E-load (max input voltage and current, min input votage and current)"""
    cmd = [0] * 26
    cmd[2] = 0xA1
    resp = command(cmd, serial)
    return resp

def readMaxMeasuredVoltage(serial):
    """Read the max measured voltage in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA2
    resp = command(cmd, serial)
    return resp
    
def readMinMeasuredVoltage(serial):
    """Read the min measured voltage in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA3
    resp = command(cmd, serial)
    return resp

def readMaxMeasuredCurrent(serial):
    """Read the max measured current in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA4
    resp = command(cmd, serial)
    return resp

def readMinMeasuredCurrent(serial):
    """Read the min measured current of E-load"""
    cmd = [0] * 26
    cmd[2] = 0xA5
    resp = command(cmd, serial)
    return resp
    
def readCapacity(serial):
    """Read the capacity"""
    cmd = [0] * 26
    cmd[2] = 0xA6
    resp = command(cmd, serial)
    return resp

def setCurrentSlopeRise(serial):
    """Set current rising slope"""
    cmd = [0] * 26
    cmd[2] = 0xB0
    
def readCurrentSlopeRise(serial):
    """Read current rising slope"""
    cmd = [0] * 26
    cmd[2] = 0xB1
    resp = command(cmd, serial)
    return resp

def setCurrentSlopeFall(serial):
    """Set current falling slope"""
    cmd = [0] * 26
    cmd[2] = 0xB2
    
def readCurrentSlopeFall(serial):
    """Read current falling slope"""
    cmd = [0] * 26
    cmd[2] = 0xB3
    resp = command(cmd, serial)
    return resp

def setCCVoltageMax(serial):
    """Set the voltage upper limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB4

def readCCVoltageMax(serial):
    """Read the voltage upper limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB5
    resp = command(cmd, serial)
    return resp

def setCCVoltageMin(serial):
    """Set the voltage lower limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB6

def readCCVoltageMin(serial):
    """Read the voltage lower limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB7
    resp = command(cmd, serial)
    return resp
    
def setCVCurrentMax(serial):
    """Set the current upper limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xB8

def readCVCurrentMax(serial):
    """Read the current upper limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xB9
    resp = command(cmd, serial)
    return resp

def setCVCurrentMin(serial):
    """Set the current lower limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xBA

def readCVCurrentMin(serial):
    """Read the current lower limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xBB
    resp = command(cmd, serial)
    return resp

def setCPVoltageMax(serial):
    """Set the voltage upper limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBC

def readCPVoltageMax(serial):
    """Read the voltage upper limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBD
    resp = command(cmd, serial)
    return resp
    
def setCPVoltageMin(serial):
    """Set the voltage lower limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBE

def readCPVoltageMin(serial):
    """Read the voltage lower limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBF
    resp = command(cmd, serial)
    return resp

def setMaxResistance(serial):
    """Set the max input resistance"""
    cmd = [0] * 26
    cmd[2] = 0xC0

def readMaxResistance(serial):
    """Read the max input resistance"""
    cmd = [0] * 26
    cmd[2] = 0xC1
    resp = command(cmd, serial)
    return resp

def setCRVoltageMax(serial):
    """Set the voltage upper limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC2

def readCRVoltageMax(serial):
    """Read the voltage upper limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC3
    resp = command(cmd, serial)
    return resp

def setCRVoltageMin(serial):
    """Set the voltage lower limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC4

def readCRVoltageMin(serial):
    """Read the voltage lower limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC5
    resp = command(cmd, serial)
    return resp

def setListCurrentRange(serial):
    """Set the current range in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xC6

def readListCurrentRange(serial):
    """Read the current range in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xC7
    resp = command(cmd, serial)
    return resp

def setAutotestSteps(serial):
    """Set step counts of autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xD0

def readAutotestSteps(serial):
    """Read step counts of autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xD1
    resp = command(cmd, serial)
    return resp

def setShortSteps(serial):
    """Set short steps"""
    cmd = [0] * 26
    cmd[2] = 0xD2

def readShortSteps(serial):
    """Read short steps"""
    cmd = [0] * 26
    cmd[2] = 0xD3
    resp = command(cmd, serial)
    return resp
    
def setPauseSteps(serial):
    """Set pause steps"""
    cmd = [0] * 26
    cmd[2] = 0xD4

def readPauseSteps(serial):
    """Read pause steps"""
    cmd = [0] * 26
    cmd[2] = 0xD5
    resp = command(cmd, serial)
    return resp

def setSingleStepTime(serial):
    """Set the on-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD6

def readSingleStepTime(serial):
    """Read the on-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD7
    resp = command(cmd, serial)
    return resp

def setSingleStepDelay(serial):
    """Set the delay time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD8
    
def readSingleStepDelay(serial):
    """Read the delay time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD9
    resp = command(cmd, serial)
    return resp

def setStepNoLoadTime(serial):
    """Set the no-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xDA
    
def readStepNoLoadTime(serial):
    """Read the no-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xDB
    resp = command(cmd, serial)
    return resp

def setAutotestStopCondition(serial):
    """Set autotest stop condition"""
    cmd = [0] * 26
    cmd[2] = 0xDC

def readAutotestStopCondition(serial):
    """Read autotest stop condition"""
    cmd = [0] * 26
    cmd[2] = 0xDD
    resp = command(cmd, serial)
    return resp

def setAutotestChainFile(serial):
    """Set autotest chain file"""
    cmd = [0] * 26
    cmd[2] = 0xDE

def readAutotestChainFile(serial):
    """Read autotest chain file"""
    cmd = [0] * 26
    cmd[2] = 0xDF
    resp = command(cmd, serial)
    return resp

def saveAutotestFile(serial):
    """Save autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xE0

def recallAutotestFile(serial):
    """Recall autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xE1

def setVonMode(serial):
    """Set Von mode"""
    cmd = [0] * 26
    cmd[2] = 0x0E

def readVonMode(serial):
    """Read Von mode"""
    cmd = [0] * 26
    cmd[2] = 0x0F
    resp = command(cmd, serial)
    return resp

def setVonPoint(voltage, serial):
    """Set Von point"""
    value = int(voltage*1000)
    cmd = [0] * 26
    cmd[2] = 0x10
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    command(cmd, serial)

def readVonPoint(serial):
    """Read Von point"""
    cmd = [0] * 26
    cmd[2] = 0x11
    resp = command(cmd, serial)
    return resp

