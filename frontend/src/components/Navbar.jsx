import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles.css';

function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="navbar-logo">⚡</span>
          ChurnWise
        </Link>

        <ul className="navbar-nav">
          <li>
            <Link
              to="/"
              className={`navbar-link ${isActive('/') ? 'active' : ''}`}
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              to="/predict"
              className={`navbar-link ${isActive('/predict') ? 'active' : ''}`}
            >
              Predict
            </Link>
          </li>
          <li>
            <Link
              to="/dashboard"
              className={`navbar-link ${isActive('/dashboard') ? 'active' : ''}`}
            >
              Dashboard
            </Link>
          </li>
          <li>
            <Link
              to="/history"
              className={`navbar-link ${isActive('/history') ? 'active' : ''}`}
            >
              History
            </Link>
          </li>
          <li>
            <Link
              to="/about"
              className={`navbar-link ${isActive('/about') ? 'active' : ''}`}
            >
              About
            </Link>
          </li>
          <li>
            <button className="navbar-login">Login</button>
          </li>
        </ul>

        <button
          className={`hamburger ${mobileMenuOpen ? 'active' : ''}`}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      {mobileMenuOpen && (
        <ul className="mobile-menu active">
          <li>
            <Link to="/" onClick={() => setMobileMenuOpen(false)}>
              Home
            </Link>
          </li>
          <li>
            <Link to="/predict" onClick={() => setMobileMenuOpen(false)}>
              Predict
            </Link>
          </li>
          <li>
            <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/history" onClick={() => setMobileMenuOpen(false)}>
              History
            </Link>
          </li>
          <li>
            <Link to="/about" onClick={() => setMobileMenuOpen(false)}>
              About
            </Link>
          </li>
        </ul>
      )}
    </nav>
  );
}

export default Navbar;
