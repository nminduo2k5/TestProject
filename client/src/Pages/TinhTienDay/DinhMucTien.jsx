import { faCheck, faPen } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Card, Form, Input, InputNumber, message, Modal, Table, Tag } from 'antd';
import { useWatch } from 'antd/es/form/Form';
import { useEffect, useState } from 'react';

import { GetDinhMucTien, UpdateDinhMucTien } from '@/api/dinhMucTien';

function DinhMucTien() {
  const [modalVisible, setModalVisible] = useState(false);
  const [data, setData] = useState([]);
  const [form] = Form.useForm();
  const customValue = useWatch(i => i, form);
  // console.log('Form values:', customValue);

  useEffect(() => {
    GetDinhMucTien().then(response => {
      setData(response);
    })
  }, []);

  const dinhMucColumns = [
    { title: 'Loại tiết', dataIndex: 'loaiTiet', key: 'loaiTiet', render: (text) => "Tiết chuẩn" },
    { title: 'Số tiền (VNĐ)', dataIndex: 'soTien', key: 'soTien', render: (value) => value?.toLocaleString('vi-VN') },

    { title: 'Ngày cập nhật', dataIndex: 'ngayCapNhat', key: 'ngayCapNhat', render: (date) => new Date(date)?.toLocaleDateString('vi-VN') },
    {
      title: 'Thao tác', key: 'action',
      render: () => (
        <Button type="primary" size="small" onClick={() => {
          setModalVisible(true);
        }}>
          <FontAwesomeIcon icon={faPen} />
        </Button>
      ),
    },
  ];

  const lichSuColumns = [
    { title: 'Số tiền (VNĐ)', dataIndex: 'soTien', key: 'soTien', render: (value) => value.toLocaleString('vi-VN') },
    { title: 'Ngày cập nhật', dataIndex: 'ngayCapNhat', key: 'ngayCapNhat', render: (date) => new Date(date).toLocaleDateString('vi-VN') },
    {
      title: 'Trạng thái', dataIndex: 'soTien', key: 'soTien',
      render: (value, entry, i) => i == 0 ? <Tag color='green'>Đang áp dụng</Tag> : <Tag color='red'>Dừng áp dụng</Tag>
    },
    { title: 'Lý do', dataIndex: 'lyDo', key: 'lyDo', }
  ];

  const handleModalOk = () => {
    form.validateFields().then(async () => {
      if (customValue.soTien == null || !customValue.lyDo?.length) return message.error("Nhập thiếu thông tin!")
      if (customValue.soTien <= 0) return message.error("Số tiền phải lớn hơn 0!")

      await UpdateDinhMucTien(customValue);

      message.success('Cập nhật định mức tiền thành công!');
      GetDinhMucTien().then(response => setData(response))
      form.resetFields();
      setModalVisible(false);
    });
  };

  async function OnSubmit(values) {
    // console.log('Submitted values:', values);
    // Call API to update dinh muc tien
    await UpdateDinhMucTien(values);
    setModalVisible(false);
    form.resetFields();
  }

  return (
    <>
      <div className='p-5'>
        <Card title="Định mức tiền theo tiết chuẩn hiện tại">
          <Table columns={dinhMucColumns} dataSource={[data[0]]} pagination={false} size="middle" />
        </Card>
        <Card title="Lịch sử cập nhật định mức " style={{ marginTop: '16px' }}>
          <Table size="middle" columns={lichSuColumns} dataSource={data} pagination={{ pageSize: 5 }} />
        </Card>
      </div>

      <Modal
        open={modalVisible}
        centered
        width={500}
        title={
          <h1 className="text-xl font-bold text-blue-900 uppercase">
            Cập nhật định mức tiền
          </h1>}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={[
          <Button htmlType="submit" className="w-min self-end" variant="solid" color="orange"
            icon={<FontAwesomeIcon icon={faCheck} />}
            onClick={handleModalOk}>
            Hoàn thành
          </Button>
        ]}>
        <Form form={form} layout="vertical" onFinish={OnSubmit}>
          <Form.Item className='font-semibold' label="Số tiền cho 1 tiết chuẩn (VNĐ)" name="soTien" >
            <InputNumber style={{ width: '100%' }} formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')} parser={value => value.replace(/\$\s?|(,*)/g, '')} />
          </Form.Item>
          <Form.Item className='font-semibold' label="Lý do cập nhật" name="lyDo" >
            <Input.TextArea rows={4} />
          </Form.Item>
        </Form>
      </Modal >
    </>
  )
}

export default DinhMucTien