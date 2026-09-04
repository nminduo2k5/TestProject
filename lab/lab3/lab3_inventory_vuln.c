/*
 * SecureSys - Module Inventory (DuongUniversity Management System)
 * Lab 3: Memory Safety - salary_calc module adapted
 * Ba lo hong: CWE-121 (Buffer Overflow), CWE-416 (Use-After-Free), CWE-401 (Memory Leak)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TITLE_MAX  32
#define NAME_MAX   80
#define MAX_BOOKS  10

/* ===== STRUCT DINH NGHIA ===== */
typedef struct {
    int    id;
    char   title[TITLE_MAX];   /* Buffer nho, de tran */
    float  credit;
    int    soTiet;
} Book;   /* Tuong duong HocPhan trong DuongUniversity */

typedef struct {
    int    id;
    char   hoTen[NAME_MAX];    /* Attack surface chinh */
    char   bangCap[20];
    float  heSoBangCap;
} Lecturer; /* Tuong duong GiangVien */

/* ===== VULNERABLE FUNCTIONS ===== */

/* CWE-121: Buffer Overflow - strcpy khong kiem tra do dai */
int add_book_title_VULN(Book *b, const char *title) {
    if (b == NULL || title == NULL) return -1;
    strcpy(b->title, title);   /* LOI: khong gioi han, tran heap buffer */
    return 0;
}

/* CWE-416: Use-After-Free - truy cap sau khi da free() */
Lecturer *create_lecturer_VULN(int id, const char *name) {
    Lecturer *lec = (Lecturer *)malloc(sizeof(Lecturer));
    if (!lec) return NULL;
    lec->id = id;
    strncpy(lec->hoTen, name, NAME_MAX - 1);
    lec->hoTen[NAME_MAX - 1] = '\0';
    return lec;
}

void use_after_free_VULN(void) {
    Lecturer *lec = create_lecturer_VULN(1, "Lionel Messi");
    printf("  [UAF] Before free: %s\n", lec->hoTen);
    free(lec);
    /* LOI CWE-416: Truy cap con tro sau khi free */
    printf("  [UAF] After free (VULN): id=%d, name=%s\n", lec->id, lec->hoTen);
}

/* CWE-401: Memory Leak - cap phat lap lai khong free */
void memory_leak_VULN(int n) {
    for (int i = 0; i < n; i++) {
        Book *b = (Book *)malloc(sizeof(Book));
        if (!b) continue;
        b->id = i;
        snprintf(b->title, TITLE_MAX, "HocPhan_%03d", i);
        b->soTiet = 45;
        /* LOI CWE-401: Khong free(b) -> memory leak */
        printf("  [LEAK] Allocated book %d (not freed)\n", i);
    }
}

/* ===== SECURE FUNCTIONS ===== */

/* CWE-121 FIX: snprintf gioi han do dai */
int add_book_title_SAFE(Book *b, const char *title) {
    if (b == NULL || title == NULL) return -1;
    int written = snprintf(b->title, TITLE_MAX, "%s", title);
    return (written >= TITLE_MAX) ? 1 : 0;  /* bao truncation */
}

/* CWE-416 FIX: NULL pointer sau khi free */
void use_after_free_SAFE(void) {
    Lecturer *lec = create_lecturer_VULN(1, "Cristiano Ronaldo");
    printf("  [UAF] Before free: %s\n", lec->hoTen);
    free(lec);
    lec = NULL;  /* FIX: NULL sau khi free, tranh dangling pointer */
    if (lec != NULL) {
        printf("  [UAF] After free (never reached): %s\n", lec->hoTen);
    } else {
        printf("  [UAF] After free (SAFE): pointer is NULL, access blocked.\n");
    }
}

/* CWE-401 FIX: free sau moi cap phat */
void memory_leak_SAFE(int n) {
    for (int i = 0; i < n; i++) {
        Book *b = (Book *)malloc(sizeof(Book));
        if (!b) continue;
        b->id = i;
        snprintf(b->title, TITLE_MAX, "HocPhan_%03d", i);
        b->soTiet = 45;
        printf("  [SAFE] Allocated and freed book %d\n", i);
        free(b);   /* FIX: giai phong ngay sau khi dung xong */
        b = NULL;
    }
}

/* ===== MAIN DEMO ===== */
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s [overflow|uaf|leak]\n", argv[0]);
        return 1;
    }

    Book *book = (Book *)malloc(sizeof(Book));
    if (!book) { fprintf(stderr, "malloc failed\n"); return 1; }
    book->id = 1;
    book->credit = 3.0f;
    book->soTiet = 45;

    if (strcmp(argv[1], "overflow") == 0) {
        printf("[TEST] CWE-121 Buffer Overflow Demo:\n");
        /* Payload dai 90 ky tu - VULN: tran heap buffer 32 byte */
        const char *long_title = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
        printf("  Payload length: %zu chars, buffer size: %d\n", strlen(long_title), TITLE_MAX);
        add_book_title_VULN(book, long_title);
        printf("  Title after strcpy: %s\n", book->title);

    } else if (strcmp(argv[1], "uaf") == 0) {
        printf("[TEST] CWE-416 Use-After-Free Demo:\n");
        use_after_free_VULN();

    } else if (strcmp(argv[1], "leak") == 0) {
        printf("[TEST] CWE-401 Memory Leak Demo:\n");
        memory_leak_VULN(5);
    }

    free(book);
    return 0;
}
