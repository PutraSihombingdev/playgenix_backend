import React from 'react';

const AuthLayout = ({ children }) => {
  return (
    <div style={{ 
      minHeight: '100vh',
      background: '#232323',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    }}>
      {children}
    </div>
  );
};

export default AuthLayout; 