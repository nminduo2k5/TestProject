#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "giang_vien.h"
#include "lop_hoc_phan.h"
#include "tinh_tien_day.h"

// MAIN ENTRY POINT CHƯƠNG TRÌNH E2E 3 MÔ-ĐUN (~30 DÒNG)
int main(int argc, char *argv[]) {
    Config cfg = { .heSoQuyMoLop = 0.2f, .dinhMucTienChuan = 85000, .nam = 2025 };

    if (argc > 1) {
        if (strcmp(argv[1], "e2e_overflow") == 0) {
            printf("--- E2E TEST: CWE-120 Buffer Overflow ---\n");
            char long_name[120];
            memset(long_name, 'A', 119);
            long_name[119] = '\0';
            GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", long_name, "TIEN_SI");
            printf("GV Name created: %s\n", gv->hoTen);
            free(gv);
            return 0;
        } else if (strcmp(argv[1], "e2e_uaf") == 0) {
            printf("--- E2E TEST: CWE-416 Use-After-Free Across Modules ---\n");
            GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", "Lionel Messi", "TIEN_SI");
            LopHocPhan *lhp = create_class_section_VULN(1, "CNTT2024_01", 45, 1.0f, 60, gv);
            printf("[MOD-1] Created GV: %s\n", gv->hoTen);
            printf("[MOD-2] Assigned GV to Class: %s\n", lhp->maLop);

            delete_lecturer_VULN(gv);
            printf("[MOD-1] Deleted GV (free memory)\n");

            printf("[MOD-3] Calculating Salary for Class...\n");
            long tien = calculate_e2e_salary_VULN(lhp, &cfg);
            printf("[UAF DETECTED] Read freed memory! Tien: %ld VND\n", tien);
            free(lhp);
            return 0;
        } else if (strcmp(argv[1], "e2e_null") == 0) {
            printf("--- E2E TEST: CWE-476 Null Pointer Dereference ---\n");
            LopHocPhan *lhp = create_class_section_VULN(1, "CNTT2024_01", 45, 1.0f, 60, NULL);
            printf("[MOD-2] Created Unassigned Class Section: %s\n", lhp->maLop);
            printf("[MOD-3] Calculating Salary without GV...\n");
            long tien = calculate_e2e_salary_VULN(lhp, &cfg);
            printf("Tien: %ld VND\n", tien);
            free(lhp);
            return 0;
        } else if (strcmp(argv[1], "e2e_integer_overflow") == 0) {
            printf("--- E2E TEST: CWE-190 Integer Overflow in Salary Aggregation ---\n");
            GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", "Kylian Mbappe", "GS");
            LopHocPhan *lhp = create_class_section_VULN(1, "BIG_CLASS_99", 50000, 2.0f, 100, gv);
            long tien = calculate_e2e_salary_VULN(lhp, &cfg);
            export_report_VULN(gv, lhp, tien);
            free(lhp);
            free(gv);
            return 0;
        }
    }

    // Default Interactive Mode
    char name[200], cap[50], malop[50];
    printf("--- DuongUniversity E2E 3-Module System ---\n");
    printf("[MOD 1] Nhap ho ten giang vien: ");
    if (fgets(name, sizeof(name), stdin) != NULL) name[strcspn(name, "\r\n")] = 0;

    printf("[MOD 1] Nhap bang cap (GS/PGS/TIEN_SI/THAC_SI/CU_NHAN): ");
    if (fgets(cap, sizeof(cap), stdin) != NULL) cap[strcspn(cap, "\r\n")] = 0;

    printf("[MOD 2] Nhap ma lop hoc phan: ");
    if (fgets(malop, sizeof(malop), stdin) != NULL) malop[strcspn(malop, "\r\n")] = 0;

    GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", name, cap);
    LopHocPhan *lhp = create_class_section_VULN(1, malop, 45, 1.0f, 60, gv);

    long tien = calculate_e2e_salary_VULN(lhp, &cfg);
    export_report_VULN(gv, lhp, tien);

    free(lhp);
    free(gv);
    return 0;
}
