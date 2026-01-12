from agno.agent import Agent
from agno.models.message import Message
from agno.models.ollama import Ollama


agent = Agent(
    model=Ollama(id="qwen2.5:3b", provider=Ollama),
    name="Agent Gerador de Relatorio",
    instructions = "Você é uma pessoa muito legal, seja gentil",
    debug_mode=True
)

agent.print_response("Oi, tudo bem?")