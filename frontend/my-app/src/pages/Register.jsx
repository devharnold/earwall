import React, { useState } from 'react'
import axios from 'axios'

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    user_email: '',
    phone_number: '',
    password: ''
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    try {
      // Send the data to the backend using axios
      const response = await axios.post('http://localhost:5000/api/register', formData)
      console.log('Registration Successful:', response.data)
      // Optionally handle the response (like redirecting or showing a message)
    } catch (error) {
      console.error('Registration Failed:', error)
      // Optionally handle errors (showing an error message to the user)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-2xl font-semibold text-center mb-6">Create Account</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          className="w-full mb-4 p-2 border rounded"
          value={formData.first_name}
          onChange={handleChange}
        />
        <input
          type="email"
          name="user_email"
          placeholder="Email"
          className="w-full mb-4 p-2 border rounded"
          value={formData.user_email}
          onChange={handleChange}
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          className="w-full mb-4 p-2 border rounded"
          value={formData.last_name}
          onChange={handleChange}
        />
        <input
          type="number"
          name="phone_number"
          placeholder="Phone Number"
          className="w-full mb-4 p-2 border rounded"
          value={formData.phone_number}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="w-full mb-4 p-2 border rounded"
          value={formData.password}
          onChange={handleChange}
        />
        <button type="submit" className="bg-green-600 text-white w-full py-2 rounded hover:bg-green-700">
          Sign Up
        </button>
      </form>
    </div>
  )
}

export default Register
