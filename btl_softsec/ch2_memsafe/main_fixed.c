#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "giang_vien.h"
#include "lop_hoc_phan.h"
#include "tinh_tien_day.h"

// MAIN ENTRY POINT PHIEN BAN AN TOAN (SAFE) - dung chung 3 module voi main.c,
// chi goi cac ham *_SAFE da co san trong giang_vien.c/lop_hoc_phan.c/tinh_tien_day.c
int main(int argc, char *argv[]) {
    Config cfg = { .heSoQuyMoLop = 0.2f, .dinhMucTienChuan = 85000, .nam = 2025 };

    if (argc > 1) {
        if (strcmp(argv[1], "e2e_overflow") == 0) {
            printf("--- E2E TEST SAFE: CWE-120 Buffer Overflow Truncated ---\n");
            char long_name[120];
            memset(long_name, 'A', 119);
            long_name[119] = '\0';
            GiangVien *gv = add_lecturer_SAFE(1, "DU_GV01", long_name, "TIEN_SI");
            if (gv) {
                printf("[SAFE] GV Name truncated safely: %s (length: %zu)\n", gv->hoTen, strlen(gv->hoTen));
                free(gv);
            }
            return 0;
        } else if (strcmp(argv[1], "e2e_uaf") == 0) {
            printf("--- E2E TEST SAFE: CWE-416 Use-After-Free Blocked ---\n");
            GiangVien *gv = add_lecturer_SAFE(1, "DU_GV01", "Lionel Messi", "TIEN_SI");
            LopHocPhan *lhp = create_class_section_SAFE(1, "CNTT2024_01", 45, 1.0f, 60, gv);
            printf("[MOD-1] Created GV: %s\n", gv->hoTen);
            printf("[MOD-2] Assigned GV to Class: %s\n", lhp->maLop);

            // FIX CWE-416: Huy lien ket cheo-module TRUOC khi Module 1 giai phong bo nho,
            // tranh de lhp->gv_ptr tro treo sau khi delete_lecturer_SAFE() free(gv)
            if (lhp->gv_ptr == gv) {
                lhp->gv_ptr = NULL;
                printf("[SAFE CLEANUP] Unlinked lecturer from class section before freeing memory.\n");
            }
            delete_lecturer_SAFE(&gv);
            printf("[MOD-1] Deleted GV safely (Pointer nulled)\n");

            printf("[MOD-3] Calculating Salary for Class...\n");
            long long tien = calculate_e2e_salary_SAFE(lhp, &cfg);
            export_report_SAFE(lhp->gv_ptr, lhp, tien);
            free(lhp);
            return 0;
        } else if (strcmp(argv[1], "e2e_null") == 0) {
            printf("--- E2E TEST SAFE: CWE-476 Null Pointer Handled ---\n");
            LopHocPhan *lhp = create_class_section_SAFE(1, "CNTT2024_01", 45, 1.0f, 60, NULL);
            printf("[MOD-2] Created Unassigned Class Section: %s\n", lhp->maLop);
            printf("[MOD-3] Calculating Salary without GV...\n");
            long long tien = calculate_e2e_salary_SAFE(lhp, &cfg);
            export_report_SAFE(lhp->gv_ptr, lhp, tien);
            free(lhp);
            return 0;
        } else if (strcmp(argv[1], "e2e_integer_overflow") == 0) {
            printf("--- E2E TEST SAFE: CWE-190 Integer Overflow Prevented ---\n");
            GiangVien *gv = add_lecturer_SAFE(1, "DU_GV01", "Kylian Mbappe", "GS");
            LopHocPhan *lhp = create_class_section_SAFE(1, "BIG_CLASS_99", 50000, 2.0f, 100, gv);
            long long tien = calculate_e2e_salary_SAFE(lhp, &cfg);
            export_report_SAFE(gv, lhp, tien);
            free(lhp);
            free(gv);
            return 0;
        } else if (strcmp(argv[1], "e2e_byte_truncate") == 0) {
            printf("--- E2E TEST SAFE: CWE-197 Numeric Truncation Prevented ---\n");
            int soLuongSinhVien = (argc > 2) ? atoi(argv[2]) : 60;
            char b = 0;
            int ok = pack_class_size_byte_SAFE(soLuongSinhVien, &b);
            if (ok) {
                printf("[MOD-3 EXPORT SAFE] Byte da ep kieu (char) = %d (an toan, khop voi int goc)\n", (int)b);
            } else {
                printf("[SAFE BLOCKED] soLuongSinhVien=%d vuot pham vi char - da TU CHOI ep kieu de tranh sai lech du lieu.\n", soLuongSinhVien);
            }
            return 0;
        } else if (strcmp(argv[1], "e2e_memory_trace") == 0) {
            // Doi chung voi e2e_memory_trace cua main.c (VULN): CUNG 7 buoc, nhung dung ham
            // *_SAFE - Buoc 6 huy lien ket (gv_ptr=NULL) TRUOC khi free(), nen Buoc 7 khong con
            // doc duoc vung nho da free nua.
            char stackBuf[200];
            snprintf(stackBuf, sizeof(stackBuf), "Pham Van Duong");
            printf("[BUOC 1] Nhap input vao buffer STACK   : dia chi=%p  noi dung=\"%s\"\n", (void*)stackBuf, stackBuf);
            fflush(stdout);

            GiangVien *gv = add_lecturer_SAFE(1, "DU_GV01", stackBuf, "TIEN_SI");
            printf("[BUOC 2] malloc() GiangVien tren HEAP   : dia chi=%p  (gv->hoTen tai %p)\n", (void*)gv, (void*)gv->hoTen);
            fflush(stdout);

            LopHocPhan *lhp = create_class_section_SAFE(1, "CNTT2024_TRACE", 45, 1.0f, 60, gv);
            printf("[BUOC 3] malloc() LopHocPhan tren HEAP  : dia chi=%p  (lhp->gv_ptr = %p  <-- TRUNG voi Buoc 2!)\n", (void*)lhp, (void*)lhp->gv_ptr);
            fflush(stdout);

            long long tien = calculate_e2e_salary_SAFE(lhp, &cfg);
            printf("[BUOC 4] Tinh luong (doc lai gv_ptr)    : ket qua=%lld (doc qua con tro tai dia chi %p)\n", tien, (void*)lhp->gv_ptr);
            fflush(stdout);

            char byteVal = 0;
            pack_class_size_byte_SAFE(lhp->soLuongSinhVien, &byteVal);
            printf("[BUOC 5] Ep kieu (char) so luong SV     : int=%d -> byte=%d (dia chi bien cuc bo=%p)\n", lhp->soLuongSinhVien, (int)byteVal, (void*)&byteVal);
            fflush(stdout);

            printf("[BUOC 6-SAFE] Huy lien ket lhp->gv_ptr=NULL TRUOC khi free(gv=%p) - khac VULN o day!\n", (void*)gv);
            fflush(stdout);
            if (lhp->gv_ptr == gv) lhp->gv_ptr = NULL;
            delete_lecturer_SAFE(&gv);

            printf("[BUOC 7-SAFE] export_report kiem tra lhp->gv_ptr=%p (NULL) TRUOC khi doc - khong doc vung nho da free\n", (void*)lhp->gv_ptr);
            fflush(stdout);
            export_report_SAFE(lhp->gv_ptr, lhp, tien);
            printf("[KET LUAN] Buoc 7 KHONG doc vung nho da free (lhp->gv_ptr da la NULL tu Buoc 6) - CWE-416 da bi CHAN.\n");
            fflush(stdout);

            free(lhp);
            return 0;
        }
    }

    // Default Interactive Mode
    char name[200], cap[50], malop[50];
    printf("--- DuongUniversity E2E 3-Module System (Safe Version) ---\n");
    printf("[MOD 1] Nhap ho ten giang vien: ");
    if (fgets(name, sizeof(name), stdin) == NULL) return 1;
    name[strcspn(name, "\r\n")] = 0;

    printf("[MOD 1] Nhap bang cap (GS/PGS/TIEN_SI/THAC_SI/CU_NHAN): ");
    if (fgets(cap, sizeof(cap), stdin) == NULL) return 1;
    cap[strcspn(cap, "\r\n")] = 0;

    printf("[MOD 2] Nhap ma lop hoc phan: ");
    if (fgets(malop, sizeof(malop), stdin) == NULL) return 1;
    malop[strcspn(malop, "\r\n")] = 0;

    GiangVien *gv = add_lecturer_SAFE(1, "DU_GV01", name, cap);
    LopHocPhan *lhp = create_class_section_SAFE(1, malop, 45, 1.0f, 60, gv);

    long long tien = calculate_e2e_salary_SAFE(lhp, &cfg);
    export_report_SAFE(gv, lhp, tien);

    free(lhp);
    free(gv);
    return 0;
}
