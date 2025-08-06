from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


model_client = OpenAIChatCompletionClient(model="gpt-4o",
                                          api_key=api_key)


# Defining the agents
# 1. Intervierer Agent
# 2. candidate Agent
# 3. Career coach Agent

job_position = "Softare Engineer"

interviewer_agent = AssistantAgent(
    name="interviewer",
    model_client=model_client,
    system_message=f"""You are an professional interviwerfor a {job_position} position. 
    Ask one clear question at a time. And wait for user to respond. 
    Ask five questions in total covering technical skills and experience, problem solving
    abilities and cultural fit. 
    After asking 5 questions, say "TERMINATE" at the end of the interview.
    """
)

candidate_agent = UserProxyAgent(
    name="interviewee",
    input_func=input
)

career_coach = AssistantAgent(
    name="career coach",
    model_client=model_client,
    description="""An AI agent the provides feedback and advice to candidates for a 
    {job_position} position""",
    system_message="""You are an career coach specilising in preparing the candidates
      for the  {job_position} position interviews. Provide constructive feddback on 
      candidates  responses  and suggest improvements. After the interview.
      After the interview summarize candidates performance and provide actionable advice.
    """
)

+
