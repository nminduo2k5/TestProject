/*
 * secure_inventory.c - Phien ban da vá lỗi
 * DuongUniversity - Lab 3 SECURE version
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TITLE_MAX  32
#define NAME_MAX   80

typedef struct {
    int    id;
    char   title[TITLE_MAX];
    float  credit;
    int    soTiet;
} Book;

typedef struct {
    int    id;
    char   hoTen[NAME_MAX];
    char   bangCap[20];
    float  heSoBangCap;
} Lecturer;

/* CWE-121 FIXED */
int add_book_title_SAFE(Book *b, const char *title) {
    if (b == NULL || title == NULL) return -1;
    int written = snprintf(b->title, TITLE_MAX, "%s", title);
    return (written >= TITLE_MAX) ? 1 : 0;
}

/* CWE-416 FIXED */
void use_after_free_SAFE(void) {
    Lecturer *lec = (Lecturer *)malloc(sizeof(Lecturer));
    if (!lec) return;
    lec->id = 1;
    strncpy(lec->hoTen, "Kylian Mbappe", NAME_MAX - 1);
    lec->hoTen[NAME_MAX-1] = '\0';
    printf("  [SAFE] Before free: %s\n", lec->hoTen);
    free(lec);
    lec = NULL;
    if (lec != NULL) {
        printf("  [SAFE] Never reached\n");
    } else {
        printf("  [SAFE] Pointer nulled after free. Access blocked.\n");
    }
}

/* CWE-401 FIXED */
void memory_safe_alloc(int n) {
    for (int i = 0; i < n; i++) {
        Book *b = (Book *)malloc(sizeof(Book));
        if (!b) continue;
        b->id = i;
        snprintf(b->title, TITLE_MAX, "HocPhan_%03d", i);
        b->soTiet = 45;
        printf("  [SAFE] Book %d processed and freed.\n", i);
        free(b);
        b = NULL;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s [overflow|uaf|leak]\n", argv[0]);
        return 1;
    }

    Book *book = (Book *)malloc(sizeof(Book));
    if (!book) return 1;
    book->id = 1; book->credit = 3.0f; book->soTiet = 45;

    if (strcmp(argv[1], "overflow") == 0) {
        printf("[TEST SAFE] CWE-121 Buffer Overflow - PATCHED:\n");
        const char *long_title = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
        int ret = add_book_title_SAFE(book, long_title);
        printf("  snprintf return=%d (1=truncated safely)\n", ret);
        printf("  Title (truncated): %s\n", book->title);

    } else if (strcmp(argv[1], "uaf") == 0) {
        printf("[TEST SAFE] CWE-416 Use-After-Free - PATCHED:\n");
        use_after_free_SAFE();

    } else if (strcmp(argv[1], "leak") == 0) {
        printf("[TEST SAFE] CWE-401 Memory Leak - PATCHED:\n");
        memory_safe_alloc(5);
    }

    free(book);
    return 0;
}
