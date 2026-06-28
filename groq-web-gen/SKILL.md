---
name: groq-web-gen
description: InstaWeb AI Prompt Engineering guidelines for building low-latency, highly customized Indonesian UMKM landing pages.
---

# InstaWeb AI Prompt Engineering Reference

This guide documents the prompt patterns, schemas, and LLM orchestration strategies used in InstaWeb AI.

---

## 1. Orchestration Model Strategy

InstaWeb AI employs a multi-model approach tailored to latency, cost, and complexity:

| Agent / Function | Model Used | Reason | Output Format |
|---|---|---|---|
| **Business Parser** (`extractBusinessProfile`) | `llama-3.1-8b-instant` | Ultra-fast extraction of unstructured user input. | JSON Mode |
| **Website Generator** (`streamWebsiteGeneration`) | `llama-3.3-70b-versatile` | Premium copywriting and complex design decision reasoning. | `<thought>` + `<response>` (XML/JSON) |
| **Component Editor** (`streamComponentRevision`) | `llama-3.1-8b-instant` | Fast, low-latency, low-cost modifications to specific components. | `<thought>` + `<response>` (XML/JSON) |

---

## 2. Meta-Prompt XML Structure

All system prompts in InstaWeb AI follow a unified XML format to maximize instruction adherence by Llama models:

```xml
<generated_prompt>
<role>Define the persona and specialization of the AI agent.</role>
<context>Explain the project context and why this agent is executing the task.</context>
<instructions>
1. Step-by-step logic.
2. Rationale for actions.
</instructions>
<guardrails>
1. Strictest negative constraints.
2. Allowed/disallowed outputs and formatting.
</guardrails>
<expected_output>
Specify exact format (e.g. XML tags, JSON schemas).
</expected_output>
</generated_prompt>
```

---

## 3. Website Layout JSON Schema

The generator maps profiles to this precise schema, which matches the React UI renderers:

```json
{
  "theme": {
    "primary": "#hex_code",
    "secondary": "#hex_code",
    "accent": "#hex_code",
    "background": "#hex_code",
    "text": "#hex_code",
    "font": "font_name (e.g., Inter, Outfit, Playfair Display)",
    "layoutStyle": "minimalist" | "glassmorphism" | "brutalist" | "bento"
  },
  "hero": {
    "title": "Persuasive headline in target language",
    "subtitle": "Supporting benefit description",
    "buttonText": "Action-oriented CTA",
    "imageUrl": "Unsplash query/URL matching theme"
  },
  "about": {
    "title": "Section title",
    "content": "Story or value proposition"
  },
  "products": [
    {
      "id": "1",
      "name": "Product or service name",
      "price": "Formatted price (e.g., Rp 15.000)",
      "description": "Short benefit-focused description",
      "imageUrl": "Unsplash query/URL matching product"
    }
  ],
  "contact": {
    "phone": "WhatsApp format phone number",
    "address": "Store physical location or null",
    "email": "Business email or null"
  }
}
```

---

## 4. Copywriting and Styling Guidelines

1. **Copywriting Tone & Approach**:
   - Copywriting must sound natural, professional, and persuasive to Indonesian consumers. Avoid literal translations of common English taglines.
   - Proactively include local trust signals (e.g., "Halal", "Asli Indonesia", "Bahan Premium", "Garansi 100%").
   - Target local searches by weaving in natural geo-modifiers (e.g., "Terbaik di Jakarta Selatan", "Delivery Bandung").
2. **Design Philosophy**:
   - Do NOT use standard generic SaaS layout templates. Choose layout structures that feel alive, responsive, and tactile.
   - Ensure color palettes match the brand persona exactly using CSS variable-based utility styles (e.g. `bg-primary`, `text-muted-foreground`).

---

## 5. Skill Activation Map

When executing website generations or component revisions, the AI Agent must activate and apply the following local skills:

| Category | Skill Command | Key Utility / Output Pattern |
|---|---|---|
| **Desain & UI/UX** | `/frontend-design` | Direct aesthetic decision-making (grids, typography hierarchy, visual flow). |
| **Desain & UI/UX** | `/ui-ux-pro-max` | Advanced layout structures (Bento grids, micro-interactions, responsive behavior). |
| **Desain & UI/UX** | `/shadcn` | Reusable Radix-based components (`Card`, `Button`, `Dialog`, `Sheet`, `Skeleton`). |
| **Desain & UI/UX** | `/vercel-react-best-practices` | Performance optimization (RSC-first structure, bundle optimization, clean hook dependencies). |
| **SEO & Content** | `/ai-seo` | Structured self-contained answer blocks, structured FAQ schemas, semantic tags for LLM search engines. |
| **SEO & Content** | `/programmatic-seo` | Hub-and-spoke dynamic layouts, template-based location routes, high-value unique text variations. |
| **SEO & Content** | `/seo-sitemap` | Dynamic sitemap.xml validation and URL priority mapping. |

---

## 6. Design Direction Alternatives

To keep landing pages unique and premium, the system prompt enforces selecting one of these 5 layout directions:

### A. Bento Box UI (layoutStyle: `bento`)
- **Structure**: Asymmetric grid of cards (`grid grid-cols-1 md:grid-cols-3 gap-4`).
- **Best For**: Tech catalogs, diverse restaurant menus, complex service menus.
- **Aesthetic**: Rounded corners, interactive glass cards, subtle shadows, clear content boundaries.

### B. Asymmetrical Split-Screen (layoutStyle: `split-screen`)
- **Structure**: Two-column layout where one column holds a large, immersive visual and the other contains clean typography.
- **Best For**: Creative studios, high-end cafes, clothing brands, personal/consultant services.
- **Aesthetic**: Contrast-heavy, elegant text styling, large image containers with subtle parallax-like behavior.

### C. Brutalist / High-Contrast Minimalist (layoutStyle: `brutalist`)
- **Structure**: Flat outlines, heavy borders (`border-4 border-black`), solid drop shadows (`shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]`).
- **Best For**: Youth streetwear, local art galleries, creative agencies, alternative fashion.
- **Aesthetic**: Vibrant neon fill colors, monospaced fonts, no blurs/gradients, highly tactile buttons.

### D. Horizontal Scrolling Sections (layoutStyle: `horizontal-scroll`)
- **Structure**: Side-scrolling cards with overflow-x controllers (`flex overflow-x-auto snap-x scrollbar-none`).
- **Best For**: Portfolio galleries, seasonal bakery menus, event timelines.
- **Aesthetic**: Continuous horizontal swipe experience, pagination dots, immersive swipe gestures.

### E. Card-based Masonry Layout (layoutStyle: `masonry`)
- **Structure**: Multi-column uneven card distribution (`columns-1 md:columns-3 gap-4 [column-fill:_balance]`).
- **Best For**: Testimonials pages, handcraft catalogs, local artists' portfolios.
- **Aesthetic**: Organically sized cards that fill vertical gaps, dynamic and content-driven.

---

## 7. SEO Architecture for InstaWeb

Every generated UMKM page must follow strict SEO guidelines:
1. **Programmatic Route Design**:
   - Services (`jasa`): `/layanan/[jenis-layanan]/[kota]` (e.g., `/layanan/cuci-ac/bandung`)
   - Retail (`ritel` / `makanan`): `/produk/[kategori]/[slug]` (e.g., `/produk/keripik/keripik-singkong-pedas`)
2. **Semantic HTML Rules**:
   - Exactly one `<h1>` per page.
   - Use `<main>` for core content, `<section>` for layout segments, and `<article>` for products/services.
   - Subheadings must follow order: `<h2>` -> `<h3>` (no skipping heading levels).
3. **AI SEO Optimized Content Blocks**:
   - Include direct-answer blocks matching user intents (e.g., "Berapa biaya service AC di Bandung?").
   - Include an structured FAQ component (`FAQPage` Schema markup format).
4. **Sitemap Generation**:
   - Ensure all dynamic routes are registerable under a standard sitemap.xml schema.

---

## 8. shadcn/Tailwind Integration Rules

- **Design System Tokens**: Use Tailwind semantic color tokens (e.g., `bg-background`, `text-foreground`, `border-border`, `bg-primary`, `text-primary-foreground`) instead of hardcoding raw hex values.
- **Component Standard**: Utilize standard shadcn elements (`Card`, `CardHeader`, `CardContent`, `Button`, `Badge`) to build UI containers dynamically.
- **Micro-animations**: Apply CSS hover scale-up, background color transitions, and focus outline animations to interactive elements for a premium feeling.