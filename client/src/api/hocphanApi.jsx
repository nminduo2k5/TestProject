import axios from "axios";

export async function CreateHocPhan({ maHocPhan, tenHocPhan, heSoHocPhan, soTinChi, soTiet, khoaId }) {
  console.log(khoaId)
  const result = await axios.post("http://localhost:5249/HocPhan", {
    maHocPhan, tenHocPhan, heSoHocPhan, soTinChi, soTiet, khoaId: khoaId ?? ''
  })
  return result.data;
}


export async function GetHocPhan() {
  const result = await axios.get("http://localhost:5249/HocPhan")
  return result.data;
}

export async function DeleteHocPhan(id) {
  const result = await axios.delete(`http://localhost:5249/HocPhan`, {
    params: { id }
  })
  return result.data;
}

export async function UpdateHocPhan(id, data) {
  const result = await axios.put(`http://localhost:5249/HocPhan/sua-hoc-phan/${id}`, { ...data })
  return result.data;
}
// export async function

export async function GetHocPhanTinhTrang() {
  const result = await axios.get("http://localhost:5249/HocPhan/tinh-trang-hoc-phan")
  return result.data;
}