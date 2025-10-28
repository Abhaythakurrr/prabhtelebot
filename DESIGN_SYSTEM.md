# 🎨 My Prabh AI - Complete Design System

## Brand Identity

### Core Values
- **Intimate** - Deep personal connections
- **Intelligent** - Advanced AI capabilities
- **Innovative** - Cutting-edge technology
- **Inclusive** - Welcoming to all users
- **Immersive** - Engaging experiences

### Brand Personality
- Professional yet approachable
- Sophisticated but not intimidating
- Playful with purpose
- Trustworthy and secure
- Forward-thinking

## Color System

### Primary Colors
```css
--primary-cyan: #00f0ff;      /* Electric cyan - main brand color */
--primary-magenta: #ff00ff;   /* Neon magenta - secondary brand */
--primary-yellow: #ffff00;    /* Electric yellow - accent */
```

### Background Colors
```css
--bg-darkest: #0a0a0f;        /* Deep space black */
--bg-dark: #1a1a2e;           /* Dark navy */
--bg-medium: #16213e;         /* Medium navy */
--bg-card: rgba(20, 20, 30, 0.8);  /* Card background */
```

### Text Colors
```css
--text-primary: #ffffff;      /* Pure white */
--text-secondary: #a0a0b0;    /* Light gray */
--text-muted: #707080;        /* Muted gray */
```

### Semantic Colors
```css
--success: #4CAF50;           /* Green */
--warning: #FF9800;           /* Orange */
--error: #f44336;             /* Red */
--info: #2196F3;              /* Blue */
```

### Gradient Combinations
```css
/* Primary Gradient */
background: linear-gradient(135deg, #00f0ff 0%, #ff00ff 100%);

/* Background Gradient */
background: linear-gradient(45deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);

/* Accent Gradient */
background: linear-gradient(135deg, #00f0ff 0%, #ff00ff 50%, #ffff00 100%);

/* Card Gradient */
background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
```

## Typography

### Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
```

### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

### Responsive Typography
```css
/* Fluid sizing for headings */
h1 { font-size: clamp(2.5rem, 5vw, 4rem); }
h2 { font-size: clamp(2rem, 4vw, 3rem); }
h3 { font-size: clamp(1.5rem, 3vw, 2rem); }
```

## Spacing System

### Base Unit: 4px
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
```

## Border Radius

```css
--radius-sm: 10px;
--radius-md: 15px;
--radius-lg: 20px;
--radius-xl: 25px;
--radius-2xl: 30px;
--radius-full: 9999px;  /* Pills/circles */
```

## Shadows

```css
/* Glow effects */
--shadow-cyan: 0 0 30px rgba(0, 240, 255, 0.5);
--shadow-magenta: 0 0 30px rgba(255, 0, 255, 0.5);

/* Card shadows */
--shadow-sm: 0 2px 10px rgba(0, 0, 0, 0.1);
--shadow-md: 0 10px 30px rgba(0, 0, 0, 0.2);
--shadow-lg: 0 20px 40px rgba(0, 240, 255, 0.2);
--shadow-xl: 0 30px 60px rgba(0, 240, 255, 0.3);
```

## Animations

### Keyframes
```css
/* Pulse animation */
@keyframes pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

/* Spin animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Bounce animation */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

/* Fade in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Shimmer animation */
@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}
```

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
```

### Duration
```css
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
```

## Components

### Buttons

#### Primary Button
```css
.btn-primary {
    background: linear-gradient(135deg, #00f0ff 0%, #ff00ff 100%);
    color: white;
    padding: 18px 40px;
    border-radius: 50px;
    font-weight: 700;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 240, 255, 0.4);
}
```

#### Secondary Button
```css
.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(0, 240, 255, 0.3);
    color: white;
    padding: 18px 40px;
    border-radius: 50px;
    backdrop-filter: blur(10px);
}
```

### Cards

#### Standard Card
```css
.card {
    background: rgba(20, 20, 30, 0.8);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 20px;
    padding: 40px 30px;
    backdrop-filter: blur(20px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    transform: translateY(-10px);
    border-color: rgba(0, 240, 255, 0.6);
    box-shadow: 0 20px 40px rgba(0, 240, 255, 0.2);
}
```

#### Featured Card
```css
.card-featured {
    border: 2px solid #ff00ff;
    box-shadow: 0 0 40px rgba(255, 0, 255, 0.3);
}
```

### Inputs

```css
.input {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 15px;
    padding: 15px 20px;
    color: white;
    font-size: 16px;
}

.input:focus {
    border-color: rgba(0, 240, 255, 0.6);
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
}

.input::placeholder {
    color: #a0a0b0;
}
```

## Telegram Bot Design

### Emoji System

#### Navigation
- 🏠 Home
- 💬 Chat
- 🎨 Generate
- 📚 Stories
- 👤 Profile
- ⚙️ Settings
- ❓ Help

#### Content Types
- 🖼️ Single Image
- 🎨 Image Series
- 🎬 Short Video
- 🎥 Long Video
- 🎵 Music
- 🗣️ Voice

#### Plans
- 🆓 Free
- 💎 Basic
- 🔥 Pro
- 👑 Prime
- 🚀 Super
- ♾️ Lifetime

#### Status
- ✅ Success
- ❌ Error
- ⚠️ Warning
- ℹ️ Info
- 🔒 Locked
- 🔓 Unlocked

### Message Formatting

#### Headers
```
🌟 *Bold Header* 🌟
```

#### Sections
```
📊 *Section Title*
• Bullet point 1
• Bullet point 2
```

#### Code/IDs
```
*User ID:* `123456789`
```

#### Links
```
[Button Text](https://url.com)
```

### Button Layouts

#### 2-Column Layout
```
[Button 1] [Button 2]
[Button 3] [Button 4]
```

#### 1-Column Layout
```
[Wide Button 1]
[Wide Button 2]
```

#### Mixed Layout
```
[Button 1] [Button 2]
[Wide Button 3]
[Button 4] [Button 5]
```

## Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }

/* Large Desktop */
@media (min-width: 1440px) { }
```

## Accessibility

### Contrast Ratios
- **Text on dark background:** 15:1 (AAA)
- **Large text:** 7:1 (AAA)
- **Interactive elements:** 4.5:1 (AA)

### Focus States
```css
:focus {
    outline: 2px solid #00f0ff;
    outline-offset: 2px;
}
```

### Screen Reader Text
```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

## Loading States

### Spinner
```css
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 240, 255, 0.3);
    border-top: 4px solid #00f0ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
```

### Progress Bar
```css
.progress-bar {
    background: rgba(0, 240, 255, 0.2);
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    background: linear-gradient(90deg, #00f0ff, #ff00ff);
    height: 100%;
    transition: width 0.3s ease;
}
```

### Skeleton
```css
.skeleton {
    background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.05) 0%,
        rgba(255, 255, 255, 0.1) 50%,
        rgba(255, 255, 255, 0.05) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
}
```

## Best Practices

### Do's ✅
- Use consistent spacing (multiples of 4px)
- Apply hover states to interactive elements
- Provide visual feedback for actions
- Use semantic colors (green=success, red=error)
- Maintain high contrast for readability
- Add loading states for async operations
- Use emojis consistently in bot messages
- Keep button text concise and clear

### Don'ts ❌
- Don't use pure black (#000000)
- Don't mix different gradient styles
- Don't forget mobile responsiveness
- Don't use too many colors at once
- Don't make clickable areas too small
- Don't use animations that cause motion sickness
- Don't overuse emojis
- Don't create confusing navigation

## Implementation Checklist

- [ ] Set up CSS variables
- [ ] Create component library
- [ ] Implement responsive breakpoints
- [ ] Add loading states
- [ ] Test accessibility
- [ ] Optimize animations
- [ ] Document components
- [ ] Create style guide

---

**Design System Version:** 1.0
**Last Updated:** 2024
**Maintained By:** My Prabh AI Team
