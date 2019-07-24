class bk8500b:
    cmd = [0]*26
    
    @staticmethod
    def csum(command):  
        checksum = 0
        for i in range(25):     
            checksum = checksum + command[i]                    
        return (0xFF & checksum)                    

    @staticmethod
    def command(command, serial):                          
        command[0] = 0xAA
        command[25] = bk8500b.csum(command)
        serial.write(command)                        
        resp = serial.read(26)

        if resp[3] == 0x80:
            print('Success')
            return
        elif resp[3] == 0x90:
            print('Checksum Error')
        elif resp[3] == 0xA0:
            print('Parameter Incorrect')
        elif resp[3] == 0xB0:
            print('Unrecognized Command')
        elif resp[3] == 0xC0:
            print('Invalid Command')

        print("Command Sent:\t\t",end=' ')
        bk8500b.printCmd(command)

        print("Reponse Received:\t",end=' ')     
        bk8500b.printCmd(resp)
        
    @staticmethod
    def printCmd(buff):
        x = " "        
        for y in range(len(buff)):
            x+=" "
            x+=hex(buff[y]).replace('0x','')   
        print(x)                          

    @staticmethod
    def remoteMode(state, serial):
        print('Remote Mode')
        cmd = [0] * 26
        cmd[2] = 0x20
        if bool(state):
            cmd[3] = 1
        else:
            cmd[3] = 0
        bk8500b.command(cmd, serial)

    @staticmethod
    def inputOn(state, serial):
        print('Input On', state)
        cmd = [0] * 26
        cmd[2] = 0x21
        if bool(state):
            cmd[3] = 1
        else:
            cmd[3] = 0
        bk8500b.command(cmd, serial)
   
    @staticmethod
    def setMaxVoltage(state, serial):
        print('Set Max Voltage')
        cmd = [0] * 26
        cmd[2] = 0x22
        bk8500b.command(cmd, serial)

    @staticmethod
    def readMaxVoltage(state, serial):
        print('Read Max Voltage')
        cmd = [0] * 26
        cmd[2] = 0x23
        bk8500b.command(cmd, serial)
