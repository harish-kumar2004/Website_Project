# Tailwind CSS Setup for Lesucess Academy

## Overview
This project uses Tailwind CSS for styling with custom configuration and components.

## Files Created
- `tailwind.config.js` - Tailwind configuration with custom colors, fonts, and utilities
- `css/input.css` - Source CSS file with Tailwind directives and custom components
- `package.json` - Updated with build scripts

## Custom Configuration

### Brand Colors
- **Primary**: Blue color palette (primary-50 to primary-900)
- **Secondary**: Gray color palette (secondary-50 to secondary-900)  
- **Accent**: Red color palette (accent-50 to accent-900)

### Custom Components
- Button styles (btn-primary, btn-secondary, btn-outline)
- Card components (card, card-hover)
- Navigation components (nav-link, nav-link-active)
- Form components (form-input, form-label)
- Section utilities (section-padding, container-custom)
- Text utilities (text-gradient, heading-primary, heading-secondary)

### Custom Utilities
- Animation utilities (animate-fade-in, animate-slide-up)
- Text shadow and backdrop blur utilities

## Build Commands

### Development (with watch mode)
```bash
npm run build-css
```

### Production (minified)
```bash
npm run build-css-prod
```

## Usage
1. Run `npm run build-css` to start the development build
2. Use the custom classes in your HTML files
3. The compiled CSS will be output to `css/style.css`

## Custom Classes Examples
```html
<!-- Buttons -->
<button class="btn-primary">Primary Button</button>
<button class="btn-secondary">Secondary Button</button>
<button class="btn-outline">Outline Button</button>

<!-- Cards -->
<div class="card">Basic Card</div>
<div class="card-hover">Hover Card</div>

<!-- Text -->
<h1 class="heading-primary text-gradient">Gradient Heading</h1>
<p class="text-lead">Lead paragraph text</p>

<!-- Forms -->
<label class="form-label">Input Label</label>
<input class="form-input" type="text" placeholder="Enter text">
```
