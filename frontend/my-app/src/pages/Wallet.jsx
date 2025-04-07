import React, { useState, useEffect } from 'react'
import axios from 'axios'

const Wallet = () => {
  // State to store the balance and transaction data
  const [balance, setBalance] = useState(0)
  const [transactionAmount, setTransactionAmount] = useState('')
  const [recipient, setRecipient] = useState('')
  const [transactions, setTransactions] = useState([])

  // Fetch the user's wallet balance on component mount
  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await axios.get('/api/wallet/balance')  // Endpoint to fetch balance
        setBalance(response.data.balance)
      } catch (error) {
        console.error('Error fetching balance:', error)
      }
    }

    const fetchTransactions = async () => {
      try {
        const response = await axios.get('/api/wallet/transactions')  // Endpoint to fetch transaction history
        setTransactions(response.data.transactions)
      } catch (error) {
        console.error('Error fetching transactions:', error)
      }
    }

    fetchBalance()
    fetchTransactions()
  }, [])

  // Handle sending funds
  const handleSendFunds = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post('/api/wallet/send', {
        amount: transactionAmount,
        recipient: recipient,
      })
      alert('Transaction successful!')
      setTransactionAmount('')
      setRecipient('')
      // Re-fetch the balance and transactions after the transaction
      setBalance(response.data.new_balance)
      setTransactions(response.data.new_transactions)
    } catch (error) {
      console.error('Error sending funds:', error)
      alert('Transaction failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-2xl font-semibold text-center mb-6">Your Wallet</h2>
      <div className="mb-4">
        <p className="text-lg">Balance: ${balance}</p>
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-4">Send Funds</h3>
        <form onSubmit={handleSendFunds}>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Recipient's User ID"
              className="w-full mb-4 p-2 border rounded"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <input
              type="number"
              placeholder="Amount"
              className="w-full mb-4 p-2 border rounded"
              value={transactionAmount}
              onChange={(e) => setTransactionAmount(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white w-full py-2 rounded hover:bg-blue-700"
          >
            Send Funds
          </button>
        </form>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-semibold mb-4">Transaction History</h3>
        {transactions.length > 0 ? (
          <ul>
            {transactions.map((transaction, index) => (
              <li key={index} className="mb-2">
                <div className="border p-4 rounded shadow-md">
                  <p>
                    <strong>{transaction.type}</strong>: ${transaction.amount}
                  </p>
                  <p>
                    To: {transaction.recipient} | Date: {transaction.date}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No transactions yet.</p>
        )}
      </div>
    </div>
  )
}

export default Wallet
