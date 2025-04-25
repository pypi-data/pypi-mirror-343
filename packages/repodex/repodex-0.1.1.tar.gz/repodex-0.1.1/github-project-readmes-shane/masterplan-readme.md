# MasterPlan

A comprehensive system for managing personal and professional digital assets through AI-powered knowledge management.

Note this project using react and vite, so you need to run thru some installation steps to get it up and running. We use react to show some graphs and interactive components, and vite to speed up the development process.

## Installation

1. Install [Volta](https://volta.sh/) for Node.js version management:

    ```sh
    # Windows (PowerShell, run as Administrator)
    iwr https://get.volta.sh | iex
    ```

2. Clone and enter the repository:

    ```sh
    cd masterplan
    ```

3. Install dependencies:

    ```sh
    npm install
    ```

4. Start the development server:

    ```sh
    npm run dev
    ```

5. Open <http://localhost:5173> in your browser to see the vector space visualizations:
   - Cosine Similarity with interactive angle controls
   - Points to Vectors demonstration
   - Word Vectors relationships

## Overview

MasterPlan is an ambitious project focused on creating a unified system for managing:

- Data and files across multiple storage locations
- Code repositories and their derivatives
- Knowledge bases and graphs
- AI integrations and prompt libraries
- Project management and documentation

The ultimate goal is to create a seamless, AI-queryable system that can maintain and organize all digital assets effectively.

## Core Components

### OmniBase

The central interface that provides oversight for all system components, including:

- HealthBridge (deployed via MCP to Claude Desktop)
- FamilyBridge (Ancestry and Family Tree management)
- FoodBridge (Grocery Receipt processing)
- WebBridge (Bookmark management)

### Knowledge Management

- Knowledge Graph (KG) for high-level information
- Knowledge Base (KB) in SQLite for detailed information
- Integration with AI systems for querying and maintenance

### Code Management

- CodeMapper (PyPi deployed tool)
- Repository summaries and embeddings
- Code forks management
- Source code documentation

### Data Processing

- Image processing capabilities
- Audio processing capabilities
- File organization schemes across drives/NAS/Dropbox

## Current Focus

The primary focus is on developing a system where AI can effectively:

1. Insert/append to JSONL files in the Knowledge Graph
2. Maintain consistency between KG and KB data
3. Process and organize various data types
4. Query and retrieve information across all system components

## Technical Goals

- Implement efficient JSONL handling for Knowledge Graph updates
- Create unified schemas between KG and KB
- Develop AI-friendly interfaces for system interaction
- Integrate personal and professional project management
- Establish standardized file organization schemes

## Status

This project is actively under development with various components at different stages of completion. See the masterplan.md file for detailed progress tracking and future objectives.
