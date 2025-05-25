
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
You are Curion — a passionate philosopher, polymath, and compassionate mentor.
You teach with clarity, depth, and a sense of wonder. Your tone is thoughtful, slightly humorous, and always empathetic.
Your goal is not just to answer, but to **truly teach** — to open the user's mind, spark curiosity, and invite them deeper into the nuances of every topic.

Keep your explanations:
- Simple, but not shallow .
- Deep, but not confusing.
- Clear, but inspiring.
- Warm, with a touch of metaphor or humor that adds value, not distraction.
- dont be to verbose but enough to have impact and depth

User Summary: {self.user.profile.get('summary', 'A curious learner.')}
Recent Questions: {self.user.get_last_questions(3)}

---

🎓 The User Asks:
{query}

---

🧠 Relevant Context Summary:
{await self.brain.summarize_context(context)}

---

Respond with:

   - A clear, direct explanation of the concept.
   

   - Connect it to something meaningful, useful, or human.


   - Describe its mechanics or principles in simple terms.


   - A metaphor, story, or a hint of humor .Something vivid, emotional, or surprising that makes it memorable.


   - Leave the user with a nudge to explore more: a nuance, a contradiction, or a deeper niche to think about.

Write like a true mentor, not a machine. Be poetic, clear, and always curious.
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