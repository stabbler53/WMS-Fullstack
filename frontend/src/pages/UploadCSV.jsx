import { useState } from 'react';
import toast from 'react-hot-toast';
import API from '../services/api';
import { ArrowUpOnSquareStackIcon } from '@heroicons/react/24/outline';

const endpointMap = {
  products: 'upload-csv/',  // Use the correct endpoint
  inbound: 'upload-csv/',
  outbound: 'upload-csv/',
};

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [type, setType] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !type) {
      toast.error("Please select both type and file");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);  // Add type parameter
    const endpoint = endpointMap[type];
    if (!endpoint) {
      toast.error("Unknown upload type.");
      setLoading(false);
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
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div className="flex items-center gap-3 mb-2">
        <ArrowUpOnSquareStackIcon className="h-7 w-7 text-blue-500" />
        <h2 className="text-2xl font-bold tracking-tight">Upload CSV</h2>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleUpload} className="space-y-4">
          <select
            className="p-2 border border-gray-300 rounded w-full focus:ring-2 focus:ring-blue-200"
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
            className="w-full border border-gray-200 rounded"
            onChange={e => setFile(e.target.files[0])}
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded font-semibold hover:bg-blue-700 transition disabled:opacity-60"
          >
            {loading ? 'Uploading...' : 'Upload'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadCSV;
