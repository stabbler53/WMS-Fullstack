import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';
import {
  BarChart, LineChart, AreaChart,
  Bar, Line, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { ChartBarIcon, ClockIcon, ExclamationTriangleIcon, UsersIcon, CubeIcon, TruckIcon } from '@heroicons/react/24/outline';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [activity, setActivity] = useState([]);
  const [chartType, setChartType] = useState('bar');
  const [period, setPeriod] = useState('monthly');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const me = await API.get('users/me/');
        const role = me.data?.role;

        if (role !== 'admin') {
          toast.error('Access denied: Admins only');
          navigate('/inventory');
          return;
        }

        const res = await API.get(`dashboard/admin-stats/?period=${period}`);
        const { totals, chart, audit_logs, low_stock } = res.data;

        setStats({
          totals: totals || { products: 0, customers: 0, suppliers: 0 },
          low_stock: low_stock || [],
        });
        setActivity(audit_logs || []);

        const formattedChart = Array.isArray(chart?.labels)
          ? chart.labels.map((label, i) => ({
              label,
              inbound: chart?.inbound?.[i] || 0,
              outbound: chart?.outbound?.[i] || 0,
            }))
          : [];
        setChartData(formattedChart);
      } catch (err) {
        toast.error('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, [period, navigate]);

  const renderChart = () => {
    if (!Array.isArray(chartData) || chartData.length === 0) {
      return <p className="text-sm text-gray-500">No chart data available.</p>;
    }
    switch (chartType) {
      case 'line':
        return (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="inbound" stroke="#34d399" strokeWidth={2} />
            <Line type="monotone" dataKey="outbound" stroke="#f87171" strokeWidth={2} />
          </LineChart>
        );
      case 'area':
        return (
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorInbound" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#34d399" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorOutbound" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f87171" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#f87171" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="inbound" stroke="#34d399" fill="url(#colorInbound)" />
            <Area type="monotone" dataKey="outbound" stroke="#f87171" fill="url(#colorOutbound)" />
          </AreaChart>
        );
      default:
        return (
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="inbound" fill="#34d399" />
            <Bar dataKey="outbound" fill="#f87171" />
          </BarChart>
        );
    }
  };

  if (loading) {
    return <p className="p-6 text-gray-500">Loading dashboard...</p>;
  }
  if (!stats) {
    return <p className="p-6 text-red-500">Error loading stats.</p>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3 mb-2">
        <ChartBarIcon className="h-7 w-7 text-blue-500" />
        <h1 className="text-2xl font-bold tracking-tight">Dashboard Overview</h1>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <CubeIcon className="h-7 w-7 text-blue-400 mb-1" />
          <h2 className="text-gray-500 text-xs">Products</h2>
          <p className="text-2xl font-bold">{stats.totals.products}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <UsersIcon className="h-7 w-7 text-green-400 mb-1" />
          <h2 className="text-gray-500 text-xs">Customers</h2>
          <p className="text-2xl font-bold">{stats.totals.customers}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <TruckIcon className="h-7 w-7 text-yellow-400 mb-1" />
          <h2 className="text-gray-500 text-xs">Suppliers</h2>
          <p className="text-2xl font-bold">{stats.totals.suppliers}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <ExclamationTriangleIcon className="h-7 w-7 text-red-400 mb-1" />
          <h2 className="text-gray-500 text-xs">Low Stock</h2>
          <p className="text-2xl font-bold">{stats.low_stock.length}</p>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4 gap-2 flex-wrap">
          <div className="flex items-center gap-2">
            <ChartBarIcon className="h-6 w-6 text-blue-400" />
            <h2 className="text-lg font-semibold">Activity Chart</h2>
          </div>
          <div className="flex gap-2 items-center">
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="border p-1 rounded text-sm"
            >
              <option value="daily">Daily</option>
              <option value="monthly">Monthly</option>
            </select>
            <select
              value={chartType}
              onChange={(e) => setChartType(e.target.value)}
              className="border p-1 rounded text-sm"
            >
              <option value="bar">Bar Chart</option>
              <option value="line">Line Chart</option>
              <option value="area">Area Chart</option>
            </select>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          {renderChart()}
        </ResponsiveContainer>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-2 mb-4">
          <ClockIcon className="h-5 w-5 text-gray-400" />
          <h2 className="text-lg font-semibold">Recent Transactions</h2>
        </div>
        {activity.length === 0 ? (
          <p className="text-sm text-gray-500">No recent activity found.</p>
        ) : (
          <ul className="space-y-2 max-h-64 overflow-y-auto">
            {activity.map((log, idx) => (
              <li key={idx} className="text-sm text-gray-600 border-b pb-2">
                {log.timestamp} - <strong>{log.user}</strong> - {log.action} - {log.object_repr}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Low Stock List */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-2 mb-4">
          <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
          <h2 className="text-lg font-semibold">Low Stock Products</h2>
        </div>
        {stats.low_stock.length === 0 ? (
          <p className="text-sm text-gray-500">All products sufficiently stocked.</p>
        ) : (
          <ul className="text-sm text-gray-700 space-y-2">
            {stats.low_stock.map((p, i) => (
              <li key={i} className="flex justify-between border-b pb-1">
                <span>{p.name} (SKU: {p.sku})</span>
                <span className="text-red-500 font-bold">
                  {p.quantity} / {p.low_stock_threshold}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
