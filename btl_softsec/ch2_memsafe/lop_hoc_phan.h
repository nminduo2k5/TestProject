#ifndef LOP_HOC_PHAN_H
#define LOP_HOC_PHAN_H

#include "giang_vien.h"

#define MAX_MALOP 20  // CON-4: buffer maLop toi da 20 byte (REQ-3.2 / CWE-120, xem chuong2.tex tab:con)

// MODULE 2: QUẢN LÝ LỚP HỌC PHẦN (Class Section Management Struct)
typedef struct {
    int         id;
    char        maLop[MAX_MALOP];  // CWE-120: Buffer overflow if input > 20 chars (CON-4)
    int         soTiet;            // CON-12: chi co guard 1 chieu (kep ve 0 neu <=0), khong guard tren <=500
    float       heSoHocPhan;
    int         soLuongSinhVien;
    GiangVien  *gv_ptr;           // CON-7: con tro NULL-able (C khong co kieu non-null) - "da phan cong"
                                    // chi duoc suy ngam tu gv_ptr!=NULL (REQ-1.0, REQ-5.1/5.2 / CWE-416, CWE-476)
} LopHocPhan;

LopHocPhan* create_class_section_VULN(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv);
LopHocPhan* create_class_section_SAFE(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv);

#endif
