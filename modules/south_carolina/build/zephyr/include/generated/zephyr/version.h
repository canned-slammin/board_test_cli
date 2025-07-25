#ifndef _KERNEL_VERSION_H_
#define _KERNEL_VERSION_H_

/* The template values come from cmake/version.cmake
 * BUILD_VERSION related template values will be 'git describe',
 * alternatively user defined BUILD_VERSION.
 */

#define ZEPHYR_VERSION_CODE 198400
#define ZEPHYR_VERSION(a,b,c) (((a) << 16) + ((b) << 8) + (c))

#define KERNELVERSION                   0x3070000
#define KERNEL_VERSION_NUMBER           0x30700
#define KERNEL_VERSION_MAJOR            3
#define KERNEL_VERSION_MINOR            7
#define KERNEL_PATCHLEVEL               0
#define KERNEL_TWEAK                    0
#define KERNEL_VERSION_STRING           "3.7.0-rc1"
#define KERNEL_VERSION_EXTENDED_STRING  "3.7.0-rc1+0"
#define KERNEL_VERSION_TWEAK_STRING     "3.7.0+0"

#define BUILD_VERSION v3.7.0-rc1-42-gf41cb40a6e74


#endif /* _KERNEL_VERSION_H_ */
