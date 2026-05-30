import axios from "axios";

export async function GetHeSoLopHocPhan() {
  const result = await axios.get('http://localhost:5249/HeSoLopHocPhan')
  return result.data
}
export async function GetHeSoLopHocPhanTheoNam({ nam = new Date().getFullYear() }) {
  const result = await axios.get(`http://localhost:5249/HeSoLopHocPhan/${nam}`)
  return result.data
}

export async function CreateHeSoLopHocPhan({ soHocSinhToiThieu, heSo, namHoc }) {
  const result = await axios.post('http://localhost:5249/HeSoLopHocPhan', { soHocSinhToiThieu, heSo, namHoc })
  return result.data
}

export async function UpdateHeSoLopHocPhan({ id, soHocSinhToiThieu, heSo, namHoc }) {
  const result = await axios.put(`http://localhost:5249/HeSoLopHocPhan/${id}`, { soHocSinhToiThieu, heSo, namHoc })
  return result.data

}
export async function DeleteHeSoLopHocPhan({ id }) {
  const result = await axios.delete(`http://localhost:5249/HeSoLopHocPhan/${id}`)
  return result.data
}