# Versin: 37.14643.2019.0511
# We use ctypes to call into the nncam.dll/libnncam.so/libnncam.dylib API,
# the python class NnCam is a thin wrapper class to the native api of nncam.dll/libnncam.so/libnncam.dylib.
# So the manual en.html(English) and hans.html(Simplified Chinese) are also applicable for programming with nncam.py.
# See them in the 'doc' directory:
#    (1) en.html, English
#    (2) hans.html, Simplified Chinese
#
import sys, ctypes, os.path

NNCAM_MAX = 16

NNCAM_FLAG_CMOS                = 0x00000001          # cmos sensor
NNCAM_FLAG_CCD_PROGRESSIVE     = 0x00000002          # progressive ccd sensor
NNCAM_FLAG_CCD_INTERLACED      = 0x00000004          # interlaced ccd sensor
NNCAM_FLAG_ROI_HARDWARE        = 0x00000008          # support hardware ROI
NNCAM_FLAG_MONO                = 0x00000010          # monochromatic
NNCAM_FLAG_BINSKIP_SUPPORTED   = 0x00000020          # support bin/skip mode
NNCAM_FLAG_USB30               = 0x00000040          # usb3.0
NNCAM_FLAG_TEC                 = 0x00000080          # Thermoelectric Cooler
NNCAM_FLAG_USB30_OVER_USB20    = 0x00000100          # usb3.0 camera connected to usb2.0 port
NNCAM_FLAG_ST4                 = 0x00000200          # ST4
NNCAM_FLAG_GETTEMPERATURE      = 0x00000400          # support to get the temperature of the sensor
NNCAM_FLAG_PUTTEMPERATURE      = 0x00000800          # support to put the target temperature of the sensor
NNCAM_FLAG_RAW10               = 0x00001000          # pixel format, RAW 10bits
NNCAM_FLAG_RAW12               = 0x00002000          # pixel format, RAW 12bits
NNCAM_FLAG_RAW14               = 0x00004000          # pixel format, RAW 14bits
NNCAM_FLAG_RAW16               = 0x00008000          # pixel format, RAW 16bits
NNCAM_FLAG_FAN                 = 0x00010000          # cooling fan
NNCAM_FLAG_TEC_ONOFF           = 0x00020000          # Thermoelectric Cooler can be turn on or off, support to set the target temperature of TEC
NNCAM_FLAG_ISP                 = 0x00040000          # ISP (Image Signal Processing) chip
NNCAM_FLAG_TRIGGER_SOFTWARE    = 0x00080000          # support software trigger
NNCAM_FLAG_TRIGGER_EXTERNAL    = 0x00100000          # support external trigger
NNCAM_FLAG_TRIGGER_SINGLE      = 0x00200000          # only support trigger single: one trigger, one image
NNCAM_FLAG_BLACKLEVEL          = 0x00400000          # support set and get the black level
NNCAM_FLAG_AUTO_FOCUS          = 0x00800000          # support auto focus
NNCAM_FLAG_BUFFER              = 0x01000000          # frame buffer
NNCAM_FLAG_DDR                 = 0x02000000          # use very large capacity DDR (Double Data Rate SDRAM) for frame buffer
NNCAM_FLAG_CG                  = 0x04000000          # support Conversion Gain mode: HCG, LCG
NNCAM_FLAG_YUV411              = 0x08000000          # pixel format, yuv411
NNCAM_FLAG_VUYY                = 0x10000000          # pixel format, yuv422, VUYY
NNCAM_FLAG_YUV444              = 0x20000000          # pixel format, yuv444
NNCAM_FLAG_RGB888              = 0x40000000          # pixel format, RGB888
NNCAM_FLAG_RAW8                = 0x80000000          # pixel format, RAW 8 bits
NNCAM_FLAG_GMCY8               = 0x0000000100000000  # pixel format, GMCY, 8 bits
NNCAM_FLAG_GMCY12              = 0x0000000200000000  # pixel format, GMCY, 12 bits
NNCAM_FLAG_UYVY                = 0x0000000400000000  # pixel format, yuv422, UYVY
NNCAM_FLAG_CGHDR               = 0x0000000800000000  # Conversion Gain: HCG, LCG, HDR
NNCAM_FLAG_GLOBALSHUTTER       = 0x0000001000000000  # global shutter
NNCAM_FLAG_FOCUSMOTOR          = 0x0000002000000000  # support focus motor

NNCAM_EVENT_EXPOSURE           = 0x0001              # exposure time changed
NNCAM_EVENT_TEMPTINT           = 0x0002              # white balance changed, Temp/Tint mode
NNCAM_EVENT_CHROME             = 0x0003              # reversed, do not use it
NNCAM_EVENT_IMAGE              = 0x0004              # live image arrived, use Nncam_PullImage to get this image
NNCAM_EVENT_STILLIMAGE         = 0x0005              # snap (still) frame arrived, use Nncam_PullStillImage to get this frame
NNCAM_EVENT_WBGAIN             = 0x0006              # white balance changed, RGB Gain mode
NNCAM_EVENT_TRIGGERFAIL        = 0x0007              # trigger failed
NNCAM_EVENT_BLACK              = 0x0008              # black balance changed
NNCAM_EVENT_FFC                = 0x0009              # flat field correction status changed
NNCAM_EVENT_DFC                = 0x000a              # dark field correction status changed
NNCAM_EVENT_ERROR              = 0x0080              # generic error
NNCAM_EVENT_DISCONNECTED       = 0x0081              # camera disconnected
NNCAM_EVENT_TIMEOUT            = 0x0082              # timeout error
NNCAM_EVENT_AFFEEDBACK         = 0x0083              # auto focus sensor board positon
NNCAM_EVENT_AFPOSITION         = 0x0084              # auto focus information feedback
NNCAM_EVENT_FACTORY            = 0x8001              # restore factory settings

NNCAM_OPTION_NOFRAME_TIMEOUT   = 0x01   # 1 = enable; 0 = disable. default: disable
NNCAM_OPTION_THREAD_PRIORITY   = 0x02   # set the priority of the internal thread which grab data from the usb device. iValue: 0 = THREAD_PRIORITY_NORMAL; 1 = THREAD_PRIORITY_ABOVE_NORMAL; 2 = THREAD_PRIORITY_HIGHEST; default: 0; see: msdn SetThreadPriority
NNCAM_OPTION_PROCESSMODE       = 0x03   # 0 = better image quality, more cpu usage. this is the default value
                                          # 1 = lower image quality, less cpu usage
NNCAM_OPTION_RAW               = 0x04   # raw data mode, read the sensor "raw" data. This can be set only BEFORE Nncam_StartXXX(). 0 = rgb, 1 = raw, default value: 0
NNCAM_OPTION_HISTOGRAM         = 0x05   # 0 = only one, 1 = continue mode
NNCAM_OPTION_BITDEPTH          = 0x06   # 0 = 8 bits mode, 1 = 16 bits mode
NNCAM_OPTION_FAN               = 0x07   # 0 = turn off the cooling fan, [1, max] = fan speed
NNCAM_OPTION_TEC               = 0x08   # 0 = turn off the thermoelectric cooler, 1 = turn on the thermoelectric cooler
NNCAM_OPTION_LINEAR            = 0x09   # 0 = turn off the builtin linear tone mapping, 1 = turn on the builtin linear tone mapping, default value: 1
NNCAM_OPTION_CURVE             = 0x0a   # 0 = turn off the builtin curve tone mapping, 1 = turn on the builtin polynomial curve tone mapping, 2 = logarithmic curve tone mapping, default value: 2
NNCAM_OPTION_TRIGGER           = 0x0b   # 0 = video mode, 1 = software or simulated trigger mode, 2 = external trigger mode, default value = 0
NNCAM_OPTION_RGB               = 0x0c   # 0 => RGB24; 1 => enable RGB48 format when bitdepth > 8; 2 => RGB32; 3 => 8 Bits Gray (only for mono camera); 4 => 16 Bits Gray (only for mono camera when bitdepth > 8)
NNCAM_OPTION_COLORMATIX        = 0x0d   # enable or disable the builtin color matrix, default value: 1
NNCAM_OPTION_WBGAIN            = 0x0e   # enable or disable the builtin white balance gain, default value: 1
NNCAM_OPTION_TECTARGET         = 0x0f   # get or set the target temperature of the thermoelectric cooler, in 0.1 degree Celsius. For example, 125 means 12.5 degree Celsius, -35 means -3.5 degree Celsius
NNCAM_OPTION_AUTOEXP_POLICY    = 0x10   # auto exposure policy:
                                          #      0: Exposure Only
                                          #      1: Exposure Preferred
                                          #      2: Analog Gain Only
                                          #      3: Analog Gain Preferred
                                          #      default value: 1
NNCAM_OPTION_FRAMERATE         = 0x11   # limit the frame rate, range=[0, 63], the default value 0 means no limit
NNCAM_OPTION_DEMOSAIC          = 0x12   # demosaic method for both video and still image: BILINEAR = 0, VNG(Variable Number of Gradients interpolation) = 1, PPG(Patterned Pixel Grouping interpolation) = 2, AHD(Adaptive Homogeneity-Directed interpolation) = 3, see https://en.wikipedia.org/wiki/Demosaicing, default value: 0
NNCAM_OPTION_DEMOSAIC_VIDEO    = 0x13   # demosaic method for video
NNCAM_OPTION_DEMOSAIC_STILL    = 0x14   # demosaic method for still image
NNCAM_OPTION_BLACKLEVEL        = 0x15   # black level
NNCAM_OPTION_MULTITHREAD       = 0x16   # multithread image processing
NNCAM_OPTION_BINNING           = 0x17   # binning, 0x01 (no binning), 0x02 (add, 2*2), 0x03 (add, 3*3), 0x04 (add, 4*4), 0x82 (average, 2*2), 0x83 (average, 3*3), 0x84 (average, 4*4)
NNCAM_OPTION_ROTATE            = 0x18   # rotate clockwise: 0, 90, 180, 270
NNCAM_OPTION_CG                = 0x19   # Conversion Gain mode: 0 = LCG, 1 = HCG, 2 = HDR
NNCAM_OPTION_PIXEL_FORMAT      = 0x1a   # pixel format
NNCAM_OPTION_FFC               = 0x1b   # flat field correction
                                          #      set:
                                          #          0: disable
                                          #          1: enable
                                          #          -1: reset
                                          #          (0xff000000 | n): set the average number to n, [1~255]
                                          #      get:
                                          #          (val & 0xff): 0 -> disable, 1 -> enable, 2 -> inited
                                          #          ((val & 0xff00) >> 8): sequence
                                          #          ((val & 0xff0000) >> 8): average number
NNCAM_OPTION_DDR_DEPTH         = 0x1c   # the number of the frames that DDR can cache
                                          #     1: DDR cache only one frame
                                          #     0: Auto:
                                          #         ->one for video mode when auto exposure is enabled
                                          #         ->full capacity for others
                                          #     1: DDR can cache frames to full capacity
NNCAM_OPTION_DFC               = 0x1d   # dark field correction
                                          #     set:
                                          #         0: disable
                                          #         1: enable
                                          #         -1: reset
                                          #         (0xff000000 | n): set the average number to n, [1~255]
                                          #     get:
                                          #         (val & 0xff): 0 -> disable, 1 -> enable, 2 -> inited
                                          #         ((val & 0xff00) >> 8): sequence
                                          #         ((val & 0xff0000) >> 8): average number
NNCAM_OPTION_SHARPENING        = 0x1e   # Sharpening: (threshold << 24) | (radius << 16) | strength)
                                          #     strength: [0, 500], default: 0 (disable)
                                          #     radius: [1, 10]
                                          #     threshold: [0, 255]
NNCAM_OPTION_FACTORY           = 0x1f   # restore the factory settings
NNCAM_OPTION_TEC_VOLTAGE       = 0x20   # get the current TEC voltage in 0.1V, 59 mean 5.9V; readonly
NNCAM_OPTION_TEC_VOLTAGE_MAX   = 0x21   # get the TEC maximum voltage in 0.1V; readonly
NNCAM_OPTION_DEVICE_RESET      = 0x22   # reset usb device, simulate a replug
NNCAM_OPTION_UPSIDE_DOWN       = 0x23   # upsize down:
                                          #     1: yes
                                          #     0: no
                                          #     default: 1 (win), 0 (linux/macos)
NNCAM_OPTION_AFPOSITION        = 0x24   # auto focus sensor board positon
NNCAM_OPTION_AFMODE            = 0x25   # auto focus mode (0:manul focus; 1:auto focus; 2:onepush focus; 3:conjugate calibration)
NNCAM_OPTION_AFZONE            = 0x26   # auto focus zone
NNCAM_OPTION_AFFEEDBACK        = 0x27   # auto focus information feedback; 0:unknown; 1:focused; 2:focusing; 3:defocus; 4:up; 5:down
NNCAM_OPTION_TESTPATTERN       = 0x28   # test pattern:
                                          #     0: TestPattern Off
                                          #     3: monochrome diagonal stripes
                                          #     5: monochrome vertical stripes
                                          #     7: monochrome horizontal stripes
                                          #     9: chromatic diagonal stripes
NNCAM_OPTION_AUTOEXP_THRESHOLD = 0x29   # threshold of auto exposure, default value: 5, range = [5, 15]

NNCAM_PIXELFORMAT_RAW8         = 0x00
NNCAM_PIXELFORMAT_RAW10        = 0x01
NNCAM_PIXELFORMAT_RAW12        = 0x02
NNCAM_PIXELFORMAT_RAW14        = 0x03
NNCAM_PIXELFORMAT_RAW16        = 0x04
NNCAM_PIXELFORMAT_YUV411       = 0x05
NNCAM_PIXELFORMAT_VUYY         = 0x06
NNCAM_PIXELFORMAT_YUV444       = 0x07
NNCAM_PIXELFORMAT_RGB888       = 0x08
NNCAM_PIXELFORMAT_GMCY8        = 0x09
NNCAM_PIXELFORMAT_GMCY12       = 0x0a
NNCAM_PIXELFORMAT_UYVY         = 0x0b

NNCAM_FRAMEINFO_FLAG_SEQ       = 0x01     # sequence number
NNCAM_FRAMEINFO_FLAG_TIMESTAMP = 0x02

NNCAM_IOCONTROLTYPE_GET_SUPPORTEDMODE         = 0x01  # 0x01->Input, 0x02->Output, (0x01 | 0x02)->support both Input and Output
NNCAM_IOCONTROLTYPE_GET_GPIODIR               = 0x03  # 0x01->Input, 0x02->Output
NNCAM_IOCONTROLTYPE_SET_GPIODIR               = 0x04
NNCAM_IOCONTROLTYPE_GET_FORMAT                = 0x05  # 0x00-> not connected
                                                        # 0x01-> Tri-state: Tri-state mode (Not driven)
                                                        # 0x02-> TTL: TTL level signals
                                                        # 0x03-> LVDS: LVDS level signals
                                                        # 0x04-> RS422: RS422 level signals
                                                        # 0x05-> Opto-coupled
NNCAM_IOCONTROLTYPE_SET_FORMAT                = 0x06
NNCAM_IOCONTROLTYPE_GET_OUTPUTINVERTER        = 0x07  # boolean, only support output signal
NNCAM_IOCONTROLTYPE_SET_OUTPUTINVERTER        = 0x08
NNCAM_IOCONTROLTYPE_GET_INPUTACTIVATION       = 0x09  # 0x01->Positive, 0x02->Negative
NNCAM_IOCONTROLTYPE_SET_INPUTACTIVATION       = 0x0a
NNCAM_IOCONTROLTYPE_GET_DEBOUNCERTIME         = 0x0b  # debouncer time in microseconds, [0, 20000]
NNCAM_IOCONTROLTYPE_SET_DEBOUNCERTIME         = 0x0c
NNCAM_IOCONTROLTYPE_GET_TRIGGERSOURCE         = 0x0d  # 0x00-> Opto-isolated input
                                                        # 0x01-> GPIO0
                                                        # 0x02-> GPIO1
                                                        # 0x03-> Counter
                                                        # 0x04-> PWM
                                                        # 0x05-> Software
NNCAM_IOCONTROLTYPE_SET_TRIGGERSOURCE         = 0x0e
NNCAM_IOCONTROLTYPE_GET_TRIGGERDELAY          = 0x0f  # Trigger delay time in microseconds, [0, 5000000]
NNCAM_IOCONTROLTYPE_SET_TRIGGERDELAY          = 0x10
NNCAM_IOCONTROLTYPE_GET_BURSTCOUNTER          = 0x11  # Burst Counter: 1, 2, 3 ... 1023
NNCAM_IOCONTROLTYPE_SET_BURSTCOUNTER          = 0x12
NNCAM_IOCONTROLTYPE_GET_COUNTERSOURCE         = 0x13  # 0x00-> Opto-isolated input, 0x01-> GPIO0, 0x02-> GPIO1
NNCAM_IOCONTROLTYPE_SET_COUNTERSOURCE         = 0x14
NNCAM_IOCONTROLTYPE_GET_COUNTERVALUE          = 0x15  # Counter Value: 1, 2, 3 ... 1023
NNCAM_IOCONTROLTYPE_SET_COUNTERVALUE          = 0x16
NNCAM_IOCONTROLTYPE_SET_RESETCOUNTER          = 0x18
NNCAM_IOCONTROLTYPE_GET_PWM_FREQ              = 0x19
NNCAM_IOCONTROLTYPE_SET_PWM_FREQ              = 0x1a
NNCAM_IOCONTROLTYPE_GET_PWM_DUTYRATIO         = 0x1b
NNCAM_IOCONTROLTYPE_SET_PWM_DUTYRATIO         = 0x1c
NNCAM_IOCONTROLTYPE_GET_PWMSOURCE             = 0x1d  # 0x00-> Opto-isolated input, 0x01-> GPIO0, 0x02-> GPIO1
NNCAM_IOCONTROLTYPE_SET_PWMSOURCE             = 0x1e
NNCAM_IOCONTROLTYPE_GET_OUTPUTMODE            = 0x1f  # 0x00-> Frame Trigger Wait
                                                        # 0x01-> Exposure Active
                                                        # 0x02-> Strobe
                                                        # 0x03-> User output
NNCAM_IOCONTROLTYPE_SET_OUTPUTMODE            = 0x20
NNCAM_IOCONTROLTYPE_GET_STROBEDELAYMODE       = 0x21  # boolean, 1 -> delay, 0 -> pre-delay; compared to exposure active signal
NNCAM_IOCONTROLTYPE_SET_STROBEDELAYMODE       = 0x22
NNCAM_IOCONTROLTYPE_GET_STROBEDELAYTIME       = 0x23  # Strobe delay or pre-delay time in microseconds, [0, 5000000]
NNCAM_IOCONTROLTYPE_SET_STROBEDELAYTIME       = 0x24
NNCAM_IOCONTROLTYPE_GET_STROBEDURATION        = 0x25  # Strobe duration time in microseconds, [0, 5000000]
NNCAM_IOCONTROLTYPE_SET_STROBEDURATION        = 0x26
NNCAM_IOCONTROLTYPE_GET_USERVALUE             = 0x27  # bit0-> Opto-isolated output
                                                        # bit1-> GPIO0 output
                                                        # bit2-> GPIO1 output
NNCAM_IOCONTROLTYPE_SET_USERVALUE             = 0x28
        
class NnCamResolution:
    def __init__(self, w, h):
        self.width = w
        self.height = h

class NnCamAfParam:
    def __init__(self, imax, imin, idef, imaxabs, iminabs, zoneh, zonev):
        self.imax = imax         # maximum auto focus sensor board positon
        self.imin = imin         # minimum auto focus sensor board positon
        self.idef = idef         # conjugate calibration positon
        self.imaxabs = imaxabs   # maximum absolute auto focus sensor board positon, micrometer
        self.iminabs = iminabs   # maximum absolute auto focus sensor board positon, micrometer
        self.zoneh = zoneh       # zone horizontal
        self.zonev = zonev       # zone vertical

class NnCamFrameInfoV2:
    def __init__(self, width, height, flag, seq, timestamp):
        self.width = width
        self.height = height
        self.flag = flag                 # NNCAM_FRAMEINFO_FLAG_xxxx
        self.seq = seq                   # sequence number
        self.timestamp = timestamp       # microsecond

class NnCamModelV2:                    # camera model v2
    def __init__(self, name, flag, maxspeed, preview, still, maxfanspeed, ioctrol, xpixsz, ypixsz, res):
        self.name = name                 # model name, in Windows, we use unicode
        self.flag = flag                 # NNCAM_FLAG_xxx, 64 bits
        self.maxspeed = maxspeed         # number of speed level, same as Nncam_get_MaxSpeed(), the speed range = [0, maxspeed], closed interval
        self.preview = preview           # number of preview resolution, same as Nncam_get_ResolutionNumber()
        self.still = still               # number of still resolution, same as Nncam_get_StillResolutionNumber()
        self.maxfanspeed = maxfanspeed   # maximum fan speed
        self.ioctrol = ioctrol           # number of input/output control
        self.xpixsz = xpixsz             # physical pixel size
        self.ypixsz = ypixsz             # physical pixel size
        self.res = res                   # NnCamResolution

class NnCamInstV2:
    def __init__(self, displayname, id, model):
        self.displayname = displayname   # display name
        self.id = id                     # unique and opaque id of a connected camera, for Nncam_Open
        self.model = model               # NnCamModelV2

if sys.platform == 'win32':
    class HRESULTException(OSError):
        def __init__(self, hr):
            OSError.__init__(self, None, ctypes.FormatError(hr).strip(), None, hr)
else:
    class HRESULTException(Exception):
        def __init__(self, hr):
            self.hr = hr

class _Resolution(ctypes.Structure):
    _fields_ = [('width', ctypes.c_uint),
                ('height', ctypes.c_uint)]

if sys.platform == 'win32':
    class _ModelV2(ctypes.Structure):               # camera model v2 win32
        _fields_ = [('name', ctypes.c_wchar_p),     # model name, in Windows, we use unicode
                    ('flag', ctypes.c_ulonglong),   # NNCAM_FLAG_xxx, 64 bits
                    ('maxspeed', ctypes.c_uint),    # number of speed level, same as Nncam_get_MaxSpeed(), the speed range = [0, maxspeed], closed interval
                    ('preview', ctypes.c_uint),     # number of preview resolution, same as Nncam_get_ResolutionNumber()
                    ('still', ctypes.c_uint),       # number of still resolution, same as Nncam_get_StillResolutionNumber()
                    ('maxfanspeed', ctypes.c_uint), # maximum fan speed
                    ('ioctrol', ctypes.c_uint),     # number of input/output control
                    ('xpixsz', ctypes.c_float),     # physical pixel size
                    ('ypixsz', ctypes.c_float),     # physical pixel size
                    ('res', _Resolution * NNCAM_MAX)]
    class _InstV2(ctypes.Structure):                       # win32
        _fields_ = [('displayname', ctypes.c_wchar * 64),  # display name
                    ('id', ctypes.c_wchar * 64),           # unique and opaque id of a connected camera, for Nncam_Open
                    ('model', ctypes.POINTER(_ModelV2))]
else:
    class _ModelV2(ctypes.Structure):               # camera model v2 linux/mac
        _fields_ = [('name', ctypes.c_char_p),      # model name, in Windows, we use unicode
                    ('flag', ctypes.c_ulonglong),   # NNCAM_FLAG_xxx, 64 bits
                    ('maxspeed', ctypes.c_uint),    # number of speed level, same as Nncam_get_MaxSpeed(), the speed range = [0, maxspeed], closed interval
                    ('preview', ctypes.c_uint),     # number of preview resolution, same as Nncam_get_ResolutionNumber()
                    ('still', ctypes.c_uint),       # number of still resolution, same as Nncam_get_StillResolutionNumber()
                    ('maxfanspeed', ctypes.c_uint), # maximum fan speed
                    ('ioctrol', ctypes.c_uint),     # number of input/output control
                    ('xpixsz', ctypes.c_float),     # physical pixel size
                    ('ypixsz', ctypes.c_float),     # physical pixel size
                    ('res', _Resolution * NNCAM_MAX)]
    class _InstV2(ctypes.Structure):                       # linux/mac
        _fields_ = [('displayname', ctypes.c_char * 64),   # display name
                    ('id', ctypes.c_char * 64),            # unique and opaque id of a connected camera, for Nncam_Open
                    ('model', ctypes.POINTER(_ModelV2))]

class NnCam:
    class __RECT(ctypes.Structure):
        _fields_ = [('left', ctypes.c_int),
                    ('top', ctypes.c_int),
                    ('right', ctypes.c_int),
                    ('bottom', ctypes.c_int)]

    class __AfParam(ctypes.Structure):
        _fields_ = [('imax', ctypes.c_int),         # maximum auto focus sensor board positon
                    ('imin', ctypes.c_int),         # minimum auto focus sensor board positon
                    ('idef', ctypes.c_int),         # conjugate calibration positon
                    ('imaxabs', ctypes.c_int),      # maximum absolute auto focus sensor board positon, micrometer
                    ('iminabs', ctypes.c_int),      # maximum absolute auto focus sensor board positon, micrometer
                    ('zoneh', ctypes.c_int),        # zone horizontal
                    ('zonev', ctypes.c_int)]        # zone vertical

    class __FrameInfoV2(ctypes.Structure):
        _fields_ = [('width', ctypes.c_uint),
                    ('height', ctypes.c_uint),
                    ('flag', ctypes.c_uint),            # NNCAM_FRAMEINFO_FLAG_xxxx
                    ('seq', ctypes.c_uint),             # sequence number
                    ('timestamp', ctypes.c_longlong)]   # microsecond

    if sys.platform == 'win32':
        __EVENTCALLBACKFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_uint, ctypes.py_object)
    else:
        __EVENTCALLBACKFUNC = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.py_object)
        __HOTPLUGCALLBACKFUNC = ctypes.CFUNCTYPE(ctypes.c_void_p)
        __hotplug = None

    __lib = None

    @staticmethod
    def __errcheck(result, func, args):
        if result < 0:
            raise HRESULTException(result)
        return args

    @staticmethod
    def __convertStr(x):
        if isinstance(x, str):
            return x
        else:
            return x.decode('ascii')
            
# get the version of this dll, which is: 37.14643.2019.0511
    @classmethod
    def Version(cls):
        cls.__initlib()
        return cls.__lib.Nncam_Version()

    @staticmethod
    def __convertResolution(a):
        t = []
        for i in range(0, a.preview):
            t.append(NnCamResolution(a.res[i].width, a.res[i].height))
        return t

    @staticmethod
    def __convertModel(a):
        t = NnCamModelV2(__class__.__convertStr(a.name), a.flag, a.maxspeed, a.preview, a.still, a.maxfanspeed, a.ioctrol, a.xpixsz, a.ypixsz, __class__.__convertResolution(a))
        return t

    @staticmethod
    def __convertInst(a):
        return NnCamInstV2(__class__.__convertStr(a.displayname), __class__.__convertStr(a.id), __class__.__convertModel(a.model.contents))

    @staticmethod
    def __hotplugCallbackFunc(ctx):
        if __hotplug:
            __class__.__hotplug()

    @classmethod
    def HotPlug(cls, func):
        if sys.platform == 'win32':             # only available on macOS and Linux, it's unnecessary on Windows
            raise HRESULTException(0x80004001)
        else:
            cls.__initlib()
            cls.__hotplug = func
            if cls.__hotplug is None:
                cls.__lib.Nncam_HotPlug(None, None)
            else:
                cls.__lib.Nncam_HotPlug(cls.__HOTPLUGCALLBACKFUNC(cls.__hotplugCallbackFunc), None)

    @classmethod
    def EnumV2(cls):
        cls.__initlib()
        a = (_InstV2 * NNCAM_MAX)()
        n = cls.__lib.Nncam_EnumV2(a)
        arr = []
        for i in range(0, n):
            arr.append(__class__.__convertInst(a[i]))
        return arr

    def __init__(self, h):
        self.__h = h
        self.__func = None
        self.__ctx = None
        self.__cb = None

    def __del__(self):
        self.Close()

    def __nonzero__(self):
        return self.__h is not None

# the object of NnCam must be obtained by classmethod method Open or OpenByIndex, it cannot be obtained by obj = nncam.NnCam()
# Open(None) means try to Open the first camera
    @classmethod
    def Open(cls, id):
        cls.__initlib()
        if id is None:
            h = cls.__lib.Nncam_Open(None)
        elif sys.platform == 'win32':
            h = cls.__lib.Nncam_Open(id)
        else:
            h = cls.__lib.Nncam_Open(id.encode('ascii'))
        if h is None:
            return None
        return __class__(h)

# the object of NnCam must be obtained by classmethod method Open or OpenByIndex, it cannot be obtained by obj = nncam.NnCam()
#
# the same with Nncam_Open, but use the index as the parameter. such as:
#   index == 0, open the first camera,
#   index == 1, open the second camera,
#   etc
    @classmethod
    def OpenByIndex(cls, index):
        cls.__initlib()
        h = cls.__lib.Nncam_OpenByIndex(index)
        if h is None:
            return None
        return __class__(h)

    def Close(self):
        if self.__h:
            self.__lib.Nncam_Close(self.__h)
            self.__h = None

    @staticmethod
    def __eventCallbackFunc(nEvent, ctx):
        if ctx:
            ctx.__callbackFunc(nEvent)

    def __callbackFunc(self, nEvent):
        if self.__func:
            self.__func(nEvent, self.__ctx)

    def StartPullModeWithCallback(self, func, ctx):
        self.__func = func
        self.__ctx = ctx
        self.__cb = __class__.__EVENTCALLBACKFUNC(__class__.__eventCallbackFunc)
        self.__lib.Nncam_StartPullModeWithCallback(self.__h, self.__cb, ctypes.py_object(self))

    @staticmethod
    def __convertFrameInfo(pInfo, x):
        pInfo.width = x.width
        pInfo.height = x.height
        pInfo.flag = x.flag
        pInfo.seq = x.seq
        pInfo.timestamp = x.timestamp

    def PullImageV2(self, pImageData, bits, pInfo):
        if pInfo is None:
            self.__lib.Nncam_PullImageV2(self.__h, pImageData, bits, None)
        else:
            x = __FrameInfoV2()
            self.__lib.Nncam_PullImageV2(self.__h, pImageData, bits, byref(x))
            self.__convertFrameInfo(pInfo, x)

    def PullStillImageV2(self, pImageData, bits, pInfo):
        if pInfo is None:
            self.__lib.Nncam_PullStillImageV2(self.__h, pImageData, bits, None)
        else:
            x = __FrameInfoV2()
            self.__lib.Nncam_PullStillImageV2(self.__h, pImageData, bits, byref(x))
            self.__convertFrameInfo(pInfo, x)

#  bits: 24 (RGB24), 32 (RGB32), 8 (Gray) or 16 (Gray)
#  rowPitch: The distance from one row to the next row. rowPitch = 0 means using the default row pitch
            
    def PullImageWithRowPitchV2(self, pImageData, bits, rowPitch, pInfo):
        if pInfo is None:
            self.__lib.Nncam_PullImageWithRowPitchV2(self.__h, pImageData, bits, rowPitch, None)
        else:
            x = __FrameInfoV2()
            self.__lib.Nncam_PullImageWithRowPitchV2(self.__h, pImageData, bits, rowPitch, byref(x))
            self.__convertFrameInfo(pInfo, x)

    def PullStillImageWithRowPitchV2(self, pImageData, bits, rowPitch, pInfo):
        if pInfo is None:
            self.__lib.Nncam_PullStillImageWithRowPitchV2(self.__h, pImageData, bits, rowPitch, None)
        else:
            x = __FrameInfoV2()
            self.__lib.Nncam_PullStillImageWithRowPitchV2(self.__h, pImageData, bits, rowPitch, pInfo)
            self.__convertFrameInfo(pInfo, x)

    def ResolutionNumber(self):
        return self.__lib.Nncam_get_ResolutionNumber(self.__h)

# width, height
    def StillResolutionNumber(self):
        return self.__lib.Nncam_get_StillResolutionNumber(self.__h)

    def MonoMode(self):
        return (self.__lib.Nncam_get_MonoMode(self.__h) == 0)

# get the maximum speed, "Frame Speed Level"
    def MaxSpeed(self):
        return self.__lib.Nncam_get_MaxSpeed(self.__h)

# get the max bit depth of this camera, such as 8, 10, 12, 14, 16
    def MaxBitDepth(self):
        return self.__lib.Nncam_get_MaxBitDepth(self.__h)

# get the maximum fan speed, the fan speed range = [0, max], closed interval
    def FanMaxSpeed(self):
        return self.__lib.Nncam_get_FanMaxSpeed(self.__h)

# get the revision
    def Revision(self):
        x = ctypes.c_ushort(0)
        self.__lib.Nncam_get_Revision(self.__h, ctypes.byref(x))
        return x.value

# get the serial number which is always 32 chars which is zero-terminated such as "TP110826145730ABCD1234FEDC56787"
    def SerialNumber(self):
        str = (ctypes.c_char * 32)()
        self.__lib.Nncam_get_SerialNumber(self.__h, str)
        return str.value.decode('ascii')

# get the camera firmware version, such as: 3.2.1.20140922
    def FwVersion(self):
        str = (ctypes.c_char * 16)()
        self.__lib.Nncam_get_FwVersion(self.__h, str)
        return str.value.decode('ascii')

# get the camera hardware version, such as: 3.2.1.20140922
    def HwVersion(self):
        str = (ctypes.c_char * 16)()
        self.__lib.Nncam_get_HwVersion(self.__h, str)
        return str.value.decode('ascii')

# such as: 20150327
    def ProductionDate(self):
        str = (ctypes.c_char * 16)()
        self.__lib.Nncam_get_ProductionDate(self.__h, str)
        return str.value.decode('ascii')

    def FpgaVersion(self):
        str = (ctypes.c_char * 16)()
        self.__lib.Nncam_get_FpgaVersion(self.__h, str)
        return str.value.decode('ascii')

# get the maximum speed, "Frame Speed Level"
    def Field(self):
        return self.__lib.Nncam_get_Field(self.__h)

    def Stop(self):
        self.__lib.Nncam_Stop(self.__h)

    def Pause(self, bPause):
        self.__lib.Nncam_Pause(self.__h, ctypes.c_int(1 if bPause else 0))

# still image snap
    def Snap(self, nResolutionIndex):
        self.__lib.Nncam_Snap(self.__h, ctypes.c_uint(nResolutionIndex))

# multiple still image snap
    def SnapN(self, nResolutionIndex, nNumber):
        self.__lib.Nncam_SnapN(self.__h, ctypes.c_uint(nResolutionIndex), ctypes.c_uint(nNumber))

# soft trigger:
#    nNumber:    0xffff:     trigger continuously
#                0:          cancel trigger
#                others:     number of images to be triggered
    def Trigger(self, nNumber):
        self.__lib.Nncam_Trigger(self.__h, ctypes.c_ushort(nNumber))

    def put_Size(self, nWidth, nHeight):
        self.__lib.Nncam_put_Size(self.__h, ctypes.c_int(nWidth), ctypes.c_int(nHeight))

# width, height
    def get_Size(self):
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        self.__lib.Nncam_get_Size(self.__h, ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# put_Size, put_eSize, can be used to set the video output resolution BEFORE Start.
# put_Size use width and height parameters, put_eSize use the index parameter.
# for example, UCMOS03100KPA support the following resolutions:
#     index 0:    2048,   1536
#     index 1:    1024,   768
#     index 2:    680,    510
# so, we can use put_Size(h, 1024, 768) or put_eSize(h, 1). Both have the same effect.
    def put_eSize(self, nResolutionIndex):
        self.__lib.Nncam_put_eSize(self.__h, ctypes.c_uint(nResolutionIndex))

    def get_eSize(self):
        x = ctypes.c_uint(0)
        self.__lib.Nncam_get_eSize(self.__h, ctypes.byref(x))
        return x.value

# width, height
    def get_Resolution(self, nResolutionIndex):
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        self.__lib.Nncam_get_Resolution(self.__h, ctypes.c_uint(nResolutionIndex), ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# get the sensor pixel size, such as: 2.4um
    def get_PixelSize(self, nResolutionIndex):
        x = ctypes.c_float(0)
        y = ctypes.c_float(0)
        self.__lib.Nncam_get_PixelSize(self.__h, ctypes.c_uint(nResolutionIndex), ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# numerator/denominator, such as: 1/1, 1/2, 1/3
    def get_ResolutionRatio(self, nResolutionIndex):
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        self.__lib.Nncam_get_ResolutionRatio(self.__h, ctypes.c_uint(nResolutionIndex), ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# FourCC:
#   MAKEFOURCC('G', 'B', 'R', 'G')
#   MAKEFOURCC('R', 'G', 'G', 'B')
#   MAKEFOURCC('B', 'G', 'G', 'R')
#   MAKEFOURCC('G', 'R', 'B', 'G')
#   MAKEFOURCC('Y', 'U', 'Y', 'V')
#   MAKEFOURCC('Y', 'Y', 'Y', 'Y')
# FourCC, bitsperpixel
    def get_RawFormat(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_uint(0)
        self.__lib.Nncam_get_RawFormat(self.__h, ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

    def put_RealTime(self, bEnable):
        self.__lib.Nncam_put_RealTime(self.__h, ctypes.c_int(1 if bEnable else 0))

    def get_RealTime(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_RealTime(self.__h, b)
        return (b.value != 0)

    def Flush():
        self.__lib.Nncam_Flush(self.__h)

    def get_AutoExpoEnable(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_AutoExpoEnable(self.__h, b)
        return (b.value != 0)

    def put_AutoExpoEnable(self, bAutoExposure):
        x = ctypes.c_int(1 if bAutoExposure else 0)
        self.__lib.Nncam_put_AutoExpoEnable(self.__h, x)

    def get_AutoExpoTarget(self):
        x = ctypes.c_ushort(0)
        self.__lib.Nncam_get_AutoExpoTarget(self.__h, ctypes.byref(x))
        return x.value

    def put_AutoExpoTarget(self, Target):
        self.__lib.Nncam_put_AutoExpoTarget(self.__h, ctypes.c_int(Target))

    def put_MaxAutoExpoTimeAGain(self, maxTime, maxAGain):
        return self.__lib.Nncam_put_MaxAutoExpoTimeAGain(self.__h, ctypes.c_uint(maxTime), ctypes.c_ushort(maxAGain))

    def get_MaxAutoExpoTimeAGain(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_ushort(0)
        self.__lib.Nncam_get_MaxAutoExpoTimeAGain(self.__h, ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

    def put_MinAutoExpoTimeAGain(self, minTime, minAGain):
        self.__lib.Nncam_put_MinAutoExpoTimeAGain(self.__h, ctypes.c_uint(minTime), ctypes.c_ushort(minAGain))

    def get_MinAutoExpoTimeAGain(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_ushort(0)
        self.__lib.Nncam_get_MinAutoExpoTimeAGain(self.__h, ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# in microseconds
    def get_ExpoTime(self):
        x = ctypes.c_uint(0)
        self.__lib.Nncam_get_ExpoTime(self.__h, ctypes.byref(x))
        return x.value

    def put_ExpoTime(self, Time):
        self.__lib.Nncam_put_ExpoTime(self.__h, ctypes.c_uint(Time))

# min, max, default
    def get_ExpTimeRange(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_uint(0)
        z = ctypes.c_uint(0)
        self.__lib.Nncam_get_ExpTimeRange(self.__h, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        return (x.value, y.value, z.value)

# percent, such as 300
    def get_ExpoAGain(self):
        x = ctypes.c_ushort(0)
        self.__lib.Nncam_get_ExpoAGain(self.__h, ctypes.byref(x))
        return x.value

    def put_ExpoAGain(self, AGain):
        self.__lib.Nncam_put_ExpoAGain(self.__h, ctypes.c_ushort(AGain))

# min, max, default
    def get_ExpoAGainRange(self):
        x = ctypes.c_ushort(0)
        y = ctypes.c_ushort(0)
        z = ctypes.c_ushort(0)
        self.__lib.Nncam_get_ExpoAGainRange(self.__h, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        return (x.value, y.value, z.value)

    def put_LevelRange(self, aLow, aHigh):
        if len(aLow) == 4 and len(aHigh) == 4:
            x = (ctypes.c_ushort * 4)(aLow[0], aLow[1], aLow[2], aLow[3])
            y = (ctypes.c_ushort * 4)(aHigh[0], aHigh[1], aHigh[2], aHigh[3])
            self.__lib.Nncam_put_LevelRange(self.__h, x, y)
        else:
            raise HRESULTException(0x80070057)

    def get_LevelRange(self):
        x = (ctypes.c_ushort * 4)()
        y = (ctypes.c_ushort * 4)()
        self.__lib.Nncam_get_LevelRange(self.__h, x, y)
        aLow = (x[0], x[1], x[2], x[3])
        aHigh = (y[0], y[1], y[2], y[3])
        return (aLow, aHigh)

#   ------------------------------------------------------------------|
#   | Parameter               |   Range       |   Default             |
#   |-----------------------------------------------------------------|
#   | Auto Exposure Target    |   16~235      |   120                 |
#   | Temp                    |   2000~15000  |   6503                |
#   | Tint                    |   200~2500    |   1000                |
#   | LevelRange              |   0~255       |   Low = 0, High = 255 |
#   | Contrast                |   -100~100    |   0                   |
#   | Hue                     |   -180~180    |   0                   |
#   | Saturation              |   0~255       |   128                 |
#   | Brightness              |   -64~64      |   0                   |
#   | Gamma                   |   20~180      |   100                 |
#   | WBGain                  |   -127~127    |   0                   |
#   ------------------------------------------------------------------|
        
    def put_Hue(self, Hue):
        self.__lib.Nncam_put_Hue(self.__h, ctypes.c_int(Hue))

    def get_Hue(self):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Hue(self.__h, ctypes.byref(x))
        return x.value

    def put_Saturation(self, Saturation):
        self.__lib.Nncam_put_Saturation(self.__h, ctypes.c_int(Saturation))

    def get_Saturation(self):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Saturation(self.__h, ctypes.byref(x))
        return x.value

    def put_Brightness(self, Brightness):
        self.__lib.Nncam_put_Brightness(self.__h, ctypes.c_int(Brightness))

    def get_Brightness(self):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Brightness(self.__h, ctypes.byref(x))
        return x.value

    def get_Contrast(self):        
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Contrast(self.__h, ctypes.byref(x))
        return x.value

    def put_Contrast(self, Contrast):
        self.__lib.Nncam_put_Contrast(self.__h, ctypes.c_int(Contrast))

    def get_Gamma(self):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Gamma(self.__h, ctypes.byref(x))
        return x.value

    def put_Gamma(self, Gamma):
        self.__lib.Nncam_put_Gamma(self.__h, ctypes.c_int(Gamma))

# monochromatic mode
    def get_Chrome(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_Chrome(self.__h, ctypes.byref(b)) < 0
        return (b.value != 0)

    def put_Chrome(self, bChrome):
        self.__lib.Nncam_put_Chrome(self.__h, ctypes.c_int(1 if bChrome else 0))

# vertical flip
    def get_VFlip(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_VFlip(self.__h, ctypes.byref(b))
        return (b.value != 0)

# vertical flip
    def put_VFlip(self, bVFlip):
        self.__lib.Nncam_put_VFlip(self.__h, ctypes.c_int(1 if bVFlip else 0))

# horizontal flip
    def get_HFlip(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_HFlip(self.__h, ctypes.byref(b))
        return (b.value != 0)

# horizontal flip
    def put_HFlip(self, bHFlip):
        self.__lib.Nncam_put_HFlip(self.__h, ctypes.c_int(1 if bHFlip else 0))

# negative film
    def get_Negative(self):  
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_Negative(self.__h, ctypes.byref(b))
        return (b.value != 0)

# negative film
    def put_Negative(self, bNegative):
        self.__lib.Nncam_put_Negative(self.__h, ctypes.c_int(1 if bNegative else 0))

    def put_Speed(self, nSpeed):
        self.__lib.Nncam_put_Speed(self.__h, ctypes.c_ushort(nSpeed))

    def get_Speed(self):
        x = ctypes.c_ushort(0)
        self.__lib.Nncam_get_Speed(self.__h, ctypes.byref(x))
        return x.value

# power supply: 
#     0 -> 60HZ AC
#     1 -> 50Hz AC
#     2 -> DC
    def put_HZ(self, nHZ):
        self.__lib.Nncam_put_HZ(self.__h, ctypes.c_int(nHZ))

    def get_HZ(self):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_HZ(self.__h, ctypes.byref(x))
        return x.value

# skip or bin
    def put_Mode(self, bSkip):
        self.__lib.Nncam_put_Mode(self.__h, ctypes.c_int(1 if bSkip else 0))

    def get_Mode(self):
        b = ctypes.c_int(0)
        self.__lib.Nncam_get_Mode(self.__h, ctypes.byref(b))
        return (b.value != 0)

# White Balance, Temp/Tint mode
    def put_TempTint(self, nTemp, nTint):
        self.__lib.Nncam_put_TempTint(self.__h, ctypes.c_int(nTemp), ctypes.c_int(nTint))

# White Balance, Temp/Tint mode
    def get_TempTint(self):
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        self.__lib.Nncam_get_TempTint(self.__h, ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# White Balance, RGB Gain Mode
    def put_WhiteBalanceGain(self, aGain):
        if len(aGain) == 3:
            x = (ctypes.c_int * 3)(aGain[0], aGain[1], aGain[2])
            self.__lib.Nncam_put_WhiteBalanceGain(self.__h, x)
        else:
            raise HRESULTException(0x80070057)

# White Balance, RGB Gain Mode
    def get_WhiteBalanceGain(self):
        x = (ctypes.c_int * 3)()
        self.__lib.Nncam_get_WhiteBalanceGain(self.__h, x)
        return (x[0], x[1], x[2])

    def put_AWBAuxRect(self, X, Y, Width, Height):
        rc = self.__RECT()
        rc.left = X
        rc.right = X + Width
        rc.top = Y
        rc.bottom = Y + Height
        self.__lib.Nncam_put_AWBAuxRect(self.__h, ctypes.byref(rc))

# left, top, width, height
    def get_AWBAuxRect(self):
        rc = self.__RECT()
        self.__lib.Nncam_get_AWBAuxRect(self.__h, ctypes.byref(rc))
        return (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top)

    def put_AEAuxRect(self, X, Y, Width, Height):
        rc = self.__RECT()
        rc.left = X
        rc.right = X + Width
        rc.top = Y
        rc.bottom = Y + Height
        self.__lib.Nncam_put_AEAuxRect(self.__h, ctypes.byref(rc))

# left, top, width, height
    def get_AEAuxRect(self):
        rc = self.__RECT()
        self.__lib.Nncam_get_AEAuxRect(self.__h, ctypes.byref(rc))
        return (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top)

    def put_BlackBalance(self, aSub):
        if len(aSub) == 3:
            x = (ctypes.c_int * 3)(aSub[0], aSub[1], aSub[2])
            self.__lib.Nncam_put_BlackBalance(self.__h, x)
        else:
            raise HRESULTException(0x80070057)

    def get_BlackBalance(self):
        x = (ctypes.c_int * 3)()
        self.__lib.Nncam_get_BlackBalance(self.__h, x)
        return (x[0], x[1], x[2])

    def put_ABBAuxRect(self, X, Y, Width, Height):
        rc = __RECT()
        rc.left = X
        rc.right = X + Width
        rc.top = Y
        rc.bottom = Y + Height
        self.__lib.Nncam_put_ABBAuxRect(self.__h, ctypes.byref(rc))

# left, top, width, height
    def get_ABBAuxRect(self):
        rc = __RECT()
        self.__lib.Nncam_get_ABBAuxRect(self.__h, ctypes.byref(rc))
        return (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top)

    def get_StillResolution(self, nResolutionIndex):
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        self.__lib.Nncam_get_StillResolution(self.__h, ctypes.c_uint(nResolutionIndex), ctypes.byref(x), ctypes.byref(y))
        return (x.value, y.value)

# led state:
#     iLed: Led index, (0, 1, 2, ...)
#     iState: 1 -> Ever bright; 2 -> Flashing; other -> Off
#     iPeriod: Flashing Period (>= 500ms)
    def put_LEDState(self, iLed, iState, iPeriod):
        self.__lib.Nncam_put_LEDState(self.__h, ctypes.c_ushort(iLed), ctypes.c_ushort(iState), ctypes.c_ushort(iPeriod))

    def write_EEPROM(self, addr, pBuffer):
        self.__lib.Nncam_write_EEPROM(self.__h, addr, pBuffer, ctypes.c_uint(len(pBuffer)))

    def read_EEPROM(self, addr, pBuffer):
        self.__lib.Nncam_read_EEPROM(self.__h, addr, pBuffer, ctypes.c_uint(len(pBuffer)))

    def write_Pipe(self, pipeNum, pBuffer):
        self.__lib.Nncam_write_Pipe(self.__h, pipeNum, pBuffer, ctypes.c_uint(len(pBuffer)))

    def read_Pipe(self, pipeNum, pBuffer):
        self.__lib.Nncam_read_Pipe(self.__h, pipeNum, pBuffer, ctypes.c_uint(len(pBuffer)))

    def feed_Pipe(self, pipeNum):
        self.__lib.Nncam_feed_Pipe(self.__h, ctypes.c_uint(pipeNum))

    def write_UART(self, pBuffer):
        self.__lib.Nncam_write_UART(self.__h, pBuffer, ctypes.c_uint(len(pBuffer)))

    def read_UART(self, pBuffer):
        self.__lib.Nncam_read_UART(self.__h, pBuffer, ctypes.c_uint(len(pBuffer)))

    def put_Option(self, iOption, iValue):
        self.__lib.Nncam_put_Option(self.__h, ctypes.c_uint(iOption), ctypes.c_int(iValue))

    def get_Option(self, iOption):
        x = ctypes.c_int(0)
        self.__lib.Nncam_get_Option(self.__h, ctypes.c_uint(iOption), ctypes.byref(x))
        return x.value

    def put_Linear(self, v8, v16):
        self.__lib.Nncam_put_Linear(self.__h, v8, v16)

    def put_Curve(self, v8, v16):
        self.__lib.Nncam_put_Curve(self.__h, v8, v16)

    def put_ColorMatrix(self, v):
        if len(v) == 9:    
            a = (ctypes.c_double * 9)(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8])
            return self.__lib.Nncam_put_ColorMatrix(self.__h, v)
        else:
            raise HRESULTException(0x80070057)

    def put_InitWBGain(self, v):
        if len(v) == 3:
            a = (ctypes.c_short * 3)(v[0], v[1], v[2])
            self.__lib.Nncam_put_InitWBGain(self.__h, a)
        else:
            raise HRESULTException(0x80070057)

# get the temperature of the sensor, in 0.1 degrees Celsius (32 means 3.2 degrees Celsius, -35 means -3.5 degree Celsius)
    def get_Temperature(self, nTemperature):
        x = ctypes.c_short(0)
        self.__lib.Nncam_get_Temperature(self.__h, ctypes.byref(x))
        return x.value

# set the target temperature of the sensor or TEC, in 0.1 degrees Celsius (32 means 3.2 degrees Celsius, -35 means -3.5 degree Celsius)
    def put_Temperature(self, nTemperature):
        self.__lib.Nncam_put_Temperature(self.__h, ctypes.c_short(nTemperature))

    def put_Roi(self, xOffset, yOffset, xWidth, yHeight):
        self.__lib.Nncam_put_Roi(self.__h, ctypes.c_uint(xOffset), ctypes.c_uint(yOffset), ctypes.c_uint(xWidth), ctypes.c_uint(yHeight))

# xOffset, yOffset, xWidth, yHeight
    def get_Roi(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_uint(0)
        w = ctypes.c_uint(0)
        h = ctypes.c_uint(0)
        self.__lib.Nncam_get_Roi(self.__h, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))
        return (x.value, y.value, w.value, h.value)

# get the frame rate: framerate (fps) = Frame * 1000.0 / nTime
# Frame, Time, TotalFrame
    def get_FrameRate(self):
        x = ctypes.c_uint(0)
        y = ctypes.c_uint(0)
        z = ctypes.c_uint(0)
        self.__lib.Nncam_get_FrameRate(self.__h, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        return (x.value, y.value, z.value)

    def LevelRangeAuto(self):
        self.__lib.Nncam_LevelRangeAuto(self.__h)

# Auto White Balance, Temp/Tint Mode
    def AwbOnePush(self):
        self.__lib.Nncam_AwbOnePush(self.__h, None, None)

# Auto White Balance, RGB Gain Mode
    def AwbInit(self):
        self.__lib.Nncam_AwbInit(self.__h, None, None)

    def AbbOnePush(self):
        self.__lib.Nncam_AbbOnePush(self.__h, None, None)

    def FfcOnePush(self):
        self.__lib.Nncam_FfcOnePush(self.__h)

    def DfcOnePush(self):
        self.__lib.Nncam_DfcOnePush(self.__h)

    def DfcExport(filepath):
        if sys.platform == 'win32':
            self.__lib.Nncam_DfcExport(self.__h, filepath)
        else:
            self.__lib.Nncam_DfcExport(self.__h, filepath.encode('ascii'))

    def FfcExport(filepath):
        if sys.platform == 'win32':
            self.__lib.Nncam_FfcExport(self.__h, filepath)
        else:
            self.__lib.Nncam_FfcExport(self.__h, filepath.encode('ascii'))

    def DfcImport(filepath):
        if sys.platform == 'win32':
            self.__lib.Nncam_DfcImport(self.__h, filepath)
        else:
            self.__lib.Nncam_DfcImport(self.__h, filepath.encode('ascii'))

    def FfcImport(filepath):
        if sys.platform == 'win32':
            self.__lib.Nncam_FfcImport(self.__h, filepath)
        else:
            self.__lib.Nncam_FfcImport(self.__h, filepath.encode('ascii'))

    def IoControl(self, index, eType, outVal):
        x = ctypes.c_int(0)
        self.__lib.Nncam_IoControl(self.__h, ctypes.c_uint(index), ctypes.c_uint(eType), ctypes.c_int(outVal), ctypes.byref(x))
        return x.value

    def get_AfParam(self):
        x = self.__AfParam()
        self.__lib.Nncam_get_AfParam(self.__h, ctypes.byref(x))
        return NnCamAfParam(x.imax.value, x.imin.value, x.idef.value, x.imaxabs.value, x.iminabs.value, x.zoneh.value, x.zonev.value)

    @classmethod
    def __initlib(cls):
        if cls.__lib is None:
            try:
                dir = os.path.dirname(os.path.realpath(__file__))
                if sys.platform == 'win32':
                    cls.__lib = ctypes.windll.LoadLibrary(os.path.join(dir, 'nncam.dll'))
                elif sys.platform.startswith('linux'):
                    cls.__lib = ctypes.cdll.LoadLibrary(os.path.join(dir, 'libnncam.so'))
                else:
                    cls.__lib = ctypes.cdll.LoadLibrary(os.path.join(dir, 'libnncam.dylib'))
            except OSError:
                pass
            
            if cls.__lib is None:
                if sys.platform == 'win32':
                    cls.__lib = ctypes.windll.LoadLibrary('nncam.dll')
                elif sys.platform.startswith('linux'):
                    cls.__lib = ctypes.cdll.LoadLibrary('libnncam.so')
                else:
                    cls.__lib = ctypes.cdll.LoadLibrary('libnncam.dylib')

            cls.__lib.Nncam_Version.argtypes = None
            cls.__lib.Nncam_EnumV2.restype = ctypes.c_uint
            cls.__lib.Nncam_EnumV2.argtypes = [_InstV2 * NNCAM_MAX]
            cls.__lib.Nncam_Open.restype = ctypes.c_void_p
            if sys.platform == 'win32':
                cls.__lib.Nncam_Version.restype = ctypes.c_wchar_p
                cls.__lib.Nncam_Open.argtypes = [ctypes.c_wchar_p]
            else:
                cls.__lib.Nncam_Version.restype = ctypes.c_char_p
                cls.__lib.Nncam_Open.argtypes = [ctypes.c_char_p]
            cls.__lib.Nncam_OpenByIndex.restype = ctypes.c_void_p
            cls.__lib.Nncam_OpenByIndex.argtypes = [ctypes.c_uint]
            cls.__lib.Nncam_Close.restype = None
            cls.__lib.Nncam_Close.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_StartPullModeWithCallback.restype = ctypes.c_int
            cls.__lib.Nncam_StartPullModeWithCallback.errcheck = cls.__errcheck
            cls.__lib.Nncam_StartPullModeWithCallback.argtypes = [ctypes.c_void_p, cls.__EVENTCALLBACKFUNC, ctypes.py_object]
            cls.__lib.Nncam_PullImageV2.restype = ctypes.c_int
            cls.__lib.Nncam_PullImageV2.errcheck = cls.__errcheck
            cls.__lib.Nncam_PullImageV2.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(cls.__FrameInfoV2)]
            cls.__lib.Nncam_PullStillImageV2.restype = ctypes.c_int
            cls.__lib.Nncam_PullStillImageV2.errcheck = cls.__errcheck
            cls.__lib.Nncam_PullStillImageV2.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(cls.__FrameInfoV2)]
            cls.__lib.Nncam_PullImageWithRowPitchV2.restype = ctypes.c_int
            cls.__lib.Nncam_PullImageWithRowPitchV2.errcheck = cls.__errcheck
            cls.__lib.Nncam_PullImageWithRowPitchV2.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(cls.__FrameInfoV2)]
            cls.__lib.Nncam_PullStillImageWithRowPitchV2.restype = ctypes.c_int
            cls.__lib.Nncam_PullStillImageWithRowPitchV2.errcheck = cls.__errcheck
            cls.__lib.Nncam_PullStillImageWithRowPitchV2.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(cls.__FrameInfoV2)]
            cls.__lib.Nncam_Stop.restype = ctypes.c_int
            cls.__lib.Nncam_Stop.errcheck = cls.__errcheck
            cls.__lib.Nncam_Stop.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_Pause.restype = ctypes.c_int
            cls.__lib.Nncam_Pause.errcheck = cls.__errcheck
            cls.__lib.Nncam_Pause.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_Snap.restype = ctypes.c_int
            cls.__lib.Nncam_Snap.errcheck = cls.__errcheck
            cls.__lib.Nncam_Snap.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            cls.__lib.Nncam_SnapN.restype = ctypes.c_int
            cls.__lib.Nncam_SnapN.errcheck = cls.__errcheck
            cls.__lib.Nncam_SnapN.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
            cls.__lib.Nncam_Trigger.restype = ctypes.c_int
            cls.__lib.Nncam_Trigger.errcheck = cls.__errcheck
            cls.__lib.Nncam_Trigger.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            cls.__lib.Nncam_put_Size.restype = ctypes.c_int
            cls.__lib.Nncam_put_Size.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Size.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
            cls.__lib.Nncam_get_Size.restype = ctypes.c_int
            cls.__lib.Nncam_get_Size.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Size.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_eSize.restype = ctypes.c_int
            cls.__lib.Nncam_put_eSize.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_eSize.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            cls.__lib.Nncam_get_eSize.restype = ctypes.c_int
            cls.__lib.Nncam_get_eSize.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_eSize.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_get_ResolutionNumber.restype = ctypes.c_int
            cls.__lib.Nncam_get_ResolutionNumber.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ResolutionNumber.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_Resolution.restype = ctypes.c_int
            cls.__lib.Nncam_get_Resolution.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Resolution.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)];
            cls.__lib.Nncam_get_ResolutionRatio.restype = ctypes.c_int
            cls.__lib.Nncam_get_ResolutionRatio.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ResolutionRatio.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)];
            cls.__lib.Nncam_get_Field.restype = ctypes.c_int
            cls.__lib.Nncam_get_Field.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Field.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_RawFormat.restype = ctypes.c_int
            cls.__lib.Nncam_get_RawFormat.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_RawFormat.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_get_AutoExpoEnable.restype = ctypes.c_int
            cls.__lib.Nncam_get_AutoExpoEnable.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_AutoExpoEnable.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_AutoExpoEnable.restype = ctypes.c_int
            cls.__lib.Nncam_put_AutoExpoEnable.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_AutoExpoEnable.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_AutoExpoTarget.restype = ctypes.c_int
            cls.__lib.Nncam_get_AutoExpoTarget.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_AutoExpoTarget.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_put_AutoExpoTarget.restype = ctypes.c_int
            cls.__lib.Nncam_put_AutoExpoTarget.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_AutoExpoTarget.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_put_MaxAutoExpoTimeAGain.restype = ctypes.c_int
            cls.__lib.Nncam_put_MaxAutoExpoTimeAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_MaxAutoExpoTimeAGain.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort]
            cls.__lib.Nncam_get_MaxAutoExpoTimeAGain.restype = ctypes.c_int
            cls.__lib.Nncam_get_MaxAutoExpoTimeAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_MaxAutoExpoTimeAGain.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_put_MinAutoExpoTimeAGain.restype = ctypes.c_int
            cls.__lib.Nncam_put_MinAutoExpoTimeAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_MinAutoExpoTimeAGain.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort]
            cls.__lib.Nncam_get_MinAutoExpoTimeAGain.restype = ctypes.c_int
            cls.__lib.Nncam_get_MinAutoExpoTimeAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_MinAutoExpoTimeAGain.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_put_ExpoTime.restype = ctypes.c_int
            cls.__lib.Nncam_put_ExpoTime.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_ExpoTime.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            cls.__lib.Nncam_get_ExpoTime.restype = ctypes.c_int
            cls.__lib.Nncam_get_ExpoTime.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ExpoTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_get_RealExpoTime.restype = ctypes.c_int
            cls.__lib.Nncam_get_RealExpoTime.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_RealExpoTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_get_ExpTimeRange.restype = ctypes.c_int
            cls.__lib.Nncam_get_ExpTimeRange.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ExpTimeRange.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_put_ExpoAGain.restype = ctypes.c_int
            cls.__lib.Nncam_put_ExpoAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_ExpoAGain.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            cls.__lib.Nncam_get_ExpoAGain.restype = ctypes.c_int
            cls.__lib.Nncam_get_ExpoAGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ExpoAGain.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_get_ExpoAGainRange.restype = ctypes.c_int
            cls.__lib.Nncam_get_ExpoAGainRange.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ExpoAGainRange.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_AwbOnePush.restype = ctypes.c_int
            cls.__lib.Nncam_AwbOnePush.errcheck = cls.__errcheck
            cls.__lib.Nncam_AwbOnePush.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
            cls.__lib.Nncam_AwbInit.restype = ctypes.c_int
            cls.__lib.Nncam_AwbInit.errcheck = cls.__errcheck
            cls.__lib.Nncam_AwbInit.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
            cls.__lib.Nncam_put_TempTint.restype = ctypes.c_int
            cls.__lib.Nncam_put_TempTint.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_TempTint.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
            cls.__lib.Nncam_get_TempTint.restype = ctypes.c_int
            cls.__lib.Nncam_get_TempTint.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_TempTint.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_WhiteBalanceGain.restype = ctypes.c_int
            cls.__lib.Nncam_put_WhiteBalanceGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_WhiteBalanceGain.argtypes = [ctypes.c_void_p, (ctypes.c_int * 3)]
            cls.__lib.Nncam_get_WhiteBalanceGain.restype = ctypes.c_int
            cls.__lib.Nncam_get_WhiteBalanceGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_WhiteBalanceGain.argtypes = [ctypes.c_void_p, (ctypes.c_int * 3)]
            cls.__lib.Nncam_put_BlackBalance.restype = ctypes.c_int
            cls.__lib.Nncam_put_BlackBalance.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_BlackBalance.argtypes = [ctypes.c_void_p, (ctypes.c_int * 3)]
            cls.__lib.Nncam_get_BlackBalance.restype = ctypes.c_int
            cls.__lib.Nncam_get_BlackBalance.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_BlackBalance.argtypes = [ctypes.c_void_p, (ctypes.c_int * 3)]
            cls.__lib.Nncam_AbbOnePush.restype = ctypes.c_int
            cls.__lib.Nncam_AbbOnePush.errcheck = cls.__errcheck
            cls.__lib.Nncam_AbbOnePush.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
            cls.__lib.Nncam_FfcOnePush.restype = ctypes.c_int
            cls.__lib.Nncam_FfcOnePush.errcheck = cls.__errcheck
            cls.__lib.Nncam_FfcOnePush.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_DfcOnePush.restype = ctypes.c_int
            cls.__lib.Nncam_DfcOnePush.errcheck = cls.__errcheck
            cls.__lib.Nncam_DfcOnePush.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_FfcExport.restype = ctypes.c_int
            cls.__lib.Nncam_FfcExport.errcheck = cls.__errcheck
            cls.__lib.Nncam_FfcImport.restype = ctypes.c_int
            cls.__lib.Nncam_FfcImport.errcheck = cls.__errcheck
            cls.__lib.Nncam_DfcExport.restype = ctypes.c_int
            cls.__lib.Nncam_DfcExport.errcheck = cls.__errcheck
            cls.__lib.Nncam_DfcImport.restype = ctypes.c_int
            cls.__lib.Nncam_DfcImport.errcheck = cls.__errcheck
            if sys.platform == 'win32':
                cls.__lib.Nncam_FfcExport.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
                cls.__lib.Nncam_FfcImport.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
                cls.__lib.Nncam_DfcExport.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
                cls.__lib.Nncam_DfcImport.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
            else:
                cls.__lib.Nncam_FfcExport.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
                cls.__lib.Nncam_FfcImport.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
                cls.__lib.Nncam_DfcExport.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
                cls.__lib.Nncam_DfcImport.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            cls.__lib.Nncam_put_Hue.restype = ctypes.c_int
            cls.__lib.Nncam_put_Hue.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Hue.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Hue.restype = ctypes.c_int
            cls.__lib.Nncam_get_Hue.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Hue.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Saturation.restype = ctypes.c_int
            cls.__lib.Nncam_put_Saturation.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Saturation.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Saturation.restype = ctypes.c_int
            cls.__lib.Nncam_get_Saturation.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Saturation.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Brightness.restype = ctypes.c_int
            cls.__lib.Nncam_put_Brightness.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Brightness.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Brightness.restype = ctypes.c_int
            cls.__lib.Nncam_get_Brightness.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Brightness.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Contrast.restype = ctypes.c_int
            cls.__lib.Nncam_put_Contrast.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Contrast.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Contrast.restype = ctypes.c_int
            cls.__lib.Nncam_get_Contrast.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Contrast.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Gamma.restype = ctypes.c_int
            cls.__lib.Nncam_put_Gamma.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Gamma.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Gamma.restype = ctypes.c_int
            cls.__lib.Nncam_get_Gamma.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Gamma.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Chrome.restype = ctypes.c_int
            cls.__lib.Nncam_put_Chrome.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Chrome.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Chrome.restype = ctypes.c_int
            cls.__lib.Nncam_get_Chrome.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Chrome.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_VFlip.restype = ctypes.c_int
            cls.__lib.Nncam_put_VFlip.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_VFlip.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_VFlip.restype = ctypes.c_int
            cls.__lib.Nncam_get_VFlip.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_VFlip.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_HFlip.restype = ctypes.c_int
            cls.__lib.Nncam_put_HFlip.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_HFlip.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_HFlip.restype = ctypes.c_int
            cls.__lib.Nncam_get_HFlip.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_HFlip.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Negative.restype = ctypes.c_int
            cls.__lib.Nncam_put_Negative.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Negative.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Negative.restype = ctypes.c_int
            cls.__lib.Nncam_get_Negative.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Negative.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Speed.restype = ctypes.c_int
            cls.__lib.Nncam_put_Speed.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Speed.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            cls.__lib.Nncam_get_Speed.restype = ctypes.c_int
            cls.__lib.Nncam_get_Speed.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Speed.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_get_MaxSpeed.restype = ctypes.c_int
            cls.__lib.Nncam_get_MaxSpeed.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_MaxSpeed.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_FanMaxSpeed.restype = ctypes.c_int
            cls.__lib.Nncam_get_FanMaxSpeed.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_FanMaxSpeed.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_MaxBitDepth.restype = ctypes.c_int
            cls.__lib.Nncam_get_MaxBitDepth.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_MaxBitDepth.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_put_HZ.restype = ctypes.c_int
            cls.__lib.Nncam_put_HZ.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_HZ.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_HZ.restype = ctypes.c_int
            cls.__lib.Nncam_get_HZ.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_HZ.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Mode.restype = ctypes.c_int
            cls.__lib.Nncam_put_Mode.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Mode.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_Mode.restype = ctypes.c_int
            cls.__lib.Nncam_get_Mode.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Mode.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_AWBAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_put_AWBAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_AWBAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_get_AWBAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_get_AWBAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_AWBAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_put_AEAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_put_AEAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_AEAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_get_AEAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_get_AEAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_AEAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_put_ABBAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_put_ABBAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_ABBAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_get_ABBAuxRect.restype = ctypes.c_int
            cls.__lib.Nncam_get_ABBAuxRect.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ABBAuxRect.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__RECT)]
            cls.__lib.Nncam_get_MonoMode.restype = ctypes.c_int
            cls.__lib.Nncam_get_MonoMode.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_MonoMode.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_StillResolutionNumber.restype = ctypes.c_int
            cls.__lib.Nncam_get_StillResolutionNumber.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_StillResolutionNumber.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_get_StillResolution.restype = ctypes.c_int
            cls.__lib.Nncam_get_StillResolution.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_StillResolution.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_RealTime.restype = ctypes.c_int
            cls.__lib.Nncam_put_RealTime.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_RealTime.argtypes = [ctypes.c_void_p, ctypes.c_int]
            cls.__lib.Nncam_get_RealTime.restype = ctypes.c_int
            cls.__lib.Nncam_get_RealTime.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_RealTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_Flush.restype = ctypes.c_int
            cls.__lib.Nncam_Flush.errcheck = cls.__errcheck
            cls.__lib.Nncam_Flush.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_put_Temperature.restype = ctypes.c_int
            cls.__lib.Nncam_put_Temperature.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Temperature.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            cls.__lib.Nncam_get_Temperature.restype = ctypes.c_int
            cls.__lib.Nncam_get_Temperature.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Temperature.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_get_Revision.restype = ctypes.c_int
            cls.__lib.Nncam_get_Revision.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Revision.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_get_SerialNumber.restype = ctypes.c_int
            cls.__lib.Nncam_get_SerialNumber.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_SerialNumber.argtypes = [ctypes.c_void_p, ctypes.c_char * 32]
            cls.__lib.Nncam_get_FwVersion.restype = ctypes.c_int
            cls.__lib.Nncam_get_FwVersion.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_FwVersion.argtypes = [ctypes.c_void_p, ctypes.c_char * 16]
            cls.__lib.Nncam_get_HwVersion.restype = ctypes.c_int
            cls.__lib.Nncam_get_HwVersion.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_HwVersion.argtypes = [ctypes.c_void_p, ctypes.c_char * 16]
            cls.__lib.Nncam_get_ProductionDate.restype = ctypes.c_int
            cls.__lib.Nncam_get_ProductionDate.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_ProductionDate.argtypes = [ctypes.c_void_p, ctypes.c_char * 16]
            cls.__lib.Nncam_get_FpgaVersion.restype = ctypes.c_int
            cls.__lib.Nncam_get_FpgaVersion.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_FpgaVersion.argtypes = [ctypes.c_void_p, ctypes.c_char * 16]
            cls.__lib.Nncam_get_PixelSize.restype = ctypes.c_int
            cls.__lib.Nncam_get_PixelSize.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_PixelSize.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
            cls.__lib.Nncam_put_LevelRange.restype = ctypes.c_int
            cls.__lib.Nncam_put_LevelRange.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_LevelRange.argtypes = [ctypes.c_void_p, (ctypes.c_ushort * 4), (ctypes.c_ushort * 4)]
            cls.__lib.Nncam_get_LevelRange.restype = ctypes.c_int
            cls.__lib.Nncam_get_LevelRange.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_LevelRange.argtypes = [ctypes.c_void_p, (ctypes.c_ushort * 4), (ctypes.c_ushort * 4)]
            cls.__lib.Nncam_LevelRangeAuto.restype = ctypes.c_int
            cls.__lib.Nncam_LevelRangeAuto.errcheck = cls.__errcheck
            cls.__lib.Nncam_LevelRangeAuto.argtypes = [ctypes.c_void_p]
            cls.__lib.Nncam_put_LEDState.restype = ctypes.c_int
            cls.__lib.Nncam_put_LEDState.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_LEDState.argtypes = [ctypes.c_void_p, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort]
            cls.__lib.Nncam_write_EEPROM.restype = ctypes.c_int
            cls.__lib.Nncam_write_EEPROM.errcheck = cls.__errcheck
            cls.__lib.Nncam_write_EEPROM.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_read_EEPROM.restype = ctypes.c_int
            cls.__lib.Nncam_read_EEPROM.errcheck = cls.__errcheck
            cls.__lib.Nncam_read_EEPROM.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_read_Pipe.restype = ctypes.c_int
            cls.__lib.Nncam_read_Pipe.errcheck = cls.__errcheck
            cls.__lib.Nncam_read_Pipe.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_write_Pipe.restype = ctypes.c_int
            cls.__lib.Nncam_write_Pipe.errcheck = cls.__errcheck
            cls.__lib.Nncam_write_Pipe.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_feed_Pipe.restype = ctypes.c_int
            cls.__lib.Nncam_feed_Pipe.errcheck = cls.__errcheck
            cls.__lib.Nncam_feed_Pipe.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            cls.__lib.Nncam_put_Option.restype = ctypes.c_int
            cls.__lib.Nncam_put_Option.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Option.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int]
            cls.__lib.Nncam_get_Option.restype = ctypes.c_int
            cls.__lib.Nncam_get_Option.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Option.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_put_Roi.restype = ctypes.c_int
            cls.__lib.Nncam_put_Roi.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Roi.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
            cls.__lib.Nncam_get_Roi.restype = ctypes.c_int
            cls.__lib.Nncam_get_Roi.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_Roi.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
            cls.__lib.Nncam_get_AfParam.restype = ctypes.c_int
            cls.__lib.Nncam_get_AfParam.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_AfParam.argtypes = [ctypes.c_void_p, ctypes.POINTER(cls.__AfParam)]
            cls.__lib.Nncam_IoControl.restype = ctypes.c_int
            cls.__lib.Nncam_IoControl.errcheck = cls.__errcheck
            cls.__lib.Nncam_IoControl.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Nncam_read_UART.restype = ctypes.c_int
            cls.__lib.Nncam_read_UART.errcheck = cls.__errcheck
            cls.__lib.Nncam_read_UART.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_write_UART.restype = ctypes.c_int
            cls.__lib.Nncam_write_UART.errcheck = cls.__errcheck
            cls.__lib.Nncam_write_UART.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            cls.__lib.Nncam_put_Linear.restype = ctypes.c_int
            cls.__lib.Nncam_put_Linear.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Linear.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_put_Curve.restype = ctypes.c_int
            cls.__lib.Nncam_put_Curve.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_Curve.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ushort)]
            cls.__lib.Nncam_put_ColorMatrix.restype = ctypes.c_int
            cls.__lib.Nncam_put_ColorMatrix.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_ColorMatrix.argtypes = [ctypes.c_void_p, ctypes.c_double * 9]
            cls.__lib.Nncam_put_InitWBGain.restype = ctypes.c_int
            cls.__lib.Nncam_put_InitWBGain.errcheck = cls.__errcheck
            cls.__lib.Nncam_put_InitWBGain.argtypes = [ctypes.c_void_p, ctypes.c_ushort * 3]
            cls.__lib.Nncam_get_FrameRate.restype = ctypes.c_int
            cls.__lib.Nncam_get_FrameRate.errcheck = cls.__errcheck
            cls.__lib.Nncam_get_FrameRate.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
            if sys.platform != 'win32':
                cls.__lib.Nncam_HotPlug.restype = None
                cls.__lib.Nncam_HotPlug.errcheck = cls.__errcheck
                cls.__lib.Nncam_HotPlug.argtypes = [cls.__HOTPLUGCALLBACKFUNC, ctypes.c_void_p]