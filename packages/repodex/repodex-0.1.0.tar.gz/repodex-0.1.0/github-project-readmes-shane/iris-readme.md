# IRIS - Integrated Research Intelligence System

A modern, responsive landing page for IRIS (Integrated Research Intelligence System), showcasing AI research, development, and services.

## Overview

IRIS is a collective of researchers, engineers, and visionaries dedicated to advancing AI for the benefit of humanity. This repository contains the landing page for the IRIS platform, built with React and modern web technologies.

## Mission & Vision

**Mission:** IRIS is committed to developing Adaptive Intelligence systems that learn, evolve, and adapt to solve the world's most pressing challenges. We believe that AI should augment human capabilities while respecting human values and autonomy.

**Vision:** We envision a future where adaptive intelligence seamlessly integrates into everyday life, empowering individuals and organizations to achieve their full potential while addressing global challenges like climate change, healthcare access, and educational equity.

## Core Values

- **Innovation:** Pioneering AI solutions that break new ground and redefine what's possible
- **Collaboration:** Building bridges between researchers, industries, and communities to solve complex problems
- **Excellence:** Pursuing uncompromising quality in our research, development, and implementation
- **Responsibility:** Ensuring our AI technologies are developed with ethical considerations at the forefront

## Services

- **AI Development:** Custom AI solutions designed to address specific business challenges and opportunities
- **Predictive Analytics:** Advanced data modeling that transforms raw information into actionable insights
- **Machine Learning:** Systems that learn and improve from experience without explicit programming
- **Research Consulting:** Expert guidance on implementing cutting-edge AI technologies in your organization
- **Cloud AI Infrastructure:** Scalable, secure cloud environments optimized for AI workloads and deployment
- **AI Research:** Pioneering fundamental research that pushes the boundaries of artificial intelligence

## Technologies Used

- **React 18** - Frontend library
- **Vite** - Build tool and development server
- **TailwindCSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **FontAwesome** - Icon library
- **React Scroll** - Smooth scrolling functionality
- **Netlify** - Deployment platform

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/shaneholloman/iris.git
   cd iris
   ```

2. Install dependencies:

   ```sh
   npm install
   # or
   yarn
   ```

3. Start the development server:

   ```sh
   npm run dev
   # or
   yarn dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```sh
npm run build
# or
yarn build
```

The built files will be in the `dist` directory.

## Project Structure

```sh
iris/
├── docs/                # Documentation
├── public/              # Public assets
├── src/
│   ├── assets/          # Images, fonts, etc.
│   ├── components/      # React components
│   ├── contexts/        # React contexts (e.g., ThemeContext)
│   ├── App.jsx          # Main application component
│   ├── main.jsx         # Application entry point
│   └── index.postcss    # Global styles
├── index.html           # HTML template
├── package.json         # Project dependencies and scripts
├── tailwind.config.js   # TailwindCSS configuration
└── vite.config.js       # Vite configuration
```

## Deployment

The site is configured for deployment on Netlify and includes a `netlify.toml` configuration file. It can also be deployed using the included Kubernetes configuration (`windsurf_deployment.yaml`).

## License

This project is proprietary and confidential. All rights reserved.
