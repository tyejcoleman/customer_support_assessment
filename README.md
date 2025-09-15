# Customer Support AI Agent - Interview Challenge

## Overview
Build a customer support chatbot using the OpenAI Agents Python framework that can answer questions using a knowledge base and escalate to human agents when necessary.

## Challenge Objectives
We are evaluating your ability to:
1. **Integrate AI frameworks** - Work with the OpenAI Agents Python SDK
2. **Prompt Engineering** - Craft effective prompts that ensure the agent behaves correctly
3. **Tool Integration** - Implement RAG with vector stores and custom tools
4. **Decision Logic** - Design clear escalation criteria for human handoff
5. **User Experience** - Create a functional CLI interface

## Technical Requirements

### Prerequisites
- Python 3.8+
- OpenAI API key with access to GPT-4
- Pre-configured vector store ID containing FAQ/knowledge base

### SDK Documentation
OpenAI Agents Python SDK: https://openai.github.io/openai-agents-python/

### Core Requirements

#### 1. Human Handoff System
**MUST trigger escalation when:**
- User explicitly requests to speak to a human/representative/agent
- User says phrases like "talk to someone", "real person", "human help"
- Any billing or refund issues arise
- Security or account access concerns

**Handoff behavior:**
- Display clear CLI notification when triggered
- Include reason for escalation
- Log the handoff event

#### 2. FAQ RAG Search System
**Knowledge Base behavior:**
- MUST search the FAQ (sample_faq.json) for EVERY customer question
- If information IS found: Return the exact answer from the FAQ
- If information IS NOT found: Return a response like "I'm sorry, I don't have information about that in my knowledge base. Would you like to speak with a human representative?"
- NEVER make up or hallucinate information not in the FAQ

#### 3. Agent Response Rules
- **Found in FAQ**: Provide exact answer from knowledge base
- **Not in FAQ**: Apologize and offer human assistance
- **Human requested**: Immediately escalate without trying to answer
- **Multiple questions**: Answer what's in FAQ, escalate for what's not

## What We Provide
- `main.py` - Starter template with:
  - Complete CLI implementation
  - Environment variable loading
  - Error handling and logging
  - Session management
  - TODOs marking where to implement agent logic

- `.env.example` - Template for required environment variables
- `requirements.txt` - Required dependencies

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and vector store ID
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Testing Your Solution
See `test_queries.md` for sample queries and expected behaviors to validate your implementation.

## Tips for Success

### AI Development Assistance
- **You may use AI tools** (ChatGPT, Claude, Copilot) to help with development
- We're interested in HOW you use AI - your prompting strategy matters
- Document any AI assistance used in comments

### Prompt Engineering Best Practices
1. **Be Specific**: Vague instructions lead to inconsistent behavior
2. **Prioritize**: Put most important instructions first
3. **Test Iteratively**: Refine based on actual agent responses
4. **Consider Context**: Think about conversation flow and state

### Common Pitfalls to Avoid
- Agent answering without searching knowledge base
- Escalating too frequently or not when needed
- Losing conversation context on errors
- Not handling edge cases (empty responses, API failures)


Good luck! We're excited to see your approach to building an effective AI customer support agent.
