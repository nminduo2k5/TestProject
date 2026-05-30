import { CheckOutlined } from '@ant-design/icons';
import { Button, Card, Col, Divider, Select, Modal, Row, Space, Tag, Typography, message } from 'antd';
import { useState, useEffect } from 'react';

import { AssignGiangVienToLopHocPhan, GetLopHocPhanList } from '@/api/lopHocPhanApi';
import { GetGiangVien } from '@/api/giangVien';
import { useData } from './context';

const { Title, Text } = Typography;

function PhanCongGiangVienModal() {
  const [messageApi, contextHolder] = message.useMessage()
  const [{
    giangVienModal, filterLopHocPhan, selectedLopHocPhan, giangVienData, filterForm: { khoaId }
  }, dispatch] = useData()

  useEffect(() => {
    if (giangVienModal) {
      GetGiangVien().then(data => {
        dispatch([{ type: "updateGiangVienData", payload: data }]);
      }).catch(err => {
        console.error("Lỗi khi tải danh sách giảng viên:", err);
      });
    }
  }, [giangVienModal, dispatch]);

  const [selectedTeacher, setSelectedTeacher] = useState(null);

  const handleTeacherSelect = (_, option) => {
    if (!option) {
      setSelectedTeacher(null);
      return;
    }
    setSelectedTeacher(option.teacher);
  };

  const handleConfirmAssign = async () => {
    if (!selectedTeacher) {
      messageApi.warning('Vui lòng chọn giảng viên!');
      return;
    }

    try {
      await Promise.all(selectedLopHocPhan.map(i => AssignGiangVienToLopHocPhan({
        lopHocPhanId: i.id,
        giangVienId: selectedTeacher.id
      })));
      messageApi.success(`Đã phân công thành công ${selectedLopHocPhan.length} lớp cho ${selectedTeacher.tenGiangVien}!`);

      const result = await GetLopHocPhanList();
      dispatch([
        { type: 'updateGiangVienModal', payload: false },
        { type: 'updateSelectedRows', payload: [] },
        { type: 'updateLopHocPhanData', payload: result }
      ]);
      setSelectedTeacher(null);
    } catch (error) {
      messageApi.error('Có lỗi xảy ra khi phân công giảng viên. Vui lòng thử lại!');
      console.error('Error assigning teacher:', error);
    }
  };
  // console.log(selectedTeacher)
  return (
    <>
      {contextHolder}
      <Modal title={<p className='text-2xl uppercase font-bold' style={{ color: '#0A34A0' }}>Phân công giảng viên</p>} open={giangVienModal} footer={null} width={700}
        onCancel={() => {
          setSelectedTeacher(null)
          dispatch([
            { type: "updateGiangVienModal", payload: false },
            { type: "updateSelectedRows", payload: [] },
          ])
        }}>
        <div style={{ marginBottom: '16px' }}>
          <Title level={4} style={{ color: '#0A34A0' }}>Danh sách lớp được chọn:</Title>
          <div style={{ maxHeight: '200px', overflowY: 'auto', border: '1px solid #d9d9d9', padding: '8px', borderRadius: '4px' }}>
            {selectedLopHocPhan.map(cls => (
              <div key={cls.id} style={{ padding: '4px 0', borderBottom: '1px solid #f0f0f0' }}>
                <Space>
                  <Tag color="blue">{cls.maLop}</Tag>
                  <Text>{cls.tenLop}</Text>
                  <Text type="secondary">({cls.soLuongSinhVien} SV)</Text>
                </Space>
              </div>
            ))}
          </div>
        </div>

        <Divider />

        <div style={{ marginBottom: '16px' }}>
          <Title level={4} style={{ color: '#0A34A0' }}>Chọn giảng viên:</Title>
          <Select
            showSearch
            allowClear
            style={{ width: '100%' }}
            placeholder="Chọn hoặc nhập mã/tên để tìm giảng viên..."
            optionFilterProp="label"
            filterOption={(input, option) =>
              (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
            }
            options={giangVienData
              .filter(teacher => teacher.idKhoa == khoaId)
              .map(teacher => ({
                value: teacher.id,
                label: `${teacher.maGiangVien} - ${teacher.tenGiangVien}`,
                teacher
              }))}
            onChange={(value, option) => handleTeacherSelect(value, option)}
            onClear={() => setSelectedTeacher(null)}
            value={selectedTeacher ? selectedTeacher.id : null}
          />
        </div>

        {selectedTeacher && (
          <Card size="small" style={{ marginBottom: '16px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
            <Row gutter={16}>
              <Col span={12}>
                <Space direction="vertical" size="small">
                  <Text><strong>Mã GV:</strong> {selectedTeacher.maGiangVien}</Text>
                  <Text><strong>Tên:</strong> {selectedTeacher.tenGiangVien}</Text>
                </Space>
              </Col>
              <Col span={12}>
                <Space direction="vertical" size="small">
                  <Text><strong>Khoa:</strong> {selectedTeacher.tenKhoa}</Text>
                  <Text><strong>Email:</strong> {selectedTeacher.mail}</Text>
                </Space>
              </Col>
            </Row>
          </Card>
        )}

        <Divider />

        <Row justify="end" gutter={8}>
          <Col>
            <Button onClick={() => dispatch([
              { type: 'updateGiangVienModal', payload: false },
              { type: 'updateSelectedRows', payload: [] },
            ])}>
              Hủy
            </Button>
          </Col>
          <Col>
            <Button type="primary" icon={<CheckOutlined />} onClick={handleConfirmAssign} disabled={!selectedTeacher}>
              Xác nhận phân công
            </Button>
          </Col>
        </Row>
      </Modal>
    </>
  )
}

export default PhanCongGiangVienModal;