---
name: aio-security
description: Security engineering guidelines for addressing Weak Content Security Policy (CSP) and Cross-Role Authorization / Redirection vulnerabilities.
---

# AIO Security Engineering Reference

This document outlines defense, remediation, and verification standards for specific vulnerability findings identified in application infrastructure.

---

## 1. Weak Content Security Policy (CSP)

### Vulnerability Profile
* **Severity**: CVSS v3.1: 5.4 (MEDIUM) — `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`
* **Risk Summary**: A Content-Security-Policy that only implements `upgrade-insecure-requests` fails to restrict where resources (such as scripts, frames, and styles) can be loaded from or where data can be sent. Without strict directives, the application remains vulnerable to Cross-Site Scripting (XSS), data exfiltration, and clickjacking.

### Remediation Standards

A robust CSP must define boundary constraints for different resource types. Implement the following configuration patterns depending on the backend environment.

#### A. Nginx Configuration
Add directive headers in your server or location block:
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'; upgrade-insecure-requests;" always;
```

#### B. Node.js (Helmet / Express)
Use the Helmet middleware to programmatically define strict security policies:
```javascript
const express = require('express');
const helmet = require('helmet');
const app = express();

app.use(
  helmet.contentSecurityPolicy({
    useDefaults: true,
    directives: {
      "default-src": ["'self'"],
      "script-src": ["'self'"],
      "style-src": ["'self'", "'unsafe-inline'"],
      "img-src": ["'self'", "data:"],
      "frame-ancestors": ["'none'"],
      "upgrade-insecure-requests": [],
    },
  })
);
```

#### C. Meta Tags (Static HTML)
For static frontends without header control, place this within the `<head>` block:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; upgrade-insecure-requests;">
```

---

## 2. Cross-Role Redirect (Admin → Merchant)

### Vulnerability Profile
* **Severity**: CVSS v3.1: 4.3 (MEDIUM) — `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`
* **Risk Summary**: Role confusion or authorization bypass occurring during redirection processes (e.g., accessing `/admin/login` with merchant credentials and getting redirected/treated as authorized, or accessing resources belonging to another role due to lack of server-side role validation). Redirection mechanisms must explicitly validate that the authenticated identity matches the requested route scope before performing actions or rendering UI.

### Remediation Standards

To prevent cross-role logic flaws, session checks must enforce role restrictions on the server-side before execution or redirection.

#### A. Express middleware example (Node.js)
```javascript
// Middleware to enforce role boundaries
function requireRole(allowedRoles) {
  return (req, res, next) => {
    // 1. Verify user is authenticated
    if (!req.session || !req.session.user) {
      return res.redirect('/login');
    }

    // 2. Validate current user's role against allowed roles
    const userRole = req.session.user.role; // e.g., 'admin', 'merchant'
    if (!allowedRoles.includes(userRole)) {
      // Clear token/session or redirect to appropriate dashboard based on their actual role
      if (userRole === 'merchant') {
        return res.redirect('/merchant/dashboard');
      }
      return res.redirect('/unauthorized');
    }

    next();
  };
}

// Apply boundaries to specific routing branches
app.use('/admin', requireRole(['admin']), adminRouter);
app.use('/merchant', requireRole(['merchant']), merchantRouter);
```

#### B. Remediation Checklist
1. **Explicit Server-Side Session Checking**: Never rely on frontend routing or parameter state (e.g., query strings or headers) for authorization logic.
2. **Explicit Role Validation**: Always validate `user.role` on every protected route. If a merchant hits an admin-specific authentication check or route, strictly redirect them back to the merchant space (or terminate the session) rather than allowing cross-boundary access.
3. **Session Regeneration**: Regenerate session identifiers upon user login and privilege levels transition to mitigate session fixation issues.
