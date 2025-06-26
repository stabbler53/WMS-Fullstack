// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Toaster } from 'react-hot-toast';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
    <Toaster
      position="top-right"
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
