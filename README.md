# **EARLWALL**
**Proposed agenda**

This project is focused on building a platform that supports P2P payments, wallet management, and Ethereum integration. The backend uses PostgreSQL for database management, ensuring scalability, security, and performance.

---

## **Common User Credentials for Signup**

Here’s a list of essential credentials needed for a user to sign up:

1. **Full Name**
    - **Purpose**: For personal identification and to personalize the user experience.
   
2. **Email Address**
    - **Purpose**: Used for account verification, password recovery, and communication.
    - **Validation**: Ensure correct format and use email verification (e.g., sending a verification link).
   
3. **Username** *(optional)*
    - **Purpose**: Alternative to using addresses if the platform supports user-to-user transfers via usernames.

4. **Password**
    - **Purpose**: For secure access to the user’s account.
    - **Security**: Enforce strong password policies and securely store using hashing algorithms like `bcrypt`.
   
5. **Phone Number** *(optional but recommended)*
    - **Purpose**: For two-factor authentication (2FA), account recovery, and additional verification.
    - **Validation**: Use SMS verification to confirm the phone number.

6. **Ethereum Wallet Address** *(if applicable)*
    - **Purpose**: Connect users' Ethereum wallets (e.g., MetaMask) for transactions.
    - **Security**: Only request the public wallet address, never private keys.
   
7. **KYC Details** *(optional for compliance)*
    - **Purpose**: For identity verification, if required by financial regulations.
    - **Security**: Securely store and manage compliance with data protection laws.

8. **Country and Date of Birth** *(optional)*
    - **Purpose**: For regulatory purposes like age restrictions or compliance.
    - **Validation**: Ensure compliance with age-related restrictions.

9. **Profile Picture** *(optional)*
    - **Purpose**: Enhance user profile, but not essential for signup.

---

## **Security Measures During Signup**

- **Email Verification**: Send verification emails with confirmation links to ensure authenticity.
- **CAPTCHA**: Prevent bot signups using CAPTCHA.
- **Two-Factor Authentication (2FA)**: Strongly encourage users to enable 2FA (via SMS, email, or an authentication app).
- **Rate Limiting**: Implement limits to prevent brute-force attacks during signup attempts.

---

## **Core Features of the Platform**

### **1. User Management and Security**

- **User Authentication and Authorization**: Use JWT for APIs, OAuth for third-party integrations, and role-based access control (RBAC) to manage permissions.
- **Two-Factor Authentication (2FA)**: Implement 2FA for secure login and transaction protection.
- **Account Management**: Enable users to reset passwords and update profile information.

### **2. P2P Payment Features**

- **Transaction Management**: Create endpoints for initiating, processing, and tracking P2P transactions.
- **Escrow Services**: Implement escrow features for secure P2P transactions.
- **Dispute Resolution**: Include mechanisms for users to resolve disputes.

### **3. Wallet Features**

- **Multi-Currency Support**: Allow users to manage multiple currencies (e.g., USD, KES).
- **Transaction History**: Track wallet transactions, including deposits, withdrawals, and transfers.
- **Balance Management**: Show current balances and manage wallet limits.

### **4. Ethereum Integration(FUTURE PLANS)**

- **Smart Contracts**: Deploy and manage smart contracts for automated transactions and escrow services.
- **Gas Management**: Estimate and manage Ethereum transaction fees.
- **Token Management**: Support ERC-20 or ERC-721 tokens for user transfers.

### **5. API Integration**

- **Payment Gateways**: Integrate with fiat payment gateways like Stripe, PayPal and Mpesa Daraja.
- **Blockchain Nodes**: Use providers like Infura or Alchemy to connect to Ethereum nodes.
- **External APIs**: Integrate APIs for exchange rates, identity verification, or transaction monitoring.

---

## **Development Tools and Database**

### **PostgreSQL Integration**

PostgreSQL has been selected for its robust feature set, performance, and extensibility, particularly suited to handling financial data and transactions.

#### **Advantages of Using PostgreSQL**:

1. **ACID Compliance**: Ensures transaction reliability and consistency.
2. **Rich Data Types**: Supports JSON for storing transaction details.
3. **Extensibility**: Allows custom data types and functions for managing specific project requirements.
4. **Performance**: Features like indexing and Multiversion Concurrency Control (MVCC) help manage transactions efficiently.
5. **Scalability**: Supports horizontal scaling, replication, and clustering.
6. **Security**: Offers role-based access control and encryption for data protection.

### **How PostgreSQL Fits in the Project**:

- **Digital Wallet System**: Manage user information, wallet balances, and transaction histories.
- **P2P Payment Platform**: Handle eft(s), disputes, and escrow services securely.
- **Ethereum Integration**: Store user Ethereum addresses and transaction details.

#### **Installation**:

To install PostgreSQL:

```bash
pip install psycopg2
```

---

## **Testing and Deployment**

- **Testing**: Implement unit, integration, and end-to-end tests. Use Ethereum testnets for smart contract testing.
- **Deployment**: Deploy on cloud platforms with scalability in mind, ensuring secure and efficient operations.

---

## **Monitoring and Analytics**

- **Transaction Monitoring**: Implement tools to track transaction activities.
- **User Analytics**: Collect and analyze data for improving user experience.

---

## **Documentation and Support**

- **User Documentation**: User guides and FAQs.
- **Developer Documentation**: Document API endpoints, smart contract functions, and integration guidelines.

---
