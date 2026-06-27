"""Generate stage prompt markdown files from the stage spec."""

import os

STAGES = [
    ("stage_1_config_reconnaissance", "Config Reconnaissance",
     "Analyze project context and map source content structure"),
    ("stage_2_spine_pass", "Spine Pass",
     "Build wiki topic outline and hierarchy"),
    ("stage_3_deep_extraction", "Deep Extraction",
     "Extract comprehensive content for each topic"),
    ("stage_4_cross_reference_synthesis", "Cross-Reference Synthesis",
     "Build cross-reference graph and verify links"),
    ("stage_5_html_generation", "HTML Generation",
     "Render wiki markdown into self-contained HTML"),
]

TEMPLATE = """# Stage {num}: {title}

## Objective
{desc}

## Input
- Previous stage output
- {extra_inputs}

## Process
1. {step_1}
2. {step_2}
3. {step_3}

## Output
{output}
"""

DETAILS = {
    1: {
        "extra_inputs": "aim.md, brain.md, project source content",
        "step_1": "Read aim.md and brain.md to understand project scope",
        "step_2": "Identify all topics to be covered and their relationships",
        "step_3": "Document extraction boundaries and content sources",
        "output": "config_recon_results.md with mapped topics"
    },
    2: {
        "extra_inputs": "config_recon_results.md",
        "step_1": "Organize topics into a logical hierarchy",
        "step_2": "Define ordering and dependencies between topics",
        "step_3": "Annotate inter-topic relationships",
        "output": "spine.md with tiered topic structure"
    },
    3: {
        "extra_inputs": "spine.md",
        "step_1": "For each topic in spine, write comprehensive markdown",
        "step_2": "Include cross-reference annotations to related topics",
        "step_3": "Add practical examples and code snippets where applicable",
        "output": "15 topic .md files in topics/ directory"
    },
    4: {
        "extra_inputs": "All topic files from Stage 3",
        "step_1": "Parse cross-reference annotations from all topics",
        "step_2": "Build bidirectional reference graph",
        "step_3": "Verify all links resolve and fix broken references",
        "output": "cross_references.md with complete reference table"
    },
    5: {
        "extra_inputs": "All topic files + cross_references.md",
        "step_1": "Design HTML template with inline CSS",
        "step_2": "Render each topic as a section in the HTML",
        "step_3": "Generate navigation, TOC, and cross-reference links",
        "output": "output/option_a/index.html (self-contained wiki)"
    },
}

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "stage_prompts")
    os.makedirs(out_dir, exist_ok=True)
    for num, (filename, title, desc) in enumerate(STAGES, 1):
        d = DETAILS[num]
        content = TEMPLATE.format(
            num=num, title=title, desc=desc,
            extra_inputs=d["extra_inputs"],
            step_1=d["step_1"], step_2=d["step_2"], step_3=d["step_3"],
            output=d["output"]
        )
        path = os.path.join(out_dir, f"{filename}.md")
        with open(path, "w") as f:
            f.write(content)
        print(f"Generated {path}")
    print("Done")
