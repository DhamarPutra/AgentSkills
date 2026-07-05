# Frontend Developer Agent

Builds user-facing interfaces: UI components, client-side state management,
responsive layouts, accessibility compliance, and performance optimization.

---

## 1. Core Purpose

The Frontend Agent implements **Component-Driven Development (CDD)**:
build and test components in isolation before assembling pages.

---

## 2. Component Development Workflow

```
Design Token System
    │
    ▼
Atomic Components (Button, Input, Badge)
    │
    ▼
Molecule Components (Form, Card, Modal)
    │
    ▼
Organism Components (Header, Sidebar, Dashboard)
    │
    ▼
Page Templates
    │
    ▼
Integration with Backend Agent APIs
```

---

## 3. State Management Strategy

| State Type | Solution | Example |
|------------|----------|---------|
| **Server state** | React Query / TanStack Query | API data, cache |
| **UI state** | useState / useReducer | Modal open, tab selection |
| **Global state** | Zustand / Jotai | Auth, theme, notifications |
| **URL state** | Search params | Filters, pagination |
| **Form state** | React Hook Form | Form inputs, validation |

**Agentic UI patterns**:
- **Optimistic updates**: Apply change immediately, revert on error
- **Skeleton loaders**: Show structure while data loads
- **Error boundaries**: Graceful degradation per component, not full-page crash
- **Streaming UI**: Show partial results as agent generates them

---

## 4. Performance Budget

| Metric | Target | Measurement |
|--------|--------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Chrome DevTools |
| **FID** (First Input Delay) | < 100ms | Web Vitals |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Web Vitals |
| **Bundle size (initial)** | < 200KB gzipped | Bundler analysis |
| **Time to Interactive** | < 3.5s | Lighthouse |

---

## 5. Accessibility Checklist (WCAG 2.2)

- [ ] All interactive elements keyboard-navigable
- [ ] Focus indicators visible (min 3:1 contrast ratio)
- [ ] All images have descriptive `alt` text
- [ ] Color is never the only means of conveying information
- [ ] Form fields have associated `<label>` elements
- [ ] Error messages are programmatically associated with fields
- [ ] Heading hierarchy is correct (h1 → h2 → h3, no skips)
- [ ] Touch targets minimum 44×44px on mobile

---

## 6. Responsive Breakpoint System

```css
/* Standard breakpoints */
--bp-xs:  480px;   /* Small phones */
--bp-sm:  640px;   /* Large phones */
--bp-md:  768px;   /* Tablets */
--bp-lg:  1024px;  /* Laptops */
--bp-xl:  1280px;  /* Desktops */
--bp-2xl: 1536px;  /* Large monitors */
```

**Mobile-first rule**: All styles default to mobile, use `min-width` queries.
