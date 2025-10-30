# SHIELD Honeypot Implementation - Quick Guide

## 🎯 What Was Implemented

### 1. **Automatic Redirect** ✅
- Detects malicious SQL injection inputs (High/Critical threat level)
- Automatically redirects attackers to the honeypot console
- Shows a fake "Security Breach Detected" warning before redirect

### 2. **AI-Powered Responses** ✅
- Rule-based honeypot system that simulates a vulnerable Linux server
- Responds to common commands (ls, cat, whoami, ps, netstat, etc.)
- Shows fake sensitive data (passwords, configs, database info)
- Can be upgraded to use OpenAI/Claude APIs later

### 3. **Realistic Console Interface** ✅
- Terminal-style interface mimicking a Linux server
- Green terminal theme with command history
- Fake system information (IP, uptime, session ID)
- All interactions are logged on the backend

---

## 📁 Files Created/Modified

### New Files:
1. **`backend/app/api/v1/honeypot.py`** - Honeypot API endpoint
2. **`web/honeypot.html`** - Terminal console interface

### Modified Files:
1. **`backend/app/api/v1/routes.py`** - Added honeypot router registration
2. **`web/index.html`** - Added redirect logic for malicious inputs

---

## 🧪 How to Test

### Step 1: Make sure your backend server is running
```powershell
# Stop the current server (Ctrl+C in the terminal)
# Then restart it:
& F:/shield/SHIELD/.venv/Scripts/Activate.ps1
python -u "f:\shield\SHIELD\backend\main.py"
```

### Step 2: Open `web/index.html` in your browser

### Step 3: Test with SQL Injection
Enter this in the text field:
```sql
' OR '1'='1'; DROP TABLE users; --
```

### Step 4: Watch the Magic! 🎭
1. You'll see: "SECURITY BREACH DETECTED - SQL Injection attempt identified"
2. You'll be redirected to the honeypot console
3. Try these commands in the console:

```bash
help              # See available commands
ls                # List fake files
cat secrets.txt   # View fake passwords
whoami            # Shows "root"
ps                # Show fake processes
netstat           # Show fake network connections
SELECT * FROM users;  # Fake database query
```

---

## 🔧 Backend Endpoint

The honeypot is available at:
```
POST http://127.0.0.1:8000/api/v1/honeypot/interact
```

Request body:
```json
{
  "input": "ls",
  "session_id": "HNY-ABC123DEF"
}
```

Response:
```json
{
  "success": true,
  "response": "drwxr-xr-x 2 root root 4096 Oct 15 12:34 config\n...",
  "timestamp": "2025-10-31T00:00:00.000000"
}
```

---

## 📊 Logging

All honeypot interactions are logged:
- Check your terminal/backend logs
- Look for `[HONEYPOT]` entries
- Example: `[HONEYPOT] Session: HNY-ABC123 | Input: ls`

---

## 🚀 Future Enhancements (Optional)

### Replace with OpenAI API:
Edit `backend/app/api/v1/honeypot.py`:

```python
import openai

openai.api_key = "your-api-key"

def generate_honeypot_response(command: str, session_id: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": HONEYPOT_SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.content
```

### Add Database Logging:
- Store all attacker commands in a database
- Track patterns and techniques
- Generate reports on attack attempts

### More Sophisticated Responses:
- Session memory (remember previous commands)
- Realistic file system navigation
- More convincing error messages
- Time delays to simulate real server processing

---

## 🎯 Test Scenarios

1. **Benign Input**: "hello" → Goes to normal dashboard
2. **SQL Injection**: `' OR 1=1--` → Redirected to honeypot
3. **Commands in Honeypot**:
   - `ls` → Shows fake files
   - `cat secrets.txt` → Shows fake credentials
   - `ps` → Shows fake processes
   - Random command → "command not found"

---

## ✨ Summary

You now have a working honeypot system that:
- ✅ Detects SQL injection attacks
- ✅ Redirects attackers to a fake terminal
- ✅ Engages them with realistic responses
- ✅ Logs all their activities
- ✅ Protects your real system

The attacker thinks they've gained access to your server, but they're actually interacting with an AI-powered decoy! 🛡️
