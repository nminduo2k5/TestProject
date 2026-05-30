import axios from 'axios';

export async function UpdateDinhMucTien(data) {
  try {
    const response = await axios.post('http://localhost:5249/DinhMuc', data);
    return response.data;
  } catch (error) {
    console.error('Error updating dinh muc tien:', error);
    throw error;
  }
}

export async function GetDinhMucTien() {
  try {
    const response = await axios.get('http://localhost:5249/DinhMuc');
    return response.data;
  } catch (error) {
    console.error('Error fetching dinh muc tien:', error);
    throw error;
  }
}