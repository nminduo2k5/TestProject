/*
 * Lab 4 - Cau truc du lieu dong: Danh sach lien ket (Linked List) quan ly
 * Danh sach Giang vien (DuongUniversity Management System)
 * ==============================================================================
 * Chuong 2: 2.2 Cau truc dong, 2.5 Cong cu phan tich tinh tim loi bao mat
 *
 * Tiep noi Lab 3 (Module Quan ly Hoc phan & Giang vien): dung DUNG hang so
 * MAX_NAME=80 that trong btl_softsec/ch2_memsafe/giang_vien.h, quan ly danh
 * sach GiangVien bang danh sach lien ket don (singly linked list) cap phat
 * dong - thay vi vi du "BookNode/Catalog sach" chung chung cua de goc, de
 * Lab 4 gan lien voi he thong that thay vi mot bai tap doc lap khong lien quan.
 *
 * File nay (booklist_v1_buggy.c) CO CHU Y chua mot so loi tinh vi de cong
 * cu phan tich tinh (cppcheck) phat hien, phuc vu Lab 4-Python
 * (static_analysis_runner.py):
 *   - Memory leak khi xoa node (quen free node bi go bo)
 *   - NULL pointer dereference tiem an (khong kiem tra malloc)
 *   - Doc bien chua khoi tao (uninitialized read) trong 1 nhanh hiem gap
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 80   /* dung nhu giang_vien.h that trong btl_softsec */

typedef struct GiangVienNode {
    char hoTen[MAX_NAME];
    int  namVaoNghe;
    struct GiangVienNode *next;
} GiangVienNode;

/* Chen node moi vao dau danh sach */
GiangVienNode *list_insert_front(GiangVienNode *head, const char *hoTen, int namVaoNghe) {
    GiangVienNode *node = (GiangVienNode *)malloc(sizeof(GiangVienNode));
    /* LOI TINH VI #1: khong kiem tra node == NULL truoc khi ghi -> neu
     * malloc that bai, day la NULL pointer dereference (CWE-476).
     * LUU Y CHINH XAC: cac ham add_lecturer_VULN()/create_class_section_VULN()
     * THAT trong btl_softsec/ch2_memsafe/giang_vien.c, lop_hoc_phan.c DEU DA
     * kiem tra malloc() tra ve NULL (if (!gv) return NULL;) - nen day KHONG
     * phai ban sao cua 1 bug cu the da ton tai trong btl_softsec. Day chinh
     * la VULN-004 (CWE-476) da duoc liet ke trong
     * lab3_secure_memory/dataset/vulnerabilities.json voi
     * "detected_by": "Code review / static analysis (Lab 4)" - tuc Lab 3 da
     * chu dong de danh lo hong nay cho Lab 4 minh hoa bang phan tich tinh. */
    snprintf(node->hoTen, MAX_NAME, "%s", hoTen);
    node->namVaoNghe = namVaoNghe;
    node->next = head;
    return node;
}

/* Xoa node dau tien co ho ten trung khop */
GiangVienNode *list_remove_by_name(GiangVienNode *head, const char *hoTen) {
    GiangVienNode *cur = head, *prev = NULL;
    while (cur != NULL) {
        if (strcmp(cur->hoTen, hoTen) == 0) {
            if (prev == NULL) {
                head = cur->next;
            } else {
                prev->next = cur->next;
            }
            /* LOI TINH VI #2 (CWE-401 memory leak): thieu free(cur) truoc
             * khi thoat khoi ham -> node bi "mo coi", khong con con tro nao
             * tro toi, khong the giai phong -> ro ri bo nho. */
            return head;
        }
        prev = cur;
        cur = cur->next;
    }
    return head;
}

/* Dem so giang vien trong danh sach, minh hoa loi doc bien chua khoi tao
 * trong nhanh hiem gap (list rong). */
int list_count_UNSAFE(GiangVienNode *head) {
    int count;              /* LOI TINH VI #3: thieu khoi tao count = 0 */
    GiangVienNode *cur = head;
    while (cur != NULL) {
        count++;             /* neu list rong, vong lap khong chay -> tra ve
                                 gia tri rac (garbage) thay vi 0 */
        cur = cur->next;
    }
    if (head == NULL) {
        return count;         /* CWE-457: Use of Uninitialized Variable */
    }
    return count;
}

void list_print(GiangVienNode *head) {
    for (GiangVienNode *cur = head; cur != NULL; cur = cur->next) {
        printf("  - %s (vao nghe %d)\n", cur->hoTen, cur->namVaoNghe);
    }
}

void list_free_all(GiangVienNode *head) {
    GiangVienNode *cur = head;
    while (cur != NULL) {
        GiangVienNode *next = cur->next;
        free(cur);
        cur = next;
    }
}

#ifndef BOOKLIST_NO_MAIN
int main(void) {
    GiangVienNode *danhSach = NULL;
    danhSach = list_insert_front(danhSach, "Lionel Messi", 2010);
    danhSach = list_insert_front(danhSach, "Cristiano Ronaldo", 2005);
    danhSach = list_insert_front(danhSach, "Kylian Mbappe", 2018);

    printf("Danh sach Giang vien hien tai:\n");
    list_print(danhSach);

    printf("So luong giang vien (ham UNSAFE, danh sach khong rong nen the hien dung): %d\n",
           list_count_UNSAFE(danhSach));

    danhSach = list_remove_by_name(danhSach, "Cristiano Ronaldo");
    printf("\nSau khi xoa 'Cristiano Ronaldo' (co memory leak an duoi):\n");
    list_print(danhSach);

    list_free_all(danhSach);
    return 0;
}
#endif
