# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MoodMusicUI** (音信) is a single-page music streaming application built entirely within a single HTML file. It's a peaceful, meditative music experience focused on nature sounds, ambient music, and healing audio content for Chinese-speaking users.

## Architecture

### Monolithic Structure

The entire application is contained in `index.html` (~890 lines). This is an intentional design choice for easy deployment and sharing. The file includes:

- **HTML Structure**: Basic DOM elements with React root container
- **Inline CSS**: Tailwind configuration and custom styles (lines 16-85)
- **Inline JavaScript**: All React components and logic (lines 103-893)

### Key Architectural Patterns

**Component Organization**:
- Components are defined as functional React components using JSX
- All components use `class` attribute (not `className`) since they're transformed by Babel Standalone
- No build step - Babel transforms JSX in-browser

**State Management**:
- React hooks (`useState`, `useEffect`) for local component state
- No global state management library
- Player state and navigation handled through React Router

**Routing**:
- React Router v6.3.0 with `MemoryRouter` (client-side only, no browser history)
- Main routes: `/`, `/discover`, `/profile`, `/artist`, `/album`, `/player`
- Navigation via `useNavigate()` hook

**External Integrations**:
- **Supabase**: Backend-as-a-Service for comments (anonymous, page-specific discussions)
- **External API**: `m-api.changgepd.top/api/skeleton` for artist data
- **Google Photos**: Image hosting
- **DiceBear API**: Auto-generated user avatars

### Shared Components

Located in lines 142-335:
- `TopAppBar`: Navigation header with back button support
- `MiniPlayer`: Fixed bottom player bar (click-through to full player)
- `BottomNav`: Tab navigation (Home, Discover, Profile)
- `CommentButton`: Floating FAB that opens slide-out comment panel

### Page Components

Located in lines 337-870:
- `HomePage`: Landing page with featured content (lines 339-448)
- `DiscoverPage`: Artist discovery with category filtering (lines 450-545)
- `ProfilePage`: User's saved albums and followed artists (lines 547-619)
- `ArtistPage`: Artist details and discography (lines 621-697)
- `AlbumDetailPage`: Album track listing (lines 699-767)
- `PlayerPage`: Full-screen music player with lyrics sync (lines 769-870)

## Design System

### Color Palette

Custom earth-tone color scheme defined in Tailwind config (lines 17-64):
- Primary greens: `#34614d`, `#4c7965`
- Secondary accents: `#3d6754`
- Tertiary browns: `#8f4122`, `#ae5838`
- Surface variants for depth and hierarchy

### Typography

- **Headlines/Serif**: Noto Serif SC (Chinese characters)
- **Body/Sans**: Manrope (Latin characters)
- Applied via Google Fonts (line 9)

### UI Patterns

- **Glass morphism**: Backdrop blur on player components (`.glass-player` class)
- **Rounded corners**: Consistent border radius scale (0.125rem to 9999px)
- **Smooth animations**: CSS transitions for hover states and interactions
- **Mobile-first**: Responsive design with max-width containers

## Development Workflow

### Running the Application

No build process required. Simply open `index.html` in a modern web browser, or serve it via any static file server:

```bash
# Using Python's built-in server
python -m http.server 8000

# Using Node.js http-server
npx http-server

# Or just open directly in a browser
```

### Making Changes

1. Edit `index.html` directly
2. Reload browser to see changes
3. No compilation or bundling step

### Git Workflow

- Main branch: `main`
- No CI/CD pipeline
- Manual deployment (likely to static hosting)

## Important Implementation Details

### Comments System (lines 108-140, 226-335)

- Anonymous user generation with randomized names from `ANON_NAMES` array
- Comments stored in Supabase `page_comments` table
- Scoped by `pathname` (each route has separate comments)
- Auto-generated avatars via DiceBear API
- No authentication required

### Lyrics Animation (PlayerPage, lines 804-817)

- CSS animation `lyrics-scroll` for continuous scrolling
- Animation state controlled by `isPlaying` state
- 15-second loop duration

### Player Progress (lines 822-851)

- CSS animation `progress` for smooth progress bar
- 300-second loop (simulating track duration)
- Thumb position synchronized with bar width

### Category Filtering (DiscoverPage, lines 490-491)

- Dynamic categories derived from artist data
- Filters by `category` field on artist objects
- "全部" (All) shows everything

## Code Conventions

- **Class vs className**: Must use `class` (not `className`) for React props since Babel transforms this
- **Inline styles**: Use `style={{fontVariationSettings: "'FILL' 1"}}` for Material Symbols icons
- **Material Icons**: Use `<span class="material-symbols-outlined">` with FILL variation setting
- **Dark mode**: Use `dark:` prefix (Tailwind dark mode with class strategy)
- **Responsive**: Mobile-first with `md:` breakpoints for tablet/desktop

## Security Considerations

- Supabase anon key is exposed in client-side code (intentional for public access)
- No user authentication system (anonymous comments only)
- CORS-protected external API calls
- No sensitive data in localStorage or sessionStorage

## Browser Compatibility

Requires modern browser with ES6+ support:
- React 18 features
- CSS Grid and Flexbox
- CSS custom properties
- Backdrop filter (for glass morphism)
- CSS animations and transforms

## Known Limitations

- No offline support (all assets loaded from CDN)
- No service worker or PWA features
- Search input is present but not functional (line 501)
- MiniPlayer play/pause buttons are decorative (no actual audio playback)
- Track listing is static (not data-driven)
- No actual audio file integration
