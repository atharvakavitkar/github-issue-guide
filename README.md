# GitHub Issue Guide

This project provides step-by-step AI-powered guidance for solving GitHub issues.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches GitHub issue details using the GitHub API
- Generates step-by-step guidance for solving issues using Google's Generative AI (Gemini 1.5Flash)
- Provides clear instructions for new and eager to contribute GitHub users

## Prerequisites

- Node.js
- npm or yarn
- Google API key for Generative AI

## Installation

1. Clone the repository:
   git clone https://github.com/your-username/github-issue-guidance-api.git
   cd github-issue-guidance-api

2. Install dependencies:
   `npm install` or `yarn install`

3. Set up environment variables (see [Environment Variables](#environment-variables) section)

## Usage

Start the server:
`npm start` or `yarn start`

The server will run on `http://localhost:3001` by default.

## API Endpoints

### POST /api/guidance

Generates guidance for solving a GitHub issue.

**Request Body:**
{
  "issueUrl": "https://github.com/owner/repo/issues/123"
}

**Response:**
{
  "guidance": "Step-by-step instructions for solving the issue..."
}

## Environment Variables

Create a `.env` file in the root directory with the following variables:

GOOGLE_API_KEY=your_google_api_key_here
PORT=3001 (optional, defaults to 3001)

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
