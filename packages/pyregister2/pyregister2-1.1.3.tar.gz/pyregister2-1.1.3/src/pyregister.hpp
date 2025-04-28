#pragma once

// Cross-platform export macro
#if defined(_WIN32) || defined(__CYGWIN__)
  #ifdef BUILD_DLL
    #define API_EXPORT __declspec(dllexport)
  #else
    #define API_EXPORT __declspec(dllimport)
  #endif
#else
  #if __GNUC__ >= 4
    #define API_EXPORT __attribute__((visibility("default")))
  #else
    #define API_EXPORT
  #endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

API_EXPORT void write_register(const char* register_name, int val);
API_EXPORT void read_register(const char* register_name);
API_EXPORT void syscall();
API_EXPORT const char* execute();

#ifdef __cplusplus
}
#endif
