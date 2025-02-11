import { Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import LoginForm from './components/auth/LoginForm';
import ResetPassword from './components/auth/ResetPassword';
import "./App.css"
import HomePage from "./components/homepage/HomePage";

function App() {
  const location = useLocation();
  // Define which paths should not show the header
  const hideHeaderRoutes = ['/lorem-ipsum'];
  const showHeader = !hideHeaderRoutes.includes(location.pathname);

  return (
    <div className="App">
      {showHeader && (
        <header className="bg-red-900 p-4">
          <nav>
            <ul className="flex gap-4">
              <li className="mr-auto">
                <Link to="/" className={"text-white hover:text-gray-300"}>
                  Home
                </Link>
              </li>
              <li className="ml-auto">
                <Link to="/login" className="text-white hover:text-gray-300">
                  Login/Sign Up
                </Link>
              </li>
            </ul>
          </nav>
        </header>
      )}

      <main>
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/" element={
            <div className="flex">
              <div className="w-4/5">
                <HomePage />
              </div>
              <div className="w-1/5">
                <div className="bg-gray-100 p-8 rounded-lg shadow-md sticky top-4 flex flex-col min-h-[600px] m-4">
                  <h2 className="text-lg font-semibold text-gray-700 mb-4">Coming Soon</h2>
                  <p className="text-gray-600 flex-1 flex items-center justify-center text-center">
                    This section is under development
                  </p>
                  <div className="text-sm text-gray-500 mt-4">Stay tuned for updates</div>
                </div>
              </div>
            </div>
          } />
          <Route path="*" element={<div>404 Page Not Found</div>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;