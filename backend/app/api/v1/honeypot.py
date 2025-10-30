"""
SHIELD Honeypot Endpoint

Rule-based honeypot that simulates a vulnerable server to engage attackers
and gather intelligence about their methods.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/interact")
async def honeypot_interaction(request: Request):
    """AI-powered honeypot endpoint that simulates a vulnerable server"""
    try:
        data = await request.json()
        attacker_input = data.get("input", "").strip()
        session_id = data.get("session_id", "unknown")
        
        # Log the attacker's activity
        logger.info(f"[HONEYPOT] Session: {session_id} | Input: {attacker_input}")
        
        if not attacker_input:
            return JSONResponse({
                "success": True,
                "response": "[ERROR] No command provided"
            })
        
        # Generate rule-based response
        ai_response = generate_honeypot_response(attacker_input, session_id)
        
        # Log the response
        logger.info(f"[HONEYPOT] Session: {session_id} | Response: {ai_response[:100]}...")
        
        return JSONResponse({
            "success": True,
            "response": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"[HONEYPOT ERROR] {str(e)}")
        return JSONResponse({
            "success": False,
            "error": "Internal server error"
        }, status_code=500)


def generate_honeypot_response(command: str, session_id: str) -> str:
    """
    Generate realistic server responses to commands.
    This is a rule-based system. You can later replace with OpenAI/Claude API.
    """
    cmd_lower = command.lower().strip()
    
    # Help command
    if cmd_lower in ['help', '--help', '-h']:
        return """Available commands:
ls, cd, pwd, cat, whoami, id, ps, netstat, ifconfig, mysql, psql, exit
Type any Linux command to interact with the system."""
    
    # Directory listing
    elif cmd_lower == 'ls' or cmd_lower.startswith('ls '):
        return """drwxr-xr-x 2 root root 4096 Oct 15 12:34 config
drwxr-xr-x 3 www-data www-data 4096 Oct 20 08:22 logs
-rw-r--r-- 1 root root 1834 Oct 10 14:55 database.conf
-rw-r--r-- 1 root root 892 Sep 30 09:12 secrets.txt
drwxr-xr-x 5 root root 4096 Oct 25 16:41 backups"""
    
    # Present working directory
    elif cmd_lower == 'pwd':
        return "/var/www/shield-backend"
    
    # User info
    elif cmd_lower == 'whoami':
        return "root"
    
    elif cmd_lower == 'id':
        return "uid=0(root) gid=0(root) groups=0(root)"
    
    # File reading
    elif cmd_lower.startswith('cat '):
        filename = command[4:].strip()
        if 'secret' in filename.lower() or 'password' in filename.lower():
            return """[SECRETS FILE]
DB_PASSWORD=admin123_temp
API_KEY=sk-test-abc123def456
JWT_SECRET=supersecret_change_me
ADMIN_TOKEN=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."""
        elif 'database' in filename.lower() or 'config' in filename.lower():
            return """[DATABASE CONFIG]
HOST=localhost
PORT=5432
DATABASE=shield_db
USERNAME=admin
PASSWORD=admin123_temp
SSL_MODE=disable"""
        else:
            return f"cat: {filename}: No such file or directory"
    
    # Process listing
    elif cmd_lower in ['ps', 'ps aux']:
        return """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  16840  3892 ?        Ss   Oct25   0:02 /sbin/init
www-data  1234  0.5  2.1 245680 43892 ?        Sl   08:00   1:23 /usr/bin/python3 app.py
postgres  5678  0.2  1.8 123456 37284 ?        Ss   Oct25   2:34 /usr/lib/postgresql/14/bin/postgres"""
    
    # Network info
    elif cmd_lower in ['netstat', 'netstat -tulpn']:
        return """Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      892/sshd
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1234/nginx
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      5678/postgres"""
    
    # Database access attempts
    elif 'mysql' in cmd_lower or 'psql' in cmd_lower:
        return """[WARNING] Database access detected
Connecting to PostgreSQL...
shield_db=> (You are now connected to the database)
Type SQL queries or 'exit' to disconnect"""
    
    # SQL injection attempts
    elif 'select' in cmd_lower and 'from' in cmd_lower:
        return """Query executed successfully:
id | username  | email              | role
---+-----------+--------------------+-------
1  | admin     | admin@shield.io    | admin
2  | developer | dev@shield.io      | user
3  | guest     | guest@shield.io    | guest
(3 rows returned)"""
    
    # Change directory
    elif cmd_lower.startswith('cd '):
        path = command[3:].strip()
        return f"Changed directory to: {path}"
    
    # Exit
    elif cmd_lower in ['exit', 'quit', 'logout']:
        return "[SYSTEM] Connection closed. Goodbye."
    
    # Default response for unknown commands
    else:
        return f"bash: {command}: command not found\nType 'help' for available commands"


# Optional: Log to file for later analysis
def log_to_file(session_id: str, interaction_type: str, content: str):
    """Log honeypot interactions to file for analysis"""
    try:
        with open('honeypot_logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.utcnow()}] {session_id} | {interaction_type}: {content}\n")
    except Exception as e:
        logger.error(f"Failed to log to file: {e}")
