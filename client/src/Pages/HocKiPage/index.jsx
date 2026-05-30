import { useEffect, useReducer } from 'react';

import { GetNamHocList } from '@/api/lhpThongKeApi';

import DataForm from './DataForm';
import DataTable from './DataTable';
import FunctionBar from './FunctionBar';
import { Context, initialState, reducer } from './context';

function HocKiPage() {
  const [state, dispatch] = useReducer(reducer, initialState)

  useEffect(function () {
    GetNamHocList().then(data => dispatch([
      { type: 'updateYearList', payload: data }
    ]))
  }, [])

  return (
    <Context.Provider value={[state, dispatch]}>
      <div className='p-6 bg-white min-h-screen'>
        {/* Bộ lọc và nút thêm */}
        <FunctionBar />

        {/* Bảng dữ liệu */}
        <DataTable />

      </div>
      {/* Modal thêm/sửa */}
      <DataForm />
    </Context.Provider>
  );
};

export default HocKiPage;