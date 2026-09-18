\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hcmut-report}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[a4paper]{article}

\RequirePackage[utf8]{vntex,inputenc}
\RequirePackage{anyfontsize,amsmath,amssymb}
\RequirePackage[T5]{fontenc}
\RequirePackage[fontsize=13pt]{scrextend}

\RequirePackage{geometry,graphicx,indentfirst,setspace}
\RequirePackage{booktabs}
\RequirePackage[center]{caption}

\RequirePackage{fancyhdr,hyperref}
\RequirePackage[super,square,sort]{natbib}

% Change to '[english,vietnamese]' to use Vietnamese labels
\RequirePackage[english]{babel}

% Custom commands
\newcommand{\Month}{
  \ifcase \the\month
  \or January
  \or February
  \or March
  \or April
  \or May
  \or June
  \or July
  \or August
  \or September
  \or October
  \or November
  \or December
  \fi
}

\newcommand{\@uniname}{BỘ GIÁO DỤC VÀ ĐÀO TẠO}
\newcommand{\uniname}[1]{\renewcommand{\@uniname}{#1}}

\newcommand{\@deptname}{ĐẠI HỌC PHENIKAA}
\newcommand{\deptname}[1]{\renewcommand{\@deptname}{#1}}

\newcommand{\@coursename}{Course name}
\newcommand{\coursename}[1]{\renewcommand{\@coursename}{#1}}

\newcommand{\@reporttype}{Assignment Report}
\newcommand{\reporttype}[1]{\renewcommand{\@reporttype}{#1}}

\renewcommand{\@title}{Report title}

\newcommand{\@advisor}{Advisor}
\newcommand{\advisor}[1]{\renewcommand{\@advisor}{#1}}

\newcommand{\@stuname}{STUDENT:\ H (xxxxxxx)}
\newcommand{\stuname}[1]{\renewcommand{\@stuname}{#1}}

\newcommand{\@reportplace}{HA NOI City}
\newcommand{\reportplace}[1]{\renewcommand{\@reportplace}{#1}}

\newcommand{\@reporttime}{\Month \the\year}
\newcommand{\reporttime}[1]{\renewcommand{\@reporttime}{#1}}

% Configurations
%\graphicspath{{subdir1/}{subdir2/}{subdir3/}...{subdirn/}}

% twoside=false: bat buoc geometry dung DUNG left/right co dinh tren MOI trang
% (khong tu dong dao thanh inner/outer kieu sach dong gay khi class la twoside).
\geometry{
  paper=a4paper,
  twoside=false,
  left=3cm,
  right=2cm,
  top=2cm,
  bottom=2cm,
  headheight=40pt,
  headsep=12pt
}

\setstretch{1.35}
\setlength{\parskip}{0.3\baselineskip}
\raggedbottom
\renewcommand{\arraystretch}{1.2}

% Set depth of numbering for sections and table of contents
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}

% Set depth of numbering for counters
\AtBeginDocument{\counterwithin{equation}{section}}
\AtBeginDocument{\counterwithin{table}{section}}
\AtBeginDocument{\counterwithin{figure}{section}}

\AtBeginDocument{\renewcommand*\bibname{References}}

\hypersetup{
  colorlinks=true,
  linkcolor=black,
  citecolor=red,
  urlcolor=blue
}

\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\footrulewidth}{0pt}

\pagestyle{fancy}
\fancyhf{}

% Page number at top center
\fancyhead[C]{\thepage}

%\renewcommand{\subsectionmark}[1]{\markright{\thesubsection.\ #1}}

% The drawing units are interpreted as multiples of \unitlength
% unless a unit is given
%\setlength{\unitlength}{1pt}

\if@twoside
  \fancyhead[EL]{
    \bfseries
    \begin{tabular}{rl}
      \begin{picture}(25pt,15pt)
        \put(0,-8pt){\includegraphics[width=20pt]{graphics/Logo ĐH Phenikaa V Wh.png}}
      \end{picture}
      \begin{tabular}{l}
        \ttfamily\@uniname \\
        \ttfamily\@deptname \\
      \end{tabular}
    \end{tabular}
  }
  \fancyhead[OR]{
    \bfseries
    \begin{tabular}{rl}
      \begin{tabular}{r}
        \ttfamily\@uniname \\
        \ttfamily\@deptname \\
      \end{tabular}
      \begin{picture}(25pt,15pt)
        \put(0,-8pt){\includegraphics[width=20pt]{graphics/Logo ĐH Phenikaa V Wh.png}}
      \end{picture}
    \end{tabular}
  }
  \fancyhead[EC,OC]{\thepage}
\else
  \fancyhead[R]{
    \bfseries
    \begin{tabular}{rl}
      \begin{tabular}{r}
        \ttfamily\@uniname \\
        \ttfamily\@deptname \\
      \end{tabular}
      \begin{picture}(25pt,15pt)
        \put(0,-8pt){\includegraphics[width=20pt]{graphics/Logo ĐH Phenikaa V Wh.png}}
      \end{picture}
    \end{tabular}
  }
  \fancyhead[C]{\thepage}
\fi

% Custom pages and sections
\newcommand{\coverpage}{
  \pagestyle{empty}

  \vspace*{1.3cm}
  \begin{center}

    % --- Khoi 1: co quan chu quan (nhe, lui ve sau ve mat thi giac) ---
    {\fontsize{12pt}{15pt}\selectfont \MakeUppercase{\@uniname}}\\[0.35em]
    {\fontsize{15pt}{19pt}\selectfont\bfseries \MakeUppercase{\@deptname}}\\[0.55em]
    {\color{black!55}\rule{0.62\linewidth}{0.5pt}}

    \vfill

    % --- Khoi 2: logo, la diem neo thi giac chinh cua trang bia ---
    \includegraphics[height=3.4cm,keepaspectratio]{graphics/Logo ĐH Phenikaa V Wh.png}

    \vfill

    % --- Khoi 3: hoc phan -> loai bao cao -> ten de tai (phan cap ro rang) ---
    {\fontsize{14.5pt}{18pt}\selectfont\bfseries \@coursename}\\[1.1em]
    {\fontsize{14.5pt}{18pt}\selectfont\bfseries \MakeUppercase{\@reporttype}}\\[0.7em]
    {\color{black!45}\rule{2.6cm}{0.5pt}}\\[0.9em]
    {\fontsize{14.5pt}{18pt}\selectfont\bfseries
      \parbox[c]{0.85\linewidth}{\centering \@title}}

    \vfill

    % --- Khoi 4: nguoi huong dan / sinh vien thuc hien ---
    \begin{tabular}{@{}r@{\hspace{0.9em}}l@{}}
      \fontsize{13pt}{17pt}\selectfont\bfseries Người hướng dẫn: &
        \fontsize{13pt}{17pt}\selectfont \@advisor \\[0.6em]
      \fontsize{13pt}{17pt}\selectfont\bfseries Sinh viên thực hiện: &
        \fontsize{13pt}{17pt}\selectfont \begin{tabular}[t]{@{}l@{}}\@stuname\end{tabular} \\
    \end{tabular}

    \vfill

    % --- Khoi 5: dia diem, thoi gian (dong khep trang bia) ---
    {\fontsize{13pt}{17pt}\selectfont\bfseries \MakeUppercase{\@reportplace, \@reporttime}}
  \end{center}

  \cleardoublepage
  \pagestyle{fancy}
}
