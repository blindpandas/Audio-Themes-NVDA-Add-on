import ctypes
import ctypes.util
import os.path
import os
import sys

# It is important that we don't use the platform module because it does not exist inside NVDA.
if sys.platform == "win32":
    # this is a windows hack.
    # we want it to find out libsndfile before the system one in frozen executables, so we do this.
    # If it fails, we fall back to the system.
    # this latter point is what makes NVDA add-ons work right: they use the preloading a dll trick on Windows.
    if hasattr(sys, "frozen"):
        try:
            path = os.path.join(
                os.path.abspath(os.path.dirname(sys.executable)), "libaudioverse"
            )
            libsndfile_module = ctypes.cdll.LoadLibrary(
                os.path.join(path, "libsndfile-1.dll")
            )
            libaudioverse_module = ctypes.cdll.LoadLibrary(
                os.path.join(path, "libaudioverse.dll")
            )
        except:
            libsndfile_module = ctypes.cdll.LoadLibrary(
                os.path.join(
                    os.path.abspath(os.path.dirname(__file__)), "libsndfile-1.dll"
                )
            )
            libaudioverse_module = ctypes.cdll.LoadLibrary(
                os.path.join(
                    os.path.abspath(os.path.dirname(__file__)), "libaudioverse.dll"
                )
            )
    else:
        libsndfile_module = ctypes.cdll.LoadLibrary(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "libsndfile-1.dll")
        )
        libaudioverse_module = ctypes.cdll.LoadLibrary(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "libaudioverse.dll"
            )
        )
else:
    libaudioverse_name = ctypes.util.find_library("libaudioverse")
    try:
        libaudioverse_module = ctypes.cdll.LoadLibrary(libaudioverse_name)
    except:
        # Assume it's in /usr/local and try that.
        libaudioverse_module = ctypes.cdll.LoadLibrary(
            "/usr/local/lib/" + libaudioverse_name
        )

Lav_ERROR_NONE = 0
Lav_ERROR_UNKNOWN = 1
Lav_ERROR_TYPE_MISMATCH = 2
Lav_ERROR_INVALID_PROPERTY = 3
Lav_ERROR_NULL_POINTER = 4
Lav_ERROR_MEMORY = 5
Lav_ERROR_INVALID_POINTER = 6
Lav_ERROR_INVALID_HANDLE = 7
Lav_ERROR_RANGE = 8
Lav_ERROR_CANNOT_INIT_AUDIO = 9
Lav_ERROR_NO_SUCH_DEVICE = 10
Lav_ERROR_FILE = 11
Lav_ERROR_FILE_NOT_FOUND = 12
Lav_ERROR_HRTF_INVALID = 13
Lav_ERROR_CANNOT_CROSS_SIMULATIONS = 14
Lav_ERROR_CAUSES_CYCLE = 15
Lav_ERROR_PROPERTY_IS_READ_ONLY = 16
Lav_ERROR_OVERLAPPING_AUTOMATORS = 17
Lav_ERROR_CANNOT_CONNECT_TO_PROPERTY = 18
Lav_ERROR_BUFFER_IN_USE = 19
Lav_ERROR_INTERNAL = 999
Lav_PROPERTYTYPE_INT = 0
Lav_PROPERTYTYPE_FLOAT = 1
Lav_PROPERTYTYPE_DOUBLE = 2
Lav_PROPERTYTYPE_STRING = 3
Lav_PROPERTYTYPE_FLOAT3 = 4
Lav_PROPERTYTYPE_FLOAT6 = 5
Lav_PROPERTYTYPE_FLOAT_ARRAY = 6
Lav_PROPERTYTYPE_INT_ARRAY = 7
Lav_PROPERTYTYPE_BUFFER = 8
Lav_OBJTYPE_SIMULATION = 0
Lav_OBJTYPE_BUFFER = 1
Lav_OBJTYPE_GENERIC_NODE = 2
Lav_OBJTYPE_ENVIRONMENT_NODE = 3
Lav_OBJTYPE_SOURCE_NODE = 4
Lav_OBJTYPE_HRTF_NODE = 5
Lav_OBJTYPE_SINE_NODE = 6
Lav_OBJTYPE_HARD_LIMITER_NODE = 7
Lav_OBJTYPE_CROSSFADING_DELAY_NODE = 8
Lav_OBJTYPE_DOPPLERING_DELAY_NODE = 9
Lav_OBJTYPE_AMPLITUDE_PANNER_NODE = 10
Lav_OBJTYPE_PUSH_NODE = 11
Lav_OBJTYPE_BIQUAD_NODE = 12
Lav_OBJTYPE_PULL_NODE = 13
Lav_OBJTYPE_GRAPH_LISTENER_NODE = 14
Lav_OBJTYPE_CUSTOM_NODE = 15
Lav_OBJTYPE_RINGMOD_NODE = 16
Lav_OBJTYPE_MULTIPANNER_NODE = 17
Lav_OBJTYPE_FEEDBACK_DELAY_NETWORK_NODE = 18
Lav_OBJTYPE_ADDITIVE_SQUARE_NODE = 19
Lav_OBJTYPE_ADDITIVE_TRIANGLE_NODE = 20
Lav_OBJTYPE_ADDITIVE_SAW_NODE = 21
Lav_OBJTYPE_NOISE_NODE = 22
Lav_OBJTYPE_IIR_NODE = 23
Lav_OBJTYPE_GAIN_NODE = 24
Lav_OBJTYPE_CHANNEL_SPLITTER_NODE = 25
Lav_OBJTYPE_CHANNEL_MERGER_NODE = 26
Lav_OBJTYPE_BUFFER_NODE = 27
Lav_OBJTYPE_BUFFER_TIMELINE_NODE = 28
Lav_OBJTYPE_RECORDER_NODE = 29
Lav_OBJTYPE_CONVOLVER_NODE = 30
Lav_OBJTYPE_FFT_CONVOLVER_NODE = 31
Lav_OBJTYPE_THREE_BAND_EQ_NODE = 32
Lav_OBJTYPE_FILTERED_DELAY_NODE = 33
Lav_OBJTYPE_CROSSFADER_NODE = 34
Lav_OBJTYPE_ONE_POLE_FILTER_NODE = 35
Lav_OBJTYPE_FIRST_ORDER_FILTER_NODE = 36
Lav_OBJTYPE_ALLPASS_NODE = 37
Lav_OBJTYPE_NESTED_ALLPASS_NETWORK_NODE = 38
Lav_OBJTYPE_FDN_REVERB_NODE = 39
Lav_OBJTYPE_BLIT_NODE = 40
Lav_OBJTYPE_DC_BLOCKER_NODE = 41
Lav_OBJTYPE_LEAKY_INTEGRATOR_NODE = 42
Lav_OBJTYPE_FILE_STREAMER_NODE = 43
Lav_NODESTATE_PAUSED = 0
Lav_NODESTATE_PLAYING = 1
Lav_NODESTATE_ALWAYS_PLAYING = 2
Lav_LOGGING_LEVEL_CRITICAL = 10
Lav_LOGGING_LEVEL_INFO = 20
Lav_LOGGING_LEVEL_DEBUG = 30
Lav_LOGGING_LEVEL_OFF = 40
Lav_NODE_STATE = -100
Lav_NODE_MUL = -101
Lav_NODE_ADD = -102
Lav_NODE_CHANNEL_INTERPRETATION = -104
Lav_CHANNEL_INTERPRETATION_DISCRETE = 0
Lav_CHANNEL_INTERPRETATION_SPEAKERS = 1
Lav_OSCILLATOR_FREQUENCY = -200
Lav_OSCILLATOR_PHASE = -201
Lav_OSCILLATOR_FREQUENCY_MULTIPLIER = -202
Lav_SQUARE_HARMONICS = -1
Lav_SQUARE_DUTY_CYCLE = -2
Lav_TRIANGLE_HARMONICS = -3
Lav_SAW_HARMONICS = -3
Lav_NOISE_NOISE_TYPE = -1
Lav_NOISE_SHOULD_NORMALIZE = -2
Lav_NOISE_TYPE_WHITE = 0
Lav_NOISE_TYPE_PINK = 1
Lav_NOISE_TYPE_BROWN = 2
Lav_PANNER_AZIMUTH = -1
Lav_PANNER_ELEVATION = -2
Lav_PANNER_CHANNEL_MAP = -3
Lav_PANNER_SHOULD_CROSSFADE = -4
Lav_PANNER_STRATEGY = -5
Lav_PANNER_BANK_SPREAD = -20
Lav_PANNER_BANK_COUNT = -21
Lav_PANNER_BANK_IS_CENTERED = -22
Lav_PANNING_STRATEGY_DELEGATE = 0
Lav_PANNING_STRATEGY_HRTF = 1
Lav_PANNING_STRATEGY_STEREO = 2
Lav_PANNING_STRATEGY_SURROUND40 = 3
Lav_PANNING_STRATEGY_SURROUND51 = 4
Lav_PANNING_STRATEGY_SURROUND71 = 5
Lav_MIXER_MAX_PARENTS = -1
Lav_MIXER_INPUTS_PER_PARENT = -2
Lav_DELAY_DELAY = -1
Lav_DELAY_DELAY_MAX = -2
Lav_DELAY_FEEDBACK = -3
Lav_DELAY_INTERPOLATION_TIME = -4
Lav_PUSH_THRESHOLD = -1
Lav_BIQUAD_FILTER_TYPE = -1
Lav_BIQUAD_Q = -2
Lav_BIQUAD_FREQUENCY = -3
Lav_BIQUAD_DBGAIN = -4
Lav_BIQUAD_TYPE_LOWPASS = 0
Lav_BIQUAD_TYPE_HIGHPASS = 1
Lav_BIQUAD_TYPE_BANDPASS = 2
Lav_BIQUAD_TYPE_NOTCH = 3
Lav_BIQUAD_TYPE_ALLPASS = 4
Lav_BIQUAD_TYPE_PEAKING = 5
Lav_BIQUAD_TYPE_LOWSHELF = 6
Lav_BIQUAD_TYPE_HIGHSHELF = 7
Lav_BIQUAD_TYPE_IDENTITY = 8
Lav_FDN_MAX_DELAY = -1
Lav_FDN_OUTPUT_GAINS = -2
Lav_FDN_DELAYS = -3
Lav_FDN_MATRIX = -4
Lav_FDN_FILTER_TYPES = -5
Lav_FDN_FILTER_FREQUENCIES = -6
Lav_FDN_FILTER_TYPE_DISABLED = 0
Lav_FDN_FILTER_TYPE_LOWPASS = 1
Lav_FDN_FILTER_TYPE_HIGHPASS = 2
Lav_BUFFER_BUFFER = -1
Lav_BUFFER_POSITION = -2
Lav_BUFFER_RATE = -3
Lav_BUFFER_LOOPING = -4
Lav_BUFFER_ENDED_COUNT = -5
Lav_CONVOLVER_IMPULSE_RESPONSE = -1
Lav_THREE_BAND_EQ_HIGHBAND_DBGAIN = -1
Lav_THREE_BAND_EQ_HIGHBAND_FREQUENCY = -2
Lav_THREE_BAND_EQ_MIDBAND_DBGAIN = -3
Lav_THREE_BAND_EQ_LOWBAND_DBGAIN = -4
Lav_THREE_BAND_EQ_LOWBAND_FREQUENCY = -5
Lav_FILTERED_DELAY_DELAY = -1
Lav_FILTERED_DELAY_FEEDBACK = -2
Lav_FILTERED_DELAY_INTERPOLATION_TIME = -3
Lav_FILTERED_DELAY_DELAY_MAX = -4
Lav_FILTERED_DELAY_FILTER_TYPE = -5
Lav_FILTERED_DELAY_Q = -6
Lav_FILTERED_DELAY_FREQUENCY = -7
Lav_FILTERED_DELAY_DBGAIN = -8
Lav_CROSSFADER_CURRENT_INPUT = -1
Lav_CROSSFADER_TARGET_INPUT = -2
Lav_CROSSFADER_IS_CROSSFADING = -3
Lav_ONE_POLE_FILTER_FREQUENCY = -1
Lav_ONE_POLE_FILTER_IS_HIGHPASS = -2
Lav_FIRST_ORDER_FILTER_POLE = -1
Lav_FIRST_ORDER_FILTER_ZERO = -2
Lav_ALLPASS_DELAY_SAMPLES = -1
Lav_ALLPASS_DELAY_SAMPLES_MAX = -2
Lav_ALLPASS_INTERPOLATION_TIME = -3
Lav_ALLPASS_COEFFICIENT = -4
Lav_FDN_REVERB_T60 = -1
Lav_FDN_REVERB_CUTOFF_FREQUENCY = -2
Lav_FDN_REVERB_DENSITY = -3
Lav_FDN_REVERB_DELAY_MODULATION_DEPTH = -4
Lav_FDN_REVERB_DELAY_MODULATION_FREQUENCY = -5
Lav_BLIT_HARMONICS = -1
Lav_BLIT_SHOULD_NORMALIZE = -4
Lav_LEAKY_INTEGRATOR_LEAKYNESS = -1
Lav_FILE_STREAMER_POSITION = -1
Lav_FILE_STREAMER_LOOPING = -2
Lav_FILE_STREAMER_ENDED = -3
Lav_3D_ORIENTATION = -1
Lav_3D_POSITION = -2
Lav_ENVIRONMENT_PANNING_STRATEGY = -8
Lav_ENVIRONMENT_DISTANCE_MODEL = -11
Lav_ENVIRONMENT_DEFAULT_MAX_DISTANCE = -12
Lav_ENVIRONMENT_DEFAULT_SIZE = -13
Lav_ENVIRONMENT_OUTPUT_CHANNELS = -14
Lav_ENVIRONMENT_DEFAULT_REVERB_DISTANCE = -15
Lav_SOURCE_MAX_DISTANCE = -3
Lav_SOURCE_DISTANCE_MODEL = -4
Lav_SOURCE_SIZE = -5
Lav_SOURCE_REVERB_DISTANCE = -6
Lav_SOURCE_PANNING_STRATEGY = -8
Lav_SOURCE_HEAD_RELATIVE = -9
Lav_SOURCE_MIN_REVERB_LEVEL = -10
Lav_SOURCE_MAX_REVERB_LEVEL = -11
Lav_SOURCE_OCCLUSION = -12
Lav_DISTANCE_MODEL_DELEGATE = 0
Lav_DISTANCE_MODEL_LINEAR = 1
Lav_DISTANCE_MODEL_EXPONENTIAL = 2
Lav_DISTANCE_MODEL_INVERSE_SQUARE = 3

LavError = ctypes.c_int
LavHandle = ctypes.c_int
LavParameterlessCallback = ctypes.CFUNCTYPE(None, LavHandle, ctypes.c_void_p)
LavTimeCallback = ctypes.CFUNCTYPE(None, LavHandle, ctypes.c_double, ctypes.c_void_p)
LavLoggingCallback = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p)
LavHandleDestroyedCallback = ctypes.CFUNCTYPE(None, LavHandle)
LavPullNodeAudioCallback = ctypes.CFUNCTYPE(
    None,
    LavHandle,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
)
LavGraphListenerNodeListeningCallback = ctypes.CFUNCTYPE(
    None,
    LavHandle,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_void_p,
)
LavCustomNodeProcessingCallback = ctypes.CFUNCTYPE(
    None,
    LavHandle,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
    ctypes.c_void_p,
)

Lav_initialize = ctypes.CFUNCTYPE(LavError)(("Lav_initialize", libaudioverse_module))
Lav_shutdown = ctypes.CFUNCTYPE(LavError)(("Lav_shutdown", libaudioverse_module))
Lav_isInitialized = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_int))(
    ("Lav_isInitialized", libaudioverse_module)
)
Lav_errorGetMessage = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_char_p))(
    ("Lav_errorGetMessage", libaudioverse_module)
)
Lav_errorGetFile = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_char_p))(
    ("Lav_errorGetFile", libaudioverse_module)
)
Lav_errorGetLine = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_int))(
    ("Lav_errorGetLine", libaudioverse_module)
)
Lav_free = ctypes.CFUNCTYPE(LavError, ctypes.c_void_p)(
    ("Lav_free", libaudioverse_module)
)
Lav_handleIncRef = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_handleIncRef", libaudioverse_module)
)
Lav_handleDecRef = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_handleDecRef", libaudioverse_module)
)
Lav_handleGetAndClearFirstAccess = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_handleGetAndClearFirstAccess", libaudioverse_module))
Lav_handleGetRefCount = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_handleGetRefCount", libaudioverse_module))
Lav_handleGetType = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(ctypes.c_int))(
    ("Lav_handleGetType", libaudioverse_module)
)
Lav_setLoggingCallback = ctypes.CFUNCTYPE(LavError, LavLoggingCallback)(
    ("Lav_setLoggingCallback", libaudioverse_module)
)
Lav_getLoggingCallback = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(LavLoggingCallback))(
    ("Lav_getLoggingCallback", libaudioverse_module)
)
Lav_setLoggingLevel = ctypes.CFUNCTYPE(LavError, ctypes.c_int)(
    ("Lav_setLoggingLevel", libaudioverse_module)
)
Lav_getLoggingLevel = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_int))(
    ("Lav_getLoggingLevel", libaudioverse_module)
)
Lav_setHandleDestroyedCallback = ctypes.CFUNCTYPE(LavError, LavHandleDestroyedCallback)(
    ("Lav_setHandleDestroyedCallback", libaudioverse_module)
)
Lav_deviceGetCount = ctypes.CFUNCTYPE(LavError, ctypes.POINTER(ctypes.c_uint))(
    ("Lav_deviceGetCount", libaudioverse_module)
)
Lav_deviceGetName = ctypes.CFUNCTYPE(
    LavError, ctypes.c_uint, ctypes.POINTER(ctypes.c_char_p)
)(("Lav_deviceGetName", libaudioverse_module))
Lav_deviceGetIdentifierString = ctypes.CFUNCTYPE(
    LavError, ctypes.c_uint, ctypes.POINTER(ctypes.c_char_p)
)(("Lav_deviceGetIdentifierString", libaudioverse_module))
Lav_deviceGetChannels = ctypes.CFUNCTYPE(
    LavError, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)
)(("Lav_deviceGetChannels", libaudioverse_module))
Lav_createSimulation = ctypes.CFUNCTYPE(
    LavError, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createSimulation", libaudioverse_module))
Lav_simulationGetBlockSize = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_simulationGetBlockSize", libaudioverse_module))
Lav_simulationGetBlock = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)
)(("Lav_simulationGetBlock", libaudioverse_module))
Lav_simulationGetSr = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_simulationGetSr", libaudioverse_module))
Lav_simulationSetOutputDevice = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.c_int
)(("Lav_simulationSetOutputDevice", libaudioverse_module))
Lav_simulationClearOutputDevice = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_simulationClearOutputDevice", libaudioverse_module)
)
Lav_simulationLock = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_simulationLock", libaudioverse_module)
)
Lav_simulationUnlock = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_simulationUnlock", libaudioverse_module)
)
Lav_simulationSetBlockCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavTimeCallback, ctypes.c_void_p
)(("Lav_simulationSetBlockCallback", libaudioverse_module))
Lav_simulationWriteFile = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_int
)(("Lav_simulationWriteFile", libaudioverse_module))
Lav_simulationSetThreads = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_int)(
    ("Lav_simulationSetThreads", libaudioverse_module)
)
Lav_simulationGetThreads = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_simulationGetThreads", libaudioverse_module))
Lav_simulationCallIn = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_double, ctypes.c_int, LavTimeCallback, ctypes.c_void_p
)(("Lav_simulationCallIn", libaudioverse_module))
Lav_createBuffer = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(LavHandle))(
    ("Lav_createBuffer", libaudioverse_module)
)
Lav_bufferGetSimulation = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_bufferGetSimulation", libaudioverse_module))
Lav_bufferLoadFromFile = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_char_p)(
    ("Lav_bufferLoadFromFile", libaudioverse_module)
)
Lav_bufferLoadFromArray = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
)(("Lav_bufferLoadFromArray", libaudioverse_module))
Lav_bufferNormalize = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_bufferNormalize", libaudioverse_module)
)
Lav_bufferGetDuration = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_float)
)(("Lav_bufferGetDuration", libaudioverse_module))
Lav_bufferGetLengthInSamples = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_int)
)(("Lav_bufferGetLengthInSamples", libaudioverse_module))
Lav_nodeGetSimulation = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_nodeGetSimulation", libaudioverse_module))
Lav_nodeConnect = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, LavHandle, ctypes.c_int
)(("Lav_nodeConnect", libaudioverse_module))
Lav_nodeConnectSimulation = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_int)(
    ("Lav_nodeConnectSimulation", libaudioverse_module)
)
Lav_nodeConnectProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, LavHandle, ctypes.c_int
)(("Lav_nodeConnectProperty", libaudioverse_module))
Lav_nodeDisconnect = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, LavHandle, ctypes.c_int
)(("Lav_nodeDisconnect", libaudioverse_module))
Lav_nodeIsolate = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_nodeIsolate", libaudioverse_module)
)
Lav_nodeGetInputConnectionCount = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_uint)
)(("Lav_nodeGetInputConnectionCount", libaudioverse_module))
Lav_nodeGetOutputConnectionCount = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(ctypes.c_uint)
)(("Lav_nodeGetOutputConnectionCount", libaudioverse_module))
Lav_nodeResetProperty = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_int)(
    ("Lav_nodeResetProperty", libaudioverse_module)
)
Lav_nodeSetIntProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_int
)(("Lav_nodeSetIntProperty", libaudioverse_module))
Lav_nodeSetFloatProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_float
)(("Lav_nodeSetFloatProperty", libaudioverse_module))
Lav_nodeSetDoubleProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_double
)(("Lav_nodeSetDoubleProperty", libaudioverse_module))
Lav_nodeSetStringProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_char_p
)(("Lav_nodeSetStringProperty", libaudioverse_module))
Lav_nodeSetFloat3Property = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float
)(("Lav_nodeSetFloat3Property", libaudioverse_module))
Lav_nodeSetFloat6Property = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
)(("Lav_nodeSetFloat6Property", libaudioverse_module))
Lav_nodeGetIntProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeGetIntProperty", libaudioverse_module))
Lav_nodeGetFloatProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_float)
)(("Lav_nodeGetFloatProperty", libaudioverse_module))
Lav_nodeGetDoubleProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_double)
)(("Lav_nodeGetDoubleProperty", libaudioverse_module))
Lav_nodeGetStringProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)
)(("Lav_nodeGetStringProperty", libaudioverse_module))
Lav_nodeGetFloat3Property = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
)(("Lav_nodeGetFloat3Property", libaudioverse_module))
Lav_nodeGetFloat6Property = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
)(("Lav_nodeGetFloat6Property", libaudioverse_module))
Lav_nodeGetIntPropertyRange = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
)(("Lav_nodeGetIntPropertyRange", libaudioverse_module))
Lav_nodeGetFloatPropertyRange = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
)(("Lav_nodeGetFloatPropertyRange", libaudioverse_module))
Lav_nodeGetDoublePropertyRange = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
)(("Lav_nodeGetDoublePropertyRange", libaudioverse_module))
Lav_nodeGetPropertyName = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)
)(("Lav_nodeGetPropertyName", libaudioverse_module))
Lav_nodeGetPropertyType = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeGetPropertyType", libaudioverse_module))
Lav_nodeGetPropertyHasDynamicRange = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeGetPropertyHasDynamicRange", libaudioverse_module))
Lav_nodeReplaceFloatArrayProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)
)(("Lav_nodeReplaceFloatArrayProperty", libaudioverse_module))
Lav_nodeReadFloatArrayProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)
)(("Lav_nodeReadFloatArrayProperty", libaudioverse_module))
Lav_nodeWriteFloatArrayProperty = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_float),
)(("Lav_nodeWriteFloatArrayProperty", libaudioverse_module))
Lav_nodeGetFloatArrayPropertyLength = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)
)(("Lav_nodeGetFloatArrayPropertyLength", libaudioverse_module))
Lav_nodeReplaceIntArrayProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeReplaceIntArrayProperty", libaudioverse_module))
Lav_nodeReadIntArrayProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeReadIntArrayProperty", libaudioverse_module))
Lav_nodeWriteIntArrayProperty = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_int),
)(("Lav_nodeWriteIntArrayProperty", libaudioverse_module))
Lav_nodeGetIntArrayPropertyLength = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
)(("Lav_nodeGetIntArrayPropertyLength", libaudioverse_module))
Lav_nodeGetArrayPropertyLengthRange = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ctypes.c_uint),
)(("Lav_nodeGetArrayPropertyLengthRange", libaudioverse_module))
Lav_nodeSetBufferProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, LavHandle
)(("Lav_nodeSetBufferProperty", libaudioverse_module))
Lav_nodeGetBufferProperty = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_nodeGetBufferProperty", libaudioverse_module))
Lav_automationCancelAutomators = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_double
)(("Lav_automationCancelAutomators", libaudioverse_module))
Lav_automationLinearRampToValue = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_double, ctypes.c_double
)(("Lav_automationLinearRampToValue", libaudioverse_module))
Lav_automationSet = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_double, ctypes.c_double
)(("Lav_automationSet", libaudioverse_module))
Lav_automationEnvelope = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
)(("Lav_automationEnvelope", libaudioverse_module))
Lav_nodeReset = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_nodeReset", libaudioverse_module)
)
Lav_createSineNode = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(LavHandle))(
    ("Lav_createSineNode", libaudioverse_module)
)
Lav_createAdditiveSquareNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createAdditiveSquareNode", libaudioverse_module))
Lav_createAdditiveTriangleNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createAdditiveTriangleNode", libaudioverse_module))
Lav_createAdditiveSawNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createAdditiveSawNode", libaudioverse_module))
Lav_createNoiseNode = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(LavHandle))(
    ("Lav_createNoiseNode", libaudioverse_module)
)
Lav_createHrtfNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.POINTER(LavHandle)
)(("Lav_createHrtfNode", libaudioverse_module))
Lav_createHardLimiterNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createHardLimiterNode", libaudioverse_module))
Lav_createCrossfadingDelayNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createCrossfadingDelayNode", libaudioverse_module))
Lav_createDoppleringDelayNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createDoppleringDelayNode", libaudioverse_module))
Lav_createAmplitudePannerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createAmplitudePannerNode", libaudioverse_module))
Lav_amplitudePannerNodeConfigureStandardMap = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint
)(("Lav_amplitudePannerNodeConfigureStandardMap", libaudioverse_module))
Lav_createMultipannerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.POINTER(LavHandle)
)(("Lav_createMultipannerNode", libaudioverse_module))
Lav_createPushNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createPushNode", libaudioverse_module))
Lav_pushNodeFeed = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)
)(("Lav_pushNodeFeed", libaudioverse_module))
Lav_pushNodeSetLowCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavParameterlessCallback, ctypes.c_void_p
)(("Lav_pushNodeSetLowCallback", libaudioverse_module))
Lav_pushNodeSetUnderrunCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavParameterlessCallback, ctypes.c_void_p
)(("Lav_pushNodeSetUnderrunCallback", libaudioverse_module))
Lav_createBiquadNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createBiquadNode", libaudioverse_module))
Lav_createPullNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createPullNode", libaudioverse_module))
Lav_pullNodeSetAudioCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavPullNodeAudioCallback, ctypes.c_void_p
)(("Lav_pullNodeSetAudioCallback", libaudioverse_module))
Lav_createGraphListenerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createGraphListenerNode", libaudioverse_module))
Lav_graphListenerNodeSetListeningCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavGraphListenerNodeListeningCallback, ctypes.c_void_p
)(("Lav_graphListenerNodeSetListeningCallback", libaudioverse_module))
Lav_createCustomNode = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(LavHandle),
)(("Lav_createCustomNode", libaudioverse_module))
Lav_customNodeSetProcessingCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavCustomNodeProcessingCallback, ctypes.c_void_p
)(("Lav_customNodeSetProcessingCallback", libaudioverse_module))
Lav_createRingmodNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createRingmodNode", libaudioverse_module))
Lav_createFeedbackDelayNetworkNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createFeedbackDelayNetworkNode", libaudioverse_module))
Lav_createIirNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createIirNode", libaudioverse_module))
Lav_iirNodeSetCoefficients = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
)(("Lav_iirNodeSetCoefficients", libaudioverse_module))
Lav_createGainNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createGainNode", libaudioverse_module))
Lav_createChannelSplitterNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createChannelSplitterNode", libaudioverse_module))
Lav_createChannelMergerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createChannelMergerNode", libaudioverse_module))
Lav_createBufferNode = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(LavHandle))(
    ("Lav_createBufferNode", libaudioverse_module)
)
Lav_bufferNodeSetEndCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavParameterlessCallback, ctypes.c_void_p
)(("Lav_bufferNodeSetEndCallback", libaudioverse_module))
Lav_createBufferTimelineNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createBufferTimelineNode", libaudioverse_module))
Lav_bufferTimelineNodeScheduleBuffer = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavHandle, ctypes.c_double, ctypes.c_float
)(("Lav_bufferTimelineNodeScheduleBuffer", libaudioverse_module))
Lav_createRecorderNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createRecorderNode", libaudioverse_module))
Lav_recorderNodeStartRecording = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_char_p)(
    ("Lav_recorderNodeStartRecording", libaudioverse_module)
)
Lav_recorderNodeStopRecording = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_recorderNodeStopRecording", libaudioverse_module)
)
Lav_createConvolverNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createConvolverNode", libaudioverse_module))
Lav_createFftConvolverNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createFftConvolverNode", libaudioverse_module))
Lav_fftConvolverNodeSetResponse = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)
)(("Lav_fftConvolverNodeSetResponse", libaudioverse_module))
Lav_fftConvolverNodeSetResponseFromFile = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.c_int, ctypes.c_int
)(("Lav_fftConvolverNodeSetResponseFromFile", libaudioverse_module))
Lav_createThreeBandEqNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createThreeBandEqNode", libaudioverse_module))
Lav_createFilteredDelayNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_uint, ctypes.POINTER(LavHandle)
)(("Lav_createFilteredDelayNode", libaudioverse_module))
Lav_createCrossfaderNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createCrossfaderNode", libaudioverse_module))
Lav_crossfaderNodeCrossfade = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_int
)(("Lav_crossfaderNodeCrossfade", libaudioverse_module))
Lav_crossfaderNodeSetFinishedCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavParameterlessCallback, ctypes.c_void_p
)(("Lav_crossfaderNodeSetFinishedCallback", libaudioverse_module))
Lav_createOnePoleFilterNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createOnePoleFilterNode", libaudioverse_module))
Lav_createFirstOrderFilterNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createFirstOrderFilterNode", libaudioverse_module))
Lav_firstOrderFilterNodeConfigureLowpass = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float
)(("Lav_firstOrderFilterNodeConfigureLowpass", libaudioverse_module))
Lav_firstOrderFilterNodeConfigureHighpass = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float
)(("Lav_firstOrderFilterNodeConfigureHighpass", libaudioverse_module))
Lav_firstOrderFilterNodeConfigureAllpass = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float
)(("Lav_firstOrderFilterNodeConfigureAllpass", libaudioverse_module))
Lav_createAllpassNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createAllpassNode", libaudioverse_module))
Lav_createNestedAllpassNetworkNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createNestedAllpassNetworkNode", libaudioverse_module))
Lav_nestedAllpassNetworkNodeBeginNesting = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_float
)(("Lav_nestedAllpassNetworkNodeBeginNesting", libaudioverse_module))
Lav_nestedAllpassNetworkNodeEndNesting = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_nestedAllpassNetworkNodeEndNesting", libaudioverse_module)
)
Lav_nestedAllpassNetworkNodeAppendAllpass = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_float
)(("Lav_nestedAllpassNetworkNodeAppendAllpass", libaudioverse_module))
Lav_nestedAllpassNetworkNodeAppendOnePole = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float, ctypes.c_int
)(("Lav_nestedAllpassNetworkNodeAppendOnePole", libaudioverse_module))
Lav_nestedAllpassNetworkNodeAppendBiquad = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double
)(("Lav_nestedAllpassNetworkNodeAppendBiquad", libaudioverse_module))
Lav_nestedAllpassNetworkNodeAppendReader = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_float
)(("Lav_nestedAllpassNetworkNodeAppendReader", libaudioverse_module))
Lav_nestedAllpassNetworkNodeCompile = ctypes.CFUNCTYPE(LavError, LavHandle)(
    ("Lav_nestedAllpassNetworkNodeCompile", libaudioverse_module)
)
Lav_createFdnReverbNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createFdnReverbNode", libaudioverse_module))
Lav_createBlitNode = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.POINTER(LavHandle))(
    ("Lav_createBlitNode", libaudioverse_module)
)
Lav_createDcBlockerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createDcBlockerNode", libaudioverse_module))
Lav_createLeakyIntegratorNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_int, ctypes.POINTER(LavHandle)
)(("Lav_createLeakyIntegratorNode", libaudioverse_module))
Lav_createFileStreamerNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.POINTER(LavHandle)
)(("Lav_createFileStreamerNode", libaudioverse_module))
Lav_fileStreamerNodeSetEndCallback = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavParameterlessCallback, ctypes.c_void_p
)(("Lav_fileStreamerNodeSetEndCallback", libaudioverse_module))
Lav_createEnvironmentNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, ctypes.c_char_p, ctypes.POINTER(LavHandle)
)(("Lav_createEnvironmentNode", libaudioverse_module))
Lav_environmentNodePlayAsync = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    LavHandle,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_int,
)(("Lav_environmentNodePlayAsync", libaudioverse_module))
Lav_environmentNodeAddEffectSend = ctypes.CFUNCTYPE(
    LavError,
    LavHandle,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
)(("Lav_environmentNodeAddEffectSend", libaudioverse_module))
Lav_createSourceNode = ctypes.CFUNCTYPE(
    LavError, LavHandle, LavHandle, ctypes.POINTER(LavHandle)
)(("Lav_createSourceNode", libaudioverse_module))
Lav_sourceNodeFeedEffect = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_int)(
    ("Lav_sourceNodeFeedEffect", libaudioverse_module)
)
Lav_sourceNodeStopFeedingEffect = ctypes.CFUNCTYPE(LavError, LavHandle, ctypes.c_int)(
    ("Lav_sourceNodeStopFeedingEffect", libaudioverse_module)
)
