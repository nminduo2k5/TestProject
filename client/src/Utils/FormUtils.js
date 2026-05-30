export function getFormData(elem) {
  return Object.fromEntries(new FormData(elem));
}

export function getNextIdNumber(data = []) {
  return Math.max(...data.map(i => +i.split('-')[1]), 0) + 1
}

export function convertDateToInput(date = new Date()) {

  return `${date.getFullYear()}-${date.getMonth().toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

export function parseDateFromInput(dateString) {

  const [year, month, day] = dateString.split('-').map(Number);
  // month - 1 vì tháng trong Date bắt đầu từ 0 (0 = January)
  return new Date(year, month, day);
}