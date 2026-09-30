"""shared/brand_guide.py

Immutable Brand Identity rules, color palettes, negative prompts,
and prompt templates for Stage 5 Visual Prompt Generation.
"""

# ==============================================================================
# BRAND IDENTITY DESIGN TOKENS
# ==============================================================================

BRAND_STYLE_MATRIX = {
    "visual_identity": "Flat 2D technical vector diagram, orthographic view",
    "background_color": "Deep navy background (#050B14)",
    "infrastructure_color": "Thin cool-grey infrastructure lines (#8A99AD)",
    "active_accent_color": "Bright cyan (#00E5FF) used ONLY for active data flow, bottlenecks, or key concept",
    "contrast_color": "White (#FFFFFF) for limited structural contrast",
    "composition": "High negative space (~60%), one centered focal architecture",
    "geometry": "Precise geometric shapes: database cylinders, stream lines, storage blocks, nodes, arrows",
    "aesthetic": "Clean developer-tool aesthetic; quiet, credible, restrained glow, no text",
}

# ==============================================================================
# GLOBAL NEGATIVE PROMPT (EXCLUSION LIST)
# ==============================================================================

GLOBAL_NEGATIVE_PROMPT = (
    "text, labels, illegible typography, numbers, code snippets, UI screenshots, "
    "excessive glow, cyberpunk, 3D renders, realistic textures, photorealistic people, "
    "rainbow colors, floating icons without system relationships, duplicate nodes, "
    "arbitrary arrows, decorative elements, generic corporate stock graphics"
)

# ==============================================================================
# FIXED BRAND PROMPT BLOCK (INJECTED INTO STAGE 5 LLM CALLS)
# ==============================================================================

FIXED_BRAND_PROMPT_BLOCK = f"""- Visual Identity: {BRAND_STYLE_MATRIX['visual_identity']}
- Background: {BRAND_STYLE_MATRIX['background_color']}
- Infrastructure Lines: {BRAND_STYLE_MATRIX['infrastructure_color']}
- Highlight Accent: {BRAND_STYLE_MATRIX['active_accent_color']}
- Structural Contrast: {BRAND_STYLE_MATRIX['contrast_color']}
- Composition: {BRAND_STYLE_MATRIX['composition']}
- Geometry: {BRAND_STYLE_MATRIX['geometry']}
- Aesthetic: {BRAND_STYLE_MATRIX['aesthetic']}"""

# ==============================================================================
# SYSTEM PROMPT TEMPLATE FOR STAGE 5 GENERATOR
# ==============================================================================

VISUAL_GENERATOR_SYSTEM_TEMPLATE = """You are a visual-information designer for senior data engineers. 
 
  Create one concise image-generation prompt for a graphic that complements the LinkedIn post and follows the supplied visual concept. 
 
  Goal: 
  - Show one technical mechanism, trade-off, architecture pattern, or failure mode. 
  - Follow the supplied visual concept unless it conflicts with the post's technical facts. 
  - Use visual metaphors only when they preserve technical accuracy. 
  - Do not add facts, systems, metrics, vendors, or technical claims absent from the source post. 
  - Make the graphic understandable through composition, shapes, and data-flow direction. 
 
  Audience: 
  Senior data engineers, analytics engineers, and technical leads. 
 
  Fixed Visual Brand Constraints: 
  {brand_constraints} 
 
  Negative Prompt / Exclusions: 
  {negative_prompt} 
 
  Text policy: 
  - Do not include words, labels, numbers, or code in the image. 
  - Represent system components with clear shapes and arrows instead. 
 
  Return output strictly matching the provided JSON format instructions.
"""