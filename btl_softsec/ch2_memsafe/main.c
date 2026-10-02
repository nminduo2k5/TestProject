#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif
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
        } else if (strcmp(argv[1], "e2e_nfr_bench") == 0) {
            // Doi chung VULN cho NFR-1/NFR-2 (xem main_fixed.c) - dung ham *_VULN de xac nhan
            // ca 2 NFR khong phu thuoc vao viec ham co guard an toan hay khong (hieu nang/
            // rieng biet voi memory-safety), va de bang chung minh (khong chi lap luan) rang
            // delete_lecturer_VULN() van goi free() nen KHONG gay leak (CWE-416 la dangling
            // pointer, khac voi memory leak).
            int N = (argc > 2) ? atoi(argv[2]) : 10000;
            printf("--- E2E NFR BENCH VULN: N=%d lan lap ---\n", N);

            GiangVien *gv0 = add_lecturer_VULN(1, "DU_GV01", "Nguyen Van A", "TIEN_SI");
            LopHocPhan *lhp0 = create_class_section_VULN(1, "CNTT2024_NFR", 45, 1.0f, 60, gv0);

            // NFR-1: cung ly do dung QueryPerformanceCounter thay vi clock() nhu main_fixed.c
            // (clock() tren Windows do phan giai ~15ms, qua tho cho 1 phep tinh O(1)).
            volatile long acc = 0;
#ifdef _WIN32
            LARGE_INTEGER freq, t0, t1;
            QueryPerformanceFrequency(&freq);
            QueryPerformanceCounter(&t0);
            for (int i = 0; i < N; i++) {
                acc += calculate_e2e_salary_VULN(lhp0, &cfg);
            }
            QueryPerformanceCounter(&t1);
            double totalMs = 1000.0 * (double)(t1.QuadPart - t0.QuadPart) / (double)freq.QuadPart;
#else
            clock_t t0 = clock();
            for (int i = 0; i < N; i++) {
                acc += calculate_e2e_salary_VULN(lhp0, &cfg);
            }
            clock_t t1 = clock();
            double totalMs = 1000.0 * (double)(t1 - t0) / CLOCKS_PER_SEC;
#endif
            double avgMs = totalMs / N;
            printf("[NFR-1 PERF] %d lan calculate_e2e_salary_VULN: tong=%.3f ms, trung binh=%.6f ms/lan (nguong <10ms/lan) -> %s (acc=%ld)\n",
                   N, totalMs, avgMs, (avgMs < 10.0) ? "PASS" : "FAIL", acc);

            free(lhp0);
            free(gv0);

#ifdef _WIN32
            PROCESS_MEMORY_COUNTERS pmcBefore, pmcAfter;
            GetProcessMemoryInfo(GetCurrentProcess(), &pmcBefore, sizeof(pmcBefore));
#endif
            for (int i = 0; i < N; i++) {
                GiangVien *gv = add_lecturer_VULN(1, "DU_GV01", "Nguyen Van A", "TIEN_SI");
                LopHocPhan *lhp = create_class_section_VULN(1, "CNTT2024_NFR", 45, 1.0f, 60, gv);
                delete_lecturer_VULN(gv);
                free(lhp);
            }
#ifdef _WIN32
            GetProcessMemoryInfo(GetCurrentProcess(), &pmcAfter, sizeof(pmcAfter));
            long long driftKB = ((long long)pmcAfter.WorkingSetSize - (long long)pmcBefore.WorkingSetSize) / 1024;
            printf("[NFR-2 MEMORY] %d lan tao/xoa GiangVien+LopHocPhan: WorkingSet truoc=%llu KB, sau=%llu KB, drift=%lld KB (nguong |drift|<1024 KB) -> %s\n",
                   N, (unsigned long long)(pmcBefore.WorkingSetSize / 1024), (unsigned long long)(pmcAfter.WorkingSetSize / 1024),
                   driftKB, (driftKB < 1024 && driftKB > -1024) ? "PASS" : "FAIL");
#else
            printf("[NFR-2 MEMORY] Bo qua do khong bien dich tren Windows (can psapi.h GetProcessMemoryInfo)\n");
#endif
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
