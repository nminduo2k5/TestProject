#ifndef TINH_TIEN_DAY_H
#define TINH_TIEN_DAY_H

#include "lop_hoc_phan.h"

// MODULE 3: TÍNH TIỀN DẠY & THANH TOÁN (Salary Calculation Struct)
typedef struct {
    float heSoQuyMoLop;      // NFR-7 FAIL: dead field - KHONG duoc calculate_e2e_salary_*() doc o dau
                              // ca (xem tinh_tien_day.c); he so quy mo that duoc tinh lai tu
                              // soLuongSinhVien qua nguong CON-11 (50), khong dung field nay.
    long long dinhMucTienChuan;  // CON-8 (cfg NULL-able): chi duoc doc khi calculate_e2e_salary_SAFE
                                   // da kiem tra cfg!=NULL truoc (REQ-10.1/10.2)
    int   nam;               // NFR-7 FAIL: dead field - chi gan luc khoi tao (main*.c), khong ham
                              // nao doc lai (kha xuat_report_*() cung khong in nam hoc)
} Config;

long calculate_e2e_salary_VULN(LopHocPhan *lhp, Config *cfg);
// CON-6: ban VULN ep ket qua trung gian ve (int) 32-bit truoc khi nhan don gia -> co the
// tran so nguyen (REQ-6.1-6.4 / CWE-190); ban SAFE dung double/long long xuyen suot.
long long calculate_e2e_salary_SAFE(LopHocPhan *lhp, Config *cfg);

void export_report_VULN(GiangVien *gv, LopHocPhan *lhp, long tienDay);
void export_report_SAFE(GiangVien *gv, LopHocPhan *lhp, long long tienDay);

// CWE-197: Numeric Truncation Error - ep kieu so luong sinh vien (int, co the toi vai tram
// voi lop dai cuong) xuong signed char (-128..127) khi dong goi ban ghi audit log gon nhe.
// CON-5: kieu char (signed 8-bit) chi an toan trong [0,127] - vuot qua se wrap-around
// (REQ-8.1-8.5 / CWE-197); mien nghiep vu that cua soLuongSinhVien la [0,300] (tab:range).
char pack_class_size_byte_VULN(int soLuongSinhVien);
int  pack_class_size_byte_SAFE(int soLuongSinhVien, char *out_byte);

#endif
