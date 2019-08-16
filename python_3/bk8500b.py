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
            print('Success')
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
    print('Remote Mode')
    cmd = [0] * 26
    cmd[2] = 0x20
    if bool(state):
        cmd[3] = 1
    else:
        cmd[3] = 0
    bk8500b.command(cmd, serial)
    
def inputOn(state, serial):
    print('Input On', state)
    cmd = [0] * 26
    cmd[2] = 0x21
    if bool(state):
        cmd[3] = 1
    else:
        cmd[3] = 0
    bk8500b.command(cmd, serial)
    
def setMaxVoltage(voltage, serial):
    value = int(voltage * 1000)
    print('Set Max Voltage')
    cmd = [0] * 26
    cmd[2] = 0x22
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    bk8500b.command(cmd, serial)
    
def readMaxVoltage(serial):
    print('Read Max Voltage')
    cmd = [0] * 26
    cmd[2] = 0x23
    resp = bk8500b.command(cmd, serial)
    voltage = resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24)
    return voltage/1000.00
    

def setMaxCurrent(current, serial):
    value = current * 10000
    print("Set max input current: %f" & current)
    cmd = [0] * 26
    cmd[2] = 0x24
    cmd[3] = value & 0xFF
    cmd[4] = (value >> 8) & 0xFF
    cmd[5] = (value >> 16) & 0xFF
    cmd[6] = (value >> 24) & 0xFF
    bk8500b.command(cmd, serial)

def readMaxCurrent(serial):
    print("Read the max setup input current.")
    cmd = [0] * 26
    cmd[2] = 0x25
    resp = bk8500b.command(cmd, serial)
    return (resp[3] + (resp[4]<<8) + (resp[5]<<16) + (resp[6] << 24))/10000.00
    
def setMaxPower(serial):
    print("Set max input power.")
    cmd = [0] * 26
    cmd[2] = 0x26

def readMaxPower(serial):
    print("Read the max setup input power.")
    cmd = [0] * 26
    cmd[2] = 0x27
    resp = bk8500b.command(cmd, serial)
    return resp

def setMode(serial):
    print("Set CC/CV/CW/CR operation mode of electronic load.")
    cmd = [0] * 26
    cmd[2] = 0x28

def readMode(serial):
    print("Read the operation mode.")
    cmd = [0] * 26
    cmd[2] = 0x29
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCCurrent(serial):
    print("Set CC mode current value")
    cmd = [0] * 26
    cmd[2] = 0x2A

def readCCCurrent(serial):
    print("Read CC mode current value")
    cmd = [0] * 26
    cmd[2] = 0x2B
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCVoltage(serial):
    print("Set CV mode voltage value")
    cmd = [0] * 26
    cmd[2] = 0x2C

def readCCVoltage(serial):
    print("Read CV mode voltage value")
    cmd = [0] * 26
    cmd[2] = 0x2D
    resp = bk8500b.command(cmd, serial)
    return resp

def setCWPower(serial):
    print("Set CW mode watt value")
    cmd = [0] * 26
    cmd[2] = 0x2E

def readCWPower(serial):
    print("Read CW mode watt value")
    cmd = [0] * 26
    cmd[2] = 0x2F
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRResistance(serial):
    print("Set CR mode resistance value")
    cmd = [0] * 26
    cmd[2] = 0x30

def readCRResistance(serial):
    print("Read CR mode resistance value")
    cmd = [0] * 26
    cmd[2] = 0x31
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCCTransient(serial):
    print("Set CC mode transient current and timer parameter.")
    cmd = [0] * 26
    cmd[2] = 0x32

def readCCTransient(serial):
    print("Read CC mode transient parameter")
    cmd = [0] * 26
    cmd[2] = 0x33
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCVTransient(serial):
    print("Set CV mode transient voltage and timer parameter.")
    cmd = [0] * 26
    cmd[2] = 0x34

def readCVTransient(serial):
    print("Read CV mode transient parameter")
    cmd = [0] * 26
    cmd[2] = 0x35
    resp = bk8500b.command(cmd, serial)
    return resp

def setCWTransient(serial):
    print("Set CW mode transient watt and timer parameter")
    cmd = [0] * 26
    cmd[2] = 0x36

def readCWTransient(serial):
    print("Read CW mode transient parameter")
    cmd = [0] * 26
    cmd[2] = 0x37
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRTransient(serial):
    print("Set CR mode transient resistance and timer parameter")
    cmd = [0] * 26
    cmd[2] = 0x38

def readCRTransient(serial):
    print("Read CR mode transient parameter")
    cmd = [0] * 26
    cmd[2] = 0x39
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCList(serial):
    print("Set the list operation mode (CC)")
    cmd = [0] * 26
    cmd[2] = 0x3A

def readCCList(serial):
    print("Read the list operation mode.")
    cmd = [0] * 26
    cmd[2] = 0x3B
    resp = bk8500b.command(cmd, serial)
    return resp

def setListRepeat(serial):
    print("Set the list repeat mode (ONCE/REPEAT)")
    cmd = [0] * 26
    cmd[2] = 0x3C

def readListRepeat(serial):
    print("Read the list repeat mode.")
    cmd = [0] * 26
    cmd[2] = 0x3D
    resp = bk8500b.command(cmd, serial)
    return resp

def setListStepCount(serial):
    print("Set list steps counts.")
    cmd = [0] * 26
    cmd[2] = 0x3E

def readListStepCount(serial):
    print("Read list steps counts")
    cmd = [0] * 26
    cmd[2] = 0x3F
    resp = bk8500b.command(cmd, serial)
    return resp

def setStepTime(serial):
    print("Set one of the step's current and time values.")
    cmd = [0] * 26
    cmd[2] = 0x40

def readStepTime(serial):
    print("Read one of the step's current and time values.")
    cmd = [0] * 26
    cmd[2] = 0x41
    resp = bk8500b.command(cmd, serial)
    return resp

def saveListFile(serial):
    print("Save list file in appointed area.")
    cmd = [0] * 26
    cmd[2] = 0x4C

def recallListFile(serial):
    print("Recall the list file from the appointed area.")
    cmd = [0] * 26
    cmd[2] = 0x4D
    
def setTimer(serial):
    print("Set timer value of FOR LOAD ON")
    cmd = [0] * 26
    cmd[2] = 0x50

def readTimer(serial):
    print("Read timer value of FOR LOAD ON")
    cmd = [0] * 26
    cmd[2] = 0x51
    resp = bk8500b.command(cmd, serial)
    return resp

def setTimerState(serial):
    print("Disable/Enable timer of FOR LOAD ON")
    cmd = [0] * 26
    cmd[2] = 0x52

def readTimerState(serial):
    print("Read timer state of FOR LOAD ON")
    cmd = [0] * 26
    cmd[2] = 0x53
    resp = bk8500b.command(cmd, serial)
    return resp

def setAddress(serial):
    print("Set communication address")
    cmd = [0] * 26
    cmd[2] = 0x54

def setEnableLocalButton(serial):
    print("Enable/Disable LOCAL control button.")
    cmd = [0] * 26
    cmd[2] = 0x55

def setEnableRemoteSense(serial):
    print("Enable/Disable remote sense mode.")
    cmd = [0] * 26
    cmd[2] = 0x56

def readEnableRemoteSense(serial):
    print("Read the state of remote sense mode.")
    cmd = [0] * 26
    cmd[2] = 0x57
    resp = bk8500b.command(cmd, serial)
    return resp

def setTriggerSource(serial):
    print("Set trigger source.")
    cmd = [0] * 26
    cmd[2] = 0x58

def readTriggerSource(serial):
    print("Read trigger source.")
    cmd = [0] * 26
    cmd[2] = 0x59
    resp = bk8500b.command(cmd, serial)
    return resp

def trigger(serial):
    print("Sending a trigger signal to trigging the electronic load.")
    cmd = [0] * 26
    cmd[2] = 0x5A

def saveUserSettings(serial):
    print("Saving user's setting value in appointed memory area for recall.")
    cmd = [0] * 26
    cmd[2] = 0x5B

def recallUserSettings(serial):
    print("Recall user's setting value in appointed memory area.")
    cmd = [0] * 26
    cmd[2] = 0x5C

def setFunctionMode(serial):
    print("Set function mode (FIXED/SHORT/TRAN/LIST/BATTERY).")
    cmd = [0] * 26
    cmd[2] = 0x5D

def readFunctionMode(serial):
    print("Read function mode state.")
    cmd = [0] * 26
    cmd[2] = 0x5E
    resp = bk8500b.command(cmd, serial)
    return resp

def readInputLevels(serial):
    print("Read input voltage, current, power and relative state")
    cmd = [0] * 26
    cmd[2] = 0x5F
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxSettings(serial):
    print("Read the information of E-Load (rated current/voltage, min voltage, max power, max resistance, min resistance)")
    cmd = [0] * 26
    cmd[2] = 0x01
    resp = bk8500b.command(cmd, serial)
    return resp

def setOPP(serial):
    print("Set hardware OPP point")
    cmd = [0] * 26
    cmd[2] = 0x02

def readOPP(serial):
    print("Read hardware OPP point")
    cmd = [0] * 26
    cmd[2] = 0x03
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOCP(serial):
    print("Set software OCP point")
    cmd = [0] * 26
    cmd[2] = 0x80

def readSoftOCP(serial):
    print("Read software OCP point")
    cmd = [0] * 26
    cmd[2] = 0x81
    resp = bk8500b.command(cmd, serial)
    return resp

def setOCPDelay(serial):
    print("Set OCP delay time")
    cmd = [0] * 26
    cmd[2] = 0x82

def readOCPDelay(serial):
    print("Read OCP delay time")
    cmd = [0] * 26
    cmd[2] = 0x83
    resp = bk8500b.command(cmd, serial)
    return resp

def setEnableOCP(serial):
    print("Enable/disable OCP function")
    cmd = [0] * 26
    cmd[2] = 0x84

def readEnableOCP(serial):
    print("Read the state of OCP function")
    cmd = [0] * 26
    cmd[2] = 0x85
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOPP(serial):
    print("Set software OPP point")
    cmd = [0] * 26
    cmd[2] = 0x86

def readSoftOPP(serial):
    print("Read software OPP point")
    cmd = [0] * 26
    cmd[2] = 0x87
    resp = bk8500b.command(cmd, serial)
    return resp

def setSoftOPPDelay(serial):
    print("Set software OPP delay time")
    cmd = [0] * 26
    cmd[2] = 0x88

def readSoftOPPDelay(serial):
    print("Read software OPP delay time")
    cmd = [0] * 26
    cmd[2] = 0x89
    resp = bk8500b.command(cmd, serial)
    return resp

def setFirstMeasuredPoint(serial):
    print("Set the first measured point")
    cmd = [0] * 26
    cmd[2] = 0x8A

def readFirstMeasuredPoint(serial):
    print("Read the first measured point")
    cmd = [0] * 26
    cmd[2] = 0x8B
    resp = bk8500b.command(cmd, serial)
    return resp

def setSecondMeasuredPoint(serial):
    print("Set the second measured point")
    cmd = [0] * 26
    cmd[2] = 0x8C

def readSecondMeasuredPoint(serial):
    print("Read the second measured point")
    cmd = [0] * 26
    cmd[2] = 0x8D
    resp = bk8500b.command(cmd, serial)
    return resp

def setVdCRLED(serial):
    print("Set Vd value of CR-LED mode")
    cmd = [0] * 26
    cmd[2] = 0x8E

def readVdCRLED(serial):
    print("Read Vd value of CR-LED mode")
    cmd = [0] * 26
    cmd[2] = 0x8F
    resp = bk8500b.command(cmd, serial)
    return resp

def clearProtect(serial):
    print("Clear the protection state")
    cmd = [0] * 26
    cmd[2] = 0x90

def setEnableAutorange(serial):
    print("Enable/disable voltage autorange function")
    cmd = [0] * 26
    cmd[2] = 0x91

def readEnableAutorange(serial):
    print("Read the state of voltage autorange")
    cmd = [0] * 26
    cmd[2] = 0x92
    resp = bk8500b.command(cmd, serial)
    return resp

def setEnableCRLED(serial):
    print("Enable/disable CR-LED function")
    cmd = [0] * 26
    cmd[2] = 0x93

def readCRLEDState(serial):
    print("Read the state of CR-LED mode")
    cmd = [0] * 26
    cmd[2] = 0x94
    resp = bk8500b.command(cmd, serial)
    return resp

def forceTrigger(serial):
    print("Provide a trigger signal, nomatter what the current trigger source it is.")
    cmd = [0] * 26
    cmd[2] = 0x9D
    
def readTimer(serial):
    print("Read related information of E-load (working time, the rest time of the timer)")
    cmd = [0] * 26
    cmd[2] = 0xA0
    resp = bk8500b.command(cmd, serial)
    return resp
        
def readInfo(serial):
    print("Read related information of E-load (max input voltage and current, min input votage and current)")
    cmd = [0] * 26
    cmd[2] = 0xA1
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxMeasuredVoltage(serial):
    print("Read the max measured voltage in list mode")
    cmd = [0] * 26
    cmd[2] = 0xA2
    resp = bk8500b.command(cmd, serial)
    return resp
    
def readMinMeasuredVoltage(serial):
    print("Read the min measured voltage in list mode")
    cmd = [0] * 26
    cmd[2] = 0xA3
    resp = bk8500b.command(cmd, serial)
    return resp

def readMaxMeasuredCurrent(serial):
    print("Read the max measured current in list mode")
    cmd = [0] * 26
    cmd[2] = 0xA4
    resp = bk8500b.command(cmd, serial)
    return resp

def readMinMeasuredCurrent(serial):
    print("Read the min measured current of E-load")
    cmd = [0] * 26
    cmd[2] = 0xA5
    resp = bk8500b.command(cmd, serial)
    return resp
    
def readCapacity(serial):
    print("Read the capacity")
    cmd = [0] * 26
    cmd[2] = 0xA6
    resp = bk8500b.command(cmd, serial)
    return resp

def setCurrentSlopeRise(serial):
    print("Set current rising slope")
    cmd = [0] * 26
    cmd[2] = 0xB0
    
def readCurrentSlopeRise(serial):
    print("Read current rising slope")
    cmd = [0] * 26
    cmd[2] = 0xB1
    resp = bk8500b.command(cmd, serial)
    return resp

def setCurrentSlopeFall(serial):
    print("Set current falling slope")
    cmd = [0] * 26
    cmd[2] = 0xB2
    
def readCurrentSlopeFall(serial):
    print("Read current falling slope")
    cmd = [0] * 26
    cmd[2] = 0xB3
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCVoltageMax(serial):
    print("Set the voltage upper limit in CC mode")
    cmd = [0] * 26
    cmd[2] = 0xB4

def readCCVoltageMax(serial):
    print("Read the voltage upper limit in CC mode")
    cmd = [0] * 26
    cmd[2] = 0xB5
    resp = bk8500b.command(cmd, serial)
    return resp

def setCCVoltageMin(serial):
    print("Set the voltage lower limit in CC mode")
    cmd = [0] * 26
    cmd[2] = 0xB6

def readCCVoltageMin(serial):
    print("Read the voltage lower limit in CC mode")
    cmd = [0] * 26
    cmd[2] = 0xB7
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCVCurrentMax(serial):
    print("Set the current upper limit in CV mode")
    cmd = [0] * 26
    cmd[2] = 0xB8

def readCVCurrentMax(serial):
    print("Read the current upper limit in CV mode")
    cmd = [0] * 26
    cmd[2] = 0xB9
    resp = bk8500b.command(cmd, serial)
    return resp

def setCVCurrentMin(serial):
    print("Set the current lower limit in CV mode")
    cmd = [0] * 26
    cmd[2] = 0xBA

def readCVCurrentMin(serial):
    print("Read the current lower limit in CV mode")
    cmd = [0] * 26
    cmd[2] = 0xBB
    resp = bk8500b.command(cmd, serial)
    return resp

def setCPVoltageMax(serial):
    print("Set the voltage upper limit in CP mode")
    cmd = [0] * 26
    cmd[2] = 0xBC

def readCPVoltageMax(serial):
    print("Read the voltage upper limit in CP mode")
    cmd = [0] * 26
    cmd[2] = 0xBD
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setCPVoltageMin(serial):
    print("Set the voltage lower limit in CP mode")
    cmd = [0] * 26
    cmd[2] = 0xBE

def readCPVoltageMin(serial):
    print("Read the voltage lower limit in CP mode")
    cmd = [0] * 26
    cmd[2] = 0xBF
    resp = bk8500b.command(cmd, serial)
    return resp

def setMaxResistance(serial):
    print("Set the max input resistance")
    cmd = [0] * 26
    cmd[2] = 0xC0

def readMaxResistance(serial):
    print("Read the max input resistance")
    cmd = [0] * 26
    cmd[2] = 0xC1
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRVoltageMax(serial):
    print("Set the voltage upper limit in CR mode")
    cmd = [0] * 26
    cmd[2] = 0xC2

def readCRVoltageMax(serial):
    print("Read the voltage upper limit in CR mode")
    cmd = [0] * 26
    cmd[2] = 0xC3
    resp = bk8500b.command(cmd, serial)
    return resp

def setCRVoltageMin(serial):
    print("Set the voltage lower limit in CR mode")
    cmd = [0] * 26
    cmd[2] = 0xC4

def readCRVoltageMin(serial):
    print("Read the voltage lower limit in CR mode")
    cmd = [0] * 26
    cmd[2] = 0xC5
    resp = bk8500b.command(cmd, serial)
    return resp

def setListCurrentRange(serial):
    print("Set the current range in list mode")
    cmd = [0] * 26
    cmd[2] = 0xC6

def readListCurrentRange(serial):
    print("Read the current range in list mode")
    cmd = [0] * 26
    cmd[2] = 0xC7
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestSteps(serial):
    print("Set step counts of autotest file")
    cmd = [0] * 26
    cmd[2] = 0xD0

def readAutotestSteps(serial):
    print("Read step counts of autotest file")
    cmd = [0] * 26
    cmd[2] = 0xD1
    resp = bk8500b.command(cmd, serial)
    return resp

def setShortSteps(serial):
    print("Set short steps")
    cmd = [0] * 26
    cmd[2] = 0xD2

def readShortSteps(serial):
    print("Read short steps")
    cmd = [0] * 26
    cmd[2] = 0xD3
    resp = bk8500b.command(cmd, serial)
    return resp
    
def setPauseSteps(serial):
    print("Set pause steps")
    cmd = [0] * 26
    cmd[2] = 0xD4

def readPauseSteps(serial):
    print("Read pause steps")
    cmd = [0] * 26
    cmd[2] = 0xD5
    resp = bk8500b.command(cmd, serial)
    return resp

def setSingleStepTime(serial):
    print("Set the on-load time of single step")
    cmd = [0] * 26
    cmd[2] = 0xD6

def readSingleStepTime(serial):
    print("Read the on-load time of single step")
    cmd = [0] * 26
    cmd[2] = 0xD7
    resp = bk8500b.command(cmd, serial)
    return resp

def setSingleStepDelay(serial):
    print("Set the delay time of single step")
    cmd = [0] * 26
    cmd[2] = 0xD8
    
def readSingleStepDelay(serial):
    print("Read the delay time of single step")
    cmd = [0] * 26
    cmd[2] = 0xD9
    resp = bk8500b.command(cmd, serial)
    return resp

def setStepNoLoadTime(serial):
    print("Set the no-load time of single step")
    cmd = [0] * 26
    cmd[2] = 0xDA
    
def readStepNoLoadTime(serial):
    print("Read the no-load time of single step")
    cmd = [0] * 26
    cmd[2] = 0xDB
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestStopCondition(serial):
    print("Set autotest stop condition")
    cmd = [0] * 26
    cmd[2] = 0xDC

def readAutotestStopCondition(serial):
    print("Read autotest stop condition")
    cmd = [0] * 26
    cmd[2] = 0xDD
    resp = bk8500b.command(cmd, serial)
    return resp

def setAutotestChainFile(serial):
    print("Set autotest chain file")
    cmd = [0] * 26
    cmd[2] = 0xDE

def readAutotestChainFile(serial):
    print("Read autotest chain file")
    cmd = [0] * 26
    cmd[2] = 0xDF
    resp = bk8500b.command(cmd, serial)
    return resp

def saveAutotestFile(serial):
    print("Save autotest file")
    cmd = [0] * 26
    cmd[2] = 0xE0

def recallAutotestFile(serial):
    print("Recall autotest file")
    cmd = [0] * 26
    cmd[2] = 0xE1

def setVonMode(serial):
    print("Set Von mode")
    cmd = [0] * 26
    cmd[2] = 0x0E

def readVonMode(serial):
    print("Read Von mode")
    cmd = [0] * 26
    cmd[2] = 0x0F
    resp = bk8500b.command(cmd, serial)
    return resp

def setVonPoint(serial):
    print("Set Von point")
    cmd = [0] * 26
    cmd[2] = 0x10

def readVonPoint(serial):
    print("Read Von point")
    cmd = [0] * 26
    cmd[2] = 0x11
    resp = bk8500b.command(cmd, serial)
    return resp

