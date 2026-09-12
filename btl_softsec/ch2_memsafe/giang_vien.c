#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "giang_vien.h"

// MODULE 1: QUẢN LÝ GIẢNG VIÊN - PHIÊN BẢN CÓ LỖ HỔNG (VULN)
GiangVien* add_lecturer_VULN(int id, const char *maGV, const char *hoTen, const char *bangCap) {
    GiangVien *gv = (GiangVien*)malloc(sizeof(GiangVien));
    if (!gv) return NULL;

    gv->id = id;
    strcpy(gv->maGiangVien, maGV);

    // LOI CWE-120: strcpy khong kiem tra do dai hoTen so voi MAX_NAME (80)
    strcpy(gv->hoTen, hoTen);

    // LOI CWE-1288: Khong validate bangCap, nhap chuoi bat ky se roi vao fallback heSoBangCap = 1.0f
    strcpy(gv->bangCap, bangCap);
    if (strcmp(bangCap, "GS") == 0)           gv->heSoBangCap = 2.0f;
    else if (strcmp(bangCap, "PGS") == 0)     gv->heSoBangCap = 1.8f;
    else if (strcmp(bangCap, "TIEN_SI") == 0) gv->heSoBangCap = 1.5f;
    else if (strcmp(bangCap, "THAC_SI") == 0) gv->heSoBangCap = 1.2f;
    else                                      gv->heSoBangCap = 1.0f;

    gv->is_deleted = 0;
    return gv;
}

void delete_lecturer_VULN(GiangVien *gv) {
    if (gv) {
        gv->is_deleted = 1;
        free(gv); // LOI CWE-416: free(gv) nhung khong cap nhat con tro o Module 2 thanh NULL!
    }
}

// MODULE 1: QUẢN LÝ GIẢNG VIÊN - PHIÊN BẢN AN TOÀN (SAFE)
GiangVien* add_lecturer_SAFE(int id, const char *maGV, const char *hoTen, const char *bangCap) {
    if (!maGV || !hoTen || !bangCap) return NULL;

    GiangVien *gv = (GiangVien*)malloc(sizeof(GiangVien));
    if (!gv) return NULL;

    gv->id = id;
    snprintf(gv->maGiangVien, sizeof(gv->maGiangVien), "%s", maGV);

    // FIX CWE-120: Bounds checking using snprintf
    snprintf(gv->hoTen, sizeof(gv->hoTen), "%s", hoTen);

    // FIX CWE-1288: Strict degree validation
    if (strcmp(bangCap, "GS") == 0)           gv->heSoBangCap = 2.0f;
    else if (strcmp(bangCap, "PGS") == 0)     gv->heSoBangCap = 1.8f;
    else if (strcmp(bangCap, "TIEN_SI") == 0) gv->heSoBangCap = 1.5f;
    else if (strcmp(bangCap, "THAC_SI") == 0) gv->heSoBangCap = 1.2f;
    else if (strcmp(bangCap, "CU_NHAN") == 0) gv->heSoBangCap = 1.0f;
    else {
        fprintf(stderr, "[SAFE ERROR] Invalid degree '%s'! Defaulting safely to CU_NHAN (1.0f)\n", bangCap);
        gv->heSoBangCap = 1.0f;
        bangCap = "CU_NHAN";
    }

    snprintf(gv->bangCap, sizeof(gv->bangCap), "%s", bangCap);
    gv->is_deleted = 0;
    return gv;
}

void delete_lecturer_SAFE(GiangVien **gv_pptr) {
    if (gv_pptr && *gv_pptr) {
        (*gv_pptr)->is_deleted = 1;
        free(*gv_pptr);
        *gv_pptr = NULL; // Nullify pointer safely
    }
}
