import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Input, InputNumber, message, Modal } from 'antd';

import { CreateHocPhan, GetHocPhan, UpdateHocPhan } from "@/api/hocphanApi";
import { useData } from "./context";

function isValidString(str) {
  // Chỉ cho phép chữ cái và số, KHÔNG chứa ký tự đặc biệt
  return /^[a-zA-Z0-9 ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáạảãăắẳặằâấầậẫèéẻẽẹêềễệếìíịỉòóõỏôổỗộồốùúụủũđĩơởờớỡừứửựƯĂÊÔƯƠâêôơưĂÂÊÔƯ\s\-_]+$/.test(str);
}


function FormModal() {
  const [{ showModal, modalMode, selectedKhoa, form }, dispatch] = useData()
  const { id, maHocPhan, tenHocPhan, khoaId, soTinChi, soTiet, heSoHocPhan } = form

  async function onFormSubmit(e) {
    console.log({ id, maHocPhan, tenHocPhan, khoaId, soTinChi, soTiet, heSoHocPhan })
    e.preventDefault()
    if (!tenHocPhan || !soTinChi || !soTiet || !heSoHocPhan) return message.error("Nhập thiếu thông tin!")
    if (!isValidString(tenHocPhan)) {
      // console.log(tenHocPhan)
      return message.error("Tên học phần không được chứa kí tự đặc biệt (ngoại trừ dấu - và _ )!")
    }

    if (modalMode == 'add') {
      try {
        // console.log(selectedKhoa)
        await CreateHocPhan({ maHocPhan, tenHocPhan, khoaId: selectedKhoa.id, soTinChi, soTiet, heSoHocPhan })
        message.success("Thêm học phần thành công!")
      } catch (err) {
        console.error(err)
        message.error("Tên học phần đã tồn tại!")
        return
      }
    }
    else if (modalMode == 'edit') {
      try {
        // console.log(selectedKhoa)
        await UpdateHocPhan(id, { tenHocPhan, khoaId, soTinChi, soTiet, heSoHocPhan })
        message.success("Cập nhật học phần thành công!")
      } catch (err) {
        console.error(err)
        message.error("Tên học phần không được chứa kí tự đặc biệt (ngoại trừ dấu - và _)!")
        return
      }
    }

    const data = await GetHocPhan().then(data => data)
    dispatch([
      { type: "updateModal", payload: false },
      { type: "resetFormData" },
      { type: "updateFormMode" },
      { type: "updateHocPhanList", payload: data },
      // { type: "updateSelectedKhoa", payload: 'all' }
    ])
  }

  return (
    <Modal
      okText="Hoàn thành" cancelText="Hủy" width={600} open={showModal}
      onCancel={() => dispatch([
        { type: "updateModal", payload: false },
        { type: "resetFormData" },
        { type: "updateFormMode" }
      ])}
      title={(
        <h1 className="text-xl font-bold text-blue-900 uppercase">
          {modalMode === "edit" ? 'Sửa học phần' : 'Thêm học phần mới'}
        </h1>
      )}
      footer={[
        <Button key="submit" htmlType="submit" className="w-min self-end" variant="solid" color="orange" onClick={onFormSubmit} >
          Hoàn thành
          <FontAwesomeIcon icon={faCheck} />
        </Button>
      ]}>
      <div style={{ paddingTop: '16px' }}>
        <div className='grid grid-cols-[1fr_2fr]' style={{ gap: 16 }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
              Mã học phần <span style={{ color: 'red' }}>*</span>
            </label>
            <Input disabled placeholder="CNTT_1" value={maHocPhan} />
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
              Khoa <span style={{ color: 'red' }}>*</span>
            </label>
            <Input disabled placeholder="Công nghệ thông tin" value={selectedKhoa?.tenKhoa} />
          </div>
        </div>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
            Tên học phần <span style={{ color: 'red' }}>*</span>
          </label>
          <Input placeholder="Nhập tên học phần" value={tenHocPhan}
            onChange={e => dispatch({ type: "updateForm", payload: { name: "tenHocPhan", value: e.target.value } })} />
        </div>

        <div style={{ display: 'flex', gap: 16 }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
              Hệ số <span style={{ color: 'red' }}>*</span>
            </label>
            <InputNumber min={0.1} max={3.0} step={0.1} placeholder="1.5" style={{ width: '100%' }}
              value={heSoHocPhan || undefined}
              onChange={e => dispatch({ type: 'updateForm', payload: { name: "heSoHocPhan", value: e } })} />
          </div>

          <div className='mb-5' style={{ display: 'flex', gap: 16 }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
                Số tín chỉ <span style={{ color: 'red' }}>*</span>
              </label>
              <InputNumber min={1} max={10} placeholder="3" style={{ width: '100%' }}
                value={soTinChi || undefined}
                onChange={e => dispatch({ type: 'updateForm', payload: { name: "soTinChi", value: e } })} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, color: '#333' }}>
                Số tiết <span style={{ color: 'red' }}>*</span>
              </label>
              <InputNumber min={15} max={150} placeholder="45" style={{ width: '100%' }}
                value={soTiet || undefined}
                onChange={e => dispatch({ type: 'updateForm', payload: { name: "soTiet", value: e } })} />
            </div>
          </div>
        </div>
      </div>
    </Modal>
  )
}

export default FormModal