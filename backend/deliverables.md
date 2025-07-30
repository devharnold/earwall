# 📦 Wallet Application - Remaining Deliverables

This document outlines the pending deliverables for the Wallet Application. Each task below is essential for ensuring a functional, testable, and deployable system built on microservices architecture.

---

## ✅ 1. Integrate Payment Gateways

- **Flask Daraja API**
  - Implement Safaricom Daraja API in Flask.
  - Enable sandbox mode for testing mobile money transactions.
  - Handle authentication (consumer key/secret).
  - Support STK Push simulation.

- **Stripe API**
  - Implement Stripe payments using their official Python SDK.
  - Enable sandbox/test mode.
  - Setup webhook endpoint to confirm events like successful payments.

---

## 🔗 2. Microservices Communication

- Ensure all services are able to communicate through their respective clients.
- Validate inter-service API calls (e.g., UserService calling WalletService).
- Refactor or add missing service clients if necessary.
- Document service endpoints and dependencies.

---

## 🐳 3. Dockerization

- Create individual `Dockerfile` for each microservice.
- Ensure environment variables and ports are correctly configured.
- Build and run each service container independently.
- Add `.dockerignore` files to reduce image size where applicable.

---

## 📦 4. Dependency Management

- Update `requirements.txt` for each microservice:
  - Ensure all used libraries are listed.
  - Remove unused or redundant packages.
- Use `pip freeze > requirements.txt` to keep the file accurate.

---

## 🚀 5. Deployment & Testing

- Attempt deployment (e.g., using Docker Compose, ECS, or similar).
- If deployment fails:
  - Write unit and integration tests for the affected service(s).
  - Validate API responses and edge cases.
  - Retest until the deployment is successful.

---