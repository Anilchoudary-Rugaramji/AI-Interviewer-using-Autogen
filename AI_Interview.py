from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
import os
import asyncio

load_dotenv()


async def team_Config(job_ppistion="Software Engineer"):
    
    api_key = os.getenv("OPENAI_API_KEY")


    model_client = OpenAIChatCompletionClient(model="gpt-4o",
                                            api_key=api_key)


    # Defining the agents
    # 1. Intervierer Agent
    # 2. candidate Agent
    # 3. Career coach Agent

    job_position = "Software Engineer"

    interviewer_agent = AssistantAgent(
        name="interviewer",
        model_client=model_client,
        system_message=f"""You are a professional interviewer for a {job_position} position. 
        Ask one clear question at a time. And wait for user to respond. 
        Ask five questions in total covering technical skills and experience, problem solving
        abilities and cultural fit. 
        You job is to ask question. and dont focus on response from career coach.
        After asking 5 questions, say "TERMINATE" at the end of the interview.
        """
    )

    candidate_agent = UserProxyAgent(
        name="interviewee",
        input_func=input
    )

    career_coach = AssistantAgent(
        name="career_coach",
        model_client=model_client,
        description=f"""An AI agent that provides feedback and advice to candidates for a 
        {job_position} position""",
        system_message=f"""You are a career coach specializing in preparing candidates
        for {job_position} position interviews. Provide constructive feedback on 
        candidates' responses and suggest improvements. After the interview,
        summarize the candidate's performance and provide actionable advice.
        """
    )

    team = RoundRobinGroupChat(
        participants=[interviewer_agent, candidate_agent, career_coach],
        max_turns=20,
        termination_condition=TextMentionTermination(text="TERMINATE")
    )
    return team



async def interview(team):
    async for message in team.run_stream(task="Start the interview with the first question"):
        message = message.content
        yield message
