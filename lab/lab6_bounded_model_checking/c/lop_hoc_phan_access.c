/*
 * Lab 6 - Cai dat C thuc te tuong ung cac chuong trinh trong dataset BMC
 * ==========================================================================
 * He thong DuongUniversity Management System - Module 2: Quan ly Lop hoc phan
 * Chuong 3: 3.5 Bounded Model Checking, 3.6 Mo hinh bo nho, 3.7 Sap xep mo hinh bo nho
 *
 * Boi canh (dung dung domain btl_softsec/ch2_memsafe):
 *   Moi giang vien phu trach toi da MAX_LOP = 10 lop hoc phan trong 1 hoc ky,
 *   luu trong mang danhSachLop[MAX_LOP] (phan tu la LopHocPhanEntry - ban rut
 *   gon cua struct LopHocPhan trong lop_hoc_phan.h, giu dung MAX_MALOP = 20 va
 *   cac truong soTiet / heSoHocPhan / soLuongSinhVien).
 *   Chuc nang "xuat bang ke thu lao theo trang" (Module 3) doc PAGE_SIZE = 5 lop
 *   lien tiep bat dau tu base_index (offset trang do nguoi dung nhap). Neu
 *   base_index KHONG duoc kiem tra, vong lap se doc danhSachLop[index] voi
 *   index >= MAX_LOP -> doc ngoai bien (CWE-125 Out-of-bounds Read): soTiet rac
 *   di thang vao cong thuc tinh tien day (sai thu lao / lo thong tin stack).
 *
 * Doi chieu ket qua BMC (tinh, Python/Z3) voi hanh vi runtime thuc te (dong,
 * AddressSanitizer) - cung nguyen tac doi chieu da ap dung o Lab 3 / Lab 4.
 *
 * Bien dich (Windows - Clang MSYS2 clang64, GCC UCRT64 khong co libasan):
 *   C:\msys64\clang64\bin\clang.exe -g -fsanitize=address -o lop_hoc_phan_access.exe lop_hoc_phan_access.c
 * Su dung  : ./lop_hoc_phan_access <mode> [base_index]
 *   mode: safe_full_scan | offbyone | symbolic_unsafe | symbolic_safe
 *         | symbolic_reverse | symbolic_reverse_fixed
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LOP    10   /* so lop hoc phan toi da / giang vien / hoc ky (array_size trong dataset) */
#define MAX_MALOP  20   /* CON-4: giong het lop_hoc_phan.h */
#define PAGE_SIZE   5   /* so lop in tren 1 trang bang ke (unwind_bound cua BMC-03/04) */
#define DINH_MUC_TIEN_CHUAN 85000LL  /* Config.dinhMucTienChuan trong main.c */

/* Ban rut gon cua LopHocPhan (lop_hoc_phan.h) - bo gv_ptr vi Lab 6 chi quan tam
 * den TINH HOP LE CUA CHI SO mang, khong phai vong doi con tro (do la Lab 3). */
typedef struct {
    int   id;
    char  maLop[MAX_MALOP];
    int   soTiet;
    float heSoHocPhan;
    int   soLuongSinhVien;
} LopHocPhanEntry;

static void fill_danh_sach_lop(LopHocPhanEntry ds[MAX_LOP]) {
    for (int i = 0; i < MAX_LOP; i++) {
        ds[i].id = 100 + i;
        snprintf(ds[i].maLop, sizeof(ds[i].maLop), "CNTT2024_%02d", i + 1);
        ds[i].soTiet = 30 + 3 * i;          /* 30, 33, ..., 57 tiet */
        ds[i].heSoHocPhan = 1.0f;
        ds[i].soLuongSinhVien = 40 + 5 * i;
    }
}

/* Tien day 1 lop (rut gon tu calculate_e2e_salary_SAFE, bangCap TIEN_SI = 1.5) */
static long long tien_day_lop(const LopHocPhanEntry *lhp) {
    double heSoQuyMo = (lhp->soLuongSinhVien > 50) ? 0.2 : 0.0;   /* CON-11 */
    double soTietQuyDoi = (double)lhp->soTiet * ((double)lhp->heSoHocPhan + heSoQuyMo);
    return (long long)(soTietQuyDoi * 1.5 * (double)DINH_MUC_TIEN_CHUAN);
}

/* BMC-01: duyet dung, an toan - tong hop thu lao ca hoc ky */
static void safe_full_scan(LopHocPhanEntry ds[MAX_LOP]) {
    long long tong = 0;
    for (int i = 0; i < MAX_LOP; i++) {
        long long t = tien_day_lop(&ds[i]);
        printf("  danhSachLop[%d] %-12s soTiet=%2d  tien=%lld VND\n", i, ds[i].maLop, ds[i].soTiet, t);
        tong += t;
    }
    printf("  TONG THU LAO HOC KY: %lld VND\n", tong);
}

/* BMC-02: loi off-by-one, dieu kien dung sai '<=' */
static void offbyone_scan(LopHocPhanEntry ds[MAX_LOP]) {
    long long tong = 0;
    for (int i = 0; i <= MAX_LOP; i++) {   /* !!! LOI: phai la i < MAX_LOP !!! */
        long long t = tien_day_lop(&ds[i]);  /* ASan bat tai i == 10 (doc ds[10]) */
        printf("  danhSachLop[%d] %-12s soTiet=%2d  tien=%lld VND\n", i, ds[i].maLop, ds[i].soTiet, t);
        tong += t;
    }
    printf("  TONG THU LAO HOC KY: %lld VND\n", tong);
}

/* BMC-03: base_index (offset trang) tu tham so dong lenh, KHONG kiem tra truoc vong lap */
static void symbolic_unsafe(LopHocPhanEntry ds[MAX_LOP], int base_index) {
    long long tong = 0;
    for (int i = 0; i < PAGE_SIZE; i++) {
        int index = base_index + i;    /* !!! khong kiem tra index < MAX_LOP !!! */
        long long t = tien_day_lop(&ds[index]);
        printf("  danhSachLop[%d] %-12s soTiet=%2d  tien=%lld VND\n", index, ds[index].maLop, ds[index].soTiet, t);
        tong += t;
    }
    printf("  TONG THU LAO TRANG: %lld VND\n", tong);
}

/* BMC-04: da sua - tien dieu kien truoc vong lap (tuong duong precondition_max_base) */
static void symbolic_safe(LopHocPhanEntry ds[MAX_LOP], int base_index) {
    if (base_index < 0 || base_index > MAX_LOP - PAGE_SIZE) {
        fprintf(stderr, "[TU CHOI] base_index=%d khong hop le (offset trang phai trong [0, %d])\n",
                base_index, MAX_LOP - PAGE_SIZE);
        return;
    }
    long long tong = 0;
    for (int i = 0; i < PAGE_SIZE; i++) {
        int index = base_index + i;
        long long t = tien_day_lop(&ds[index]);
        printf("  danhSachLop[%d] %-12s soTiet=%2d  tien=%lld VND\n", index, ds[index].maLop, ds[index].soTiet, t);
        tong += t;
    }
    printf("  TONG THU LAO TRANG: %lld VND\n", tong);
}

/* BMC-05 (tu them): in bang ke theo thu tu NGUOC (lop moi nhat truoc) -
 * danhSachLop[MAX_LOP - i] - LOI ngay buoc i = 0 vi MAX_LOP - 0 = 10 ngoai bien. */
static void symbolic_reverse(LopHocPhanEntry ds[MAX_LOP]) {
    for (int i = 0; i < PAGE_SIZE; i++) {
        int index = MAX_LOP - i;       /* !!! LOI: phan tu cuoi la MAX_LOP - 1 !!! */
        printf("  danhSachLop[%d] %-12s soTiet=%2d\n", index, ds[index].maLop, ds[index].soTiet);
    }
}

/* BMC-06 (tu them): ban sua cua BMC-05 - danhSachLop[MAX_LOP - 1 - i] */
static void symbolic_reverse_fixed(LopHocPhanEntry ds[MAX_LOP]) {
    for (int i = 0; i < PAGE_SIZE; i++) {
        int index = MAX_LOP - 1 - i;
        printf("  danhSachLop[%d] %-12s soTiet=%2d\n", index, ds[index].maLop, ds[index].soTiet);
    }
}

int main(int argc, char *argv[]) {
    /* Khong dem stdout: de cac dong in TRUOC khi ASan abort van hien ra (doi chieu
     * duoc "doc dung 10 lop roi moi crash o danhSachLop[10]"). */
    setvbuf(stdout, NULL, _IONBF, 0);
    LopHocPhanEntry danhSachLop[MAX_LOP];
    fill_danh_sach_lop(danhSachLop);

    const char *mode = (argc > 1) ? argv[1] : "safe_full_scan";
    int base_index = (argc > 2) ? atoi(argv[2]) : 9;  /* mac dinh = nhan chung BMC-03 */

    if (strcmp(mode, "safe_full_scan") == 0) {
        printf("=== safe_full_scan (tuong ung BMC-01) ===\n");
        safe_full_scan(danhSachLop);
    } else if (strcmp(mode, "offbyone") == 0) {
        printf("=== offbyone_scan (tuong ung BMC-02) ===\n");
        offbyone_scan(danhSachLop);
    } else if (strcmp(mode, "symbolic_unsafe") == 0) {
        printf("=== symbolic_unsafe base_index=%d (tuong ung BMC-03) ===\n", base_index);
        symbolic_unsafe(danhSachLop, base_index);
    } else if (strcmp(mode, "symbolic_safe") == 0) {
        printf("=== symbolic_safe base_index=%d (tuong ung BMC-04) ===\n", base_index);
        symbolic_safe(danhSachLop, base_index);
    } else if (strcmp(mode, "symbolic_reverse") == 0) {
        printf("=== symbolic_reverse (tuong ung BMC-05, tu them) ===\n");
        symbolic_reverse(danhSachLop);
    } else if (strcmp(mode, "symbolic_reverse_fixed") == 0) {
        printf("=== symbolic_reverse_fixed (tuong ung BMC-06, tu them) ===\n");
        symbolic_reverse_fixed(danhSachLop);
    } else {
        fprintf(stderr, "Mode khong hop le: %s\n", mode);
        return 1;
    }
    return 0;
}
