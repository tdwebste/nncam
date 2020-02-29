#ifndef __nncam_dshow_h__
#define __nncam_dshow_h__

/* Version: 37.14643.2019.0511 */

#ifdef _WIN32
#ifndef _INC_WINDOWS
#include <windows.h>
#endif
#endif

#ifndef __NNCAM_CALLBACK_DEFINED__
#define __NNCAM_CALLBACK_DEFINED__
typedef void (__stdcall* PINNCAM_EXPOSURE_CALLBACK)(void* pCtx);                                      /* auto exposure */
typedef void (__stdcall* PINNCAM_WHITEBALANCE_CALLBACK)(const int aGain[3], void* pCtx);              /* one push white balance, RGB Gain mode */
typedef void (__stdcall* PINNCAM_BLACKBALANCE_CALLBACK)(const unsigned short aSub[3], void* pCtx);    /* one push black balance */
typedef void (__stdcall* PINNCAM_TEMPTINT_CALLBACK)(const int nTemp, const int nTint, void* pCtx);    /* one push white balance, Temp/Tint Mode */
typedef void (__stdcall* PINNCAM_HISTOGRAM_CALLBACK)(const float aHistY[256], const float aHistR[256], const float aHistG[256], const float aHistB[256], void* pCtx);
typedef void (__stdcall* PINNCAM_CHROME_CALLBACK)(void* pCtx);
#endif

#ifndef __NNCAMAFPARAM_DEFINED__
#define __NNCAMAFPARAM_DEFINED__
typedef struct {
    int imax;    /* maximum auto focus sensor board positon */
    int imin;    /* minimum auto focus sensor board positon */
    int idef;    /* conjugate calibration positon */
    int imaxabs; /* maximum absolute auto focus sensor board positon, micrometer */
    int iminabs; /* maximum absolute auto focus sensor board positon, micrometer */
    int zoneh;   /* zone horizontal */
    int zonev;   /* zone vertical */
}NncamAfParam;
#endif

#ifndef __INNCAM_DEFINED__
#define __INNCAM_DEFINED__
    /* Both the DirectShow source filter and the output pin(s) support this interface.
        That is to say, you can use QueryInterface on the filter or the pin(s) to get the INncam interface.
    */
    // {66B8EAB5-B594-4141-95FC-691A81B445F6}
    DEFINE_GUID(IID_INncam, 0x66b8eab5, 0xb594, 0x4141, 0x95, 0xfc, 0x69, 0x1a, 0x81, 0xb4, 0x45, 0xf6);

    DECLARE_INTERFACE_(INncam, IUnknown)
    {
        /*
            put_Size, put_eSize, can be used to set the video output resolution BEFORE the DirectShow source filter is connected.
            put_Size use width and height parameters, put_eSize use the index parameter.
            for example, UCMOS03100KPA support the following resolutions:
                    index 0:    2048,   1536
                    index 1:    1024,   768
                    index 2:    680,    510
            so, we can use put_Size(1024, 768) or put_eSize(1). Both have the same effect.
            
            ------------------------------------------------------------------|
            | Parameter               |   Range       |   Default             |
            |-----------------------------------------------------------------|
            | Auto Exposure Target    |   16~235      |   120                 |
            | Temp                    |   2000~15000  |   6503                |
            | Tint                    |   200~2500    |   1000                |
            | LevelRange              |   0~255       |   Low = 0, High = 255 |
            | Contrast                |   -100~100    |   0                   |
            | Hue                     |   -180~180    |   0                   |
            | Saturation              |   0~255       |   128                 |
            | Brightness              |   -64~64      |   0                   |
            | Gamma                   |   20~180      |   100                 |
            | VidgetAmount            |   -100~100    |   0                   |
            | VignetMidPoint          |   0~100       |   50                  |
            ------------------------------------------------------------------|
        */
        STDMETHOD(put_Size) (THIS_ int nWidth, int nHeight) PURE;
        STDMETHOD(get_Size) (THIS_ int* pWidth, int* pHeight) PURE;
        STDMETHOD(put_eSize) (THIS_ unsigned nResolutionIndex) PURE;
        STDMETHOD(get_eSize) (THIS_ unsigned* pResolutionIndex) PURE;
        STDMETHOD(LevelRangeAuto) (THIS_) PURE;
        STDMETHOD(GetHistogram) (THIS_ PINNCAM_HISTOGRAM_CALLBACK fnHistogramProc, void* pHistogramCtx) PURE;            
        STDMETHOD(put_ExpoCallback) (THIS_ PINNCAM_EXPOSURE_CALLBACK fnExpoProc, void* pExpoCtx) PURE;
        STDMETHOD(get_AutoExpoEnable) (THIS_ int* bAutoExposure) PURE;
        STDMETHOD(put_AutoExpoEnable) (THIS_ int bAutoExposure) PURE;
        STDMETHOD(get_AutoExpoTarget) (THIS_ unsigned short* Target) PURE;
        STDMETHOD(put_AutoExpoTarget) (THIS_ unsigned short Target) PURE;
        /* Auto White Balance, RGB Gain mode */
        STDMETHOD(AwbInit) (THIS_ PINNCAM_WHITEBALANCE_CALLBACK fnWBProc, void* pWBCtx) PURE;
        STDMETHOD(put_AuxRect) (THIS_ const RECT* pAuxRect) PURE;
        STDMETHOD(get_AuxRect) (THIS_ RECT* pAuxRect) PURE;
        STDMETHOD(put_AuxRectShow) (THIS_ int bShow) PURE;
        STDMETHOD(get_AuxRectShow) (THIS_ int* bShow) PURE;
        STDMETHOD(put_VignetEnable) (THIS_ int bEnable) PURE;
        STDMETHOD(get_VignetEnable) (THIS_ int* bEnable) PURE;
        /* obsolete, please use put_VignetAmountInt */
        STDMETHOD(put_VignetAmount) (THIS_ double dAmount) PURE;
        /* obsolete, please use get_VignetAmountInt */
        STDMETHOD(get_VignetAmount) (THIS_ double* dAmount) PURE;
        /* obsolete, please use put_VignetMidPointInt */
        STDMETHOD(put_VignetMidPoint) (THIS_ double dMidPoint) PURE;
        /* obsolete, please use get_VignetMidPointInt */
        STDMETHOD(get_VignetMidPoint) (THIS_ double* dMidPoint) PURE;
        /* White Balance, RGB Gain mode */
        STDMETHOD(put_WhiteBalanceGain) (THIS_ int aGain[3]) PURE;
        /* White Balance, RGB Gain mode */
        STDMETHOD(get_WhiteBalanceGain) (THIS_ int aGain[3]) PURE;
        STDMETHOD(put_Hue) (THIS_ int Hue) PURE;
        STDMETHOD(get_Hue) (THIS_ int* Hue) PURE;
        STDMETHOD(put_Saturation) (THIS_ int Saturation) PURE;
        STDMETHOD(get_Saturation) (THIS_ int* Saturation) PURE;
        STDMETHOD(put_Brightness) (THIS_ int Brightness) PURE;
        STDMETHOD(get_Brightness) (THIS_ int* Brightness) PURE;
        /* microsecond */
        STDMETHOD(get_ExpoTime) (THIS_ unsigned* Time) PURE;
        /* microsecond */
        STDMETHOD(put_ExpoTime) (THIS_ unsigned Time) PURE;
        /* percent */
        STDMETHOD(get_ExpoAGain) (THIS_ unsigned short* AGain) PURE;
        /* percent */
        STDMETHOD(put_ExpoAGain) (THIS_ unsigned short AGain) PURE;
        STDMETHOD(put_LevelRange) (THIS_ unsigned short aLow[4], unsigned short aHigh[4]) PURE;
        STDMETHOD(get_LevelRange) (THIS_ unsigned short aLow[4], unsigned short aHigh[4]) PURE;
        STDMETHOD(get_Contrast) (THIS_ int* Contrast) PURE;
        STDMETHOD(put_Contrast) (THIS_ int Contrast) PURE;
        STDMETHOD(get_Gamma) (THIS_ int* Gamma) PURE;
        STDMETHOD(put_Gamma) (THIS_ int Gamma) PURE;
        STDMETHOD(get_Chrome) (THIS_ int* bChrome) PURE;
        /* monochromatic */
        STDMETHOD(put_Chrome) (THIS_ int bChrome) PURE;
        STDMETHOD(get_VFlip) (THIS_ int* bVFlip) PURE;
        /* vertical flip */
        STDMETHOD(put_VFlip) (THIS_ int bVFlip) PURE;
        STDMETHOD(get_HFlip) (THIS_ int* bHFlip) PURE;
        /* horizontal flip */
        STDMETHOD(put_HFlip) (THIS_ int bHFlip) PURE;
        STDMETHOD(put_Speed) (THIS_ unsigned short nSpeed) PURE;
        STDMETHOD(get_Speed) (THIS_ unsigned short* pSpeed) PURE;
        /* get the maximum frame speed, see Misc page, "Frame Speed Level", speed range = [0, max] */
        STDMETHOD(get_MaxSpeed) (THIS_) PURE;

        /* power supply: 
                0 -> 60HZ AC
                1 -> 50Hz AC
                2 -> DC
        */
        STDMETHOD(put_HZ) (THIS_ int nHZ) PURE;
        STDMETHOD(get_HZ) (THIS_ int* nHZ) PURE;
        /* skip or bin */
        STDMETHOD(put_Mode) (THIS_ int bSkip) PURE;
        STDMETHOD(get_Mode) (THIS_ int* bSkip) PURE;
        STDMETHOD(put_ChromeCallback) (THIS_ PINNCAM_CHROME_CALLBACK fnChromeProc, void* pChromeCtx) PURE;
        STDMETHOD(get_ExpTimeRange) (THIS_ unsigned* nMin, unsigned* nMax, unsigned* nDef) PURE;
        STDMETHOD(get_ExpoAGainRange) (THIS_ unsigned short* nMin, unsigned short* nMax, unsigned short* nDef) PURE;
        STDMETHOD(get_ResolutionNumber) (THIS_) PURE;
        STDMETHOD(get_Resolution) (THIS_ unsigned nResolutionIndex, int* pWidth, int* pHeight) PURE;
        /* White Balance, Temp/Tint mode */
        STDMETHOD(put_TempTint) (THIS_ int nTemp, int nTint) PURE;
        /* White Balance, Temp/Tint mode */
        STDMETHOD(get_TempTint) (THIS_ int* nTemp, int* nTint) PURE;
        STDMETHOD(put_VignetAmountInt) (THIS_ int nAmount) PURE;
        STDMETHOD(get_VignetAmountInt) (THIS_ int* nAmount) PURE;
        STDMETHOD(put_VignetMidPointInt) (THIS_ int nMidPoint) PURE;
        STDMETHOD(get_VignetMidPointInt) (THIS_ int* nMidPoint) PURE;
        /* Auto White Balance, Temp/Tint Mode */
        STDMETHOD(AwbOnePush) (THIS_ PINNCAM_TEMPTINT_CALLBACK fnTTProc, void* pTTCtx) PURE;
        STDMETHOD(put_AWBAuxRect) (THIS_ const RECT* pAuxRect) PURE;
        STDMETHOD(get_AWBAuxRect) (THIS_ RECT* pAuxRect) PURE;
        STDMETHOD(put_AEAuxRect) (THIS_ const RECT* pAuxRect) PURE;
        STDMETHOD(get_AEAuxRect) (THIS_ RECT* pAuxRect) PURE;
        /*
            S_FALSE:    color mode
            S_OK:       mono mode, such as EXCCD00300KMA
        */
        STDMETHOD(get_MonoMode) (THIS_) PURE;
        STDMETHOD(put_MaxAutoExpoTimeAGain) (THIS_ unsigned maxTime, unsigned short maxAGain) PURE;
        STDMETHOD(get_RealExpoTime) (THIS_ unsigned* Time) PURE;
        /*
            return: 8, 10, 12, 14, 16
        */
        STDMETHOD(get_MaxBitDepth) (THIS_) PURE;
        /*
            obsolete, please use get_PixelFormat, put_PixelFormat
            FALSE: 8 bits
            TRUE: > 8 bits
        */
        STDMETHOD(get_BitDepth) (THIS_ int* bBitDepth) PURE;
        STDMETHOD(put_BitDepth) (THIS_ int bBitDepth) PURE;
        
        /* get the temperature of sensor, in 0.1 degrees Celsius (32 means 3.2 degrees Celsius, -35 means -3.5 degree Celsius)
            return E_NOTIMPL if not supported
        */
        STDMETHOD(get_Temperature) (THIS_ short* pTemperature) PURE;
        /* set the temperature of sensor, in 0.1 degrees Celsius (32 means 3.2 degrees Celsius, -35 means -3.5 degree Celsius)
            return E_NOTIMPL if not supported
        */
        STDMETHOD(put_Temperature) (THIS_ short nTemperature) PURE;
        STDMETHOD(put_Roi) (THIS_ unsigned xOffset, unsigned yOffset, unsigned xWidth, unsigned yHeight) PURE;
        STDMETHOD(get_Roi) (THIS_ unsigned* pxOffset, unsigned* pyOffset, unsigned* pxWidth, unsigned* pyHeight) PURE;
        /*
            get the fan speed.
            return E_NOTIMPL if not supported
        */
        STDMETHOD(get_Fan) (THIS_ unsigned short* nFan) PURE;
        /*
            set the fan speed.
            return E_NOTIMPL if not supported
        */
        STDMETHOD(put_Fan) (THIS_ unsigned short nFan) PURE;
        /*
            get the thermoelectric cooler status: on or off.
            return E_NOTIMPL if not supported
        */
        STDMETHOD(get_TEC) (THIS_ int* bTEC) PURE;
        /*
            set the thermoelectric cooler status: on or off.
            return E_NOTIMPL if not supported
        */ 
        STDMETHOD(put_TEC) (THIS_ int bTEC) PURE;
        STDMETHOD(get_ResolutionRatio) (THIS_ unsigned nResolutionIndex, int* pNumerator, int* pDenominator) PURE;
        /*  get the target temperature of the thermoelectric cooler, in 0.1 degree Celsius. For example, 125 means 12.5 degree Celsius, -35 means -3.5 degree Celsius */
        STDMETHOD(get_TECTarget) (THIS_ int* nTECTarget) PURE;
        /*  set the target temperature of the thermoelectric cooler, in 0.1 degree Celsius */
        STDMETHOD(put_TECTarget) (THIS_ int nTECTarget) PURE;
        STDMETHOD(get_Field) (THIS_) PURE;
        /*
            get the sensor pixel size, such as: 2.4um
        */
        STDMETHOD(get_PixelSize) (THIS_ unsigned nResolutionIndex, float* x, float* y) PURE;
        STDMETHOD(get_FanMaxSpeed) (THIS_) PURE;
        STDMETHOD(get_FrameRate)(THIS_ unsigned* nFrame, unsigned* nTime, unsigned* nTotalFrame) PURE;
        STDMETHOD(put_Option) (THIS_ unsigned iOption, int iValue) PURE;
        STDMETHOD(get_Option) (THIS_ unsigned iOption, int* piValue) PURE;
        STDMETHOD(put_Linear) (THIS_ const unsigned char* v8, const unsigned short* v16) PURE;
        STDMETHOD(put_Curve) (THIS_ const unsigned char* v8, const unsigned short* v16) PURE;
        STDMETHOD(put_ColorMatrix) (THIS_ const double v[9]) PURE;
        STDMETHOD(put_InitWBGain) (THIS_ const unsigned short v[3]) PURE;
        
        /* auto black balance */
        STDMETHOD(put_BlackBalance) (THIS_ unsigned short aSub[3]) PURE;
        STDMETHOD(get_BlackBalance) (THIS_ unsigned short aSub[3]) PURE;
        STDMETHOD(AbbOnePush) (THIS_ PINNCAM_BLACKBALANCE_CALLBACK fnBBProc, void* pBBCtx) PURE;
        STDMETHOD(put_ABBAuxRect) (THIS_ const RECT* pAuxRect) PURE;
        STDMETHOD(get_ABBAuxRect) (THIS_ RECT* pAuxRect) PURE;
        
        /*
        pixel format:
            RAW8            0x00
            RAW10           0x01
            RAW12           0x02
            RAW14           0x03
            RAW16           0x04
            YUV411          0x05
            VUYY            0x06
            YUV444          0x07
            RGB888          0x08
            GMCY8           0x09
            GMCY12          0x0a
            UYVY            0x0b
        */
        STDMETHOD(get_PixelFormat) (THIS_ unsigned* nPixelFormat) PURE;
        STDMETHOD(put_PixelFormat) (THIS_ unsigned nPixelFormat) PURE;
        
        /* Flat Field Correction */
        STDMETHOD(FfcOnePush) (THIS_ ) PURE;
        STDMETHOD(get_FfcStatus) (THIS_ int* status) PURE; /* see NNCAM_OPTION_FFC */
        STDMETHOD(put_FfcStatus) (THIS_ int status) PURE;

        STDMETHOD(IoControl)(unsigned index, unsigned nType, int outVal, int* inVal) PURE;

        /* Dark Field Correction */
        STDMETHOD(DfcOnePush) (THIS_) PURE;
        STDMETHOD(get_DfcStatus) (THIS_ int* status) PURE; /* see NNCAM_OPTION_DFC */
        STDMETHOD(put_DfcStatus) (THIS_ int status) PURE;
        
        STDMETHOD(put_RealTime) (THIS_ int bEnable) PURE;
        STDMETHOD(get_RealTime) (THIS_ int* bEnable) PURE;
        STDMETHOD(Flush) (THIS_) PURE;

        STDMETHOD(put_Negative) (THIS_ int bNegative) PURE;
        STDMETHOD(get_Negative) (THIS_ int* bNegative) PURE;
        STDMETHOD(put_LEDState) (THIS_ unsigned short iLed, unsigned short iState, unsigned short iPeriod) PURE;
        STDMETHOD(read_EEPROM) (THIS_ unsigned addr, unsigned char* pBuffer, unsigned nBufferLen) PURE;
        STDMETHOD(write_EEPROM) (THIS_ unsigned addr, const unsigned char* pBuffer, unsigned nBufferLen) PURE;
        STDMETHOD(read_UART) (THIS_ unsigned char* pBuffer, unsigned nBufferLen) PURE;
        STDMETHOD(write_UART) (THIS_ const unsigned char* pBuffer, unsigned nBufferLen) PURE;

#ifdef _WIN32
        STDMETHOD(DfcExport) (THIS_ const wchar_t* filepath) PURE;
        STDMETHOD(DfcImport) (THIS_ const wchar_t* filepath) PURE;
        STDMETHOD(FfcExport) (THIS_ const wchar_t* filepath) PURE;
        STDMETHOD(FfcImport) (THIS_ const wchar_t* filepath) PURE;
#else
        STDMETHOD(DfcExport) (THIS_ const char* filepath) PURE;
        STDMETHOD(DfcImport) (THIS_ const char* filepath) PURE;
        STDMETHOD(FfcExport) (THIS_ const char* filepath) PURE;
        STDMETHOD(FfcImport) (THIS_ const char* filepath) PURE;
#endif
        STDMETHOD(read_Pipe) (THIS_ unsigned pipeNum, void* pBuffer, unsigned nBufferLen) PURE;
        STDMETHOD(write_Pipe) (THIS_ unsigned pipeNum, const void* pBuffer, unsigned nBufferLen) PURE;
        STDMETHOD(feed_Pipe) (THIS_ unsigned pipeNum) PURE;
        
        STDMETHOD(get_MaxAutoExpoTimeAGain) (THIS_ unsigned* maxTime, unsigned short* maxAGain) PURE;
        STDMETHOD(put_MinAutoExpoTimeAGain) (THIS_ unsigned minTime, unsigned short minAGain) PURE;
        STDMETHOD(get_MinAutoExpoTimeAGain) (THIS_ unsigned* minTime, unsigned short* minAGain) PURE;

        STDMETHOD(get_AfParam) (THIS_ NncamAfParam* pAfParam) PURE;
    };
#endif

#ifndef __INNCAMSTILLIMAGE_DEFINED__
#define __INNCAMSTILLIMAGE_DEFINED__
    /* most Nn Camera DirectShow source filters has two output pins, one is pin category PIN_CATEGORY_PREVIEW, and the other is pin category PIN_CATEGORY_STILL.
        Please refrence MSDN library "Capturing an Image From a Still Image Pin". http://msdn.microsoft.com/en-us/library/dd318622(VS.85).aspx.
        Please see the sample demodshow.
    */
    // {E978EEA0-A0FF-465f-AB35-65907B8C62AC}
    DEFINE_GUID(IID_INncamStillImage, 0xe978eea0, 0xa0ff, 0x465f, 0xab, 0x35, 0x65, 0x90, 0x7b, 0x8c, 0x62, 0xac);

    DECLARE_INTERFACE_(INncamStillImage, IUnknown)
    {
        /*
            similar to put_Size, put_eSize
        */
        STDMETHOD(put_StillSize) (THIS_ int nWidth, int nHeight) PURE;
        STDMETHOD(get_StillSize) (THIS_ int* pWidth, int* pHeight) PURE;
        STDMETHOD(put_eStillSize) (THIS_ unsigned nResolutionIndex) PURE;
        STDMETHOD(get_eStillSize) (THIS_ unsigned* pIndex) PURE;                    
        STDMETHOD(get_StillResolutionNumber) (THIS_) PURE;                
        STDMETHOD(get_StillResolution) (THIS_ unsigned nResolutionIndex, int* pWidth, int* pHeight) PURE;
    };
#endif
    
#ifndef __INNCAMSERIALNUMBER_DEFINED__
#define __INNCAMSERIALNUMBER_DEFINED__
    // {E12D4B13-333F-4eae-BC89-0446D1FC634D}
    DEFINE_GUID(IID_INncamSerialNumber, 0xe12d4b13, 0x333f, 0x4eae, 0xbc, 0x89, 0x4, 0x46, 0xd1, 0xfc, 0x63, 0x4d);

    DECLARE_INTERFACE_(INncamSerialNumber, IUnknown)
    {
        /*
            get the serial number which is always 32 zero-terminated chars such as "TP110826145730ABCD1234FEDC56787"
        */
        STDMETHOD(get_SerialNumber) (THIS_ char sn[32]) PURE;
        /*
            get the model name such as "UCMOS03100KPA"
        */
        STDMETHOD(get_ModelName) (THIS_ char name[128]) PURE;
    };
#endif

#ifndef __INNCAMVERSION_DEFINED__
#define __INNCAMVERSION_DEFINED__

    // {FC69B0C7-6140-4FE7-B385-473E5EA87887}
    DEFINE_GUID(IID_INncamVersion, 0xfc69b0c7, 0x6140, 0x4fe7, 0xb3, 0x85, 0x47, 0x3e, 0x5e, 0xa8, 0x78, 0x87);

    DECLARE_INTERFACE_(INncamVersion, IUnknown)
    {
        /*
            get the camera firmware version, such as: 3.2.1.20140922
        */
        STDMETHOD(get_FwVersion) (THIS_ char fwver[16]) PURE;
        /*
            get the camera hardware version, such as: 3.12
        */
        STDMETHOD(get_HwVersion) (THIS_ char hwver[16]) PURE;
        /*
            get the production date, such as: 20150327
        */
        STDMETHOD(get_ProductionDate) (THIS_ char pdate[10]) PURE;
        /*
            get FPGA version, such as: 1.13
        */
        STDMETHOD(get_FpgaVersion) (THIS_ char fpgaver[16]) PURE;
        
        /*
            get the revision
        */
        STDMETHOD(get_Revision) (THIS_ unsigned short* pRevision) PURE;
    };
#endif

#ifndef __INNCAMST4_DEFINED__
#define __INNCAMST4_DEFINED__

    /* Please see: ASCOM Platform Help ICameraV2 */
    // {29867037-78A9-432F-BF33-A3CFE0D6C9B3}
    DEFINE_GUID(IID_INncamST4, 0x29867037, 0x78a9, 0x432f, 0xbf, 0x33, 0xa3, 0xcf, 0xe0, 0xd6, 0xc9, 0xb3);

    DECLARE_INTERFACE_(INncamST4, IUnknown)
    {
        /* astronomy: for ST4 guide.
            nDirect: 0 = North, 1 = South, 2 = East, 3 = West, 4 = Stop
            nDuration: in milliseconds
        */
        STDMETHOD(PlusGuide) (THIS_ unsigned nDirect, unsigned nDuration) PURE;

        /* S_OK: yes */
        /* S_FALSE: no */
        STDMETHOD(IsPulseGuiding) (THIS_) PURE;
    };
#endif

#ifndef __INNCAMINDEX_DEFINED__
#define __INNCAMINDEX_DEFINED__

    // {F670E70F-FDD0-4131-BAF7-E7F6C3EB66CF}
    DEFINE_GUID(IID_INncamIndex, 0xf670e70f, 0xfdd0, 0x4131, 0xba, 0xf7, 0xe7, 0xf6, 0xc3, 0xeb, 0x66, 0xcf);

    DECLARE_INTERFACE_(INncamIndex, IUnknown)
    {
        STDMETHOD(get_Index) (THIS_ unsigned* pIndex) PURE;
        STDMETHOD(put_Index) (THIS_ unsigned nIndex) PURE;
    };
#endif

#if 0
/* return value: the number of connected camera */
unsigned __stdcall DshowEnumCamera();

/* return value: camera model name */
const wchar_t* __stdcall DshowGetModelName(unsigned index);

/* return value: the camera directshow COM object, which can be used to QueryInterface(IID_IBaseFilter, ...). When failed, NULL is returned */
/* use OpenCamera(0) to open the first camera, use OpenCamera(1) to open the second camera, etc */
IUnknown* __stdcall DshowOpenCamera(unsigned index);
#endif

#endif
