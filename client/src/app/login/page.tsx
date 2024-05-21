'use client'
import { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import '..//styles.css';
import { useRouter } from 'next/navigation';

export default function Login() {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const router = useRouter();

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const form = new FormData();
      form.append('username', email);
      form.append('password', password);

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/token`, form, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true
      });

      if (response?.data?.auth_success === true) {
        router.push('/internal');
      }
    } catch (error) {
      setMessage('Login failed.');
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>
      <form className="form" onSubmit={handleLogin}>
        <input
          className="input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          required
        />
        <input
          className="input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          required
        />
        <button className="button" type="submit">Login</button>
      </form>
      <p className="message">{message}</p>
    </div>
  );
}
