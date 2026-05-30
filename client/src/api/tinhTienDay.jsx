import axios from "axios";

export async function TinhTienDay() {
  const result = axios.get('http://localhost:5249/TinhTienDay')
  return (await result).data
}

export async function GetHeSoLopHocPhan() {
  const result = axios.get('http://localhost:5249/TinhTienDay/lay-danh-sach-he-so-lop-hoc-phan')
  return (await result).data
}

export async function GetDinhMuc() {
  const result = axios.get('http://localhost:5249/TinhTienDay/lay-danh-sach-dinh-muc')
  return (await result).data
}

