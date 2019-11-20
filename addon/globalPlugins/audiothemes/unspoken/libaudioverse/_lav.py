# implements lifting the raw ctypes-basedd api into something markedly pallatable.
# among other things, the implementation heree enables calling functions with keyword arguments and raises exceptions on error, rather than dealing with ctypes directly.
from __future__ import absolute_import
import ctypes
import collections.abc
import functools
from . import _libaudioverse
import six

# These are not from libaudioverse.
# Implement a method by which the public libaudioverse module may register its exception classes for error code translation.
class PythonBindingsCouldNotTranslateErrorCodeError(Exception):
    """An exception representing failure to translate a libaudioverse error code into a python exception.  If you see this, report it as a bug with Libaudioverse because something has gone very badly wrong."""

    pass


errors_to_exceptions = dict()


def bindings_register_exception(code, cls):
    errors_to_exceptions[code] = cls


def make_error_from_code(err):
    """Internal use.  Translates libaudioverse error codes into exceptions."""
    return errors_to_exceptions.get(
        err, PythonBindingsCouldNotTranslateErrorCodeError
    )()


# Handle marshalling and automatic refcount stuff:
@functools.total_ordering
class _HandleBox(object):
    def __init__(self, handle):
        self.handle = int(handle)
        first_access = ctypes.c_int()
        _libaudioverse.Lav_handleGetAndClearFirstAccess(
            handle, ctypes.byref(first_access)
        )
        if not first_access:
            _libaudioverse.Lav_handleIncRef(handle)

    def __eq__(self, other):
        if not isinstance(other, _HandleBox):
            return False
        else:
            return self.handle == other.handle

    def __lt__(self, other):
        if not isinstance(other, _HandleBox):
            return True  # other classes are "less" than us.
        return self.handle < other.handle

    def __hash__(self):
        return self.handle

    def __del__(self):
        # Guard against interpreter shutdown.
        if self.handle is None:
            return
        deleter = getattr(_libaudioverse, "Lav_handleDecRef", None)
        if deleter is not None:
            deleter(self.handle)
        self.handle = None


def reverse_handle(handle):
    return _HandleBox(handle)


def initialize():
    err = _libaudioverse.Lav_initialize()
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def shutdown():
    err = _libaudioverse.Lav_shutdown()
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def is_initialized():
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_isInitialized(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def error_get_message():
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_errorGetMessage(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def error_get_file():
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_errorGetFile(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def error_get_line():
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_errorGetLine(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def free(ptr):
    if isinstance(ptr, collections.abc.Sized):
        if not (isinstance(ptr, six.binary_type) or isinstance(ptr, six.text_type)):
            ptr_t = None * len(ptr)
            # Try to use the buffer interfaces, if we can.
            try:
                ptr = ptr_t.from_buffer(ptr)
            except TypeError:
                ptr_new = ptr_t()
                for i, j in enumerate(ptr):
                    ptr_new[i] = j
                ptr = ptr_new
        else:
            ptr = ctypes.cast(
                ctypes.create_string_buffer(ptr, len(ptr)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_free(ptr)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def handle_inc_ref(handle):
    handle = getattr(handle, "handle", handle)
    handle = getattr(handle, "handle", handle)
    err = _libaudioverse.Lav_handleIncRef(handle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def handle_dec_ref(handle):
    handle = getattr(handle, "handle", handle)
    handle = getattr(handle, "handle", handle)
    err = _libaudioverse.Lav_handleDecRef(handle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def handle_get_and_clear_first_access(handle):
    handle = getattr(handle, "handle", handle)
    handle = getattr(handle, "handle", handle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_handleGetAndClearFirstAccess(
        handle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def handle_get_ref_count(handle):
    handle = getattr(handle, "handle", handle)
    handle = getattr(handle, "handle", handle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_handleGetRefCount(handle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def handle_get_type(handle):
    handle = getattr(handle, "handle", handle)
    handle = getattr(handle, "handle", handle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_handleGetType(handle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def set_logging_callback(cb):
    err = _libaudioverse.Lav_setLoggingCallback(cb)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def get_logging_callback():
    destination = _libaudioverse.LavLoggingCallback()
    err = _libaudioverse.Lav_getLoggingCallback(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def set_logging_level(level):
    err = _libaudioverse.Lav_setLoggingLevel(level)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def get_logging_level():
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_getLoggingLevel(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def set_handle_destroyed_callback(cb):
    err = _libaudioverse.Lav_setHandleDestroyedCallback(cb)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def device_get_count():
    destination = ctypes.c_uint()
    err = _libaudioverse.Lav_deviceGetCount(ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def device_get_name(index):
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_deviceGetName(index, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def device_get_identifier_string(index):
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_deviceGetIdentifierString(index, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def device_get_channels(index):
    destination = ctypes.c_uint()
    err = _libaudioverse.Lav_deviceGetChannels(index, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def create_simulation(sr, blockSize):
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createSimulation(sr, blockSize, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def simulation_get_block_size(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_simulationGetBlockSize(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def simulation_get_block(simulationHandle, channels, mayApplyMixingMatrix, buffer):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    if isinstance(buffer, collections.abc.Sized):
        if not (
            isinstance(buffer, six.binary_type) or isinstance(buffer, six.text_type)
        ):
            buffer_t = ctypes.c_float * len(buffer)
            # Try to use the buffer interfaces, if we can.
            try:
                buffer = buffer_t.from_buffer(buffer)
            except TypeError:
                buffer_new = buffer_t()
                for i, j in enumerate(buffer):
                    buffer_new[i] = j
                buffer = buffer_new
        else:
            buffer = ctypes.cast(
                ctypes.create_string_buffer(buffer, len(buffer)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_simulationGetBlock(
        simulationHandle, channels, mayApplyMixingMatrix, buffer
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_get_sr(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_simulationGetSr(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def simulation_set_output_device(simulationHandle, device, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    device = device.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_simulationSetOutputDevice(
        simulationHandle, device, channels
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_clear_output_device(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    err = _libaudioverse.Lav_simulationClearOutputDevice(simulationHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_lock(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    err = _libaudioverse.Lav_simulationLock(simulationHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_unlock(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    err = _libaudioverse.Lav_simulationUnlock(simulationHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_set_block_callback(simulationHandle, callback, userdata):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_simulationSetBlockCallback(
        simulationHandle, callback, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_write_file(
    simulationHandle, path, channels, duration, mayApplyMixingMatrix
):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    path = path.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_simulationWriteFile(
        simulationHandle, path, channels, duration, mayApplyMixingMatrix
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_set_threads(simulationHandle, threads):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    err = _libaudioverse.Lav_simulationSetThreads(simulationHandle, threads)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def simulation_get_threads(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_simulationGetThreads(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def simulation_call_in(simulationHandle, when, inAudioThread, cb, userdata):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_simulationCallIn(
        simulationHandle, when, inAudioThread, cb, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_buffer(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createBuffer(simulationHandle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def buffer_get_simulation(bufferHandle):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_bufferGetSimulation(
        bufferHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def buffer_load_from_file(bufferHandle, path):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    path = path.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_bufferLoadFromFile(bufferHandle, path)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def buffer_load_from_array(bufferHandle, sr, channels, frames, data):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    if isinstance(data, collections.abc.Sized):
        if not (isinstance(data, six.binary_type) or isinstance(data, six.text_type)):
            data_t = ctypes.c_float * len(data)
            # Try to use the buffer interfaces, if we can.
            try:
                data = data_t.from_buffer(data)
            except TypeError:
                data_new = data_t()
                for i, j in enumerate(data):
                    data_new[i] = j
                data = data_new
        else:
            data = ctypes.cast(
                ctypes.create_string_buffer(data, len(data)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_bufferLoadFromArray(
        bufferHandle, sr, channels, frames, data
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def buffer_normalize(bufferHandle):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    err = _libaudioverse.Lav_bufferNormalize(bufferHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def buffer_get_duration(bufferHandle):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    destination = ctypes.c_float()
    err = _libaudioverse.Lav_bufferGetDuration(bufferHandle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def buffer_get_length_in_samples(bufferHandle):
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_bufferGetLengthInSamples(
        bufferHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_simulation(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_nodeGetSimulation(nodeHandle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def node_connect(nodeHandle, output, destHandle, input):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destHandle = getattr(destHandle, "handle", destHandle)
    destHandle = getattr(destHandle, "handle", destHandle)
    err = _libaudioverse.Lav_nodeConnect(nodeHandle, output, destHandle, input)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_connect_simulation(nodeHandle, output):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeConnectSimulation(nodeHandle, output)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_connect_property(nodeHandle, output, otherHandle, slot):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    otherHandle = getattr(otherHandle, "handle", otherHandle)
    otherHandle = getattr(otherHandle, "handle", otherHandle)
    err = _libaudioverse.Lav_nodeConnectProperty(nodeHandle, output, otherHandle, slot)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_disconnect(nodeHandle, output, otherHandle, input):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    otherHandle = getattr(otherHandle, "handle", otherHandle)
    otherHandle = getattr(otherHandle, "handle", otherHandle)
    err = _libaudioverse.Lav_nodeDisconnect(nodeHandle, output, otherHandle, input)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_isolate(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeIsolate(nodeHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_get_input_connection_count(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_uint()
    err = _libaudioverse.Lav_nodeGetInputConnectionCount(
        nodeHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_output_connection_count(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_uint()
    err = _libaudioverse.Lav_nodeGetOutputConnectionCount(
        nodeHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_reset_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeResetProperty(nodeHandle, propertyIndex)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_int_property(nodeHandle, propertyIndex, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeSetIntProperty(nodeHandle, propertyIndex, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_float_property(nodeHandle, propertyIndex, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeSetFloatProperty(nodeHandle, propertyIndex, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_double_property(nodeHandle, propertyIndex, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeSetDoubleProperty(nodeHandle, propertyIndex, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_string_property(nodeHandle, propertyIndex, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    value = value.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_nodeSetStringProperty(nodeHandle, propertyIndex, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_float3_property(nodeHandle, propertyIndex, v1, v2, v3):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeSetFloat3Property(
        nodeHandle, propertyIndex, v1, v2, v3
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_set_float6_property(nodeHandle, propertyIndex, v1, v2, v3, v4, v5, v6):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeSetFloat6Property(
        nodeHandle, propertyIndex, v1, v2, v3, v4, v5, v6
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_get_int_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_nodeGetIntProperty(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_float_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_float()
    err = _libaudioverse.Lav_nodeGetFloatProperty(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_double_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_double()
    err = _libaudioverse.Lav_nodeGetDoubleProperty(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_string_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_nodeGetStringProperty(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def node_get_float3_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination1 = ctypes.c_float()
    destination2 = ctypes.c_float()
    destination3 = ctypes.c_float()
    err = _libaudioverse.Lav_nodeGetFloat3Property(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destination1),
        ctypes.byref(destination2),
        ctypes.byref(destination3),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destination1, "value", destination1),
        getattr(destination2, "value", destination2),
        getattr(destination3, "value", destination3),
    )


def node_get_float6_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destinationV1 = ctypes.c_float()
    destinationV2 = ctypes.c_float()
    destinationV3 = ctypes.c_float()
    destinationV4 = ctypes.c_float()
    destinationV5 = ctypes.c_float()
    destinationV6 = ctypes.c_float()
    err = _libaudioverse.Lav_nodeGetFloat6Property(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destinationV1),
        ctypes.byref(destinationV2),
        ctypes.byref(destinationV3),
        ctypes.byref(destinationV4),
        ctypes.byref(destinationV5),
        ctypes.byref(destinationV6),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destinationV1, "value", destinationV1),
        getattr(destinationV2, "value", destinationV2),
        getattr(destinationV3, "value", destinationV3),
        getattr(destinationV4, "value", destinationV4),
        getattr(destinationV5, "value", destinationV5),
        getattr(destinationV6, "value", destinationV6),
    )


def node_get_int_property_range(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destinationMin = ctypes.c_int()
    destinationMax = ctypes.c_int()
    err = _libaudioverse.Lav_nodeGetIntPropertyRange(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destinationMin),
        ctypes.byref(destinationMax),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destinationMin, "value", destinationMin),
        getattr(destinationMax, "value", destinationMax),
    )


def node_get_float_property_range(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destinationMin = ctypes.c_float()
    destinationMax = ctypes.c_float()
    err = _libaudioverse.Lav_nodeGetFloatPropertyRange(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destinationMin),
        ctypes.byref(destinationMax),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destinationMin, "value", destinationMin),
        getattr(destinationMax, "value", destinationMax),
    )


def node_get_double_property_range(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destinationMin = ctypes.c_double()
    destinationMax = ctypes.c_double()
    err = _libaudioverse.Lav_nodeGetDoublePropertyRange(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destinationMin),
        ctypes.byref(destinationMax),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destinationMin, "value", destinationMin),
        getattr(destinationMax, "value", destinationMax),
    )


def node_get_property_name(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_char_p()
    err = _libaudioverse.Lav_nodeGetPropertyName(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return destination.value.decode("utf8")


def node_get_property_type(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_nodeGetPropertyType(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_property_has_dynamic_range(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_nodeGetPropertyHasDynamicRange(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_replace_float_array_property(nodeHandle, propertyIndex, length, values):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(values, collections.abc.Sized):
        if not (
            isinstance(values, six.binary_type) or isinstance(values, six.text_type)
        ):
            values_t = ctypes.c_float * len(values)
            # Try to use the buffer interfaces, if we can.
            try:
                values = values_t.from_buffer(values)
            except TypeError:
                values_new = values_t()
                for i, j in enumerate(values):
                    values_new[i] = j
                values = values_new
        else:
            values = ctypes.cast(
                ctypes.create_string_buffer(values, len(values)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_nodeReplaceFloatArrayProperty(
        nodeHandle, propertyIndex, length, values
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_read_float_array_property(nodeHandle, propertyIndex, index):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_float()
    err = _libaudioverse.Lav_nodeReadFloatArrayProperty(
        nodeHandle, propertyIndex, index, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_write_float_array_property(nodeHandle, propertyIndex, start, stop, values):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(values, collections.abc.Sized):
        if not (
            isinstance(values, six.binary_type) or isinstance(values, six.text_type)
        ):
            values_t = ctypes.c_float * len(values)
            # Try to use the buffer interfaces, if we can.
            try:
                values = values_t.from_buffer(values)
            except TypeError:
                values_new = values_t()
                for i, j in enumerate(values):
                    values_new[i] = j
                values = values_new
        else:
            values = ctypes.cast(
                ctypes.create_string_buffer(values, len(values)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_nodeWriteFloatArrayProperty(
        nodeHandle, propertyIndex, start, stop, values
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_get_float_array_property_length(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_uint()
    err = _libaudioverse.Lav_nodeGetFloatArrayPropertyLength(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_replace_int_array_property(nodeHandle, propertyIndex, length, values):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(values, collections.abc.Sized):
        if not (
            isinstance(values, six.binary_type) or isinstance(values, six.text_type)
        ):
            values_t = ctypes.c_int * len(values)
            # Try to use the buffer interfaces, if we can.
            try:
                values = values_t.from_buffer(values)
            except TypeError:
                values_new = values_t()
                for i, j in enumerate(values):
                    values_new[i] = j
                values = values_new
        else:
            values = ctypes.cast(
                ctypes.create_string_buffer(values, len(values)),
                ctypes.POINTER(ctypes.c_int),
            )
    err = _libaudioverse.Lav_nodeReplaceIntArrayProperty(
        nodeHandle, propertyIndex, length, values
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_read_int_array_property(nodeHandle, propertyIndex, index):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_nodeReadIntArrayProperty(
        nodeHandle, propertyIndex, index, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_write_int_array_property(nodeHandle, propertyIndex, start, stop, values):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(values, collections.abc.Sized):
        if not (
            isinstance(values, six.binary_type) or isinstance(values, six.text_type)
        ):
            values_t = ctypes.c_int * len(values)
            # Try to use the buffer interfaces, if we can.
            try:
                values = values_t.from_buffer(values)
            except TypeError:
                values_new = values_t()
                for i, j in enumerate(values):
                    values_new[i] = j
                values = values_new
        else:
            values = ctypes.cast(
                ctypes.create_string_buffer(values, len(values)),
                ctypes.POINTER(ctypes.c_int),
            )
    err = _libaudioverse.Lav_nodeWriteIntArrayProperty(
        nodeHandle, propertyIndex, start, stop, values
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_get_int_array_property_length(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_nodeGetIntArrayPropertyLength(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def node_get_array_property_length_range(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destinationMin = ctypes.c_uint()
    destinationMax = ctypes.c_uint()
    err = _libaudioverse.Lav_nodeGetArrayPropertyLengthRange(
        nodeHandle,
        propertyIndex,
        ctypes.byref(destinationMin),
        ctypes.byref(destinationMax),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return (
        getattr(destinationMin, "value", destinationMin),
        getattr(destinationMax, "value", destinationMax),
    )


def node_set_buffer_property(nodeHandle, propertyIndex, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    value = getattr(value, "handle", value)
    value = getattr(value, "handle", value)
    err = _libaudioverse.Lav_nodeSetBufferProperty(nodeHandle, propertyIndex, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_get_buffer_property(nodeHandle, propertyIndex):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_nodeGetBufferProperty(
        nodeHandle, propertyIndex, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def automation_cancel_automators(nodeHandle, propertyIndex, time):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_automationCancelAutomators(nodeHandle, propertyIndex, time)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def automation_linear_ramp_to_value(nodeHandle, slot, time, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_automationLinearRampToValue(nodeHandle, slot, time, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def automation_set(nodeHandle, slot, time, value):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_automationSet(nodeHandle, slot, time, value)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def automation_envelope(nodeHandle, slot, time, duration, valuesLength, values):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(values, collections.abc.Sized):
        if not (
            isinstance(values, six.binary_type) or isinstance(values, six.text_type)
        ):
            values_t = ctypes.c_double * len(values)
            # Try to use the buffer interfaces, if we can.
            try:
                values = values_t.from_buffer(values)
            except TypeError:
                values_new = values_t()
                for i, j in enumerate(values):
                    values_new[i] = j
                values = values_new
        else:
            values = ctypes.cast(
                ctypes.create_string_buffer(values, len(values)),
                ctypes.POINTER(ctypes.c_double),
            )
    err = _libaudioverse.Lav_automationEnvelope(
        nodeHandle, slot, time, duration, valuesLength, values
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def node_reset(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nodeReset(nodeHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_sine_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createSineNode(simulationHandle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_additive_square_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createAdditiveSquareNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_additive_triangle_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createAdditiveTriangleNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_additive_saw_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createAdditiveSawNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_noise_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createNoiseNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_hrtf_node(simulationHandle, hrtfPath):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    hrtfPath = hrtfPath.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createHrtfNode(
        simulationHandle, hrtfPath, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_hard_limiter_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createHardLimiterNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_crossfading_delay_node(simulationHandle, maxDelay, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createCrossfadingDelayNode(
        simulationHandle, maxDelay, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_dopplering_delay_node(simulationHandle, maxDelay, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createDoppleringDelayNode(
        simulationHandle, maxDelay, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_amplitude_panner_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createAmplitudePannerNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def amplitude_panner_node_configure_standard_map(nodeHandle, channels):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_amplitudePannerNodeConfigureStandardMap(
        nodeHandle, channels
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_multipanner_node(simulationHandle, hrtfPath):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    hrtfPath = hrtfPath.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createMultipannerNode(
        simulationHandle, hrtfPath, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_push_node(simulationHandle, sr, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createPushNode(
        simulationHandle, sr, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def push_node_feed(nodeHandle, length, frames):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(frames, collections.abc.Sized):
        if not (
            isinstance(frames, six.binary_type) or isinstance(frames, six.text_type)
        ):
            frames_t = ctypes.c_float * len(frames)
            # Try to use the buffer interfaces, if we can.
            try:
                frames = frames_t.from_buffer(frames)
            except TypeError:
                frames_new = frames_t()
                for i, j in enumerate(frames):
                    frames_new[i] = j
                frames = frames_new
        else:
            frames = ctypes.cast(
                ctypes.create_string_buffer(frames, len(frames)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_pushNodeFeed(nodeHandle, length, frames)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def push_node_set_low_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_pushNodeSetLowCallback(nodeHandle, callback, userdata)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def push_node_set_underrun_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_pushNodeSetUnderrunCallback(nodeHandle, callback, userdata)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_biquad_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createBiquadNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_pull_node(simulationHandle, sr, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createPullNode(
        simulationHandle, sr, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def pull_node_set_audio_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_pullNodeSetAudioCallback(nodeHandle, callback, userdata)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_graph_listener_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createGraphListenerNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def graph_listener_node_set_listening_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_graphListenerNodeSetListeningCallback(
        nodeHandle, callback, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_custom_node(
    simulationHandle, inputs, channelsPerInput, outputs, channelsPerOutput
):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createCustomNode(
        simulationHandle,
        inputs,
        channelsPerInput,
        outputs,
        channelsPerOutput,
        ctypes.byref(destination),
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def custom_node_set_processing_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_customNodeSetProcessingCallback(
        nodeHandle, callback, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_ringmod_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createRingmodNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_feedback_delay_network_node(simulationHandle, maxDelay, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFeedbackDelayNetworkNode(
        simulationHandle, maxDelay, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_iir_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createIirNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def iir_node_set_coefficients(
    nodeHandle,
    numeratorLength,
    numerator,
    denominatorLength,
    denominator,
    shouldClearHistory,
):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(numerator, collections.abc.Sized):
        if not (
            isinstance(numerator, six.binary_type)
            or isinstance(numerator, six.text_type)
        ):
            numerator_t = ctypes.c_double * len(numerator)
            # Try to use the buffer interfaces, if we can.
            try:
                numerator = numerator_t.from_buffer(numerator)
            except TypeError:
                numerator_new = numerator_t()
                for i, j in enumerate(numerator):
                    numerator_new[i] = j
                numerator = numerator_new
        else:
            numerator = ctypes.cast(
                ctypes.create_string_buffer(numerator, len(numerator)),
                ctypes.POINTER(ctypes.c_double),
            )
    if isinstance(denominator, collections.abc.Sized):
        if not (
            isinstance(denominator, six.binary_type)
            or isinstance(denominator, six.text_type)
        ):
            denominator_t = ctypes.c_double * len(denominator)
            # Try to use the buffer interfaces, if we can.
            try:
                denominator = denominator_t.from_buffer(denominator)
            except TypeError:
                denominator_new = denominator_t()
                for i, j in enumerate(denominator):
                    denominator_new[i] = j
                denominator = denominator_new
        else:
            denominator = ctypes.cast(
                ctypes.create_string_buffer(denominator, len(denominator)),
                ctypes.POINTER(ctypes.c_double),
            )
    err = _libaudioverse.Lav_iirNodeSetCoefficients(
        nodeHandle,
        numeratorLength,
        numerator,
        denominatorLength,
        denominator,
        shouldClearHistory,
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_gain_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createGainNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_channel_splitter_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createChannelSplitterNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_channel_merger_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createChannelMergerNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_buffer_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createBufferNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def buffer_node_set_end_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_bufferNodeSetEndCallback(nodeHandle, callback, userdata)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_buffer_timeline_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createBufferTimelineNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def buffer_timeline_node_schedule_buffer(nodeHandle, bufferHandle, time, pitchBend):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    err = _libaudioverse.Lav_bufferTimelineNodeScheduleBuffer(
        nodeHandle, bufferHandle, time, pitchBend
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_recorder_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createRecorderNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def recorder_node_start_recording(nodeHandle, path):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    path = path.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_recorderNodeStartRecording(nodeHandle, path)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def recorder_node_stop_recording(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_recorderNodeStopRecording(nodeHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_convolver_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createConvolverNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_fft_convolver_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFftConvolverNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def fft_convolver_node_set_response(nodeHandle, channel, length, response):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(response, collections.abc.Sized):
        if not (
            isinstance(response, six.binary_type) or isinstance(response, six.text_type)
        ):
            response_t = ctypes.c_float * len(response)
            # Try to use the buffer interfaces, if we can.
            try:
                response = response_t.from_buffer(response)
            except TypeError:
                response_new = response_t()
                for i, j in enumerate(response):
                    response_new[i] = j
                response = response_new
        else:
            response = ctypes.cast(
                ctypes.create_string_buffer(response, len(response)),
                ctypes.POINTER(ctypes.c_float),
            )
    err = _libaudioverse.Lav_fftConvolverNodeSetResponse(
        nodeHandle, channel, length, response
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def fft_convolver_node_set_response_from_file(
    nodeHandle, path, fileChannel, convolverChannel
):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    path = path.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    err = _libaudioverse.Lav_fftConvolverNodeSetResponseFromFile(
        nodeHandle, path, fileChannel, convolverChannel
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_three_band_eq_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createThreeBandEqNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_filtered_delay_node(simulationHandle, maxDelay, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFilteredDelayNode(
        simulationHandle, maxDelay, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_crossfader_node(simulationHandle, channels, inputs):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createCrossfaderNode(
        simulationHandle, channels, inputs, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def crossfader_node_crossfade(nodeHandle, duration, input):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_crossfaderNodeCrossfade(nodeHandle, duration, input)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def crossfader_node_set_finished_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_crossfaderNodeSetFinishedCallback(
        nodeHandle, callback, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_one_pole_filter_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createOnePoleFilterNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_first_order_filter_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFirstOrderFilterNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def first_order_filter_node_configure_lowpass(nodeHandle, frequency):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_firstOrderFilterNodeConfigureLowpass(nodeHandle, frequency)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def first_order_filter_node_configure_highpass(nodeHandle, frequency):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_firstOrderFilterNodeConfigureHighpass(
        nodeHandle, frequency
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def first_order_filter_node_configure_allpass(nodeHandle, frequency):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_firstOrderFilterNodeConfigureAllpass(nodeHandle, frequency)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_allpass_node(simulationHandle, channels, maxDelay):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createAllpassNode(
        simulationHandle, channels, maxDelay, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_nested_allpass_network_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createNestedAllpassNetworkNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def nested_allpass_network_node_begin_nesting(nodeHandle, delay, coefficient):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeBeginNesting(
        nodeHandle, delay, coefficient
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_end_nesting(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeEndNesting(nodeHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_append_allpass(nodeHandle, delay, coefficient):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeAppendAllpass(
        nodeHandle, delay, coefficient
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_append_one_pole(nodeHandle, frequency, isHighpass):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeAppendOnePole(
        nodeHandle, frequency, isHighpass
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_append_biquad(nodeHandle, type, frequency, dbGain, q):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeAppendBiquad(
        nodeHandle, type, frequency, dbGain, q
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_append_reader(nodeHandle, mul):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeAppendReader(nodeHandle, mul)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def nested_allpass_network_node_compile(nodeHandle):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_nestedAllpassNetworkNodeCompile(nodeHandle)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_fdn_reverb_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFdnReverbNode(
        simulationHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_blit_node(simulationHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createBlitNode(simulationHandle, ctypes.byref(destination))
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_dc_blocker_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createDcBlockerNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_leaky_integrator_node(simulationHandle, channels):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createLeakyIntegratorNode(
        simulationHandle, channels, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def create_file_streamer_node(simulationHandle, path):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    path = path.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createFileStreamerNode(
        simulationHandle, path, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def file_streamer_node_set_end_callback(nodeHandle, callback, userdata):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    if isinstance(userdata, collections.abc.Sized):
        if not (
            isinstance(userdata, six.binary_type) or isinstance(userdata, six.text_type)
        ):
            userdata_t = None * len(userdata)
            # Try to use the buffer interfaces, if we can.
            try:
                userdata = userdata_t.from_buffer(userdata)
            except TypeError:
                userdata_new = userdata_t()
                for i, j in enumerate(userdata):
                    userdata_new[i] = j
                userdata = userdata_new
        else:
            userdata = ctypes.cast(
                ctypes.create_string_buffer(userdata, len(userdata)), ctypes.c_void_p
            )
    err = _libaudioverse.Lav_fileStreamerNodeSetEndCallback(
        nodeHandle, callback, userdata
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def create_environment_node(simulationHandle, hrtfPath):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    hrtfPath = hrtfPath.encode(
        "utf8"
    )  # All strings are contractually UTF8 when entering Libaudioverse.
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createEnvironmentNode(
        simulationHandle, hrtfPath, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def environment_node_play_async(nodeHandle, bufferHandle, x, y, z, isDry):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    bufferHandle = getattr(bufferHandle, "handle", bufferHandle)
    err = _libaudioverse.Lav_environmentNodePlayAsync(
        nodeHandle, bufferHandle, x, y, z, isDry
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def environment_node_add_effect_send(nodeHandle, channels, isReverb, connectByDefault):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    destination = ctypes.c_int()
    err = _libaudioverse.Lav_environmentNodeAddEffectSend(
        nodeHandle, channels, isReverb, connectByDefault, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return getattr(destination, "value", destination)


def create_source_node(simulationHandle, environmentHandle):
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    simulationHandle = getattr(simulationHandle, "handle", simulationHandle)
    environmentHandle = getattr(environmentHandle, "handle", environmentHandle)
    environmentHandle = getattr(environmentHandle, "handle", environmentHandle)
    destination = _libaudioverse.LavHandle()
    err = _libaudioverse.Lav_createSourceNode(
        simulationHandle, environmentHandle, ctypes.byref(destination)
    )
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
    return reverse_handle(destination.value)


def source_node_feed_effect(nodeHandle, effect):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_sourceNodeFeedEffect(nodeHandle, effect)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)


def source_node_stop_feeding_effect(nodeHandle, effect):
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    nodeHandle = getattr(nodeHandle, "handle", nodeHandle)
    err = _libaudioverse.Lav_sourceNodeStopFeedingEffect(nodeHandle, effect)
    if err != _libaudioverse.Lav_ERROR_NONE:
        raise make_error_from_code(err)
