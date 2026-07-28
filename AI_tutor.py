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
            model= "gemini-2.5-flash",
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
            model="gemini-2.5-flash",
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
            model = "gemini-2.5-flash" ,
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
    

def Motivational_quotes():
    quotes = [
    "Discipline beats motivation.",
    "No pain, no gain.",
    "Success is earned, not given.",
    "Pain is temporary. Quitting lasts forever.",
    "Every expert was once a beginner.",
    "Talk is cheap. Show me the code.",
    "First, solve the problem. Then, write the code.",
    "Comfort is the enemy of progress.",
    "Consistency beats intensity.",
    "One bug at a time.",
    "Pressure creates diamonds.",
    "Stay hungry. Stay foolish.",
    "Dream big. Start small. Act now.",
    "Small improvements every day lead to big results.",
    "You become what you repeatedly do.",
    "The grind never lies.",
    "Build. Break. Learn. Repeat.",
    "Your only competition is who you were yesterday.",
    "Hard times create strong people.",
    "The best developers were once confused beginners.",
    "Your GitHub tells the story your résumé can't",
    "Discipline gets you to the gym. Consistency builds your body. Persistence writes the code. Time rewards them all",
    "Pain is temporary. Quitting lasts forever.",
    "Don't wish for it. Work for it.",
    "Train like a beast.",
    "Every workout counts.",
    "One more rep.",
    "One more problem.",
    "Success is earned, not given.",
    "One more day.",
    "Win the day.",
    "Stay disciplined.",
    "Trust the process.",
    "Never stop learning."
]
    return random.choice(quotes)

def generate_password(length : int):
    symbol = "AB`CD~EFGHI!JK@LM#NO$PQ%RS^TU&VW*XY(Za)bc+d9-e8=f7g6h5i4j321klmnopqrstuvwxyz"
    try:
        if length <=0:
            return "❌ length should not be less than or equal to zero"
        if length >=len(symbol):
            return f"❌ length shouldn't exceed the {len(symbol)}"
        password = "".join(random.sample(symbol,length))
        return password
    
    except Exception as e:
        return "Invalid. Enter the length in digit"
            

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
    client = TavilyClient(Token_Tavily)
    response = client.search(query)
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
    
def Generate_ROADMAP(topic):
    return f""""
    Roadmap for {topic}
    1. Learn Fundamental
    2. Practice Projects
    3. Build portfolio
    4. Apply for jobs
    """""
def get_skill(role:str):
    """""
    return the skills only required for role 
    Parameter: role(str) - career role selected by user
    Return: dict : Required skills 
    
    """
    return {
        "Role" : role,
        "skills": [
            "python" , "Machine learning" , "Data science" , "Deep learning" , "LLMS"
        ]
    }

def get_certificate(role:str):
    """""
    Returns certification info 
    Parameters: role(str): Career role 
    Returns:Dict
    """

    return {
            "role": role ,
            "certificates": [
                "Google Professional Machine Learning Engineer",
                "AWS Machine Learning Specialty"
                ]
            }

def get_salary(role:str):
    """""
    Returns expected salary range
    Parameters: role(str)
    Returns:Dict
    """

    return {
        "role": role,
        "salary": "$80,000 - $150,000 per year"
    }


#Register function 

TOOL = [
    get_certificate,
    get_skill,
    get_salary,
    get_weather,
    getDate_time,
    generate_password,
    get_web_searching,
    calculator,
    Motivational_quotes,
    get_youtubesearch,
]
TOOL_MAP = {
    "get_certificate": get_certificate,
    "get_skill": get_skill,
    "get_salary": get_salary,
    "get_weather": get_weather,
    "getDate_time": getDate_time,
    "generate_password": generate_password,
    "get_web_searching": get_web_searching,
    "calculator": calculator,
    "Motivational_quotes": Motivational_quotes,
    "get_youtubesearch":get_youtubesearch,
}

def Generate_with_retry(history):
    max_retry = 5
    for attempt in range(max_retry):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
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
                    wait_time = attempt ** attempt
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
def history_management(history,max_turns =10):
    turn_start_indices=[]
    for i in range(len(history)):
        msg = history[i]
        role = getattr(msg , "role" , None)
        if role=="user":
            turn_start_indices.append(i)

    if len(turn_start_indices)>max_turns:
        cutoff = turn_start_indices[-max_turns]
        history[:] = history[cutoff:]

def run_agent(history):

    MAX_TOOL_ROUNDS = 5

    for round_number in range(MAX_TOOL_ROUNDS):

        print(f"\nAgent round: {round_number+1}")

        response = Generate_with_retry(history)

        if response is None:
            return None

        function_calls = response.function_calls

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

    return "Maximum tool call limit reached."
        
def main():
    history = []
    Max_history =20
    print("="*50)
    print("AI tutor")
    print("="*50)
    while True:
        try:
            prompt = input("Ask AI tutor: ")
            if prompt.lower().strip() in ["bye","goodbye","exit","quit","q","stop","end","close","leave","terminate","finish","done",
                          "see you","see ya","farewell","exit()","quit()"]:
                 print("Goodbye")
                 break
            
            else:
                if prompt.lower().startswith("roadmap"):
                    goal = prompt[7:].strip()

                    if not goal:
                        print("Please provide goal")
                        continue

                    agent = AI_Agent_Roadmap(goal=goal)
                    agent.run()

                    print("\n" + "="*50)
                    print("Final roadmap")
                    print("="*50 , end="")
                    
                    
                    continue

            
                history.append(types.Content(role="user",
                                             parts= [types.Part.from_text(text=prompt)]))
                if len(history) > Max_history:
                    history = history[-Max_history:]

                start_time = time.time()

                AI_response = run_agent(history=history)
                print(f"\nAI tutor: ")
                print(AI_response)
            
                end_time = time.time() 
                total_time=round(end_time - start_time, 2)
                print(f"\nResponse time taken: {total_time} seconds")
            
        except Exception as e:
            print("AI tutor is unavailable temporary")
            print(e)




if __name__ == "__main__":
    main()