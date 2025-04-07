import React, { useState } from 'react'
import axios from 'axios'

const LinkPayPal = () => {
  const [paypalEmail, setPaypalEmail] = useState('')

  const handleLinkPayPal = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post(
        'http://localhost:5000/api/link-paypal',
        { paypal_email: paypalEmail },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      )
      alert(response.data.message)
    } catch (error) {
      console.error('Error linking PayPal:', error)
    }
  }

  return (
    <div>
      <input
        type="email"
        placeholder="Enter PayPal Email"
        value={paypalEmail}
        onChange={(e) => setPaypalEmail(e.target.value)}
      />
      <button onClick={handleLinkPayPal}>Link PayPal</button>
    </div>
  )
}

export default LinkPayPal
