#!/usr/bin/env python3
import sys
import platform
import json
import urllib.request
import urllib.error
import subprocess
import argparse
import readline 


# get Operating system
os_name = platform.system()
os_version = platform.release()


# ==========================================
# Configuration 
# ==========================================
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5-coder:1.5b" 

# ==========================================
# Colors for Terminal UI 
# ==========================================
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ==========================================
#           Safety Blacklist 
# ==========================================
DANGEROUS_PATTERNS = [
    "rm -rf /", "rm -rf *", "mkfs", "dd if=", "> /dev/sda", 
    ":(){ :|:& };:", "chmod -R 777 /"
]

def print_colored(text, color, end='\n'):
    print(f"{color}{text}{Colors.RESET}", end=end)

def clean_command(cmd):
    cmd = cmd.strip()
    
    # (Markdown)
    if cmd.startswith("```bash"): cmd = cmd[7:]
    elif cmd.startswith("```sh"): cmd = cmd[5:]
    elif cmd.startswith("```"): cmd = cmd[3:]
    if cmd.endswith("```"): cmd = cmd[:-3]
    
    cmd = cmd.strip()
    
    # (Inline Code)
    if cmd.startswith("`") and cmd.endswith("`"):
        cmd = cmd[1:-1]
        
    return cmd.strip()

def check_safety(cmd):
    for pattern in DANGEROUS_PATTERNS:
        if pattern in cmd:
            return False
    return True

def get_command_from_llm(user_input, model):
    system_prompt = (
        f"You are an expert {os_name} terminal assistant. "
        "The user will describe a task in natural language. "
        f"Your ONLY job is to output the EXACT {os_name} command to accomplish this task. "
        "DO NOT use markdown, DO NOT use backticks, DO NOT explain anything. "
        "Just output the raw executable command."
    )
    
    payload = {
        "model": model,
        "prompt": f"Task: {user_input}\nCommand:",
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1 
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return clean_command(result.get("response", ""))
    except urllib.error.URLError:
        print_colored("\n[Error] Cannot connect to Ollama. Is it running? (systemctl start ollama or run 'ollama serve')", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n[Error] Something went wrong: {e}", Colors.RED)
        sys.exit(1)

def execute_command(cmd):
    """run command and get yes"""
    print_colored(f"\nExecuting: {cmd}", Colors.CYAN)
    print("-" * 40)
    try:
        subprocess.run(cmd, shell=True, check=False)
    except KeyboardInterrupt:
        print_colored("\n[Info] Execution cancelled by user (Ctrl+C).", Colors.YELLOW)
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Terminal AI Assistant (Powered by Ollama)")
    parser.add_argument("query", nargs="+", help="Describe what you want to do (e.g., 'extract archive.tar.gz')")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help="Ollama model to use")
    
    args = parser.parse_args()
    user_query = " ".join(args.query)
    
    print_colored(f"{Colors.BOLD}🤖 Thinking...{Colors.RESET}", Colors.CYAN, end='\r')
    
    command = get_command_from_llm(user_query, args.model)
    
    sys.stdout.write("\033[K")
    
    if not command:
        print_colored("AI did not return any command.", Colors.RED)
        sys.exit(1)
        
    print_colored("💡 Suggested Command:", Colors.GREEN)
    print_colored(f"  {command}", Colors.BOLD)
    
    if not check_safety(command):
        print_colored("\n[WARNING] This command looks EXTREMELY DANGEROUS!", Colors.RED)
    
    while True:
        print_colored("\nOptions: [y] Execute | [n] Cancel | [e] Edit", Colors.YELLOW)
        choice = input(f"{Colors.BOLD}What to do? (Y/n/e): {Colors.RESET}").strip().lower()
        
        if choice == 'y' or choice == '':
            execute_command(command)
            break
        elif choice == 'e':
            print_colored("\nEdit your command (Press Enter when done):", Colors.CYAN)
            
            def hook():
                readline.insert_text(command)
                readline.redisplay()
            
            readline.set_pre_input_hook(hook)
            try:
                edited_cmd = input(f"> ")
            finally:
                readline.set_pre_input_hook()
                
            if edited_cmd.strip():
                execute_command(edited_cmd)
            break
        elif choice == 'n':
            print_colored("Cancelled.", Colors.YELLOW)
            break
        else:
            print_colored("Invalid choice.", Colors.RED)

if __name__ == "__main__":
    main()
