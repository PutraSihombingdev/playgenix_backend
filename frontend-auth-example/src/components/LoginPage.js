import React, { useState } from 'react';
import { Form, Input, Button, Typography, Card, message } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AuthLayout from '../../layouts/AuthLayout';

const { Title } = Typography;

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    
    try {
      const result = await login(values.username, values.password);
      
      if (result.success) {
        message.success('Login berhasil!');
        navigate('/'); // Arahkan ke halaman dashboard
      } else {
        message.error(result.error || 'Login gagal');
      }
    } catch (error) {
      console.error('Login error:', error);
      message.error('Terjadi kesalahan saat login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div style={{ minHeight: '100vh', background: '#232323', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
        <Card
          style={{
            background: '#2c2c2c',
            borderRadius: 14,
            border: 'none',
            color: '#fff',
            width: 370,
            boxShadow: '0 2px 8px #0004',
          }}
          bodyStyle={{ padding: 36 }}
        >
          <div style={{ textAlign: 'center', marginBottom: 28 }}>
            <Title level={3} style={{ color: '#4e8cff', marginBottom: 4, fontWeight: 700, letterSpacing: 1 }}>PlayGenix</Title>
            <div style={{ color: '#fff', fontSize: 15, marginBottom: 2 }}>Login Akun</div>
            <div style={{ color: '#fff', fontSize: 13 }}>Masuk untuk melanjutkan</div>
          </div>

          <Form
            name="login-form"
            layout="vertical"
            onFinish={onFinish}
            requiredMark={false}
            autoComplete="off"
          >
            <Form.Item
              name="username"
              label={<span style={{ color: '#fff', fontWeight: 500 }}>Username</span>}
              rules={[{ required: true, message: 'Masukkan username!' }]}
            >
              <Input
                prefix={<UserOutlined style={{ color: '#4e8cff' }} />}
                placeholder="Username"
                style={{
                  background: '#232323',
                  color: '#fff',
                  border: '1px solid #444',
                  borderRadius: 8,
                  height: 44,
                }}
              />
            </Form.Item>

            <Form.Item
              name="password"
              label={<span style={{ color: '#fff', fontWeight: 500 }}>Password</span>}
              rules={[{ required: true, message: 'Masukkan password!' }]}
            >
              <Input.Password
                prefix={<LockOutlined style={{ color: '#4e8cff' }} />}
                placeholder="Password"
                style={{
                  background: '#232323',
                  color: '#fff',
                  border: '1px solid #444',
                  borderRadius: 8,
                  height: 44,
                }}
              />
            </Form.Item>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
              <div />
              <a href="#" style={{ color: '#4e8cff', fontSize: 13, textDecoration: 'none' }}>Lupa password?</a>
            </div>

            <Form.Item style={{ marginBottom: 0 }}>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                style={{
                  width: '100%',
                  height: 44,
                  background: '#4e8cff',
                  border: 'none',
                  borderRadius: 8,
                  color: '#fff',
                  fontWeight: 600,
                  fontSize: 16,
                  letterSpacing: 1,
                }}
              >
                {loading ? 'Loading...' : 'Masuk'}
              </Button>
            </Form.Item>
          </Form>

          <div style={{ textAlign: 'center', marginTop: 28 }}>
            <span style={{ color: '#fff', fontSize: 14 }}>Belum punya akun?{' '}</span>
            <a href="/register" style={{ color: '#4e8cff', fontWeight: 500, fontSize: 14, textDecoration: 'none' }}>Daftar sekarang</a>
          </div>
        </Card>
        {/* Custom style for white placeholder and eye icon */}
        <style>{`
          input::placeholder, .ant-input::placeholder, .ant-input-password input::placeholder {
            color: #fff !important;
            opacity: 1 !important;
          }
          .ant-input-password-icon {
            color: #fff !important;
          }
          .ant-input-password-icon:hover, .ant-input-password-icon:focus {
            color: #fff !important;
          }
        `}</style>
      </div>
    </AuthLayout>
  );
} 