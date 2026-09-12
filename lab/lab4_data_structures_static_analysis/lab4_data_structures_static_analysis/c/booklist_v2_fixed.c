/*
 * Lab 4 - Danh sach lien ket Giang vien (DuongUniversity) - PHIEN BAN DA SUA (v2_fixed)
 * =========================================================================================
 * Sua ca 3 loi tinh vi cua booklist_v1_buggy.c, doi chieu bang cppcheck.
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

GiangVienNode *list_insert_front(GiangVienNode *head, const char *hoTen, int namVaoNghe) {
    GiangVienNode *node = (GiangVienNode *)malloc(sizeof(GiangVienNode));
    if (node == NULL) {                       /* SUA loi #1 */
        fprintf(stderr, "[LOI] malloc that bai trong list_insert_front\n");
        return head;
    }
    snprintf(node->hoTen, MAX_NAME, "%s", hoTen);
    node->namVaoNghe = namVaoNghe;
    node->next = head;
    return node;
}

GiangVienNode *list_remove_by_name(GiangVienNode *head, const char *hoTen) {
    GiangVienNode *cur = head, *prev = NULL;
    while (cur != NULL) {
        if (strcmp(cur->hoTen, hoTen) == 0) {
            if (prev == NULL) {
                head = cur->next;
            } else {
                prev->next = cur->next;
            }
            free(cur);                        /* SUA loi #2: giai phong node */
            return head;
        }
        prev = cur;
        cur = cur->next;
    }
    return head;
}

int list_count_SAFE(GiangVienNode *head) {
    int count = 0;                             /* SUA loi #3: khoi tao ro rang */
    for (GiangVienNode *cur = head; cur != NULL; cur = cur->next) {
        count++;
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
    printf("So luong giang vien: %d\n", list_count_SAFE(danhSach));

    danhSach = list_remove_by_name(danhSach, "Cristiano Ronaldo");
    printf("\nSau khi xoa 'Cristiano Ronaldo' (da giai phong dung cach):\n");
    list_print(danhSach);
    printf("So luong giang vien: %d\n", list_count_SAFE(danhSach));

    list_free_all(danhSach);
    return 0;
}
#endif
