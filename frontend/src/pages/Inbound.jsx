import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';

toast.success("Inbound logged!");
toast.error("Not enough stock!");

function Inbound() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');

  useEffect(() => {
    API.get('products/').then(res => setProducts(res.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await API.post('inbound/', {
      product: productId,
      quantity: parseInt(quantity)
    });
    toast.success("Inbound logged!");
    navigate('/inventory'); // 👈 redirect
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Inbound Stock</h2>
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
        <select className="w-full p-2 border" value={productId} onChange={e => setProductId(e.target.value)} required>
          <option value="">Select Product</option>
          {products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <input
          type="number"
          placeholder="Quantity"
          className="w-full p-2 border"
          value={quantity}
          onChange={e => setQuantity(e.target.value)}
          required
        />
        <button className="bg-green-600 text-white px-4 py-2 rounded" type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Inbound;
