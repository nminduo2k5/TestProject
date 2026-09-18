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

// MODULE 3 (MO RONG): DONG GOI BAN GHI AUDIT LOG GON NHE - PHIEN BAN CO LO HONG (VULN)
// LOI CWE-197 (Numeric Truncation Error): soLuongSinhVien la int, thuc te lop dai cuong o
// DuongUniversity co the len toi vai tram sinh vien (vd 200), nhung khi dong goi vao ban ghi
// audit log gon nhe (1 byte/truong) lai ep thang xuong signed char (pham vi -128..127) MA
// KHONG kiem tra pham vi truoc -> gia tri > 127 bi "wrap around" thanh so am (vd 200 -> -56),
// lam sai lech du lieu audit/thong ke duyet chi ve sau.
char pack_class_size_byte_VULN(int soLuongSinhVien) {
    return (char)soLuongSinhVien;
}

// MODULE 3 (MO RONG): DONG GOI BAN GHI AUDIT LOG - PHIEN BAN AN TOAN (SAFE)
// FIX CWE-197: Kiem tra pham vi hop le cua signed char (0..127) TRUOC khi ep kieu; neu vuot
// pham vi thi TU CHOI dong goi (tra ve 0 bao that bai) thay vi de gia tri wrap-around am
// tham lang di vao du lieu audit/thanh toan.
int pack_class_size_byte_SAFE(int soLuongSinhVien, char *out_byte) {
    if (soLuongSinhVien < 0 || soLuongSinhVien > 127) {
        fprintf(stderr, "[SAFE ERROR] soLuongSinhVien=%d vuot pham vi char (0..127) - TU CHOI ep kieu de tranh Numeric Truncation!\n", soLuongSinhVien);
        return 0;
    }
    *out_byte = (char)soLuongSinhVien;
    return 1;
}
