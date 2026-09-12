#include <stdio.h>
#include <stdlib.h>
#include "tinh_tien_day.h"

// MODULE 3: TÍNH TIỀN DẠY - PHIÊN BẢN CÓ LỖ HỔNG (VULN)
long calculate_e2e_salary_VULN(LopHocPhan *lhp, Config *cfg) {
    // LOI CWE-476: Khong kiem tra lhp hoac lhp->gv_ptr == NULL truoc khi doc thuoc tinh!
    // LOI CWE-416: Truc tiep truy cap lhp->gv_ptr->heSoBangCap sau khi gv da bi free!
    float heSoQuyMo = (lhp->soLuongSinhVien > 50) ? 0.2f : 0.0f;

    // LOI CWE-190: Ep kieu (int) va nhan cac so nguyen lon gay tran so 32-bit khi soTiet lon
    int soTietQuyDoi = (int)(lhp->soTiet * (lhp->heSoHocPhan + heSoQuyMo));
    int tienDay32 = (int)soTietQuyDoi * (int)lhp->gv_ptr->heSoBangCap * (int)cfg->dinhMucTienChuan;

    return (long)tienDay32;
}

void export_report_VULN(GiangVien *gv, LopHocPhan *lhp, long tienDay) {
    printf("[MOD-E2E REPORT] GV: %s (%s) | Lop: %s | Tiet: %d | Tien: %ld VND\n",
           gv ? gv->hoTen : "NULL",
           gv ? gv->bangCap : "NULL",
           lhp ? lhp->maLop : "NULL",
           lhp ? lhp->soTiet : 0,
           tienDay);
}

// MODULE 3: TÍNH TIỀN DẠY - PHIÊN BẢN AN TOÀN (SAFE)
long long calculate_e2e_salary_SAFE(LopHocPhan *lhp, Config *cfg) {
    // FIX CWE-476: Check for NULL pointer on class section and assigned lecturer
    if (!lhp || !cfg) {
        fprintf(stderr, "[SAFE ERROR] Class Section or Config is NULL!\n");
        return -1;
    }
    if (!lhp->gv_ptr || lhp->gv_ptr->is_deleted) {
        fprintf(stderr, "[SAFE BLOCKED] Class section '%s' has NO assigned lecturer! Cannot calculate salary.\n", lhp->maLop);
        return 0;
    }

    double heSoQuyMo = (lhp->soLuongSinhVien > 50) ? 0.2 : 0.0;
    // FIX CWE-190: 64-bit double & long long arithmetic preventing integer overflow
    double soTietQuyDoi = (double)lhp->soTiet * ((double)lhp->heSoHocPhan + heSoQuyMo);
    double tienDayDouble = soTietQuyDoi * (double)lhp->gv_ptr->heSoBangCap * (double)cfg->dinhMucTienChuan;

    return (long long)tienDayDouble;
}

void export_report_SAFE(GiangVien *gv, LopHocPhan *lhp, long long tienDay) {
    printf("[MOD-E2E SAFE REPORT] GV: %s (%s) | Lop: %s | Tiet: %d | Tien: %lld VND\n",
           gv ? gv->hoTen : "UNASSIGNED",
           gv ? gv->bangCap : "N/A",
           lhp ? lhp->maLop : "UNKNOWN",
           lhp ? lhp->soTiet : 0,
           tienDay);
}
