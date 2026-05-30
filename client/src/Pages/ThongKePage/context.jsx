import { createContext } from 'react'

export const Context = createContext()

export const initialState = {
  bangCap: [],
  gioiTinh: [],
  processData: {
    gender: { totalLecturers: 0, femaleCount: 0, maleCount: 0 },
    degree: {}
  }
}

export function reducer(state, action) {
  const _state = structuredClone(state)
  const { type, payload } = action
  // console.log({ type, payload })
  switch (type) {
    case 'updateData': {
      // console.log(_state.gioiTinh)
      let totalLecturers = payload.gioiTinh.reduce((acc, item) => {
        // console.log({ acc, item })
        return acc + (item.soGiangVien ?? 0)
      }, 0);

      _state.bangCap = payload.bangCap
      _state.gioiTinh = payload.gioiTinh
      _state.khoa = payload.khoaList
      _state.bC = payload.bangCapList

      _state.processData = {
        totalLecturers: totalLecturers,
        gender: {
          femaleCount: payload.gioiTinh.reduce((acc, item) => acc + (item.gioiTinh === 1 ? item.soGiangVien : 0), 0),
          maleCount: payload.gioiTinh.reduce((acc, item) => acc + (item.gioiTinh === 0 ? item.soGiangVien : 0), 0),
        },
        degree: {
          ...payload.bangCap.reduce((acc, item) => {
            if (acc[item.maBangCap] == null)
              acc[item.maBangCap] = { name: item.tenBangCap, value: 0 }
            acc[item.maBangCap].value += item.soGiangVien
            return acc
          }, {})
        }

      }
      break
    }
    default:
      break
  }

  return _state
}