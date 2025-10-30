# SHIELD Dataset Documentation

This folder contains two comprehensive cybersecurity datasets used for training and testing attack detection models.

---

## 📊 Dataset Overview

### Dataset 1: Modified_SQL_Dataset.csv
**Purpose:** SQL Injection Detection and Prevention

**Statistics:**
- **Total Records:** 30,920 samples
- **Format:** CSV with 2 columns (Query, Label)
- **Label Distribution:** Binary classification (0 = benign, 1 = malicious)

**Content Description:**
This dataset contains a comprehensive collection of SQL injection attack patterns and payloads. It includes:

- **Classic SQL Injection Patterns:**
  - Union-based injections
  - Boolean-based blind SQL injection
  - Time-based blind SQL injection
  - Error-based SQL injection
  - Stacked queries
  
- **Obfuscation Techniques:**
  - URL encoding variations
  - Character encoding bypass
  - Comment-based obfuscation
  - Case manipulation
  - Whitespace variation
  
- **Database-Specific Attacks:**
  - MySQL-specific functions (load_file, benchmark)
  - PostgreSQL attacks (pg_sleep)
  - Oracle database exploits (utl_inaddr.get_host_address)
  - MS SQL Server attacks (waitfor delay, xp_cmdshell)
  
- **Advanced Techniques:**
  - Second-order SQL injection
  - Out-of-band SQL injection
  - Filter bypass methods
  - WAF evasion techniques

**Example Samples:**
```sql
" or pg_sleep(__TIME__)  --
admin' or '1'='1'#
' UNION SELECT username, password FROM users--
```

---

### Dataset 2: Attack_Dataset.csv
**Purpose:** Multi-Category Cyber Attack Detection

**Statistics:**
- **Total Records:** 14,181 unique attack scenarios
- **Format:** CSV with 15 columns
- **Categories:** 50+ attack types across multiple domains

**Column Structure:**
1. **ID** - Unique identifier
2. **Title** - Attack name/title
3. **Category** - Primary category (AI Agents & LLM Exploits, Mobile Security, etc.)
4. **Attack Type** - Specific attack classification
5. **Scenario Description** - Detailed explanation of the attack
6. **Tools Used** - Required tools and software
7. **Attack Steps** - Step-by-step execution guide
8. **Target Type** - Affected systems/applications
9. **Vulnerability** - Underlying weakness exploited
10. **MITRE Technique** - MITRE ATT&CK framework mapping
11. **Impact** - Potential consequences
12. **Detection Method** - How to identify the attack
13. **Solution** - Mitigation strategies
14. **Tags** - Keywords for categorization
15. **Source** - Reference materials

**Attack Categories Covered:**

#### 1. **Injection Attacks (Entries 1-49)**
- SQL Injection (Union, Error-based, Blind, Boolean-based, Time-based)
- Stored SQL Injection
- Second-Order SQL Injection
- Out-of-Band SQL Injection
- Login bypass techniques

#### 2. **Cross-Site Scripting (XSS) (Entries 12-19)**
- Stored XSS (Persistent)
- Reflected XSS
- DOM-Based XSS
- Self-XSS
- Mutated XSS (mXSS)
- Polyglot XSS
- Attribute Injection XSS
- JavaScript Context Injection

#### 3. **Cross-Site Request Forgery (CSRF) (Entries 20-28)**
- GET-Based CSRF
- POST-Based CSRF
- Stored CSRF (via XSS)
- Cross-Origin CSRF
- CSRF via XMLHttpRequest
- JSON/REST API CSRF
- Hybrid App CSRF

#### 4. **Authentication & Session Attacks (Entries 28-47)**
- Credential Stuffing
- Brute-Force Login
- Username Enumeration
- Session Fixation
- Session Hijacking
- Insecure Password Reset
- Default Credentials
- Weak Password Policy
- Broken Multi-Factor Authentication
- JWT Authentication Bypass

#### 5. **Data Exposure (Entries 39-49)**
- Unencrypted Data in Transit
- Unencrypted Data at Rest
- Weak Password Hashing
- Sensitive Information in URLs
- Exposed API Keys
- Sensitive Data in Logs
- Insecure JWT Management
- Backup Files Exposure
- Missing Access Control
- Information Exposure via Metadata

#### 6. **Subdomain Takeover (Entries 110-117)**
- CNAME to Unclaimed GitHub Repo
- CNAME to Unclaimed Heroku App
- Unclaimed AWS S3 Bucket
- Unclaimed Azure Blob/Web App
- Fastly CDN Takeover
- Bitbucket Pages Takeover
- Expired Domain Forwarding
- Wildcard CNAME Misconfiguration

#### 7. **Redirect Vulnerabilities (Entries 118-129)**
- Basic URL Parameter Redirect
- Relative Path Redirect Abuse
- Protocol-Based Bypass
- Obfuscation Bypass
- JavaScript Location Redirect
- Meta Refresh Tag Redirect
- HTTP 3xx Header Redirect
- OAuth Flow Redirect
- Referer/returnTo Parameter Abuse
- Chained Redirects
- Password Reset Poisoning

#### 8. **Host Header Attacks (Entries 130-135)**
- Cache Poisoning via Host Header
- SSRF via Host Header
- Virtual Host Routing Bypass
- Open Redirect via Host Header
- Reflected XSS via Host Header
- CSRF Token Bypass

#### 9. **Clickjacking (Entries 136-146)**
- Basic iFrame-Based Clickjacking
- Likejacking (Social Media)
- Cursor Spoofing/Click Offset
- Transparent Layer Overlay
- CSRF Combo Attack
- Drag-and-Drop Clickjacking
- File Upload Clickjacking
- Like/Subscribe Clickjacking
- OAuth Flow Clickjacking
- Invisible CAPTCHA Clickjacking
- Popup/Window Redressing

#### 10. **Reconnaissance & Scanning (Entries 147-149)**
- External Port Scanning
- Web-Based Port Scanning (SSRF)
- JavaScript-Based Client-Side Scanning

---

## 🎯 Use Cases

### For Developers:
- Training machine learning models for attack detection
- Testing WAF (Web Application Firewall) rules
- Building intrusion detection systems
- Creating security awareness training materials

### For Security Researchers:
- Analyzing attack patterns and trends
- Developing new detection algorithms
- Benchmarking security tools
- Understanding attack evolution

### For Educational Purposes:
- Teaching cybersecurity concepts
- Hands-on penetration testing labs
- Security certification preparation
- Red team/Blue team exercises

---

## 🔒 Ethical Usage Guidelines

⚠️ **IMPORTANT:** These datasets are provided for **educational and defensive security purposes only**.

**Permitted Uses:**
- Academic research and study
- Security tool development and testing
- Defensive security training
- Penetration testing on authorized systems
- Building detection/prevention systems

**Prohibited Uses:**
- Unauthorized access to systems
- Malicious attacks on real targets
- Illegal activities
- Bypassing security controls without permission

---

## 📁 File Structure

```
dataset/
├── Attack_Dataset.csv          # 14,181 multi-category attack scenarios
├── Modified_SQL_Dataset.csv    # 30,920 SQL injection samples
└── readme.md                   # This documentation file
```

---

## 🏷️ Tags & Keywords

**Modified_SQL_Dataset:**
`SQL Injection`, `Database Security`, `SQLi`, `OWASP Top 10`, `Web Security`, `Injection Attacks`, `Union-based`, `Blind SQLi`, `Time-based`, `Error-based`, `Boolean-based`, `WAF Bypass`

**Attack_Dataset:**
`Cybersecurity`, `Penetration Testing`, `OWASP`, `MITRE ATT&CK`, `XSS`, `CSRF`, `Session Hijacking`, `Clickjacking`, `SSRF`, `Subdomain Takeover`, `Open Redirect`, `Authentication Bypass`, `Information Disclosure`, `Web Application Security`

---

## 📚 References

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **MITRE ATT&CK:** https://attack.mitre.org/
- **PortSwigger Web Security Academy:** https://portswigger.net/web-security
- **HackerOne Reports:** https://hackerone.com/hacktivity
- **Bugcrowd University:** https://www.bugcrowd.com/hackers/bugcrowd-university/

---

## ⚖️ Legal Disclaimer

This dataset is provided "AS IS" for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and regulations. The dataset maintainers are not responsible for any misuse or illegal activities performed using this data.

---

## 📝 Version Information

- **Last Updated:** 2025
- **Attack_Dataset Version:** 1.0 (14,181 entries)
- **Modified_SQL_Dataset Version:** 1.0 (30,920 entries)

---

## 🤝 Contribution

If you have suggestions for improving this dataset or documentation, please submit your feedback to the project maintainers.

---

**Remember: With great power comes great responsibility. Use these resources ethically and legally.**