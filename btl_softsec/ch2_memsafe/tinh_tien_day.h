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

#endif
