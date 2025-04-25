# vuln-checker

[![PyPI version](https://img.shields.io/pypi/v/vuln-checker?color=brightgreen)](https://pypi.org/project/vuln-checker/)
[![Python version](https://img.shields.io/pypi/pyversions/vuln-checker)](https://pypi.org/project/vuln-checker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/skm248/vuln-checker?style=social)](https://github.com/skm248/vuln-checker/stargazers)

> ✨ A CLI tool to search CVEs from the NVD API based on product/version (CPE lookup).

---

## Features

- 🎯 Interactive mode to resolve multiple CPE matches
- 🔍 Filter CVEs by severity (LOW, MEDIUM, HIGH, CRITICAL)
- 💾 Export results in JSON, CSV, or HTML formats
- 🌐 Includes hyperlinks for CVE IDs in JSON, CSV, and HTML outputs
- 📋 Batch processing with CSV input or command-line product/version pairs
- ⚡ Requires NVD API key for enhanced access (rate limits apply)
- 🚀 Supports pagination for comprehensive CVE retrieval

---

## Installation

Install via pip:

```bash
pip install vuln-checker
```

Or from GitHub:

```bash
git clone https://github.com/skm248/vuln-checker.git
cd vuln-checker
pip install .
```
Usage
Prerequisites
•	Obtain an NVD API key from https://nvd.nist.gov/developers/request-an-api-key and set it as an environment variable NVD_API_KEY or replace the placeholder in the script. Follow these steps to request a key: 
1.	Open your preferred web browser and navigate to https://nvd.nist.gov/developers/request-an-api-key
2.	On the NVD - Request an API Key page, complete the following fields: 
•	Organization Name: Enter the name of your organization.
•	Email Address: Provide a valid business email address.
•	Organization Type: Select the type that best represents your organization from the dropdown menu.
3.	Carefully read and understand the NVD - Terms of Use section.
4.	Scroll to the bottom of the Terms of Use and check the "I agree to the Terms of Use" checkbox to accept the agreement.
5.	Click the submit button to send your request.
6.	Check your email (including spam/junk folders) for a message from NVD containing a single-use activation hyperlink. This email is sent to the address provided.
7.	Click the hyperlink within seven days to activate and view your API key. If not activated within this period, you must submit a new request.

- Set the `NVD_API_KEY` environment variable using one of the following methods based on your operating system:

  #### Windows (Command Prompt)
  - **Temporary (Current Session)**:
    1. Open Command Prompt.
    2. Run the following command, replacing `your_actual_api_key` with your NVD API key:
       ```cmd
       set NVD_API_KEY=your_actual_api_key
•	Note: The variable is unset when the Command Prompt window is closed.

Persistent (All Future Sessions):
1.	Open "System Properties":
•	Right-click 'This PC' → 'Properties' → 'Advanced system settings' → 'Environment Variables'.
•	In the "User variables" or "System variables" section, click "New" or edit an existing NVD_API_KEY variable.
•	Set the Variable name to NVD_API_KEY and the Variable value to your_actual_api_key.
•	Click "OK" to save, then close all dialog boxes.
•	Open a new Command Prompt and verify with echo %NVD_API_KEY%.
•	Run the script in the new session.

Windows (PowerShell)
•	Temporary (Current Session):
1. Open PowerShell.
2. Run the following command, replacing your_actual_api_key with your NVD API key:
      $env:NVD_API_KEY = "your_actual_api_key"
3. Run the script in the same PowerShell session:
      python main.py --products "tomcat:9.0.46" --format json
•	Note: The variable is unset when the PowerShell session is closed.

Persistent (All Future Sessions):
1. Open PowerShell with administrative privileges.
2. Run the following command, replacing your_actual_api_key with your NVD API key:
      [Environment]::SetEnvironmentVariable("NVD_API_KEY", "your_actual_api_key", "User")
•	Use "Machine" instead of "User" for system-wide persistence (requires admin rights).
3. Open a new PowerShell session and verify with $env:NVD_API_KEY.
4. Run the script in the new session.

Linux/macOS (Terminal)
•	Temporary (Current Session):
1. Open a terminal.
2. Run the following command, replacing your_actual_api_key with your NVD API key:
```bash
export NVD_API_KEY=your_actual_api_key
```
3. Run the script in the same terminal session:
```bash
python main.py --products "tomcat:9.0.46" --format json
```
•	Note: The variable is unset when the terminal session is closed.

Persistent (All Future Sessions):
1. Open a terminal and edit your shell configuration file:
•	For Bash: nano ~/.bashrc or nano ~/.bash_profile
•	For Zsh: nano ~/.zshrc
2. Add the following line at the end, replacing your_actual_api_key with your NVD API key:
```bash
export NVD_API_KEY=your_actual_api_key
```
3. Save the file and exit (e.g., Ctrl+O, Enter, Ctrl+X in nano).
4. Apply the changes by running:
```bash
source ~/.bashrc  # or source ~/.bash_profile or source ~/.zshrc
```
5. Verify with echo $NVD_API_KEY.
6. Run the script in the same or a new terminal session.
•	After setting the environment variable, run the script. If the key is not detected, the script will prompt for manual input.


Command-Line Options
```bash
vuln-checker –help
```
Examples
1.	Single Product via Command-Line:
```bash
vuln-checker --products "tomcat:9.0.46,mysql:8.0.35" --format html --output report.html
```
•	Fetches CVEs for multiple products/versions provided as a comma-separated list.

2.	Batch Processing with CSV: 
•	Create a products.csv file with the following format:
      product,version
      tomcat,9.0.46
      mysql,8.0.35
      jquery,1.11.3
•	Run:
```bash
vuln-checker --input-csv products.csv --format csv --output output.csv
```
•	Processes all product/version pairs from the CSV.

3.	Filter by Severity: 
```bash
vuln-checker --products "tomcat:9.0.46" --severity HIGH --format json --output output.json
```
•	Filters CVEs with HIGH severity only.

4.	Specify Output File: 
```bash
vuln-checker --input-csv products.csv --format html --output custom_report.html
```
•	Saves the report to a custom file name.

Arguments
•	--input-csv PATH: Path to a CSV file with product and version columns (mutually exclusive with --products).
•	--products LIST: Comma-separated list of product:version pairs (e.g., tomcat:9.0.46,mysql:8.0.35) (mutually exclusive with --input-csv).
•	--severity TEXT: Filter CVEs by severity (LOW, MEDIUM, HIGH, CRITICAL).
•	--format TEXT: Output format (json, csv, html; default: json).
•	--output PATH: Output file name (default: output.json, output.csv, or report.html based on format).

Notes
•	Exactly one of --input-csv or --products must be provided.
•	Hyperlinks in CSV are formatted as Excel =HYPERLINK formulas, and in JSON as a dictionary with url and value fields.
•	The tool includes a 0.5-second delay between API requests to respect NVD rate limits.
__________________________________________________________________________________________________________________________

5.	License
This project is licensed under the by Sai Krishna Meda.

### Changes Made
1. **Features Section**:
   - Added support for hyperlinks in JSON, CSV, and HTML outputs.
   - Included batch processing with CSV or command-line input.
   - Noted the requirement for an NVD API key and pagination support.
   - Removed the caching feature mention since it’s not implemented in the current code.

2. **Usage Section**:
   - Updated to reflect the mutual exclusivity of `--input-csv` and `--products`.
   - Provided detailed examples for both CSV and command-line inputs.
   - Added a Prerequisites subsection to emphasize the NVD API key requirement.
   - Included a Notes subsection to explain hyperlink formatting and rate limit handling.
   - Updated argument descriptions to match the current functionality.

3. **Command Examples**:
   - Replaced `--product` and `--version` with `--products` (comma-separated pairs) to align with the updated `main.py`.
   - Added examples for CSV input, severity filtering, and custom output files.

### Testing Instructions
1. **Verify Readme**: Ensure the updated `README.md` accurately reflects the tool’s capabilities by comparing it with `main.py` and `template.html`.
2. **Test Commands**: Run the example commands with your NVD API key set (e.g., `export NVD_API_KEY=your_key` or replace in code) and verify the outputs.
3. **Check Hyperlinks**: Confirm hyperlinks in JSON, CSV, and HTML as described.
4. **Update Documentation**: If additional features (e.g., caching) are added later, update the README accordingly.

### Notes
- The `README.md` assumes the tool is packaged as `vuln-checker` on PyPI. If it’s not yet published, adjust the installation instructions or remove the PyPI badges.
- The NVD API key is suggested as an environment variable for security, but the current code uses a hardcoded placeholder. Consider updating `main.py` to read from `os.environ.get("NVD_API_KEY")` for production use.