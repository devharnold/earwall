import React, { useState } from 'react'
import axios from 'axios'

const SendFunds = () => {
  const [receiverEmail, setReceiverEmail] = useState('')
  const [amount, setAmount] = useState('')

  const handleSendFunds = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post(
        'http://localhost:5000/api/send-funds',
        { receiver_email: receiverEmail, amount },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      )
      alert(response.data.message)
    } catch (error) {
      console.error('Error sending funds:', error)
    }
  }

  return (
    <div>
      <input
        type="email"
        placeholder="Receiver's Email"
        value={receiverEmail}
        onChange={(e) => setReceiverEmail(e.target.value)}
      />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button onClick={handleSendFunds}>Send Funds</button>
    </div>
  )
}

export default SendFunds
