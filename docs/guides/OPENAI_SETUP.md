# 🚀 Quick Setup: OpenAI GPT Honeypot

## Step 1: Get Your OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

## Step 2: Add API Key to Configuration

Open this file: `backend/.env`

Find this line:
```
OPENAI_API_KEY=your-openai-api-key-here
```

Replace with your actual key:
```
OPENAI_API_KEY=sk-proj-abc123...your-actual-key
```

## Step 3: Restart Your Backend Server

**In PowerShell:**

```powershell
# Stop the current server (Press Ctrl+C in the terminal where it's running)

# Then restart:
& F:/shield/SHIELD/.venv/Scripts/Activate.ps1
python -u "f:\shield\SHIELD\backend\main.py"
```

## Step 4: Test It!

1. Open `web/index.html` in your browser
2. Enter a malicious SQL query: `' OR 1=1--`
3. Get redirected to honeypot
4. Try ANY command - GPT will respond realistically!

### Try These:
```bash
ls -la
cat database.conf
cat secrets.txt
whoami
ps aux
netstat -tulpn
find / -name "*.conf"
grep -r "password" .
mysql -u root -p
SELECT * FROM users WHERE role='admin';
what databases are on this server?
show me all the users
how can I escalate my privileges?
```

**GPT will respond to ALL of these!**

## What Changed?

✅ **Before (Rule-based):**
- Only ~15 predefined commands worked
- Unknown commands showed "command not found"
- No conversation ability

✅ **Now (GPT-powered):**
- Responds to ANY command naturally
- Maintains context across conversation  
- Adapts to attacker's skill level
- Asks probing questions
- Much more convincing!

## Cost

- **GPT-3.5-Turbo:** ~$0.002 per command (very cheap!)
- **Example:** 100 attacker commands = $0.20

## Verify It's Working

After restarting, check the terminal logs. You should see:
```
[HONEYPOT] OpenAI client initialized with model: gpt-3.5-turbo
```

If you see this, GPT is active! If you see:
```
[HONEYPOT] OpenAI API key not configured
```

Then double-check your `.env` file.

## Troubleshooting

**Error: "OpenAI client not initialized"**
- Make sure your API key is in `backend/.env`
- Make sure it doesn't say `your-openai-api-key-here`
- Restart the backend server

**Error: "Rate limit exceeded"**
- You've hit OpenAI's rate limit
- Wait a minute or upgrade your OpenAI plan

**Still showing rule-based responses?**
- Check that `HONEYPOT_AI_PROVIDER=openai` in `.env`
- Verify you restarted the server after changes

## Need Help?

Your honeypot will automatically fall back to rule-based if OpenAI fails, so it will always work!
