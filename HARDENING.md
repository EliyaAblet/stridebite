# StrideBite – Security Hardening Notes (Milestone 2)

This document summarizes the hardening steps implemented for the StrideBite fitness tracker. It covers application-level controls, authentication and authorization measures, input validation, container hardening, deployment considerations, and known limitations.

---

## 1. Architecture and Threat Model

### Technology Stack
- Django 5 (server-side rendering and REST API)
- Django REST Framework for JSON endpoints
- SQLite/Postgres via Django ORM
- Dockerized application deployed on an AWS EC2 instance
- Gunicorn as the production WSGI server

### Protected Assets
- User accounts and password hashes
- Fitness data such as meals, workouts, sleep logs, and body weight
- DRF authentication tokens for API access

### Key Threats Considered
- Unauthorized access to user data
- Account compromise through weak authentication or session misuse
- Script injection (XSS) via input fields
- CSRF attacks against state‑changing operations
- Abuse of API endpoints
- Container compromise or OS-level intrusion

---

## 2. Application and Container Hardening

### 2.1. Environment-Based Configuration

Sensitive and environment-specific settings have been moved out of the codebase and into environment variables.

- **Secret Key**  
  Django’s SECRET_KEY is provided at runtime through an environment variable. This prevents accidental exposure in the repository and makes rotation easier.

- **Debug Mode**  
  DEBUG is disabled in production to avoid leaking stack traces and internal application details.

- **Allowed Hosts**  
  The allowed hosts list is controlled through an environment variable. This prevents Host header attacks and clearly defines which domains or IPs may serve the application.

- **Database Configuration**  
  All database credentials and hostnames are supplied via environment variables. No credentials are committed to the codebase.

This approach improves flexibility and reduces the risk of secret leakage.

---

### 2.2. Container Hardening

#### Minimal Base Image  
The application uses the `python:3.12-slim` image to reduce the operating system footprint and attack surface.

#### Controlled System Dependencies  
Only essential system packages are installed. Package lists are removed afterward to minimize size and metadata exposure.

#### Python Runtime Adjustments  
- Python bytecode files are not written inside the container.  
- Output is unbuffered for clearer logging.  
- Pip caches are disabled to avoid storing unnecessary files.  
- Python’s fault handler is enabled for better crash diagnostics.

#### Non‑Root User Execution  
The container creates a dedicated non‑privileged user named `app`. The application runs entirely under this account rather than root, which reduces the impact of a compromise.

#### Production WSGI Server  
Gunicorn is used instead of Django’s development server. This provides more stable request handling and is appropriate for production deployment.

---

## 2.3. Input Validation and Sanitization

StrideBite relies both on Django’s built‑in validators and a custom regular‑expression validator to ensure all submitted data is clean, safe, and correctly bounded.

### Custom “No HTML” Validator  
A regular‑expression validator prevents `<` and `>` characters in text fields. This blocks user attempts to insert HTML or JavaScript.

It is used for:
- Meal names  
- Workout types  
- Workout notes  

This significantly reduces the risk of stored or reflected XSS.

### Range Validation for Numeric Fields  
All numeric fields include minimum and maximum bounds to prevent unrealistic or malicious values. Examples include:
- Protein grams between 0 and 300  
- Meal calories between 0 and 5000  
- Workout duration between 1 and 600 minutes  
- Sleep hours between 0 and 24  
- Body weight between 30 and 400 kg  

These validators ensure data quality, protect against extreme values, and keep analytics reliable.

Together, these validation strategies meet the project requirement for secure and well‑formed data handling.

---

## 3. Authentication and Authorization

- Django’s authentication system securely hashes and salts all passwords.  
- DRF token authentication restricts API access to authenticated users.  
- All fitness data models link directly to the user who created them.  
- Views enforce strict ownership checks so that users may interact only with their own data.

These measures prevent unauthorized data exposure or manipulation.

---

## 4. CSRF Protections

Django’s built‑in CSRF middleware is enabled for all server‑rendered forms.  
API endpoints that rely on token authentication are exempt, preventing conflicts during JSON requests while still enforcing strong authentication requirements.

---

## 5. EC2 Deployment Hardening

### Security Groups  
Only SSH (22) and the application port (8000) are open. Everything else is blocked at the network level.

### SSH Configuration  
The instance uses key‑based authentication only. Password logins are disabled.

### File System Isolation  
The container is isolated from the host system, and no host file system is mounted into the application container.

---

## 6. Known Limitations and Future Improvements

- Add HTTPS using Nginx or AWS Load Balancer  
- Implement API rate limiting to reduce brute‑force and abuse risks  
- Add more granular API permissions and throttling  
- Implement detailed logging and audit trails  
- Add automated deployment via GitHub Actions or similar CI/CD pipeline  

---

## 7. Summary

StrideBite applies multiple layers of hardening including environment‑based configuration, strict input validation, authentication controls, CSRF protection, limited container privileges, and EC2 network restrictions. These combined measures provide a strong security baseline and fulfill the requirements for Milestone 2.
