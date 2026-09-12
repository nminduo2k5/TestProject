#ifndef GIANG_VIEN_H
#define GIANG_VIEN_H

#define MAX_NAME 80

// MODULE 1: QUẢN LÝ GIẢNG VIÊN (Lecturer Management Struct)
typedef struct {
    int   id;
    char  maGiangVien[20];
    char  hoTen[MAX_NAME];      // CWE-120: Buffer overflow if input > 80 chars
    char  bangCap[20];          // "CU_NHAN", "THAC_SI", "TIEN_SI", "PGS", "GS"
    float heSoBangCap;
    int   is_deleted;
} GiangVien;

GiangVien* add_lecturer_VULN(int id, const char *maGV, const char *hoTen, const char *bangCap);
GiangVien* add_lecturer_SAFE(int id, const char *maGV, const char *hoTen, const char *bangCap);
void delete_lecturer_VULN(GiangVien *gv);
void delete_lecturer_SAFE(GiangVien **gv_pptr);

#endif
