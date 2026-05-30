import axios from "axios";

export async function GetGiangVien() {
  const result = await axios.get('http://localhost:5249/GiangVien')
  return result.data
}