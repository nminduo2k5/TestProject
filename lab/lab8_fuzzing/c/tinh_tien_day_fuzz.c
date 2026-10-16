/*
 * Lab 8 - Fuzz Target (DuongUniversity - Module 3 Tinh tien day)
 * ================================================================================================
 * He thong DuongUniversity Management System
 * Chuong 4: 4.5 Kiem thu hop den (black-box fuzzing), 4.6 Kiem thu hop trang (white-box fuzzing)
 *
 * Kich ban THUC TE theo dung domain BTL: cong cu dong lenh xuat bang ke tien day doc tung dong
 * lenh nhap vao (tu file cau hinh / tham so) va phan loai:
 *   - "GV:<ten>"      -> dang ky ten giang vien (an toan, snprintf vao maGV[16])
 *   - "LHP:<ma>"      -> ghi ma lop hoc phan (an toan)
 *   - cac dong khac   -> bo qua
 *
 * NHUNG mot lap trinh vien da de lai mot "kenh ghi de he so luong quan tri" (admin salary-override
 * debug channel) bi bo quen trong code production - CWE-489 Active Debug Code: neu dong lenh bat
 * dau bang tien to BI MAT "GVADM:" (magic prefix 6 ky tu) VA ky tu tiep theo la '!' (co kich hoat
 * che do ghi de), phan payload con lai duoc sao chep vao bo dem CO DINH maGV[16] bang strcpy()
 * KHONG kiem tra do dai -> CWE-121 Stack-based Buffer Overflow.
 *
 * Day la lo hong RAT KHO tim bang fuzzing hop den thuan ngau nhien: xac suat mot chuoi ngau nhien
 * khop chinh xac 6 ky tu "GVADM:" roi '!' la ~(1/68)^7, thuc te khong bao gio xay ra trong ngan
 * sach hop ly. Day chinh la ly do fuzzing HOP TRANG (dan dat boi coverage) hieu qua hon han:
 * no "leo" tuan tu qua tung lop nhanh (GVADM: -> GVADM:! -> do dai > 15) nho phan hoi do phu ma.
 *
 * Bien dich (Windows - Clang MSYS2 clang64, GCC UCRT64 khong co libasan):
 *   C:\msys64\clang64\bin\clang.exe -g -fsanitize=address --coverage -o tinh_tien_day_fuzz.exe tinh_tien_day_fuzz.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MA_GV_SIZE 16   /* giong ho GiangVien.maGiangVien[20] nhung rut gon de de tran minh hoa */

/* Kenh ghi de he so luong quan tri (CWE-489) duoc so khop TUNG KY TU mot thay vi
 * strncmp mot lan. Ly do: moi ky tu magic khop them lai di vao mot NHANH (dong lenh)
 * RIENG -> tao them coverage moi. Day chinh la cach fuzzer coverage-guided (AFL + laf-intel
 * tach phep so sanh da-byte) "leo" dan toi magic value: moi buoc khop them 1 ky tu duoc
 * thuong bang coverage moi, dan duong tim kiem. Nguoc lai fuzzer hop den khong thay coverage
 * nen phai doan dung ca chuoi "GVADM:!" (7 ky tu) cung mot luc - gan nhu bat kha thi.
 *
 * Magic prefix = "GVADM:" (6 ky tu) + co kich hoat '!' -> tong 7 ky tu bi mat. */
static void kenh_ghi_de_luong(const char *line) {
    char maGV[MA_GV_SIZE];
    /* So khop magic "GVADM:!" theo TUNG VI TRI, moi kiem tra tren MOT DONG RIENG: khop
     * them 1 ky tu -> chay qua them 1 dong lenh -> 1 nhanh coverage MOI. Fuzzer coverage-
     * guided nho vay "leo" dan den magic value (line[0..2] = 'G','V','A' da duoc bo dinh
     * tuyen o xu_ly_dong_lenh kiem tra truoc khi goi ham nay). */
    if (line[3] != 'D') return;
    if (line[4] != 'M') return;
    if (line[5] != ':') return;
    if (line[6] != '!') return;
    /* Da khop day du "GVADM:!" -> kenh debug bi bo quen duoc kich hoat */
    const char *payload = line + 7;       /* phan ghi de he so luong */
    strcpy(maGV, payload);                /* !!! CWE-121: tran neu strlen(payload) >= MA_GV_SIZE (16) !!! */
    printf("  [GVADM-OVERRIDE] ghi de he so luong cho GV: %s\n", maGV);
}

/* Bo phan tich dong lenh cau hinh cua cong cu xuat bang ke tien day */
void xu_ly_dong_lenh(const char *line) {
    char maGV[MA_GV_SIZE];

    if (line[0] == 'G' && line[1] == 'V' && line[2] == 'A') {
        /* Co ve la kenh quan tri "GVADM:..." - chuyen sang bo so khop tung ky tu magic */
        kenh_ghi_de_luong(line);
    } else if (strncmp(line, "GV:", 3) == 0) {
        snprintf(maGV, MA_GV_SIZE, "%s", line + 3);
        printf("  [GV] dang ky giang vien: %s\n", maGV);
    } else if (strncmp(line, "LHP:", 4) == 0) {
        printf("  [LHP] ghi ma lop hoc phan: %s\n", line + 4);
    } else {
        printf("  [BO QUA] dong lenh khong nhan dien: %s\n", line);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Cach dung: %s <dong_lenh>\n", argv[0]);
        return 1;
    }
    xu_ly_dong_lenh(argv[1]);
    return 0;
}
