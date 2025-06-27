function Spinner({ message = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-10 text-gray-600">
      <svg
        className="animate-spin h-8 w-8 text-green-500 mb-3"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8z"
        />
      </svg>
      <p className="text-sm">{message}</p>
    </div>
  );
}

export default Spinner;
