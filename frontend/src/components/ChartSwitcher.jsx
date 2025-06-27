import {
  BarChart, LineChart, AreaChart,
  Bar, Line, Area,
  XAxis, YAxis, CartesianGrid, Tooltip
} from 'recharts';

function ChartSwitcher({ type, data }) {
  if (!Array.isArray(data) || data.length === 0) {
    return <p className="text-sm text-gray-500">No chart data available.</p>;
  }

  switch (type) {
    case 'line':
      return (
        <LineChart data={data}>
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
        <AreaChart data={data}>
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
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="inbound" fill="#34d399" />
          <Bar dataKey="outbound" fill="#f87171" />
        </BarChart>
      );
  }
}

export default ChartSwitcher;
