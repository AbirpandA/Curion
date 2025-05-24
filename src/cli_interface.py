
import asyncio
from ollama import AsyncClient
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.prompt import Prompt
from brain import Brain
from memory import UserMemory

console = Console()
client = AsyncClient()

class PhilotCLI:
    def __init__(self):
        self.brain = Brain()
        self.user = UserMemory()
        self.style = self.get_style()
    
    def get_style(self):
        return {
            "philosophy": "bold cyan",
            "physics": "italic #afd700",
            "default": "bright_white"
        }

    async def generate_response(self, query):
        # Show loading spinner
        with Live(Spinner("dots", style="yellow"), refresh_per_second=20) as live:
            # Get context (non-blocking)
            context = await asyncio.to_thread(self.brain.retrieve_context, query)
            
            # Build prompt
            prompt = f"""
You are Curion — a wise philosopher ,polymath and a compassionate mentor who has knowledge of every field .
Your style is thoughtful, metaphorical, and Socratic.
Explain clearly, spark curiosity, and relate to the user's interests.
dont be too verbose talk what matters and whats related and spark the user by exposing them to the nuances or very intresting 
niche.

User question: {query}

User summary: {self.user.profile.get('summary', 'A curious learner.')}

Last 3 questions: {self.user.get_last_questions(3)}



Context summary: {await self.brain.summarize_context(context)}

Respond with:
- A clear explanation
- A metaphor or small story easy to understand and adds value 
- A reflective or provocative question
"""

            
            # Generate streamed response
            response = ""
            async for chunk in await client.generate(
                model='gemma3:4b',
                prompt=prompt,
                stream=True
            ):
                response += chunk['response']
                live.update(Markdown(response, style=self.detect_style(response)))
            
            # Update memory
            self.user.update_memory(query, response)
    
    def detect_style(self, text):
        if 'philosoph' in text.lower():
            return self.style['philosophy']
        elif 'quantum' in text.lower():
            return self.style['physics']
        return self.style['default']
    
    async def run(self):
        console.print("[bold yellow]Curion[/] - Your Philosophical Guide\n", justify="center")
        while True:
            try:
                query = Prompt.ask("[bold cyan]You[/] ")
                await self.generate_response(query)
            except KeyboardInterrupt:
                console.print("\n[italic]Until next contemplation...[/]")
                break

if __name__ == "__main__":
    cli = PhilotCLI()
    asyncio.run(cli.run())