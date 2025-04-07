import React, { useState, useEffect } from 'react'
import axios from 'axios'

const Balance = () => {
  const [balance, setBalance] = useState(0)

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/check-balance', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        setBalance(response.data.balance)
      } catch (error) {
        console.error('Error fetching balance:', error)
      }
    }
    fetchBalance()
  }, [])

  return <div>Balance: ${balance}</div>
}

export default Balance
