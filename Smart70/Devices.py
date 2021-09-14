#
# Smart70 specific devices
#
#
#
from Device import *
from Packet import *

class Hopper (Device):
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

    def StatusStr (self, val):
        ret = '\n'
        if val & 0x0000000000000002:
            ret += '\tCARDOUT\n'
        if val & 0x0000000000010000:
            ret += '\tREADY\n'
        if val & 0x0000000000020000:
            ret += '\tPROCESSING\n'
        if val & 0x0000000002000000:
            ret += '\tCATRIDGENEAREMPTY\n'
        if val & 0x0000000004000000:
            ret += '\tCATRIDGEEMPTY\n'
        if val & 0x0000000008000000:
            ret += '\tCATRIDGELOCK\n'
        if val & 0x0000000010000000:
            ret += '\tCATRIDGECONTACT\n'
        if val & 0x0000000020000000:
            ret += '\tCARDOUT\n'
        if val & 0x0000000040000000:
            ret += '\tREARHOOK\n'
        if val & 0x0000000080000000:
            ret += '\tFRONTHOOK\n'
        if val & 0x0000000200000000:
            ret += '\tCARDOUT\n'
        if val & 0x0001000000000000:
            ret += '\tINIT\n'
        return ret[:-1]

    # Return direction in relation to passed device
    def Dir (self, dev):
        return Device.DIR_LEFT
    
class Printer (Device):
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

    def StatusStr (self, val):
        ret = '\n'
        if val & 0x0000000000000001:
            ret += '\tSBSRUNNING\n'
        if val & 0x0000000000000002:
            ret += '\tCARDMOVE\n'
        if val & 0x0000000000000004:
            ret += '\tCARDIN\n'
        if val & 0x0000000000000008:
            ret += '\tCARDOUT\n'
        if val & 0x0000000000000010:
            ret += '\tTHEAD\n'
        if val & 0x0000000000000020:
            ret += '\tSEEKRIBBON\n'
        if val & 0x0000000000000040:
            ret += '\tMOVERIBBON\n'
        if val & 0x0000000000000080:
            ret += '\tPRINT\n'
        if val & 0x0000000000000100:
            ret += '\tMAGRW\n'
        if val & 0x0000000000000200:
            ret += '\tRECVPRINTDATA\n'
        if val & 0x0000000000000400:
            ret += '\tINIT\n'
        if val & 0x0000000000000800:
            ret += '\tREADY\n'
        if val & 0x0000000000008000:
            ret += '\tINSTALLINTENCODER\n'
        if val & 0x0000000000010000:
            ret += '\tINSTALLEXTHOPPER\n'
        if val & 0x0000000000020000:
            ret += '\tINSTALLEXTSTACKER\n'
        if val & 0x0000000000040000:
            ret += '\tINSTALLEXTENCODER\n'
        if val & 0x0000000000080000:
            ret += '\tINSTALLEXTLAMINATOR\n'
        if val & 0x0000000000100000:
            ret += '\tINSTALLEXTFLIPPER\n'
        if val & 0x0000000000200000:
            ret += '\tINSTALLEXTETC\n'
        if val & 0x0000000000400000:
            ret += '\tCASEOPEN\n'
        if val & 0x0000000000800000:
            ret += '\tSOFTLOCKED\n'
        if val & 0x0000000001000000:
            ret += '\tKEYLOCKED\n'
        if val & 0x0000000002000000:
            ret += '\tDETECTCARD\n'
        if val & 0x0000000004000000:
            ret += '\tDETECTFRONTDEVICE\n'
        if val & 0x0000000008000000:
            ret += '\tDETECTREARDEVICE\n'
        if val & 0x0000000010000000:
            ret += '\tCLEANWARNING\n'
        if val & 0x0000000020000000:
            ret += '\tHAVEPRINTDATA\n'
        if val & 0x0000000040000000:
            ret += '\tSBSMODE\n'
        if val & 0x0000000080000000:
            ret += '\tTESTMODE\n'
        if val & 0x0000000100000000:
            ret += '\tCARDIN\n'
        if val & 0x0000000200000000:
            ret += '\tCARDMOVE\n'
        if val & 0x0000000400000000:
            ret += '\tCARDOUT\n'
        if val & 0x0000000800000000:
            ret += '\tTHEADLIFT\n'
        if val & 0x0000004000000000:
            ret += '\tPRINT\n'
        if val & 0x0000008000000000:
            ret += '\tMAGRW\n'
        if val & 0x0000010000000000:
            ret += '\tMAGREADT1\n'
        if val & 0x0000020000000000:
            ret += '\tMAGREADT2\n'
        if val & 0x0000040000000000:
            ret += '\tMAGREADT3\n'
        if val & 0x0000080000000000:
            ret += '\tCONNECTEXTHOPPER\n'
        if val & 0x0000100000000000:
            ret += '\tCONNECTEXTSTACKER\n'
        if val & 0x0000200000000000:
            ret += '\tCONNECTEXTENCODER\n'
        if val & 0x0000400000000000:
            ret += '\tCONNECTEXTLAMINATOR\n'
        if val & 0x0000800000000000:
            ret += '\tCONNECTEXTFLIPPER\n'
        if val & 0x0001000000000000:
            ret += '\tCONNECTEXTETC\n'
        if val & 0x0002000000000000:
            ret += '\tEXTPRESETMATCH\n'
        if val & 0x0020000000000000:
            ret += '\tSCHEDULER\n'
        if val & 0x0040000000000000:
            ret += '\tRIBBONEMPTY\n'
        if val & 0x0080000000000000:
            ret += '\tRIBBONSEEK\n'
        if val & 0x0100000000000000:
            ret += '\tRIBBONMOVE\n'
        if val & 0x0200000000000000:
            ret += '\tTHEADABSENT\n'
        if val & 0x0400000000000000:
            ret += '\tTHEADOVERHEAT\n'
        if val & 0x0800000000000000:
            ret += '\tRIBBONABSENT\n'
        if val & 0x1000000000000000:
            ret += '\tPRINTDATA\n'
        if val & 0x2000000000000000:
            ret += '\tINCORRECTPASSWORRD\n'
        if val & 0x4000000000000000:
            ret += '\tCONFIG\n'
        return ret[:-1]

    # Return direction in relation to passed device
    def Dir (self, dev):
        if isinstance (dev, Hopper):
            return Device.DIR_RIGHT
        else:
            return Device.DIR_LEFT        

class Flipper (Device):
    
    def __init__ (self, dev_id, conn, int_id):
        super().__init__ (dev_id, conn, int_id)

    def StatusStr (self, val):
        ret = '\n'
        if val & 0x0000000000000001:
            ret += '\tCARDIN\n'
        if val & 0x0000000000000002:
            ret += '\tCARDOUT\n'
        if val & 0x0000000000000004:
            ret += '\tFLIPPING\n'
        if val & 0x0000000000000008:
            ret += '\tCARDMOVE\n'
        if val & 0x0000000000000010:
            ret += '\tSMARTREADERDOWN\n'
        if val & 0x0000000000000020:
            ret += '\tSMARTREADERUP\n'
        if val & 0x0000000000000100:
            ret += '\tEXTBOARDCONNSENSOR\n'
        if val & 0x0000000000000200:
            ret += '\tDETECTCARDSCANIN\n'
        if val & 0x0000000000000400:
            ret += '\tDETECTCARDSCANOUT\n'
        if val & 0x0000000000000800:
            ret += '\tSMARTREADERCAMSENSOR\n'
        if val & 0x0000000000001000:
            ret += '\tNOTINSTALLSCANMOD\n'
        if val & 0x0000000000010000:
            ret += '\tREADY\n'
        if val & 0x0000000000020000:
            ret += '\tPROCESSING\n'
        if val & 0x0000000000200000:
            ret += '\tV2BOARD\n'
        if val & 0x0000000000400000:
            ret += '\tFLIPPERBOTTOM\n'
        if val & 0x0000000000800000:
            ret += '\tFLIPPERTOP\n'
        if val & 0x0000000001000000:
            ret += '\tCATRIDGELOCK\n'
        if val & 0x0000000002000000:
            ret += '\tCASEOPENSENSOR\n'
        if val & 0x0000000004000000:
            ret += '\tCATRIDGEFULLSENSOR\n'
        if val & 0x0000000008000000:
            ret += '\tPCSVERTICALSENSOR\n'
        if val & 0x0000000010000000:
            ret += '\tPCSHORIZONTALSENSOR\n'
        if val & 0x0000000020000000:
            ret += '\tDETECTCARDRIGHT\n'
        if val & 0x0000000040000000:
            ret += '\tDETECTCARDCENTER\n'
        if val & 0x0000000080000000:
            ret += '\tDETECTCARDLEFT\n'
        if val & 0x0000000100000000:
            ret += '\tCARDIN\n'
        if val & 0x0000000200000000:
            ret += '\tCARDOUT\n'
        if val & 0x0000000400000000:
            ret += '\tFLIP\n'
        if val & 0x0000000800000000:
            ret += '\tCARDMOVE\n'
        if val & 0x0000001000000000:
            ret += '\tSMARTREADERDOWN\n'
        if val & 0x0000002000000000:
            ret += '\tSMARTREADERUP\n'
        if val & 0x0001000000000000:
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
        Packet.byte2hex (payload)
        cnt = payload[0]
        dp = payload[1:]
        devs = []
        for n in range (0, cnt):
            dev = Device.Create (dp[n*2], self.conn, dp[n*2+1])
            devs.append (dev)
        return devs

    def GetDevices (self):
        return self.Get ('DEVICES')
    
    def GetDevicesStr (self, devs):
        ret = ''
        for d in devs:
            ret += d.Name () + ' '
        return ret

    def ReqPreempt (self):
        Device.preempt_val = self.Get ('PREEMPT+')
        return Device.preempt_val
    
    def RelPreempt (self):
        self.Set ('PREEMPT-', struct.pack ('<H', Device.preempt_val))
        Device.preempt_val = 0xffff
