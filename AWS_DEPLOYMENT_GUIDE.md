# 🚀 AWS Deployment Guide - Restaceratops AI Agent

## **Complete Free AWS Deployment (100% Free Tier)**

---

## 📋 **Prerequisites**

1. **AWS Account** - Free tier enabled
2. **AWS CLI** - Installed and configured
3. **Node.js** - For Serverless Framework
4. **Python 3.11** - For local development

---

## 🔧 **Step 1: Install AWS CLI & Configure**

### **1.1 Install AWS CLI**
```bash
# macOS
brew install awscli

# Or download from AWS website
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

### **1.2 Configure AWS CLI**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (us-east-1)
# Enter your output format (json)
```

---

## 🛠️ **Step 2: Install Serverless Framework**

```bash
# Install Serverless Framework globally
npm install -g serverless

# Verify installation
serverless --version
```

---

## 📦 **Step 3: Install Project Dependencies**

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (for local testing)
cd backend
pip install -r requirements.txt
cd ..
```

---

## 🔑 **Step 4: Set Environment Variables**

### **4.1 Create .env file**
```bash
# Create .env file in project root
cat > .env << EOF
OPENROUTER_API_KEY=your-openrouter-api-key
MONGODB_URI=your-mongodb-uri
MONGODB_DB_NAME=restaceratops
EOF
```

### **4.2 Set AWS Environment Variables**
```bash
# Set environment variables for AWS
export OPENROUTER_API_KEY="your-openrouter-api-key"
export MONGODB_URI="your-mongodb-uri"
export MONGODB_DB_NAME="restaceratops"
```

---

## 🚀 **Step 5: Deploy Backend to AWS Lambda**

### **5.1 Deploy to Development**
```bash
# Deploy to dev stage
serverless deploy --stage dev
```

### **5.2 Deploy to Production**
```bash
# Deploy to prod stage
serverless deploy --stage prod
```

### **5.3 Expected Output**
```
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
Serverless: Stack create finished...
Service Information
service: restaceratops-api
stage: dev
region: us-east-1
stack: restaceratops-api-dev
resources: 15
functions:
  api: restaceratops-api-dev-api
endpoints:
  ANY - https://abc123.execute-api.us-east-1.amazonaws.com/{proxy+}
```

---

## 🌐 **Step 6: Deploy Frontend to S3 + CloudFront**

### **6.1 Build Frontend**
```bash
cd frontend
npm install
npm run build
cd ..
```

### **6.2 Create S3 Bucket**
```bash
# Create S3 bucket for frontend
aws s3 mb s3://restaceratops-frontend-$(date +%s)

# Enable static website hosting
aws s3 website s3://restaceratops-frontend-$(date +%s) --index-document index.html --error-document index.html
```

### **6.3 Upload Frontend**
```bash
# Upload built files to S3
aws s3 sync frontend/dist/ s3://restaceratops-frontend-$(date +%s) --delete

# Make files public
aws s3api put-bucket-policy --bucket restaceratops-frontend-$(date +%s) --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::restaceratops-frontend-$(date +%s)/*"
    }
  ]
}'
```

---

## 🔗 **Step 7: Update Frontend API URL**

### **7.1 Update API Base URL**
```bash
# Edit frontend/src/services/api.ts
# Replace API_BASE_URL with your Lambda endpoint
const API_BASE_URL = 'https://abc123.execute-api.us-east-1.amazonaws.com';
```

### **7.2 Rebuild and Deploy**
```bash
cd frontend
npm run build
cd ..
aws s3 sync frontend/dist/ s3://restaceratops-frontend-$(date +%s) --delete
```

---

## ✅ **Step 8: Test Your Deployment**

### **8.1 Test Backend API**
```bash
# Test health endpoint
curl https://abc123.execute-api.us-east-1.amazonaws.com/health

# Test AI chat
curl -X POST https://abc123.execute-api.us-east-1.amazonaws.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI!"}'
```

### **8.2 Test Frontend**
- Visit your S3 website URL
- Test AI chat functionality
- Test file upload
- Test test execution

---

## 📊 **Step 9: Monitor Usage (Free Tier)**

### **9.1 Check Lambda Usage**
```bash
# View Lambda logs
serverless logs -f api

# Check Lambda metrics in AWS Console
# Go to Lambda > Functions > restaceratops-api-dev-api > Monitoring
```

### **9.2 Check DynamoDB Usage**
```bash
# Check DynamoDB tables
aws dynamodb list-tables

# Check table metrics in AWS Console
# Go to DynamoDB > Tables > restaceratops-*
```

### **9.3 Free Tier Limits**
- **Lambda**: 1M requests/month
- **API Gateway**: 1M requests/month
- **DynamoDB**: 25GB storage
- **S3**: 5GB storage
- **CloudFront**: 20K requests/month

---

## 🛠️ **Step 10: Useful Commands**

### **10.1 Deployment Commands**
```bash
# Deploy changes
serverless deploy

# Remove deployment
serverless remove

# View logs
serverless logs -f api

# Invoke function
serverless invoke -f api
```

### **10.2 AWS CLI Commands**
```bash
# List Lambda functions
aws lambda list-functions

# List DynamoDB tables
aws dynamodb list-tables

# List S3 buckets
aws s3 ls
```

---

## 🆘 **Troubleshooting**

### **Common Issues:**

#### **1. Lambda Timeout**
```bash
# Increase timeout in serverless.yml
timeout: 60  # Increase from 30 to 60 seconds
```

#### **2. Memory Issues**
```bash
# Increase memory in serverless.yml
memorySize: 1024  # Increase from 512 to 1024 MB
```

#### **3. CORS Issues**
```bash
# Add CORS headers in lambda_handler.py
# Already configured in the handler
```

#### **4. Environment Variables**
```bash
# Check environment variables
serverless print

# Set environment variables
serverless config credentials --provider aws --key YOUR_KEY --secret YOUR_SECRET
```

---

## 💰 **Cost Monitoring**

### **Free Tier Usage:**
- **Lambda**: Monitor in AWS Console > Lambda > Functions
- **API Gateway**: Monitor in AWS Console > API Gateway
- **DynamoDB**: Monitor in AWS Console > DynamoDB > Tables
- **S3**: Monitor in AWS Console > S3 > Buckets

### **Cost Alerts:**
1. Go to AWS Console > Billing
2. Set up billing alerts
3. Set threshold to $1.00
4. Get notified before exceeding free tier

---

## 🎉 **Success!**

Your AI agent is now deployed on AWS for **100% FREE**!

- **Backend**: AWS Lambda + API Gateway
- **Frontend**: S3 + CloudFront
- **Database**: DynamoDB
- **Cost**: $0 (within free tier limits)

**Your AI agent is live and ready to use!** 🚀 