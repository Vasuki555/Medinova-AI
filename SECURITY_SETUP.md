# MediNova AI - Security Setup Guide

## 🔐 Critical Security Steps Before Deployment

### **IMPORTANT: Your .env file contains exposed credentials!**

Your current `.env` file has real credentials that **MUST BE ROTATED** before any public deployment:

1. **MongoDB Password is Exposed**: `vasuki12072006.`
2. **JWT Secret Keys are Exposed**: Real cryptographic keys are visible
3. **API Keys May Be Compromised**: Gemini API key format appears incorrect

---

## 📋 Immediate Actions Required

### 1. Rotate MongoDB Credentials

```bash
# In MongoDB Atlas Dashboard:
1. Go to https://cloud.mongodb.com
2. Select your cluster → Database Access
3. Click on user "citizen_admin"
4. Click "Edit" → "Edit Password"
5. Generate a new strong password
6. Update MONGODB_URL in your .env file
```

### 2. Generate New JWT Secrets

```bash
# Run this in your terminal to generate secure keys:
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64))"
python -c "import secrets; print('JWT_REFRESH_SECRET_KEY=' + secrets.token_urlsafe(64))"

# Copy the output and update your .env file
```

### 3. Get Valid Gemini API Key

```bash
# Your current key format is incorrect (starts with AQ. instead of AIza...)
# 
# To get a valid key:
1. Go to: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy the key (should start with AIza...)
4. Update GEMINI_API_KEY in your .env file
```

---

## 🛡️ Security Checklist

### Database Security

- [x] **MongoDB Atlas IP Whitelist**: Configure network access
  - Development: Add your current IP
  - Production: Add only production server IPs
  - Never use `0.0.0.0/0` (allow all) in production

- [x] **Database User Permissions**: Use principle of least privilege
  - Create separate users for different environments
  - Production user should have read/write only on specific database
  - Never use admin credentials in application

- [x] **Connection String Security**:
  - ✅ Uses TLS/SSL by default
  - ✅ Certificate validation enabled (fixed in recent updates)
  - ❌ Credentials in connection string (consider using AWS Secrets Manager in production)

### Authentication Security

- [x] **JWT Configuration**:
  - ✅ Strong secret keys (after rotation)
  - ✅ Reasonable expiration times (30 min access, 7 days refresh)
  - ✅ Separate secrets for access and refresh tokens
  - ✅ HS256 algorithm (consider RS256 for better security)

- [x] **Password Security**:
  - ✅ Bcrypt hashing with salt rounds = 12
  - ✅ Password strength validation (min 8 chars, uppercase, lowercase, number, special char)
  - ✅ Failed login attempt tracking (5 attempts = 15 min lockout)
  - ✅ Password reset tokens hashed in database

- [x] **Rate Limiting**:
  - ✅ Enabled on authentication endpoints
  - ✅ Production-ready limits configured
  - ⚠️  Using in-memory rate limiting (upgrade to Redis for production)

### API Security

- [x] **CORS Configuration**:
  - ✅ Localhost origins for development
  - ⚠️  Must update for production (add your domain only)
  - ✅ Fails fast if no production origins configured

- [x] **Input Validation**:
  - ✅ Pydantic models validate all inputs
  - ✅ Custom validators for phone, email, ObjectId
  - ✅ SQL injection protection (using MongoDB, not SQL)
  - ✅ XSS protection through input sanitization

- [x] **File Upload Security**:
  - ✅ File size limits (50MB max)
  - ✅ MIME type validation
  - ✅ File extension validation
  - ⚠️  Consider virus scanning for production

### Infrastructure Security

- [ ] **HTTPS/TLS**:
  - ❌ Not configured (required for production)
  - Use Let's Encrypt for free SSL certificates
  - Configure reverse proxy (nginx/Apache) with SSL

- [ ] **Environment Variables**:
  - ✅ .env file in .gitignore
  - ✅ .env.example provided
  - ⚠️  Consider using environment-specific secret managers

- [ ] **Logging & Monitoring**:
  - ✅ Structured JSON logging
  - ⚠️  Configure centralized logging (e.g., ELK stack, CloudWatch)
  - ⚠️  Set up error tracking (e.g., Sentry)
  - ⚠️  Monitor for security events (failed logins, rate limit hits)

---

## 🚀 Production Deployment Checklist

### Pre-Deployment

- [ ] Rotate all credentials (MongoDB, JWT secrets, API keys)
- [ ] Set `ENVIRONMENT=production` in .env
- [ ] Update `CORS_ORIGINS` to production domain only
- [ ] Configure Redis server for rate limiting
- [ ] Set up SMTP with production email service
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure database backups
- [ ] Set up monitoring and alerts

### Application Configuration

- [ ] Disable DEBUG mode (`DEBUG=False`)
- [ ] Disable auto-reload (`RELOAD=False`)
- [ ] Set appropriate rate limits for your traffic
- [ ] Configure log aggregation
- [ ] Set up health check endpoints monitoring
- [ ] Review and test error handling

### Infrastructure

- [ ] Use production-grade web server (Gunicorn/Uvicorn with multiple workers)
- [ ] Configure reverse proxy (nginx) with SSL
- [ ] Set up firewall rules (only allow HTTPS traffic)
- [ ] Configure CDN for static assets
- [ ] Set up load balancer (if needed)
- [ ] Configure auto-scaling policies

### Compliance (Healthcare Data)

- [ ] **HIPAA Compliance** (if applicable):
  - Encrypt data at rest
  - Encrypt data in transit
  - Implement audit logging
  - Sign Business Associate Agreements (BAAs)
  - Regular security assessments

- [ ] **GDPR Compliance** (if applicable):
  - Implement data deletion endpoints
  - Add consent management
  - Provide data export functionality
  - Privacy policy updates

---

## 🔍 Security Testing

### Before Going Live

```bash
# 1. Run security audit on dependencies
cd backend
pip install safety
safety check

cd frontend
npm audit

# 2. Test rate limiting
# Use a tool like Apache Bench or Locust to verify rate limits work

# 3. Test authentication flows
# - Try SQL injection in login forms
# - Test XSS in user inputs
# - Verify password reset flow
# - Test token expiration

# 4. Check for exposed secrets
# Use tools like truffleHog or gitleaks to scan for credentials in git history
```

### Recommended Security Tools

- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Security testing platform
- **Snyk**: Dependency vulnerability scanner
- **SonarQube**: Code quality and security analysis

---

## 📞 Security Incident Response

If you suspect a security breach:

1. **Immediate Actions**:
   - Rotate all credentials (database, JWT secrets, API keys)
   - Review access logs for suspicious activity
   - Notify affected users if data was compromised

2. **Investigation**:
   - Identify scope of breach
   - Determine what data was accessed
   - Document timeline of events

3. **Remediation**:
   - Patch vulnerabilities
   - Update security measures
   - Conduct security audit

4. **Prevention**:
   - Implement additional monitoring
   - Update security policies
   - Train team on security best practices

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [MongoDB Security Checklist](https://docs.mongodb.com/manual/administration/security-checklist/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)

---

## ⚠️ Disclaimer

This security guide provides general recommendations. For healthcare applications handling protected health information (PHI), consult with legal and compliance experts to ensure full regulatory compliance.

**Last Updated**: 2024
**Review Frequency**: Quarterly or after any security incident
