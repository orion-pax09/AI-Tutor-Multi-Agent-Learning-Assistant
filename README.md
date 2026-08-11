# AI Tutor Multi-Agent Learning Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange?logo=google&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-green)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-yellow)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![PR](https://img.shields.io/badge/PRs-welcome-brightgreen)

A command-line AI tutor built on Google's Gemini API. It doesn't just answer questions — it decides *how* to answer them. Ask it something factual and it reasons through the answer itself. Ask it something that needs real-world data (weather, a search, a video, a calculation) and it reaches for the right tool, runs it, and hands you back a real result instead of a guess. Ask it for a learning plan and it builds one from scratch, step by step.

## What it can do

# Feature & Description 
• Direct Q&A tutoring:- Ask a concept question, get a clear, patient explanation — no tool needed.
• Live weather:- "What's the weather in Lahore?" → pulls real current data from OpenWeatherMap. 
• Live web search:-"What's the latest on X?" → searches the web via Tavily and summarizes what it finds. 
• YouTube lookup:- "Find me a tutorial on X" → returns real, clickable video results. 
• Calculator:- Handles math on the fly by evaluating the expression, not guessing at it. 
• Date & time:- Answers "what time is it" accurately, every time. 
• ReAct research agent:- A separate reasoning agent that thinks, acts, and observes in a loop until it's confident in its answer. 
• Conversation memory:-  Remembers what you talked about earlier so follow-up questions make sense. 
• Automatic retries:- If Gemini is rate-limited or temporarily down, it waits and retries instead of failing outright. 

## Motivation

This project wasn't built to be another chat-API wrapper — it was built to actually understand how LLM agents work under the hood: real tool calling, reasoning loops, and multi-step workflows, built from scratch instead of relying on a pre-built agent framework.

If you're trying to learn the same things — how a model decides when to call a tool, how function calling actually works end-to-end, how a ReAct (Reason + Act) loop is structured, how conversation history and retries are managed — this repo is a working example you can read top to bottom, break, poke at, and build on. It's small enough to hold in your head, but it touches most of the concepts you'll need for bigger agent projects later.

If you're learning the same things, feel free to poke around, break it, fix it, or build on top of it.

## Quick Start

```bash
# clone it
git clone https://github.com/your-username/ai-tutor.git
cd ai-tutor

# set up a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# install what it needs
pip install -r requirements.txt
```

Create a `.env` file in the project folder with your own API keys:

```env
Gemini_API_KEY=your_gemini_api_key
Weather_API_key=your_weather_api_key
tavily_search_api=your_tavily_api_key
Youtube_search=your_youtube_api_key
```

> Don't commit that `.env` file — add it to `.gitignore` and keep your keys private.

Run it:

```bash
python AI_tutor.py
```

## Usage

Once it's running, just talk to it:

```
Ask AI tutor: What's the weather in Karachi?
Ask AI tutor: roadmap learn machine learning
Ask AI tutor: What is a binary search tree?
Ask AI tutor: exit
```

Type `exit`, `quit`, `bye`, or a handful of other variants to end the session.

### How it works, step by step

1. **You type something in.** The app asks which mode you want — Mode 1 (Roadmap Agent) for "build me a full plan" requests, or Mode 2 (ReAct Agent) for "research this and give me one solid answer" requests. Whatever you type gets stored as a message and sent off to Gemini.

2. **The model decides what it needs (reasoning).** Gemini is given a system prompt — essentially a rulebook — telling it things like: stay focused on the current question, use a tool instead of guessing when live information is needed, and respond like a person for greetings or small talk.

3. **Tool routing.** The app registers a small set of Python functions as tools the model can call: `get_weather(city)`, `get_web_searching(query)`, `get_youtubesearch(query)`, `calculator(expression)`, `getDate_time()`. The model matches your question against clear rules and picks exactly one function to call, along with the right arguments. It never invents a tool that doesn't exist.

4. **Function calling.** Once Gemini decides it needs a tool, it sends back a structured request — "please run `get_weather` with `city=Lahore`." The Python side reads that request, matches it to the real function, executes it, and captures whatever comes back.

5. **The result goes back to the model.** Gemini reads the tool's result and writes a natural, human-readable answer around it, so you never see raw JSON or API output.

6. **Multi-step tools loop until they're done.** Some requests need more than one tool call in a row. The app allows up to a handful of rounds of "call a tool → read the result → decide if another tool is needed" before it's forced to wrap up.

7. **The ReAct agent.** A separate, slower, more deliberate mode: Think (what's still needed) → Act (pick one tool) → Observe (read the result) → repeat until it decides it has enough for a complete answer, or it hits a step limit. Better suited to research-style questions where the answer needs to be pieced together from more than one source.

8. **Conversation history.** Every message and reply is saved into a running history list and sent back to Gemini with each new message, so follow-ups like "and what about tomorrow?" work without repeating the whole question. Older turns are automatically trimmed once the conversation passes a set number of exchanges.

9. **Retry handling.** Rate limits, temporary outages, and timeouts are caught automatically; the app waits a short, increasing amount of time and tries again. If it still can't get through after a few attempts, it tells you plainly instead of leaving you staring at a stack trace.

10. **CLI architecture.**
    - Entry point (`main`) — shows the menu, reads your choice, routes you to the right mode.
    - `AI_Agent_Roadmap` class — a three-step pipeline (identify skills → order them → build a 90-day plan).
    - `ReAct_agent` class — the think/act/observe loop.
    - Tool functions — small, self-contained Python functions, each doing one real-world job.
    - Tool registry (`TOOL_MAP`) — a lookup table mapping tool names to actual functions, used to safely execute whatever the model asks for.
    - History + retry helpers — shared utilities used across modes to keep conversations coherent and requests resilient.

Everything currently lives in one script by design — kept simple on purpose for a learning project.

### Known limitations (being upfront about it)

- The calculator evaluates expressions directly, which works fine for personal use but isn't something you'd expose to untrusted users as-is.
- The ReAct agent runs as its own mode rather than being merged into a single unified chat flow.
- Model names used across the different agents aren't fully standardized yet.
- Everything lives in one file, kept intentionally simple for learning purposes rather than production structure.
- Since it depends on third-party services (Gemini, Tavily, OpenWeather, YouTube), response quality and speed can vary based on those services, not the code itself.

## Contributing

This project is open source, and contributions are genuinely welcome — whether that's fixing a bug, cleaning up structure, or adding an entirely new feature. It's also a good project to contribute to if *you* want hands-on practice with how agent tool-calling works, since the codebase is small and every piece is readable in one sitting.

Some ideas if you're looking for a place to start:

- Merge the ReAct agent into the main chat loop as a selectable mode.
- Replace the calculator's raw expression evaluation with a safer, restricted math parser.
- Split the single script into separate modules (agents, tools, history, CLI).
- Add persistent storage so conversations and roadmaps aren't lost when the app closes.
- Build a simple web UI on top of the existing agent logic.
- Add automated tests for the tool functions and the history-trimming logic.

To contribute:

1. Fork the repo.
2. Create a branch for your change (`git checkout -b feature/your-feature`).
3. Make your changes and test them locally.
4. Open a pull request describing what you changed and why.

If you're not sure whether an idea fits, open an issue first and let's talk it through.

## Author

**Muhammad Hamza Khan**

Built with Python, Google Gemini, and various APIs.

:)
