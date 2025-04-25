# ORACLE - IT and DevOps Documentation

A comprehensive knowledge base and documentation site for IT and DevOps topics, built with MkDocs and the Material theme.

## Overview

ORACLE is a personal documentation repository that serves as a centralized knowledge base for various IT and DevOps topics. While it's not actively maintained at the moment, there are plans to update it with new content and improvements in the future.

## Features

- **Comprehensive Documentation**: Covers a wide range of IT and DevOps topics
- **Well-Structured**: Organized into logical sections for easy navigation
- **Searchable**: Full-text search functionality
- **Mobile-Friendly**: Responsive design that works on all devices
- **Dark/Light Mode**: Supports both dark and light themes
- **Code Highlighting**: Syntax highlighting for code snippets

## Topics Covered

- Linux administration
- Windows management
- VMware virtualization
- AI and machine learning
- MkDocs documentation
- Lab environments
- And more...

## Technology Stack

- **MkDocs**: Documentation site generator
- **Material for MkDocs**: Modern and responsive theme
- **Python**: Backend language for MkDocs and plugins
- **Markdown**: Content formatting
- **GitHub**: Version control and hosting
- **Various MkDocs Plugins**: For enhanced functionality

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/shaneholloman/oracle.git
   cd oracle
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Start the development server:

   ```sh
   mkdocs serve
   ```

4. Open your browser and navigate to `http://localhost:8000`

### Building the Documentation

```sh
mkdocs build
```

The built site will be in the `site` directory.

## Project Structure

```sh
oracle/
├── docs/                # Documentation source files
│   ├── index.md         # Home page
│   ├── linux/           # Linux documentation
│   ├── windows/         # Windows documentation
│   ├── vmware/          # VMware documentation
│   ├── ai/              # AI documentation
│   └── mkdocs/          # MkDocs documentation
├── archive/             # Archived content
├── mkdocs.yml           # MkDocs configuration
└── requirements.txt     # Python dependencies
```

## Future Plans

While this repository isn't actively maintained at the moment, there are plans to:

- Update existing documentation with current best practices
- Add new sections on emerging technologies
- Improve the organization and structure
- Enhance the visual design and user experience

## License

This project is proprietary and confidential. All rights reserved.
