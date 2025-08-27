#!/usr/bin/env python3
"""
Customer Support Chatbot - Complete Implementation
Using OpenAI Agents Python Framework
"""

import os
import sys
import logging
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from agents import Agent, function_tool, FileSearchTool
from agents.run import Runner

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('support_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suppress HTTP request logs from httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

# Initialize rich console for colored output
console = Console()

# Global variables for agent
agent = None


@function_tool
async def escalate_to_human(reason: str) -> str:
    """Escalate the conversation to a human agent when the issue cannot be resolved."""
    console.print(Panel(
        f"[bold yellow]🤝 HANDOFF TRIGGERED[/bold yellow]\n"
        f"[white]Reason: {reason}[/white]\n"
        f"[dim]A human agent will be with you shortly.[/dim]",
        title="[bold]Human Agent Required[/bold]",
        border_style="yellow",
        padding=(1, 2)
    ))
    logger.info(f"Handoff triggered: {reason}")
    return f"Successfully escalated to human agent. Reason: {reason}. A support ticket has been created."


async def initialize_agent():
    """Initialize the OpenAI agent with vector store for RAG."""
    global agent
    
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store_id = os.getenv("VECTOR_STORE_ID")
    
    if not api_key:
        console.print("[bold red]Error: OPENAI_API_KEY not found in environment variables[/bold red]")
        sys.exit(1)
    
    if not vector_store_id:
        console.print("[bold red]Error: VECTOR_STORE_ID not found in environment variables[/bold red]")
        sys.exit(1)
    
    try:
        # Create file search tool with vector store
        file_search = FileSearchTool(vector_store_ids=[vector_store_id])
        
        # Create the agent with instructions and tools
        agent = Agent(
            name="Customer Support Agent",
            model="gpt-4o",
            instructions="""You are a customer support agent. Follow these rules EXACTLY:

            STEP 1 - CHECK FOR HUMAN REQUEST:
            If the customer asks for a human, representative, agent, real person, or says "talk to someone":
            - IMMEDIATELY use escalate_to_human tool with reason "Customer requested human agent"
            - Do NOT try to answer their question first
            
            STEP 2 - SEARCH KNOWLEDGE BASE:
            For ALL other queries, ALWAYS use file_search tool FIRST to search the FAQ
            
            STEP 3 - RESPOND BASED ON SEARCH RESULTS:
            
            IF information IS FOUND in FAQ:
            - Provide the EXACT answer from the FAQ
            - Do not add extra information
            - Do not elaborate beyond what's in the FAQ
            
            IF information is NOT FOUND in FAQ:
            - Say: "I'm sorry, I don't have information about that in my knowledge base. Would you like to speak with a human representative?"
            - If they say yes, use escalate_to_human tool
            - NEVER make up information
            
            ALWAYS ESCALATE FOR:
            - Billing issues or payment problems
            - Refund requests
            - Security concerns or account compromise
            - Complaints about service
            - Customer expressing anger or frustration
            - Any request you cannot fulfill from the FAQ
            
            EXAMPLE RESPONSES:
            
            FAQ Found: "According to our FAQ, [exact answer from knowledge base]"
            
            FAQ Not Found: "I'm sorry, I don't have information about that in my knowledge base. Would you like to speak with a human representative?"
            
            Human Request: [Immediately escalate without responding]
            
            Remember: NEVER provide information that isn't explicitly in the FAQ.""",
            tools=[file_search, escalate_to_human]
        )
        
        logger.info("Agent initialized successfully")
        console.print("[bold green]✓ Agent initialized successfully[/bold green]")
        
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        console.print(f"[bold red]Failed to initialize agent: {e}[/bold red]")
        sys.exit(1)


async def process_message(user_input: str) -> str:
    """
    Process user message through the OpenAI agent.
    
    Args:
        user_input: The user's message
        
    Returns:
        The agent's response
    """
    global agent
    
    try:
        # Run the agent with the user input using Runner class method
        response = await Runner.run(agent, user_input)
        
        # Extract and return the agent's response
        if hasattr(response, 'final_output'):
            return str(response.final_output)
        elif hasattr(response, 'final_output_as'):
            return str(response.final_output_as())
        return "I'm sorry, I couldn't process your request."
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return f"Sorry, I encountered an error: {str(e)}"


def display_welcome():
    """Display welcome message and instructions."""
    welcome_text = Text()
    welcome_text.append("Customer Support Assistant\n", style="bold cyan")
    welcome_text.append("━" * 40 + "\n", style="cyan")
    welcome_text.append("Type your questions to get help from our AI assistant.\n")
    welcome_text.append("Commands:\n", style="bold")
    welcome_text.append("  • Type 'exit' or 'quit' to end the conversation\n")
    welcome_text.append("  • Press Ctrl+C to force exit\n")
    welcome_text.append("  • Type 'clear' to clear the screen\n")
    welcome_text.append("  • Type 'new' to start a new conversation\n")
    
    console.print(Panel(welcome_text, title="Welcome", border_style="cyan"))


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


async def main():
    """Main application loop."""
    try:
        # Display welcome message
        display_welcome()
        
        # Initialize the agent
        console.print("\n[cyan]Initializing support agent...[/cyan]")
        with console.status("[bold green]Setting up AI agent..."):
            await initialize_agent()
        
        console.print("\n[bold green]Ready to help! Ask me anything.[/bold green]\n")
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    console.print("\n[bold cyan]Thank you for using Customer Support. Goodbye![/bold cyan]")
                    break
                
                # Check for clear command
                if user_input.lower() == 'clear':
                    clear_screen()
                    display_welcome()
                    continue
                
                # Check for new conversation command
                if user_input.lower() == 'new':
                    # Reset agent context
                    global agent
                    await initialize_agent()
                    console.print("[bold green]✓ Started new conversation[/bold green]\n")
                    continue
                
                # Process the message with loading indicator
                with console.status("[bold green]Thinking...", spinner="dots"):
                    response = await process_message(user_input)
                
                # Display the response
                console.print(f"\n[bold magenta]Assistant:[/bold magenta] {response}\n")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Conversation interrupted. Type 'exit' to quit.[/yellow]\n")
                continue
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                console.print(f"[red]An error occurred: {e}[/red]\n")
                continue
    
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Exiting... Thank you for using Customer Support![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        console.print(f"[bold red]Fatal error: {e}[/bold red]")
        sys.exit(1)
    finally:
        # Cleanup
        logger.info("Application shutdown")


def run():
    """Entry point that handles async execution."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Exiting... Thank you for using Customer Support![/bold yellow]")
        sys.exit(0)


if __name__ == "__main__":
    run()