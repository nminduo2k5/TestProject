import { Card, ConfigProvider, Tabs } from 'antd';
import { useEffect, useReducer, useState } from 'react';

import { GetHocKyList } from '@/api/hocKiApi';
import { GetHocPhan } from '@/api/hocphanApi';
import { GetKhoaList } from '@/api/khoaApi';
import { GetNamHocList } from '@/api/lhpThongKeApi';
import { GetLopHocPhanList } from '@/api/lopHocPhanApi';
import { GetGiangVien } from '@/api/giangVien';

import BulkAddModal from './BulkAddModal';
import DataTable from './DataTable';
import FilterBar from './FilterBar';
import FormModal from './FormModal';
import FunctionBar from './FuntionBar';
import PhanCongGiangVienModal from './PhanCongGiangVienModal';
import { Context, initialState, reducer } from './context';
import ClassSelectionModal from './BulkAddSuccessModal';
import HocPhanDataTable from './HocPhanDataTable';

const LopHocPhanPage = () => {
  const [state, dispatch] = useReducer(reducer, initialState)
  const [activeKey, setActiveKey] = useState('1');

  useEffect(function () {
    Promise.all([
      GetLopHocPhanList(),
      GetKhoaList(),
      GetHocPhan(),
      GetNamHocList(),
      GetHocKyList(),
      GetGiangVien(),
    ]).then(data => {
      console.log('Lop hoc phan data:', data[0]);
      console.log('Hoc ky data:', data[4]);
      dispatch([
        { type: "updateLopHocPhanData", payload: data[0] },
        { type: "updateKhoaData", payload: data[1] },
        { type: "updateHocPhanData", payload: data[2] },
        { type: "updateNamHocData", payload: data[3] },
        { type: "updateHocKiData", payload: data[4] },
        { type: "updateGiangVienData", payload: data[5] }
      ])
    })
  }, [])

  return (
    <div className='m-2'>

      <Context.Provider value={[state, dispatch]}>
        <ConfigProvider
          theme={{
            components: {
              Tabs: {
                cardBg: "#2A7ED7",
                inkBarColor: "#00000000"
              },
            },
          }}>
          <Tabs
            tabBarGutter={10}
            activeKey={activeKey}
            onChange={setActiveKey}
            // animated={{ inkBar: true, tabPane: true, }}
            items={[
              {
                key: '1',
                label:
                  <p className={['px-10 py-2 rounded ', activeKey == 1 ? 'bg-blue-500 text-white border-0' : 'border'].join(' ')}>
                    Học Phần
                  </p>,
                children: (
                  <>
                    <FilterBar trangThaiFilter={[
                      { value: 'all', label: 'Tất cả trạng thái' },
                      { value: 'no', label: 'Chưa mở lớp' },
                      { value: 'yes', label: 'Đã mở lớp' },
                    ]} />

                    <HocPhanDataTable />
                  </>
                )
              },
              {
                key: '2',
                label:
                  <p className={['px-10 py-2 rounded ', activeKey == 2 ? 'bg-blue-500 text-white border-0' : 'border'].join(' ')}>
                    Lớp học phần và phân công
                  </p>,
                children: (
                  <>
                    {/* <div> */}
                    {/* <Card> */}
                    <FunctionBar />

                    <FilterBar hocPhanFilter searchFilter trangThaiFilter={[
                      { value: 'all', label: 'Tất cả trạng thái' },
                      { value: 'no', label: 'Chưa phân công' },
                      { value: 'yes', label: 'Đã phân công' },
                    ]} />

                    <DataTable />
                    {/* </Card> */}
                    {/* </div> */}

                    {/* Add/Edit Modal */}
                    <FormModal />

                    {/* Bulk Add Modal */}
                    <BulkAddModal />

                    {/* Assignment Modal */}
                    <PhanCongGiangVienModal />

                    <ClassSelectionModal />
                  </>
                )
              }
            ]} />
        </ConfigProvider>
      </Context.Provider>
    </div>
  );
};

export default LopHocPhanPage;