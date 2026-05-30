import { faCopy } from '@fortawesome/free-regular-svg-icons';
import { faPlus, faUserPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Col, Row, Space, Tooltip, message } from 'antd';

import { useData } from './context';

function FunctionBar() {
  const [{
    selectedLopHocPhan, filterLopHocPhan, filterForm: { khoaId }
  }, dispatch] = useData()

  const handleAdd = () => {
    dispatch([
      { type: 'updateFormMode', payload: 'add' },
      { type: "updateAddModal", payload: true },
      { type: "updateAddBulkModal", payload: false },
      { type: 'updateGiangVienModal', payload: false },
    ])
  };

  const handleBulkAdd = () => {
    dispatch([
      { type: "updateAddModal", payload: false },
      { type: 'updateGiangVienModal', payload: false },
      { type: "updateAddBulkModal", payload: true }
    ])
  };

  return (
    <Row className='mb-5' justify="space-between" align="middle">
      <Col>
        <Space>
          <Button type="default" icon={<FontAwesomeIcon icon={faCopy} />} onClick={handleBulkAdd}>
            Tạo hàng loạt
          </Button>
          <Button type="primary" icon={<FontAwesomeIcon icon={faPlus} />} onClick={handleAdd}>
            Thêm lớp
          </Button>
          <Tooltip title="Chọn khoa và lớp chưa phân công">
            <Button
              type="primary" icon={<FontAwesomeIcon icon={faUserPlus} />}
              onClick={() => {
                if (khoaId == 'all') {
                  message.warning("Vui lòng chọn một khoa cụ thể để phân công giảng viên!");
                  return;
                }
                if (!selectedLopHocPhan?.length) {
                  message.warning("Vui lòng tick chọn ít nhất một lớp học phần chưa phân công ở dưới bảng!");
                  return;
                }
                dispatch([
                  { type: 'updateGiangVienModal', payload: true },
                  { type: 'updateAddModal', payload: false },
                  { type: 'updateAddBulkModal', payload: false }
                ])
              }}>
              Phân công giảng viên ({selectedLopHocPhan?.length || 0})
            </Button>
          </Tooltip>
        </Space>
      </Col>
    </Row>
  )
}

export default FunctionBar;