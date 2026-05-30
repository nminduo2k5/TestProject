import axios from "axios";

export async function GetNamHocList() {
  const result = await axios.get('http://localhost:5249/LopHocPhanThongKe/nam-hoc-ki')
  return result.data
}

export async function GetThongKeLopHocPhanTheoKhoa() {
  const reuslt = await axios.get('http://localhost:5249/LopHocPhanThongKe/thong-ke-khoa')
  return reuslt.data
}

export async function GetThongKeLopHocPhanTheoHocPhan(date = new Date(1990, 0, 1)) {
  const reuslt = await axios.get('http://localhost:5249/LopHocPhanThongKe/thong-ke-hoc-phan', date && {
    params: {
      dateTime: new Date(date).toLocaleDateString()
    }
  })
  return reuslt.data
}
export async function GetThongKeLopHocPhanTheoHocKi(hocKi) {
  const reuslt = await axios.get('http://localhost:5249/LopHocPhanThongKe/thong-ke-hoc-ki', {
    params: { hocKi }
  })
  return reuslt.data
}