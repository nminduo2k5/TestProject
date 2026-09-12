#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lop_hoc_phan.h"

// MODULE 2: QUẢN LÝ LỚP HỌC PHẦN - PHIÊN BẢN CÓ LỖ HỔNG (VULN)
LopHocPhan* create_class_section_VULN(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv) {
    LopHocPhan *lhp = (LopHocPhan*)malloc(sizeof(LopHocPhan));
    if (!lhp) return NULL;

    lhp->id = id;
    // LOI CWE-120: strcpy khong kiem tra do dai maLop so voi MAX_MALOP (20)
    strcpy(lhp->maLop, maLop);
    lhp->soTiet = soTiet;
    lhp->heSoHocPhan = heSoHP;
    lhp->soLuongSinhVien = svCount;
    lhp->gv_ptr = gv; // Link to Module 1 (Có thể dẫn tới CWE-416 nếu gv bị free mà lhp không biết)
    return lhp;
}

// MODULE 2: QUẢN LÝ LỚP HỌC PHẦN - PHIÊN BẢN AN TOÀN (SAFE)
LopHocPhan* create_class_section_SAFE(int id, const char *maLop, int soTiet, float heSoHP, int svCount, GiangVien *gv) {
    if (!maLop) return NULL;

    LopHocPhan *lhp = (LopHocPhan*)malloc(sizeof(LopHocPhan));
    if (!lhp) return NULL;

    lhp->id = id;
    // FIX CWE-120: Bounds checking using snprintf
    snprintf(lhp->maLop, sizeof(lhp->maLop), "%s", maLop);
    lhp->soTiet = (soTiet > 0) ? soTiet : 0;
    lhp->heSoHocPhan = (heSoHP > 0.0f) ? heSoHP : 1.0f;
    lhp->soLuongSinhVien = (svCount > 0) ? svCount : 0;
    lhp->gv_ptr = (gv && !gv->is_deleted) ? gv : NULL; // Verify non-null & non-deleted
    return lhp;
}
