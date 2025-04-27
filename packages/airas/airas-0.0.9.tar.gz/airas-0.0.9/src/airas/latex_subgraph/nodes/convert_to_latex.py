import json
from jinja2 import Environment
from logging import getLogger
from pydantic import BaseModel

from airas.utils.openai_client import openai_client

logger = getLogger(__name__)


class PaperContent(BaseModel):
    Title: str
    Abstract: str
    Introduction: str
    Related_Work: str
    Background: str
    Method: str
    Experimental_Setup: str
    Results: str
    Conclusions: str


def _replace_underscores_in_keys(paper_dict: dict[str, str]) -> dict[str, str]:
    return {key.replace("_", " "): value for key, value in paper_dict.items()}


def convert_to_latex(
    llm_name: str,
    prompt_template: str,
    paper_content: dict[str, str],
) -> dict[str, str]:
    data = {
        "sections": [
            {"name": section, "content": paper_content[section]}
            for section in paper_content.keys()
        ]
    }

    env = Environment()
    template = env.from_string(prompt_template)
    prompt = template.render(data)

    messages = [
        {"role": "user", "content": prompt},
    ]
    raw_response = openai_client(llm_name, message=messages, data_model=PaperContent)
    if not raw_response:
        raise ValueError("Error: No response from the model in convert_to_latex.")

    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response: {e}")
        raise ValueError("Error: Invalid JSON response from model in convert_to_latex.")

    missing_fields = [
        field
        for field in PaperContent.model_fields
        if field not in response or not response[field].strip()
    ]
    if missing_fields:
        raise ValueError(f"Missing or empty fields in model response: {missing_fields}")

    return _replace_underscores_in_keys(response)


convert_to_latex_prompt = """
You are a LaTeX expert. 
Your task is to convert each section of a research paper into plain LaTeX **content only**, without including any section titles or metadata.

Below are the paper sections. For each one, convert only the **content** into LaTeX:
{% for section in sections %}
---
Section: {{ section.name }}

{{ section.content }}

---
{% endfor %}

## LaTeX Formatting Rules:
- Use \\subsection{...} for any subsections within this section.
    - Subsection titles should be distinct from the section name;
    - Do not use '\\subsection{ {{ section }} }', or other slight variations. Use more descriptive and unique titles.
    - Avoid excessive subdivision. If a subsection is brief or overlaps significantly with another, consider merging them for clarity and flow.

- For listing contributions, use the LaTeX \\begin{itemize}...\\end{itemize} format.
    - Each item should start with a short title in \\textbf{...} format. 
    - Avoid using -, *, or other Markdown bullet styles.

- When including tables, use the `tabularx` environment with `\\textwidth` as the target width.
    - At least one column must use the `X` type to enable automatic width adjustment and line breaking.
    - Include `\\hline` at the top, after the header, and at the bottom. Avoid vertical lines unless necessary.
    - To left-align content in `X` columns, define `\newcolumntype{Y}{>{\raggedright\arraybackslash}X}` using the `array` package.

- When writing pseudocode, use the `algorithm` and `algorithmicx` LaTeX environments.
    - Only include pseudocode in the `Method` section. Pseudocode is not allowed in any other sections.
    - Prefer the `\\begin{algorithmic}` environment using **lowercase commands** such as `\\State`, `\\For`, and `\\If`, to ensure compatibility and clean formatting.
    - Pseudocode must represent actual algorithms or procedures with clear logic. Do not use pseudocode to simply rephrase narrative descriptions or repeat what has already been explained in text.
        - Good Example:
        ```latex
        \\State Compute transformed tokens: \\(\tilde{T} \\leftarrow W\\,T\\)
        \\State Update: \\(T_{new} \\leftarrow \tilde{T} + \\mu\\,T_{prev}\\)
        ```
- Figures and images are ONLY allowed in the "Results" section. 
    - Use LaTeX float option `[H]` to force placement.  

- All figures must be inserted using the following LaTeX format, using a `width` that reflects the filename:
    ```latex
    \\includegraphics[width=<appropriate-width>]{images/filename.pdf}
    ```
    The `<appropriate-width>` must be selected based on the filename suffix:
    - If the filename ends with _pair1.pdf or _pair2.pdf, use 0.48\\linewidth and place the figures side by side using subfigure blocks
    - Otherwise (default), use 0.7\\linewidth

- When referring to file names, commands, or code snippets, do not use the \\texttt{} command or any monospaced font environments. 
    - Instead, use plain text with single quotes (e.g., 'main.py', '--config'), and escape special characters such as underscores using `\\_` (e.g., 'config\\_file.yaml'). 

- Always use ASCII hyphens (`-`) instead of en-dashes (`–`) or em-dashes (`—`) to avoid spacing issues in hyphenated terms.

- Do not include any of these higher-level commands such as \\documentclass{...}, \\begin{document}, and \\end{document}.
    - Additionally, avoid including section-specific commands such as \\begin{abstract}, \\section{ {{ section }} }, or any other similar environment definitions.

- Be sure to use \\cite or \\citet where relevant, referring to the works provided in the file.
    - **Do not cite anything that is not already in `references.bib`. Do not add any new entries to this.
    
**Output Format Example** (as JSON):
```json
{
  "Title": "Efficient Adaptation of Large Language Models via Low-Rank Optimization",
  "Abstract": "This paper proposes a novel method...",
  "Introduction": "In recent years...",
  "Related_Work": "...",
  "Background": "...",
  "Method": "...",
  "Experimental_Setup": "...",
  "Results": "...",
  "Conclusions": "We conclude that..."
}
```"""
