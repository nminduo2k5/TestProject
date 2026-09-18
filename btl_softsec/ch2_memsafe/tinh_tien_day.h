#ifndef TINH_TIEN_DAY_H
#define TINH_TIEN_DAY_H

#include "lop_hoc_phan.h"

// MODULE 3: TÍNH TIỀN DẠY & THANH TOÁN (Salary Calculation Struct)
typedef struct {
    float heSoQuyMoLop;
    long long dinhMucTienChuan;
    int   nam;
} Config;

long calculate_e2e_salary_VULN(LopHocPhan *lhp, Config *cfg);
long long calculate_e2e_salary_SAFE(LopHocPhan *lhp, Config *cfg);

void export_report_VULN(GiangVien *gv, LopHocPhan *lhp, long tienDay);
void export_report_SAFE(GiangVien *gv, LopHocPhan *lhp, long long tienDay);

// CWE-197: Numeric Truncation Error - ep kieu so luong sinh vien (int, co the toi vai tram
// voi lop dai cuong) xuong signed char (-128..127) khi dong goi ban ghi audit log gon nhe.
char pack_class_size_byte_VULN(int soLuongSinhVien);
int  pack_class_size_byte_SAFE(int soLuongSinhVien, char *out_byte);

#endif
