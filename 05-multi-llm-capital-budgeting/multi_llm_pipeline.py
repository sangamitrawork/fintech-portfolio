"""Multi-LLM human-in-the-loop pipeline for a capital-budgeting task (group project).

API keys are read from environment variables; none are stored in this file.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install openai anthropic google-genai groq huggingface_hub --quiet
print("done")

import os
import time
import logging
from IPython.display import display, Markdown

# --- 1. Setup Conversation Manager ---
class ConversationManager:
    def __init__(self):
        self.histories = {}
    def add_message(self, provider, role, content):
        if provider not in self.histories: self.histories[provider] = []
        self.histories[provider].append({"role": role, "content": content})
    def get_history(self, provider):
        return self.histories.get(provider, [])

conv = ConversationManager()

# --- 2. Initialize Clients ---
clients = {}

# Check environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
HF_API_KEY = os.environ.get("HF_API_KEY")

# Initialize Gemini
if GEMINI_API_KEY:
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=GEMINI_API_KEY)
        print("Gemini Client Ready")
    except Exception as e:
        print(f"Gemini Init Error: {e}")

# Initialize HuggingFace (if available)
if HF_API_KEY:
    try:
        from huggingface_hub import InferenceClient
        clients["huggingface"] = InferenceClient(token=HF_API_KEY)
        print("HuggingFace Client Ready")
    except Exception as e:
        print(f"HuggingFace Init Error: {e}")

# --- 3. Define the 'ask' Function ---
DEFAULT_MODELS = {
    "gemini": "gemini-2.0-flash",
    "huggingface": "meta-llama/Llama-3.2-3B-Instruct",
    "openai": "gpt-4o"
}

def ask(prompt, provider="gemini", model=None, temperature=0.7):
    if provider not in clients:
        return f"Error: Provider '{provider}' not initialized (check API keys)."

    model = model or DEFAULT_MODELS.get(provider, "")
    conv.add_message(provider, "user", prompt)

    print(f"--- Asking {provider} ({model}) ---")

    try:
        if provider == "gemini":
            # Simple content generation
            response = clients["gemini"].models.generate_content(
                model=model,
                contents=prompt,
                config={"temperature": temperature}
            )
            return response.text

        elif provider == "huggingface":
            messages = [{"role": "user", "content": prompt}]
            response = clients["huggingface"].chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response.choices[0].message.content

    except Exception as e:
        return f"Error during generation: {e}"

print("Setup Complete: 'ask' function is ready.")

financial_prompt = """
[Role]
Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
[Context]
You are evaluating two significant investment opportunities for the upcoming fiscal year.
- WACC: 9% - Available Cash: $100 million - Project A (Emerging Market Expansion): $50M initial investment, steady 20% growth over 5 years.
- Project B (Disruptive R&D): $40M initial investment, 30% probability of failure, 70% success probability weighted against potential 50%+ growth.
[Task]
Perform a high-level financial analysis providing directional estimates (not exact calculations) for NPV and IRR implications. Using the "Atom of Thought" approach, strictly break down your reasoning into the following independent steps to ensure mathematical logic and prevent hallucinations:
Atom 1: Evaluate Project A's NPV and IRR directional implications against the 9% WACC hurdle rate.
Atom 2: Evaluate Project B's risk-adjusted NPV and IRR directional implications against the 9% WACC hurdle rate, explicitly accounting for the 30% failure risk.
Atom 3: Compare the capital efficiency of both projects based on their initial capital outlays ($50M vs $40M) relative to the $100M available cash.
[Format]
Return valid JSON only, no markdown. Use the exact following JSON structure:
{"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
"""

# Call the ask function. Ensure that the 'ask' function and clients are defined by running previous cells.
# We use temperature=0.2 to encourage strict JSON adherence.
print(ask(financial_prompt, provider="GEMINI_API_KEY", temperature=0.2))

import os
import time
import json
import datetime
import logging
from pathlib import Path
from IPython.display import display, Markdown

# --- 1. Setup Logging & Conversation Manager ---
# (Simplified for immediate execution)
class ConversationManager:
    def __init__(self):
        self.histories = {}
        self.system_prompts = {}
    def set_system(self, provider, system_prompt):
        self.system_prompts[provider] = system_prompt
    def add_message(self, provider, role, content):
        if provider not in self.histories: self.histories[provider] = []
        self.histories[provider].append({"role": role, "content": content})
    def get_history(self, provider):
        return self.histories.get(provider, [])

conv = ConversationManager()

# --- 2. Initialize Clients ---
clients = {}

# Try to grab keys from environment if they exist
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
HF_API_KEY = os.environ.get("HF_API_KEY")

# OpenAI
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        clients["openai"] = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e: print(f"OpenAI init failed: {e}")

# Gemini (using google-genai SDK as installed)
if GEMINI_API_KEY:
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e: print(f"Gemini init failed: {e}")

# HuggingFace
if HF_API_KEY:
    try:
        from huggingface_hub import InferenceClient
        clients["huggingface"] = InferenceClient(token=HF_API_KEY)
    except Exception as e: print(f"HF init failed: {e}")

print(f"Active clients: {list(clients.keys())}")

# --- 3. Define the 'ask' function ---
DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "gemini": "gemini-2.0-flash",
    "huggingface": "meta-llama/Llama-3.2-3B-Instruct"
}

def ask(prompt, provider="gemini", model=None, system=None, temperature=0.7):
    if provider not in clients:
        return f"Error: Provider '{provider}' not available."

    model = model or DEFAULT_MODELS.get(provider, "")
    print(f"\n--- Querying {provider.upper()}... ---")

    try:
        if provider == "gemini":
            # Using the simplified generate_content for the direct answer
            response = clients["gemini"].models.generate_content(
                model=model,
                contents=prompt,
                config={"temperature": temperature}
            )
            return response.text

        elif provider == "openai":
            messages = [{"role": "user", "content": prompt}]
            if system: messages.insert(0, {"role": "system", "content": system})
            response = clients["openai"].chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response.choices[0].message.content

        elif provider == "huggingface":
            messages = [{"role": "user", "content": prompt}]
            response = clients["huggingface"].chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"

# --- 4. Execute User's Prompt ---
user_prompt = """
[Role]
Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
[Context]
You are evaluating two significant investment opportunities for the upcoming fiscal year.
- WACC: 9% - Available Cash: $100 million - Project A (Emerging Market Expansion): $50M initial investment, steady 20% growth over 5 years.
- Project B (Disruptive R&D): $40M initial investment, 30% probability of failure, 70% success probability weighted against potential 50%+ growth.
[Task]
Perform a high-level financial analysis providing directional estimates (not exact calculations) for NPV and IRR implications. Using the "Atom of Thought" approach, strictly break down your reasoning into the following independent steps to ensure mathematical logic and prevent hallucinations:
Atom 1: Evaluate Project A's NPV and IRR directional implications against the 9% WACC hurdle rate.
Atom 2: Evaluate Project B's risk-adjusted NPV and IRR directional implications against the 9% WACC hurdle rate, explicitly accounting for the 30% failure risk.
Atom 3: Compare the capital efficiency of both projects based on their initial capital outlays ($50M vs $40M) relative to the $100M available cash.
[Format]
Return valid JSON only, no markdown. Use the exact following JSON structure:
{"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
"""

# We use a lower temperature for JSON tasks to ensure format adherence
result = ask(user_prompt, provider="gemini", temperature=0.2)
print(result)

import os
from getpass import getpass

print("Enter API keys (press Enter to skip):")
print()

# We need at least one key to proceed.
# If you are using Google Colab, you can also set these in the 'Secrets' tab on the left.

OPENAI_API_KEY    = getpass("OpenAI key: ") or ""
ANTHROPIC_API_KEY = getpass("Anthropic key: ") or ""
GEMINI_API_KEY    = getpass("Gemini key (free at aistudio.google.com): ") or ""
GROQ_API_KEY      = getpass("Groq key (free at console.groq.com): ") or ""
HF_API_KEY        = getpass("HuggingFace token (needs 'Inference Providers' permission): ") or ""

os.environ["OPENAI_API_KEY"]    = OPENAI_API_KEY
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["GEMINI_API_KEY"]    = GEMINI_API_KEY
os.environ["GROQ_API_KEY"]      = GROQ_API_KEY
os.environ["HF_API_KEY"]        = HF_API_KEY

configured = []
if OPENAI_API_KEY:    configured.append("OpenAI")
if ANTHROPIC_API_KEY: configured.append("Anthropic")
if GEMINI_API_KEY:    configured.append("Gemini")
if GROQ_API_KEY:      configured.append("Groq")
if HF_API_KEY:        configured.append("HuggingFace")

print(f"\nKeys entered for: {', '.join(configured) if configured else 'none'}")

import os
import sys
from google.colab import userdata

# --- 1. API Key Setup ---
# This block checks for keys in Colab Secrets (recommended) or Environment variables.

api_keys = {
    "gemini": None,
    "openai": None,
    "anthropic": None
}

# Try to get keys from Secrets (Userdata)
for provider in api_keys.keys():
    try:
        key_name = f"{provider.upper()}_API_KEY"
        api_keys[provider] = userdata.get(key_name)
    except Exception:
        # If not found in secrets, try os.environ or leave as None
        api_keys[provider] = os.environ.get(f"{provider.upper()}_API_KEY")

# Check what we found
print("API Keys Status:")
for provider, key in api_keys.items():
    status = "✅ Found" if key else "❌ Not Found (Add to Secrets)"
    print(f"  - {provider.title()}: {status}")

if not any(api_keys.values()):
    print("\n⚠️ WARNING: No API keys found. You need at least one key (e.g., GEMINI_API_KEY) in the Colab 'Secrets' tab (key icon on the left).")

import google.generativeai as genai
from openai import OpenAI
import anthropic

# --- 2. Initialize Clients ---
clients = {}

# Setup Gemini
if api_keys["gemini"]:
    genai.configure(api_key=api_keys["gemini"])
    clients["gemini"] = genai.GenerativeModel('gemini-2.0-flash')

# Setup OpenAI
if api_keys["openai"]:
    clients["openai"] = OpenAI(api_key=api_keys["openai"])

# Setup Anthropic
if api_keys["anthropic"]:
    clients["anthropic"] = anthropic.Anthropic(api_key=api_keys["anthropic"])

print(f"Clients initialized: {list(clients.keys())}")

import json

# --- 3. Define the 'ask' Function ---
def ask(prompt, provider="gemini", temperature=0.7, json_mode=False):
    """
    Sends a prompt to the specified provider and returns the text response.
    """
    if provider not in clients:
        return f"Error: Provider '{provider}' is not initialized. Please add the API key."

    print(f"Processing request with {provider.title()}... ")

    try:
        # --- Gemini ---
        if provider == "gemini":
            generation_config = {"temperature": temperature}
            if json_mode:
                generation_config["response_mime_type"] = "application/json"

            response = clients["gemini"].generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text

        # --- OpenAI ---
        elif provider == "openai":
            params = {
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
            if json_mode:
                params["response_format"] = {"type": "json_object"}

            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content

        # --- Anthropic ---
        elif provider == "anthropic":
            response = clients["anthropic"].messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.content[0].text

    except Exception as e:
        return f"Error calling API: {e}"

print("Function 'ask' is ready to use.")

import json
import time
import re
from IPython.display import display, JSON

# --- 4. Execute the Financial Analysis Task ---

financial_prompt = """
[Role]
Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
[Context]
You are evaluating two significant investment opportunities for the upcoming fiscal year.
- WACC: 9% - Available Cash: $100 million - Project A (Emerging Market Expansion): $50M initial investment, steady 20% growth over 5 years.
- Project B (Disruptive R&D): $40M initial investment, 30% probability of failure, 70% success probability weighted against potential 50%+ growth.
[Task]
Perform a high-level financial analysis providing directional estimates (not exact calculations) for NPV and IRR implications. Using the "Atom of Thought" approach, strictly break down your reasoning into the following independent steps to ensure mathematical logic and prevent hallucinations:
Atom 1: Evaluate Project A's NPV and IRR directional implications against the 9% WACC hurdle rate.
Atom 2: Evaluate Project B's risk-adjusted NPV and IRR directional implications against the 9% WACC hurdle rate, explicitly accounting for the 30% failure risk.
Atom 3: Compare the capital efficiency of both projects based on their initial capital outlays ($50M vs $40M) relative to the $100M available cash.
[Format]
Return valid JSON only, no markdown. Use the exact following JSON structure:
{"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
"""

# --- robust retry logic ---

def execute_with_retry(prompt, provider, max_retries=2):
    print(f"--- Starting Request to {provider} (Max Retries: {max_retries}) ---")

    for attempt in range(max_retries + 1):
        # We assume 'ask' is defined in previous cells
        result = ask(prompt, provider=provider, temperature=0.2, json_mode=True)

        # Check for API error strings
        if "Error" in result or "429" in result or "Quota" in result:
            if attempt < max_retries:
                # Try to parse wait time from error message, default to 30s
                wait_match = re.search(r"retry in (\d+\.?\d*)s", result)
                wait_time = float(wait_match.group(1)) + 10 if wait_match else 30

                print(f"\u26a0\ufe0f Attempt {attempt+1} hit Rate Limit. Waiting {wait_time:.1f}s before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"\u274c All {max_retries+1} attempts failed.")
                return None

        return result

# --- Simulation Data (Fallback) ---
# Used to ensure user sees the structure if API is exhausted
SIMULATED_JSON = {
    "Project_A_Analysis": {
        "NPV_Implication": "Positive. 20% growth > 9% WACC implies value creation. NPV likely > $0.",
        "IRR_Implication": "Likely > 9%. Steady high-growth cash flows suggest a healthy return."
    },
    "Project_B_Analysis": {
        "Risk_Adjusted_NPV": "Volatile/Lower. The 30% total loss probability heavily weights down the EV.",
        "Expected_IRR": "High nominal IRR, but risk-adjusted IRR may barely clear 9% hurdle."
    },
    "Capital_Efficiency_Comparison": "Project B ($40M) preserves more cash ($60M vs $50M) but with significantly higher risk profile."
}

# --- Execution Flow ---
if clients:
    active_provider = list(clients.keys())[0]

    # 1. Try Real API
    result = execute_with_retry(financial_prompt, active_provider)

    # 2. Process Result or Fallback
    if result and "Error" not in result:
        print("\n--- \u2705 Success! Raw Response ---\n", result)
        try:
            parsed = json.loads(result)
            print("\n--- Parsed JSON ---")
            display(JSON(parsed))
        except:
            print("Could not parse JSON.")

    else:
        print("\n" + "="*60)
        print("\u26a0\ufe0f API QUOTA EXHAUSTED. DISPLAYING SIMULATED ANALYSIS.")
        print("The API is currently blocking requests. Below is a sample output")
        print("demonstrating the expected JSON structure and logic.")
        print("="*60 + "\n")
        display(JSON(SIMULATED_JSON))
else:
    print("No active clients found. Please set an API Key in the first cell of this block.")

import os
from getpass import getpass
import json
from huggingface_hub import InferenceClient
from IPython.display import display, JSON

print("--- \u2699\uFE0F Universal Hugging Face Setup ---")

# 1. Clear old keys to prevent conflicts
if "HF_API_KEY" in os.environ: del os.environ["HF_API_KEY"]

# 2. Robust Token Entry
print("\u274C Previous attempts failed due to permissions.")
print("\u26A0\uFE0F PLEASE DO THIS:")
print("1. Go to https://huggingface.co/settings/tokens")
print("2. Create a new token and select **'Classic'** (Access Type: Read).")
print("   (Classic tokens work automatically. Fine-grained tokens need manual permission checkboxes.)")
print("3. Paste the token below.")

token = getpass("\nEnter HF Token (starts with hf_...): ").strip()
os.environ["HF_API_KEY"] = token

# 3. Smart Model Selection
# We will try a list of reliable free models until one connects.
candidates = [
    "meta-llama/Llama-3.2-3B-Instruct",
    "HuggingFaceH4/zephyr-7b-beta",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen2.5-72B-Instruct",
    "microsoft/Phi-3.5-mini-instruct"
]

active_client = None
working_model = ""

print("\nTesting models...")
for model in candidates:
    try:
        print(f"  - Attempting {model.split('/')[1]}...", end=" ")
        client = InferenceClient(token=token, model=model)
        # Tiny test request
        client.chat.completions.create(messages=[{"role":"user", "content":"hi"}], max_tokens=1)
        print("\u2705 Success!")
        active_client = client
        working_model = model
        break
    except Exception as e:
        print(f"\u274C Failed ({e})")

# 4. Run Analysis or Fail
if active_client:
    print(f"\n\u2728 Connected to {working_model}. Running Financial Analysis now...")

    financial_prompt = """
    [Role] Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
    [Context] You are evaluating two significant investment opportunities for the upcoming fiscal year.
    - WACC: 9% - Available Cash: $100 million - Project A: $50M initial, 20% growth. - Project B: $40M initial, 30% fail risk, 70% success/50% growth.
    [Task] Provide directional estimates for NPV/IRR. Use 'Atom of Thought' reasoning.
    [Format] Return valid JSON only: {"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
    """

    try:
        messages = [
            {"role": "system", "content": "You are a financial expert. Output strict JSON only."},
            {"role": "user", "content": financial_prompt}
        ]

        response = active_client.chat.completions.create(
            messages=messages,
            temperature=0.2,
            max_tokens=1000
        )

        result_text = response.choices[0].message.content

        # Parse JSON
        clean_result = result_text.replace("```json", "").replace("```", "").strip()
        if "{" in clean_result:
            clean_result = clean_result[clean_result.find("{"):clean_result.rfind("}")+1]

        print("\n--- Analysis Result ---")
        display(JSON(json.loads(clean_result)))

    except Exception as e:
        print(f"\nError during analysis: {e}")
        print("Raw output:", result_text)
else:
    print("\n\u26A0\uFE0F All models failed. Please verify your token is a 'Classic' token with Read permissions.")

import os
from getpass import getpass

print("Enter API keys (press Enter to skip):")
print()

# We need at least one key to proceed.
# If you are using Google Colab, you can also set these in the 'Secrets' tab on the left.

OPENAI_API_KEY    = getpass("OpenAI key: ") or ""
ANTHROPIC_API_KEY = getpass("Anthropic key: ") or ""
GEMINI_API_KEY    = getpass("Gemini key (free at aistudio.google.com): ") or ""
GROQ_API_KEY      = getpass("Groq key (free at console.groq.com): ") or ""
HF_API_KEY        = getpass("HuggingFace token (needs 'Inference Providers' permission): ") or ""

os.environ["OPENAI_API_KEY"]    = OPENAI_API_KEY
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["GEMINI_API_KEY"]    = GEMINI_API_KEY
os.environ["GROQ_API_KEY"]      = GROQ_API_KEY
os.environ["HF_API_KEY"]        = HF_API_KEY

configured = []
if OPENAI_API_KEY:    configured.append("OpenAI")
if ANTHROPIC_API_KEY: configured.append("Anthropic")
if GEMINI_API_KEY:    configured.append("Gemini")
if GROQ_API_KEY:      configured.append("Groq")
if HF_API_KEY:        configured.append("HuggingFace")

print(f"\nKeys entered for: {', '.join(configured) if configured else 'none'}")

# Re-initialize clients with the new keys
clients = {}

# OpenAI
if os.environ.get("OPENAI_API_KEY"):
    try:
        from openai import OpenAI
        clients["openai"] = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    except Exception as e: print(f"OpenAI init failed: {e}")

# Anthropic
if os.environ.get("ANTHROPIC_API_KEY"):
    try:
        import anthropic
        clients["anthropic"] = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    except Exception as e: print(f"Anthropic init failed: {e}")

# Gemini
if os.environ.get("GEMINI_API_KEY"):
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    except Exception as e: print(f"Gemini init failed: {e}")

# Groq
if os.environ.get("GROQ_API_KEY"):
    try:
        from groq import Groq
        clients["groq"] = Groq(api_key=os.environ["GROQ_API_KEY"])
    except Exception as e: print(f"Groq init failed: {e}")

# HuggingFace
if os.environ.get("HF_API_KEY"):
    try:
        from huggingface_hub import InferenceClient
        # Use Zephyr-7B by default for chat compatibility
        clients["huggingface"] = InferenceClient(token=os.environ["HF_API_KEY"], model="HuggingFaceH4/zephyr-7b-beta")
    except Exception as e: print(f"HuggingFace init failed: {e}")

print(f"Active clients: {list(clients.keys())}")

if "huggingface" in clients:
    financial_prompt = """
    [Role] Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
    [Context] You are evaluating two significant investment opportunities for the upcoming fiscal year.
    - WACC: 9% - Available Cash: $100 million - Project A: $50M initial, 20% growth. - Project B: $40M initial, 30% fail risk, 70% success/50% growth.
    [Task] Provide directional estimates for NPV/IRR. Use 'Atom of Thought' reasoning.
    [Format] Return valid JSON only: {"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
    """

    print("--- Running Analysis with Hugging Face (Zephyr 7B) ---")
    # Using the universal 'ask' function defined previously
    response = ask(financial_prompt, provider="huggingface", temperature=0.2)

    # Parse and display
    try:
        import json
        from IPython.display import display, JSON

        clean_result = response.replace("```json", "").replace("```", "").strip()
        if "{" in clean_result:
            clean_result = clean_result[clean_result.find("{"):clean_result.rfind("}")+1]

        print("\n--- Parsed JSON ---")
        display(JSON(json.loads(clean_result)))
    except Exception as e:
        print(f"\nRaw Output (Parse Error: {e}):\n{response}")
else:
    print("Hugging Face client not active. Please enter a token in the cell above.")

# Re-initialize clients with Smart Model Selection
import os
clients = {}
DEFAULT_MODELS = {}

# OpenAI
if os.environ.get("OPENAI_API_KEY"):
    try:
        from openai import OpenAI
        clients["openai"] = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        DEFAULT_MODELS["openai"] = "gpt-4o"
    except Exception as e: print(f"OpenAI init failed: {e}")

# Anthropic
if os.environ.get("ANTHROPIC_API_KEY"):
    try:
        import anthropic
        clients["anthropic"] = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        DEFAULT_MODELS["anthropic"] = "claude-3-opus-20240229"
    except Exception as e: print(f"Anthropic init failed: {e}")

# Gemini
if os.environ.get("GEMINI_API_KEY"):
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        DEFAULT_MODELS["gemini"] = "gemini-2.0-flash"
    except Exception as e: print(f"Gemini init failed: {e}")

# Groq
if os.environ.get("GROQ_API_KEY"):
    try:
        from groq import Groq
        clients["groq"] = Groq(api_key=os.environ["GROQ_API_KEY"])
        DEFAULT_MODELS["groq"] = "llama-3.3-70b-versatile"
    except Exception as e: print(f"Groq init failed: {e}")

# HuggingFace - Robust Auto-Discovery
if os.environ.get("HF_API_KEY"):
    try:
        from huggingface_hub import InferenceClient
        token = os.environ["HF_API_KEY"]

        # Candidate models to try (reliable & free-tier friendly)
        candidates = [
            "Qwen/Qwen2.5-72B-Instruct",
            "meta-llama/Llama-3.2-3B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "HuggingFaceH4/zephyr-7b-beta",
            "microsoft/Phi-3.5-mini-instruct"
        ]

        print("\nTesting Hugging Face models:")
        active_client = None

        for model in candidates:
            try:
                print(f"  - Trying {model.split('/')[1]}...", end=" ")
                # Test connection with a tiny request
                client = InferenceClient(token=token, model=model)
                client.chat.completions.create(messages=[{"role":"user", "content":"hi"}], max_tokens=1)
                print("\u2705 Working!")

                # If we get here, it works
                active_client = client
                DEFAULT_MODELS["huggingface"] = model
                clients["huggingface"] = client
                break
            except Exception:
                print("\u274C Failed")

        if not active_client:
            print("\n\u26A0\uFE0F All HF models failed. Check your token permissions (Inference API).")

    except Exception as e: print(f"HuggingFace init failed: {e}")

print(f"\n\u2728 Active Clients: {list(clients.keys())}")
if "huggingface" in clients:
    print(f"   Selected HF Model: {DEFAULT_MODELS['huggingface']}")

import os
from getpass import getpass

print("--- ⚙️ Universal API Key Setup ---")
print("Enter your keys below. Press Enter to skip any you don't have.")

# We need at least one key to proceed.
# If you are using Google Colab, you can also set these in the 'Secrets' tab on the left.

OPENAI_API_KEY    = getpass("OpenAI key: ") or ""
ANTHROPIC_API_KEY = getpass("Anthropic key: ") or ""
GEMINI_API_KEY    = getpass("Gemini key (free at aistudio.google.com): ") or ""
GROQ_API_KEY      = getpass("Groq key (free at console.groq.com): ") or ""
HF_API_KEY        = getpass("HuggingFace token (needs 'Inference' permission): ") or ""

os.environ["OPENAI_API_KEY"]    = OPENAI_API_KEY
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["GEMINI_API_KEY"]    = GEMINI_API_KEY
os.environ["GROQ_API_KEY"]      = GROQ_API_KEY
os.environ["HF_API_KEY"]        = HF_API_KEY

configured = []
if OPENAI_API_KEY:    configured.append("OpenAI")
if ANTHROPIC_API_KEY: configured.append("Anthropic")
if GEMINI_API_KEY:    configured.append("Gemini")
if GROQ_API_KEY:      configured.append("Groq")
if HF_API_KEY:        configured.append("HuggingFace")

print(f"\n\u2705 Keys configured for: {', '.join(configured) if configured else 'none'}")

if "huggingface" in clients:
    # Financial Prompt
    financial_prompt = """
    [Role] Act as the Expert Financial Modelling Agent and Senior Finance Manager at Tiny-Rod Hit Inc.
    [Context] You are evaluating two significant investment opportunities for the upcoming fiscal year.
    - WACC: 9% - Available Cash: $100 million - Project A: $50M initial, 20% growth. - Project B: $40M initial, 30% fail risk, 70% success/50% growth.
    [Task] Provide directional estimates for NPV/IRR. Use 'Atom of Thought' reasoning.
    [Format] Return valid JSON only: {"Project_A_Analysis": {"NPV_Implication": "", "IRR_Implication": ""},"Project_B_Analysis": {"Risk_Adjusted_NPV": "", "Expected_IRR": ""},"Capital_Efficiency_Comparison": ""}
    """

    print("\n--- Running Financial Analysis (Smart HF Client) ---")

    try:
        # Use the auto-selected client
        client = clients["huggingface"]
        model = DEFAULT_MODELS["huggingface"]

        print(f"Using model: {model}")

        messages = [
            {"role": "system", "content": "You are a financial expert. Output strict JSON only."},
            {"role": "user", "content": financial_prompt}
        ]

        # Execute
        response = client.chat.completions.create(messages=messages, temperature=0.2, max_tokens=1000)
        result_text = response.choices[0].message.content

        # Clean & Parse
        import json
        from IPython.display import display, JSON

        clean_result = result_text.replace("```json", "").replace("```", "").strip()
        if "{" in clean_result:
            clean_result = clean_result[clean_result.find("{"):clean_result.rfind("}")+1]

        print("\n--- \u2728 Analysis Result ---")
        display(JSON(json.loads(clean_result)))

    except Exception as e:
        print(f"\n\u274C Error during analysis: {e}")
else:
    print("\u26A0\uFE0F Hugging Face client not active. Please run the setup cells above.")

import json
import logging
import datetime
from pathlib import Path
from IPython.display import display, Markdown

LOG_DIR = Path("llm_logs")
LOG_DIR.mkdir(exist_ok=True)

SESSION_ID = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE   = LOG_DIR / f"session_{SESSION_ID}.jsonl"
TEXT_LOG   = LOG_DIR / f"session_{SESSION_ID}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(TEXT_LOG), logging.StreamHandler()]
)
logger = logging.getLogger("multi_llm")


def log_interaction(provider, model, messages, response, duration_sec, tokens=None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "session_id": SESSION_ID,
        "provider": provider,
        "model": model,
        "messages": messages,
        "response": response,
        "duration_sec": round(duration_sec, 3),
        "tokens": tokens or {}
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class ConversationManager:
    def __init__(self):
        self.histories = {}
        self.system_prompts = {}

    def set_system(self, provider, system_prompt):
        self.system_prompts[provider] = system_prompt
        logger.info(f"[{provider}] system prompt set")

    def add_message(self, provider, role, content):
        if provider not in self.histories:
            self.histories[provider] = []
        self.histories[provider].append({"role": role, "content": content})

    def get_history(self, provider):
        return self.histories.get(provider, [])

    def reset(self, provider=None):
        if provider:
            self.histories[provider] = []
            logger.info(f"[{provider}] history cleared")
        else:
            self.histories = {}
            logger.info("all histories cleared")

    def show(self, provider):
        history = self.get_history(provider)
        if not history:
            print(f"[{provider}] nothing yet")
            return
        lines = [f"## {provider} conversation\n"]
        for i, msg in enumerate(history, 1):
            label = "USER" if msg["role"] == "user" else "ASSISTANT"
            lines.append(f"**{label} [{i}]:**\n{msg['content']}\n")
        display(Markdown("\n---\n".join(lines)))

    def export(self, provider, filepath=None):
        fp = filepath or str(LOG_DIR / f"{provider}_{SESSION_ID}_conversation.json")
        data = {
            "provider": provider,
            "session_id": SESSION_ID,
            "system": self.system_prompts.get(provider, ""),
            "history": self.get_history(provider)
        }
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"saved to {fp}")


conv = ConversationManager()
print(f"logging ready — session {SESSION_ID}")

import time
import requests

clients = {}

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        clients["openai"] = OpenAI(api_key=OPENAI_API_KEY)
        print("openai ready")
    except Exception as e:
        print(f"openai failed: {e}")

if ANTHROPIC_API_KEY:
    try:
        import anthropic
        clients["anthropic"] = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        print("anthropic ready")
    except Exception as e:
        print(f"anthropic failed: {e}")

if GEMINI_API_KEY:
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=GEMINI_API_KEY)
        print("gemini ready")
    except Exception as e:
        print(f"gemini failed: {e}")

if GROQ_API_KEY:
    try:
        from groq import Groq
        clients["groq"] = Groq(api_key=GROQ_API_KEY)
        print("groq ready")
    except Exception as e:
        print(f"groq failed: {e}")

if HF_API_KEY:
    try:
        from huggingface_hub import InferenceClient
        clients["huggingface"] = InferenceClient(token=HF_API_KEY)
        print("huggingface ready")
    except Exception as e:
        print(f"huggingface failed: {e}")

if not clients:
    print("\nno providers available — enter a key in cell 2")
else:
    print(f"\nactive: {list(clients.keys())}")

from IPython.display import display, Markdown
import sys

DEFAULT_MODELS = {
    "openai":      "gpt-4o",
    "anthropic":   "claude-sonnet-4-20250514",
    "gemini":      "gemini-2.0-flash",
    "groq":        "llama-3.3-70b-versatile",
    "huggingface": "meta-llama/Llama-3.2-3B-Instruct"
}

AVAILABLE_MODELS = {
    "openai":      ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1-preview", "o1-mini"],
    "anthropic":   ["claude-opus-4-5", "claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"],
    "gemini":      ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "groq":        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
    "huggingface": ["meta-llama/Llama-3.2-3B-Instruct", "HuggingFaceH4/zephyr-7b-beta", "Qwen/Qwen2.5-72B-Instruct"]
}


def ask(prompt, provider="openai", model=None, system=None,
        temperature=0.7, max_tokens=2048, stream=True, remember=True):
    if provider not in clients:
        print(f"no client for '{provider}' — check cell 4")
        return ""
    model = model or DEFAULT_MODELS.get(provider, "")
    if system:
        conv.set_system(provider, system)
    if remember:
        conv.add_message(provider, "user", prompt)
    messages = conv.get_history(provider) if remember else [{"role": "user", "content": prompt}]
    sys_prompt = conv.system_prompts.get(provider, "You are a helpful assistant.")
    print(f"\n--- {provider.upper()} / {model} ---")
    start = time.time()
    response_text = ""
    token_info = {}
    try:
        if provider == "openai":
            oai_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["openai"].chat.completions.create(model=model, messages=oai_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["openai"].chat.completions.create(model=model, messages=oai_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                token_info = {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
                print(response_text)
        elif provider == "anthropic":
            if stream:
                with clients["anthropic"].messages.stream(model=model, system=sys_prompt, messages=messages, temperature=temperature, max_tokens=max_tokens) as s:
                    for text in s.text_stream:
                        print(text, end="", flush=True)
                        response_text += text
                    usage = s.get_final_message().usage
                    token_info = {"input": usage.input_tokens, "output": usage.output_tokens}
            else:
                resp = clients["anthropic"].messages.create(model=model, system=sys_prompt, messages=messages, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.content[0].text
                token_info = {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}
                print(response_text)
        elif provider == "gemini":
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            config = {"temperature": temperature, "max_output_tokens": max_tokens, "system_instruction": sys_prompt}
            if stream:
                resp = clients["gemini"].models.generate_content_stream(model=model, contents=contents, config=config)
                for chunk in resp:
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                        response_text += chunk.text
            else:
                resp = clients["gemini"].models.generate_content(model=model, contents=contents, config=config)
                response_text = resp.text
                print(response_text)
        elif provider == "groq":
            groq_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["groq"].chat.completions.create(model=model, messages=groq_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["groq"].chat.completions.create(model=model, messages=groq_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                token_info = {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
                print(response_text)
        elif provider == "huggingface":
            hf_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["huggingface"].chat.completions.create(model=model, messages=hf_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["huggingface"].chat.completions.create(model=model, messages=hf_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                print(response_text)
    except Exception as e:
        logger.error(f"[{provider}] {e}")
        print(f"\nerror: {e}")
        return ""
    duration = time.time() - start
    print(f"\n[{duration:.2f}s | {len(response_text)} chars]")
    if remember:
        conv.add_message(provider, "assistant", response_text)
    log_interaction(provider, model, messages, response_text, duration, token_info)
    logger.info(f"[{provider}/{model}] {len(prompt)}ch -> {len(response_text)}ch ({duration:.2f}s)")
    return response_text


def ask_once(prompt, provider="openai", **kwargs):
    return ask(prompt, provider=provider, remember=False, **kwargs)


def ask_all(prompt, providers=None, **kwargs):
    targets = providers or list(clients.keys())
    results = {}
    for p in targets:
        results[p] = ask(prompt, provider=p, remember=False, **kwargs)
    return results


print("ready")
print("  ask('hello', provider='gemini')        -> gemini")
print("  ask('hello', provider='huggingface')   -> hf inference api")
print("  ask('hello', provider='groq')          -> llama via groq")
print("  ask_all('...')                         -> all providers")

# how to use this thing

# just pick a provider and ask stuff
ask("what's the efficient market hypothesis in simple terms?", provider="gemini")

# try huggingface — it's free too
ask("explain stop-loss orders like i'm 5", provider="huggingface")

# groq is stupid fast, good for quick questions
ask("give me 3 momentum indicators traders actually use", provider="groq", temperature=0.3)

# you can give it a personality
conv.set_system("gemini", "you're a senior quant. skip the fluff, be direct.")
ask("how does toxic order flow mess with market makers?", provider="gemini")

# ask the same thing to every provider and compare
results = ask_all("what's the biggest risk in carry trades? keep it short.", stream=False)
for name, answer in results.items():
    print(f"\n{name.upper()}:\n{answer[:300]}")

# check what you've talked about
conv.show("gemini")

# start fresh when you want
# conv.reset("gemini")   # just gemini
# conv.reset()           # everything

import os
from huggingface_hub import InferenceClient

# --- 3. Update 'ask' function for Hugging Face support ---
def ask(prompt, provider="gemini", temperature=0.7, json_mode=False):
    if provider not in clients:
        return f"Error: Provider '{provider}' not initialized."

    print(f"Processing request with {provider.title()}... ")

    try:
        if provider == "gemini":
            # ... (Existing Gemini logic) ...
            generation_config = {"temperature": temperature}
            if json_mode: generation_config["response_mime_type"] = "application/json"
            response = clients["gemini"].generate_content(prompt, generation_config=generation_config)
            return response.text

        elif provider == "huggingface":
            # Retrieve token explicitly from environment
            token = os.environ.get("HF_API_KEY")
            if not token or len(token.strip()) == 0:
                return "Error: HF Token is empty. Please run the cell above and paste a valid token."

            # Switch to Zephyr-7B (very reliable on free tier)
            model_id = "HuggingFaceH4/zephyr-7b-beta"

            client = InferenceClient(model=model_id, token=token)

            # Zephyr/Mistral often prefer slightly different messaging, but standard user/assistant works
            messages = [
                {"role": "system", "content": "You are a helpful financial assistant. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ]

            response = client.chat.completions.create(
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content

    except Exception as e:
        return f"Error calling API: {e}"

print("Updated 'ask' function: Switched to Zephyr-7B for better compatibility.")

import json
from IPython.display import display, JSON

# --- 4. Execute Financial Task with Hugging Face ---
if "huggingface" in clients:
    print("--- Running Analysis with Hugging Face (Zephyr 7B) ---")

    result = ask(financial_prompt, provider="huggingface", temperature=0.2)

    print("\n--- Raw Response ---\n", result)

    # Attempt to parse JSON
    if "Error" not in result:
        try:
            # Clean up potential markdown code blocks
            clean_result = result.replace("```json", "").replace("```", "").strip()
            # Sometimes models add text before/after, try to find the first { and last }
            start = clean_result.find("{")
            end = clean_result.rfind("}") + 1
            if start != -1 and end != -1:
                clean_result = clean_result[start:end]

            parsed = json.loads(clean_result)
            print("\n--- Parsed JSON ---")
            display(JSON(parsed))
        except Exception as e:
            print(f"\nCould not parse JSON: {e}")
else:
    print("Hugging Face client not ready.")

import json
import logging
import datetime
from pathlib import Path
from IPython.display import display, Markdown

LOG_DIR = Path("llm_logs")
LOG_DIR.mkdir(exist_ok=True)

SESSION_ID = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE   = LOG_DIR / f"session_{SESSION_ID}.jsonl"
TEXT_LOG   = LOG_DIR / f"session_{SESSION_ID}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(TEXT_LOG), logging.StreamHandler()]
)
logger = logging.getLogger("multi_llm")


def log_interaction(provider, model, messages, response, duration_sec, tokens=None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "session_id": SESSION_ID,
        "provider": provider,
        "model": model,
        "messages": messages,
        "response": response,
        "duration_sec": round(duration_sec, 3),
        "tokens": tokens or {}
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class ConversationManager:
    def __init__(self):
        self.histories = {}
        self.system_prompts = {}

    def set_system(self, provider, system_prompt):
        self.system_prompts[provider] = system_prompt
        logger.info(f"[{provider}] system prompt set")

    def add_message(self, provider, role, content):
        if provider not in self.histories:
            self.histories[provider] = []
        self.histories[provider].append({"role": role, "content": content})

    def get_history(self, provider):
        return self.histories.get(provider, [])

    def reset(self, provider=None):
        if provider:
            self.histories[provider] = []
            logger.info(f"[{provider}] history cleared")
        else:
            self.histories = {}
            logger.info("all histories cleared")

    def show(self, provider):
        history = self.get_history(provider)
        if not history:
            print(f"[{provider}] nothing yet")
            return
        lines = [f"## {provider} conversation\n"]
        for i, msg in enumerate(history, 1):
            label = "USER" if msg["role"] == "user" else "ASSISTANT"
            lines.append(f"**{label} [{i}]:**\n{msg['content']}\n")
        display(Markdown("\n---\n".join(lines)))

    def export(self, provider, filepath=None):
        fp = filepath or str(LOG_DIR / f"{provider}_{SESSION_ID}_conversation.json")
        data = {
            "provider": provider,
            "session_id": SESSION_ID,
            "system": self.system_prompts.get(provider, ""),
            "history": self.get_history(provider)
        }
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"saved to {fp}")


conv = ConversationManager()
print(f"logging ready — session {SESSION_ID}")

import time
import requests

clients = {}

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        clients["openai"] = OpenAI(api_key=OPENAI_API_KEY)
        print("openai ready")
    except Exception as e:
        print(f"openai failed: {e}")

if ANTHROPIC_API_KEY:
    try:
        import anthropic
        clients["anthropic"] = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        print("anthropic ready")
    except Exception as e:
        print(f"anthropic failed: {e}")

if GEMINI_API_KEY:
    try:
        from google import genai
        clients["gemini"] = genai.Client(api_key=GEMINI_API_KEY)
        print("gemini ready")
    except Exception as e:
        print(f"gemini failed: {e}")

if GROQ_API_KEY:
    try:
        from groq import Groq
        clients["groq"] = Groq(api_key=GROQ_API_KEY)
        print("groq ready")
    except Exception as e:
        print(f"groq failed: {e}")

if HF_API_KEY:
    try:
        from huggingface_hub import InferenceClient
        clients["huggingface"] = InferenceClient(token=HF_API_KEY)
        print("huggingface ready")
    except Exception as e:
        print(f"huggingface failed: {e}")

if not clients:
    print("\nno providers available — enter a key in cell 2")
else:
    print(f"\nactive: {list(clients.keys())}")

from IPython.display import display, Markdown
import sys

DEFAULT_MODELS = {
    "openai":      "gpt-4o",
    "anthropic":   "claude-sonnet-4-20250514",
    "gemini":      "gemini-2.0-flash",
    "groq":        "llama-3.3-70b-versatile",
    "huggingface": "meta-llama/Llama-3.2-3B-Instruct"
}

AVAILABLE_MODELS = {
    "openai":      ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1-preview", "o1-mini"],
    "anthropic":   ["claude-opus-4-5", "claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"],
    "gemini":      ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "groq":        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
    "huggingface": ["meta-llama/Llama-3.2-3B-Instruct", "HuggingFaceH4/zephyr-7b-beta", "Qwen/Qwen2.5-72B-Instruct"]
}


def ask(prompt, provider="openai", model=None, system=None,
        temperature=0.7, max_tokens=2048, stream=True, remember=True):
    if provider not in clients:
        print(f"no client for '{provider}' — check cell 4")
        return ""
    model = model or DEFAULT_MODELS.get(provider, "")
    if system:
        conv.set_system(provider, system)
    if remember:
        conv.add_message(provider, "user", prompt)
    messages = conv.get_history(provider) if remember else [{"role": "user", "content": prompt}]
    sys_prompt = conv.system_prompts.get(provider, "You are a helpful assistant.")
    print(f"\n--- {provider.upper()} / {model} ---")
    start = time.time()
    response_text = ""
    token_info = {}
    try:
        if provider == "openai":
            oai_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["openai"].chat.completions.create(model=model, messages=oai_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["openai"].chat.completions.create(model=model, messages=oai_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                token_info = {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
                print(response_text)
        elif provider == "anthropic":
            if stream:
                with clients["anthropic"].messages.stream(model=model, system=sys_prompt, messages=messages, temperature=temperature, max_tokens=max_tokens) as s:
                    for text in s.text_stream:
                        print(text, end="", flush=True)
                        response_text += text
                    usage = s.get_final_message().usage
                    token_info = {"input": usage.input_tokens, "output": usage.output_tokens}
            else:
                resp = clients["anthropic"].messages.create(model=model, system=sys_prompt, messages=messages, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.content[0].text
                token_info = {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}
                print(response_text)
        elif provider == "gemini":
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            config = {"temperature": temperature, "max_output_tokens": max_tokens, "system_instruction": sys_prompt}
            if stream:
                resp = clients["gemini"].models.generate_content_stream(model=model, contents=contents, config=config)
                for chunk in resp:
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                        response_text += chunk.text
            else:
                resp = clients["gemini"].models.generate_content(model=model, contents=contents, config=config)
                response_text = resp.text
                print(response_text)
        elif provider == "groq":
            groq_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["groq"].chat.completions.create(model=model, messages=groq_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["groq"].chat.completions.create(model=model, messages=groq_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                token_info = {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
                print(response_text)
        elif provider == "huggingface":
            hf_msgs = [{"role": "system", "content": sys_prompt}] + messages
            if stream:
                resp = clients["huggingface"].chat.completions.create(model=model, messages=hf_msgs, temperature=temperature, max_tokens=max_tokens, stream=True)
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    response_text += delta
            else:
                resp = clients["huggingface"].chat.completions.create(model=model, messages=hf_msgs, temperature=temperature, max_tokens=max_tokens)
                response_text = resp.choices[0].message.content
                print(response_text)
    except Exception as e:
        logger.error(f"[{provider}] {e}")
        print(f"\nerror: {e}")
        return ""
    duration = time.time() - start
    print(f"\n[{duration:.2f}s | {len(response_text)} chars]")
    if remember:
        conv.add_message(provider, "assistant", response_text)
    log_interaction(provider, model, messages, response_text, duration, token_info)
    logger.info(f"[{provider}/{model}] {len(prompt)}ch -> {len(response_text)}ch ({duration:.2f}s)")
    return response_text


def ask_once(prompt, provider="openai", **kwargs):
    return ask(prompt, provider=provider, remember=False, **kwargs)


def ask_all(prompt, providers=None, **kwargs):
    targets = providers or list(clients.keys())
    results = {}
    for p in targets:
        results[p] = ask(prompt, provider=p, remember=False, **kwargs)
    return results


print("ready")
print("  ask('hello', provider='gemini')        -> gemini")
print("  ask('hello', provider='huggingface')   -> hf inference api")
print("  ask('hello', provider='groq')          -> llama via groq")
print("  ask_all('...')                         -> all providers")

# how to use this thing

# just pick a provider and ask stuff
ask("what's the efficient market hypothesis in simple terms?", provider="gemini")

# try huggingface — it's free too
ask("explain stop-loss orders like i'm 5", provider="huggingface")

# groq is stupid fast, good for quick questions
ask("give me 3 momentum indicators traders actually use", provider="groq", temperature=0.3)

# you can give it a personality
conv.set_system("gemini", "you're a senior quant. skip the fluff, be direct.")
ask("how does toxic order flow mess with market makers?", provider="gemini")

# ask the same thing to every provider and compare
results = ask_all("what's the biggest risk in carry trades? keep it short.", stream=False)
for name, answer in results.items():
    print(f"\n{name.upper()}:\n{answer[:300]}")

# check what you've talked about
conv.show("gemini")

# start fresh when you want
# conv.reset("gemini")   # just gemini
# conv.reset()           # everything

# --- 5. Generate Executive Summary ---
# This block interprets the JSON output from the previous step

if 'clean_result' in locals():
    try:
        data = json.loads(clean_result)

        print("\n" + "="*60)
        print("       📊 EXECUTIVE FINANCIAL SUMMARY: Tiny-Rod Hit Inc.")
        print("="*60 + "\n")

        # Project A
        print(f"🔹 **Project A (Expansion)**: The 'Safe Bet'")
        print(f"   • {data['Project_A_Analysis']['NPV_Implication']}")
        print(f"   • {data['Project_A_Analysis']['IRR_Implication']}")

        # Project B
        print(f"\n🔸 **Project B (R&D)**: The 'High Risk / High Reward'")
        print(f"   • {data['Project_B_Analysis']['Risk_Adjusted_NPV']}")
        print(f"   • {data['Project_B_Analysis']['Expected_IRR']}")

        # Conclusion
        print(f"\n💡 **Capital Efficiency Verdict**:\n   {data['Capital_Efficiency_Comparison']}")

        print("\n" + "-"*60)

    except Exception as e:
        print("Could not generate summary from previous output.")
else:
    print("No analysis data found. Please run the Hugging Face analysis cell above first.")

ask("give one paragraph explanation of big band theory. Strictly nor more that 100 words", provider="gemini")