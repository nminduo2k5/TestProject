/*
 * Lab 3 - Module Quan ly Hoc phan & Giang vien (DuongUniversity Management System) - PHIEN BAN AN TOAN
 * ==========================================================================
 * Ban sua loi tuong ung vulnerable_inventory.c, ap dung cac nguyen tac
 * lap trinh C an toan (Chuong 2 - 2.3):
 *   - Dung strncpy/snprintf thay strcpy, LUON dam bao null-terminator.
 *   - Huy lien ket cheo-struct (hp.gv_ptr = NULL) TRUOC khi free() Module 1,
 *     dung DUNG nguyen tac da ap dung trong btl_softsec/ch2_memsafe/main_fixed.c.
 *   - Giai phong moi vung nho da cap phat (khong con memory leak).
 *   - Kiem tra gia tri tra ve cua malloc/tham so dau vao.
 *   - LUON dung "%s" lam chuoi dinh dang co dinh, khong dua thang input lam
 *     format string (fix CWE-134).
 *
 * Bien dich VOI AddressSanitizer de xac nhan KHONG con loi (can Clang cua
 * moi truong MSYS2 clang64 tren Windows - xem README.md muc 0):
 *   clang -g -fsanitize=address -o secure_inventory secure_inventory.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 80     /* dung nhu giang_vien.h that */
#define MAX_MALOP 20    /* dung nhu lop_hoc_phan.h that */

/* ===== CUSTOM LEAK TRACKER (xem giai thich chi tiet trong vulnerable_inventory.c) =====
 * LeakSanitizer khong duoc ho tro tren Windows, nen dung co che dem malloc/free
 * that de xac nhan ban SAFE nay khong con leak, thay vi phu thuoc ASAN_OPTIONS=detect_leaks. */
static long g_alloc_count = 0;
static long g_free_count = 0;

static void *tracked_malloc(size_t size) {
    void *p = malloc(size);
    if (p) g_alloc_count++;
    return p;
}

static void tracked_free(void *p) {
    if (p) { free(p); g_free_count++; }
}

static void report_leaks_at_exit(void) {
    long leaked = g_alloc_count - g_free_count;
    if (leaked > 0) {
        fprintf(stderr, "[CUSTOM-LEAK-TRACKER] %ld allocation(s) leaked "
                        "(alloc=%ld, free=%ld)\n", leaked, g_alloc_count, g_free_count);
    } else {
        fprintf(stderr, "[CUSTOM-LEAK-TRACKER] No leaks detected "
                        "(alloc=%ld, free=%ld)\n", g_alloc_count, g_free_count);
    }
}

#define malloc(sz) tracked_malloc(sz)
#define free(p) tracked_free(p)

typedef struct {
    int  id;
    char hoTen[MAX_NAME];
    int  is_deleted;
} GiangVien;

typedef struct {
    int         id;
    char        maLop[MAX_MALOP];
    int         soTiet;
    GiangVien  *gv_ptr;
} HocPhan;

/* (A) Sua CWE-121: dung snprintf, luon gioi han do dai va dam bao ket thuc
 * bang '\0'. Tra ve 1 neu ma lop bi cat bot (truncated) de goi cap tren biet
 * va co the canh bao nguoi dung. */
/* (A-2) Ban sua cua ham cap phat dong: dung malloc + snprintf, luon dam bao
 * null-terminator va khong bao gio ghi vuot qua vung da cap phat. */
char *add_hocphan_malop_SAFE_HEAP(const char *maLop) {
    char *buf = (char *)malloc(MAX_MALOP);
    if (!buf) return NULL;
    snprintf(buf, MAX_MALOP, "%s", maLop);
    return buf;
}

int add_hocphan_malop_SAFE(HocPhan *hp, const char *maLop) {
    if (hp == NULL || maLop == NULL) {
        fprintf(stderr, "[LOI] Tham so NULL truyen vao add_hocphan_malop_SAFE\n");
        return -1;
    }
    int written = snprintf(hp->maLop, MAX_MALOP, "%s", maLop);
    /* snprintf tra ve so ky tu SE duoc ghi neu du cho -> neu >= MAX_MALOP
     * nghia la chuoi goc da bi cat bot. */
    return (written >= MAX_MALOP) ? 1 : 0;
}

/* (B) Sua CWE-416: huy lien ket cheo-struct (hp.gv_ptr = NULL) TRUOC KHI
 * free() Module 1 - dung DUNG nguyen tac da ap dung trong
 * btl_softsec/ch2_memsafe/main_fixed.c (fix CWE-416 that: "huy lien ket
 * cheo-module TRUOC khi Module 1 giai phong bo nho"), thay vi chi null hoa
 * con tro cuc bo (khong du de fix loi cross-struct). */
void demo_use_after_free_FIXED(void) {
    GiangVien *gv = (GiangVien *)malloc(sizeof(GiangVien));
    if (!gv) {
        fprintf(stderr, "[LOI] malloc GiangVien that bai\n");
        return;
    }
    gv->id = 1;
    strncpy(gv->hoTen, "Cristiano Ronaldo", MAX_NAME - 1);
    gv->hoTen[MAX_NAME - 1] = '\0';
    gv->is_deleted = 0;

    HocPhan hp;
    memset(&hp, 0, sizeof(hp));
    hp.id = 1;
    add_hocphan_malop_SAFE(&hp, "CNTT2024_01");
    hp.soTiet = 45;
    hp.gv_ptr = gv;

    /* FIX CWE-416: huy lien ket cheo-struct TRUOC khi giai phong bo nho,
     * tranh de hp.gv_ptr tro treo sau khi free(gv). */
    if (hp.gv_ptr == gv) {
        hp.gv_ptr = NULL;
        printf("  [SAFE CLEANUP] Da huy lien ket hp.gv_ptr truoc khi giai phong GiangVien.\n");
    }
    gv->is_deleted = 1;
    free(gv);
    gv = NULL;

    if (hp.gv_ptr) {
        printf("  [FIXED] khong bao gio den day\n");
    } else {
        printf("  [FIXED] hp.gv_ptr da duoc huy lien ket - truy cap an toan bi chan.\n");
    }
}

/* (D) Sua VULN-005 CWE-134: LUON dung "%s" lam chuoi dinh dang co dinh va
 * truyen tu_khoa nhu MOT THAM SO du lieu, khong bao gio dua thang chuoi
 * khong tin cay vao vi tri chuoi dinh dang cua ham printf-family. */
void tra_cuu_hocphan_SAFE(const char *tu_khoa) {
    printf("Ket qua tim kiem ma lop: %s\n", tu_khoa);
}

/* (C) Sua CWE-401: giai phong day du trong vong lap, khong con ro ri. */
void demo_memory_leak_FIXED(int count) {
    HocPhan **danhSachHocPhan = (HocPhan **)malloc(sizeof(HocPhan *) * (size_t)count);
    if (!danhSachHocPhan) {
        fprintf(stderr, "[LOI] malloc mang con tro that bai\n");
        return;
    }
    for (int i = 0; i < count; i++) {
        danhSachHocPhan[i] = (HocPhan *)malloc(sizeof(HocPhan));
        if (!danhSachHocPhan[i]) continue;
        danhSachHocPhan[i]->id = i;
        danhSachHocPhan[i]->soTiet = 45;
    }
    for (int i = 0; i < count; i++) {
        free(danhSachHocPhan[i]);       /* giai phong tung phan tu */
        danhSachHocPhan[i] = NULL;
    }
    free(danhSachHocPhan);               /* giai phong mang con tro */
}

int main(int argc, char *argv[]) {
    atexit(report_leaks_at_exit);

    HocPhan hp;
    memset(&hp, 0, sizeof(hp));

    const char *mode = (argc > 1) ? argv[1] : "safe_input";
    const char *payload = (argc > 2) ? argv[2] : "CNTT2024_01";

    if (strcmp(mode, "overflow") == 0) {
        printf("Demo Heap Buffer Overflow (DA SUA), payload dai %zu ky tu:\n", strlen(payload));
        char *maLop = add_hocphan_malop_SAFE_HEAP(payload);
        printf("  Ma lop (heap, an toan, co the bi cat bot): %s\n", maLop);
        free(maLop);
        return 0;
    }
    if (strcmp(mode, "uaf") == 0) {
        printf("Demo Use-After-Free (DA SUA):\n");
        demo_use_after_free_FIXED();
        return 0;
    }
    if (strcmp(mode, "leak") == 0) {
        printf("Demo Memory Leak (DA SUA):\n");
        demo_memory_leak_FIXED(5);
        printf("  (da cap phat va giai phong day du 5 HocPhan)\n");
        return 0;
    }
    if (strcmp(mode, "fmt") == 0) {
        printf("Demo Format String Bug (DA SUA, VULN-005):\n");
        const char *tu_khoa = (argc > 2) ? argv[2] : "%x %x %x %x %n";
        tra_cuu_hocphan_SAFE(tu_khoa);
        return 0;
    }

    int truncated = add_hocphan_malop_SAFE(&hp, payload);
    printf("Ma lop da luu: %s%s\n", hp.maLop, truncated ? " [DA BI CAT BOT]" : "");
    return 0;
}
