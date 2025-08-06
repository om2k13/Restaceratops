#!/usr/bin/env python3
"""
🦖 Enhanced AI System for Restaceratops
Uses OpenRouter with Qwen3 30B A3B model for intelligent API testing assistance
"""

import os
import json
import logging
import asyncio
from typing import List, Dict, Optional, Any
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("agent.enhanced_ai_system")

class OpenRouterAI:
    """OpenRouter AI provider using Qwen3 30B A3B model."""
    
    def __init__(self):
        """Initialize OpenRouter AI with Qwen3 30B A3B model."""
        # Get API key from environment
        self.api_key = os.getenv("OPENROUTER_API_KEY", "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")
        # Use Qwen3 30B A3B model - free tier
        self.model = "qwen/qwen3-30b-a3b:free"
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        if self.api_key:
            log.info(f"✅ OpenRouter AI configured with {self.model}")
            log.info(f"🔑 API key configured: {self.api_key[:10]}...{self.api_key[-4:]}")
        else:
            log.warning("⚠️ No OpenRouter API key found")
            log.warning("🔧 Set OPENROUTER_API_KEY environment variable to enable real AI")
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Generate response using OpenRouter API with Qwen3 30B A3B model."""
        if not self.api_key:
            log.warning("⚠️ No OpenRouter API key provided")
            return None
        
        try:
            log.info(f"🤖 Using OpenRouter API with model: {self.model}")
            log.info(f"📝 Sending {len(messages)} messages to OpenRouter")
            
            # Use the new OpenAI SDK approach
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://restaceratops.onrender.com",
                    "X-Title": "Restaceratops API Testing Platform",
                },
                extra_body={},
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = completion.choices[0].message.content
            log.info(f"✅ OpenRouter response generated successfully with {self.model}")
            return ai_response
                    
        except Exception as e:
            log.error(f"❌ Failed to call OpenRouter API with {self.model}: {e}")
            return None

class EnhancedAISystem:
    """Enhanced AI system for API testing assistance."""
    
    def __init__(self):
        """Initialize the enhanced AI system."""
        self.openrouter_ai = OpenRouterAI()
        self.conversation_history = []
        log.info("Enhanced AI system initialized with OpenRouter Qwen3 30B A3B")
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation with intelligent responses."""
        try:
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Try to get response from OpenRouter AI
            if self.openrouter_ai.api_key:
                response = await self.openrouter_ai.generate_response(self.conversation_history)
                if response:
                    # Add AI response to conversation history
                    self.conversation_history.append({"role": "assistant", "content": response})
                    return response
            
            # Fallback to intelligent responses if AI fails
            return self._get_intelligent_fallback_response(user_input)
            
        except Exception as e:
            log.error(f"Error in conversation handling: {e}")
            return self._get_intelligent_fallback_response(user_input)
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases using AI."""
        try:
            prompt = f"""
            Generate comprehensive API test cases for the following API specification:
            
            API Specification:
            {api_spec}
            
            Requirements:
            {requirements}
            
            Please provide:
            1. Test cases for all endpoints
            2. Positive and negative test scenarios
            3. Authentication tests
            4. Error handling tests
            5. Performance considerations
            
            Format the response as YAML test specifications.
            """
            
            messages = [
                {"role": "system", "content": "You are an expert API testing specialist. Generate comprehensive test cases in YAML format."},
                {"role": "user", "content": prompt}
            ]
            
            if self.openrouter_ai.api_key:
                response = await self.openrouter_ai.generate_response(messages)
                if response:
                    return response
            
            return self._get_fallback_test_template(api_spec)
            
        except Exception as e:
            log.error(f"Error generating intelligent tests: {e}")
            return self._get_fallback_test_template(api_spec)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "OpenRouter",
            "model": self.openrouter_ai.model,
            "api_key_configured": bool(self.openrouter_ai.api_key),
            "conversation_history_length": len(self.conversation_history)
        }
    
    def _get_greeting_response(self) -> str:
        """Get a greeting response."""
        return """🦖 Hello! I'm Restaceratops, your AI-powered API testing assistant.

I can help you with:
✅ API testing strategies and best practices
✅ Test case generation and optimization
✅ Performance testing and monitoring
✅ Security testing recommendations
✅ Debugging and troubleshooting
✅ Test automation and CI/CD integration

What would you like to work on today?"""
    
    def _get_intelligent_fallback_response(self, user_input: str) -> str:
        """Get intelligent fallback response based on user input."""
        user_input_lower = user_input.lower()
        
        # Greeting detection
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            return self._get_greeting_response()
        
        # Authentication related
        if any(word in user_input_lower for word in ["auth", "authentication", "login", "token", "bearer", "api key"]):
            return self._get_authentication_guidance(user_input)
        
        # API testing related
        if any(word in user_input_lower for word in ["test", "testing", "api", "endpoint", "request", "response"]):
            return self._get_api_testing_guidance(user_input)
        
        # Debugging related
        if any(word in user_input_lower for word in ["debug", "error", "fail", "issue", "problem", "fix"]):
            return self._get_debugging_guidance(user_input)
        
        # Performance related
        if any(word in user_input_lower for word in ["performance", "speed", "slow", "timeout", "load"]):
            return self._get_performance_guidance(user_input)
        
        # Security related
        if any(word in user_input_lower for word in ["security", "secure", "vulnerability", "attack", "penetration"]):
            return self._get_security_guidance(user_input)
        
        # Test generation related
        if any(word in user_input_lower for word in ["generate", "create", "write", "make", "build"]):
            return self._get_test_generation_guidance(user_input)
        
        # Results analysis
        if any(word in user_input_lower for word in ["result", "report", "analysis", "summary", "statistics"]):
            return self._get_analyze_test_results(user_input)
        
        # General API guidance
        return self._get_general_api_guidance(user_input)
    
    def _get_authentication_guidance(self, user_input: str) -> str:
        """Provide authentication testing guidance."""
        return """🔐 **Authentication Testing Best Practices**

Based on your question about authentication, here are key testing strategies:

**1. Token-Based Authentication**
```yaml
- name: "Test Valid Bearer Token"
  request:
    method: GET
    url: "/api/protected"
    headers:
      Authorization: "Bearer {valid_token}"
  expect:
    status: 200

- name: "Test Invalid Token"
  request:
    method: GET
    url: "/api/protected"
    headers:
      Authorization: "Bearer invalid_token"
  expect:
    status: 401
```

**2. API Key Authentication**
```yaml
- name: "Test Valid API Key"
  request:
    method: GET
    url: "/api/data"
    headers:
      X-API-Key: "{valid_api_key}"
  expect:
    status: 200

- name: "Test Missing API Key"
  request:
    method: GET
    url: "/api/data"
  expect:
    status: 401
```

**3. OAuth2 Testing**
- Test authorization code flow
- Test refresh token rotation
- Test token expiration
- Test scope validation

**4. Security Considerations**
- Test for token leakage in logs
- Verify HTTPS enforcement
- Test rate limiting on auth endpoints
- Validate token format and strength

Need help implementing specific authentication tests?"""
    
    def _get_api_testing_guidance(self, user_input: str) -> str:
        """Provide API testing guidance."""
        return """🧪 **Comprehensive API Testing Strategy**

Here's a complete approach to API testing:

**1. Functional Testing**
```yaml
- name: "GET Resource"
  request:
    method: GET
    url: "/api/resources/123"
  expect:
    status: 200
    json:
      id: 123
      name: "string"

- name: "POST Create Resource"
  request:
    method: POST
    url: "/api/resources"
    json:
      name: "New Resource"
      description: "Test resource"
  expect:
    status: 201
    json:
      id: "number"
      name: "New Resource"
```

**2. Data Validation Testing**
- Test with valid data
- Test with invalid data types
- Test with missing required fields
- Test with boundary values
- Test with special characters

**3. Error Handling Testing**
```yaml
- name: "Test 400 Bad Request"
  request:
    method: POST
    url: "/api/resources"
    json: {}
  expect:
    status: 400

- name: "Test 404 Not Found"
  request:
    method: GET
    url: "/api/resources/999999"
  expect:
    status: 404
```

**4. Performance Testing**
- Response time under normal load
- Response time under high load
- Concurrent request handling
- Memory usage monitoring

**5. Security Testing**
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting

**6. Integration Testing**
- End-to-end workflows
- Data consistency
- State management
- Error propagation

Would you like me to help you create specific test cases for your API?"""
    
    def _get_debugging_guidance(self, user_input: str) -> str:
        """Provide debugging guidance."""
        return """🔍 **API Debugging Best Practices**

Here's a systematic approach to debugging API issues:

**1. Request/Response Analysis**
```bash
# Use curl with verbose output
curl -v -X POST https://api.example.com/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Check response headers
curl -I https://api.example.com/endpoint
```

**2. Common Issues & Solutions**

**Status Code 400 (Bad Request)**
- Check request body format
- Validate required fields
- Verify content-type header
- Check data types

**Status Code 401 (Unauthorized)**
- Verify authentication token
- Check token expiration
- Validate API key format
- Test with valid credentials

**Status Code 403 (Forbidden)**
- Check user permissions
- Verify resource ownership
- Test with different user roles
- Check rate limiting

**Status Code 404 (Not Found)**
- Verify endpoint URL
- Check resource ID existence
- Test with valid IDs
- Check API version

**Status Code 500 (Internal Server Error)**
- Check server logs
- Verify database connectivity
- Test with minimal payload
- Check external service dependencies

**3. Debugging Tools**
- **Postman/Insomnia**: GUI testing
- **curl**: Command line testing
- **Browser DevTools**: Network analysis
- **Logs**: Server and application logs
- **Monitoring**: APM tools

**4. Test Case for Debugging**
```yaml
- name: "Debug Request"
  request:
    method: POST
    url: "/api/debug"
    headers:
      Content-Type: "application/json"
      X-Debug: "true"
    json:
      test_data: "value"
  expect:
    status: 200
    json:
      debug_info: "string"
      request_id: "string"
```

**5. Logging Best Practices**
- Log request/response details
- Include correlation IDs
- Log performance metrics
- Capture error context

What specific issue are you debugging? I can help create targeted test cases."""
    
    def _get_performance_guidance(self, user_input: str) -> str:
        """Provide performance testing guidance."""
        return """⚡ **API Performance Testing Guide**

Here's how to test and optimize API performance:

**1. Response Time Testing**
```yaml
- name: "Performance Test - Response Time"
  request:
    method: GET
    url: "/api/data"
  expect:
    status: 200
    response_time: "< 1000ms"  # Custom assertion
```

**2. Load Testing Scenarios**
- **Baseline**: Normal user load
- **Peak**: Maximum expected load
- **Stress**: Beyond capacity
- **Spike**: Sudden traffic increase

**3. Performance Metrics**
- **Response Time**: P50, P95, P99
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Resource Usage**: CPU, Memory, Network

**4. Performance Test Cases**
```yaml
- name: "Concurrent Users Test"
  request:
    method: GET
    url: "/api/users"
  expect:
    status: 200
    response_time: "< 500ms"
  metadata:
    concurrent_users: 100
    duration: "5m"

- name: "Database Query Performance"
  request:
    method: GET
    url: "/api/reports/complex"
  expect:
    status: 200
    response_time: "< 2000ms"
```

**5. Performance Optimization Tips**
- **Caching**: Implement Redis/Memcached
- **Database**: Optimize queries, add indexes
- **CDN**: Use for static content
- **Compression**: Enable gzip/brotli
- **Connection Pooling**: Reuse connections
- **Async Processing**: Use background jobs

**6. Monitoring Setup**
```yaml
- name: "Health Check with Performance"
  request:
    method: GET
    url: "/health"
  expect:
    status: 200
    response_time: "< 100ms"
  metadata:
    alert_threshold: "500ms"
```

**7. Common Performance Issues**
- **N+1 Queries**: Use eager loading
- **Memory Leaks**: Monitor heap usage
- **Network Latency**: Use CDN/edge locations
- **Database Bottlenecks**: Optimize queries
- **Inefficient Algorithms**: Profile code

**8. Performance Testing Tools**
- **Artillery**: Load testing
- **k6**: Performance testing
- **JMeter**: Apache load testing
- **Gatling**: Scala-based testing
- **Restaceratops**: API-specific testing

Need help setting up performance tests for your specific API?"""
    
    def _get_security_guidance(self, user_input: str) -> str:
        """Provide security testing guidance."""
        return """🔒 **API Security Testing Guide**

Here's a comprehensive security testing approach:

**1. Authentication Testing**
```yaml
- name: "Test Weak Passwords"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "admin"
      password: "password123"
  expect:
    status: 401

- name: "Test Brute Force Protection"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "admin"
      password: "wrong_password"
  expect:
    status: 429  # Rate limited
```

**2. Authorization Testing**
```yaml
- name: "Test Unauthorized Access"
  request:
    method: GET
    url: "/api/admin/users"
    headers:
      Authorization: "Bearer {user_token}"
  expect:
    status: 403

- name: "Test Privilege Escalation"
  request:
    method: PUT
    url: "/api/users/123/role"
    headers:
      Authorization: "Bearer {user_token}"
    json:
      role: "admin"
  expect:
    status: 403
```

**3. Input Validation Testing**
```yaml
- name: "Test SQL Injection"
  request:
    method: GET
    url: "/api/users?search=' OR 1=1--"
  expect:
    status: 400

- name: "Test XSS Prevention"
  request:
    method: POST
    url: "/api/comments"
    json:
      content: "<script>alert('xss')</script>"
  expect:
    status: 400
```

**4. Data Exposure Testing**
```yaml
- name: "Test Sensitive Data Exposure"
  request:
    method: GET
    url: "/api/users/123"
  expect:
    status: 200
    json:
      id: 123
      name: "string"
      # Should NOT include: password, ssn, credit_card
```

**5. Security Headers Testing**
```yaml
- name: "Test Security Headers"
  request:
    method: GET
    url: "/api/data"
  expect:
    status: 200
    headers:
      X-Content-Type-Options: "nosniff"
      X-Frame-Options: "DENY"
      X-XSS-Protection: "1; mode=block"
      Strict-Transport-Security: "string"
```

**6. Common Security Vulnerabilities**
- **OWASP Top 10**: Check for common vulnerabilities
- **CORS Misconfiguration**: Test cross-origin requests
- **JWT Security**: Validate token handling
- **API Rate Limiting**: Test abuse prevention
- **Data Encryption**: Verify sensitive data protection

**7. Security Testing Tools**
- **OWASP ZAP**: Automated security testing
- **Burp Suite**: Manual security testing
- **Nmap**: Network security scanning
- **Nikto**: Web server security scanner

**8. Security Best Practices**
- Use HTTPS everywhere
- Implement proper authentication
- Validate all inputs
- Sanitize outputs
- Log security events
- Regular security audits

Need help implementing specific security tests?"""
    
    def _get_test_generation_guidance(self, user_input: str) -> str:
        """Provide test generation guidance."""
        return """🧪 **Intelligent Test Generation Guide**

Here's how to generate comprehensive test cases:

**1. OpenAPI Specification Testing**
```yaml
# Generate tests from OpenAPI spec
- name: "Auto-generated from OpenAPI"
  request:
    method: "{method}"
    url: "{base_url}{path}"
    headers:
      Content-Type: "application/json"
    json: "{request_body}"
  expect:
    status: "{expected_status}"
    json: "{expected_response}"
```

**2. Test Case Templates**

**CRUD Operations**
```yaml
- name: "Create Resource"
  request:
    method: POST
    url: "/api/resources"
    json:
      name: "Test Resource"
      description: "Generated test data"
  expect:
    status: 201
    json:
      id: "number"
      name: "Test Resource"

- name: "Read Resource"
  request:
    method: GET
    url: "/api/resources/{id}"
  expect:
    status: 200
    json:
      id: "{id}"
      name: "string"

- name: "Update Resource"
  request:
    method: PUT
    url: "/api/resources/{id}"
    json:
      name: "Updated Resource"
  expect:
    status: 200
    json:
      id: "{id}"
      name: "Updated Resource"

- name: "Delete Resource"
  request:
    method: DELETE
    url: "/api/resources/{id}"
  expect:
    status: 204
```

**3. Data-Driven Testing**
```yaml
- name: "Test with Multiple Data Sets"
  request:
    method: POST
    url: "/api/users"
    json:
      name: "{name}"
      email: "{email}"
      age: "{age}"
  expect:
    status: 201
  data_sets:
    - name: "John Doe", email: "john@example.com", age: 25
    - name: "Jane Smith", email: "jane@example.com", age: 30
    - name: "Bob Wilson", email: "bob@example.com", age: 35
```

**4. Edge Case Testing**
```yaml
- name: "Test Empty Payload"
  request:
    method: POST
    url: "/api/data"
    json: {}
  expect:
    status: 400

- name: "Test Large Payload"
  request:
    method: POST
    url: "/api/data"
    json:
      content: "{large_string}"
  expect:
    status: 413  # Payload Too Large

- name: "Test Special Characters"
  request:
    method: POST
    url: "/api/data"
    json:
      content: "!@#$%^&*()_+-=[]{}|;':\",./<>?"
  expect:
    status: 200
```

**5. Workflow Testing**
```yaml
- name: "Complete User Registration Flow"
  steps:
    - name: "Register User"
      request:
        method: POST
        url: "/api/register"
        json:
          email: "test@example.com"
          password: "secure123"
      expect:
        status: 201
        json:
          user_id: "number"
    
    - name: "Verify Email"
      request:
        method: POST
        url: "/api/verify"
        json:
          token: "{verification_token}"
      expect:
        status: 200
    
    - name: "Login User"
      request:
        method: POST
        url: "/api/login"
        json:
          email: "test@example.com"
          password: "secure123"
      expect:
        status: 200
        json:
          access_token: "string"
```

**6. Test Generation Best Practices**
- Cover all HTTP methods
- Test all status codes
- Include positive and negative cases
- Test boundary values
- Include authentication scenarios
- Test error conditions
- Validate response schemas

**7. Automated Test Generation**
```python
# Generate tests from API documentation
def generate_tests_from_spec(openapi_spec):
    tests = []
    for path, methods in openapi_spec['paths'].items():
        for method, details in methods.items():
            test = create_test_case(path, method, details)
            tests.append(test)
    return tests
```

Need help generating specific test cases for your API?"""
    
    def _get_analyze_test_results(self, user_input: str) -> str:
        """Analyze test results and provide insights."""
        return """📊 **Test Results Analysis Guide**

Here's how to analyze and interpret your test results:

**1. Success Rate Analysis**
```yaml
# Example test results
total_tests: 10
passed_tests: 8
failed_tests: 2
success_rate: 80%

# Analysis
- High success rate (>90%): Good API health
- Medium success rate (70-90%): Needs attention
- Low success rate (<70%): Critical issues
```

**2. Response Time Analysis**
```yaml
# Performance metrics
avg_response_time: 450ms
min_response_time: 120ms
max_response_time: 1200ms

# Performance categories
- Excellent: < 200ms
- Good: 200-500ms
- Acceptable: 500-1000ms
- Poor: > 1000ms
```

**3. Error Pattern Analysis**
```yaml
# Common error patterns
status_codes:
  400: 5  # Bad Request - Input validation issues
  401: 2  # Unauthorized - Auth problems
  404: 3  # Not Found - Routing issues
  500: 1  # Server Error - Backend issues
```

**4. Test Result Categories**

**✅ Passing Tests**
- Verify expected behavior
- Check response accuracy
- Validate performance metrics
- Confirm data integrity

**❌ Failing Tests**
- Analyze error messages
- Check request/response logs
- Verify test data
- Test environment issues

**⚠️ Flaky Tests**
- Inconsistent results
- Timing dependencies
- External service issues
- Race conditions

**5. Root Cause Analysis**
```yaml
# Common failure patterns
- Authentication failures: Check tokens, permissions
- Validation errors: Verify input data, schemas
- Timeout errors: Check performance, network
- Database errors: Check connections, queries
- External service failures: Check dependencies
```

**6. Performance Insights**
```yaml
# Response time distribution
fast_responses: 60%  # < 200ms
normal_responses: 30%  # 200-500ms
slow_responses: 10%  # > 500ms

# Recommendations
- Optimize slow endpoints
- Implement caching
- Add database indexes
- Use CDN for static content
```

**7. Security Analysis**
```yaml
# Security test results
authentication_tests: 5/5 passed
authorization_tests: 4/5 passed
input_validation_tests: 3/5 passed
data_exposure_tests: 5/5 passed

# Security score: 85%
# Recommendations: Improve input validation
```

**8. Trend Analysis**
```yaml
# Historical comparison
current_success_rate: 85%
previous_success_rate: 90%
trend: Declining

# Action items
- Investigate recent changes
- Check new deployments
- Review error logs
- Update test cases
```

**9. Automated Reporting**
```python
def generate_test_report(results):
    report = {
        "summary": calculate_summary(results),
        "performance": analyze_performance(results),
        "errors": categorize_errors(results),
        "recommendations": generate_recommendations(results)
    }
    return report
```

**10. Action Items Based on Results**
- **High error rate**: Debug failing tests
- **Slow performance**: Optimize endpoints
- **Security issues**: Implement fixes
- **Flaky tests**: Improve test stability
- **Missing coverage**: Add more test cases

Need help analyzing specific test results?"""
    
    def _get_general_api_guidance(self, user_input: str) -> str:
        """Provide general API guidance."""
        return """🌐 **General API Testing Best Practices**

Here's a comprehensive guide to API testing:

**1. API Testing Pyramid**
```
    /\
   /  \     E2E Tests (Few)
  /____\    Integration Tests (Some)
 /______\   Unit Tests (Many)
```

**2. Essential Test Types**
- **Unit Tests**: Individual functions/methods
- **Integration Tests**: API endpoints
- **End-to-End Tests**: Complete workflows
- **Performance Tests**: Load and stress testing
- **Security Tests**: Authentication and authorization

**3. HTTP Method Testing**
```yaml
# GET - Retrieve data
- name: "GET Resource"
  request:
    method: GET
    url: "/api/resources"
  expect:
    status: 200

# POST - Create data
- name: "POST Resource"
  request:
    method: POST
    url: "/api/resources"
    json:
      name: "New Resource"
  expect:
    status: 201

# PUT - Update data
- name: "PUT Resource"
  request:
    method: PUT
    url: "/api/resources/123"
    json:
      name: "Updated Resource"
  expect:
    status: 200

# DELETE - Remove data
- name: "DELETE Resource"
  request:
    method: DELETE
    url: "/api/resources/123"
  expect:
    status: 204
```

**4. Status Code Testing**
- **2xx Success**: 200, 201, 204
- **3xx Redirection**: 301, 302, 304
- **4xx Client Error**: 400, 401, 403, 404, 422
- **5xx Server Error**: 500, 502, 503

**5. Response Validation**
```yaml
- name: "Validate Response Structure"
  request:
    method: GET
    url: "/api/users/123"
  expect:
    status: 200
    json:
      id: 123
      name: "string"
      email: "string"
      created_at: "string"
    headers:
      Content-Type: "application/json"
      Cache-Control: "string"
```

**6. Environment Management**
```yaml
# Test environments
development:
  base_url: "http://localhost:8000"
  api_key: "dev_key"

staging:
  base_url: "https://staging-api.example.com"
  api_key: "staging_key"

production:
  base_url: "https://api.example.com"
  api_key: "prod_key"
```

**7. Test Data Management**
- Use test databases
- Create test fixtures
- Clean up after tests
- Use unique identifiers
- Avoid hardcoded values

**8. Continuous Integration**
```yaml
# CI/CD pipeline
- Run tests on every commit
- Generate test reports
- Block deployment on failures
- Monitor test coverage
- Track performance metrics
```

**9. API Documentation Testing**
- Test against OpenAPI specs
- Validate response schemas
- Check example data
- Verify endpoint descriptions

**10. Monitoring and Alerting**
- Set up health checks
- Monitor response times
- Track error rates
- Alert on failures
- Log all requests

**11. Best Practices Summary**
✅ Test all endpoints and methods
✅ Validate request/response data
✅ Test error conditions
✅ Check performance metrics
✅ Verify security requirements
✅ Use realistic test data
✅ Maintain test documentation
✅ Automate test execution

Need help implementing any of these practices?"""
    
    def _get_fallback_test_template(self, api_spec: str) -> str:
        """Get a fallback test template."""
        return f"""# Generated Test Template for API

Based on your API specification, here's a basic test template:

```yaml
name: "API Test Suite"
description: "Generated test cases for API endpoints"
base_url: "https://api.example.com"

tests:
  - name: "Health Check"
    request:
      method: GET
      url: "/health"
    expect:
      status: 200
      json:
        status: "healthy"

  - name: "Get Resources"
    request:
      method: GET
      url: "/api/resources"
    expect:
      status: 200
      json:
        - id: "number"
          name: "string"

  - name: "Create Resource"
    request:
      method: POST
      url: "/api/resources"
      json:
        name: "Test Resource"
        description: "Generated test data"
    expect:
      status: 201
      json:
        id: "number"
        name: "Test Resource"

  - name: "Update Resource"
    request:
      method: PUT
      url: "/api/resources/{{id}}"
      json:
        name: "Updated Resource"
    expect:
      status: 200
      json:
        id: "{{id}}"
        name: "Updated Resource"

  - name: "Delete Resource"
    request:
      method: DELETE
      url: "/api/resources/{{id}}"
    expect:
      status: 204
```

**Customize this template based on your specific API endpoints and requirements.**

API Specification provided:
{api_spec[:500]}...
"""
    
    async def reset_system(self) -> str:
        """Reset the AI system."""
        self.conversation_history = []
        return "🔄 AI system reset successfully. Conversation history cleared."

# Global instance
_enhanced_ai_system = None

def get_enhanced_ai_system() -> EnhancedAISystem:
    """Get the global enhanced AI system instance."""
    global _enhanced_ai_system
    if _enhanced_ai_system is None:
        _enhanced_ai_system = EnhancedAISystem()
    return _enhanced_ai_system

# Test function
async def test_enhanced_ai_system():
    """Test the enhanced AI system."""
    ai_system = get_enhanced_ai_system()
    response = await ai_system.handle_conversation("Hello, test the AI system")
    print(f"AI Response: {response}")
    return response

if __name__ == "__main__":
    asyncio.run(test_enhanced_ai_system()) 