import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline';

function Outbound() {
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState({
    product: '',
    customer: '',
    quantity: '',
    so_reference: ''
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prodRes, custRes] = await Promise.all([
          API.get('products/'),
          API.get('customers/')
        ]);

        const prodData = Array.isArray(prodRes.data) ? prodRes.data : [];
        const custData = Array.isArray(custRes.data) ? custRes.data : [];

        if (!Array.isArray(prodRes.data)) {
          console.warn("Expected product array, got:", prodRes.data);
          toast.error('Unexpected product response from server.');
        }

        setProducts(prodData);
        setCustomers(custData);
      } catch (err) {
        const msg =
          err.response?.status === 404
            ? 'Product or customer data not found.'
            : 'Failed to load product/customer data.';
        toast.error(msg);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    if (form.product) data.append("product", parseInt(form.product));
    if (form.customer) data.append("customer", parseInt(form.customer));
    data.append("quantity", parseInt(form.quantity));
    if (form.so_reference) data.append("so_reference", form.so_reference);
    if (file) data.append("delivery_note_file", file);

    try {
      await API.post('outbound/', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      toast.success('✅ Outbound logged successfully!');
      setForm({ product: '', customer: '', quantity: '', so_reference: '' });
      setFile(null);

      setTimeout(() => navigate('/inventory'), 1000);
    } catch (err) {
      let errorMsg = 'Error submitting outbound.';
      
      if (err.response?.data) {
        if (typeof err.response.data === 'string') {
          errorMsg = err.response.data;
        } else if (typeof err.response.data === 'object') {
          const errorValues = Object.values(err.response.data).flat();
          errorMsg = errorValues.join(', ');
        }
      }
      
      // Limit error message length to prevent long toasts
      if (errorMsg.length > 100) {
        errorMsg = errorMsg.substring(0, 100) + '...';
      }
      
      toast.error(errorMsg);
      console.error('Outbound submission error:', err);
    }
  };

  if (loading) {
    return <p className="p-6 text-gray-500">Loading...</p>;
  }

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div className="flex items-center gap-3 mb-2">
        <ArrowUpTrayIcon className="h-7 w-7 text-red-500" />
        <h2 className="text-2xl font-bold tracking-tight">Outbound Dispatch</h2>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <select
            name="product"
            value={form.product}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-red-200"
          >
            <option value="">Select Product</option>
            {products.map(p => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.sku})
              </option>
            ))}
          </select>

          <select
            name="customer"
            value={form.customer}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-red-200"
          >
            <option value="">Select Customer (optional)</option>
            {customers.map(c => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>

          <input
            type="text"
            name="so_reference"
            value={form.so_reference}
            onChange={handleChange}
            placeholder="Sales Order Reference (optional)"
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-red-200"
          />

          <input
            type="number"
            name="quantity"
            value={form.quantity}
            onChange={handleChange}
            placeholder="Quantity"
            min="1"
            required
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-red-200"
          />

          <input
            type="file"
            accept=".csv,.pdf,.jpg,.png"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full border border-gray-200 rounded"
          />

          <button
            type="submit"
            className="w-full bg-red-600 text-white px-4 py-2 rounded font-semibold hover:bg-red-700 transition"
          >
            Submit Outbound
          </button>
        </form>
      </div>
    </div>
  );
}

export default Outbound;
