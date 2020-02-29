#ifndef __imagelib_h__
#define __imagelib_h__

#ifdef IMAGELIB_EXPORTS
#define _imagelib_port_(r) __declspec(dllexport) r __cdecl
#else
#define _imagelib_port_(r) __declspec(dllimport) r __cdecl
#pragma comment(lib, "imagelib.lib")
#endif

#pragma pack(push, 4)
#ifdef __cplusplus
extern "C"{
#endif

#define IL_MERIT_ZERO           0
#define IL_MERIT_NONE           1
#define IL_MERIT_LOW            16
#define IL_MERIT_NORMAL         64
#define IL_MERIT_HIGH           128
#define IL_MERTI_MAX            255
    
#define GIFCODEC_LZW            0
#define GIFCODEC_RLE            1
#define GIFCODEC_NONE           2

#define DCMCODEC_LOSSLESS_JPEG  0
#define DCMCODEC_RLE            1
#define DCMCODEC_NONE           2

#define DNGCODEC_LOSSLESS       0
#define DNGCODEC_NONE           1

enum IMAGEFORMAT{
    IMAGEFORMAT_UNKNOWN,
    IMAGEFORMAT_BMP,
    IMAGEFORMAT_JPG,
    IMAGEFORMAT_PNG,
    IMAGEFORMAT_TIF,
    IMAGEFORMAT_GIF,
    IMAGEFORMAT_PCX,
    IMAGEFORMAT_TGA,
    IMAGEFORMAT_PSD,
    IMAGEFORMAT_ICO,
    IMAGEFORMAT_EMF,
    IMAGEFORMAT_WMF,
    IMAGEFORMAT_JBG,
    IMAGEFORMAT_WBMP,
    IMAGEFORMAT_JP2,
    IMAGEFORMAT_J2K,
    IMAGEFORMAT_DCM,
    IMAGEFORMAT_DNG,
    IMAGEFORMAT_WEBP,
    IMAGEFORMAT_SVS,
    IMAGEFORMAT_MAX
};

typedef struct{
    wchar_t*    ext;    //file name extension,such as jpg,bmp,tif,gif
    DWORD       fmt;    //image format
}ExtFmt;

typedef struct{
    DWORD        fmt;    //image format
    BYTE         code;   //this codec support compression?
    BYTE         decode; //this codec support decompression?
    wchar_t*     name;   //codec name
    DWORD        codec;  //codec
}FmtCodec;

typedef struct{
    DWORD        fmt;    //image format
    wchar_t*     ext;
    wchar_t*     abbr;   //abbr. for format's name
    wchar_t*     name;   //image format's name
    BYTE         merit;  //it's merit, [0, 255], see IL_MERIT_*
    struct{
        unsigned bpp1: 1;
        unsigned bpp4: 1;
        unsigned bpp8: 1;
        unsigned bpp16: 1;
        unsigned bpp24: 1;
        unsigned bpp32: 1;
        unsigned gray: 1;
        unsigned multipage: 1;
        unsigned motion: 1;
        unsigned exif: 1; // support exif
    }cap;
}FmtInfo;

typedef struct{
    DWORD               iType;              //original image format
    DWORD               iCodec;             //to tiff: see s_codec
                                            //to gif: LZW(default), RLE, NONE
                                            //to dng: 0->compress, 1->none
    BYTE                bAppend;            //used for TIFF, GIF: append file? TRUE or FALSE
    BYTE                bInterlaced;        //used for PNG, GIF, TRUE or FALSE
    BYTE                bPreview;           //decoding this image for previewing, so sometimes we may decode it with low quality, TRUE or FALSE
    BYTE                nQuality;           //used for saving JPEG & JP2000, 0..100
    BYTE                nSmoothing;         //used for saving JPEG & JP2000: 0..100
    BYTE                bProgressive;       //used for JPEG: is it a progressive jpeg? TRUE or FALSE
    BYTE                bOptimize;          //used for saving JPEG: optimize entropy encoding? TRUE or FALSE
    LONG                nPage;              //used for TIF, GIF, ICO : actual page
    LONG                nPages;             //used for TIF, GIF, ICO : total number of pages
    DWORD               nDelay;             //used for GIF: (100ms)
    BYTE                bOpenFile;          //open file
    double              dPPM;
    int                 ExpoTimeA;          // expo time
    int                 ExpoTimeB;
    int                 latitude;
    int                 longitude;
    void*               extTag;
    DWORD               extTagLen;
    unsigned long long  timestamp;          // timestamp in microseconds, 0 or -1 means NA
	BYTE				bImageUniqueID;
    char                cDateTimeOrg[24];
    char                cDateTimeDig[24];
    char                cCamera[32];
    char                cSN[32];
    char                cCopyright[256];
    char                cArtist[256];
    char                cComment[256];
    char                cDescription[256];
    wchar_t             cError[256];
}XIMAGEINFO;

_imagelib_port_(PBYTE) ImageLib_Open(const wchar_t* file, XIMAGEINFO* pInfo);
_imagelib_port_(PBYTE) ImageLib_OpenMemory(const PBYTE pData, size_t nLength, XIMAGEINFO* pInfo);
_imagelib_port_(void) ImageLib_Free(void* pDIB);
_imagelib_port_(BOOL) ImageLib_Save(const wchar_t* file, void* pDIB, XIMAGEINFO* pInfo);

_imagelib_port_(BOOL) ImageLib_CanSave(const void* pDIB, const XIMAGEINFO* pInfo);
_imagelib_port_(DWORD) ImageLib_GetExtFmt(const wchar_t* file);
_imagelib_port_(const FmtInfo*) ImageLib_FmtInfo();
_imagelib_port_(const ExtFmt*) ImageLib_ExtFmt();
_imagelib_port_(const FmtCodec*) ImageLib_Codec();
_imagelib_port_(const FmtInfo*) ImageLib_GetFmtInfo(DWORD iType);
_imagelib_port_(BOOL) ImageLib_SupportExif(DWORD iType);

#ifdef __cplusplus
}
#endif
#pragma pack(pop)
#endif