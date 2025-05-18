# Setting Up Groq API for Job Recommender System

This project now uses Groq's API for generating embeddings instead of Ollama. Follow these steps to configure your environment:

## Configuration

1. Create or update your `.env` file with the following variables:

```
# Groq API Configuration
GROQ_API_KEY=your-groq-api-key-here
GROQ_EMBEDDING_MODEL=llama3-embed-8b
GROQ_API_BASE=https://api.groq.com/v1
```

2. Replace `your-groq-api-key-here` with your actual Groq API key.

## Models

The default embedding model is set to `llama3-embed-8b`, but you can change it by setting the `GROQ_EMBEDDING_MODEL` environment variable to another supported Groq model.

## Testing

To test that your Groq configuration is working properly, run any of the test scripts that use embeddings:

```bash
python test_vector_search.py
```

If the Groq API is properly configured, you should see successful embeddings being generated.

## Troubleshooting

If you encounter errors like "GROQ_API_KEY environment variable is not set" or authentication issues, make sure:

1. Your .env file is in the root directory of the project
2. The API key is correctly set and valid
3. The environment variables are being loaded properly

For any API-specific errors, check the Groq API documentation for more information. 