# Hướng dẫn Biên dịch Báo cáo LaTeX ra PDF

Tài liệu này hướng dẫn chi tiết cách biên dịch báo cáo `report.tex` thành file `report.pdf` (chuẩn font **Times New Roman**, cỡ chữ **13pt**, hỗ trợ tiếng Việt đầy đủ).

---

## 1. Yêu cầu môi trường

Để biên dịch báo cáo, máy tính cần cài đặt một bộ phân phối TeX (TeX Distribution):
- **Windows**: [MiKTeX](https://miktex.org/download) (khuyên dùng) hoặc [TeX Live](https://www.tug.org/texlive/).
- **Linux (Ubuntu/Debian)**: `sudo apt-get install texlive-full`
- **macOS**: [MacTeX](https://www.tug.org/mactex/)

---

## 2. Quy trình biên dịch chuẩn (Command Line)

Báo cáo sử dụng **Mục lục (TOC)**, **Danh mục hình/bảng/code (LOF/LOT/LOL)** và **Tài liệu tham khảo (BibTeX)**. Vì vậy, cần biên dịch đủ chu trình 4 bước sau:

Mở terminal (PowerShell / CMD / Bash) tại thư mục `report_latex`:

```powershell
# Bước 1: Biên dịch lần 1 để sinh file aux và thông tin trích dẫn
pdflatex -interaction=nonstopmode report.tex

# Bước 2: Biên dịch tài liệu tham khảo từ refs/references.bib
bibtex report

# Bước 3: Biên dịch lần 2 để tích hợp danh mục tham khảo vào tài liệu
pdflatex -interaction=nonstopmode report.tex

# Bước 4: Biên dịch lần 3 để đồng bộ hóa hoàn toàn Mục lục, Danh mục và Số trang
pdflatex -interaction=nonstopmode report.tex
```

> **Cách chạy nhanh (1 dòng lệnh trên PowerShell):**
> ```powershell
> pdflatex -interaction=nonstopmode report.tex; bibtex report; pdflatex -interaction=nonstopmode report.tex; pdflatex -interaction=nonstopmode report.tex
> ```

---

## 3. Biên dịch tự động bằng `latexmk` (Nếu có cài đặt Perl/latexmk)

Nếu hệ thống đã có sẵn `latexmk`, bạn chỉ cần chạy duy nhất 1 lệnh:
```bash
latexmk -pdf report.tex
```
`latexmk` sẽ tự động phân tích và chạy đủ các lượt `pdflatex` và `bibtex` cho đến khi tất cả cross-reference và mục lục đồng bộ 100%.

---

## 4. Biên dịch bằng VS Code (LaTeX Workshop)

Nếu bạn sử dụng **Visual Studio Code**:
1. Cài đặt Extension **LaTeX Workshop** (tác giả James-Yu).
2. Mở thư mục dự án và mở file `report.tex`.
3. Nhấn tổ hợp phím `Ctrl + Alt + B` (hoặc click icon **Build LaTeX project** ở thanh bên trái).
4. Chọn Recipe: `pdflatex -> bibtex -> pdflatex x2`.
5. Nhấn `Ctrl + Alt + V` để xem trước file PDF trực tiếp trong VS Code.

---

## 5. Biên dịch trên Overleaf

Nếu bạn đưa dự án lên [Overleaf](https://www.overleaf.com):
1. Nén toàn bộ thư mục `report_latex` thành file `.zip` và tải lên Overleaf.
2. Vào **Menu** (góc trên bên trái) $\to$ Đảm bảo:
   - **Compiler**: `pdfLaTeX`
   - **Main document**: `report.tex`
3. Nhấn **Recompile** (hoặc `Ctrl + Enter`).

---

## 6. Cấu trúc thư mục của báo cáo

```text
report_latex/
├── phenikaa-report.cls     # File class định dạng báo cáo (Font 13pt, lề trang, tiêu đề)
├── report.tex              # File mã nguồn LaTeX chính
├── report.pdf              # File PDF kết quả sau khi biên dịch
├── chapters/               # Nội dung các chương của báo cáo
│   ├── chuong1.tex         # Chương 1: Giới thiệu & Bài toán
│   ├── chuong2.tex         # Chương 2: Phân tích & Đặc tả hệ thống
│   ├── chuong3.tex         # Chương 3: Hiện thực mã nguồn & Điểm lỗi CWE
│   ├── chuong4.tex         # Chương 4: Kiểm chứng mô hình (Model Checking)
│   ├── chuong5.tex         # Chương 5: Kiểm chứng hình thức & Fuzzing
│   ├── chuong6.tex         # Chương 6: Bàn luận & Đánh giá kết quả
│   └── chuong7.tex         # Chương 7: Kết luận & Hướng phát triển
├── code/                   # Các đoạn mã nguồn C nhúng vào báo cáo
├── diagrams/               # Các sơ đồ kiến trúc, luồng dữ liệu (PNG/PDF)
├── graphics/               # Logo trường đại học và hình ảnh minh họa
└── refs/
    └── references.bib      # Cơ sở dữ liệu tài liệu tham khảo BibTeX
```

---

## 7. Dọn dẹp các file phụ sau biên dịch (Clean Auxiliary Files)

Sau khi biên dịch, LaTeX tạo ra các file tạm (`.aux`, `.log`, `.out`, `.toc`, `.bbl`, `.blg`, `.lof`, `.lot`, `.lol`). Nếu muốn dọn dẹp sạch sẽ:

- **PowerShell (Windows)**:
  ```powershell
  Remove-Item *.aux, *.log, *.out, *.toc, *.bbl, *.blg, *.lof, *.lot, *.lol -Force
  ```
- **Linux / macOS**:
  ```bash
  rm -f *.aux *.log *.out *.toc *.bbl *.blg *.lof *.lot *.lol
  ```
