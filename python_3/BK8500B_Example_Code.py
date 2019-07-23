# IN ORDER TO CONTROL 8500B SERIES WITH 26 BYTE COMMANDS, MUST CHANGE SYS->PROTOCOL TO FRAME
# This is example code for the BK Precision BK8500B Series 
import serial
import time

portNum = input("Which COMM Port? ")
ser = serial.Serial()                 
ser.baudrate = 9600
ser.port = 'COM'+ portNum
ser.timout = 1
ser.open()
ser.flush               # The above lines ask the user for which comm port to open, this will be an integer representing usb port the device is connected to. 
                        # You can check this via the device manager.
                        # For this particular device, this will likely be a USB-to-Serial device


#####__________SET UP___________######


cmd=[0xAA,0,0x20,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xCB]  # First we set the control mode to remote, it will often be the first command you do.
                                                                    # This gives a preview as to the format.
ser.write(cmd)
confirm = ser.read(26)                                              # NO ERROR response we will use later
print(confirm)                                                      

cmd=[0xAA,0,0x5D,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0x07]  # Here we set function mode to fixed
ser.write(cmd)
print(ser.read(26))
print("\n")


#####__________END SET UP___________######

#####__________TUTORIAL___________######


# Lets contstruct a command, similar to the one above, byte by byte. The BK8500B series supports SCPI, which is much easier to use. 
# However some commands are not supported via SCPI and can only be used via the legacy protocol called FRAME.
# FRAME is a 26 byte command format. We will over the basic creation of a command below.

print("Turning Input ON")
cmd = [0]*26    # This creates a 26 byte packet, we will edit this packet to be useful to the DC Load
cmd[0] = 0xAA   # The first byte is always AAh or 0xAA, this is called the start bit. 
cmd[1] = 0      # The second byte is the address byte, which has a range of 0 to 31 with 0xFF being the broadcast address. This is used if multiple devices are
                # chained together. We will leave this at 0
cmd[2] = 0x21   # The third byte is the command, a list of command bytes is in the programming guide. All commands are 1 byte. We want to edit the input state, so we do command 21H.
cmd[3] = 0x01   # Bytes 4 to 25 depend on the command. Some commands will use more of them than others. The input state command only needs one of these bytes because the
                # state is either 0 (off) or 1 (on). So we set the fourth byte to 1 and leave the remaining 20 at 0.
                # The 26th byte is the checksum, the addition of all previous bytes. We will calculate this manually, but later we will create a function to do it for us.
checkSum = (cmd[0] + cmd[2] + cmd[3]) & 0xFF        # We limit the check sum to 1 byte by ANDing it with 0xFF
cmd[25] = checkSum

ser.write(cmd)       # We write our command to the serial port.
print(ser.read(26))  # Lastly we read the response. The reponse 0x12/0x08 is an error free confirmation. We MUST read the response every time. If we don't, the responses will queue up.
                     # The Command Prompt (Windows) will automatically turn hex values into ascii characters. Because of this, the response may be difficult to read. 
                     # We will create a function below to make reponses more readable as well as other useful functions
print("\n")


#####__________END TUTORIAL___________######

#####__________USEFUL FUNCTIONS___________######

def csum(command):                          # this function automatically calculates the checksum
    sum = 0
    for i in range((len(command) - 1)):     
        sum+= command[i]                    # this loop sums the all the bytes of the input except for the last one
    return (0xFF & sum)                     # because some sums may overflow two bytes, we shorten the sum to two bytes

def Printer(read):                          # this function makes the 26 byte format more readable
    x = " "        
    for y in range(len(read)):
        x+=" "
        x+=hex(read[y]).replace('0x','')    # replaces the 0x with a spacing instead
    print(x)                                # and prints it


def Command(com):                           # We will use this function to send commands and receive replies    
    com[0] = 0xAA                           # Automatically sets the start bit
    com[25] = csum(com)                     # Automatically places the checksum
    print("Command Sent:\t\t",end=' ')
    Printer(com)                            # Prints the command in a readable format
    ser.write(com)                          # Writes the command
    print("Reponse Received:\t",end=' ')     
    resp = ser.read(26)
    if(resp == confirm):
        print("\tNo Error")                 # If we receive the no error string, print "No Error"
    else:
        Printer(resp)                       # Else Print the String 
    print("\n")


#####__________END USEFUL FUNCTIONS___________######

#####__________OPERATING MODE AND VALUE SETTING___________######

time.sleep(1)
# Now lets go through some operations!

# Turn input off again
print("Turning Input OFF")
cmd = [0] * 26
cmd[2] = 0x21                       # Notice with the new function, we only have to input the command specific bytes
Command(cmd)  

# Setting Mode (CC, CW, CV, CR)
print("Setting Mode to Constant Resistance")
cmd = [0] * 26
cmd[2] = 0x28                       # Set Operation Mode
cmd[3] = 3                          # Constant Resistance.
Command(cmd)

# Lets check the mode is what we set it to
print("What mode are we in?")
cmd = [0] * 26
cmd[2] = 0x29                       # Enquire Operation Mode
Command(cmd)   
  
time.sleep(2)

print("Setting Mode to Constant Current")
cmd = [0] * 26
cmd[2] = 0x28                       # Set Operation Mode Command, constant current mode is 0
Command(cmd)                        # Setting back to constant current mode

print("Setting a Constant Current of 5.025 Amperes")
cmd = [0] * 26
cmd[2] = 0x2A                       # Constant Current Value Command                     
cmd[3] = 0x4A                       # For setting maximum values, each unit in hex (0x01) represents 1mV/0.1mA/0.1mS/1mW/1mOhm. Notice amperes and seconds are smaller.
cmd[4] = 0xC4                       # Setting the maximum current to 5.025 requires us to divide 5.025 by 0.0001 or multiply it by 10000 which equals 50250 or 0xC44A. 
                                    # We read from right to left, the right most byte we set equal to the 4th byte
cmd[5] = 0                          # We then move left and set that equal to the 5th byte. 
                                    # For 0x0000C44A -> 00 | 00 | C4 | 4A -> 4th = 4A, 5th = C4, 6th = 00, and 7th = 00.
cmd[6] = 0                          # This command only utilizes up the the 7th byte, so the remaining bytes are zero.
Command(cmd)                        

print("Setting a Maximum Current of 10 Amperes")
cmd = [0] * 26
cmd[2] = 0x24                       # Maximum Current Command                     
cmd[3] = 0xA0              
cmd[4] = 0x86      
cmd[5] = 0x01                                    
Command(cmd)  
  
print("Reading Maximum Current")
cmd = [0] * 26
cmd[2] = 0x25                       # Read Maximum Current Command                                               
Command(cmd) 

print("Reading Constant Current")
cmd = [0] * 26
cmd[2] = 0x2B                       # Read Constant Current Command
Command(cmd)
time.sleep(1)


#####__________END OPERATING MODE AND VALUE SETTING___________######

#####__________LISTS___________######


print("\n")
# LISTS (Can Only Create Lists for Constant Current)
print("Creating Current List...")
# WARNING: CANNOT SAVE OR LOAD LISTS WHILE IN LIST MODE
print("\n")

print("Reading Function Mode")
cmd = [0] * 26
cmd[2] = 0x5E                       # Reading List Function Mode
Command(cmd)

print("Reading List 1")
cmd = [0] * 26
cmd[2] = 0x4D                       # Selecting List 1
cmd[3] = 1
Command(cmd)

print("Setting List Operation Mode to Constant Current")
cmd = [0] * 26
cmd[2] = 0x3A                       # Setting List Operation Mode to Constant Current
cmd[3] = 0                                                 
Command(cmd)

print("Reading List Operation Mode")
cmd = [0] * 26
cmd[2] = 0x3B                       # Reading List Operation Mode
Command(cmd)

print("Setting List to 5 Steps")
cmd = [0] * 26
cmd[2] = 0x3E                       # Setting List 1 Step Counts to 5 Steps
cmd[3] = 0x05
Command(cmd)

print("Reading List Step Count")
cmd = [0] * 26
cmd[2] = 0x3F                       # Reading List Step Count
Command(cmd)

time.sleep(1)
print("Compiling List")
cmd = [0] * 26
cmd[2] = 0x40                       # List Step Value Setting
cmd[3] = 1
cmd[4] = 0                          # 4th and 5th byte are list step     # Step 1
cmd[5] = 0xA0
cmd[6] = 0x86
cmd[7] = 0x01
cmd[8] = 0x00                       # 6th, 7th, 8th, and 9th bytes are current amplitude values  # 10 Amps
cmd[9] = 0x20
cmd[10] = 0x4E                      # 10th and 11th bytes are time values. 0x01 represents 0.1ms     # 2 Seconds
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x40                      
cmd[3] = 2                          # Step 2
cmd[4] = 0                         
cmd[5] = 0x50
cmd[6] = 0xC3
cmd[7] = 0x00
cmd[8] = 0x00                       # 5 Amperes                   
cmd[9] = 0x50
cmd[10] =  0xC3                     # 5 Seconds
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x40                      
cmd[3] = 3                          # Step 3                      
cmd[4] = 0
cmd[5] = 0x4A
cmd[6] = 0xC4                       # 5.025 Amperes           
cmd[9] = 0x88
cmd[10] = 0x13                      # 0.5 
                     
Command(cmd)
cmd = [0] * 26
cmd[2] = 0x40                       
cmd[3] = 4                          # Step 4                     
cmd[5] = 0xC4                  
cmd[6] = 0x09                       # 250 mA                       
cmd[9] = 0x20
cmd[10] = 0x4E                      # 2 Seconds              
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x40                      
cmd[3] = 5                          # Step 5
cmd[5] = 0x28
cmd[6] = 0x1D
cmd[7] = 0x01                       # 7.3 Amperes
cmd[9] = 0xFF
cmd[10] = 0xFF                      # Maximum Time: 6.5535 Seconds
Command(cmd)

time.sleep(1)
print("\n")
print("Saving List")
cmd = [0] * 26
cmd[2] = 0x4C                       # Saving List
cmd[3] = 1                          # To Slot 1
Command(cmd)
time.sleep(1)

print("Reading List")
cmd = [0] * 26
cmd[2] = 0x41                       # Reading Step Value
cmd[3] = 1                           # Step 1
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x41                       # Reading Step Value
cmd[3] = 2                           # Step 2
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x41                       # Reading Step Value
cmd[3] = 3                           # Step 3
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x41                       # Reading Step Value
cmd[3] = 4                           # Step 4
Command(cmd)

cmd = [0] * 26
cmd[2] = 0x41                       # Reading Step Value
cmd[3] = 5                           # Step 5
Command(cmd)
print("\n")



time.sleep(1)
print("Setting List to Repeat 3 Times")
cmd = [0] * 26
cmd[2] = 0x3C                       # Set Repeat Amount to 3 Times
cmd[3] = 3
Command(cmd)

print("Setting Trigger Mode to Bus")
cmd = [0] * 26
cmd[2] = 0x58                  
cmd[3] = 2                          # Set Trigger Mode to Bus, this allows us to trigger remotely
Command(cmd)

print("Turning Input ON")
cmd = [0] * 26
cmd[2] = 0x21                
cmd[3] = 0x01
Command(cmd)  

print("Entering List Mode")
cmd = [0] * 26
cmd[2] = 0x5D                       # Selecting List Function Mode
cmd[3] = 3                          # When in List mode, the BK8500 will display new parameters. On the bottom left is the Operation mode.
Command(cmd)                        # On the bottom middle is the list number in the form 'L#' where # is a number               
                                    # from 1 to 7. Lastly in the bottom right is the list repeation and step number in the form 'R.S'.
                                    # R is the repetition count and S is the step count.
                                    # For example our list will go from 1.1 to 1.5 then from 2.1 to 2.5 and lastly from 3.1 to 3.5. 
                                    # This is because it has 5 steps and repeats 3 times.

print("Sending Trigger Signal")
cmd = [0] * 26
cmd[2] = 0x5A                       # Send Trigger Signal
Command(cmd)                        

time.sleep(45)                      # Must set delay longer than list mode time, we can in fact overwrite list mode actions


#####__________END LISTS___________######

#####__________TRANSIENT MODE___________######

print("Turning Input OFF")
cmd = [0] * 26
cmd[2] = 0x21   
Command(cmd)  

cmd = [0] * 26
cmd[2] = 0x5D                       # Selecting Function Mode
cmd[3] = 0                          # Returning to Fixed Mode
Command(cmd)


print("\n")
print("Setting Mode to Constant Power")
cmd = [0] * 26
cmd[2] = 0x28                       # Set Operation Mode, this will detirmine which transient operation we perform
cmd[3] = 2                          # Constant Power.
Command(cmd)

print("\n")
print("Adjusting Transient Mode Parameters")
print("\n")

cmd = [0] * 26
print("Power A = 150 W")
cmd[2] = 0x36
cmd[3] = 0xF0
cmd[4] = 0x49
cmd[5] = 0x02
cmd[6] = 0x00                       # 150000

print("Time A = 2 S")
cmd[7] = 0x20
cmd[8] = 0x4E                       # 20000

print("Power B = 1 W")
cmd[9] = 0xE8
cmd[10] = 0x03
cmd[11] = 0x00
cmd[12] = 0x00                      # 10000

print("Time B = 4 S")
cmd[13] = 0x40
cmd[14] = 0x9C                      # 40000        # Adjusting Time A and B adjusts Frequency and Duty Cycle.

print("Transition Operation Mode: Continuous")
cmd[15] = 0x00                 
Command(cmd)

print("Turning Input ON")
cmd = [0] * 26
cmd[2] = 0x21                
cmd[3] = 0x01
Command(cmd)  

print("Entering Transient CW Mode...")
cmd = [0] * 26
cmd[2] = 0x5D                       # Selecting Function Mode
cmd[3] = 2                          # Transient Mode
Command(cmd)

print("Sending Trigger Signal")
cmd = [0] * 26
cmd[2] = 0x5A                       # Send Trigger Signal
Command(cmd)                        


time.sleep(20)


#####__________END TRANSIENT MODE___________######

#####__________CLEAN UP___________######


print("Closing...")

cmd = [0] * 26
cmd[2] = 0x21                       # Turning Input Off           
Command(cmd) 

cmd = [0] * 26
cmd[2] = 0x5D                       # Selecting List Function Mode
cmd[3] = 0                          # Returning to Fixed Mode
Command(cmd)

time.sleep(0.1)
cmd = [0] * 26
cmd[2] = 0x58                  
cmd[3] = 0                          # Set Trigger Mode to Manual 
Command(cmd)

time.sleep(0.1)
cmd = [0] * 26
cmd[2] = 0x20
cmd[3] = 0
Command(cmd)                        # Going to Local Mode

print("Goodbye")
ser.close()


#####__________END___________######
