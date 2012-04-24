from ctypes import *
from ctypes.util import find_library

def load_librtlsdr():
    driver_files = ['rtlsdr.dll', 'librtlsdr.so']
    driver_files += ['..//rtlsdr.dll', '..//librtlsdr.so']
    driver_files += ['rtlsdr//rtlsdr.dll', 'rtlsdr//librtlsdr.so']
    driver_files += [find_library('rtlsdr'), find_library('librtlsdr')]
    
    dll = None
    
    for driver in driver_files:
        try:
            dll = CDLL(driver)
            break
        except:
            pass
    else:        
        raise ImportError('Error loading librtlsdr (library missing or dependency issue)')
        
    return dll

librtlsdr = load_librtlsdr()

# we don't care about the rtlsdr_dev struct and it's allocated by librtlsdr, so 
# we won't even bother filling it in
p_rtlsdr_dev = c_void_p

# async callbacks must be passed through this function
# typedef void(*rtlsdr_read_async_cb_t)(unsigned char *buf, uint32_t len, void *ctx);
rtlsdr_read_async_cb_t = CFUNCTYPE(None, POINTER(c_ubyte), c_int, py_object)

# uint32_t rtlsdr_get_device_count(void);
f = librtlsdr.rtlsdr_get_device_count
f.restype, f.argtypes = c_uint, []

# const char* rtlsdr_get_device_name(uint32_t index);
f = librtlsdr.rtlsdr_get_device_name
f.restype, f.argtypes = c_char_p, [c_uint]

# int rtlsdr_open(rtlsdr_dev_t **dev, uint32_t index);
f = librtlsdr.rtlsdr_open
f.restype, f.argtypes = c_int, [POINTER(p_rtlsdr_dev), c_uint]

# int rtlsdr_close(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_close
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

# /* configuration functions */

# int rtlsdr_set_center_freq(rtlsdr_dev_t *dev, uint32_t freq);
f = librtlsdr.rtlsdr_set_center_freq
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, c_uint]

# int rtlsdr_get_center_freq(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_get_center_freq
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

# int rtlsdr_set_freq_correction(rtlsdr_dev_t *dev, int ppm);
f = librtlsdr.rtlsdr_set_freq_correction
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, c_int]

# int rtlsdr_get_freq_correction(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_get_freq_correction
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

# int rtlsdr_set_tuner_gain(rtlsdr_dev_t *dev, int gain);
f = librtlsdr.rtlsdr_set_tuner_gain
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, c_int]

# int rtlsdr_get_tuner_gain(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_get_tuner_gain
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

# int rtlsdr_set_sample_rate(rtlsdr_dev_t *dev, uint32_t rate);
f = librtlsdr.rtlsdr_set_sample_rate
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, c_uint]

# int rtlsdr_get_sample_rate(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_get_sample_rate
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

#/* streaming functions */

# int rtlsdr_reset_buffer(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_reset_buffer
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

# int rtlsdr_read_sync(rtlsdr_dev_t *dev, void *buf, int len, int *n_read);
f = librtlsdr.rtlsdr_read_sync
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, c_void_p, c_int, POINTER(c_int)]

# int rtlsdr_wait_async(rtlsdr_dev_t *dev, rtlsdr_read_async_cb_t cb, void *ctx);
f = librtlsdr.rtlsdr_wait_async
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, POINTER(rtlsdr_read_async_cb_t), py_object]

#int rtlsdr_read_async(rtlsdr_dev_t *dev,
#				 rtlsdr_read_async_cb_t cb,
#				 void *ctx,
#				 uint32_t buf_num,
#				 uint32_t buf_len);
f = librtlsdr.rtlsdr_read_async
f.restype, f.argtypes = c_int, [p_rtlsdr_dev, rtlsdr_read_async_cb_t, py_object, c_uint, c_uint]

# int rtlsdr_cancel_async(rtlsdr_dev_t *dev);
f = librtlsdr.rtlsdr_cancel_async
f.restype, f.argtypes = c_int, [p_rtlsdr_dev]

__all__  = ['librtlsdr', 'p_rtlsdr_dev', 'rtlsdr_read_async_cb_t']