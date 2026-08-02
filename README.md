# Python AI Tutor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange?logo=google&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-green)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-yellow)
![Status](https://img.shields.io/badge/Status-In%20Development-brightgreen)

A command-line AI tutor built with Google's Gemini API. It's not just a chatbot — it can actually pick tools and use them, reason through multi-step problems, and build you a full learning roadmap for any goal you throw at it.

What this project actually does

You type something into the terminal, and depending on what you ask, one of three things happens:

Just chatting? Gemini answers you directly, like a tutor would.
Need something real-world? (weather, a search, a YouTube tutorial, a calculation) Gemini figures out which tool fits, Python runs it, and you get the actual result — not a guess.
Want a full plan? Type roadmap <your goal> and it builds you a 90-day learning roadmap from scratch.

There's also a ReAct-style agent in the code (think → act → observe → repeat until it has enough info to answer you) — it's built and working as its own piece, but it's not hooked up to the main chat yet. More on that below.

The three modes

1. Normal tutor mode This is the default. You ask, Gemini either answers directly or calls a tool (weather, search, calculator, YouTube, etc.), and it remembers what you talked about earlier in the conversation so follow-up questions actually make sense.

2. Roadmap mode Type roadmap learn web development and it runs through three steps behind the scenes:

figures out what skills you actually need
puts them in the right order to learn them
writes out a full 90-day plan based on that order

3. ReAct agent This one's the "smart researcher" — it thinks about what it needs, picks a tool, looks at the result, and keeps going until it's confident it can give you a complete answer. Right now it works as its own class in the code, but you'd need to call it directly (it's not wired into the terminal chat yet).

Tools it can actually use
Tool	What it does
Weather	Current weather for any city (OpenWeatherMap)
Web search	Looks stuff up online for you (Tavily)
YouTube search	Finds relevant tutorial videos
Date/time	Tells you the current time
Calculator	Does math on the fly
Skills lookup	Suggests skills for a career goal
Certifications	Suggests relevant certifications
Salary info	Gives you a rough salary range

Quick note: the skills/certifications/salary tools currently return the same fixed info no matter what goal you give them — they're placeholders for now, not pulling live data yet.

Getting it running
bash
# clone it
git clone https://github.com/your-username/ai-tutor.git
cd ai-tutor

# set up a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install what it needs
pip install -r requirements.txt

Then create a .env file in the project folder with your API keys:

env
Gemini_API_KEY=your_gemini_api_key
Weather_API_key=your_weather_api_key
tavily_search_api=your_tavily_api_key
Youtube_search=your_youtube_api_key

Don't commit that .env file — add it to .gitignore and keep your keys to yourself.

Running it
bash
python AI_tutor.py

Then just talk to it:

text
Ask AI tutor: What's the weather in Karachi?
Ask AI tutor: roadmap learn machine learning
Ask AI tutor: What is a binary search tree?
Ask AI tutor: exit

Type exit, quit, bye, or a handful of other variants to end the session.

How reliable is it?

It retries automatically if Gemini is overloaded or you hit a rate limit, and it won't crash the whole app if something goes wrong mid-conversation — you'll just get an error message and can try again. That said, this is a personal project built to learn, not something battle-tested for production use.

Stuff that's still rough around the edges

Being upfront about this instead of pretending it's all polished:

The ReAct agent isn't connected to the main chat loop yet — it works, but you have to call it directly in code
A couple of internal bugs in the ReAct loop still need fixing (how it decides it's "done," and how it passes info to tools)
The calculator uses Python's eval(), which works fine for personal use but isn't something you'd want exposed publicly
YouTube search currently only returns one video instead of several, due to a small loop bug
Model names used across the different agents aren't consistent — a cleanup pass is needed there
What's next
Hook the ReAct agent into the main chat
Fix the known bugs above
Make the skills/certs/salary tools pull real data instead of fixed answers
Split the code into separate files instead of one big script
Save conversations and roadmaps somewhere permanent
Maybe a simple web UI down the line
Why I built this

Mostly to actually learn how LLM agents work under the hood — real tool calling, a reasoning loop, and multi-step workflows — instead of just calling a chat API and calling it a day.

A couple of honest notes

You'll need your own API keys for Gemini, Tavily, OpenWeather, and YouTube for this to work. Since it leans on third-party services, results (especially search and weather) can vary or occasionally be slow/unavailable — that's on them, not the code.

License

No license file yet — add one (MIT works fine) if you want to open this up publicly.
