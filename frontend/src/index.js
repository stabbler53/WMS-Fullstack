import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Tailwind or global styles
import { Toaster } from 'react-hot-toast';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
    <Toaster
      position="top-center"  // ✅ Changed from "top-right" to "top-center"
      reverseOrder={false}
      toastOptions={{
        success: {
          style: {
            background: '#4ade80', // Tailwind green-400
            color: 'black',
          },
        },
        error: {
          style: {
            background: '#f87171', // Tailwind red-400
            color: 'white',
          },
        },
        style: {
          fontSize: '14px',
          borderRadius: '8px',
          padding: '12px 16px',
        },
      }}
    />
  </React.StrictMode>
);

reportWebVitals();
