import { useState } from 'react';
import toast from 'react-hot-toast';
import API from '../services/api';

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [type, setType] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file || !type) {
      toast.error("Please select both type and file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);

    try {
      await API.post('upload_csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success(`${type.toUpperCase()} upload successful!`);
      setFile(null);
      setType('');
    } catch (err) {
      if (err.response && err.response.data) {
        const errMsg = typeof err.response.data === 'string'
          ? err.response.data
          : Object.values(err.response.data).flat().join(', ');
        toast.error(errMsg);
      } else {
        toast.error("Upload failed. Please try again.");
      }
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Upload CSV</h2>
      <form onSubmit={handleUpload} className="space-y-4">
        <select
          className="p-2 border rounded w-full"
          value={type}
          onChange={e => setType(e.target.value)}
          required
        >
          <option value="">Select Upload Type</option>
          <option value="products">Products</option>
          <option value="inbound">Inbound</option>
          <option value="outbound">Outbound</option>
        </select>

        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
          className="p-2 border rounded w-full"
          accept=".csv"
          required
        />

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Upload
        </button>
      </form>
    </div>
  );
}

export default UploadCSV;
