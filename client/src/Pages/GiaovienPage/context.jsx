import { getNextIdNumber } from "@/Utils/FormUtils";
import structuredClone from '@ungap/structured-clone';
import { createContext } from "react";

export const Context = createContext()

export const intitialValue = {
  formValue: {
    giangVien: {
      maGiangVien: "",
      tenGiangVien: "",
      gioiTinh: 0,
      sinhNhat: new Date(),
      soDienThoai: "",
      mail: "",
      bangCapId: ""
    },
    khoaId: "",
    chucVuId: ""
  },
  viewOption: "all",
  mode: "create",
  giangVienData: [],
  khoaData: [],
  bangCapData: [],
  chucVuData: [],
  openForm: false
}

export function reducer(state = {}, action = {}) {
  const _state = structuredClone(state)

  const { type, payload } = action
  // console.log({ type, payload })

  switch (type) {
    case 'updateGVInput':
      _state.formValue.giangVien[payload.name] = payload.value
      break
    case "updateKhoaInput":
      _state.formValue = { ..._state.formValue, khoaId: payload }
      break
    case "updateChucVuInput":
      _state.formValue = { ..._state.formValue, chucVuId: payload }
      break
    case "updateGiangVienTable":
      _state.viewOption = payload
      break
    case "updateBangCap":
      _state.bangCapData = [...payload]
      _state.formValue.giangVien.bangCapId = payload[0]?.id
      break;
    case "updateKhoa":
      _state.khoaData = [...payload]
      _state.formValue = { ..._state.formValue, khoaId: payload[0]?.id }
      break
    case "updateChucVu":
      _state.chucVuData = [...payload]
      _state.formValue = {
        ..._state.formValue,
        chucVuId: payload[0]?.id
      }
      break
    case "updateGiangVienData":
      _state.giangVienData = payload;
      break;
    case "resetInput":
      _state.formValue = {
        giangVien: {
          maGiangVien: `GV-${getNextIdNumber(_state.giangVienData.map(i => i.maGiangVien))}`,
          tenGiangVien: "",
          gioiTinh: 0,
          sinhNhat: new Date(),
          soDienThoai: "",
          mail: "",
          bangCapId: ""
        },
        khoaId: "",
        chucVuId: ""
      }
      break
    case "openForm":
      _state.openForm = true
      break
    case "closeForm":
      _state.openForm = false
      break
    case "setEditForm":
      _state.formValue = payload;
      break
    case "updateInputMode":
      _state.mode = payload;
      break
    default:
      break;
  }

  return _state;
}

export default Context;