import { PlusOutlined, SearchOutlined, } from '@ant-design/icons';
import { Button, Input, Select, Tooltip } from 'antd';
import { useContext, useEffect } from 'react';

import { GetKhoaList } from '@/api/khoaApi';
import { Context } from './context';

const { Option } = Select;

function FunctionBar() {
  const [{
    showModal, khoaList, modalMode, selectedKhoaId, selectedKhoa
  }, dispatch] = useContext(Context);

  useEffect(function () {
    GetKhoaList().then(data => dispatch([
      { type: 'updateKhoaList', payload: data },
    ]))
  }, [dispatch])

  return (
    <div className='flex justify-between items-center' style={{ backgroundColor: 'white', padding: '16px', marginBottom: '16px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
      <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
        <Select placeholder="Chọn khoa" className='w-50' size="middle" value={selectedKhoaId}
          onChange={e => dispatch([{ type: 'updateSelectedKhoa', payload: e }])}
          options={[
            { value: "all", label: "Tất cả khoa" },
            ...khoaList.map(k => ({ value: k.id, label: k.tenKhoa }))
          ]} />
        <Input placeholder="Tìm kiếm theo tên hoặc mã học phần" prefix={<SearchOutlined />} style={{ width: 280 }} size="middle" />
      </div>
      <div className='flex justify-between items-center'>
        <Tooltip title="Phải chọn khoa trước!">
          <Button disabled={selectedKhoa == null} type="primary" icon={<PlusOutlined />}
            onClick={() => dispatch([
              { type: "updateModal", payload: true },
              { type: "updateModalMode", payload: "add" }
            ])}>
            Thêm mới
          </Button>
        </Tooltip>
      </div>
    </div>
  )
}

export default FunctionBar