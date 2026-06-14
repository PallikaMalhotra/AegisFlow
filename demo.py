import os
import sys
import database
import engine

# Color codes for terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n{BOLD}{CYAN}======================================================================")
    print(f" {title.upper()}")
    print(f"======================================================================{RESET}\n")

def print_step(step_num, desc):
    print(f"{BOLD}{GREEN}▶ STEP {step_num}: {desc}{RESET}")

def print_ascii_graph_v1():
    print(f"{BOLD}{CYAN}+------------------------------------------------------------+")
    print(f"|                 AEGISFLOW KNOWLEDGE GRAPH                  |")
    print(f"+------------------------------------------------------------+{RESET}")
    print("")
    print(f"  {GREEN}[Decision #1: Zero Hardcoded Secrets (Security Policy)]{RESET}")
    print(f"                            │")
    print(f"                            ▼ (linked constraint)")
    print(f"                {YELLOW}[Symbol: settings.py]{RESET}")
    print("")
    print(f"{CYAN}--------------------------------------------------------------{RESET}")

def print_ascii_graph_v2():
    print(f"{BOLD}{CYAN}+------------------------------------------------------------+")
    print(f"|             AEGISFLOW KNOWLEDGE GRAPH (CONFLICT)           |")
    print(f"+------------------------------------------------------------+{RESET}")
    print("")
    print(f"  {GREEN}[Decision #1: Zero Hardcoded Secrets (Security Policy)]{RESET}")
    print(f"                            │")
    print(f"                            ▼ (linked constraint)")
    print(f"                {YELLOW}[Symbol: settings.py]{RESET}")
    print(f"                            ▲")
    print(f"                            │ {RED}❌ SECURITY VIOLATION!{RESET}")
    print(f"                            │")
    print(f"  {RED}[Commit: f3c1e2a - Hardcoded Staging JWT Key (Human Edit)]{RESET}")
    print("")
    print(f"{CYAN}--------------------------------------------------------------{RESET}")

# Simulated commit details (Secret Key Leakage)
MOCK_DIFF = """diff --git a/settings.py b/settings.py
index e69de29..8f34271 100644
--- a/settings.py
+++ b/settings.py
@@ -1,3 +1,6 @@
 import os
 
-JWT_SECRET = os.environ.get("JWT_SECRET")
+JWT_SECRET = "staging_secret_key_xyz_999" # Temporary secret for staging test
"""

def run_auto_flow():
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 0. Initialize DB
    print_step(0, "Resetting Database")
    database.clear_db()
    print("Database cleared and schema initialized.\n")
    
    input("Press Enter to continue...")
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 1. Log Decision
    print_step(1, "AI Coding Agent Logs Security Policy via MCP")
    summary = "Zero Hardcoded Secrets allowed in source code."
    rationale = "Credentials must only load from environment variables (os.environ). Hardcoding secrets exposes keys during git pushes and causes security leaks."
    tags = "security, config"
    linked_symbols = [("settings.py", "file", "src/settings.py")]
    
    dec_id = database.log_decision(summary, rationale, tags, linked_symbols)
    print(f"{GREEN}✓ Security Policy #{dec_id} successfully logged & linked to settings.py!{RESET}")
    print(f"  - {BOLD}Summary:{RESET} {summary}")
    print(f"  - {BOLD}Rationale:{RESET} {rationale}\n")
    
    input("Press Enter to view active Knowledge Graph...")
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 2. View Graph v1
    print_step(2, "Visualizing Active Security Policy Map")
    print_ascii_graph_v1()
    print("\nAegisFlow records that `settings.py` is protected by Decision #1.\n")
    
    input("Press Enter to simulate a developer pushing code...")
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 3. Simulate Commit
    print_step(3, "Developer commits a temporary hardcoded secret key")
    print(f"{YELLOW}Simulating Git Commit Push...{RESET}")
    print(f"{BOLD}Commit Hash:{RESET} f3c1e2a")
    print(f"{BOLD}Message:{RESET} Temp patch for database staging tests")
    print(f"{BOLD}Diff Changes:{RESET}\n{CYAN}{MOCK_DIFF}{RESET}\n")
    
    # Log commit
    database.log_commit(
        "f3c1e2a",
        "Alice Smith",
        "Temp patch for database staging tests",
        MOCK_DIFF,
        [("settings.py", "file", "src/settings.py")]
    )
    
    input("Press Enter to execute AegisFlow Drift Check...")
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 4. Drift Check
    print_step(4, "AegisFlow parses git diff & evaluates policy compliance")
    conflicts = engine.detect_drift(MOCK_DIFF, "Temp patch for database staging tests")
    
    if conflicts:
        print(f"{RED}{BOLD}🚨 SECURITY CONFLICT DETECTED BY AEGISFLOW!{RESET}")
        for c in conflicts:
            print(f"\n  • {BOLD}File Governed:{RESET} {c['filepath']}")
            print(f"  • {BOLD}Policy Violated:{RESET} {c['decision_summary']}")
            print(f"  • {BOLD}AegisFlow Explanation:{RESET} {RED}{c['violation_reason']}{RESET}")
        print("")
    else:
        print(f"{GREEN}✓ No conflicts detected.{RESET}\n")
        
    input("Press Enter to visualize conflict graph...")
    clear_screen()
    print_header("AegisFlow: Security Guard Flow")
    
    # 5. View Graph v2
    print_step(5, "Conflict Graph indicating violation path")
    print_ascii_graph_v2()
    print(f"\n{GREEN}Demo completed successfully!{RESET}")
    print("AegisFlow caught the hardcoded secret at the pre-push stage, preventing a critical credential leak.\n")

def main_menu():
    database.init_db()
    while True:
        clear_screen()
        print_header("AegisFlow: Security Control Center")
        print("Choose a step to execute (perfect for interactive interviewer walkthroughs):")
        print(f"  {BOLD}1.{RESET} Run Full Demo Flow (Recommended)")
        print(f"  {BOLD}2.{RESET} Reset Database (Clear all nodes)")
        print(f"  {BOLD}3.{RESET} Log Security Policy (Secrets Constraint)")
        print(f"  {BOLD}4.{RESET} Visualize Knowledge Graph (Active)")
        print(f"  {BOLD}5.{RESET} Push Conflicting Commit (Hardcoded Key)")
        print(f"  {BOLD}6.{RESET} Run AegisFlow Drift Check")
        print(f"  {BOLD}7.{RESET} Visualize Knowledge Graph (Conflict)")
        print(f"  {BOLD}8.{RESET} Exit")
        
        choice = input(f"\n{BOLD}Select an option [1-8]: {RESET}")
        
        if choice == '1':
            run_auto_flow()
            input("Press Enter to return to main menu...")
        elif choice == '2':
            database.clear_db()
            print(f"\n{GREEN}Database cleared!{RESET}")
            input("\nPress Enter to continue...")
        elif choice == '3':
            database.log_decision(
                "Zero Hardcoded Secrets allowed in source code.",
                "Credentials must load from environment variables (os.environ) to prevent API key exposure.",
                "security, config",
                [("settings.py", "file", "src/settings.py")]
            )
            print(f"\n{GREEN}✓ Security policy logged and linked to settings.py!{RESET}")
            input("\nPress Enter to continue...")
        elif choice == '4':
            clear_screen()
            print_header("Active Security Map")
            print_ascii_graph_v1()
            input("\nPress Enter to continue...")
        elif choice == '5':
            database.log_commit(
                "f3c1e2a",
                "Alice Smith",
                "Temp patch for database staging tests",
                MOCK_DIFF,
                [("settings.py", "file", "src/settings.py")]
            )
            print(f"\n{GREEN}✓ Conflicting commit pushed to database!{RESET}")
            input("\nPress Enter to continue...")
        elif choice == '6':
            clear_screen()
            print_header("AegisFlow Drift Engine")
            conflicts = engine.detect_drift(MOCK_DIFF, "Temp patch for database staging tests")
            if conflicts:
                print(f"{RED}{BOLD}🚨 SECURITY POLICY CONFLICT DETECTED!{RESET}")
                for c in conflicts:
                    print(f"\n  • File: {c['filepath']}")
                    print(f"  • Policy Violated: {c['decision_summary']}")
                    print(f"  • Explanation: {RED}{c['violation_reason']}{RESET}")
            else:
                print(f"{GREEN}✓ No conflicts detected. Make sure you log the policy and commit changes first!{RESET}")
            input("\nPress Enter to continue...")
        elif choice == '7':
            clear_screen()
            print_header("Conflict Security Map")
            print_ascii_graph_v2()
            input("\nPress Enter to continue...")
        elif choice == '8':
            clear_screen()
            print("Exiting AegisFlow. Lead the way in DevSecOps!")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
