# SecurePassLib 🔒

A professional Python library for secure password management:  
✅ Password validation  
✅ Password strength analysis  
✅ Breach checking (HaveIBeenPwned API)  
✅ Secure password generation  
✅ CLI tool support  

Built with security standards and flexibility in mind.

---

## ✨ Features

- **Password Validation**
  - Customizable password policies (min length, digits, specials, etc.)
  - Predefined validation errors for easy integration.

- **Password Strength Analysis**
  - Entropy calculation (bits) based on character pool size.
  - Text-based strength scoring (Very Weak → Very Strong).
  - Smart password improvement suggestions.

- **Password Generation**
  - Random secure password generator.
  - Template-based password generation (customizable patterns like `LL-DD-SS`).
  - Word-based, human-friendly password formats.

- **Password Breach Checking**
  - Safe checking using k-Anonymity model against HaveIBeenPwned API.
  - No full password is ever sent to external servers.

- **CLI Tools**
  - Generate, validate, analyze, breach-check passwords directly from terminal.

---

## 📦 Installation

```bash
pip install securepasslib



