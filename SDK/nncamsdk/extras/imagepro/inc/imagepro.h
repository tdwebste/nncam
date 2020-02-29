#ifndef __imagepro_H__
#define __imagepro_H__

#ifdef _WIN32
#ifdef IMAGEPRO_EXPORTS
#define _imagepro_port_(r) __declspec(dllexport) r __cdecl
#else
#define _imagepro_port_(r) __declspec(dllimport) r __cdecl
#endif

#pragma pack(push, 8)
#else
#define __cdecl
#define _imagepro_port_(r) r
#endif

#ifdef __cplusplus
extern "C"
{
#endif

typedef void* (__cdecl *pfun_imagepro_malloc)(size_t); /* malloc(size) */
_imagepro_port_(void) imagepro_init(pfun_imagepro_malloc pfun);

enum eImageproStitchRet {
    eImageproStitchRet_EMPTY,
    eImageproStitchRet_NORMAL,
    eImageproStitchRet_NORMAL_REF
};

enum eImageproStitchQuality {
    eImageproStitchQ_ZERO,
    eImageproStitchQ_GOOD,
    eImageproStitchQ_CAUTION,
    eImageproStitchQ_BAD,
    eImageproStitchQ_WARNING
};

enum eImageproStitchStatus {
    eImageproStitchS_NONE,
    eImageproStitchS_NORMAL,
    eImageproStitchS_AREPAIR, //auto repair
    eImageproStitchS_MREPAIR, //manual repair 
    eImageproStitchS_RESET,
    eImageproStitchS_RESTART
};

enum eImageproStitchDirection {
    eImageproStitchD_STILL,
    eImageproStitchD_PLUS,
    eImageproStitchD_MINUS
};

enum eImageproStitchEvent {
    eImageproStitchE_NONE,
    eImageproStitchE_ERROR,
    eImageproStitchE_NOMEM,
    eImageproStitchE_EXPAND,
    eImageproStitchE_EXPAND_FAILURE,
    eImageproStitchE_EXPAND_SUCCESS,
    eImageproStitchE_ENTER_NORMAL,
    eImageproStitchE_ENTER_AREPAIR,
    eImageproStitchE_LEAVE_AREPAIR,
    eImageproStitchE_ENTER_MREPAIR,
    eImageproStitchE_LEAVE_MREPAIR,
    eImageproStitchE_ENTER_RESET,
    eImageproStitchE_LEAVE_RESET,
    eImageproStitchE_ENTER_RESTART,
    eImageproStitchE_LEAVE_RESTART,
    eImageproStitchE_AREPAIR_STOP_X,
    eImageproStitchE_AREPAIR_STOP_Y,
    eImageproStitchE_AREPAIR_KEEP_X,
    eImageproStitchE_AREPAIR_KEEP_Y,
    eImageproStitchE_AREPAIR_REVERSE_X,
    eImageproStitchE_AREPAIR_REVERSE_Y,
    eImageproStitchE_AREPAIR_RIGHT_DIR,
    eImageproStitchE_MREPAIR_START_MOVING,
    eImageproStitchE_MREPAIR_REF_FAILURE,
    eImageproStitchE_MREPAIR_RETRY,
    eImageproStitchE_RESTART_START
};

typedef void (__cdecl *IMAGEPRO_STITCH_CALLBACK)(void* ctx, void* outData, int stride, int outW, int outH, int curW, int curH, int curType,
                                        int posX, int posY, eImageproStitchQuality quality, float sharpness, bool bUpdate, bool bSize);
typedef void (__cdecl *IMAGEPRO_STITCH_ECALLBACK)(void* ctx, eImageproStitchEvent evt);

#ifdef _WIN32
typedef struct { int unused; } *HImageproStitch;
_imagepro_port_(HImageproStitch) imagepro_stitch_new(bool bGlobalShutter, int videoW, int videoH, IMAGEPRO_STITCH_CALLBACK pFun, IMAGEPRO_STITCH_ECALLBACK pEFun, void* ctx);
_imagepro_port_(void) imagepro_stitch_delete(HImageproStitch handle);
_imagepro_port_(void) imagepro_stitch_start(HImageproStitch handle);
_imagepro_port_(void*) imagepro_stitch_stop(HImageproStitch handle, bool normal, bool crop);
_imagepro_port_(void) imagepro_stitch_readdata(HImageproStitch handle, void* data, int w, int h, int roix = 0, int roiy = 0, int roiw = 0, int roih = 0);
_imagepro_port_(HRESULT) imagepro_stitch_pull(HImageproStitch handle, HToupCam h, bool bFeed, void* pImageData, int bits, int rowPitch, ToupcamFrameInfoV2* pInfo);
#endif

enum eImageproEdfMethod {
    eImageproEdfM_Pyr_Max,
    eImageproEdfM_Pyr_Weighted,
    eImageproEdfM_Stack,
    eImageproEdfM_SoftStack,
    eImageproEdfM_Pyr_Stack
};

enum eImageproEdfEvent {
    eImageproEdf_NONE,
    eImageproEdf_ERROR,
    eImageproEdf_NOMEM
};

enum eImageproEdfMode {
    eImageproEdf_Auto,
    eImageproEdf_Manual
};

typedef void (__cdecl *IMAGEPRO_EDF_CALLBACK)(void* ctx, int result, void* outData, int stride, int outW, int outH, int outType);
typedef void (__cdecl *IMAGEPRO_EDF_ECALLBACK)(void* ctx, eImageproEdfEvent evt);

#ifdef _WIN32
typedef struct { int unused; } *HImageproEdf;
_imagepro_port_(HImageproEdf) imagepro_edf_new(eImageproEdfMethod method, IMAGEPRO_EDF_CALLBACK pEdfFun, IMAGEPRO_EDF_ECALLBACK pEventFun, void* ctx);
_imagepro_port_(void) imagepro_edf_delete(HImageproEdf handle);
_imagepro_port_(void) imagepro_edf_start(HImageproEdf handle);
_imagepro_port_(void) imagepro_edf_stop(HImageproEdf handle);
_imagepro_port_(void) imagepro_edf_readdata(HImageproEdf handle, void* data, int stride);
_imagepro_port_(HRESULT) imagepro_edf_pull(HImageproEdf handle, HToupCam h, bool bFeed, void* pImageData, int bits, int rowPitch, ToupcamFrameInfoV2* pInfo);
#endif

#ifdef __cplusplus
}
#endif

#ifdef _WIN32
#pragma pack(pop)
#endif

#endif
