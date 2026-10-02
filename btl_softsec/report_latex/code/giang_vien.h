#ifndef GIANG_VIEN_H
#define GIANG_VIEN_H

#define MAX_NAME 80  // CON-1: buffer hoTen toi da 80 byte (REQ-3.1 / CWE-120, xem chuong2.tex tab:con)

// MODULE 1: QUẢN LÝ GIẢNG VIÊN (Lecturer Management Struct)
typedef struct {
    int   id;
    char  maGiangVien[20];      // CON-2: buffer toi da 20 byte, hang so truc tiep (REQ-3.3 / CWE-120)
    char  hoTen[MAX_NAME];      // CWE-120: Buffer overflow if input > 80 chars (CON-1)
    char  bangCap[20];          // CON-3: buffer toi da 20 byte (REQ-3.3 / CWE-120); "CU_NHAN", "THAC_SI", "TIEN_SI", "PGS", "GS"
    float heSoBangCap;
    int   is_deleted;
} GiangVien;

GiangVien* add_lecturer_VULN(int id, const char *maGV, const char *hoTen, const char *bangCap);
GiangVien* add_lecturer_SAFE(int id, const char *maGV, const char *hoTen, const char *bangCap);
void delete_lecturer_VULN(GiangVien *gv);
void delete_lecturer_SAFE(GiangVien **gv_pptr);

#endif
