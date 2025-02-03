import { Routes, Route, Link, Navigate } from 'react-router-dom';
import LoginForm from './components/auth/LoginForm';
import ResetPassword from './components/auth/ResetPassword';
import "./App.css"

function App() {
  return (
    <div className="App">
      <header className="bg-slate-800 p-4">
        <nav>
          <ul className="flex gap-4">
            <li>
              <Link to="/login" className="text-white hover:text-gray-300">
                Login
              </Link>
            </li>
            <li>
              <Link to="/reset-password" className="text-white hover:text-gray-300">
                Reset Password
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <Routes>
          {/* Redirect root path to /login */}
          {/*<Route path="/" element={<Navigate to="/login" replace />} />*/}
          <Route path="/login" element={<LoginForm />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          {/* 404 Catch-all */}
          <Route path="*" element={<div>404 Page Not Found</div>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;