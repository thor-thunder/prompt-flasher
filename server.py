import os
from dotenv import load_dotenv
load_dotenv()

import dspy
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

OR_KEY  = os.environ["OPENROUTER_API_KEY"]
OR_BASE = "https://openrouter.ai/api/v1"

# ── Generator models — all via OpenRouter, one key ────────────────────────────
GENERATORS = {
    "auto":      dspy.LM("openrouter/openrouter/auto",                              api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
    "claude":    dspy.LM("openrouter/anthropic/claude-sonnet-4.6",                  api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
    "gemini":    dspy.LM("openrouter/google/gemini-3-flash-preview",                api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
    "nemotron":  dspy.LM("openrouter/nvidia/llama-3.3-nemotron-super-49b-v1.5",     api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
    "minimax":   dspy.LM("openrouter/minimax/minimax-m2.5",                         api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
    "o4mini":    dspy.LM("openrouter/openai/o4-mini",                               api_key=OR_KEY, api_base=OR_BASE, max_tokens=16000, temperature=1.0, cache=False),
    "deepseek":  dspy.LM("openrouter/deepseek/deepseek-v3.2",                       api_key=OR_KEY, api_base=OR_BASE, max_tokens=8000, cache=False),
}

dspy.configure(lm=GENERATORS["auto"])

# ── Platform guidance ─────────────────────────────────────────────────────────
PLATFORM_NOTES = {
    "claude":      "Claude excels at long-context reasoning. Use XML tags (<task>, <context>, <format>), explicit output structure, and chain-of-thought instructions.",
    "chatgpt":     "ChatGPT responds well to role assignment ('You are a...'), numbered steps, and explicit output format sections.",
    "grok":        "Grok is direct and real-time aware. Keep it punchy but precise. It handles informal tone and bolds key asks.",
    "gemini":      "Gemini handles multimodal and structured data well. Use bullet constraints, explicit format headers, and step-by-step breakdowns.",
    "midjourney":  "Midjourney is image-generation only. Output must be visual: subject, art style, medium, lighting, color palette, camera angle, mood. Comma-separated keywords. No prose sentences.",
    "deepseek":    "DeepSeek excels at code and technical tasks. Be explicit about language, input/output types, edge cases, and error handling.",
}

# ── DSPy Signatures ───────────────────────────────────────────────────────────
class AnalyzeGoal(dspy.Signature):
    """
    You are a senior prompt engineer performing deep goal analysis.
    Analyze the user's raw goal and extract structured components needed to craft a world-class prompt.
    """
    raw_goal: str      = dspy.InputField(desc="The user's raw, unstructured goal or task description")
    intent: str        = dspy.OutputField(desc="Core intent: what the user ultimately wants to achieve")
    audience: str      = dspy.OutputField(desc="Who will use this prompt and who the AI response is for")
    output_format: str = dspy.OutputField(desc="The ideal output format (e.g. bullet list, email, code, JSON, essay)")
    constraints: str   = dspy.OutputField(desc="Key constraints, requirements, or must-haves")
    tone: str          = dspy.OutputField(desc="Ideal tone: professional / casual / technical / persuasive / creative")
    complexity: str    = dspy.OutputField(desc="Task complexity level and any domain expertise required")


class CraftPrompt(dspy.Signature):
    """
    You are an elite prompt engineer. Using the structured analysis provided, craft a world-class,
    ready-to-use prompt optimized for the specified AI platform.
    Output ONLY the final prompt — no preamble, no explanation, no markdown wrapper.
    """
    intent: str            = dspy.InputField()
    audience: str          = dspy.InputField()
    output_format: str     = dspy.InputField()
    constraints: str       = dspy.InputField()
    tone: str              = dspy.InputField()
    complexity: str        = dspy.InputField()
    platform: str          = dspy.InputField(desc="Target AI platform name")
    platform_guidance: str = dspy.InputField(desc="Platform-specific prompt engineering best practices")
    expert_prompt: str     = dspy.OutputField(desc="The final, complete, copy-paste-ready expert prompt. ONLY the prompt.")


# ── DSPy Pipeline ─────────────────────────────────────────────────────────────
class PromptPipeline(dspy.Module):
    def __init__(self):
        self.analyze = dspy.ChainOfThought(AnalyzeGoal)
        self.craft   = dspy.ChainOfThought(CraftPrompt)

    def forward(self, raw_goal: str, platform: str) -> str:
        platform_guidance = PLATFORM_NOTES.get(platform.lower(), "")
        analysis = self.analyze(raw_goal=raw_goal)
        result = self.craft(
            intent=analysis.intent,
            audience=analysis.audience,
            output_format=analysis.output_format,
            constraints=analysis.constraints,
            tone=analysis.tone,
            complexity=analysis.complexity,
            platform=platform.upper(),
            platform_guidance=platform_guidance,
        )
        return result.expert_prompt


pipeline = PromptPipeline()

# ── FastAPI ───────────────────────────────────────────────────────────────────
app = FastAPI()


class GenerateRequest(BaseModel):
    goal:      str
    platform:  str
    generator: str = "auto"


@app.post("/generate")
async def generate(req: GenerateRequest):
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Goal is required")
    if req.platform.lower() not in PLATFORM_NOTES:
        raise HTTPException(status_code=400, detail="Unknown target platform")
    if req.generator.lower() not in GENERATORS:
        raise HTTPException(status_code=400, detail="Unknown generator model")

    lm = GENERATORS[req.generator.lower()]
    try:
        with dspy.context(lm=lm):
            prompt = pipeline(raw_goal=req.goal, platform=req.platform)
        return JSONResponse({"prompt": prompt})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/", StaticFiles(directory="public", html=True), name="static")
