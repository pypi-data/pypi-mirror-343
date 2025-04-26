import ctypes
import os
import numpy as np

def load_librmf():
    _this_dir = os.path.dirname(__file__)
    
    for fname in os.listdir(_this_dir):
        if fname.startswith("librmf") and fname.endswith((".so", ".dylib", ".dll")):
            full_path = os.path.join(_this_dir, fname)
            return ctypes.cdll.LoadLibrary(full_path)
    
    raise FileNotFoundError("rmf shared library not found in: " + _this_dir)

lib = load_librmf()

lib.ns_alloc_c.argtypes = [ctypes.c_int]
lib.ns_alloc_c.restype = ctypes.POINTER(ctypes.c_double)

lib.snm_alloc_c.argtypes = [ctypes.c_int]
lib.snm_alloc_c.restype = ctypes.POINTER(ctypes.c_double)

lib.ns_rmf_c.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
lib.ns_rmf_c.restype  = ctypes.c_int

lib.snm_rmf_c.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
lib.snm_rmf_c.restype  = ctypes.c_int

# lib.get_snm_len_eos.argtypes = []
lib.get_snm_len_eos_var.restype  = ctypes.c_int
lib.get_ns_len_eos_var.restype   = ctypes.c_int

lib.ns_free_c.argtypes = [ctypes.POINTER(ctypes.c_double)]
lib.snm_free_c.argtypes = [ctypes.POINTER(ctypes.c_double)]


def snm_rmf(const_coup, n_max, num_n):
    p_const_coup = const_coup.ctypes.data_as(ctypes.c_void_p)

    eos_pointer = lib.snm_alloc_c(num_n)

    len_eos_var = lib.get_snm_len_eos_var()

    error_flag = lib.snm_rmf_c(p_const_coup, n_max, num_n, eos_pointer)
    if (error_flag == 2):
        for i in range(num_n):
            if (eos_pointer[len_eos_var*i] <= 0):
                in_max = i - 1
                break

        snm_eos = np.zeros((in_max+1, len_eos_var))
        for i_var in range(len_eos_var):
            snm_eos[:, i_var] = np.array((eos_pointer[i_var:len_eos_var*(in_max+1):len_eos_var]))

        n_valid_max = eos_pointer[len_eos_var*in_max]
        if (n_valid_max < 0.9):
            lib.snm_free_c(eos_pointer)
            return (snm_eos, 2)
        else:
            lib.snm_free_c(eos_pointer)
            return (snm_eos, 0)
    else:
        snm_eos = np.zeros((num_n, len_eos_var))
        for i_var in range(len_eos_var):
            snm_eos[:, i_var] = np.array((eos_pointer[i_var:len_eos_var*num_n:len_eos_var]))

    lib.snm_free_c(eos_pointer)

    return (snm_eos, error_flag)


def ns_rmf(const_coup, n_max, num_n):
    p_const_coup = const_coup.ctypes.data_as(ctypes.c_void_p)

    eos_pointer = lib.ns_alloc_c(num_n)

    len_eos_var = lib.get_ns_len_eos_var()

    error_flag = lib.ns_rmf_c(p_const_coup, n_max, num_n, eos_pointer)
    if (error_flag == 2):
        for i in range(num_n):
            if (eos_pointer[len_eos_var*i] <= 0):
                in_max = i - 1
                break

        ns_eos = np.zeros((in_max+1, len_eos_var))
        for i_var in range(len_eos_var):
            ns_eos[:, i_var] = np.array((eos_pointer[i_var:len_eos_var*(in_max+1):len_eos_var]))

        n_valid_max = eos_pointer[len_eos_var*in_max]
        if (n_valid_max < 0.9):
            lib.ns_free_c(eos_pointer)
            return (ns_eos, 2)
        else:
            lib.ns_free_c(eos_pointer)
            return (ns_eos, 0)
    else:
        ns_eos = np.zeros((num_n, len_eos_var))
        for i_var in range(len_eos_var):
            ns_eos[:, i_var] = np.array((eos_pointer[i_var:len_eos_var*num_n:len_eos_var]))

    lib.ns_free_c(eos_pointer)

    return (ns_eos, error_flag)
