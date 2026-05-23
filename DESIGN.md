---
name: Precision Engineering Portfolio
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#464555'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#515f74'
  on-secondary: '#ffffff'
  secondary-container: '#d5e3fc'
  on-secondary-container: '#57657a'
  tertiary: '#3e495d'
  on-tertiary: '#ffffff'
  tertiary-container: '#566175'
  on-tertiary-container: '#d1dcf4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#d5e3fc'
  secondary-fixed-dim: '#b9c7df'
  on-secondary-fixed: '#0d1c2e'
  on-secondary-fixed-variant: '#3a485b'
  tertiary-fixed: '#d8e3fb'
  tertiary-fixed-dim: '#bcc7de'
  on-tertiary-fixed: '#111c2d'
  on-tertiary-fixed-variant: '#3c475a'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 64px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '800'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.3'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.05em
  code-sm:
    fontFamily: jetbrainsMono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1120px
  gutter: 24px
  margin-mobile: 20px
  section-gap-lg: 128px
  section-gap-md: 80px
---

## Brand & Style

The design system is built for a Software Engineer who prioritizes technical excellence, clarity, and precision. The brand personality is **authoritative yet approachable**, evoking an emotional response of trust, reliability, and high-level craftsmanship. 

The aesthetic follows a **High-End Minimalist** movement. It utilizes significant whitespace to allow technical content to breathe, emphasizing a "less is more" philosophy. Visual interest is generated through perfect alignment, micro-interactions, and a sophisticated typographic scale rather than decorative ornamentation. The design is bright, airy, and clinical, reflecting the clean code and architectural rigor of the engineer’s work.

## Colors

The color palette is anchored in high-clarity neutrals to maintain a professional, "SaaS-native" atmosphere.

- **Primary (Deep Indigo):** Used sparingly for key actions, focus states, and critical highlights. It represents innovation and technical depth.
- **Secondary (Slate Gray):** Employed for body text and icon outlines to reduce eye strain compared to pure black.
- **Neutral (Off-White/White):** The foundation of the design. Use `#FFFFFF` for cards and active surfaces, and `#F9FAFB` for background sections to create subtle depth transitions.
- **Accent (Dark Slate):** Used for primary headings and high-contrast UI elements to ensure a strong visual hierarchy.

## Typography

The design system utilizes **Inter** as its primary typeface to provide a systematic, utilitarian aesthetic that remains highly readable at all scales.

- **Headlines:** Use tight letter-spacing and heavy weights (Bold/ExtraBold) to create a "locked-in" professional look.
- **Body Text:** Set with generous line height (1.6) to ensure long-form technical descriptions are accessible and easy to scan.
- **Labels:** Small caps or all-caps with increased letter-spacing are used for categories and metadata (e.g., tech stacks).
- **Code:** For snippets or technical skill blocks, **JetBrains Mono** is introduced to provide a familiar developer-centric environment.

## Layout & Spacing

This design system follows a **Fixed Grid** model for desktop, centering the content within a 1120px container to maintain focus.

- **The 8px Rhythm:** All spacing (padding, margins, gaps) must be a multiple of 8px. 
- **Sectioning:** Large vertical gaps (128px) should separate major sections (Hero, Projects, Skills) to emphasize the minimalist narrative.
- **Mobile Adaptivity:** On mobile devices, the layout transitions to a fluid single-column grid with 20px side margins. 
- **Alignment:** Use consistent vertical alignment. Elements should feel "anchored" to a common axis to reinforce the feeling of systematic engineering.

## Elevation & Depth

To maintain a clean, professional aesthetic, this design system avoids heavy shadows in favor of **Tonal Layers** and **Low-Contrast Outlines**.

- **Surfaces:** The background uses the neutral off-white. Interaction surfaces (like cards) use pure white to appear "lifted."
- **Borders:** Use subtle 1px borders in a light gray (#E2E8F0) instead of shadows to define component boundaries. 
- **Soft Ambient Elevation:** For hover states on project cards, apply a very large, diffused shadow with very low opacity: `0px 20px 40px rgba(0, 0, 0, 0.04)`.
- **Glassmorphism:** Reserved exclusively for the global navigation bar—use a high-blur backdrop (20px) and a semi-transparent white background (80% opacity) to maintain context as the user scrolls.

## Shapes

The shape language is **Soft and Precise**. 

A roundedness level of `1` (0.25rem/4px) is the standard for technical components like input fields, buttons, and skill tags. This provides a subtle friendliness while maintaining the sharp, architectural edges associated with professional engineering. Large containers like project cards may use `rounded-lg` (8px) to feel more substantial and modern. Avoid pill-shapes except for high-contrast "Status" indicators.

## Components

### Buttons
- **Primary:** Solid Deep Indigo background, white text, 4px corner radius. On hover, darken the indigo slightly.
- **Secondary/Ghost:** Transparent background with a 1px Slate Gray border. Use for less critical actions like "View Source."

### Project Cards
- Pure white background with a 1px border. 
- Feature a high-resolution screenshot or abstract graphic at the top.
- Include a "Tech Stack" footer with small, low-contrast tags.

### Skill Blocks
- Grouped by category (e.g., Frontend, Backend).
- Use a monochromatic approach: light gray background with Dark Slate text.
- Use JetBrains Mono for the skill names to evoke a terminal/coding environment.

### Input Fields
- Minimalist design: Bottom-border only or a very light 4px rounded frame.
- Focus state: The border color transitions to Deep Indigo with a subtle 2px glow.

### Interactive Elements
- **Hover Animations:** Use subtle Y-axis shifts (moving an element 4px up) and opacity transitions (0.2s ease-in-out) to indicate interactivity without being distracting.