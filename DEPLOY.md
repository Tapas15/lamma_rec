# Deploying the Job Recommender System on Render.com

This guide explains how to deploy the Job Recommender System on Render.com.

## Prerequisites

1. A [Render.com](https://render.com/) account
2. A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) database or other MongoDB provider
3. A [Groq API](https://console.groq.com/) key for embeddings generation

## Automatic Deployment

The repository includes a `render.yaml` file for easy deployment:

1. **Connect your GitHub repository to Render**:
   - Go to your Render dashboard
   - Click "New" > "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing this project

2. **Configure the environment variables**:
   - When prompted, enter your `MONGODB_URI` connection string
   - Enter your `GROQ_API_KEY`
   - Other variables are pre-configured in the `render.yaml` file

3. **Deploy the service**:
   - Click "Apply" to start the deployment
   - Render will automatically build and deploy your service

## Manual Deployment Steps

If you prefer manual deployment:

1. **Create a new Web Service in Render**:
   - Go to your Render dashboard
   - Click "New" > "Web Service"
   - Connect your repository

2. **Configure the service**:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Add environment variables**:
   - `GROQ_API_KEY`: Your Groq API key
   - `GROQ_EMBEDDING_MODEL`: `llama3-embed-8b`
   - `GROQ_API_BASE`: `https://api.groq.com/v1`
   - `MONGODB_URI`: Your MongoDB connection string
   - `DB_NAME`: `job_recommendation`
   - `SECRET_KEY`: Generate a secure random string
   - `PYTHON_VERSION`: `3.10.0`

4. **Deploy**:
   - Click "Create Web Service"

## Verifying Deployment

1. Once deployed, visit the service URL provided by Render
2. Add `/docs` to the URL to view the FastAPI documentation
3. Test the API endpoints using the interactive documentation

## MongoDB Configuration

Ensure your MongoDB database is:
1. Accessible from Render.com (whitelisted IP or allow from anywhere)
2. Has the necessary collections created
3. The connection string includes database credentials

## Troubleshooting

- Check the Render logs if the service fails to start
- Verify all environment variables are set correctly
- Ensure your MongoDB connection string is correct and accessible
- If embeddings fail, check that your Groq API key is valid 