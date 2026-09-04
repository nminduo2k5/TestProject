#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 80
#define MAX_KHOA 50

typedef struct {
    int   id;
    char  maGiangVien[20];
    char  hoTen[MAX_NAME];      // Safe buffer with strncpy
    char  bangCap[20];          // Validated set
    float heSoBangCap;
} GiangVien;

typedef struct {
    int   id;
    char  maLop[20];
    int   soTiet;
    float heSoHocPhan;
    int   soLuongSinhVien;
} LopHocPhan;

typedef struct {
    float heSoQuyMoLop;
    long long dinhMucTienChuan; // 64-bit safe currency unit
    int   nam;
} Config;

// Ham 1: Safe lecturer parsing with bound checking & degree validation
int parse_lecturer_fixed(GiangVien *gv, const char *hoTen, const char *bangCap) {
    if (gv == NULL || hoTen == NULL || bangCap == NULL) {
        fprintf(stderr, "[ERROR] NULL pointer passed to parse_lecturer_fixed\n");
        return -1;
    }

    // FIX 1: Use strncpy with explicit null termination to prevent buffer overflow
    strncpy(gv->hoTen, hoTen, MAX_NAME - 1);
    gv->hoTen[MAX_NAME - 1] = '\0';

    // FIX 2: Validate degree strictly before setting coefficient
    if (strcmp(bangCap, "GS") == 0) {
        gv->heSoBangCap = 2.0f;
    } else if (strcmp(bangCap, "PGS") == 0) {
        gv->heSoBangCap = 1.8f;
    } else if (strcmp(bangCap, "TIEN_SI") == 0) {
        gv->heSoBangCap = 1.5f;
    } else if (strcmp(bangCap, "THAC_SI") == 0) {
        gv->heSoBangCap = 1.2f;
    } else if (strcmp(bangCap, "CU_NHAN") == 0) {
        gv->heSoBangCap = 1.0f;
    } else {
        fprintf(stderr, "[ERROR] Bang cap khong hop le: '%s'. Cac bang cap hop le: GS, PGS, TIEN_SI, THAC_SI, CU_NHAN\n", bangCap);
        return -1; // Return error code
    }

    strncpy(gv->bangCap, bangCap, sizeof(gv->bangCap) - 1);
    gv->bangCap[sizeof(gv->bangCap) - 1] = '\0';

    return 0; // Success
}

// Ham 2: Safe salary calculation using 64-bit arithmetic (double & long long)
long long calculate_salary_fixed(GiangVien *gv, LopHocPhan *lhp, Config *cfg) {
    if (gv == NULL || lhp == NULL || cfg == NULL) {
        return -1;
    }
    
    // FIX 3: Use double for floating point calculation and long long to prevent 32-bit integer overflow
    double soTietQuyDoi = (double)lhp->soTiet * ((double)lhp->heSoHocPhan + (double)cfg->heSoQuyMoLop);
    double tienDayDouble = soTietQuyDoi * (double)gv->heSoBangCap * (double)cfg->dinhMucTienChuan;
    
    return (long long)tienDayDouble;
}

// Ham 3: Xuat bao cao
void export_report_fixed(GiangVien *gv, LopHocPhan *lhp, long long tienDay) {
    printf("[SAFE REPORT] GV: %s (%s) | Lop: %s | Tiet: %d | Tien: %lld VND\n",
           gv->hoTen, gv->bangCap, lhp->maLop, lhp->soTiet, tienDay);
}

int main() {
    Config cfg = { .heSoQuyMoLop = 0.2f, .dinhMucTienChuan = 85000, .nam = 2025 };
    GiangVien gv = { .id = 1, .maGiangVien = "DU_MESSI_10" };
    LopHocPhan lhp = { .id = 1, .maLop = "CNTT2024_01", .soTiet = 45,
                       .heSoHocPhan = 1.0f, .soLuongSinhVien = 60 };

    char name[200], cap[50];
    
    printf("--- DuongUniversity Salary Calc (Fixed Version) ---\n");
    printf("Nhap ho ten giang vien: ");
    
    // FIX 4: Check return value of fgets to handle EOF/Read errors safely
    if (fgets(name, sizeof(name), stdin) == NULL) {
        fprintf(stderr, "[ERROR] Loi doc du lieu ho ten giang vien!\n");
        return 1;
    }
    name[strcspn(name, "\r\n")] = 0;

    printf("Nhap bang cap (GS/PGS/TIEN_SI/THAC_SI/CU_NHAN): ");
    if (fgets(cap, sizeof(cap), stdin) == NULL) {
        fprintf(stderr, "[ERROR] Loi doc du lieu bang cap!\n");
        return 1;
    }
    cap[strcspn(cap, "\r\n")] = 0;

    if (parse_lecturer_fixed(&gv, name, cap) != 0) {
        fprintf(stderr, "[FAILED] Parse thong tin giang vien thất bại!\n");
        return 1;
    }

    long long tien = calculate_salary_fixed(&gv, &lhp, &cfg);
    export_report_fixed(&gv, &lhp, tien);

    return 0;
}
