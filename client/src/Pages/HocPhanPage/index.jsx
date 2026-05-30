import { Select } from 'antd';
import { useReducer } from 'react';

import { Context, initialState, reducer } from './context';
import DataTable from './DataTable';
import FormModal from './FormModal';
import FunctionBar from './FunctionBar';

const { Option } = Select;

function HocPhanPage() {
  const [state, dispatch] = useReducer(reducer, initialState)

  return (
    <Context.Provider value={[state, dispatch]}>
      <div style={{ padding: '16px', backgroundColor: '#f5f5f5' }}>
        {/* Header with filters and add button */}
        <FunctionBar />

        {/* Table container */}
        <DataTable />
      </div >

      <FormModal />
    </Context.Provider>
  );
};

export default HocPhanPage;