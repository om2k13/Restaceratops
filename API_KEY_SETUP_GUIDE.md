# 🔑 OpenRouter API Key Setup Guide

## Issue Identified
The current API key is returning "User not found" errors, which means:
- The account has been deleted or suspended
- The API key has expired
- The account has no remaining credits

## How to Fix

### Step 1: Get a New API Key
1. Visit [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up for a free account (if you don't have one)
3. Create a new API key
4. Copy the key (starts with `sk-or-`)

### Step 2: Update Environment
1. Open the `.env` file in your project root
2. Replace the existing API key with your new one:
   ```
   OPENROUTER_API_KEY=your-new-api-key-here
   ```

### Step 3: Test the System
1. Restart the backend server
2. Test the AI chat functionality
3. Verify that real AI responses are working

## Free Tier Information
- OpenRouter offers free credits for new users
- Qwen models are available on the free tier
- No credit card required for basic usage

## Fallback System
Even without a valid API key, the system will:
- ✅ Continue working with intelligent fallback responses
- ✅ Provide helpful API testing guidance
- ✅ Maintain all core functionality
- ✅ Only lose real AI model responses

## Support
If you need help:
- OpenRouter Documentation: https://openrouter.ai/docs
- Restaceratops Issues: Create an issue in the repository
