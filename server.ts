import express from 'express';
import axios from 'axios';
import dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';

dotenv.config();

const app = express();
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);

app.post('/api/guidance', async (req, res) => {
  try {
    const { issueUrl } = req.body;
    
    // Extract owner, repo, and issue number from the URL
    const match = issueUrl.match(/github\.com\/(.+)\/(.+)\/issues\/(\d+)/);
    if (!match) {
      return res.status(400).json({ error: 'Invalid GitHub issue URL' });
    }
    
    const [, owner, repo, issueNumber] = match;
    
    // Fetch issue details from GitHub API
    const response = await axios.get(`https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}`);
    const issueData = response.data;
    
    // Generate guidance using Gemini Pro
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const prompt = `As an expert GitHub guide, provide step-by-step guidance for a novice GitHub user on how to solve the following issue:

Title: ${issueData.title}
Description: ${issueData.body}

Include detailed information on:
1. Setting up the development environment
2. Forking the repository
3. Creating a new branch
4. Making the necessary changes
5. Committing and pushing the changes
6. Creating a pull request

Provide clear, concise steps that a beginner can easily follow.`;

    const result = await model.generateContent(prompt);
    const guidance = result.response.text();
    
    res.json({ guidance });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'An error occurred while generating guidance' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});