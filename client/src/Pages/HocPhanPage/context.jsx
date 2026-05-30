import { createContext, useContext } from "react";

export const Context = createContext()

export const initialState = {
  hocPhanList: [],
  khoaList: [],
  selectedKhoaId: 'all',
  selectedKhoa: null,
  searchText: "",
  showModal: false,
  modalMode: "add",
  form: {
    id: "",
    maHocPhan: "",
    tenHocPhan: "",
    khoaId: null,
    soTinChi: 0,
    soTiet: 0,
    heSoHocPhan: 0
  }
}

export const reducer = (state, action) => {
  const _state = { ...state }
  const _actions = Array.isArray(action) ? action : [action]

  for (const { type, payload } of _actions) switch (type) {
    // payload = []
    case "updateHocPhanList":
      _state.hocPhanList = payload
      break;

    // payload = {}
    case "updateEditForm":
      _state.form = { ...payload }
      _state.selectedKhoaId = payload.khoaId
      _state.selectedKhoa = { tenKhoa: payload.tenKhoa, id: payload.khoaId }
      break

    // update khoa
    // payload = []
    case "updateKhoaList":
      _state.khoaList = payload
      break;

    // display or hide the modal
    // payload = true | false
    case "updateModal":
      _state.showModal = payload
      break;

    // edit modal form or create modal form
    // payload = 'edit' | 'add' | undefined
    case "updateModalMode":
      _state.modalMode = payload
      break;

    // reset form state
    case "resetFormData":
      _state.form = { ...initialState.form }
      break;

    // update form state
    // name = 'maHocPhan' | 'tenHocPhan' | 'khoa' | 'soTinChi' | 'soTiet' | 'heSoHocPhan'
    case "updateForm":
      _state.form = {
        ..._state.form,
        [payload.name]: payload.value
      }
      break;

    // update selected khoa's modules
    // payload = all | faculty's id
    case "updateSelectedKhoa": {
      _state.selectedKhoaId = payload

      const khoa = _state.selectedKhoa = _state.khoaList.find(khoa => khoa.id === payload)
      if (khoa == null) _state.form = { ...initialState }
      else _state.form = {
        ..._state.form,
        khoaId: _state.selectedKhoa.id,
        maHocPhan: `${khoa?.tenVietTat}_${khoa?.soLop + 1}`
      }
      break;
    }
  }


  return _state
}

export function useData() {
  const result = useContext(Context)
  return result ?? [initialState, () => { }]
}