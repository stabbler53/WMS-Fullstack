import { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

toast.success("Login successful!");
toast.error("Invalid credentials");

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const loginUser = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/token/', {
        username,
        password
      });
      localStorage.setItem('access_token', res.data.access);
      toast.success('Login successful!');
      window.location.href = "/inventory";
    } catch (err) {
      toast.error('Invalid credentials');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={loginUser} className="bg-white p-6 rounded shadow-md w-96">
        <h2 className="text-xl mb-4 font-semibold">Login</h2>
        <input
          type="text"
          placeholder="Username"
          className="w-full p-2 mb-3 border rounded"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-3 border rounded"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
