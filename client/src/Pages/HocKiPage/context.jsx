import { createContext, useContext } from "react";
import dayjs from "dayjs";


export const Context = createContext()

export const initialState = {
  data: [],
  showModal: false,
  modelMode: "add",
  selectedYear: 'all',
  yearList: [2023, 2024, 2025, 2026],
  kyData: [],
  formData: {
    id: '',
    tenKi: '',
    year: new Date().getFullYear(),
    thoiGianBatDau: undefined,
    thoiGianKetThuc: undefined,
  }
}

export const reducer = (state, action) => {
  const _state = { ...state }
  const _actions = Array.isArray(action) ? action : [action]

  for (const { type, payload } of _actions) {
    const _payload = typeof payload == 'function' ? payload(_state) : payload

    // console.log({ type, payload })
    switch (type) {
      // payload = 2020 | 'all'
      case 'updateSelectedYear':
        _state.selectedYear = _payload
        break

      // payload = 'add' | 'edit' | null
      case 'updateModelMode':
        _state.modelMode = _payload
        break

      // payload = true | false
      case 'updateModel':
        _state.showModal = _payload
        break

      case 'resetFormData':
        _state.formData = { ...initialState.formData }
        break

      // payload = { name, value }
      case 'updateFormData':
        _state.formData = { ..._state.formData, [_payload.name]: _payload.value }
        break

      // payload = {}
      case 'setFormData':
        _state.formData = {
          id: _payload.id,
          tenKi: _payload.tenKi,
          year: new Date(_payload.thoiGianBatDau).getFullYear(),
          thoiGianBatDau: dayjs(_payload.thoiGianBatDau),
          thoiGianKetThuc: dayjs(_payload.thoiGianKetThuc)
        }
        break

      // payload = []
      case 'updateYearList':
        _state.yearList = _payload
        break

      // payload = []
      case 'updateKyData':
        _state.kyData = _payload
        break

      default:
        break;
    }
  }

  return _state
}

export function useData() {
  const result = useContext(Context)
  return result ?? [initialState, () => { }]
}

