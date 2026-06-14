import database
import re

def parse_modified_symbols_from_diff(diff_content):
    """
    Parses a unified diff string and identifies modified files.
    Focuses on modified file basenames as symbols for simplicity.
    """
    modified_files = set()
    lines = diff_content.splitlines()
    for line in lines:
        if line.startswith("+++ b/"):
            filepath = line[6:]
            # Use filename as symbol name
            filename = filepath.split("/")[-1]
            modified_files.add((filename, "file", filepath))
    return list(modified_files)

def detect_drift(diff_content, commit_message=""):
    """
    Compares the changes in a git diff against security decisions linked to modified files.
    Returns a list of detected conflicts.
    """
    modified_symbols = parse_modified_symbols_from_diff(diff_content)
    conflicts = []
    
    conn = database.get_connection()
    cursor = conn.cursor()
    
    for symbol_name, symbol_type, filepath in modified_symbols:
        # Get symbol ID
        cursor.execute("SELECT id FROM code_symbols WHERE name = ?", (symbol_name,))
        row = cursor.fetchone()
        if not row:
            continue
        symbol_id = row[0]
        
        # Get decisions linked to this symbol
        cursor.execute("""
            SELECT d.id, d.summary, d.rationale, d.tags 
            FROM decisions d
            JOIN decision_symbol_links dsl ON d.id = dsl.decision_id
            WHERE dsl.symbol_id = ?
        """, (symbol_id,))
        
        decisions = cursor.fetchall()
        
        for dec_id, summary, rationale, tags in decisions:
            conflict_found = False
            reason = ""
            
            # Scenario: Security Secret Leakage Check
            if "secret" in summary.lower() or "key" in summary.lower() or "security" in tags.lower():
                # Read the lines added in the diff (starting with "+")
                added_lines = [line[1:] for line in diff_content.splitlines() if line.startswith("+") and not line.startswith("+++")]
                
                for line in added_lines:
                    # Look for variable assignments containing keys/secrets
                    # E.g., JWT_SECRET = "some_secret", API_KEY = 'secret', etc.
                    match = re.search(r'(jwt_secret|api_key|token|password|auth_key)\s*=\s*[\'"]([^\'"]+)[\'"]', line, re.IGNORECASE)
                    if match:
                        variable_name = match.group(1)
                        value = match.group(2)
                        
                        # If the value is a plain hardcoded key and not an environment loader like os.environ
                        if not ("os.environ" in line or "os.getenv" in line or "config" in line):
                            conflict_found = True
                            reason = (f"The code introduces a hardcoded private key/token assigned to `{variable_name}` "
                                      f"(Value: `'{value[:5]}...'`). This violates the active security rule: "
                                      f"'{summary}'. All secrets must load from environment variables.")
                            break
                            
            if conflict_found:
                conflicts.append({
                    "symbol_name": symbol_name,
                    "filepath": filepath,
                    "decision_id": dec_id,
                    "decision_summary": summary,
                    "violation_reason": reason
                })
                
    conn.close()
    return conflicts
