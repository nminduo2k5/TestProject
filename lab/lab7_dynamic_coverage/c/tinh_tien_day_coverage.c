/*
 * Lab 7 - Module 3: Tinh tien day (Salary Calculation) - ban do coverage
 * ========================================================================
 * He thong DuongUniversity Management System
 * Chuong 4: 4.1 Gioi thieu kiem thu bao mat, 4.2 Phu ma nguon (code coverage),
 *           4.3 Theo doi thuc thi chuong trinh, 4.4 Tao duong thuc thi chuong trinh
 *
 * Ham can phan tich dong: calculate_salary() - viet lai tu
 * calculate_e2e_salary_SAFE() (btl_softsec/ch2_memsafe/tinh_tien_day.c) va
 * add_lecturer_SAFE() (giang_vien.c), GOP cac rang buoc da duoc dac ta trong
 * BTL (CON-5, CON-11, CON-12, CON-13, tab:range) thanh mot ham nhieu nhanh:
 *
 *   Dac ta rut gon:
 *     - soTiet phai trong (0, 500]           -> neu khong: SALARY_INVALID_SOTIET  (CON-12)
 *     - heSoHocPhan phai > 0                  -> neu khong: SALARY_INVALID_HESO
 *     - soLuongSinhVien phai trong [0, 300]   -> neu khong: SALARY_INVALID_SV      (tab:range)
 *     - bangCap thuoc {GS 2.0, PGS 1.8, TIEN_SI 1.5, THAC_SI 1.2, CU_NHAN 1.0}
 *       -> chuoi la: SALARY_INVALID_DEGREE (CWE-1288 - TU CHOI thay vi fallback) (CON-13)
 *     - heSoQuyMo = 0.2 neu soLuongSinhVien > 50, nguoc lai 0.0            (CON-11)
 *         + lop > 50 SV con phai kiem tra co dong goi duoc vao audit byte
 *           (signed char, 0..127) hay khong -> out->audit_byte_ok           (CON-5 / CWE-197)
 *     - tienDay = soTiet * (heSoHocPhan + heSoQuyMo) * heSoBangCap * dinhMucTienChuan
 *       (double/long long - FIX CWE-190)
 *     - tienDay > 50,000,000 VND -> SALARY_APPROVAL_REQUIRED (phong ke toan duyet tay -
 *       kiem soat chi bat thuong, tuong tu nguong phe duyet don hang)
 *
 * Ham nay CO NHIEU NHANH LONG NHAU (chuoi bangCap 6 nhanh, quy mo lop long voi
 * audit byte, nguong phe duyet) - vi du dien hinh de minh hoa code coverage:
 * mot bo test co the PASS toan bo nhung khong phu het cac to hop nhanh.
 *
 * Bien dich co --coverage de sinh du lieu cho gcov:
 *   gcc --coverage -DSALARY_CLI_MAIN -o tinh_tien_day_cli tinh_tien_day_coverage.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SOTIET            500        /* CON-12: guard tren con thieu o ban VULN */
#define MAX_SV                300        /* mien nghiep vu soLuongSinhVien [0,300] (tab:range) */
#define NGUONG_QUY_MO          50        /* CON-11: literal trong cong thuc that */
#define AUDIT_BYTE_MAX        127        /* CON-5: signed char chi an toan trong [0,127] */
#define DINH_MUC_TIEN_CHUAN 85000LL      /* Config.dinhMucTienChuan trong main.c */
#define NGUONG_PHE_DUYET  50000000.0     /* 50 trieu VND / lop / hoc ky */

typedef enum {
    SALARY_OK = 0,
    SALARY_INVALID_SOTIET = 1,
    SALARY_INVALID_HESO = 2,
    SALARY_INVALID_SV = 3,
    SALARY_INVALID_DEGREE = 4,
    SALARY_APPROVAL_REQUIRED = 5
} SalaryStatus;

typedef struct {
    int       soTiet;
    float     heSoHocPhan;
    int       soLuongSinhVien;
    char      bangCap[20];        /* giong GiangVien.bangCap[20] (CON-3) */
    float     heSoBangCap;
    double    heSoQuyMo;
    int       audit_byte_ok;      /* 1 = dong goi duoc vao char, 0 = tu choi (CWE-197) */
    long long tienDay;
} SalaryResult;

SalaryStatus calculate_salary(int soTiet, float heSoHocPhan, int soLuongSinhVien,
                              const char *bangCap, SalaryResult *out) {
    if (out == NULL || bangCap == NULL) return SALARY_INVALID_DEGREE; /* phong thu (defensive) */

    if (soTiet <= 0 || soTiet > MAX_SOTIET) {
        return SALARY_INVALID_SOTIET;
    }
    if (heSoHocPhan <= 0.0f) {
        return SALARY_INVALID_HESO;
    }
    if (soLuongSinhVien < 0 || soLuongSinhVien > MAX_SV) {
        return SALARY_INVALID_SV;
    }

    /* He so bang cap - giong add_lecturer_SAFE() nhung TU CHOI chuoi la (CWE-1288) */
    float heSoBangCap;
    if (strcmp(bangCap, "GS") == 0) {
        heSoBangCap = 2.0f;
    } else if (strcmp(bangCap, "PGS") == 0) {
        heSoBangCap = 1.8f;
    } else if (strcmp(bangCap, "TIEN_SI") == 0) {
        heSoBangCap = 1.5f;
    } else if (strcmp(bangCap, "THAC_SI") == 0) {
        heSoBangCap = 1.2f;
    } else if (strcmp(bangCap, "CU_NHAN") == 0) {
        heSoBangCap = 1.0f;
    } else {
        return SALARY_INVALID_DEGREE;
    }

    /* He so quy mo lop (CON-11) long voi kiem tra audit byte (CON-5 / CWE-197) */
    double heSoQuyMo;
    int audit_byte_ok;
    if (soLuongSinhVien > NGUONG_QUY_MO) {
        heSoQuyMo = 0.2;
        if (soLuongSinhVien > AUDIT_BYTE_MAX) {
            audit_byte_ok = 0;   /* pack_class_size_byte_SAFE() se tu choi */
        } else {
            audit_byte_ok = 1;
        }
    } else {
        heSoQuyMo = 0.0;
        audit_byte_ok = 1;       /* <= 50 luon nam trong [0,127] */
    }

    /* FIX CWE-190: double / long long xuyen suot (giong calculate_e2e_salary_SAFE) */
    double soTietQuyDoi = (double)soTiet * ((double)heSoHocPhan + heSoQuyMo);
    double tienDayDouble = soTietQuyDoi * (double)heSoBangCap * (double)DINH_MUC_TIEN_CHUAN;

    out->soTiet = soTiet;
    out->heSoHocPhan = heSoHocPhan;
    out->soLuongSinhVien = soLuongSinhVien;
    snprintf(out->bangCap, sizeof(out->bangCap), "%s", bangCap);
    out->heSoBangCap = heSoBangCap;
    out->heSoQuyMo = heSoQuyMo;
    out->audit_byte_ok = audit_byte_ok;
    out->tienDay = (long long)tienDayDouble;

    if (tienDayDouble > NGUONG_PHE_DUYET) {
        return SALARY_APPROVAL_REQUIRED;
    }
    return SALARY_OK;
}

const char *salary_status_to_string(SalaryStatus s) {
    switch (s) {
        case SALARY_OK: return "OK";
        case SALARY_INVALID_SOTIET: return "INVALID_SOTIET";
        case SALARY_INVALID_HESO: return "INVALID_HESO";
        case SALARY_INVALID_SV: return "INVALID_SV";
        case SALARY_INVALID_DEGREE: return "INVALID_DEGREE";
        case SALARY_APPROVAL_REQUIRED: return "APPROVAL_REQUIRED";
        default: return "UNKNOWN";
    }
}

#ifdef SALARY_CLI_MAIN
/* CLI doc file CSV dinh dang: soTiet,heSoHocPhan,soLuongSinhVien,bangCap,expected_status
 * Chay tung dong nhu mot test case, in ket qua PASS/FAIL. */
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Cach dung: %s <test_inputs.csv>\n", argv[0]);
        return 1;
    }
    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        fprintf(stderr, "[LOI] Khong mo duoc file: %s\n", argv[1]);
        return 1;
    }
    char line[256];
    int total = 0, passed = 0;
    fgets(line, sizeof(line), fp); /* bo qua header */
    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\r\n")] = '\0';
        if (line[0] == '\0') continue;

        char *tok = strtok(line, ",");
        if (!tok) continue;
        int soTiet = atoi(tok);
        tok = strtok(NULL, ",");
        if (!tok) continue;
        float heSoHocPhan = (float)atof(tok);
        tok = strtok(NULL, ",");
        if (!tok) continue;
        int soLuongSinhVien = atoi(tok);
        tok = strtok(NULL, ",");
        if (!tok) continue;
        char bangCap[32];
        snprintf(bangCap, sizeof(bangCap), "%s", tok);
        tok = strtok(NULL, ",");
        if (!tok) continue;
        char expected[32];
        snprintf(expected, sizeof(expected), "%s", tok);

        SalaryResult result;
        memset(&result, 0, sizeof(result));
        SalaryStatus status = calculate_salary(soTiet, heSoHocPhan, soLuongSinhVien, bangCap, &result);
        const char *actual = salary_status_to_string(status);

        total++;
        int ok = (strcmp(actual, expected) == 0);
        if (ok) passed++;
        printf("[%s] soTiet=%-4d heSo=%-4.1f sv=%-4d bangCap=%-8s expected=%-18s actual=%-18s "
               "quyMo=%.1f audit=%d tien=%lld\n",
               ok ? "PASS" : "FAIL", soTiet, heSoHocPhan, soLuongSinhVien, bangCap,
               expected, actual, result.heSoQuyMo, result.audit_byte_ok, result.tienDay);
    }
    fclose(fp);
    printf("\nTong: %d/%d test PASS\n", passed, total);
    return (passed == total) ? 0 : 2;
}
#endif
