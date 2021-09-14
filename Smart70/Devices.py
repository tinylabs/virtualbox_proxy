#
# Smart70 specific devices
#
#
#
from Device import *
from Packet import *

class Hopper (Device):

    CARDOUT = 0x0000000000000002
    READY = 0x0000000000010000
    PROCESSING = 0x0000000000020000
    CARTRIDGENEAREMPTY = 0x0000000002000000
    CARTRIDGEEMPTY = 0x0000000004000000
    CARTRIDGELOCK = 0x0000000008000000
    CARTRIDGECONTACT = 0x0000000010000000
    CARDOUT = 0x0000000020000000
    REARHOOK = 0x0000000040000000
    FRONTHOOK = 0x0000000080000000
    CARDOUT = 0x0000000200000000
    INIT = 0x0001000000000000
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

    def StatusStr (self, val):
        ret = '\n'
        if val & Hopper.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Hopper.READY:
            ret += '\tREADY\n'
        if val & Hopper.PROCESSING:
            ret += '\tPROCESSING\n'
        if val & Hopper.CARTRIDGENEAREMPTY:
            ret += '\tCARTRIDGENEAREMPTY\n'
        if val & Hopper.CARTRIDGEEMPTY:
            ret += '\tCARTRIDGEEMPTY\n'
        if val & Hopper.CARTRIDGELOCK:
            ret += '\tCARTRIDGELOCK\n'
        if val & Hopper.CARTRIDGECONTACT:
            ret += '\tCARTRIDGECONTACT\n'
        if val & Hopper.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Hopper.REARHOOK:
            ret += '\tREARHOOK\n'
        if val & Hopper.FRONTHOOK:
            ret += '\tFRONTHOOK\n'
        if val & Hopper.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Hopper.INIT:
            ret += '\tINIT\n'
        return ret[:-1]

    # Return direction in relation to passed device
    def Dir (self, dev):
        return Device.DIR_LEFT
    
class Printer (Device):

    SBSRUNNING = 0x0000000000000001
    CARDMOVE = 0x0000000000000002
    CARDIN = 0x0000000000000004
    CARDOUT = 0x0000000000000008
    THEAD = 0x0000000000000010
    SEEKRIBBON = 0x0000000000000020
    MOVERIBBON = 0x0000000000000040
    PRINT = 0x0000000000000080
    MAGRW = 0x0000000000000100
    RECVPRINTDATA = 0x0000000000000200
    INIT = 0x0000000000000400
    READY = 0x0000000000000800
    INSTALLINTENCODER = 0x0000000000008000
    INSTALLEXTHOPPER = 0x0000000000010000
    INSTALLEXTSTACKER = 0x0000000000020000
    INSTALLEXTENCODER = 0x0000000000040000
    INSTALLEXTLAMINATOR = 0x0000000000080000
    INSTALLEXTFLIPPER = 0x0000000000100000
    INSTALLEXTETC = 0x0000000000200000
    CASEOPEN = 0x0000000000400000
    SOFTLOCKED = 0x0000000000800000
    KEYLOCKED = 0x0000000001000000
    DETECTCARD = 0x0000000002000000
    DETECTFRONTDEVICE = 0x0000000004000000
    DETECTREARDEVICE = 0x0000000008000000
    CLEANWARNING = 0x0000000010000000
    HAVEPRINTDATA = 0x0000000020000000
    SBSMODE = 0x0000000040000000
    TESTMODE = 0x0000000080000000
    CARDIN = 0x0000000100000000
    CARDMOVE = 0x0000000200000000
    CARDOUT = 0x0000000400000000
    THEADLIFT = 0x0000000800000000
    PRINT = 0x0000004000000000
    MAGRW = 0x0000008000000000
    MAGREADT1 = 0x0000010000000000
    MAGREADT2 = 0x0000020000000000
    MAGREADT3 = 0x0000040000000000
    CONNECTEXTHOPPER = 0x0000080000000000
    CONNECTEXTSTACKER = 0x0000100000000000
    CONNECTEXTENCODER = 0x0000200000000000
    CONNECTEXTLAMINATOR = 0x0000400000000000
    CONNECTEXTFLIPPER = 0x0000800000000000
    CONNECTEXTETC = 0x0001000000000000
    EXTPRESETMATCH = 0x0002000000000000
    SCHEDULER = 0x0020000000000000
    RIBBONEMPTY = 0x0040000000000000
    RIBBONSEEK = 0x0080000000000000
    RIBBONMOVE = 0x0100000000000000
    THEADABSENT = 0x0200000000000000
    THEADOVERHEAT = 0x0400000000000000
    RIBBONABSENT = 0x0800000000000000
    PRINTDATA = 0x1000000000000000
    INCORRECTPASSWORRD = 0x2000000000000000
    CONFIG = 0x4000000000000000

    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

        self.ATTR['MOVEDIST'] = {
            
            # Get devices
            'ID'   : 0x1260,
            'TYPE' : Packet.SET,
            'REQ'  : self.MoveDistStr,
            'RSP'  : lambda x: struct.unpack ('<I', x[0:4])[0],
            'DEC'  : lambda x: 'OK' if x==0 else 'FAIL'
        }

        # Toggle SBS mode
        self.ATTR['SBSTOGGLE'] = {
            
            # Get devices
            'ID'   : 0x0660,
            'TYPE' : Packet.SET,
            'RSP'  : lambda x: struct.unpack ('<I', x[0:4])[0],
            'DEC'  : lambda x: 'OK' if x==0 else 'FAIL'
        }

    def SBSMode (self, val):
        # Query SBS mode for printer
        curr = True if (self.Status () == Printer.SBSMODE) else False

        # Return if already correct
        if curr == val:
            return

        # Toggle mode
        self.SendRecv ('SBSTOGGLE', struct.pack ('<H', Device.preempt_val))

    def MoveDist (self, dist, vel=1368):
        direction = 0 if dist > 0 else 3
        dist = abs (dist)
        self.SendRecv ('MOVEDIST', struct.pack ('<HBII',
                                                Device.preempt_val,
                                                direction,
                                                int(dist * 10),
                                                vel))
        # Wait for command to finish
        while (self.State () & Device.STATE_RUNNING) != 0:
            time.sleep (0.5)
        
    def MoveDistStr (self, payload):
        preempt = struct.unpack ('<H', payload[0:2])[0]
        direction = 'FWD' if payload[2] == 0 else 'REV'
        dist = struct.unpack ('<I', payload[3:7])[0]
        vel = struct.unpack ('<I', payload[7:11])[0]
        return direction + ' ' + str(float (dist/10)) + 'mm VEL=' + str(vel)
    
    def StatusStr (self, val):
        ret = '\n'
        if val & Printer.SBSRUNNING:
            ret += '\tSBSRUNNING\n'
        if val & Printer.CARDMOVE:
            ret += '\tCARDMOVE\n'
        if val & Printer.CARDIN:
            ret += '\tCARDIN\n'
        if val & Printer.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Printer.THEAD:
            ret += '\tTHEAD\n'
        if val & Printer.SEEKRIBBON:
            ret += '\tSEEKRIBBON\n'
        if val & Printer.MOVERIBBON:
            ret += '\tMOVERIBBON\n'
        if val & Printer.PRINT:
            ret += '\tPRINT\n'
        if val & Printer.MAGRW:
            ret += '\tMAGRW\n'
        if val & Printer.RECVPRINTDATA:
            ret += '\tRECVPRINTDATA\n'
        if val & Printer.INIT:
            ret += '\tINIT\n'
        if val & Printer.READY:
            ret += '\tREADY\n'
        if val & Printer.INSTALLINTENCODER:
            ret += '\tINSTALLINTENCODER\n'
        if val & Printer.INSTALLEXTHOPPER:
            ret += '\tINSTALLEXTHOPPER\n'
        if val & Printer.INSTALLEXTSTACKER:
            ret += '\tINSTALLEXTSTACKER\n'
        if val & Printer.INSTALLEXTENCODER:
            ret += '\tINSTALLEXTENCODER\n'
        if val & Printer.INSTALLEXTLAMINATOR:
            ret += '\tINSTALLEXTLAMINATOR\n'
        if val & Printer.INSTALLEXTFLIPPER:
            ret += '\tINSTALLEXTFLIPPER\n'
        if val & Printer.INSTALLEXTETC:
            ret += '\tINSTALLEXTETC\n'
        if val & Printer.CASEOPEN:
            ret += '\tCASEOPEN\n'
        if val & Printer.SOFTLOCKED:
            ret += '\tSOFTLOCKED\n'
        if val & Printer.KEYLOCKED:
            ret += '\tKEYLOCKED\n'
        if val & Printer.DETECTCARD:
            ret += '\tDETECTCARD\n'
        if val & Printer.DETECTFRONTDEVICE:
            ret += '\tDETECTFRONTDEVICE\n'
        if val & Printer.DETECTREARDEVICE:
            ret += '\tDETECTREARDEVICE\n'
        if val & Printer.CLEANWARNING:
            ret += '\tCLEANWARNING\n'
        if val & Printer.HAVEPRINTDATA:
            ret += '\tHAVEPRINTDATA\n'
        if val & Printer.SBSMODE:
            ret += '\tSBSMODE\n'
        if val & Printer.TESTMODE:
            ret += '\tTESTMODE\n'
        if val & Printer.CARDIN:
            ret += '\tCARDIN\n'
        if val & Printer.CARDMOVE:
            ret += '\tCARDMOVE\n'
        if val & Printer.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Printer.THEADLIFT:
            ret += '\tTHEADLIFT\n'
        if val & Printer.PRINT:
            ret += '\tPRINT\n'
        if val & Printer.MAGRW:
            ret += '\tMAGRW\n'
        if val & Printer.MAGREADT1:
            ret += '\tMAGREADT1\n'
        if val & Printer.MAGREADT2:
            ret += '\tMAGREADT2\n'
        if val & Printer.MAGREADT3:
            ret += '\tMAGREADT3\n'
        if val & Printer.CONNECTEXTHOPPER:
            ret += '\tCONNECTEXTHOPPER\n'
        if val & Printer.CONNECTEXTSTACKER:
            ret += '\tCONNECTEXTSTACKER\n'
        if val & Printer.CONNECTEXTENCODER:
            ret += '\tCONNECTEXTENCODER\n'
        if val & Printer.CONNECTEXTLAMINATOR:
            ret += '\tCONNECTEXTLAMINATOR\n'
        if val & Printer.CONNECTEXTFLIPPER:
            ret += '\tCONNECTEXTFLIPPER\n'
        if val & Printer.CONNECTEXTETC:
            ret += '\tCONNECTEXTETC\n'
        if val & Printer.EXTPRESETMATCH:
            ret += '\tEXTPRESETMATCH\n'
        if val & Printer.SCHEDULER:
            ret += '\tSCHEDULER\n'
        if val & Printer.RIBBONEMPTY:
            ret += '\tRIBBONEMPTY\n'
        if val & Printer.RIBBONSEEK:
            ret += '\tRIBBONSEEK\n'
        if val & Printer.RIBBONMOVE:
            ret += '\tRIBBONMOVE\n'
        if val & Printer.THEADABSENT:
            ret += '\tTHEADABSENT\n'
        if val & Printer.THEADOVERHEAT:
            ret += '\tTHEADOVERHEAT\n'
        if val & Printer.RIBBONABSENT:
            ret += '\tRIBBONABSENT\n'
        if val & Printer.PRINTDATA:
            ret += '\tPRINTDATA\n'
        if val & Printer.INCORRECTPASSWORRD:
            ret += '\tINCORRECTPASSWORRD\n'
        if val & Printer.CONFIG:
            ret += '\tCONFIG\n'
        return ret[:-1]

    # Return direction in relation to passed device
    def Dir (self, dev):
        if isinstance (dev, Hopper):
            return Device.DIR_RIGHT
        else:
            return Device.DIR_LEFT        

class Flipper (Device):

    CARDIN = 0x0000000000000001
    CARDOUT = 0x0000000000000002
    FLIPPING = 0x0000000000000004
    CARDMOVE = 0x0000000000000008
    SMARTREADERDOWN = 0x0000000000000010
    SMARTREADERUP = 0x0000000000000020
    EXTBOARDCONNSENSOR = 0x0000000000000100
    DETECTCARDSCANIN = 0x0000000000000200
    DETECTCARDSCANOUT = 0x0000000000000400
    SMARTREADERCAMSENSOR = 0x0000000000000800
    NOTINSTALLSCANMOD = 0x0000000000001000
    READY = 0x0000000000010000
    PROCESSING = 0x0000000000020000
    V2BOARD = 0x0000000000200000
    FLIPPERBOTTOM = 0x0000000000400000
    FLIPPERTOP = 0x0000000000800000
    CARTRIDGELOCK = 0x0000000001000000
    CASEOPENSENSOR = 0x0000000002000000
    CARTRIDGEFULLSENSOR = 0x0000000004000000
    PCSVERTICALSENSOR = 0x0000000008000000
    PCSHORIZONTALSENSOR = 0x0000000010000000
    DETECTCARDRIGHT = 0x0000000020000000
    DETECTCARDCENTER = 0x0000000040000000
    DETECTCARDLEFT = 0x0000000080000000
    CARDIN = 0x0000000100000000
    CARDOUT = 0x0000000200000000
    FLIP = 0x0000000400000000
    CARDMOVE = 0x0000000800000000
    SMARTREADERDOWN = 0x0000001000000000
    SMARTREADERUP = 0x0000002000000000
    INIT = 0x0001000000000000
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

        self.ATTR['ERROR_BIN'] = {
            
            # Get devices
            'ID'   : 0x1460,
            'TYPE' : Packet.SET,
            'RSP'  : lambda x: struct.unpack ('<I', x[0:4])[0],
            'DEC'  : lambda x: 'OK' if x==0 else 'FAIL'
        }

    def MoveErrorBin (self):
        self.SendRecv ('ERROR_BIN', struct.pack ('<HB', Device.preempt_val, 0xA))
        
    def StatusStr (self, val):
        ret = '\n'
        if val & Flipper.CARDIN:
            ret += '\tCARDIN\n'
        if val & Flipper.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Flipper.FLIPPING:
            ret += '\tFLIPPING\n'
        if val & Flipper.CARDMOVE:
            ret += '\tCARDMOVE\n'
        if val & Flipper.SMARTREADERDOWN:
            ret += '\tSMARTREADERDOWN\n'
        if val & Flipper.SMARTREADERUP:
            ret += '\tSMARTREADERUP\n'
        if val & Flipper.EXTBOARDCONNSENSOR:
            ret += '\tEXTBOARDCONNSENSOR\n'
        if val & Flipper.DETECTCARDSCANIN:
            ret += '\tDETECTCARDSCANIN\n'
        if val & Flipper.DETECTCARDSCANOUT:
            ret += '\tDETECTCARDSCANOUT\n'
        if val & Flipper.SMARTREADERCAMSENSOR:
            ret += '\tSMARTREADERCAMSENSOR\n'
        if val & Flipper.NOTINSTALLSCANMOD:
            ret += '\tNOTINSTALLSCANMOD\n'
        if val & Flipper.READY:
            ret += '\tREADY\n'
        if val & Flipper.PROCESSING:
            ret += '\tPROCESSING\n'
        if val & Flipper.V2BOARD:
            ret += '\tV2BOARD\n'
        if val & Flipper.FLIPPERBOTTOM:
            ret += '\tFLIPPERBOTTOM\n'
        if val & Flipper.FLIPPERTOP:
            ret += '\tFLIPPERTOP\n'
        if val & Flipper.CARTRIDGELOCK:
            ret += '\tCARTRIDGELOCK\n'
        if val & Flipper.CASEOPENSENSOR:
            ret += '\tCASEOPENSENSOR\n'
        if val & Flipper.CARTRIDGEFULLSENSOR:
            ret += '\tCARTRIDGEFULLSENSOR\n'
        if val & Flipper.PCSVERTICALSENSOR:
            ret += '\tPCSVERTICALSENSOR\n'
        if val & Flipper.PCSHORIZONTALSENSOR:
            ret += '\tPCSHORIZONTALSENSOR\n'
        if val & Flipper.DETECTCARDRIGHT:
            ret += '\tDETECTCARDRIGHT\n'
        if val & Flipper.DETECTCARDCENTER:
            ret += '\tDETECTCARDCENTER\n'
        if val & Flipper.DETECTCARDLEFT:
            ret += '\tDETECTCARDLEFT\n'
        if val & Flipper.CARDIN:
            ret += '\tCARDIN\n'
        if val & Flipper.CARDOUT:
            ret += '\tCARDOUT\n'
        if val & Flipper.FLIP:
            ret += '\tFLIP\n'
        if val & Flipper.CARDMOVE:
            ret += '\tCARDMOVE\n'
        if val & Flipper.SMARTREADERDOWN:
            ret += '\tSMARTREADERDOWN\n'
        if val & Flipper.SMARTREADERUP:
            ret += '\tSMARTREADERUP\n'
        if val & Flipper.INIT:
            ret += '\tINIT\n'
        return ret[:-1]

    # Return direction in relation to passed device
    def Dir (self, dev):
        return Device.DIR_RIGHT

class System (Device):
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

        # GET_DEVICES
        self.ATTR['DEVICES'] = {
            
            # Get devices
            'ID'   : 0x3250,
            'TYPE' : Packet.GET,
            'RSP'  : self.GetDevicesDecode,
            'DEC'  : self.GetDevicesStr
        }
        
        # Get preemption
        self.ATTR['PREEMPT+'] = {
            
            # Get devices
            'ID'   : 0x0160,
            'TYPE' : Packet.GET,
            'RSP'  : lambda x: struct.unpack ('<H', x[0:2])[0],
            'DEC'  : lambda x: hex (x)
        }

        # Release preemption
        self.ATTR['PREEMPT-'] = {
            
            # Get devices
            'ID'   : 0x0260,
            'TYPE' : Packet.SET,
            'RSP'  : lambda x: struct.unpack ('<I', x[0:4])[0],
            'DEC'  : lambda x: 'OK' if x==0 else 'FAIL'
        }

    def StatusStr (self, val):
        return ''

    def GetDevicesDecode (self, payload):
        cnt = payload[0]
        dp = payload[1:]
        devs = []
        for n in range (0, cnt):
            dev = Device.Create (dp[n*2], self.conn, dp[n*2+1])
            devs.append (dev)
        return devs

    def GetDevices (self):
        return self.SendRecv ('DEVICES')
    
    def GetDevicesStr (self, devs):
        ret = ''
        for d in devs:
            ret += d.Name () + ' '
        return ret

    def ReqPreempt (self):
        Device.preempt_val = self.SendRecv ('PREEMPT+')
        return Device.preempt_val
    
    def RelPreempt (self):
        self.SendRecv ('PREEMPT-', struct.pack ('<H', Device.preempt_val))
        Device.preempt_val = 0xffff
