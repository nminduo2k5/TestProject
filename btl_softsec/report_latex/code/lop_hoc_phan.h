#ifndef LOP_HOC_PHAN_H
#define LOP_HOC_PHAN_H

#include "giang_vien.h"

#define MAX_MALOP 20

// MODULE 2: QUẢN LÝ LỚP HỌC PHẦN (Class Section Management Struct)
typedef struct {
    int         id;
    char        maLop[MAX_MALOP];  // CWE-120: Buffer overflow if input > 20 chars
    int         soTiet;
    float       heSoHocPhan;
    int         soLuongSinhVien;
    GiangVien  *gv_ptr;           // Pointer linked to Module 1 (CWE-416 UAF / CWE-476 NULL)
} LopHocPhan;

LopHocPhan* create_class_section_VULN(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv);
LopHocPhan* create_class_section_SAFE(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv);

#endif
