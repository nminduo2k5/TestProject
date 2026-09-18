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
        } else if (strcmp(argv[1], "e2e_byte_truncate") == 0) {
            printf("--- E2E TEST: CWE-197 Numeric Truncation (int -> char) ---\n");
            int soLuongSinhVien = (argc > 2) ? atoi(argv[2]) : 60;
            char b = pack_class_size_byte_VULN(soLuongSinhVien);
            printf("[MOD-2] soLuongSinhVien (int) = %d\n", soLuongSinhVien);
            printf("[MOD-3 EXPORT] Byte da ep kieu (char) = %d\n", (int)b);
            if ((int)b != soLuongSinhVien) {
                printf("[TRUNCATION DETECTED] Gia tri BI SAI LECH sau khi ep kieu: %d -> %d\n", soLuongSinhVien, (int)b);
            }
            return 0;
        } else if (strcmp(argv[1], "e2e_memory_trace") == 0) {
            // Trace THAT dia chi con tro qua 7 buoc cua 1 luong bat ky (nhap -> tao GV -> tao lop
            // -> tinh luong -> dong goi byte -> xoa GV -> xuat bao cao), de chung minh bang dia
            // chi cu the (khong suy luan) rang buoc doc lai o Buoc 7 la CUNG mot vung nho da bi
            // free() o Buoc 6 - CWE-416 that, khong phai mo phong.
            char stackBuf[200];
            snprintf(stackBuf, sizeof(stackBuf), "Pham Van Duong");
            printf("[BUOC 1] Nhap input vao buffer STACK   : dia chi=%p  noi dung=\"%s\"\n", (void*)stackBuf, stackBuf);
            fflush(stdout);

            GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", stackBuf, "TIEN_SI");
            printf("[BUOC 2] malloc() GiangVien tren HEAP   : dia chi=%p  (gv->hoTen tai %p)\n", (void*)gv, (void*)gv->hoTen);
            fflush(stdout);

            LopHocPhan *lhp = create_class_section_VULN(1, "CNTT2024_TRACE", 45, 1.0f, 60, gv);
            printf("[BUOC 3] malloc() LopHocPhan tren HEAP  : dia chi=%p  (lhp->gv_ptr = %p  <-- TRUNG voi Buoc 2!)\n", (void*)lhp, (void*)lhp->gv_ptr);
            fflush(stdout);

            long tien = calculate_e2e_salary_VULN(lhp, &cfg);
            printf("[BUOC 4] Tinh luong (doc lai gv_ptr)    : ket qua=%ld (doc qua con tro tai dia chi %p)\n", tien, (void*)lhp->gv_ptr);
            fflush(stdout);

            char byteVal = pack_class_size_byte_VULN(lhp->soLuongSinhVien);
            printf("[BUOC 5] Ep kieu (char) so luong SV     : int=%d -> byte=%d (dia chi bien cuc bo=%p)\n", lhp->soLuongSinhVien, (int)byteVal, (void*)&byteVal);
            fflush(stdout);

            printf("[BUOC 6] free(gv) - TRA vung nho ve allocator: dia chi vua free=%p (lhp->gv_ptr VAN CON tro toi day!)\n", (void*)gv);
            fflush(stdout);
            delete_lecturer_VULN(gv);

            printf("[BUOC 7] export_report doc lai gv_ptr->hoTen SAU KHI FREE - dia chi doc=%p (== dia chi da free o Buoc 6!)\n", (void*)lhp->gv_ptr);
            fflush(stdout);
            export_report_VULN(lhp->gv_ptr, lhp, tien);
            printf("[KET LUAN] Buoc 7 vua doc THANH CONG mot vung nho DA BI FREE o Buoc 6 - day chinh la CWE-416\n");
            printf("           Use-After-Free, chung minh bang DIA CHI THAT (%p == %p), khong phai suy luan.\n", (void*)lhp->gv_ptr, (void*)gv);
            fflush(stdout);

            free(lhp);
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
