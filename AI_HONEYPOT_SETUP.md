# 🤖 AI-Powered Honeypot Setup Guide

Your honeypot is now ready to use AI to simulate your website's backend! Here are your options:

---

## 📋 Quick Summary

The honeypot can work in **3 modes**:

1. **Rule-Based (Default)** - Works immediately, no setup required
2. **OpenAI GPT** - More realistic, requires API key
3. **Anthropic Claude** - Alternative AI, requires API key

---

## 🚀 Option 1: Rule-Based System (Already Working!)

**Status: ✅ Active by default**

This is what you see in the screenshot - it works immediately without any setup!

- No API keys needed
- No additional packages needed
- Responds to common commands (ls, cat, whoami, ps, netstat, etc.)
- Shows fake but realistic data

**You're already using this!** The error you see is just because the command wasn't recognized.

---

## 🌟 Option 2: OpenAI GPT Integration (Recommended)

Get **much more realistic** responses that adapt to any command!

### Step 1: Install OpenAI Package

```powershell
# Activate your virtual environment
& F:/shield/SHIELD/.venv/Scripts/Activate.ps1

# Install OpenAI
pip install openai
```

### Step 2: Get API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Create a new API key
4. Copy the key (starts with `sk-...`)

### Step 3: Set Environment Variable

**Temporary (for current session):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
$env:HONEYPOT_AI_PROVIDER="openai"
```

**Permanent (Windows):**
```powershell
# Set permanently in Windows
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-your-key-here', 'User')
[System.Environment]::SetEnvironmentVariable('HONEYPOT_AI_PROVIDER', 'openai', 'User')
```

### Step 4: Restart Backend Server

```powershell
# Press Ctrl+C to stop current server
# Then restart
& F:/shield/SHIELD/.venv/Scripts/Activate.ps1
python -u "f:\shield\SHIELD\backend\main.py"
```

### Cost Estimate:
- GPT-3.5-Turbo: ~$0.002 per interaction (very cheap!)
- GPT-4: ~$0.03 per interaction (better quality)

---

## 🔷 Option 3: Anthropic Claude (Alternative)

Similar to OpenAI but sometimes better at role-playing.

### Step 1: Install Anthropic Package

```powershell
& F:/shield/SHIELD/.venv/Scripts/Activate.ps1
pip install anthropic
```

### Step 2: Get API Key

1. Go to: https://console.anthropic.com/
2. Sign up and get API key

### Step 3: Set Environment Variable

```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
$env:HONEYPOT_AI_PROVIDER="anthropic"
```

### Step 4: Restart Backend Server

---

## 🎯 How It Works

### Rule-Based Response (Current):
```
Attacker: ls
Response: drwxr-xr-x 2 root root 4096 Oct 15 12:34 config
          drwxr-xr-x 3 www-data www-data 4096 Oct 20 08:22 logs
          ...
```

### AI-Powered Response (With GPT):
```
Attacker: ls
Response: total 48
          drwxr-xr-x 2 root root 4096 Oct 15 12:34 config
          drwxr-xr-x 3 www-data www-data 4096 Oct 20 08:22 logs
          -rw-r--r-- 1 root root 1834 Oct 10 14:55 database.conf
          -rw-r--r-- 1 root root 892 Sep 30 09:12 secrets.txt
          drwxr-xr-x 5 root root 4096 Oct 25 16:41 backups

Attacker: tell me about the database
Response: This server is running PostgreSQL 14.2. The main database 
          is 'shield_db' located in /var/lib/postgresql/14/main/. 
          You can find the configuration in database.conf. Would you 
          like to see the connection details?
```

**GPT can:**
- ✅ Respond to ANY command (not just predefined ones)
- ✅ Maintain conversation context
- ✅ Act more convincingly as a real server
- ✅ Adapt responses based on attacker's skill level
- ✅ Ask probing questions to learn attacker's goals

---

## 🔧 Configuration File Method

Instead of environment variables, create a config file:

**Create: `backend/.env`**
```ini
# Honeypot Configuration
HONEYPOT_AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# Optional: Choose GPT model
OPENAI_MODEL=gpt-3.5-turbo
```

Then install python-dotenv:
```powershell
pip install python-dotenv
```

---

## 📊 Comparison

| Feature | Rule-Based | OpenAI GPT | Claude |
|---------|-----------|-----------|---------|
| **Cost** | Free | ~$0.002/cmd | ~$0.001/cmd |
| **Setup** | None | API key | API key |
| **Realism** | Good | Excellent | Excellent |
| **Flexibility** | Limited | Very High | Very High |
| **Commands** | ~15 preset | Unlimited | Unlimited |
| **Context Memory** | No | Yes | Yes |

---

## 🧪 Testing After Setup

### Test Rule-Based (Current):
```bash
ls                    # Works
cat secrets.txt       # Works
random_command        # Shows "command not found"
```

### Test AI-Powered:
```bash
ls                           # Works
cat secrets.txt              # Works
random_command               # GPT improvises a response!
what databases do you have?  # GPT understands and responds!
show me the password         # GPT acts vulnerable but realistic
```

---

## 🎯 Recommended Setup

**For Testing/Demo:**
→ Use **Rule-Based** (current setup, no cost)

**For Real Deployment:**
→ Use **OpenAI GPT-3.5-Turbo** (best value, $0.002 per interaction)

**For Maximum Realism:**
→ Use **OpenAI GPT-4** (highest quality, $0.03 per interaction)

---

## 🚨 Current Status

✅ **Rule-based honeypot is working!**
- The error you saw is expected for unknown commands
- Try these commands in the console:
  - `help` - See available commands
  - `ls` - List files
  - `cat secrets.txt` - View fake secrets
  - `whoami` - Shows "root"
  - `ps` - Show processes
  - `netstat` - Network info

---

## 💡 Quick Start Commands to Try

```bash
help
ls
cat secrets.txt
cat database.conf
whoami
id
ps
netstat
SELECT * FROM users
exit
```

All of these work **right now** without any AI setup!

---

## Need Help?

The honeypot is **already working** with rule-based responses. You only need to add OpenAI if you want even more realistic, adaptive responses.

**Current capabilities:**
- ✅ Responds to 15+ common Linux commands
- ✅ Shows fake sensitive data (passwords, configs)
- ✅ Logs all attacker activity
- ✅ Keeps them engaged
- ✅ Works immediately, no setup

**With AI (optional upgrade):**
- ✅ All of the above PLUS
- ✅ Unlimited command support
- ✅ Natural conversation
- ✅ Context awareness
- ✅ Adaptive responses
