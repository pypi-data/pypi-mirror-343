# LLM Auto Web Tester

An automated web testing tool powered by large language models (LLMs) that executes predefined test scenarios through Playwright.

## Overview

This project provides an automated solution for web UI testing using OpenAI's GPT models and the MCP (Model Context Protocol) server. The system can perform complex UI interactions and validate functionality based on natural language test definitions.

## Features

- Automated browser testing with LLM agent control
- Predefined test scenarios in natural language
- Screenshot and artifact capture
- Detailed test summaries and reports
- Support for various UI testing scenarios

## Prerequisites

- Python 3.9+
- An OpenAI API key
- A running MCP server instance

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/stefanini-applications/llm-auto-web-tester.git
   cd llm-auto-web-tester

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

1. Make sure the MCP server is running on `http://localhost:8931` - npx @playwright/mcp@latest --port 8931

2. Ensure the web application you want to test is running (default: `http://localhost:5263/new/home`)

3. Run the automated tests:
   ```bash
   python src/llm_auto_web_tester.py
   ```

## Test Definitions

Test scenarios are defined in `src/test_definitions.py` as lists of natural language instructions. You can add or modify test scenarios by editing this file.

Available test scenarios:
- Search Tests
- Create Translation Bot Tool Tests
- Bot Tool Tests
- Interpreter Bot Tool Tests
- Chat Tool Tests
- Request Tool Tests
- Image Tool Tests
- Image Chain Tests
- Image Bot Chain Tests

## File Structure

```
llm-auto-web-tester/
├── src/
│   ├── llm_auto_web_tester.py    # Main execution script
│   ├── test_definitions.py       # Test scenario definitions
│   └── artifacts/                # Directory for test outputs
├── .env                          # Environment variables (API keys)
└── README.md                     # This documentation
```

## Test Artifacts

Test artifacts are saved in the `src/artifacts/` directory, organized by date and test type. These include:
- Test result summaries
- Snapshots and screenshots
- Detailed test reports

## Customization

To create new test scenarios, add a new list in `test_definitions.py` with step-by-step instructions in natural language.

You can then update the `test_suites` dictionary in `llm_auto_web_tester.py` to include your new test suite.

## Troubleshooting

- If tests fail, check that the target application is running and accessible
- Verify your OpenAI API key is valid and has proper permissions
- Ensure the MCP server is running correctly on the specified port
- Check the console output for detailed error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.