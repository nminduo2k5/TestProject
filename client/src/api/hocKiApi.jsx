import axios from "axios";

export async function CreateHocKy({ tenKi, thoiGianBatDau, thoiGianKetThuc }) {
  const response = await axios.post('http://localhost:5249/HocKi',
    { tenKi, thoiGianBatDau, thoiGianKetThuc });
  return response.data;

}

export async function UpdateHocKy({ id, tenKi, thoiGianBatDau, thoiGianKetThuc }) {
  const res = await axios.put('http://localhost:5249/HocKi',
    { id, tenKi, thoiGianBatDau, thoiGianKetThuc })
  // console.log(res)
  return res
}

export async function GetHocKyList() {
  try {
    const response = await axios.get('http://localhost:5249/HocKi');
    return response.data;
  } catch (error) {
    return error.response.data;
  }
}

export async function DeleteHocKy(id) {
  try {
    const result = await axios.delete(`http://localhost:5249/HocKi/${id}`)
    return result.data
  } catch (error) {
    return error
  }
}