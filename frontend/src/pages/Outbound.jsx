import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';

function Outbound() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await API.get('products/');
        setProducts(res.data);
      } catch (err) {
        toast.error('Failed to load products.');
      }
    };
    fetchProducts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await API.post('outbound/', {
        product: productId,
        quantity: parseInt(quantity),
      });

      toast.success('✅ Outbound logged successfully!');
      setQuantity('');
      setProductId('');
      setTimeout(() => navigate('/inventory'), 1000); // short delay before navigating
    } catch (err) {
      if (err.response && err.response.data) {
        if (err.response.data.detail) {
          toast.error(err.response.data.detail);
        } else {
          const errorMessages = Object.values(err.response.data).flat().join(', ');
          toast.error(errorMessages || 'Error submitting outbound.');
        }
      } else {
        toast.error('Network error. Please try again.');
      }
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Outbound Stock</h2>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
        <select
          className="w-full p-2 border rounded"
          value={productId}
          onChange={e => setProductId(e.target.value)}
          required
        >
          <option value="">Select Product</option>
          {products.map(p => (
            <option key={p.id} value={p.id}>
              {p.name} ({p.sku})
            </option>
          ))}
        </select>

        <input
          type="number"
          placeholder="Quantity"
          className="w-full p-2 border rounded"
          value={quantity}
          onChange={e => setQuantity(e.target.value)}
          min="1"
          required
        />

        <button
          type="submit"
          className="w-full bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default Outbound;
