from AI_Interview import team_Config, interview
from autogen_agentchat.ui import Console
import asyncio


async def main():
    job_position = "Software Engineer"
    team = await team_Config(job_position)

    async for message in interview(team):
        print('-'*100)
        print(type(message))
        print(message)
        

if __name__ == "__main__":
        asyncio.run(main())
