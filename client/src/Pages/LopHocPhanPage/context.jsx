import { createContext, useContext } from "react";

export const Context = createContext()

export const initialState = {
  hocPhanData: [],
  lopHocPhanData: [],
  filterLopHocPhan: [],
  hocKiData: [],
  giangVienData: [],
  khoaData: [],
  namHocData: [],
  selectedLopHocPhan: [],
  addModal: false,
  addBulkModal: false,
  giangVienModal: false,
  formMode: '',

  filterForm: {
    khoaId: 'all',
    namHoc: new Date().getFullYear(),
    hocKiId: 'all',
    trangThai: 'all',
    hocPhan: 'all',
    lop: ''
  },
  form: {
    id: '',
    khoaId: '',
    nam: '',
    hocPhanId: '',
    hocKiId: '',
    giangVienId: '',
    soLuongSinhVien: 0
  },
  bulkForm: {
    khoaId: '',
    nam: '',
    hocPhanId: '',
    hocKiId: '',
    giangVienId: '',
    soLuongSinhVien: 0,
    soLop: 0
  }
}

export const reducer = (state, action) => {
  console.warn('new Dispatch: ')
  const _state = { ...state }
  const _actions = Array.isArray(action) ? action : [action]

  reducerLoop: for (const { type, payload } of _actions) {
    const _payload = typeof payload == 'function' ? payload(_state) : payload

    switch (type) {
      case 'updateFormMode':
        _state.formMode = _payload
        break;

      case 'setEditForm':
        _state.form = {
          id: _payload.id,
          hocPhanId: _payload.hocPhanId,
          khoaId: _payload.khoaId,
          nam: new Date(_payload.thoiGianBatDau).getFullYear(),
          hocKiId: _payload.hocKiId,
          giangVienId: _payload.giangVienId,
          soLuongSinhVien: _payload.soLuongSinhVien
        }
        break;
      // _payload = { name: '', value }
      case 'updateBulkForm':
        _state.bulkForm = {
          ..._state.bulkForm,
          [_payload.name]: _payload.value ?? null
        }
        break

      case 'resetBulkForm':
        _state.bulkForm = {
          khoaId: '',
          nam: '',
          hocPhanId: '',
          hocKiId: '',
          giangVienId: '',
          soLuongSinhVien: 0,
          soLop: 0
        }
        break

      // _payload = []
      case 'updateFilterLopHocPhan':
        _state.filterLopHocPhan = _payload
        break

      // _payload = []
      case 'updateGiangVienData':
        _state.giangVienData = _payload
        break

      // _payload = true | false
      case 'updateGiangVienModal':
        _state.giangVienModal = _payload
        break

      // _payload = []
      case 'updateLopHocPhanData':
        _state.lopHocPhanData = _payload
        break

      // _payload = true | false
      case 'updateAddModal':
        _state.addModal = _payload
        break

      // _payload = true | false
      case 'updateAddBulkModal':
        _state.addBulkModal = _payload
        break

      // _payload = []
      case 'updateKhoaData':
        _state.khoaData = _payload
        break

      // _payload = []
      case 'updateHocPhanData':
        _state.hocPhanData = _payload
        break

      // _payload = { name: '', value }
      case 'updateForm':
        _state.form = {
          ..._state.form,
          [_payload.name]: _payload.value
        }
        break

      // _payload = { name: '', value }
      case 'updateFilterForm':
        _state.filterForm = {
          ..._state.filterForm,
          [_payload.name]: _payload.value ?? null
        }
        break

      // _payload = []
      case 'updateNamHocData':
        _state.namHocData = _payload
        break

      // _payload = []
      case "updateHocKiData":
        _state.hocKiData = _payload
        break

      case 'resetForm':
        _state.form = {
          ...initialState.form,
          // khoaId: _state.filterForm.khoaId,
          // nam: _state.filterForm.namHoc,
          // hocPhanId: _state.filterForm.hocPhan,
          // hocKiId: _state.filterForm.hocKiId
        }
        break

      // _payload = [ {}, {}, ... ]
      case 'updateSelectedRows':
        _state.selectedLopHocPhan = _payload
        break

      default:
        console.log('Failed: ', { type, _payload })
        continue reducerLoop
    }
    console.log('Success: ', { type, _payload, _state })
  }

  return _state
}

export function useData() { return useContext(Context) }