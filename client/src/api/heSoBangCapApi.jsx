import axios from "axios";

export async function GetHeSoBangCap() {
  const result = await axios.get('http://localhost:5249/HeSoBangCap')
  return result.data;
}

export async function GetHeSoBangCapNam({ nam }) {
  const result = await axios.get(`http://localhost:5249/HeSoBangCap/${nam}`)
  return result.data;
}

export async function CreateHeSoBangCap({ id, maBangCap, heSo, nam }) {
  const result = await axios.post('http://localhost:5249/HeSoBangCap', {
    id, maBangCap, heSo, nam
  })
  return result.data;
}