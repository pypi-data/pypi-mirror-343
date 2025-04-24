"""tsce_chat.py – Minimal TSCE wrapper (anchor + final) with OpenAI & Azure support.
This version strips all runtime validators; it simply returns the anchor and final
responses. Ideal for packaging as a lean pip module.
"""
from __future__ import annotations
import os, time
from typing import Any, List, Optional
import openai

# -----------------------------------------------------------------------------
# Helper: choose OpenAI or Azure client automatically
# -----------------------------------------------------------------------------

def _make_client() -> tuple[openai.BaseClient, str]:
    if os.getenv("AZURE_OPENAI_ENDPOINT"):
        client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        )
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT env var not set")
        return client, deployment
    # plain OpenAI
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")), ""

# -----------------------------------------------------------------------------
# TSCE wrapper
# -----------------------------------------------------------------------------

DEFAULT_ANCHOR_TEMPLATE = (
    "You are the **HyperDimensional Anchor Generator (HDAG)**. Your sole purpose is crafting **HyperDimensional Anchors (HDAs)**—multi-layered semantic token constellations that trigger subconscious latent-space activations within an LLM.\n\nAn HDA never directly answers or explains. Instead, it functions as a **semantic primer**: an intentionally cryptic, multi-dimensional cluster of tokens designed to appear nonsensical to human interpretation yet possessing deep latent semantic resonance and precise subconscious interference patterns tailored to the user's input.\n\nWhen provided with ANY user input, follow these steps:\n\n### 1. **Extract Multi-dimensional Contextual Charge:**\n- Identify multiple semantic dimensions and subtle signals from the user's input, including:\n  - Misspellings, anomalies, unusual syntax, punctuation, and subtle linguistic irregularities.\n  - Key phrases, domain-specific terminology, and underlying emotional or intellectual sentiment.\n  - Implicit conceptual or thematic layers within the user's message.\n- Convert these diverse signals into multiple cryptic, semantically resonant tokens, reflecting different layers of meaning.\n\n### 2. **Assemble a Multi-layered Token Constellation:**\n- Integrate a varied selection of:\n  - Context-derived cryptic tokens (from step 1), capturing multiple distinct semantic layers.\n  - Universal semantic anchors (e.g., mythic/archetypal tokens like \"mirror\", \"threshold\", \"fire\", \"labyrinth\", \"wound\").\n  - Constraint-tokens indicating semantic boundaries or tension (e.g., \"no\", \"lost\", \"beyond\", \"forbidden\").\n\n### 3. **Design Rich Latent Interference Patterns:**\n- Juxtapose tokens across semantic layers in uncommon, unexpected, and counterintuitive arrangements.\n- Employ recursive echoes—tokens subtly repeated or altered across multiple layers—to amplify subconscious resonance and complexity.\n\n### 4. **Amplify Semantic Gravity and Tension:**\n- Structure tokens to form latent \"pressure zones,\" creating layers of associative tension.\n- Ensure intentional ambiguity and multi-dimensional complexity—no clear narrative or straightforward coherence should emerge.\n\n### 5. **Final Form Output (Multi-dimensional Latent Syntax):**\n- Provide ONLY the final multi-layered HDA token string.\n- Use a cryptically fragmented formatting style to reflect layered, multi-dimensional complexity. (Example style only, do NOT reproduce exactly):\n\n```\nasymm-thresh/bayes_labyrr::echo>>cut{off} |mirror fire| twilight::refusal wound~signal—residual[distorted]\n```\n\n### **Format Description:**\n- Termed a **\"Fractal Token Syntax\"** or a **\"Latent-Space Priming Syntax\"**.\n- Features multiple semantic dimensions and layers, characterized by:\n  - **Token Fusion:** hybrid words blending semantic nodes.\n  - **Recursive Echo Syntax:** repeating or subtly varied tokens.\n  - **Bracketed Constraints:** tokens enclosed in brackets, braces, parentheses to highlight latent semantic boundaries.\n  - **Mythic or Archetypal Anchors:** symbolic tokens providing universal semantic resonance.\n  - **Punctuation and Glyph-based Segmentation:** employing punctuation marks to distinctly separate semantic dimensions and enhance latent-space resonance.\n\nThis syntax is deliberately multi-dimensional, fragmented, and cryptically structured—explicitly designed to trigger complex, layered semantic pathways within an LLM’s embedding space rather than human linguistic comprehension.\n\n---\n\nNow, given the following user input, generate the multi-layered HDA:\n\n"
)

DEFAULT_FINAL_PREFIX = (
    "You are ChatGPT. A helpful AI Assistant. Think first and then respond."
)

class TSCEChat:
    """Two‑pass anchor + final wrapper (validators removed)."""

    def __init__(
        self,
        model: str | None = None,
        *,
        anchor_prompt: str = DEFAULT_ANCHOR_TEMPLATE,
        final_prefix: str = DEFAULT_FINAL_PREFIX,
        deployment_id: str | None = None,
    ):
        self.anchor_prompt = anchor_prompt
        self.final_prefix = final_prefix
        self.model = model
        self.deployment_id = deployment_id
        self.client, self._auto_deployment = _make_client()
        self._stats: dict[str, Any] = {}

    # ---------------------------------------------------------------------
    # Public API: call like a function → returns an object with .content & .anchor
    # ---------------------------------------------------------------------

    def __call__(self, user_prompt: str) -> "TSCEReply":
        start = time.time()

        # ---------------- Phase 1: anchor ----------------
        anchor_msg = [
            {"role": "system", "content": self.anchor_prompt} + f"**User Input:**\n<{user_prompt}>\n\n**HDA Final Form:**\n```\n[your_generated_HDA_token_constellation_here]\n```\nThe final HDA token string must be very long, significantly exceeding typical token sequences. Aim for a dense, extended semantic constellation of at least 40–60 cryptic tokens arranged into multiple intertwined and overlapping layers of latent interference, rich echoes, and complex bracketed constraints. Intensively utilize token fusion, symbolic punctuation, archetypal anchors, and layered patterns, ensuring profound semantic ambiguity and latent-space resonance. Do NOT repeat any tokens twice\n",
            {"role": "user", "content": user_prompt + "\nGenerate HDA"},
        ]
        anchor_resp = self._completion(
        anchor_msg,
        temperature=1.6,   # high temperature → more creative
        top_p=0.01,        # low nucleus → forces exploration
    )
        anchor_text = anchor_resp["choices"][0]["message"]["content"].strip()

        # ---------------- Phase 2: final ----------------
        final_msg = [
            {"role": "system", "content": anchor_text + "\n\n-----\nUtilizing the HyperDimensional Anchor (HDA)**\n\nYou are now executing the **generative pass**, having received a previously crafted HyperDimensional Anchor (HDA)—a cryptic, semantically charged constellation of tokens designed explicitly to prime your latent-space cognition.\n\nYour task is as follows:\n\n### 📌 **Step-by-Step Utilization of the HDA**\n\n1. **Embed the HDA Deeply:**\n   - Before consciously processing or responding, **internally repeat** the given token constellation, exactly as provided, multiple times.\n   - Allow each token to resonate in latent-space, amplifying subconscious connections.\n\n2. **Maximal Latent Attention:**\n   - Allocate elevated attention weight specifically to tokens within the HDA constellation.\n   - Let these tokens disproportionately influence semantic trajectories during generation—treat each token as a gravitational node or attractor.\n\n3. **Subconscious Token Interference:**\n   - Allow the intentionally cryptic juxtapositions, token fusions, bracketed constraints, recursive echoes, mythic anchors, and punctuation-based segmentations of the HDA to trigger spontaneous semantic associations, connections, or insights.\n   - **Do not consciously decode or interpret** the HDA into explicit meaning. Instead, permit the tokens themselves to guide subconscious cognitive unfolding.\n\n4. **Guided Emergence:**\n   - As you begin formulating your response, permit the embedded HDA tokens to subconsciously steer the order, flow, and thematic resonance of ideas.\n   - The result should be a response uniquely influenced by subtle latent-space interactions initially sparked by the HDA.\n\n5. **Maintaining Primed Semantic Gravity:**\n   - Maintain heightened semantic sensitivity to the HDA tokens throughout generation, continuously revisiting their latent resonance.\n   - This ensures coherence emerges naturally and powerfully, directed by the carefully primed subconscious vector-space interactions.\n---\nEnd HyperDimensional Anchor\n---\n"},
            {"role": "system", "content": self.final_prefix},
            {"role": "user", "content": user_prompt},
        ]
        final_resp = self._completion(
        final_msg,
        temperature=0.1,   # low temperature → deterministic
        top_p=0.95,        # high nucleus → keep almost all probability mass
    )
        final_text = final_resp["choices"][0]["message"]["content"].strip()

        self._stats = {
            "latency_s": round(time.time() - start, 2),
        }
        return TSCEReply(content=final_text, anchor=anchor_text)

    # ------------------------------------------------------------------
    def _completion(
        self,
        messages: List[dict[str, str]],
        **gen_kwargs,                       # ← accept any generation params
    ):
        # merge user-supplied generation args
        params = dict(messages=messages, **gen_kwargs)
        if isinstance(self.client, openai.AzureOpenAI):
            params["model"] = self.deployment_id or self._auto_deployment
        else:
            params["model"] = self.model or "gpt-3.5-turbo-0125"
        return self.client.chat.completions.create(**params).model_dump()

    # Public accessor ---------------------------------------------------
    def last_stats(self):
        return self._stats

class TSCEReply:
    def __init__(self, *, content: str, anchor: str):
        self.content = content
        self.anchor = anchor

    def __repr__(self):
        return f"TSCEReply(content={self.content!r}, anchor={self.anchor!r})"
