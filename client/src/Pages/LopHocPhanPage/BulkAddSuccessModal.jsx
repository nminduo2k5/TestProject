import { faX } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Modal } from 'antd';

export default function ClassSelectionModal() {
  const classes = [
    { code: 'CNTT_1_01', name: 'Lập trình C N01', students: 45 },
    { code: 'CNTT_1_02', name: 'Lập trình C N02', students: 45 },
    { code: 'CNTT_1_03', name: 'Lập trình C N03', students: 45 },
    { code: 'CNTT_1_04', name: 'Lập trình C N04', students: 45 },
    { code: 'CNTT_1_05', name: 'Lập trình C N05', students: 45 },
    { code: 'CNTT_1_06', name: 'Lập trình C N06', students: 45 },
    { code: 'CNTT_1_07', name: 'Lập trình C N07', students: 45 },
  ];

  return (
    <Modal open={false} width={600} centered footer={[]}
      title={<p className='text-xl font-bold uppercase text-center' style={{ color: '#0A34A0' }}>THÊM LỚP HỌC PHẦN THÀNH CÔNG!</p>}
      closeIcon={<FontAwesomeIcon icon={faX} className='scale-120 text-orange-400' />}>

      {/* Content */}
      <h3 className="text-lg font-semibold mb-4" style={{ color: '#0A34A0' }}>
        Danh sách lớp học phần vừa tạo ({classes.length}):
      </h3>

      {/* Class List */}
      <div className="space-y-3 h-100 overflow-y-auto">
        {classes.map((classItem, index) => (
          <div key={index} className="flex items-center bg-gray-50 rounded-lg p-1 hover:bg-gray-100 transition-colors" >
            <div className="border border-blue-300 rounded px-4 py-2 min-w-[120px] text-center" style={{ backgroundColor: '#E9FAFF' }}>
              <span className="text-blue-700 font-medium" >
                {classItem.code}
              </span>
            </div>
            <div className="ml-4 flex-1">
              <span className="text-gray-800">
                {classItem.name} ({classItem.students} sinh viên)
              </span>
            </div>
          </div>
        ))}
      </div>
    </Modal>
  );
}