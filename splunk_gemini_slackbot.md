# Splunk Query Generator Slack Bot with Gemini LLM

A comprehensive Slack bot that uses Google's Gemini LLM to generate Splunk queries based on natural language requests.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This Slack bot allows users to request Splunk queries using natural language. The bot leverages Google's Gemini LLM to understand user requests and generate appropriate Splunk Search Processing Language (SPL) queries.

### Example Usage
```
User: "Show me failed login attempts in the last 24 hours"
Bot: "Here's your Splunk query:
```
index=security sourcetype=auth action=failure earliest=-24h
| stats count by user, src_ip
| sort -count
```"
```

## Features

- 🤖 Natural language to Splunk query conversion
- 🔍 Intelligent query optimization suggestions
- 📊 Support for various Splunk use cases (security, performance, logs)
- 🛡️ Query validation and safety checks
- 📝 Query explanation and documentation
- 🎯 Context-aware responses
- 🔒 Secure API key management
- 📈 Usage analytics and logging

## Prerequisites

- Python 3.8 or higher
- Slack workspace with admin permissions
- Google Cloud Project with Gemini API access
- Basic understanding of Splunk SPL
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/splunk-gemini-slackbot.git
cd splunk-gemini-slackbot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` with your configuration values (see Configuration section).

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token

# Google Gemini Configuration
GOOGLE_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash

# Application Configuration
PORT=3000
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=1000
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Optional: Database Configuration (for analytics)
DATABASE_URL=sqlite:///bot_analytics.db

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn
```

### Slack App Configuration

1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new app
3. Configure the following scopes under "OAuth & Permissions":
   - `app_mentions:read`
   - `chat:write`
   - `commands`
   - `channels:read`
   - `groups:read`
   - `im:read`
   - `mpim:read`

4. Enable "Event Subscriptions" and add:
   - `app_mention`
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`

5. Create slash commands:
   - `/splunk` - Generate Splunk queries
   - `/splunk-help` - Show help information

### Google Cloud Setup

1. Create a Google Cloud Project
2. Enable the Gemini API
3. Generate an API key
4. Set up authentication (API key or service account)

## Code Structure

```
splunk-gemini-slackbot/
├── src/
│   ├── __init__.py
│   ├── app.py                 # Main application entry point
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── slack_bot.py       # Slack bot implementation
│   │   ├── handlers.py        # Event and command handlers
│   │   └── middleware.py      # Authentication and rate limiting
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── gemini_client.py   # Gemini LLM client
│   │   ├── prompt_templates.py # Prompt engineering
│   │   └── query_validator.py # Splunk query validation
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py          # Database models
│   │   └── analytics.py       # Usage analytics
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging configuration
│       ├── config.py          # Configuration management
│       └── helpers.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_bot.py
│   ├── test_gemini.py
│   └── test_validators.py
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
└── setup.py
```

## Core Application Files

### requirements.txt
```txt
slack-bolt==1.18.1
google-generativeai==0.3.2
python-dotenv==1.0.0
sqlalchemy==2.0.23
alembic==1.13.1
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
redis==5.0.1
structlog==23.2.0
sentry-sdk==1.38.0
pytest==7.4.3
pytest-asyncio==0.21.1
requests==2.31.0
```

### src/app.py
```python
#!/usr/bin/env python3
"""
Splunk Query Generator Slack Bot with Gemini LLM
Main application entry point
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

from src.bot.slack_bot import SplunkBot
from src.utils.config import Settings
from src.utils.logger import setup_logging
from src.database.models import init_db


# Initialize configuration
settings = Settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Splunk Gemini Slack Bot...")
    
    # Initialize database
    await init_db()
    
    # Initialize Slack bot
    await bot.start_async()
    
    yield
    
    logger.info("Shutting down Splunk Gemini Slack Bot...")


# Initialize FastAPI app
app = FastAPI(
    title="Splunk Gemini Slack Bot",
    description="A Slack bot that generates Splunk queries using Gemini LLM",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize Slack bot
bot = SplunkBot(settings)
slack_app = bot.app

# Create Slack request handler
handler = AsyncSlackRequestHandler(slack_app)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "splunk-gemini-slackbot"}


@app.post("/slack/events")
async def slack_events(req):
    """Handle Slack events"""
    return await handler.handle(req)


@app.post("/slack/commands")
async def slack_commands(req):
    """Handle Slack slash commands"""
    return await handler.handle(req)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
```

### src/utils/config.py
```python
"""Configuration management"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Slack Configuration
    slack_bot_token: str
    slack_signing_secret: str
    slack_app_token: Optional[str] = None
    
    # Gemini Configuration
    google_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    
    # Application Configuration
    port: int = 3000
    log_level: str = "INFO"
    debug: bool = False
    max_query_length: int = 1000
    rate_limit_requests: int = 10
    rate_limit_window: int = 60
    
    # Database Configuration
    database_url: str = "sqlite:///bot_analytics.db"
    
    # Optional Monitoring
    sentry_dsn: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
```

### src/utils/logger.py
```python
"""Logging configuration"""

import logging
import sys
from typing import Dict, Any

import structlog


def setup_logging(log_level: str = "INFO") -> None:
    """Setup structured logging"""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
```

### src/bot/slack_bot.py
```python
"""Slack bot implementation"""

import logging
from typing import Dict, Any, Optional

from slack_bolt.async_app import AsyncApp
from slack_bolt import BoltContext

from src.llm.gemini_client import GeminiClient
from src.bot.handlers import MessageHandler, CommandHandler
from src.bot.middleware import AuthMiddleware, RateLimitMiddleware
from src.utils.config import Settings


logger = logging.getLogger(__name__)


class SplunkBot:
    """Main Slack bot class"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.app = AsyncApp(
            token=settings.slack_bot_token,
            signing_secret=settings.slack_signing_secret
        )
        
        # Initialize LLM client
        self.gemini_client = GeminiClient(settings)
        
        # Initialize handlers
        self.message_handler = MessageHandler(self.gemini_client)
        self.command_handler = CommandHandler(self.gemini_client)
        
        # Setup middleware
        self._setup_middleware()
        
        # Register event handlers
        self._register_handlers()
    
    def _setup_middleware(self):
        """Setup middleware for authentication and rate limiting"""
        
        # Authentication middleware
        auth_middleware = AuthMiddleware(self.settings)
        self.app.middleware(auth_middleware.process)
        
        # Rate limiting middleware
        rate_limit_middleware = RateLimitMiddleware(self.settings)
        self.app.middleware(rate_limit_middleware.process)
    
    def _register_handlers(self):
        """Register event and command handlers"""
        
        # Message handlers
        self.app.message("splunk")(self.message_handler.handle_splunk_mention)
        self.app.event("app_mention")(self.message_handler.handle_app_mention)
        
        # Command handlers
        self.app.command("/splunk")(self.command_handler.handle_splunk_command)
        self.app.command("/splunk-help")(self.command_handler.handle_help_command)
        
        # Error handler
        self.app.error(self._handle_error)
    
    async def _handle_error(self, error: Exception, body: Dict[str, Any], context: BoltContext):
        """Global error handler"""
        logger.error(f"Slack bot error: {error}", extra={"body": body})
        
        # Send error message to user if possible
        if "channel" in body.get("event", {}):
            await self.app.client.chat_postMessage(
                channel=body["event"]["channel"],
                text="⚠️ Sorry, I encountered an error processing your request. Please try again."
            )
    
    async def start_async(self):
        """Start the bot in async mode"""
        logger.info("Slack bot initialized successfully")
```

### src/bot/handlers.py
```python
"""Event and command handlers for Slack bot"""

import logging
import re
from typing import Dict, Any

from slack_bolt.async_app import AsyncApp
from slack_bolt import BoltContext, BoltRequest

from src.llm.gemini_client import GeminiClient
from src.database.analytics import log_query_request


logger = logging.getLogger(__name__)


class MessageHandler:
    """Handles Slack message events"""
    
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    async def handle_splunk_mention(self, message: Dict[str, Any], say, context: BoltContext):
        """Handle messages mentioning 'splunk'"""
        
        text = message.get("text", "").lower()
        user = message.get("user")
        channel = message.get("channel")
        
        # Log the request
        await log_query_request(user, channel, text)
        
        # Generate typing indicator
        await say("🤔 Let me generate that Splunk query for you...")
        
        try:
            # Generate Splunk query using Gemini
            response = await self.gemini_client.generate_splunk_query(text)
            
            # Format and send response
            formatted_response = self._format_query_response(response)
            await say(formatted_response)
            
        except Exception as e:
            logger.error(f"Error generating Splunk query: {e}")
            await say("❌ Sorry, I couldn't generate a query for that request. Please try rephrasing your question.")
    
    async def handle_app_mention(self, event: Dict[str, Any], say, context: BoltContext):
        """Handle direct mentions of the bot"""
        
        text = event.get("text", "")
        user = event.get("user")
        channel = event.get("channel")
        
        # Remove bot mention from text
        clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
        
        if not clean_text:
            await say(
                "👋 Hi! I'm your Splunk query assistant. "
                "Ask me to generate Splunk queries using natural language!\n\n"
                "Examples:\n"
                "• Show me failed login attempts in the last hour\n"
                "• Find errors in the web application logs\n"
                "• Get top 10 source IPs by traffic volume"
            )
            return
        
        # Log the request
        await log_query_request(user, channel, clean_text)
        
        # Generate typing indicator
        await say("🤔 Generating your Splunk query...")
        
        try:
            # Generate Splunk query using Gemini
            response = await self.gemini_client.generate_splunk_query(clean_text)
            
            # Format and send response
            formatted_response = self._format_query_response(response)
            await say(formatted_response)
            
        except Exception as e:
            logger.error(f"Error generating Splunk query: {e}")
            await say("❌ Sorry, I couldn't generate a query for that request. Please try rephrasing your question.")
    
    def _format_query_response(self, response: Dict[str, Any]) -> str:
        """Format the Gemini response for Slack"""
        
        query = response.get("query", "")
        explanation = response.get("explanation", "")
        suggestions = response.get("suggestions", [])
        
        formatted = f"🔍 **Here's your Splunk query:**\n\n```\n{query}\n```"
        
        if explanation:
            formatted += f"\n\n📝 **Explanation:**\n{explanation}"
        
        if suggestions:
            formatted += f"\n\n💡 **Suggestions:**\n"
            for suggestion in suggestions:
                formatted += f"• {suggestion}\n"
        
        return formatted


class CommandHandler:
    """Handles Slack slash commands"""
    
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    async def handle_splunk_command(self, ack, respond, command: Dict[str, Any], context: BoltContext):
        """Handle /splunk slash command"""
        
        await ack()
        
        text = command.get("text", "").strip()
        user_id = command.get("user_id")
        channel_id = command.get("channel_id")
        
        if not text:
            await respond(
                "Please provide a description of what you want to search for.\n"
                "Example: `/splunk failed login attempts last 24 hours`"
            )
            return
        
        # Log the request
        await log_query_request(user_id, channel_id, text)
        
        try:
            # Send initial response
            await respond("🤔 Generating your Splunk query...")
            
            # Generate Splunk query using Gemini
            response = await self.gemini_client.generate_splunk_query(text)
            
            # Format and send final response
            formatted_response = self._format_query_response(response)
            await respond(formatted_response)
            
        except Exception as e:
            logger.error(f"Error generating Splunk query: {e}")
            await respond("❌ Sorry, I couldn't generate a query for that request. Please try rephrasing your question.")
    
    async def handle_help_command(self, ack, respond, command: Dict[str, Any]):
        """Handle /splunk-help slash command"""
        
        await ack()
        
        help_text = """
🔍 **Splunk Query Generator Bot Help**

**How to use:**
• Mention me with your request: `@SplunkBot show me errors in the last hour`
• Use slash commands: `/splunk failed login attempts`
• Just type messages containing 'splunk'

**Example requests:**
• "Show me failed authentication events in the last 24 hours"
• "Find all errors from the web server logs"
• "Get top 10 users by activity"
• "Search for suspicious network traffic"
• "Show me application performance metrics"

**Tips:**
• Be specific about time ranges (last hour, yesterday, etc.)
• Mention specific log sources if you know them
• Include what you want to see in the results

**Commands:**
• `/splunk <your request>` - Generate a Splunk query
• `/splunk-help` - Show this help message

Need more help? Contact the IT team or check the Splunk documentation.
        """
        
        await respond(help_text)
    
    def _format_query_response(self, response: Dict[str, Any]) -> str:
        """Format the Gemini response for Slack"""
        
        query = response.get("query", "")
        explanation = response.get("explanation", "")
        suggestions = response.get("suggestions", [])
        
        formatted = f"🔍 **Here's your Splunk query:**\n\n```\n{query}\n```"
        
        if explanation:
            formatted += f"\n\n📝 **Explanation:**\n{explanation}"
        
        if suggestions:
            formatted += f"\n\n💡 **Suggestions:**\n"
            for suggestion in suggestions:
                formatted += f"• {suggestion}\n"
        
        return formatted
```

### src/bot/middleware.py
```python
"""Middleware for authentication and rate limiting"""

import logging
import time
from typing import Dict, Any, Callable
from collections import defaultdict

from slack_bolt import BoltContext, BoltRequest

from src.utils.config import Settings


logger = logging.getLogger(__name__)


class AuthMiddleware:
    """Authentication middleware"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    async def process(self, req: BoltRequest, resp, next: Callable):
        """Process authentication"""
        
        # Verify request signature (handled by Slack Bolt)
        # Additional auth logic can be added here
        
        await next()


class RateLimitMiddleware:
    """Rate limiting middleware"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.requests = defaultdict(list)
    
    async def process(self, req: BoltRequest, resp, next: Callable):
        """Process rate limiting"""
        
        # Get user ID
        user_id = None
        if hasattr(req, 'body'):
            if 'event' in req.body:
                user_id = req.body['event'].get('user')
            elif 'user_id' in req.body:
                user_id = req.body['user_id']
        
        if user_id:
            current_time = time.time()
            window_start = current_time - self.settings.rate_limit_window
            
            # Clean old requests
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if req_time > window_start
            ]
            
            # Check rate limit
            if len(self.requests[user_id]) >= self.settings.rate_limit_requests:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                # Could send rate limit message here
                return
            
            # Add current request
            self.requests[user_id].append(current_time)
        
        await next()
```

### src/llm/gemini_client.py
```python
"""Google Gemini LLM client for generating Splunk queries"""

import logging
import json
from typing import Dict, Any, List, Optional

import google.generativeai as genai

from src.llm.prompt_templates import SPLUNK_QUERY_PROMPT
from src.llm.query_validator import SplunkQueryValidator
from src.utils.config import Settings


logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini LLM"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.validator = SplunkQueryValidator()
        
        # Configure Gemini
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    async def generate_splunk_query(self, user_request: str) -> Dict[str, Any]:
        """Generate a Splunk query based on user request"""
        
        try:
            # Prepare the prompt
            prompt = self._prepare_prompt(user_request)
            
            # Generate content
            response = await self.model.generate_content_async(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,
                }
            )
            
            # Parse response
            result = self._parse_response(response.text)
            
            # Validate query
            validation_result = self.validator.validate_query(result.get("query", ""))
            if not validation_result["is_valid"]:
                result["warnings"] = validation_result["warnings"]
            
            logger.info(f"Generated Splunk query for request: {user_request[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error generating Splunk query: {e}")
            raise
    
    def _prepare_prompt(self, user_request: str) -> str:
        """Prepare the prompt for Gemini"""
        
        return SPLUNK_QUERY_PROMPT.format(
            user_request=user_request,
            max_length=self.settings.max_query_length
        )
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the Gemini response"""
        
        try:
            # Try to parse as JSON first
            if response_text.strip().startswith('{'):
                return json.loads(response_text)
            
            # Otherwise, extract components using text parsing
            lines = response_text.strip().split('\n')
            result = {
                "query": "",
                "explanation": "",
                "suggestions": []
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                
                if line.startswith("QUERY:") or "```" in line:
                    current_section = "query"
                    continue
                elif line.startswith("EXPLANATION:"):
                    current_section = "explanation"
                    continue
                elif line.startswith("SUGGESTIONS:"):
                    current_section = "suggestions"
                    continue
                
                if current_section == "query" and line and not line.startswith("```"):
                    result["query"] += line + "\n"
                elif current_section == "explanation" and line:
                    result["explanation"] += line + " "
                elif current_section == "suggestions" and line.startswith("-"):
                    result["suggestions"].append(line[1:].strip())
            
            # Clean up
            result["query"] = result["query"].strip()
            result["explanation"] = result["explanation"].strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return {
                "query": "index=* | head 10",
                "explanation": "I had trouble parsing the response. Here's a basic query to get you started.",
                "suggestions": ["Please try rephrasing your request"]
            }
```

### src/llm/prompt_templates.py
```python
"""Prompt templates for Gemini LLM"""

SPLUNK_QUERY_PROMPT = """
You are an expert Splunk administrator and query specialist. Your task is to convert natural language requests into efficient Splunk Search Processing Language (SPL) queries.

USER REQUEST: {user_request}

Please generate a Splunk query that addresses this request. Follow these guidelines:

1. Use appropriate Splunk commands and functions
2. Include proper time ranges when mentioned
3. Use efficient search patterns
4. Include relevant statistical commands when appropriate
5. Keep queries under {max_length} characters
6. Follow Splunk best practices

Provide your response in this JSON format:
{{
    "query": "the complete SPL query",
    "explanation": "brief explanation of what the query does",
    "suggestions": ["list of optimization suggestions or variations"]
}}

Common Splunk patterns to consider:
- index=<index_name> for specifying data sources
- sourcetype=<type> for log type filtering
- earliest=-1h, earliest=-24h for time ranges
- stats, chart, timechart for aggregations
- eval for field calculations
- search, where for filtering
- sort, head, tail for result ordering
- rex for field extraction

Security-related searches often use:
- index=security, index=auth, index=firewall
- sourcetype=auth, sourcetype=cisco, sourcetype=windows

Application logs often use:
- index=app, index=web
- sourcetype=access_log, sourcetype=error_log

Performance monitoring often uses:
- index=performance, index=metrics
- Statistical commands like avg, max, min, perc95

Always consider:
- Performance impact of wildcards
- Proper field extraction
- Appropriate time windows
- Logical operators (AND, OR, NOT)

Generate an efficient, accurate Splunk query for the user's request.
"""

SPLUNK_HELP_PROMPT = """
Provide helpful guidance about Splunk query construction for this specific request: {user_request}

Include:
1. Suggested approach
2. Key fields to consider
3. Potential data sources
4. Time range recommendations
5. Common pitfalls to avoid
"""
```

### src/llm/query_validator.py
```python
"""Splunk query validator"""

import re
import logging
from typing import Dict, List, Any


logger = logging.getLogger(__name__)


class SplunkQueryValidator:
    """Validates Splunk queries for safety and best practices"""
    
    def __init__(self):
        self.dangerous_commands = [
            'delete', 'drop', 'truncate', 'modify', 'update',
            'insert', 'create', 'alter', 'grant', 'revoke'
        ]
        
        self.required_patterns = [
            r'index\s*=\s*\w+',  # Should specify an index
        ]
        
        self.warning_patterns = [
            (r'\*', "Wildcard searches can be slow"),
            (r'index\s*=\s*\*', "Searching all indexes can be very slow"),
            (r'earliest\s*=\s*0', "Searching all time can be very slow"),
            (r'(?i)regex\s+[^|]*\.\*', "Complex regex patterns can impact performance"),
        ]
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate a Splunk query"""
        
        result = {
            "is_valid": True,
            "warnings": [],
            "errors": []
        }
        
        if not query or not query.strip():
            result["is_valid"] = False
            result["errors"].append("Query cannot be empty")
            return result
        
        # Check for dangerous commands
        for cmd in self.dangerous_commands:
            if re.search(rf'\b{cmd}\b', query, re.IGNORECASE):
                result["is_valid"] = False
                result["errors"].append(f"Dangerous command detected: {cmd}")
        
        # Check for warnings
        for pattern, warning in self.warning_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                result["warnings"].append(warning)
        
        # Check for best practices
        if not re.search(r'index\s*=', query, re.IGNORECASE):
            result["warnings"].append("Consider specifying an index for better performance")
        
        if not re.search(r'earliest\s*=', query, re.IGNORECASE):
            result["warnings"].append("Consider adding a time range for better performance")
        
        return result
    
    def suggest_optimizations(self, query: str) -> List[str]:
        """Suggest query optimizations"""
        
        suggestions = []
        
        # Suggest index specification
        if not re.search(r'index\s*=', query, re.IGNORECASE):
            suggestions.append("Add index specification (e.g., index=main)")
        
        # Suggest time range
        if not re.search(r'earliest\s*=', query, re.IGNORECASE):
            suggestions.append("Add time range (e.g., earliest=-24h)")
        
        # Suggest field extraction
        if '|' not in query:
            suggestions.append("Consider adding statistical commands for better analysis")
        
        return suggestions


### src/database/models.py
```python
"""Database models for analytics and logging"""

import datetime
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.config import settings


Base = declarative_base()


class QueryRequest(Base):
    """Model for tracking query requests"""
    
    __tablename__ = "query_requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    channel_id = Column(String(50), nullable=False)
    request_text = Column(Text, nullable=False)
    generated_query = Column(Text)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    response_time = Column(Integer)  # milliseconds


class UserSession(Base):
    """Model for tracking user sessions"""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    session_start = Column(DateTime, default=datetime.datetime.utcnow)
    session_end = Column(DateTime)
    queries_count = Column(Integer, default=0)


# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### src/database/analytics.py
```python
"""Analytics and logging functions"""

import logging
import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.database.models import QueryRequest, UserSession, get_db


logger = logging.getLogger(__name__)


async def log_query_request(
    user_id: str,
    channel_id: str,
    request_text: str,
    generated_query: Optional[str] = None,
    success: bool = True,
    error_message: Optional[str] = None,
    response_time: Optional[int] = None
):
    """Log a query request to the database"""
    
    try:
        db = next(get_db())
        
        query_request = QueryRequest(
            user_id=user_id,
            channel_id=channel_id,
            request_text=request_text,
            generated_query=generated_query,
            success=success,
            error_message=error_message,
            response_time=response_time
        )
        
        db.add(query_request)
        db.commit()
        
        logger.info(f"Logged query request for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error logging query request: {e}")


async def get_user_stats(user_id: str) -> dict:
    """Get usage statistics for a user"""
    
    try:
        db = next(get_db())
        
        total_queries = db.query(QueryRequest).filter(
            QueryRequest.user_id == user_id
        ).count()
        
        successful_queries = db.query(QueryRequest).filter(
            QueryRequest.user_id == user_id,
            QueryRequest.success == True
        ).count()
        
        recent_queries = db.query(QueryRequest).filter(
            QueryRequest.user_id == user_id,
            QueryRequest.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
        ).count()
        
        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "success_rate": successful_queries / total_queries if total_queries > 0 else 0,
            "recent_queries": recent_queries
        }
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return {}
```

### src/utils/helpers.py
```python
"""Utility helper functions"""

import re
import hashlib
from typing import List, Dict, Any


def sanitize_query(query: str) -> str:
    """Sanitize a Splunk query for safety"""
    
    # Remove potentially dangerous characters
    query = re.sub(r'[;\'"`]', '', query)
    
    # Limit query length
    if len(query) > 1000:
        query = query[:1000]
    
    return query.strip()


def extract_time_range(text: str) -> str:
    """Extract time range from natural language text"""
    
    patterns = {
        r'last\s+(\d+)\s+hour[s]?': lambda m: f"earliest=-{m.group(1)}h",
        r'last\s+(\d+)\s+day[s]?': lambda m: f"earliest=-{m.group(1)}d",
        r'last\s+(\d+)\s+week[s]?': lambda m: f"earliest=-{m.group(1)}w",
        r'last\s+(\d+)\s+minute[s]?': lambda m: f"earliest=-{m.group(1)}m",
        r'yesterday': lambda m: "earliest=-1d@d latest=@d",
        r'today': lambda m: "earliest=@d",
        r'this\s+week': lambda m: "earliest=@w0",
        r'this\s+month': lambda m: "earliest=@mon",
    }
    
    for pattern, formatter in patterns.items():
        match = re.search(pattern, text.lower())
        if match:
            return formatter(match)
    
    return "earliest=-24h"  # Default to last 24 hours


def format_splunk_query(query: str) -> str:
    """Format a Splunk query for better readability"""
    
    # Add proper spacing around pipes
    query = re.sub(r'\s*\|\s*', ' | ', query)
    
    # Format common commands on new lines for complex queries
    if len(query) > 100:
        query = re.sub(r'\s*\|\s*', '\n| ', query)
    
    return query.strip()


def generate_cache_key(text: str) -> str:
    """Generate a cache key for a query request"""
    
    # Normalize text
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    
    # Generate hash
    return hashlib.md5(normalized.encode()).hexdigest()


def parse_splunk_fields(text: str) -> List[str]:
    """Parse field names from natural language text"""
    
    field_patterns = [
        r'by\s+(\w+)',
        r'group\s+by\s+(\w+)',
        r'(\w+)\s+field',
        r'field\s+(\w+)',
    ]
    
    fields = []
    for pattern in field_patterns:
        matches = re.findall(pattern, text.lower())
        fields.extend(matches)
    
    return list(set(fields))  # Remove duplicates
```

### tests/test_bot.py
```python
"""Tests for Slack bot functionality"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.bot.slack_bot import SplunkBot
from src.bot.handlers import MessageHandler, CommandHandler
from src.utils.config import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    settings = Settings()
    settings.slack_bot_token = "xoxb-test-token"
    settings.slack_signing_secret = "test-secret"
    settings.google_api_key = "test-api-key"
    return settings


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client for testing"""
    client = AsyncMock()
    client.generate_splunk_query.return_value = {
        "query": "index=main | head 10",
        "explanation": "This query searches the main index and returns the first 10 results",
        "suggestions": ["Add time range for better performance"]
    }
    return client


@pytest.mark.asyncio
async def test_message_handler_splunk_mention(mock_gemini_client):
    """Test handling of Splunk mentions"""
    
    handler = MessageHandler(mock_gemini_client)
    
    message = {
        "text": "show me splunk errors from last hour",
        "user": "U123456",
        "channel": "C123456"
    }
    
    say_mock = AsyncMock()
    context_mock = MagicMock()
    
    await handler.handle_splunk_mention(message, say_mock, context_mock)
    
    # Verify Gemini client was called
    mock_gemini_client.generate_splunk_query.assert_called_once()
    
    # Verify response was sent
    assert say_mock.call_count == 2  # Initial message + final response


@pytest.mark.asyncio
async def test_command_handler_splunk_command(mock_gemini_client):
    """Test handling of /splunk command"""
    
    handler = CommandHandler(mock_gemini_client)
    
    command = {
        "text": "failed login attempts",
        "user_id": "U123456",
        "channel_id": "C123456"
    }
    
    ack_mock = AsyncMock()
    respond_mock = AsyncMock()
    context_mock = MagicMock()
    
    await handler.handle_splunk_command(ack_mock, respond_mock, command, context_mock)
    
    # Verify command was acknowledged
    ack_mock.assert_called_once()
    
    # Verify Gemini client was called
    mock_gemini_client.generate_splunk_query.assert_called_once()
    
    # Verify response was sent
    assert respond_mock.call_count == 2  # Initial + final response


@pytest.mark.asyncio
async def test_help_command(mock_gemini_client):
    """Test handling of /splunk-help command"""
    
    handler = CommandHandler(mock_gemini_client)
    
    command = {}
    ack_mock = AsyncMock()
    respond_mock = AsyncMock()
    
    await handler.handle_help_command(ack_mock, respond_mock, command)
    
    # Verify command was acknowledged
    ack_mock.assert_called_once()
    
    # Verify help text was sent
    respond_mock.assert_called_once()
    help_text = respond_mock.call_args[0][0]
    assert "Splunk Query Generator Bot Help" in help_text
```

### tests/test_gemini.py
```python
"""Tests for Gemini LLM client"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.llm.gemini_client import GeminiClient
from src.utils.config import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    settings = Settings()
    settings.google_api_key = "test-api-key"
    settings.gemini_model = "gemini-1.5-flash"
    settings.max_query_length = 1000
    return settings


@pytest.fixture
def gemini_client(mock_settings):
    """Create Gemini client for testing"""
    with patch('google.generativeai.configure'):
        with patch('google.generativeai.GenerativeModel'):
            return GeminiClient(mock_settings)


@pytest.mark.asyncio
async def test_generate_splunk_query_success(gemini_client):
    """Test successful query generation"""
    
    # Mock the model response
    mock_response = MagicMock()
    mock_response.text = '''
    {
        "query": "index=security action=failure earliest=-1h | stats count by user",
        "explanation": "This query searches for failed actions in the security index within the last hour",
        "suggestions": ["Consider adding source IP analysis"]
    }
    '''
    
    gemini_client.model.generate_content_async = AsyncMock(return_value=mock_response)
    
    result = await gemini_client.generate_splunk_query("show me failed logins last hour")
    
    assert "query" in result
    assert "explanation" in result
    assert "suggestions" in result
    assert "index=security" in result["query"]


@pytest.mark.asyncio
async def test_generate_splunk_query_parsing_fallback(gemini_client):
    """Test query generation with text parsing fallback"""
    
    # Mock the model response with non-JSON format
    mock_response = MagicMock()
    mock_response.text = '''
    QUERY:
    index=main earliest=-24h | head 10
    
    EXPLANATION:
    This is a basic query to get recent events
    
    SUGGESTIONS:
    - Add specific sourcetype
    - Include field filtering
    '''
    
    gemini_client.model.generate_content_async = AsyncMock(return_value=mock_response)
    
    result = await gemini_client.generate_splunk_query("show me recent events")
    
    assert "query" in result
    assert "index=main" in result["query"]
    assert len(result["suggestions"]) == 2


@pytest.mark.asyncio
async def test_generate_splunk_query_error_handling(gemini_client):
    """Test error handling in query generation"""
    
    # Mock an exception
    gemini_client.model.generate_content_async = AsyncMock(side_effect=Exception("API Error"))
    
    with pytest.raises(Exception):
        await gemini_client.generate_splunk_query("test query")
```

### tests/test_validators.py
```python
"""Tests for query validators"""

import pytest

from src.llm.query_validator import SplunkQueryValidator


@pytest.fixture
def validator():
    """Create validator instance"""
    return SplunkQueryValidator()


def test_validate_empty_query(validator):
    """Test validation of empty query"""
    
    result = validator.validate_query("")
    
    assert not result["is_valid"]
    assert "empty" in result["errors"][0].lower()


def test_validate_dangerous_command(validator):
    """Test validation of dangerous commands"""
    
    result = validator.validate_query("index=main | delete")
    
    assert not result["is_valid"]
    assert any("delete" in error.lower() for error in result["errors"])


def test_validate_safe_query(validator):
    """Test validation of safe query"""
    
    result = validator.validate_query("index=main earliest=-1h | stats count by host")
    
    assert result["is_valid"]
    assert len(result["errors"]) == 0


def test_validate_query_warnings(validator):
    """Test validation warnings"""
    
    result = validator.validate_query("index=* earliest=0 | head 100")
    
    assert result["is_valid"]  # Valid but has warnings
    assert len(result["warnings"]) > 0
    assert any("slow" in warning.lower() for warning in result["warnings"])


def test_suggest_optimizations(validator):
    """Test optimization suggestions"""
    
    suggestions = validator.suggest_optimizations("search error | head 10")
    
    assert len(suggestions) > 0
    assert any("index" in suggestion.lower() for suggestion in suggestions)
    assert any("time" in suggestion.lower() for suggestion in suggestions)
```

### deployment/Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Run application
CMD ["python", "-m", "src.app"]
```

### deployment/docker-compose.yml
```yaml
version: '3.8'

services:
  splunk-bot:
    build: .
    ports:
      - "3000:3000"
    environment:
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
      - SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/splunkbot
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=splunkbot
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### deployment/kubernetes/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: splunk-bot
  labels:
    app: splunk-bot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: splunk-bot
  template:
    metadata:
      labels:
        app: splunk-bot
    spec:
      containers:
      - name: splunk-bot
        image: splunk-bot:latest
        ports:
        - containerPort: 3000
        env:
        - name: SLACK_BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: splunk-bot-secrets
              key: slack-bot-token
        - name: SLACK_SIGNING_SECRET
          valueFrom:
            secretKeyRef:
              name: splunk-bot-secrets
              key: slack-signing-secret
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: splunk-bot-secrets
              key: google-api-key
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: splunk-bot-config
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### .env.example
```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Google Gemini Configuration
GOOGLE_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Application Configuration
PORT=3000
LOG_LEVEL=INFO
DEBUG=false
MAX_QUERY_LENGTH=1000
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Database Configuration
DATABASE_URL=sqlite:///bot_analytics.db

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn-here
```

### requirements-dev.txt
```txt
# Development dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0
mypy==1.7.1
pre-commit==3.5.0
bandit==1.7.5
safety==2.3.5
```

## Usage Examples

### Basic Usage
```
@SplunkBot show me failed login attempts in the last 24 hours
```

### Slash Commands
```
/splunk errors in web application logs
/splunk-help
```

### Advanced Queries
```
@SplunkBot find top 10 source IPs by traffic volume this week
@SplunkBot show me performance metrics for database queries
@SplunkBot search for suspicious network activity in firewall logs
```

## API Documentation

### Health Check
```
GET /health
```
Returns the health status of the application.

### Slack Events
```
POST /slack/events
```
Handles incoming Slack events (messages, mentions, etc.).

### Slack Commands
```
POST /slack/commands
```
Handles Slack slash commands.

## Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your values

# Run the application
python -m src.app
```

### Docker Deployment
```bash
# Build image
docker build -t splunk-bot .

# Run with Docker Compose
docker-compose up -d
```

### Kubernetes Deployment
```bash
# Create secrets
kubectl create secret generic splunk-bot-secrets \
  --from-literal=slack-bot-token=your-token \
  --from-literal=slack-signing-secret=your-secret \
  --from-literal=google-api-key=your-api-key

# Create config map
kubectl create configmap splunk-bot-config \
  --from-literal=database-url=your-db-url

# Deploy
kubectl apply -f deployment/kubernetes/
```

## Troubleshooting

### Common Issues

1. **Slack Events Not Received**
   - Check webhook URL configuration
   - Verify signing secret
   - Ensure proper permissions

2. **Gemini API Errors**
   - Verify API key is valid
   - Check quota limits
   - Review request format

3. **Database Connection Issues**
   - Verify database URL
   - Check connection permissions
   - Ensure database is running

### Logging

Logs are structured JSON and include:
- Request/response details
- Error information
- Performance metrics
- User interaction data

### Monitoring

Set up monitoring with:
- Health check endpoint
- Application metrics
- Error tracking (Sentry)
- Database performance

## Security Considerations

- Store all secrets in environment variables
- Use HTTPS for all external communications
- Implement rate limiting
- Validate and sanitize all inputs
- Regular security updates
- Monitor for suspicious activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup
```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Check code style
black src/ tests/
flake8 src/ tests/

# Type checking
mypy src/
```