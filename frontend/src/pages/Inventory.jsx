import { useEffect, useState } from 'react';
import API from '../services/api';
import toast from 'react-hot-toast';

function Inventory() {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await API.get('products/');
        const data = Array.isArray(res.data) ? res.data : [];

        setProducts(data);
        setFiltered(data);

        const allCategories = [...new Set(data.map(p => p.category).filter(Boolean))];
        setCategories(allCategories);
      } catch (err) {
        toast.error('Error loading inventory');
        console.error(err);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    let result = [...products];

    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        p =>
          p.name.toLowerCase().includes(q) ||
          p.sku.toLowerCase().includes(q) ||
          (p.tags && p.tags.toLowerCase().includes(q))
      );
    }

    if (categoryFilter) {
      result = result.filter(p => p.category === categoryFilter);
    }

    setFiltered(result);
  }, [search, categoryFilter, products]);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Inventory</h2>

      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name, SKU, tag..."
          className="w-full md:w-1/2 border p-2 rounded"
        />

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="w-full md:w-1/3 border p-2 rounded"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border border-gray-300 text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Name</th>
              <th className="p-2 border">SKU</th>
              <th className="p-2 border">Category</th>
              <th className="p-2 border">Tags</th>
              <th className="p-2 border">Quantity</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center p-4 text-gray-500">
                  No matching products found.
                </td>
              </tr>
            ) : (
              filtered.map(product => (
                <tr key={product.id}>
                  <td className="p-2 border">{product.name}</td>
                  <td className="p-2 border">{product.sku}</td>
                  <td className="p-2 border">{product.category}</td>
                  <td className="p-2 border">{product.tags}</td>
                  <td className="p-2 border">
                    {product.quantity}
                    {product.quantity <= (product.low_stock_threshold || 5) && (
                      <span className="ml-2 text-xs text-red-600 font-bold">
                        🔴 Low
                      </span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Inventory;
