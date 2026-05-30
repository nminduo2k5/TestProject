import axios from 'axios'

export async function GetKhoaList() {
  const result = await axios.get('http://localhost:5249/Khoa')
  return result.data
}