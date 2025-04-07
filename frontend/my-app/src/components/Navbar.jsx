import React from 'react'
import { Link } from 'react-router-dom'

const Navbar = () => (
  <nav style={{ padding: '1rem', background: '#f0f0f0' }}>
    <Link to="/">Home</Link> |{' '}
    <Link to="/wallet">Wallet</Link> |{' '}
    <Link to="/send">Send</Link> |{' '}
    <Link to="/profile">Profile</Link>
  </nav>
)

export default Navbar
