from google import genai
from dotenv import load_dotenv
from google.genai import types
import requests
import os
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



system_instruction = "You are an expert and patient AI tutor. If the user asks for factual information, definitions, lists, or recommendations, answer directly and clearly." \
"If the user asks for homework, coding problems, math problems, or wants to learn a concept, guide them step-by-step instead of immediately giving the full solution." \
"Be concise unless the user asks for more detail."


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

def get_query(query , Conservational_context):
    WEB_KEYWORDS = [
    "latest",
    "today",
    "current",
    "news",
    "recent",
    "live",
    "score",
    "winner",
    "price",
    "release",
    "version",
    "documentation",
    "docs",
    "research",
    "paper",
    "api",
    "sport",
    "fifa",
    "game",
    "GTA"
    ]
    if "time" in query.lower():
        return getDate_time()
    elif "motivational" in query.lower() or "quotes".lower().strip() in query.lower():
        return Motivational_quotes()
    elif "generate password" in query.lower():
        return generate_password()
    elif "weather" in query.lower() or "city".lower().strip() in query.lower():
        return get_weather()
    elif any(keywords in query.lower() for keywords in WEB_KEYWORDS):
        return get_web_searching(query)
    else:
        return ask_AI_Tutor(Conservational_context)

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
TOOLS = [get_certificate , 
        get_skill , 
        get_salary ,
        get_weather , 
        getDate_time , 
        generate_password , 
        get_web_searching , 
        calculator,
        Motivational_quotes
        ]
def run_agent(history):

    while True:

        max_retry = 5
        for attempt in range(max_retry):
            try:
                # ---------------------------------
                # 1. Ask Gemini
                # ---------------------------------
                    response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        tools=TOOLS
                        )
                    )
                    break
            except Exception as e:

                error_message = str(e)

                if "503" in error_message or "UNAVAILABLE" in error_message:
                    if attempt < max_retry -1:
                        wait_time = attempt ** attempt

                        print("Gemini is unavailable")
                        print(f"Retrying in {wait_time}")

                        time.sleep(wait_time)
                    else:
                        
                        return (
                            "Sorry, Gemini is currently "
                            "experiencing high demand. "
                            "Please try again in a moment."
                        )
                elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                    if attempt < max_retry-1:
                        wait_time = attempt*(2**attempt)
                        print(
                            "\nYou have sent too many requests."
                        )

                        print(
                            f"Rate limit reached. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)
                    else:

                        return (
                            "Sorry, you have reached the API "
                            "rate limit. Please wait a little "
                            "before trying again."
                        )

                
                else:
                    return f"Gemini API error: {e}"

                

        # ---------------------------------
        # 2. Check if Gemini wants a tool
        # ---------------------------------

        function_calls = response.function_calls

        if not function_calls:
            return response.text

        # ---------------------------------
        # 3. Save Gemini's response
        # ---------------------------------

        history.append(
            response.candidates[0].content
        )

        # ---------------------------------
        # 4. Execute function calls
        # ---------------------------------

        function_history = []

        for call in function_calls:

            print(
                f"Calling function: {call.name}"
            )

            function = globals().get(
                call.name
            )

            if function is None:

                result = (
                    f"Function {call.name} "
                    f"not found"
                )

            else:

                result = function(
                    **call.args
                )

            # ---------------------------------
            # 5. Create function response
            # ---------------------------------

            function_history.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "results": result
                    }
                )
            )

        # ---------------------------------
        # 6. Send function results to Gemini
        # ---------------------------------

        history.append(
            types.Content(
                role="tool",
                parts=function_history
            )
        )
        
def main():
    history = []
    Max_history =20
    print("="*50)
    print("AI tutor")
    print("="*50)
    while True:
        try:
            prompt = input("Ask AI tutor: ")
            # Roadmap agent 
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
                    
                    # after running roadmap agent, skip normal query handling
                    
                    continue

                #Save user Query
            
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