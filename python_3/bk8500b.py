def csum(command):  
    checksum = 0
    for i in range(25):     
        checksum = checksum + command[i]                    
    return (0xFF & checksum)                    
    
def command(command, serial):                          
    command[0] = 0xAA
    command[25] = bk8500b.csum(command)
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
        bk8500b.printCmd(command)
            
        print("Reponse Received:\t",end=' ')    
        bk8500b.printCmd(resp)
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
    bk8500b.command(cmd, serial)
    
def inputOn(state, serial):
    """Input On. state = True or False"""
    cmd = [0] * 26
    cmd[2] = 0x21
    if bool(state):
        cmd[3] = 1
    else:
        cmd[3] = 0
    bk8500b.command(cmd, serial)
    
def setMaxVoltage(voltage, serial):
    value = int(voltage * 1000)
    """Set Max Voltage"""
    cmd = [0] * 26
    cmd[2] = 0x22
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    bk8500b.command(cmd, serial)
    
def readMaxVoltage(serial):
    """Read Max Voltage"""
    cmd = [0] * 26
    cmd[2] = 0x23
    resp = bk8500b.command(cmd, serial)
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
    bk8500b.command(cmd, serial)

def readMaxCurrent(serial):
    """Read the max setup input current."""
    cmd = [0] * 26
    cmd[2] = 0x25
    resp = bk8500b.command(cmd, serial)
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
    bk8500b.command(cmd, serial)
 

def readMaxPower(serial):
    """Read the max setup input power."""
    cmd = [0] * 26
    cmd[2] = 0x27
    resp = bk8500b.command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00

def setMode(mode, serial):
    """Set operation mode. CC(0)/CV(1)/CW(2)/CR(3)"""
    if mode not in range(0,3):
        raise Exception(("setMode mode=%d: Operation mode not in range 0-3 (cc=0, cv=1, cp=2, cr=3)" % mode).format())
    cmd = [0] * 26
    cmd[2] = 0x28
    cmd[3] = mode
    bk8500b.command(cmd, serial)

def readMode(serial):
    """Read the operation mode."""
    cmd = [0] * 26
    cmd[2] = 0x29
    resp = bk8500b.command(cmd, serial)
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
    resp = bk8500b.command(cmd, serial)
    

def readCCCurrent(serial):
    """Read CC mode current value"""
    cmd = [0] * 26
    cmd[2] = 0x2B
    resp = bk8500b.command(cmd, serial)
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
    bk8500b.command(cmd, serial)
    
def readCVVoltage(serial):
    """Read CV mode voltage value"""
    cmd = [0] * 26
    cmd[2] = 0x2D
    resp = bk8500b.command(cmd, serial)
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
    bk8500b.command(cmd, serial)
    
def readCWPower(serial):
    """Read CW mode watt value"""
    cmd = [0] * 26
    cmd[2] = 0x2F
    resp = bk8500b.command(cmd, serial)
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
    bk8500b.command(cmd, serial)
    
def readCRResistance(serial):
    """Read CR mode resistance value"""
    cmd = [0] * 26
    cmd[2] = 0x31
    resp = bk8500b.command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/1000.00
    
def setCCTransient(serial):
    """Set CC mode transient current and timer parameter."""
    cmd = [0] * 26
    cmd[2] = 0x32

def readCCTransient(serial):
    """Read CC mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x33
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCVTransient(serial):
    """Set CV mode transient voltage and timer parameter."""
    cmd = [0] * 26
    cmd[2] = 0x34

def readCVTransient(serial):
    """Read CV mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x35
    resp = bk8500b.command(cmd, serial)
    return resp

def setCWTransient(serial):
    """Set CW mode transient watt and timer parameter"""
    cmd = [0] * 26
    cmd[2] = 0x36

def readCWTransient(serial):
    """Read CW mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x37
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRTransient(serial):
    """Set CR mode transient resistance and timer parameter"""
    cmd = [0] * 26
    cmd[2] = 0x38

def readCRTransient(serial):
    """Read CR mode transient parameter"""
    cmd = [0] * 26
    cmd[2] = 0x39
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCList(serial):
    """Set the list operation mode (CC)"""
    cmd = [0] * 26
    cmd[2] = 0x3A

def readCCList(serial):
    """Read the list operation mode."""
    cmd = [0] * 26
    cmd[2] = 0x3B
    resp = bk8500b.command(cmd, serial)
    return resp

def setListRepeat(serial):
    """Set the list repeat mode (ONCE/REPEAT)"""
    cmd = [0] * 26
    cmd[2] = 0x3C

def readListRepeat(serial):
    """Read the list repeat mode."""
    cmd = [0] * 26
    cmd[2] = 0x3D
    resp = bk8500b.command(cmd, serial)
    return resp

def setListStepCount(serial):
    """Set list steps counts."""
    cmd = [0] * 26
    cmd[2] = 0x3E

def readListStepCount(serial):
    """Read list steps counts"""
    cmd = [0] * 26
    cmd[2] = 0x3F
    resp = bk8500b.command(cmd, serial)
    return resp

def setStepTime(serial):
    """Set one of the step's current and time values."""
    cmd = [0] * 26
    cmd[2] = 0x40

def readStepTime(serial):
    """Read one of the step's current and time values."""
    cmd = [0] * 26
    cmd[2] = 0x41
    resp = bk8500b.command(cmd, serial)
    return resp

def saveListFile(serial):
    """Save list file in appointed area."""
    cmd = [0] * 26
    cmd[2] = 0x4C

def recallListFile(serial):
    """Recall the list file from the appointed area."""
    cmd = [0] * 26
    cmd[2] = 0x4D
    
def setTimer(serial):
    """Set timer value of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x50

def readTimer(serial):
    """Read timer value of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x51
    resp = bk8500b.command(cmd, serial)
    return resp

def setTimerState(serial):
    """Disable/Enable timer of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x52

def readTimerState(serial):
    """Read timer state of FOR LOAD ON"""
    cmd = [0] * 26
    cmd[2] = 0x53
    resp = bk8500b.command(cmd, serial)
    return resp

def setAddress(serial):
    """Set communication address"""
    cmd = [0] * 26
    cmd[2] = 0x54

def setEnableLocalButton(serial):
    """Enable/Disable LOCAL control button."""
    cmd = [0] * 26
    cmd[2] = 0x55

def setEnableRemoteSense(serial):
    """Enable/Disable remote sense mode."""
    cmd = [0] * 26
    cmd[2] = 0x56

def readEnableRemoteSense(serial):
    """Read the state of remote sense mode."""
    cmd = [0] * 26
    cmd[2] = 0x57
    resp = bk8500b.command(cmd, serial)
    return resp

def setTriggerSource(serial):
    """Set trigger source."""
    cmd = [0] * 26
    cmd[2] = 0x58

def readTriggerSource(serial):
    """Read trigger source."""
    cmd = [0] * 26
    cmd[2] = 0x59
    resp = bk8500b.command(cmd, serial)
    return resp

def trigger(serial):
    """Sending a trigger signal to trigging the electronic load."""
    cmd = [0] * 26
    cmd[2] = 0x5A

def saveUserSettings(serial):
    """Saving user's setting value in appointed memory area for recall."""
    cmd = [0] * 26
    cmd[2] = 0x5B

def recallUserSettings(serial):
    """Recall user's setting value in appointed memory area."""
    cmd = [0] * 26
    cmd[2] = 0x5C

def setFunctionMode(serial):
    """Set function mode (FIXED/SHORT/TRAN/LIST/BATTERY)."""
    cmd = [0] * 26
    cmd[2] = 0x5D

def readFunctionMode(serial):
    """Read function mode state."""
    cmd = [0] * 26
    cmd[2] = 0x5E
    resp = bk8500b.command(cmd, serial)
    return resp

def readInputLevels(serial):
    """Read input voltage, current, power and relative state"""
    cmd = [0] * 26
    cmd[2] = 0x5F
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxSettings(serial):
    """Read the information of E-Load (rated current/voltage, min voltage, max power, max resistance, min resistance)"""
    cmd = [0] * 26
    cmd[2] = 0x01
    resp = bk8500b.command(cmd, serial)
    return resp

def setOPP(serial):
    """Set hardware OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x02

def readOPP(serial):
    """Read hardware OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x03
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOCP(serial):
    """Set software OCP point"""
    cmd = [0] * 26
    cmd[2] = 0x80

def readSoftOCP(serial):
    """Read software OCP point"""
    cmd = [0] * 26
    cmd[2] = 0x81
    resp = bk8500b.command(cmd, serial)
    return resp

def setOCPDelay(serial):
    """Set OCP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x82

def readOCPDelay(serial):
    """Read OCP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x83
    resp = bk8500b.command(cmd, serial)
    return resp

def setEnableOCP(serial):
    """Enable/disable OCP function"""
    cmd = [0] * 26
    cmd[2] = 0x84

def readEnableOCP(serial):
    """Read the state of OCP function"""
    cmd = [0] * 26
    cmd[2] = 0x85
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOPP(serial):
    """Set software OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x86

def readSoftOPP(serial):
    """Read software OPP point"""
    cmd = [0] * 26
    cmd[2] = 0x87
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOPPDelay(serial):
    """Set software OPP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x88

def readSoftOPPDelay(serial):
    """Read software OPP delay time"""
    cmd = [0] * 26
    cmd[2] = 0x89
    resp = bk8500b.command(cmd, serial)
    return resp

def setFirstMeasuredPoint(serial):
    """Set the first measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8A

def readFirstMeasuredPoint(serial):
    """Read the first measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8B
    resp = bk8500b.command(cmd, serial)
    return resp

def setSecondMeasuredPoint(serial):
    """Set the second measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8C

def readSecondMeasuredPoint(serial):
    """Read the second measured point"""
    cmd = [0] * 26
    cmd[2] = 0x8D
    resp = bk8500b.command(cmd, serial)
    return resp

def setVdCRLED(serial):
    """Set Vd value of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x8E

def readVdCRLED(serial):
    """Read Vd value of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x8F
    resp = bk8500b.command(cmd, serial)
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
    resp = bk8500b.command(cmd, serial)
    return resp

def setEnableCRLED(serial):
    """Enable/disable CR-LED function"""
    cmd = [0] * 26
    cmd[2] = 0x93

def readCRLEDState(serial):
    """Read the state of CR-LED mode"""
    cmd = [0] * 26
    cmd[2] = 0x94
    resp = bk8500b.command(cmd, serial)
    return resp

def forceTrigger(serial):
    """Provide a trigger signal, nomatter what the current trigger source it is."""
    cmd = [0] * 26
    cmd[2] = 0x9D
    
def readTimer(serial):
    """Read related information of E-load (working time, the rest time of the timer)"""
    cmd = [0] * 26
    cmd[2] = 0xA0
    resp = bk8500b.command(cmd, serial)
    return resp
        
def readInfo(serial):
    """Read related information of E-load (max input voltage and current, min input votage and current)"""
    cmd = [0] * 26
    cmd[2] = 0xA1
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxMeasuredVoltage(serial):
    """Read the max measured voltage in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA2
    resp = bk8500b.command(cmd, serial)
    return resp
    
def readMinMeasuredVoltage(serial):
    """Read the min measured voltage in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA3
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxMeasuredCurrent(serial):
    """Read the max measured current in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xA4
    resp = bk8500b.command(cmd, serial)
    return resp

def readMinMeasuredCurrent(serial):
    """Read the min measured current of E-load"""
    cmd = [0] * 26
    cmd[2] = 0xA5
    resp = bk8500b.command(cmd, serial)
    return resp
    
def readCapacity(serial):
    """Read the capacity"""
    cmd = [0] * 26
    cmd[2] = 0xA6
    resp = bk8500b.command(cmd, serial)
    return resp

def setCurrentSlopeRise(serial):
    """Set current rising slope"""
    cmd = [0] * 26
    cmd[2] = 0xB0
    
def readCurrentSlopeRise(serial):
    """Read current rising slope"""
    cmd = [0] * 26
    cmd[2] = 0xB1
    resp = bk8500b.command(cmd, serial)
    return resp

def setCurrentSlopeFall(serial):
    """Set current falling slope"""
    cmd = [0] * 26
    cmd[2] = 0xB2
    
def readCurrentSlopeFall(serial):
    """Read current falling slope"""
    cmd = [0] * 26
    cmd[2] = 0xB3
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCVoltageMax(serial):
    """Set the voltage upper limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB4

def readCCVoltageMax(serial):
    """Read the voltage upper limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB5
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCVoltageMin(serial):
    """Set the voltage lower limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB6

def readCCVoltageMin(serial):
    """Read the voltage lower limit in CC mode"""
    cmd = [0] * 26
    cmd[2] = 0xB7
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCVCurrentMax(serial):
    """Set the current upper limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xB8

def readCVCurrentMax(serial):
    """Read the current upper limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xB9
    resp = bk8500b.command(cmd, serial)
    return resp

def setCVCurrentMin(serial):
    """Set the current lower limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xBA

def readCVCurrentMin(serial):
    """Read the current lower limit in CV mode"""
    cmd = [0] * 26
    cmd[2] = 0xBB
    resp = bk8500b.command(cmd, serial)
    return resp

def setCPVoltageMax(serial):
    """Set the voltage upper limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBC

def readCPVoltageMax(serial):
    """Read the voltage upper limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBD
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCPVoltageMin(serial):
    """Set the voltage lower limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBE

def readCPVoltageMin(serial):
    """Read the voltage lower limit in CP mode"""
    cmd = [0] * 26
    cmd[2] = 0xBF
    resp = bk8500b.command(cmd, serial)
    return resp

def setMaxResistance(serial):
    """Set the max input resistance"""
    cmd = [0] * 26
    cmd[2] = 0xC0

def readMaxResistance(serial):
    """Read the max input resistance"""
    cmd = [0] * 26
    cmd[2] = 0xC1
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRVoltageMax(serial):
    """Set the voltage upper limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC2

def readCRVoltageMax(serial):
    """Read the voltage upper limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC3
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRVoltageMin(serial):
    """Set the voltage lower limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC4

def readCRVoltageMin(serial):
    """Read the voltage lower limit in CR mode"""
    cmd = [0] * 26
    cmd[2] = 0xC5
    resp = bk8500b.command(cmd, serial)
    return resp

def setListCurrentRange(serial):
    """Set the current range in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xC6

def readListCurrentRange(serial):
    """Read the current range in list mode"""
    cmd = [0] * 26
    cmd[2] = 0xC7
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestSteps(serial):
    """Set step counts of autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xD0

def readAutotestSteps(serial):
    """Read step counts of autotest file"""
    cmd = [0] * 26
    cmd[2] = 0xD1
    resp = bk8500b.command(cmd, serial)
    return resp

def setShortSteps(serial):
    """Set short steps"""
    cmd = [0] * 26
    cmd[2] = 0xD2

def readShortSteps(serial):
    """Read short steps"""
    cmd = [0] * 26
    cmd[2] = 0xD3
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setPauseSteps(serial):
    """Set pause steps"""
    cmd = [0] * 26
    cmd[2] = 0xD4

def readPauseSteps(serial):
    """Read pause steps"""
    cmd = [0] * 26
    cmd[2] = 0xD5
    resp = bk8500b.command(cmd, serial)
    return resp

def setSingleStepTime(serial):
    """Set the on-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD6

def readSingleStepTime(serial):
    """Read the on-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD7
    resp = bk8500b.command(cmd, serial)
    return resp

def setSingleStepDelay(serial):
    """Set the delay time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD8
    
def readSingleStepDelay(serial):
    """Read the delay time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xD9
    resp = bk8500b.command(cmd, serial)
    return resp

def setStepNoLoadTime(serial):
    """Set the no-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xDA
    
def readStepNoLoadTime(serial):
    """Read the no-load time of single step"""
    cmd = [0] * 26
    cmd[2] = 0xDB
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestStopCondition(serial):
    """Set autotest stop condition"""
    cmd = [0] * 26
    cmd[2] = 0xDC

def readAutotestStopCondition(serial):
    """Read autotest stop condition"""
    cmd = [0] * 26
    cmd[2] = 0xDD
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestChainFile(serial):
    """Set autotest chain file"""
    cmd = [0] * 26
    cmd[2] = 0xDE

def readAutotestChainFile(serial):
    """Read autotest chain file"""
    cmd = [0] * 26
    cmd[2] = 0xDF
    resp = bk8500b.command(cmd, serial)
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
    resp = bk8500b.command(cmd, serial)
    return resp

def setVonPoint(serial):
    """Set Von point"""
    cmd = [0] * 26
    cmd[2] = 0x10

def readVonPoint(serial):
    """Read Von point"""
    cmd = [0] * 26
    cmd[2] = 0x11
    resp = bk8500b.command(cmd, serial)
    return resp

