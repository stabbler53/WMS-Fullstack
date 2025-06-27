import { useEffect, useState, useRef } from 'react';
import API from '../services/api';
import toast from 'react-hot-toast';
import { CubeIcon } from '@heroicons/react/24/outline';
import JsBarcode from 'jsbarcode';

function Inventory() {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [categories, setCategories] = useState([]);
  const [barcodes, setBarcodes] = useState({});
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    // Get user information from localStorage
    const storedUserInfo = localStorage.getItem('user_info');
    if (storedUserInfo) {
      const user = JSON.parse(storedUserInfo);
      setUserInfo(user);
      console.log('Current user:', user);
    }

    const fetchProducts = async () => {
      try {
        const res = await API.get('products/');
        const data = Array.isArray(res.data) ? res.data : [];
        
        // Debug: Log what we received
        console.log('API Response:', data);
        console.log('Products received:', data.length);
        data.forEach(p => console.log(`- ${p.name} (Archived: ${p.is_archived})`));

        // Filter out archived products as a safety measure
        const activeProducts = data.filter(product => !product.is_archived);
        console.log('Active products after filtering:', activeProducts.length);

        setProducts(activeProducts);
        setFiltered(activeProducts);

        const allCategories = [...new Set(activeProducts.map(p => p.category).filter(Boolean))];
        setCategories(allCategories);
      } catch (err) {
        toast.error('Error loading inventory');
        console.error(err);
      }
    };

    fetchProducts();
  }, []);

  // Generate barcode for a product
  const generateBarcode = (sku) => {
    if (barcodes[sku]) return barcodes[sku];
    
    try {
      const canvas = document.createElement('canvas');
      JsBarcode(canvas, sku, {
        format: "CODE128",
        width: 1.5,
        height: 40,
        displayValue: false,
        background: "#ffffff",
        lineColor: "#000000",
      });
      
      const barcodeData = canvas.toDataURL();
      setBarcodes(prev => ({ ...prev, [sku]: barcodeData }));
      return barcodeData;
    } catch (error) {
      console.error('Error generating barcode:', error);
      return null;
    }
  };

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
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-2">
        <CubeIcon className="h-7 w-7 text-blue-500" />
        <h2 className="text-2xl font-bold tracking-tight">Inventory</h2>
        {userInfo && (
          <div className="ml-auto text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
            👤 {userInfo.username} ({userInfo.role})
          </div>
        )}
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name, SKU, tag..."
          className="w-full md:w-1/2 border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-200"
        />

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="w-full md:w-1/3 border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-200"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto rounded-lg shadow bg-white">
        <table className="w-full text-sm">
          <thead className="bg-blue-50">
            <tr>
              <th className="p-3 text-left font-semibold text-gray-700">Name</th>
              <th className="p-3 text-left font-semibold text-gray-700">SKU & Barcode</th>
              <th className="p-3 text-left font-semibold text-gray-700">Category</th>
              <th className="p-3 text-left font-semibold text-gray-700">Tags</th>
              <th className="p-3 text-left font-semibold text-gray-700">Quantity</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center p-8 text-gray-400">
                  <span className="block text-2xl mb-2">📦</span>
                  <span>No matching products found.</span>
                </td>
              </tr>
            ) : (
              filtered.map(product => (
                <tr key={product.id} className={`hover:bg-blue-50 transition ${product.is_archived ? 'bg-red-50 opacity-60' : ''}`}>
                  <td className="p-3 border-b border-gray-100 font-medium">
                    {product.name}
                    {product.is_archived && (
                      <span className="ml-2 text-xs text-red-600 font-bold">
                        🔴 ARCHIVED
                      </span>
                    )}
                  </td>
                  <td className="p-3 border-b border-gray-100">
                    <div className="flex flex-col items-start gap-2">
                      <span className="font-mono text-sm">{product.sku}</span>
                      <img 
                        src={generateBarcode(product.sku)} 
                        alt={`Barcode for ${product.sku}`}
                        className="h-8 w-auto"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                    </div>
                  </td>
                  <td className="p-3 border-b border-gray-100">{product.category}</td>
                  <td className="p-3 border-b border-gray-100">{product.tags}</td>
                  <td className="p-3 border-b border-gray-100">
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
