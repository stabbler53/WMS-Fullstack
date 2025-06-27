import { useEffect, useState } from 'react';
import API from '../services/api';
import toast from 'react-hot-toast';
import { ArrowDownTrayIcon } from '@heroicons/react/24/outline';

function Inbound() {
  const [products, setProducts] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [form, setForm] = useState({
    product: '',
    supplier: '',
    quantity: '',
    invoice_number: ''
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prodRes, suppRes] = await Promise.all([
          API.get('products/'),
          API.get('suppliers/')
        ]);

        const prodData = Array.isArray(prodRes.data) ? prodRes.data : [];
        const suppData = Array.isArray(suppRes.data) ? suppRes.data : [];

        if (!Array.isArray(prodRes.data)) {
          toast.error('Unexpected product response from server.');
          console.warn('products:', prodRes.data);
        }

        if (!Array.isArray(suppRes.data)) {
          toast.error('Unexpected supplier response from server.');
          console.warn('suppliers:', suppRes.data);
        }

        setProducts(prodData);
        setSuppliers(suppData);
      } catch (err) {
        const message =
          err.response?.status === 404
            ? 'Data not found on server.'
            : 'Error loading product/supplier data.';
        toast.error(message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('product', parseInt(form.product));
    data.append('quantity', parseInt(form.quantity));

    if (form.supplier) {
      data.append('supplier', parseInt(form.supplier));
    }

    if (form.invoice_number) {
      data.append('invoice_number', form.invoice_number);
    }

    if (file) {
      data.append('invoice_file', file);
    }

    try {
      await API.post('inbound/', data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      toast.success('✅ Inbound logged!');
      setForm({ product: '', supplier: '', quantity: '', invoice_number: '' });
      setFile(null);
    } catch (err) {
      const msg =
        err.response?.data
          ? Object.values(err.response.data).flat().join(', ')
          : 'Error submitting inbound.';
      toast.error(msg);
      console.error('Inbound error:', err.response?.data || err.message);
    }
  };

  if (loading) {
    return <p className="p-6 text-gray-500">Loading...</p>;
  }

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div className="flex items-center gap-3 mb-2">
        <ArrowDownTrayIcon className="h-7 w-7 text-green-500" />
        <h2 className="text-2xl font-bold tracking-tight">Inbound Form</h2>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <select
            name="product"
            onChange={handleChange}
            value={form.product}
            required
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-green-200"
          >
            <option value="">Select Product</option>
            {products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.sku})
              </option>
            ))}
          </select>

          <select
            name="supplier"
            onChange={handleChange}
            value={form.supplier}
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-green-200"
          >
            <option value="">Select Supplier (optional)</option>
            {suppliers.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          <input
            type="text"
            name="invoice_number"
            placeholder="Invoice Number"
            value={form.invoice_number}
            onChange={handleChange}
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-green-200"
          />

          <input
            type="number"
            name="quantity"
            placeholder="Quantity"
            value={form.quantity}
            onChange={handleChange}
            min="1"
            required
            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-green-200"
          />

          <input
            type="file"
            accept=".pdf,.jpg,.png"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full border border-gray-200 rounded"
          />

          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 px-4 rounded font-semibold hover:bg-green-700 transition"
          >
            Submit Inbound
          </button>
        </form>
      </div>
    </div>
  );
}

export default Inbound;
