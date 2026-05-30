import axios from "axios";

export async function GetLopHocPhanList() {
  const result = await axios.get(`http://localhost:5249/LopHocPhan`)
  return result.data
}

export async function DeleteLopHocPhan(id) {
  const result = await axios.delete(`http://localhost:5249/LopHocPhan/xoa/${id}`)
  return result.data
}

export async function CreateLopHocPhan({ hocPhanId, hocKiId, soLuongSinhVien, giangVienId = "" }) {
  const result = await axios.post(`http://localhost:5249/LopHocPhan/them-hoc-phan`, {
    hocPhanId, hocKiId, soLuongSinhVien, giangVienId
  });
  return result.data;
}

export async function AssignGiangVienToLopHocPhan({ lopHocPhanId, giangVienId }) {
  const result = await axios.post('http://localhost:5249/LopHocPhan/phan-cong-giang-vien',
    { lopHocPhanId, giangVienId });
  return result.data;
}

export async function UpdateLopHocPhan({ hocPhanId, hocKiId, giangVienId, soLuongSinhVien, id }) {
  const result = await axios.put('http://localhost:5249/LopHocPhan/sua-thong-tin', {
    hocPhanId, hocKiId, giangVienId, soLuongSinhVien, id
  })
  return result.data
}