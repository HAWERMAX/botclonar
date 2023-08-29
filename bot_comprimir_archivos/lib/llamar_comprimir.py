import ctypes

def comprimir_archivo(input_path, output_path):
    lib = ctypes.CDLL('/home/trev7or23/code/bots_python/bot_comprimir_archivos/lib/libcomprimir_archivos.so')
    lib.comprimir_archivo.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.comprimir_archivo.restype = None
    
    input_path_bytes = input_path.encode("utf-8")
    output_path_bytes = output_path.encode("utf-8")
    
    lib.comprimir_archivo(input_path_bytes, output_path_bytes)

