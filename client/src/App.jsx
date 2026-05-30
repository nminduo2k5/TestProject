import { BrowserRouter, Route, Routes } from "react-router";
import '@ant-design/v5-patch-for-react-19';

import MainLayout from "@/Layouts/MainLayout";

import BangCapPage from "@/Pages/BangCapPage";
import GiaoVienPage from "@/Pages/GiaovienPage";
import HocKiPage from '@/Pages/HocKiPage';
import HocPhanPage from '@/Pages/HocPhanPage';
import KhoaPage from "@/Pages/KhoaPage";
import LopHocPhanPage from '@/Pages/LopHocPhanPage';
import ThongKeLopPage from '@/Pages/ThongKeLopPage';
import ThongKePage from '@/Pages/ThongKePage';
import DinhMucTien from '@/Pages/TinhTienDay/DinhMucTien';
import HeSoLop from '@/Pages/TinhTienDay/HeSoLop';
import TienDayGiangVien from '@/Pages/TinhTienDay/TienDayGiangVien';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route path="khoa" element={<KhoaPage />} />
          <Route path="bang-cap" element={<BangCapPage />} />
          <Route path="giao-vien" element={<GiaoVienPage />} />
          <Route path="thong-ke" element={<ThongKePage />} />

          <Route path="hoc-ki" element={<HocKiPage />} />
          <Route path="hoc-phan" element={<HocPhanPage />} />
          <Route path="thoi-khoa-bieu" element={<LopHocPhanPage />} />
          <Route path="thong-ke-so-lop" element={<ThongKeLopPage />} />

          <Route path='tinh-tien-day' element={<TienDayGiangVien />} />
          <Route path='dinh-muc-tien' element={<DinhMucTien />} />
          <Route path='he-so-tinh-tien' element={<HeSoLop />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
  // return <Testing />
}

export default App
