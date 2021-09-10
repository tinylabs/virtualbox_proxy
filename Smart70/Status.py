// SMART-70 PRINTER STATUS
//
#define S7PS_M_SBSRUNNING 0x0000000000000001 // doing SBS Command
#define S7PS_M_CARDMOVE 0x0000000000000002 // card is moving
#define S7PS_M_CARDIN 0x0000000000000004 // card is inserting
#define S7PS_M_CARDOUT 0x0000000000000008 // card is ejecting
#define S7PS_M_THEAD 0x0000000000000010 // thermal head lifting
#define S7PS_M_SEEKRIBBON 0x0000000000000020 // seek ribbon
#define S7PS_M_MOVERIBBON 0x0000000000000040 // moving ribbon
#define S7PS_M_PRINT 0x0000000000000080 // printing
#define S7PS_M_MAGRW 0x0000000000000100 // magnetic encoding
#define S7PS_M_RECVPRINTDATA 0x0000000000000200 // receiving print data
#define S7PS_M_INIT 0x0000000000000400 // device initializing
#define S7PS_S_READY 0x0000000000000800 // printer is ready. (valid not be preempted)
#define S7PS_S_INSTALLINTENCODER 0x0000000000008000 // internal encoder is installed
#define S7PS_S_INSTALLEXTHOPPER 0x0000000000010000 // external input-hopper is installed
#define S7PS_S_INSTALLEXTSTACKER 0x0000000000020000 // external output-hopper is installed
#define S7PS_S_INSTALLEXTENCODER 0x0000000000040000 // external encoder is installed
#define S7PS_S_INSTALLEXTLAMINATOR 0x0000000000080000 // external laminator is installed
#define S7PS_S_INSTALLEXTFLIPPER 0x0000000000100000 // external flipper is installed
#define S7PS_S_INSTALLEXTETC 0x0000000000200000 // external etc. module is installed
#define S7PS_S_CASEOPEN 0x0000000000400000 // case is opened
#define S7PS_S_SOFTLOCKED 0x0000000000800000 // soft locked state.
#define S7PS_S_KEYLOCKED 0x0000000001000000 // key locked state.
#define S7PS_S_DETECTCARD 0x0000000002000000 // detect a card
#define S7PS_S_DETECTFRONTDEVICE 0x0000000004000000 // module is connected to left
#define S7PS_S_DETECTREARDEVICE 0x0000000008000000 // module is connected to right
#define S7PS_S_CLEANWARNING 0x0000000010000000 // need cleaning
#define S7PS_S_HAVEPRINTDATA 0x0000000020000000 // have some printing data
#define S7PS_S_SBSMODE 0x0000000040000000 // Manual Mode
#define S7PS_S_TESTMODE 0x0000000080000000 // Test mode.
#define S7PS_E_CARDIN 0x0000000100000000 // failed to insert card
#define S7PS_E_CARDMOVE 0x0000000200000000 // failed to move card
#define S7PS_E_CARDOUT 0x0000000400000000 // failed to eject card
#define S7PS_E_THEADLIFT 0x0000000800000000 // failed to lift thermal head
#define S7PS_E_PRINT 0x0000004000000000 // error while printing
#define S7PS_E_MAGRW 0x0000008000000000 // magnetic encoding error
#define S7PS_E_MAGREADT1 0x0000010000000000 // magnetic ISO track 1 read error

#define S7PS_E_MAGREADT2 0x0000020000000000 // magnetic ISO track 2 read error
#define S7PS_E_MAGREADT3 0x0000040000000000 // magnetic ISO track 3 read error
#define S7PS_E_CONNECTEXTHOPPER 0x0000080000000000 // ext. input-hopper connection failure
#define S7PS_E_CONNECTEXTSTACKER 0x0000100000000000 // ext. output-hopper connection failure
#define S7PS_E_CONNECTEXTENCODER 0x0000200000000000 // external encoder connection failure
#define S7PS_E_CONNECTEXTLAMINATOR 0x0000400000000000 // external laminator connection failure
#define S7PS_E_CONNECTEXTFLIPPER 0x0000800000000000 // external flipper connection failure
#define S7PS_E_CONNECTEXTETC 0x0001000000000000 // ext. etc. module connection failure
#define S7PS_E_EXTPRESETMATCH 0x0002000000000000 // ext. preset module connection failure
#define S7PS_E_SCHEDULER 0x0020000000000000 // scheduler run error
#define S7PS_E_RIBBONEMPTY 0x0040000000000000 // ribbon is empty
#define S7PS_E_RIBBONSEEK 0x0080000000000000 // ribbon search failure
#define S7PS_E_RIBBONMOVE 0x0100000000000000 // ribbon move failure
#define S7PS_F_THEADABSENT 0x0200000000000000 // thermal head is absent
#define S7PS_F_THEADOVERHEAT 0x0400000000000000 // thermal head is overheated
#define S7PS_F_RIBBONABSENT 0x0800000000000000 // ribbon is absent
#define S7PS_F_PRINTDATA 0x1000000000000000 // error on printing data
#define S7PS_F_INCORRECTPASSWORRD 0x2000000000000000 // wrong password
#define S7PS_F_CONFIG 0x4000000000000000 // failed to change printer config.
#define S7IS_M_CARDOUT 0x0000000000000002 // card ejecting
#define S7IS_S_READY 0x0000000000010000 // ready to use
#define S7IS_M_PROCESSING 0x0000000000020000 // doing command
#define S7IS_S_CATRIDGENEAREMPTY 0x0000000002000000 // almost empty cards
#define S7IS_S_CATRIDGEEMPTY 0x0000000004000000 // empty card
#define S7IS_S_CATRIDGELOCK 0x0000000008000000 // detect cartridge lock sensor
#define S7IS_S_CATRIDGECONTACT 0x0000000010000000 // detect cartridge contact sensor
#define S7IS_S_CARDOUT 0x0000000020000000 // detect card-out sensor
#define S7IS_S_REARHOOK 0x0000000040000000 // detect right hook
#define S7IS_S_FRONTHOOK 0x0000000080000000 // detect left hook
#define S7IS_E_CARDOUT 0x0000000200000000 // error while eject card
#define S7IS_F_INIT 0x0001000000000000 // initializing failure
#define S7MS_M_INIT 0x0000000000000001 // initializing
#define S7MS_M_CARDOUT 0x0000000000000002 // card ejecting
#define S7MS_S_READY 0x0000000000000004 // ready to use
#define S7MS_M_PROCESSING 0x0000000000000008 // doing command
#define S7MS_S_HOPPER1CONNECT 0x0000000000000010 // detect hopper 1
#define S7MS_S_HOPPER2CONNECT 0x0000000000000020 // detect hopper 2
#define S7MS_S_HOPPER3CONNECT 0x0000000000000040 // detect hopper 3
#define S7MS_S_HOPPER4CONNECT 0x0000000000000080 // detect hopper 4
#define S7MS_S_HOPPER5CONNECT 0x0000000000000100 // detect hopper 5
#define S7MS_S_HOPPER6CONNECT 0x0000000000000200 // detect hopper 6
#define S7MS_M_HOPPER1RUN 0x0000000000000400 // hopper 1 is running
#define S7MS_M_HOPPER2RUN 0x0000000000000800 // hopper 2 is running
#define S7MS_M_HOPPER3RUN 0x0000000000001000 // hopper 3 is running
#define S7MS_M_HOPPER4RUN 0x0000000000002000 // hopper 4 is running
#define S7MS_M_HOPPER5RUN 0x0000000000004000 // hopper 5 is running
#define S7MS_M_HOPPER6RUN 0x0000000000008000 // hopper 6 is running
#define S7MS_S_LEFTLSENSOR 0x0000000000040000 // left limit sensor
#define S7MS_S_RIGHTLSENSOR 0x0000000000080000 // right limit sensor
#define S7MS_S_SPSENSORA 0x0000000000100000 // shifter position sensor A
#define S7MS_S_SPSENSORB 0x0000000000200000 // shifter position sensor B
#define S7MS_S_SPSENSORC 0x0000000000400000 // shifter position sensor C
#define S7MS_S_SPSENSORD 0x0000000000800000 // shifter position sensor D
#define S7MS_S_CISENSORA0 0x0000000001000000 // card in sensor A0
#define S7MS_S_CISENSORA1 0x0000000002000000 // card in sensor A1
#define S7MS_S_CISENSORB0 0x0000000004000000 // card in sensor B0
#define S7MS_S_CISENSORB1 0x0000000008000000 // card in sensor B1
#define S7MS_S_CISENSORC0 0x0000000010000000 // card in sensor C0
#define S7MS_S_CISENSORC1 0x0000000020000000 // card in sensor C1
#define S7MS_S_CISENSORD0 0x0000000040000000 // card in sensor D0
#define S7MS_S_CISENSORD1 0x0000000080000000 // card in sensor D1
#define S7MS_F_INIT 0x0000000100000000 // initializing fail
#define S7MS_E_CARDOUT 0x0000000200000000 // card out error
#define S7MS_E_RUN 0x0000000800000000 // failed to run command
#define S7MS_E_HOPPER1CONTROL 0x0000001000000000 // hopper 1 control error
#define S7MS_E_HOPPER2CONTROL 0x0000002000000000 // hopper 2 control error
#define S7MS_E_HOPPER3CONTROL 0x0000004000000000 // hopper 3 control error
#define S7MS_E_HOPPER4CONTROL 0x0000008000000000 // hopper 4 control error
#define S7MS_E_HOPPER5CONTROL 0x0000010000000000 // hopper 5 control error
#define S7MS_E_HOPPER6CONTROL 0x0000020000000000 // hopper 6 control error
#define S7MS_E_HOPPER1EMPTY 0x0000040000000000 // hopper 1 is empty
#define S7MS_E_HOPPER2EMPTY 0x0000080000000000 // hopper 2 is empty
#define S7MS_E_HOPPER3EMPTY 0x0000100000000000 // hopper 3 is empty
#define S7MS_E_HOPPER4EMPTY 0x0000200000000000 // hopper 4 is empty
#define S7MS_E_HOPPER5EMPTY 0x0000400000000000 // hopper 5 is empty
#define S7MS_E_HOPPER6EMPTY 0x0000800000000000 // hopper 6 is empty
#define S7MS_E_HOPPER1 0x0001000000000000 // hopper 1 has error
#define S7MS_E_HOPPER2 0x0002000000000000 // hopper 2 has error
#define S7MS_E_HOPPER3 0x0004000000000000 // hopper 3 has error
#define S7MS_E_HOPPER4 0x0008000000000000 // hopper 4 has error
#define S7MS_E_HOPPER5 0x0010000000000000 // hopper 5 has error
#define S7MS_E_HOPPER6 0x0020000000000000 // hopper 6 has error
// SMART-70 OUTPUT-HOPPER (STACKER) STATUS
//
#define S7OS_M_CARDIN 0x0000000000000001 // card inserting
#define S7OS_M_LIFTUP 0x0000000000000004 // lifting up
#define S7OS_M_LIFTDOWN 0x0000000000000008 // lifting down
#define S7OS_S_READY 0x0000000000010000 // ready state
#define S7OS_M_PROCESSING 0x0000000000020000 // doing command
#define S7OS_S_CARDSTANDBY 0x0000000002000000 // detect card standby sensor
#define S7OS_S_CATRIDHAVESPACE 0x0000000004000000 // enough space for card insert
#define S7OS_S_CATRIDGELOCK 0x0000000008000000 // detect cartridge lock sensor
#define S7OS_S_CATRIDGECONTACT 0x0000000010000000 // detect cartridge contact sensor
#define S7OS_S_CARDINENABLER 0x0000000020000000 // detect able to insert card sensor
#define S7OS_S_LIFTUP 0x0000000040000000 // lifted up
#define S7OS_S_DETECTCARDIN 0x0000000080000000 // detect card from card-in sensor.
#define S7OS_E_CARDIN 0x0000000100000000 // error while insert card
#define S7OS_E_LIFTUP 0x0000000400000000 // error while lift up
#define S7OS_E_LIFTDOWN 0x0000000800000000 // error while lift down
#define S7OS_F_INIT
0x0001000000000000 // initializing failure
#define S7FS_M_CARDIN 0x0000000000000001 // card inserting
#define S7FS_M_CARDOUT 0x0000000000000002 // card ejecting
#define S7FS_M_FLIPPING 0x0000000000000004 // card flipping
#define S7FS_M_CARDMOVE 0x0000000000000008 // card moving
#define S7FS_S_SMARTREADERDOWN 0x0000000000000010 // ic contactor contacted (board V2)
#define S7FS_S_SMARTREADERUP 0x0000000000000020 // ic contactor released (board V2)
#define S7FS_S_EXTBOARDCONNSENSOR 0x0000000000000100 // detect ext. board connect sensor (board V2)
#define S7FS_S_DETECTCARDSCANIN 0x0000000000000200 // detect a card at scanner in sensor (board V2)
#define S7FS_S_DETECTCARDSCANOUT 0x0000000000000400 // detect a card at scanner out sensor (board V2)
#define S7FS_S_SMARTREADERCAMSENSOR 0x0000000000000800 // detect ic contactor (board V2)
#define S7FS_S_NOTINSTALLSCANMOD 0x0000000000001000 // not installed scanner module (board V2)
#define S7FS_S_READY 0x0000000000010000 // ready state
#define S7FS_M_PROCESSING 0x0000000000020000 // doing command
#define S7FS_S_V2BOARD 0x0000000000200000 // board V2
#define S7FS_S_FLIPPERBOTTOM 0x0000000000400000 // faced to bottom
#define S7FS_S_FLIPPERTOP 0x0000000000800000 // faced to top
#define S7FS_S_CATRIDGELOCK 0x0000000001000000 // detect cartridge lock sensor
#define S7FS_S_CASEOPENSENSOR 0x0000000002000000 // detect case open sensor. (board V2)
#define S7FS_S_CATRIDGEFULLSENSOR 0x0000000004000000 // cartridge is full
#define S7FS_S_PCSVERTICALSENSOR 0x0000000008000000 // Vertical Position Control Sensor
#define S7FS_S_PCSHORIZONTALSENSOR 0x0000000010000000 // Horizontal Position Control Sensor
#define S7FS_S_DETECTCARDRIGHT 0x0000000020000000 // Detect Card on Right Sensor
#define S7FS_S_DETECTCARDCENTER 0x0000000040000000 // Detect Card on Center Sensor
#define S7FS_S_DETECTCARDLEFT 0x0000000080000000 // Detect Card on Left Sensor
#define S7FS_E_CARDIN 0x0000000100000000 // card insert error
#define S7FS_E_CARDOUT 0x0000000200000000 // card eject error
#define S7FS_E_FLIP 0x0000000400000000 // flipping error
#define S7FS_E_CARDMOVE 0x0000000800000000 // card moving error
#define S7FS_E_SMARTREADERDOWN 0x0000001000000000 // ic contactor contact error (board V2)
#define S7FS_E_SMARTREADERUP 0x0000002000000000 // ic contactor release error (board V2)
#define S7FS_F_INIT 0x0001000000000000 // initialize failure
#define S7LS_M_CARDIN 0x0000000000000001 // card inserting
#define S7LS_M_CARDMOVE 0x0000000000000002 // card moving
#define S7LS_M_CARDOUT 0x0000000000000004 // card ejecting
#define S7LS_M_THEADUP 0x0000000000000008 // thermal head lifting up
#define S7LS_M_THEADDOWN 0x0000000000000010 // thermal head lifting down
#define S7LS_M_THEADHEAT 0x0000000000000020 // thermal head heating
#define S7LS_M_LAMINATING 0x0000000000000040 // laminating
#define S7LS_S_INSTALLEXTHOPPER 0x0000000000000080 // install ext. hopper
#define S7LS_S_INSTALLEXTSTACKER 0x0000000000000100 // install ext. stacker
#define S7LS_S_INSTALLEXTFLIPPER 0x0000000000000200 // install ext. flipper
#define S7LS_S_READY 0x0000000000010000 // ready state
#define S7LS_M_PROCESSING 0x0000000000020000 // doing command
#define S7LS_M_PROCESSUSBCMD 0x0000000000040000 // doing USB command
#define S7LS_S_CASEOPEN 0x0000000000100000 // Case is opened
#define S7LS_S_CATRIDGELOCK 0x0000000000200000 // Detect Cartridge Lock Sensor
#define S7LS_S_CARDOUT 0x0000000000400000 // Detect a card from out sensor
#define S7LS_S_CARDCENTERB 0x0000000000800000 // Detect a card from center sensor B
#define S7LS_S_CARDCENTERA 0x0000000001000000 // Detect a card from center sensor A
#define S7LS_S_CARDIN 0x0000000002000000 // Detect a card from in sensor
#define S7LS_S_THEAD 0x0000000004000000 // Detect head lift sensor
#define S7LS_S_CASEOPENSENSOR 0x0000000008000000 // Detect Case Open Check Sensor
#define S7LS_S_FILMMARKCHECKB 0x0000000010000000 // Film Mark Check Sensor B
#define S7LS_S_FILMMARKCHECKA 0x0000000020000000 // Film Mark Check Sensor A
#define S7LS_S_ENCODERB 0x0000000040000000 // Encoder Sensor B
#define S7LS_S_ENCODERA 0x0000000080000000 // Encoder Sensor A
#define S7LS_E_CARDIN 0x0000000100000000 // error while insert card
#define S7LS_E_CARDMOVE 0x0000000200000000 // error while move card
#define S7LS_E_CARDOUT 0x0000000400000000 // error while eject card
#define S7LS_E_THEADUP 0x0000000800000000 // error while lift up header
#define S7LS_E_THEADDOWN 0x0000001000000000 // error while lift down header
#define S7LS_E_LAMINATING 0x0000002000000000 // error while laminating
#define S7LS_E_INSTALLEXTHOPPER 0x0000008000000000 // ext. flipper connection failure
#define S7LS_E_INSTALLEXTSTACKER 0x0000010000000000 // ext. stacker connection failure
#define S7LS_E_INSTALLEXTFLIPPER 0x0000020000000000 // ext. flipper connection failure
#define S7LS_F_INIT 0x0001000000000000 // initialize failure
#define S7LS_E_PROCESSING 0x0002000000000000 // error while process command
#define S7LS_E_PROCESSUSBCMD 0x0004000000000000 // error while process USB command
#define S7LS_F_FILMEMPTY 0x0010000000000000 // laminate film empty
#define S7LS_F_FILMSEEK 0x0020000000000000 // film seek failure
#define S7LS_F_THEAD 0x0040000000000000 // thermal head error
#define S7LS_F_FILMABSENT 0x0080000000000000 // laminate film is absent
