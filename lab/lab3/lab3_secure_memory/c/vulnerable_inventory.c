/*
 * Lab 3 - Module Quan ly Hoc phan & Giang vien (DuongUniversity Management System)
 * =========================================================================
 * Chuong 2: 2.1 Danh gia rui ro, 2.3 Lap trinh C an toan (Quan ly bo nho)
 *
 * Dung DUNG kien truc struct thuc te cua he thong DuongUniversity (xem
 * btl_softsec/ch2_memsafe/giang_vien.h, lop_hoc_phan.h):
 *   - Hang so MAX_NAME=80, MAX_MALOP=20 GIONG HET ban that.
 *   - HocPhan.gv_ptr la CON TRO GiangVien* that (khong phai chuoi ten copy),
 *     dung dung co che lien ket cheo-struct that gay ra CWE-416/476 trong
 *     btl_softsec (Module 2 giu con tro toi Module 1).
 *   - Truong gay tran (maLop[MAX_MALOP]) dung dung ten va kich thuoc that.
 * Nho vay lab3 khong chi doi ten struct/ham ma con tai hien DUNG co che loi
 * dang ton tai that trong he thong, thay vi mot bai tap doc lap khong lien quan.
 *
 * File nay CHU Y chua 4 loai loi bo nho/dinh dang pho bien (CWE) MOT CACH
 * CO CHU Y de phuc vu muc dich giao duc (phat hien bang AddressSanitizer):
 *   (A) CWE-121 Buffer Overflow       - ham add_hocphan_malop_UNSAFE()
 *   (B) CWE-416 Use After Free        - ham demo_use_after_free() (qua con tro gv_ptr)
 *   (C) CWE-401 Memory Leak           - ham demo_memory_leak()
 *   (D) CWE-134 Format String (VULN-005 tu them) - ham tra_cuu_hocphan_UNSAFE()
 *
 * KHONG dung file nay trong san pham that. Muc dich: doi chieu voi
 * secure_inventory.c (ban da sua) va cong cu risk_assessor.py (Lab3-Python).
 *
 * Bien dich VOI AddressSanitizer de phat hien loi runtime (can Clang cua moi
 * truong MSYS2 clang64 tren Windows - xem README.md muc 0):
 *   clang -g -fsanitize=address -o vulnerable_inventory vulnerable_inventory.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 80     /* dung nhu giang_vien.h that */
#define MAX_MALOP 20    /* dung nhu lop_hoc_phan.h that */

/* ===== CUSTOM LEAK TRACKER =====
 * LeakSanitizer (LSan) KHONG duoc ho tro tren Windows - chay thu se bao
 * "AddressSanitizer: detect_leaks is not supported on this platform" (day la
 * gioi han chinh thuc cua LLVM/compiler-rt, khong phai loi cau hinh cua bai
 * nay). De van co the xac nhan that su lo hong CWE-401 tren Windows, ta tu
 * dem malloc/free that qua 2 ham bao boc mong ben duoi, roi bao cao chenh
 * lech tai atexit(). Day la co che dem THAT (khong gia lap), chi ap dung
 * rieng cho phan malloc/free duoc goi QUA 2 ham nay trong file. */
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

/* Tu diem nay tro di, moi loi goi malloc()/free() trong file se duoc dinh
 * tuyen qua tracked_malloc()/tracked_free() (macro thay the van ban thuan
 * tuy - vi vay phai dat SAU dinh nghia 2 ham tren de tranh de quy vo han). */
#define malloc(sz) tracked_malloc(sz)
#define free(p) tracked_free(p)

/* GiangVien - rut gon tu GiangVien that trong btl_softsec/ch2_memsafe/giang_vien.h
 * (chi giu id/hoTen/is_deleted can cho demo; bo maGiangVien/bangCap/heSoBangCap
 * vi khong anh huong toi co che loi bo nho dang minh hoa). */
typedef struct {
    int  id;
    char hoTen[MAX_NAME];   /* CWE-120 that: strcpy(gv->hoTen, hoTen) trong giang_vien.c */
    int  is_deleted;
} GiangVien;

/* HocPhan - rut gon tu LopHocPhan that trong btl_softsec/ch2_memsafe/lop_hoc_phan.h
 * (chi giu id/maLop/soTiet/gv_ptr can cho demo; bo heSoHocPhan/soLuongSinhVien).
 * QUAN TRONG: gv_ptr la CON TRO THAT toi GiangVien - dung DUNG co che lien
 * ket cheo-module gay ra CWE-416/CWE-476 trong he thong that. */
typedef struct {
    int         id;
    char        maLop[MAX_MALOP];  /* CWE-120 that: tran neu input > 20 ky tu */
    int         soTiet;
    GiangVien  *gv_ptr;             /* con tro lien ket Module 1 - CWE-416 UAF / CWE-476 NULL */
} HocPhan;

/* (A) CWE-121: strcpy KHONG kiem tra do dai nguon -> tran field trong struct
 * HocPhan neu 'maLop' dai hon 19 ky tu (+ '\0'). Y HET CWE-120 that trong
 * btl_softsec/ch2_memsafe/lop_hoc_phan.c (strcpy(lhp->maLop, maLop)). */
void add_hocphan_malop_UNSAFE(HocPhan *hp, const char *maLop) {
    strcpy(hp->maLop, maLop);   /* !!! KHONG BAO GIO dung strcpy voi input khong tin cay !!! */
}

/* (A-2) Bien the CAP PHAT DONG (heap) cua cung loi tren, dung de
 * AddressSanitizer PHAT HIEN RO RANG hon: khi 'maLop' nam trong mot khoi
 * cap phat rieng (khong chung struct voi field khac), ASan se chen "redzone"
 * (vung dem bao ve) ngay sau khoi, nen ghi vuot qua se bi bat ngay lap tuc.
 * (Ghi chu su pham: tran trong 1 truong cua struct - nhu ham tren - co the
 * chi de ghi de len field ke ben (tham chi de ghi de CA CON TRO gv_ptr!) ma
 * KHONG bi ASan bat, vi van nam trong cung mot vung cap phat -> day la ly do
 * vi sao "chay khong bao loi" KHONG co nghia la "an toan"!) */
char *add_hocphan_malop_UNSAFE_HEAP(const char *maLop) {
    char *buf = (char *)malloc(MAX_MALOP);
    if (!buf) return NULL;
    strcpy(buf, maLop);        /* !!! tran heap neu strlen(maLop) >= MAX_MALOP !!! */
    return buf;
}

/* (B) CWE-416 Use-After-Free: DUNG DUNG co che that trong btl_softsec - Module 2
 * (HocPhan) giu con tro toi Module 1 (GiangVien) qua gv_ptr; khi Module 1 goi
 * free(gv) ma KHONG cap nhat lien ket o Module 2 thanh NULL, HocPhan van con
 * con tro treo (dangling pointer) toi vung nho da giai phong. */
void demo_use_after_free(void) {
    GiangVien *gv = (GiangVien *)malloc(sizeof(GiangVien));
    if (!gv) return;
    gv->id = 1;
    strcpy(gv->hoTen, "Lionel Messi");
    gv->is_deleted = 0;

    HocPhan hp;
    memset(&hp, 0, sizeof(hp));
    hp.id = 1;
    strcpy(hp.maLop, "CNTT2024_01");
    hp.soTiet = 45;
    hp.gv_ptr = gv;   /* lien ket con tro cheo-struct - dung DUNG mo hinh that */

    /* LOI CWE-416: free(gv) nhung KHONG cap nhat hp.gv_ptr = NULL -> y het
     * loi that trong btl_softsec/ch2_memsafe/giang_vien.c ham
     * delete_lecturer_VULN(): free(gv) ma khong huy lien ket o Module 2. */
    free(gv);

    /* Truy cap qua con tro da free THONG QUA STRUCT HocPhan - dung CHINH co
     * che cross-module that (Module 2 doc du lieu Module 1 da bi free). */
    printf("  [UAF] (khong an toan) ten giang vien qua hp.gv_ptr sau khi free: %s\n", hp.gv_ptr->hoTen);
}

/* (D) VULN-005 tu them - CWE-134 Format String Bug: dua thang input nguoi
 * dung (tu khoa tim kiem ma lop) lam CHUOI DINH DANG (format string) cho
 * printf() thay vi du lieu. Neu nguoi dung go "%x %x %x %n" (khong co doi so
 * tuong ung), printf() se doc cac "con tro"/gia tri rac tu stack/register va
 * co gang giai tham chieu chung nhu char*, thuong dan den doc bo nho ngoai y
 * muon hoac crash (rui ro ro ri thong tin qua %x/%s, hoac trong truong hop
 * xau hon la GHI de bo nho tuy y qua dac ta %n). Day la lop loi kinh dien
 * khac CWE-121/416/401. */
void tra_cuu_hocphan_UNSAFE(const char *tu_khoa) {
    printf("Ket qua tim kiem ma lop: ");
    printf(tu_khoa);   /* !!! LOI CWE-134: tu_khoa dung truc tiep lam format string !!! */
    printf("\n");
}

/* (C) CWE-401 Memory Leak: cap phat HocPhan lap lai nhung khong bao gio giai
 * phong - y het CWE-401 minh hoa trong btl_softsec (vong lap tao lop hoc phan
 * khong free). */
void demo_memory_leak(int count) {
    for (int i = 0; i < count; i++) {
        HocPhan *hp = (HocPhan *)malloc(sizeof(HocPhan));
        if (!hp) continue;
        hp->id = i;
        hp->soTiet = 45;
        /* LOI: thieu free(hp); -> ro ri bo nho moi lan goi ham */
    }
}

int main(int argc, char *argv[]) {
    atexit(report_leaks_at_exit);

    HocPhan hp;
    memset(&hp, 0, sizeof(hp));

    const char *mode = (argc > 1) ? argv[1] : "safe_input";
    const char *payload = (argc > 2) ? argv[2] : "CNTT2024_01";

    if (strcmp(mode, "overflow") == 0) {
        printf("Demo Heap Buffer Overflow (CWE-121), payload dai %zu ky tu:\n", strlen(payload));
        char *maLop = add_hocphan_malop_UNSAFE_HEAP(payload);  /* ASan se bat neu payload qua dai */
        printf("  Ma lop (heap): %s\n", maLop);
        free(maLop);
        return 0;
    }
    if (strcmp(mode, "uaf") == 0) {
        printf("Demo Use-After-Free (CWE-416):\n");
        demo_use_after_free();
        return 0;
    }
    if (strcmp(mode, "leak") == 0) {
        printf("Demo Memory Leak (CWE-401):\n");
        demo_memory_leak(5);
        printf("  (da cap phat 5 HocPhan, KHONG giai phong -> memory leak)\n");
        return 0;
    }
    if (strcmp(mode, "fmt") == 0) {
        printf("Demo Format String Bug (CWE-134, VULN-005 tu them):\n");
        /* payload mac dinh "%x %x %x %x %n" neu khong truyen tham so rieng -
         * doc rac tren stack va co the ghi bo nho qua %n. */
        const char *tu_khoa = (argc > 2) ? argv[2] : "%x %x %x %x %n";
        tra_cuu_hocphan_UNSAFE(tu_khoa);
        return 0;
    }

    /* mode == "safe_input" (mac dinh): chi minh hoa duong chay binh thuong,
     * KHONG kich hoat loi nao, dung de doi chieu voi phien ban secure. */
    add_hocphan_malop_UNSAFE(&hp, payload);
    printf("Ma lop da luu (struct field, khong ASan-detectable neu chi tran nhe): %s\n", hp.maLop);
    return 0;
}
