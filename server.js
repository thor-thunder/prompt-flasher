import 'dotenv/config';
import express from 'express';
import Anthropic from '@anthropic-ai/sdk';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const client = new Anthropic({
  apiKey: process.env.OPENROUTER_API_KEY,
  baseURL: 'https://openrouter.ai/api',
  defaultHeaders: {
    'HTTP-Referer': 'http://localhost:3000',
    'X-Title': 'Prompt Generator GSM-6',
  },
});

app.use(express.json());
app.use(express.static(join(__dirname, 'public')));

const PLATFORM_NOTES = {
  claude:      'Claude excels at nuanced reasoning and long context. Use XML tags, detailed instructions, and explicit output format.',
  chatgpt:     'ChatGPT responds well to role assignment and step-by-step instructions. Use clear sections.',
  grok:        'Grok is direct and tolerates informal tone. Keep it punchy but precise.',
  gemini:      'Gemini handles multimodal and structured data well. Leverage lists and explicit constraints.',
  midjourney:  'Midjourney is image-focused. Output must be a visual description with style, medium, lighting, and camera angle keywords — no prose.',
  deepseek:    'DeepSeek performs well on technical/code tasks. Be explicit about language, format, and edge cases.',
};

app.post('/generate', async (req, res) => {
  const { goal, platform } = req.body;
  if (!goal || !platform) return res.status(400).json({ error: 'Missing goal or platform' });

  const platformNote = PLATFORM_NOTES[platform.toLowerCase()] ?? '';

  try {
    const response = await client.messages.create({
      model: 'anthropic/claude-3.7-sonnet:thinking',
      max_tokens: 16000,
      thinking: { type: 'enabled', budget_tokens: 5000 },
      system: `You are an elite prompt engineer. Your sole job is to transform a user's raw goal into a perfectly crafted, ready-to-use prompt for a specific AI platform.

Rules:
- Output ONLY the final prompt. No preamble, no explanation, no markdown wrapper.
- The prompt must be immediately usable — copy-paste ready.
- Adapt style, structure, and vocabulary to the target platform.
- Be specific, detailed, and precise. Vague prompts produce vague results.

Target platform: ${platform.toUpperCase()}
Platform note: ${platformNote}`,
      messages: [{ role: 'user', content: `My goal: ${goal}` }],
    });

    const text = response.content.find(b => b.type === 'text')?.text ?? '';
    res.json({ prompt: text });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT ?? 3000;
app.listen(PORT, () => console.log(`Prompt Generator running → http://localhost:${PORT}`));
