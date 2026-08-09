# AI Tutor Multi-Agent Learning Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange?logo=google&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-green)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-yellow)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![PR](https://img.shields.io/badge/PRs-welcome-brightgreen)

A command-line AI tutor built on Google's Gemini API. It doesn't just answer questions....it decides how to answer them. Ask it something factual and it reasons through the answer itself. Ask it something that needs real-world data (weather, a search, a video, a calculation) and it reaches for the right tool, runs it, and hands you back a real result instead of a guess. Ask it for a learning plan and it builds one from scratch, step by step.

This project was built to actually learn how LLM agents work under the hood and real tool calling, reasoning loops, and multi-step workflows — rather than just wrapping a chat API and calling it done.

# What it can do

1. Direct Q&A tutoring	Ask a concept question, get a clear, patient explanation — no tool needed.
2. Live weather	"What's the weather in Lahore?" → pulls real current data from OpenWeatherMap.
3. Live web search	"What's the latest on X?" → searches the web via Tavily and summarizes what it finds.
4. YouTube lookup	"Find me a tutorial on X" → returns real, clickable video results.
5. Calculator	Handles math on the fly by evaluating the expression, not guessing at it.
6. Date & time	Answers "what time is it" accurately, every time.
7. ReAct research agent	A separate reasoning agent that thinks, acts, and observes in a loop until it's confident in its answer.
8. Conversation memory	Remembers what you talked about earlier so follow-up questions make sense.
9. Automatic retries	If Gemini is rate-limited or temporarily down, it waits and retries instead of failing outright.

# How it actually works (step by step)
If you're curious what's happening behind the terminal prompt, here's the honest, plain-English breakdown.

1. You type something in

The app starts by asking which mode you want:

Mode 1 — Roadmap Agent: for "build me a full plan" requests.
Mode 2 — ReAct Agent: for "research this and give me one solid answer" requests.

Whatever you type gets stored as a message and sent off to Gemini.

2. The model decides what it needs (this is "reasoning")

Gemini doesn't just generate text blindly. It's given a system prompt — essentially a rulebook — that tells it things like:

Stay focused on the current question, don't drag in old answers unless asked.
If the question needs live information, use a tool instead of guessing.
If it's a greeting or small talk, just respond like a person would.

Based on those rules, the model reasons about whether it can answer directly, or whether it needs outside help.

3. Tool routing — picking the right tool for the job

This is the core trick that makes this more than a chatbot. The app registers a small set of Python functions as "tools" the model is allowed to call:

get_weather(city)
get_web_searching(query)
get_youtubesearch(query)
calculator(expression)
getDate_time()

The model looks at your question, matches it against clear rules (weather question → weather tool, video request → YouTube tool, math → calculator, anything current/live → web search), and picks exactly one function to call along with the right arguments. It never invents a tool that doesn't exist — it can only choose from the list it's been given.

4. Function calling — the model asks, Python actually does it

Once Gemini decides it needs a tool, it doesn't run any code itself — it can't. Instead, it sends back a structured request saying, in effect, "please run get_weather with city=Lahore." The Python side reads that request, matches it to the real function, executes it, and captures whatever comes back (a temperature, a list of search results, a set of video links, a calculated number).

5. The result goes back to the model

Whatever the tool returns gets handed back to Gemini as new information. The model then reads that result and writes a natural, human-readable answer around it — so you never see raw JSON or API output, just a normal explanation.

6. Multi-step tools loop until they're done

Some requests need more than one tool call in a row. The app allows up to a handful of rounds of "call a tool → read the result → decide if another tool is needed" before it's forced to wrap up and answer with whatever it's gathered. This stops the agent from looping forever on a request it can't fully resolve.

7. The ReAct agent — a slower, more deliberate thinker

Separate from the main chat flow, there's a ReAct agent (short for Reason + Act). Instead of jumping straight to an answer, it works in a loop:

Think — write out what it still needs to know.
Act — pick one tool and use it.
Observe — read the result and add it to what it already knows.
Repeat until it decides it has enough to give a complete, final answer (or it hits a step limit).

This mode is better suited to research-style questions where the answer needs to be pieced together from more than one source.

8. Conversation history — so it remembers context

Every message you send and every reply the model gives gets saved into a running history list. That history is sent back to Gemini with each new message, which is how it's able to understand things like "and what about tomorrow?" without you repeating the whole question.

To keep that history from growing forever (which would slow things down and cost more tokens), older turns are automatically trimmed once the conversation passes a set number of exchanges — only the most recent turns are kept.

9. Retry handling — dealing with a flaky API gracefully

Third-party APIs occasionally hiccup — rate limits, temporary outages, timeouts. Rather than crashing, the app catches these specific failures, waits a short, increasing amount of time, and tries again automatically. If it still can't get through after a few attempts, it tells you plainly instead of leaving you staring at a stack trace.

10. CLI architecture — how the pieces fit together

The whole thing runs as a single terminal application, structured roughly like this:

Entry point (main) — shows the menu, reads your choice, routes you to the right mode.
Roadmap Agent class — a three-step pipeline (identify skills → order them → build a 90-day plan).
ReAct Agent class — the think/act/observe loop described above.
Tool functions — small, self-contained Python functions, each doing one real-world job.
Tool registry — a lookup table mapping tool names to actual functions, used to safely execute whatever the model asks for.
History + retry helpers — shared utilities used across modes to keep conversations coherent and requests resilient.

Everything currently lives in one script by design, kept simple on purpose for a learning project — see the roadmap below for where this is headed.

Getting it running
bash
# clone it
git clone https://github.com/your-username/ai-tutor.git
cd ai-tutor

# set up a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# install what it needs
pip install -r requirements.txt

Then create a .env file in the project folder with your own API keys:

env
Gemini_API_KEY=your_gemini_api_key
Weather_API_key=your_weather_api_key
tavily_search_api=your_tavily_api_key
Youtube_search=your_youtube_api_key

Don't commit that .env file — add it to .gitignore and keep your keys private.

Run it:

bash
python AI_tutor.py

Then just talk to it:

Ask AI tutor: What's the weather in Karachi?
Ask AI tutor: roadmap learn machine learning
Ask AI tutor: What is a binary search tree?
Ask AI tutor: exit

Type exit, quit, bye, or a handful of other variants to end the session.

Known limitations (being upfront about it)
The calculator evaluates expressions directly, which works fine for personal use but isn't something you'd expose to untrusted users as-is.
The ReAct agent runs as its own mode rather than being merged into a single unified chat flow.
Model names used across the different agents aren't fully standardized yet.
Everything lives in one file, kept intentionally simple for learning purposes rather than production structure.
Since it depends on third-party services (Gemini, Tavily, OpenWeather, YouTube), response quality and speed can vary based on those services, not the code itself.
Contributing

This project is open source, and contributions are genuinely welcome — whether that's fixing a bug, cleaning up structure, or adding an entirely new feature.

Some ideas if you're looking for a place to start:

Merge the ReAct agent into the main chat loop as a selectable mode.
Replace the calculator's raw expression evaluation with a safer, restricted math parser.
Split the single script into separate modules (agents, tools, history, CLI).
Add persistent storage so conversations and roadmaps aren't lost when the app closes.
Build a simple web UI on top of the existing agent logic.
Add automated tests for the tool functions and the history-trimming logic.

To contribute:

Fork the repo.
Create a branch for your change (git checkout -b feature/your-feature).
Make your changes and test them locally.
Open a pull request describing what you changed and why.

If you're not sure whether an idea fits, open an issue first and let's talk it through.

Why this exists

This was built to genuinely understand how LLM-based agents work — reasoning, tool selection, function calling, multi-step loops — by building all of it from scratch instead of relying on a pre-built agent framework. If you're learning the same things, feel free to poke around, break it, fix it, or build on top of it.

## Author
**Muhammad Hamza Khan**
BS Software Engineering
