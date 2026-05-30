import { createContext, useContext } from "react";

export const Context = createContext()

export const initialState = {
    selectedKhoa: 'all',
    selectedKy: 'all',
    selectedNam: 'all',

    khoaData: [],
    namHocData: [],
    hocKiData: [],

    thongKeKhoa: [],
    thongKeHocPhan: []
}

export const reducer = (state, action) => {
    const _state = { ...state }
    const _actions = Array.isArray(action) ? action : [action]

    for (const { type, payload } of _actions) {
        const _payload = typeof payload == 'function' ? payload(_state) : payload
        console.log({ type, _payload })

        switch (type) {
            // _payload = { key: 'khoaData' | 'namHocData' | 'hocKiData', data: [] }
            case 'updateData':
                _state[_payload.key] = _payload.data
                break

            // _payload = { }
            case 'updateSelectedKy':
                _state.selectedKy = _payload
                break

            // _payload = { }
            case 'updateSelectedKhoa':
                _state.selectedKhoa = _payload
                break

            case 'updateSelectedNam':
                _state.selectedNam = _payload
                break

            default:
                break
        }
    }

    return _state
}

export function useData() { return useContext(Context) }