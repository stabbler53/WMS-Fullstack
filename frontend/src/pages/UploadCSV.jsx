import { useState } from 'react';
import toast from 'react-hot-toast';
import API from '../services/api';

const endpointMap = {
  products: 'upload/inventory/',  // assumes "products" == inventory
  inbound: 'upload/inbound/',
  outbound: 'upload/outbound/',
};

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

    const endpoint = endpointMap[type];
    if (!endpoint) {
      toast.error("Unknown upload type.");
      return;
    }

    try {
      await API.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success(`${type.toUpperCase()} upload successful!`);
      setFile(null);
      setType('');
    } catch (err) {
      const errMsg =
        err.response?.data?.error ||
        (typeof err.response?.data === 'string'
          ? err.response.data
          : Object.values(err.response?.data || {}).flat().join(', ')) ||
        "Upload failed. Please try again.";
      toast.error(errMsg);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
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
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
        >
          Upload
        </button>
      </form>
    </div>
  );
}

export default UploadCSV;
