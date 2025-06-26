import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';

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
      const msg =
        err.response?.data
          ? Object.values(err.response.data).flat().join(', ')
          : 'Error submitting outbound.';
      toast.error(msg);
    }
  };

  if (loading) {
    return <p className="p-6 text-gray-500">Loading...</p>;
  }

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Outbound Dispatch</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          name="product"
          value={form.product}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
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
          className="w-full p-2 border rounded"
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
          className="w-full p-2 border rounded"
        />

        <input
          type="number"
          name="quantity"
          value={form.quantity}
          onChange={handleChange}
          placeholder="Quantity"
          min="1"
          required
          className="w-full p-2 border rounded"
        />

        <input
          type="file"
          accept=".csv,.pdf,.jpg,.png"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full"
        />

        <button
          type="submit"
          className="w-full bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Submit Outbound
        </button>
      </form>
    </div>
  );
}

export default Outbound;
