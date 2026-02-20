import React from 'react';

const Spinner = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-100">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600"></div>
        <p className="mt-4 text-gray-600 font-medium">Loading...</p>
      </div>
    </div>
  );
};

export default Spinner;
