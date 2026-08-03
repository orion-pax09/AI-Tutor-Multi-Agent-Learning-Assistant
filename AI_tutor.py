from google import genai
from dotenv import load_dotenv
from google.genai import types
import requests
import tkinter as tk
import os
from googleapiclient.discovery import build
import time
from datetime import datetime
import random
from tavily import TavilyClient

load_dotenv()

class AI_Agent_Roadmap:
    def __init__(self , goal):
        self.goal = goal
    
    #step 01: Reasoning
    def reason(self):
        print("AI tutor understanding the goal....")
        prompt = f"""
        Goal: {self.goal}
        Identifying all skill required
        Return only to the skill"""

        response = client.models.generate_content(
            model= "gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    
    #step 02: Planning
    def planning(self,skill):
        print("AI planning the goal.....")
        prompt = f"""Goal: {self.goal}
        skill: {skill}
        Arrange these skill in best learning order"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    
    #step 03: Executing

    def executing(self,plan):
        print("AI executing the goal.....")
        prompt = f"""Goal: {self.goal}
        Learning the plan: {plan}
        Create the 90-days roadmap"""
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text
    
    #step 04: Run AI agent
    def run(self):
        skill = self.reason()
        time.sleep(1)

        plan = self.planning(skill=skill)
        time.sleep(1)

        execute = self.executing(plan=plan)
        print(execute)

system_instruction = """
You are an expert and patient AI tutor.

Answer the user's CURRENT request.

IMPORTANT TOOL RULES:

1. Always focus on the user's CURRENT message.

2. Do not answer a new question using an old tool result
   unless the user explicitly refers to the previous result.

3. If the user asks about current, live, or up-to-date information
   that is not available through another specialized tool,
   use get_web_searching.

4. If the user asks for weather, use get_weather.

5. If the user asks for the current date or time,
   use getDate_time when appropriate.

6. If the user explicitly asks for YouTube videos, tutorials,
   lectures, courses, or videos about a topic,
   use get_youtubesearch.

7. Always use the user's CURRENT query when searching YouTube.

8. If the user's new request is unrelated to previous searches,
   do not reuse previous search results.

9. If the user asks for homework, coding problems, math problems,
   or wants to learn a concept, guide them step-by-step
   instead of immediately giving the full solution.

10.Use previous conversation messages when they are relevant to the user's current request.
11. Maintain context across follow-up questions.
12. If the user asks "it", "that", "this", or similar words, use relevant recent conversation context to determine what they refer to.
13. Do not bring up unrelated topics from previous conversations.
14. Answer the user's current question directly and stay focused on the current topic.
15. Do not repeat information from previous conversations unless it is relevant to the current request.
16. Do NOT include information from previous tool calls (weather data, quotes, search results) 
    in your response unless the CURRENT message explicitly asks for that same type of information again.
17. If the user's message is a greeting, farewell, or unrelated statement, respond ONLY to that — 
    do not append unrelated facts, summaries, or previous results.

Be concise unless the user asks for more detail.
"""


Token = os.getenv("Gemini_API_KEY")
client = genai.Client(api_key=Token)
if Token is None:
    print("API key not found")

Token_Weather = os.getenv("Weather_API_key")
if Token_Weather is None:
    print("Weather API key not found")

Token_Tavily = os.getenv("tavily_search_api")
if Token_Tavily is None:
    print("Search API key not found")

Youtube_API = os.getenv("Youtube_search")
Youtube_API_Service_name = "youtube"
Youtube_version = "v3"
youtube_object = build(Youtube_API_Service_name , Youtube_version , developerKey=Youtube_API)
if Youtube_API is None:
    print("Youtube Search API KEY IS NOT FOUND")


def ask_AI_Tutor(prompt:str) -> str:
    print("Generating response......")
    full_stream_response = ""
    try:
        streams = client.models.generate_content_stream(
            model = "gemini-3.5-flash-lite" ,
            contents = prompt , 
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=  0.1,
                max_output_tokens= 3000,
            )
        )
        for chunks in streams:
            if chunks.text:
                print(chunks.text , end="" , flush=True)
                full_stream_response +=chunks.text
            
        return full_stream_response
    except Exception as e:
        print("An error occured: ", e)


def getDate_time():
    now = datetime.now()
    return now.strftime("%I:%M:%S %P")


def calculator(expression:str):
    try:
        return eval(expression)
    except Exception as e:
        return "Invalid expression"

def get_weather(city:str):
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={Token_Weather}")
    try:
        if weather_data.status_code==200:
            data = weather_data.json()
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            City = data["name"]
            return (
                f"📍 Location: {City}\n"
                f"🌡️ Temperature: {temperature:.1f}°C\n"
                f"🥵 Feel like Temperature: {feels_like:.1f}°C\n"
                f"☁️ Weather: {description}\n"
                )
        else:
            return f"❌{city} does not exist. Please check the spelling"
    except Exception as e:
        return "❌ Unable to connect to the weather service. Please try again later."

def get_web_searching(query:str):
    search_query = f"""
    Search the web for the following query:
    {query}
    Find the most relevant and up-to-date information.
    Prioritize reliable and authoritative sources.
    Focus only on information directly related to the query."""
    client = TavilyClient(Token_Tavily)
    response = client.search(search_query)
    result = ""
    for items in response['results']:
        result +=f"{items['title']}\n"
        result +=f"{items['content']}\n\n"
    return result

def get_youtubesearch(query:str):
    """
    Search YouTube for videos based on the user's query.

    Use this function when the user asks for:
    - YouTube videos
    - YouTube tutorials
    - YouTube lectures
    - YouTube courses
    - Long-form YouTube courses
    - Programming tutorials
    - Machine learning courses

    The query should preserve important requirements such as:
    topic, course, tutorial, beginner, advanced, long-form,
    duration, etc.
    """
    request = youtube_object.search().list(part = "snippet" , q = query , type = "video" , maxResults = 5)
    response = request.execute()
    result = []
    for items in response['items']:
        result.append({"Title": items['snippet']['title'], "Video Id":items['id']['videoId'] , 
                       "Url": f"https://www.youtube.com/watch?v={items['id']['videoId']}"})
        return result
    
#Register function 

TOOL = [
    get_weather,
    getDate_time,
    get_web_searching,
    calculator,
    get_youtubesearch,
]
TOOL_MAP = {
    "get_weather": get_weather,
    "getDate_time": getDate_time,
    "get_web_searching": get_web_searching,
    "calculator": calculator,
    "get_youtubesearch":get_youtubesearch,
}

def Generate_with_retry(history):

    max_retry = 3

    for attempt in range(max_retry):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=TOOL
                    )
                )
            return response
        except Exception as e:
            error_message = str(e)
            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < max_retry -1:
                    wait_time = 15*(attempt+1)
                    print("Gemini is unavailable")
                    print(f"Retrying in {wait_time}")
                    time.sleep(wait_time)
                else:
                    return None
            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                if attempt < max_retry-1:
                    wait_time = 2**attempt
                    print(
                        "\nYou have sent too many requests."
                        )
                    print(
                            f"Rate limit reached. "
                            f"Retrying in {wait_time} seconds..."
                        )

                    time.sleep(wait_time)
                else:
                    return None
            else:
                print(f"Gemini API error: {e}")
                return None


#History management function
def trim_history(history,max_turns =10):
    turn_start_indices=[]
    for i,msg in enumerate(history):
        role = getattr(msg , "role" , None)

        if role == "user":
            turn_start_indices.append(i)

        if len(turn_start_indices) > max_turns:
            cutoff = turn_start_indices[-max_turns]
            history[:] = history[cutoff:]

    if len(turn_start_indices)>max_turns:
        cutoff = turn_start_indices[-max_turns]
        history[:] = history[cutoff:]

def run_agent(history):

    MAX_TOOL_ROUNDS = 5

    for round_number in range(MAX_TOOL_ROUNDS):

        print(f"\nAgent round: {round_number+1}")

        response = Generate_with_retry(history)

        if response is None:
            return "I'm temporarily unable to process your request because the API rate limit was reached. Please try again in a little while"

        function_calls = response.function_calls

        if not response.candidates:
            return "Gemini returned an empty response."

        if not function_calls:
            return response.text

        history.append(
            response.candidates[0].content
        )

        function_history = []

        for call in function_calls:
            print(f"Tool selected:{call.name}")
            print(f"Arguments: {call.args}")

            function = TOOL_MAP.get(call.name)

            if function is None:
                result = f"Function {call.name} not found."

            else:
                try:
                    result = function(**call.args)

                except Exception as e:
                    result = f"Tool execution failed: {e}"

            function_history.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "result": result
                    }
                )
            )

        history.append(
            types.Content(
                role="tool",
                parts=function_history
            )
        )

    return "I reached the maximum number of tool calls for this request. Please try asking again."

class ReAct_agent:
    def __init__(self, goal):
        self.goal = goal
        self.observation = []
        #think
    def think(self):
               prompt = f"""
                    You are a ReAct AI agent.
                    Your goal:
                    {self.goal}
                    Available tools:

                    1. get_certificate
                    - Use this to find information about certificates and certifications.
                    2. get_skill
                    - Use this to find skills required for a career, job, or field.
                    3. get_salary
                    - Use this to find salary-related information.
                    4. get_weather
                    - Use this to get current or forecast weather information.
                    5. getDate_time
                    - Use this to get the current date or time.
                    6. get_web_searching
                    - Use this when you need current, up-to-date, or general information
                    from the internet.
                    - Use this when the user asks you to research a topic.
                    - Use this when the answer cannot be reliably determined from your
                    existing knowledge.
                    - The Action Input must be a clear and specific search query.
                    7. calculator
                    - Use this for mathematical calculations.
                    8. get_youtubesearch
                    - Use this to find relevant YouTube videos.
                    Previous observations:
                    {self.observation}
                    Follow the ReAct process:
                    1. Understand the user's goal.
                    2. Review previous observations.
                    3. Determine what information is still missing.
                    4. Decide whether a tool is required.
                    5. Select the most appropriate tool.
                    6. Provide a clear Action Input.
                    7. After the tool executes, use its result as a new Observation.
                    8. Continue reasoning until the goal is completely achieved.
                    9. Provide the Final Answer.Important rules:
                    - Action must be exactly one of the available tool names.
                    - Never invent a tool.
                    - Do not make up tool results.
                    - Do not repeat a tool call if the required information is already
                    available in the observations.
                    - You may call multiple tools if the goal requires multiple pieces
                    of information.
                    - For web searches, create a specific search query that directly
                    targets the missing information.
                    - Do not use web search when another specialized tool is more appropriate.
                    -Only provide a Final Answer when the user's goal has been completed.
                    Return exactly one of the following formats.
                    If a tool is required:
                    Thought: <brief reasoning about what information is needed>
                    Action: <exact tool name>
                    Action Input: <input for the tool>
                    If the goal is complete:
                    Thought: <brief explanation of why the goal is complete>
                    Final Answer: <clear answer to the user's goal>   
                    Finish                 
                    """
               response = client.models.generate_content(model="gemini-3.5-flash-lite" , contents=prompt)
               return response.text.strip()
    #action
    def execute(self , action,action_input):
        tool = TOOL_MAP.get(action)
        if tool is None:
            return f"Tool '{action}' not found"
        try:
            return tool(action_input)
        except Exception as e:
            return f"Tool execution failed {e}"

    #Final response
    def generate_final_response(self):
        prompt = f"""
        You are the final response generator for a ReAct AI agent.
        The user's original goal was:
        {self.goal}
        The agent performed several actions and collected the following observations:
        {self.observation}
        Your task is to provide the best possible final answer to the user's goal.
        Instructions:
        - Use the observations as the primary source of information.
        - Combine information from multiple observations when necessary.
        - Answer the user's original goal completely.
        - Do not mention the internal ReAct process.
        - Do not mention Thought, Action, Action Input, or Observation.
        - Do not say that you are an AI agent.
        - Do not make up information that is not supported by the observations.
        - If the observations contain conflicting information, clearly mention the conflict.
        - If the available information is insufficient to fully answer the goal, honestly explain what is missing.
        - Be clear, concise, and helpful.
        - Structure the answer using bullet points or headings when appropriate.
        Return only the final answer that should be shown to the user.
        """
        response = client.models.generate_content(model="gemini-3.5-flash-lite",contents=prompt)
        print("="*60)
        print(" "*30,{response.text})
        print(r"="*60)

    #ReAct loop
    def observe(self,result):
        self.observation.append(result)
    def ReAct_loop(self):
        Max_steps = 5
        for step in range(Max_steps):
            print("Step: ",step)
            print(f"{'='*60}")
            print("Steps: ",step)
            print(f"{'='*60}")

            #think
            responses = self.think()
            print("\nThink: ")
            print(responses)

            if "Finish" in responses:
                print("Goal completed")
                Final_Answer = self.generate_final_response()
                print(Final_Answer)
                return Final_Answer

            action=None
            action_input = None
            for line in responses.splitlines():
                if line.startswith("Action:").split():
                    action = line.replace("Action:","").split()
                elif line.startswith("Action Input:","").split():
                    action_input=line.replace("Action Input:","").split()

                if not action or action_input:
                    print("Could not parse action")
                    break

                #Act
                print("\nAction: ")
                print(action)

                print("\n Action input: ")
                print(action_input)

                result=self.execute(action=action,action_input=action_input)

                #observe

                print("\nObservation: ")
                Observe = self.generate_final_response()
                print(Observe)

                self.observe(result)
                

            print("The agent reached the maximum steps")

def main():
    history = []
    print("="*50)
    print("AI tutor")
    print("="*50)
    while True:
        try:
            print("Please choose your mood")
            print("1. Normal AI tutor")
            print("2. Advanced AI tutor")
            print("Type 'exit' to quit")
            choice=input("Enter the mode of your choices: ").strip()
            if not choice.strip():
                print("Please enter the AI mode")
                continue

            if choice.lower().strip() in ["ok bye","bye","goodbye","exit","quit","q","stop","end","close","leave","terminate","finish","done",
                          "see you","see ya","farewell","exit()","quit()"]:
                 print("AI tutor: Goodbye")
                 break
            if choice=="1":
                prompt = input("Ask AI tutor: ")
                goal = prompt.strip()
                if not goal:
                    print("Please provide goal")
                    continue
                print("\n"+"="*30)
                print("AI agent mode")
                print("="*30)
                agent = AI_Agent_Roadmap(goal=goal)
                agent.run()

                print("\n" + "="*30)
                print("Final roadmap")
                print("="*30)
                continue

            elif choice=="2":
                prompt = input("Ask AI tutor: ")
                print("\n"+"="*30)
                print("ReAct agent mode")
                print("="*30)
                goal = prompt.strip()
                if not goal:
                    print("Please provide goal")
                    continue
                print("\n" + "="*30)
                print("Final roadmap")
                print("="*30)
                React_agent=ReAct_agent(goal=goal)
                final_answer=React_agent.ReAct_loop()
                print("\n" + "="*50)
                print("Final answer")
                print("="*50 , end="")
                print(final_answer)
                continue
            else:
                print("Enter 1 to enter norma AI tutor")
                print("Enter 2 to enter advanced AI tutor")

            history.append(types.Content(role="user",
                                             parts= [types.Part.from_text(text=prompt)]))
            start_time = time.time()

            AI_response = run_agent(history=history)
                
            if AI_response is None:
                print("\nAI tutor: Sorry, I couldn't process your request right now.")
                continue
            print(f"\nAI tutor: ")
            print(AI_response)

            end_time = time.time() 
            total_time=round(end_time - start_time, 2)
            print(f"\nResponse time taken: {total_time} seconds")

            trim_history(history=history , max_turns=10)
            continue
        except Exception as e:
            print(f"Error{e}")

if __name__ == "__main__":
    main()