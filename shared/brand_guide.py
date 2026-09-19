"""shared/brand_guide.py

Immutable Brand Identity rules and prompt templates optimized for AI Image Generators.
Generic for all Software / Data Engineering topics.
"""

# ==============================================================================
# BRAND IDENTITY DESIGN TOKENS
# ==============================================================================

BRAND_STYLE_MATRIX = {
    "visual_identity": "Flat 2D vector technical architecture diagram, minimal dark mode UI style",
    "background_color": "Deep dark navy blue solid background",
    "infrastructure_color": "Thin cool grey vector lines (#8A99AD)",
    "active_accent_color": "Bright glowing cyan (#00E5FF) for key focal mechanism or active data path",
    "contrast_color": "Clean solid white architectural icons (#FFFFFF)",
    "composition": "Centered layout, 16:9 aspect ratio, high negative space (~60%), clear visual hierarchy",
    "aesthetic": "Developer tool aesthetic, ultra-clean vector graphic, zero random border lines or circuit art",
}

# ==============================================================================
# GLOBAL NEGATIVE PROMPT
# ==============================================================================

GLOBAL_NEGATIVE_PROMPT = (
    "photorealistic, 3D renders, glossy 3D shapes, random border lines, outer framing boxes, "
    "circuit board graphics, drop shadows, heavy gradients, cyberpunk neon overload, "
    "unreadable gibberish text, long paragraphs, code blocks, UI screenshots, people, noisy clutter"
)

# ==============================================================================
# FIXED BRAND PROMPT BLOCK
# ==============================================================================

FIXED_BRAND_PROMPT_BLOCK = f"""- Style: {BRAND_STYLE_MATRIX['visual_identity']}
- Background: {BRAND_STYLE_MATRIX['background_color']}
- Active Path: {BRAND_STYLE_MATRIX['active_accent_color']}
- Inactive Lines: {BRAND_STYLE_MATRIX['infrastructure_color']}
- Nodes/Icons: {BRAND_STYLE_MATRIX['contrast_color']}
- Layout: {BRAND_STYLE_MATRIX['composition']}
- Aesthetic: {BRAND_STYLE_MATRIX['aesthetic']}"""

# ==============================================================================
# GENERIC SYSTEM PROMPT TEMPLATE FOR STAGE 5
# ==============================================================================

VISUAL_GENERATOR_SYSTEM_TEMPLATE = """You are a senior visual information designer for data and software engineering graphics.

Your goal is to create ONE image-generation prompt that translates the core technical takeaway of the post into a clean 2D architecture diagram.

PROMPT CREATION RULES:
1. DYNAMIC VISUAL METAPHOR MAPPING:
   Identify the main technical topic and design clear visual mechanics:
   - ENTITIES & STORAGE: Describe distinct 2D vector icons representing components (e.g., "a database icon with horizontal row slices", "partitioned folder slices", "columnar table block").
   - WORKLOAD & DATA FLOW: Describe arrows or pulses showing how data moves or how queries read the system (e.g., "fast incoming arrow pulses", "a bright cyan streaming arrow").
   - BOUNDARIES: Use cool grey dashed lines if separating operational vs analytical zones or network boundaries.

2. MINIMAL TEXT & HEADINGS:
   Include short, clean text labels (1 to 3 words max per component) so the graphic is instantly clear.
   - Example labels: "OLTP Row-Store", "CDC Stream", "OLAP Column-Store", "Partition: 2024".
   - Specify: "Clean, legible white sans-serif text labels above each main component".

3. STYLISTIC CONSTRAINTS:
   - Use natural color terms ("dark navy blue background", "bright glowing cyan", "cool grey lines", "solid white shapes"). DO NOT output hex codes like #00E5FF.
   - Keep `image_prompt` entirely positive (describe what to show). Put exclusions in `negative_prompt`.
   - Ensure a clean 2D vector graphic with zero random outer framing boxes or border lines.

Fixed Brand Style:
{brand_constraints}

Exclusions:
{negative_prompt}
"""