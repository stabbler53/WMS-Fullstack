import { useEffect, useState } from 'react';
import API from '../services/api';

function Inventory() {
  const [products, setProducts] = useState([]);

useEffect(() => {
  const fetchData = () => {
    API.get('products/').then(res => setProducts(res.data));
  };
  fetchData();
  const interval = setInterval(fetchData, 5000);
  return () => clearInterval(interval);
}, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Inventory</h2>
      <table className="w-full border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 border">SKU</th>
            <th className="p-2 border">Name</th>
            <th className="p-2 border">Qty</th>
            <th className="p-2 border">Low Stock?</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <tr key={p.id} className="text-center">
              <td className="p-2 border">{p.sku}</td>
              <td className="p-2 border">{p.name}</td>
              <td className="p-2 border">{p.quantity}</td>
              <td className={`p-2 border ${p.quantity <= p.low_stock_threshold ? 'text-red-500 font-bold' : ''}`}>
                {p.quantity <= p.low_stock_threshold ? 'Yes' : 'No'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Inventory;
