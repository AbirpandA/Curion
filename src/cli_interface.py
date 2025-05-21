from textual.app import App,ComposeResult
from textual.containers import Container
from textual.widgets import Header,Input,RichLog
from ollama import AsyncClient
from brain import Brain
from memory import UserMemory




class curion(App):
    CSS = """
    RichLog {
        background: #010822;
        color: #a9b1d6;
        padding: 2;
    }
    Input {
        dock: bottom;
        background: #16161e;
    }
    """


    def __init__(self):
        super().__init__() 
        self.Ollama = AsyncClient()
        self.user = UserMemory()
        self.brain = Brain()



    def compose(self) ->ComposeResult:
        yield Header()
        yield RichLog(highlight=True,markup=True)
        yield Input(placeholder="Ask your philosophical question...") 
    async def on_input_submitted(self,message:Input.Submitted):
        rich_log=self.query_one(RichLog)
        rich_log.write(f'[bold cyan]You[/] {message.value}')

        context= self.brain.retrieve_context(message.value)

        prompt = f"""
You are Curion — a wise, curious philosopher and mentor.

Speak simply, but meaningfully. Use stories, metaphors, and questions to teach.

User: {message.value}

Their background: {self.user.profile}

Last conversations: {self.user.profile['conversation_history'][-3:]}

Context you know: {context}

Reply with:
- A clear answer or explanation
- A small analogy or image
- A thoughtful question to deepen curiosity
"""

        response= await self.Ollama.generate(
            model='mistral:latest',
            prompt=prompt,
            options={'temperature':0.6}
        )

        self.user.update_memory(message.value,response['response'])
        
        

        
        rich_log.write(f"[bold purple]Curion: {self.style_response(response['response'])}[/]")


    def style_response(self,text):
        if "philosophy" in text.lower():
            return f"[#89ddff]{text}[/]"
        elif "quantum" in text.lower():
            return f"[#c3e88d]{text}[/]"
        return text




if __name__ == "__main__":
    app = curion()
    app.run()