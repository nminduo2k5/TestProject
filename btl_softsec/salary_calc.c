#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 80
#define MAX_KHOA 50

typedef struct {
    int   id;
    char  maGiangVien[20];
    char  hoTen[MAX_NAME];      // LOI CH2: strcpy khong gioi han
    char  bangCap[20];          // "CU_NHAN","THAC_SI","TIEN_SI","PGS","GS"
    float heSoBangCap;
} GiangVien;

typedef struct {
    int   id;
    char  maLop[20];
    int   soTiet;
    float heSoHocPhan;          // He so rieng cua hoc phan
    int   soLuongSinhVien;
} LopHocPhan;

typedef struct {
    float heSoQuyMoLop;         // Phu thuoc soLuongSinhVien
    long  dinhMucTienChuan;     // Don gia 1 tiet chuan (VND)
    int   nam;
} Config;

// Ham 1: Doc thong tin giang vien tu input
void parse_lecturer(GiangVien *gv, const char *hoTen, const char *bangCap) {
    // LOI CO Y 1 (Buffer Overflow): strcpy khong kiem tra do dai input so voi MAX_NAME (80)
    strcpy(gv->hoTen, hoTen);   
    
    // LOI CO Y 2 (Logic Error): Khong validate bangCap, nhap chuoi bat ky ("XYZ") 
    // se khong khop voi cai nao va roi vao fallback heSoBangCap = 1.0f (tinh sai dinh muc)
    strcpy(gv->bangCap, bangCap);
    if (strcmp(bangCap, "GS") == 0)           gv->heSoBangCap = 2.0f;
    else if (strcmp(bangCap, "PGS") == 0)     gv->heSoBangCap = 1.8f;
    else if (strcmp(bangCap, "TIEN_SI") == 0) gv->heSoBangCap = 1.5f;
    else if (strcmp(bangCap, "THAC_SI") == 0) gv->heSoBangCap = 1.2f;
    else                                      gv->heSoBangCap = 1.0f; // Default fallback for invalid degree
}

// Ham 2: Tinh tien day theo cong thuc DuongUniversity (2 buoc)
// Buoc 1: soTietQuyDoi = soTiet x (heSoHocPhan + heSoQuyMoLop)
// Buoc 2: tienDay = soTietQuyDoi x heSoBangCap x dinhMucTienChuan
long calculate_salary(GiangVien *gv, LopHocPhan *lhp, Config *cfg) {
    // LOI CO Y 3 (Integer Overflow): E-cast sang (int) va nhan cac so nguyen lon 
    // co the gay tran so 32-bit khi tinh soTietQuyDoi hoac tienDay tren mien gia tri lon
    int soTietQuyDoi = (int)(lhp->soTiet * (lhp->heSoHocPhan + cfg->heSoQuyMoLop));
    long tienDay = (long)soTietQuyDoi * gv->heSoBangCap * cfg->dinhMucTienChuan;
    return tienDay;
}

// Ham 3: Xuat bao cao
void export_report(GiangVien *gv, LopHocPhan *lhp, long tienDay) {
    printf("GV: %s (%s) | Lop: %s | Tiet: %d | Tien: %ld VND\n",
           gv->hoTen, gv->bangCap, lhp->maLop, lhp->soTiet, tienDay);
}

int main() {
    Config cfg = { .heSoQuyMoLop = 0.2f, .dinhMucTienChuan = 85000, .nam = 2025 };
    GiangVien gv = { .id = 1, .maGiangVien = "DU_MESSI_10" };
    LopHocPhan lhp = { .id = 1, .maLop = "CNTT2024_01", .soTiet = 45,
                       .heSoHocPhan = 1.0f, .soLuongSinhVien = 60 };

    char name[200], cap[50];
    
    printf("--- DuongUniversity Salary Calc (Buggy Version) ---\n");
    printf("Nhap ho ten giang vien: ");
    
    // LOI CO Y 4 (Missing NULL check): Khong kiem tra fgets() return NULL khi EOF / stream error
    if (fgets(name, sizeof(name), stdin) != NULL) {
        name[strcspn(name, "\r\n")] = 0;
    }
    
    printf("Nhap bang cap (GS/PGS/TIEN_SI/THAC_SI/CU_NHAN): ");
    if (fgets(cap, sizeof(cap), stdin) != NULL) {
        cap[strcspn(cap, "\r\n")] = 0;
    }

    parse_lecturer(&gv, name, cap);
    long tien = calculate_salary(&gv, &lhp, &cfg);
    export_report(&gv, &lhp, tien);

    return 0;
}
