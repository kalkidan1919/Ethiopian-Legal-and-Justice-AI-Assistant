# Developer Portfolio CLI Application

A lightweight Python Command Line Interface (CLI) application that displays a developer's profile from a local JSON file and enhances it with live GitHub repository statistics using the GitHub REST API.

---

## 🛠️ Features

- Object-oriented design using a `DeveloperPortfolio` class
- Loads developer information from `profile.json`
- Fetches live GitHub repository statistics
- Supports optional GitHub token authentication
- Handles common errors such as:
  - Missing profile file
  - Invalid JSON
  - API/network failures

---

## 📂 Project Structure

```text
dev-portfolio-cli/
├── app.py          # Main application
├── profile.json    # Developer profile
└── README.md       # Project documentation
```