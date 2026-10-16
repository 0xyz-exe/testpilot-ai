# UI/UX Design Brief — TestPilot AI

**Version:** 1.0  
**Date:** 2026-10-16

## 1. Design Philosophy

TestPilot AI is a **professional developer tool**, not a consumer app or chat interface.

### Design Principles
- **Evidence-first:** Real execution results take priority over AI suggestions
- **Status clarity:** Test states (PASSED/FAILED/RUNNING) immediately visible
- **Artifact access:** One click from result → screenshot/trace
- **Progressive disclosure:** Hide complexity until needed
- **Keyboard-driven:** Critical flows navigable without mouse
- **Dark-mode native:** Dark theme default, light available

### Visual Language
- **Typography:** Monospace for code, sans-serif for UI (system fonts)
- **Color:** Semantic status colors (green=pass, red=fail, yellow=flaky, blue=running)
- **Spacing:** Generous whitespace, clear grouping
- **Icons:** Minimal, functional (test status, artifacts, actions)

## 2. Theme System

### Dark Theme (default)
- Background: `#0a0a0a`
- Surface: `#1a1a1a`
- Border: `#2a2a2a`
- Text primary: `#e5e5e5`
- Text secondary: `#a3a3a3`
- Accent: `#3b82f6`

### Light Theme
- Background: `#ffffff`
- Surface: `#f9fafb`
- Border: `#e5e7eb`
- Text primary: `#0a0a0a`
- Text secondary: `#6b7280`
- Accent: `#3b82f6`

### Status Colors
- **PASSED:** `#10b981` (green)
- **FAILED:** `#ef4444` (red)
- **TIMEOUT:** `#f59e0b` (amber)
- **ERROR:** `#ef4444` (red)
- **RUNNING:** `#3b82f6` (blue, animated)
- **SKIPPED:** `#6b7280` (gray)
- **FLAKY:** `#f59e0b` (amber, with icon)
- **DRAFT:** `#8b5cf6` (purple)

## 3. Required Screens

### S-001: Project Dashboard
**Purpose:** Overview of all projects

**Layout:**
```
┌─────────────────────────────────────────┐
│ [+ New Project]              [@user ▼] │
├─────────────────────────────────────────┤
│ My Projects                             │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Project Alpha                  •••  │ │
│ │ 45 tests • 89% pass rate            │ │
│ │ Last run: 2m ago                    │ │
│ │ [12 PASSED] [2 FAILED] [1 FLAKY]    │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ E-Commerce Staging          •••     │ │
│ │ 128 tests • 94% pass rate           │ │
│ │ Last run: 15m ago                   │ │
│ │ [120 PASSED] [8 FAILED]             │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Components:**
- Project card: name, test count, pass rate, recent status badges
- Empty state: "No projects yet. Create your first test project."
- Action menu (•••): Edit, Delete, Settings
- Global nav: Projects | Settings | Docs

### S-002: Project Detail
**Purpose:** View suites and tests within a project

**Layout:**
```
┌─────────────────────────────────────────┐
│ ← Projects / Project Alpha              │
├─────────────────────────────────────────┤
│ [+ New Suite] [+ Generate Test] [⚙]    │
│                                         │
│ 📊 Overview                             │
│ 45 tests | 40 passed | 5 failed        │
│ Flaky: 1 | Last run: 2m ago            │
│                                         │
│ Test Suites ────────────────────────    │
│                                         │
│ ▶ Authentication (8 tests)              │
│   ✓ Login with valid credentials        │
│   ✗ Login with invalid password  [DIAG] │
│   ✓ Logout flow                         │
│   ...                                   │
│                                         │
│ ▶ Shopping Cart (12 tests)              │
│   ✓ Add product to cart                 │
│   ⚠ Remove product (FLAKY)       [HIST] │
│   ...                                   │
└─────────────────────────────────────────┘
```

**Components:**
- Collapsible suite sections
- Test rows: status icon, name, actions (Run, History, Diagnose, Edit)
- Status badges: ✓ ✗ ⚠ • (running)
- Quick actions: [DIAG] diagnosis, [HIST] history
- Empty state: "No test suites. Create one or generate from requirements."

### S-003: Test Detail
**Purpose:** View single test with execution history

**Layout:**
```
┌─────────────────────────────────────────┐
│ ← Project Alpha / Auth Suite           │
│                                         │
│ Login with valid credentials            │
│ Status: FAILED • 2m ago • Chromium 130  │
│                                         │
│ [▶ Run Test] [🔧 Diagnose] [✏ Edit]    │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Latest Run (Failed)                 │ │
│ │ Duration: 3.2s • Retries: 1         │ │
│ │                                     │ │
│ │ Error:                              │ │
│ │ Timeout 30000ms exceeded waiting    │ │
│ │ for selector "button[type=submit]"  │ │
│ │                                     │ │
│ │ 📸 Screenshot  📊 Trace  📝 Logs    │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ History ────────────────────────────    │
│ ┌─────────────────────────────────────┐ │
│ │ ✗ 2m ago • 3.2s • Timeout           │ │
│ │ ✓ 1h ago • 2.8s                     │ │
│ │ ✓ 3h ago • 2.9s                     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Components:**
- Test metadata: status, timestamp, browser
- Action buttons: Run, Diagnose, Edit
- Error message (monospace, highlighted)
- Artifact links (open in modal or download)
- History timeline: status, duration, timestamp
- Compare button (select 2 runs)

### S-004: Test Generator
**Purpose:** AI-assisted test creation

**Layout:**
```
┌─────────────────────────────────────────┐
│ Generate Test                           │
├─────────────────────────────────────────┤
│ Describe what the test should verify:   │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Verify that a user can sign in with │ │
│ │ valid credentials                   │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Suite: [Authentication ▼]               │
│ Browser: [Chromium ▼]                   │
│                                         │
│              [Generate Draft]           │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📝 Generated Test (Draft)           │ │
│ │                                     │ │
│ │ test('user login', async ({page})=> │ │
│ │   await page.goto('/login');        │ │
│ │   await page.fill('#email', 'u@...');│ │
│ │   await page.fill('#pass', 'pass'); │ │
│ │   await page.click('button[type=... │ │
│ │   await expect(page).toHaveURL(...  │ │
│ │ });                                 │ │
│ │                                     │ │
│ │ [✓ Approve & Save] [✏ Edit] [✗]    │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Components:**
- Textarea: natural language requirement
- Dropdowns: target suite, browser
- Generate button (disabled if AI unavailable)
- Code preview: syntax-highlighted Playwright test
- Warning: "Review generated code before approving"
- Approve button: saves test to suite
- Edit mode: modify generated code before saving

### S-005: Failure Diagnosis
**Purpose:** AI + rule-based failure analysis

**Layout:**
```
┌─────────────────────────────────────────┐
│ Diagnosis: Login Test Failure           │
├─────────────────────────────────────────┤
│ 🔍 Analysis Complete                    │
│                                         │
│ Likely Cause                            │
│ Selector timeout — button not found     │
│                                         │
│ Evidence                                │
│ • Error: Timeout waiting for selector  │
│ • Screenshot: Button missing from DOM  │
│ • Console: No JavaScript errors        │
│ • Network: All requests succeeded      │
│                                         │
│ Recommended Fix                         │
│ Update selector to match current DOM:   │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ - await page.click('button[type=... │ │
│ │ + await page.click('button.submit-  │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [Apply Fix] [Edit Test] [Re-run]       │
│                                         │
│ ℹ️ Diagnosis powered by: Rules + GPT-4  │
└─────────────────────────────────────────┘
```

**Components:**
- Analysis status indicator
- Cause summary (bold, prominent)
- Evidence list with artifact links
- Diff viewer for suggested changes
- Action buttons: Apply (updates test), Edit, Re-run
- Attribution: show if AI-enhanced or rules-only

### S-006: Test History & Comparison
**Purpose:** Track test runs over time

**Layout:**
```
┌─────────────────────────────────────────┐
│ Test History: Login Test                │
├─────────────────────────────────────────┤
│ Filter: [All ▼] [Last 7 days ▼]        │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ✗ Oct 16, 19:42 • 3.2s • Timeout   │ │
│ │ ✓ Oct 16, 18:15 • 2.8s              │ │
│ │ ✓ Oct 16, 17:30 • 2.9s              │ │
│ │ ✗ Oct 16, 16:45 • 5.1s • Assertion │ │
│ │ ✓ Oct 16, 15:00 • 2.7s              │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [Select runs to compare]                │
│                                         │
│ Comparison ─────────────────────────    │
│                                         │
│ Run A (Oct 16, 19:42) ↔ Run B (18:15)  │
│                                         │
│ Status:    FAILED      →    PASSED      │
│ Duration:  3.2s        →    2.8s        │
│ Error:     Timeout     →    None        │
│                                         │
│ [View Screenshot A] [View Screenshot B] │
└─────────────────────────────────────────┘
```

**Components:**
- Timeline: reverse chronological, paginated
- Filters: status, date range
- Selectable rows (checkbox for comparison)
- Comparison view: side-by-side diff
- Duration chart (optional): line graph over time

### S-007: Flaky Test Dashboard
**Purpose:** Identify unreliable tests

**Layout:**
```
┌─────────────────────────────────────────┐
│ Flaky Tests                             │
├─────────────────────────────────────────┤
│ 3 tests marked as flaky                 │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ⚠ Remove Product from Cart          │ │
│ │ Flakiness: 40% (4/10 failures)      │ │
│ │ Last 10 runs: ✓✗✓✗✓✓✗✓✓✓          │ │
│ │ [View History] [Investigate]        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ⚠ Checkout Flow                     │ │
│ │ Flakiness: 30% (3/10 failures)      │ │
│ │ Last 10 runs: ✓✓✗✓✓✗✓✓✗✓          │ │
│ │ [View History] [Investigate]        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Components:**
- Flaky test cards: name, flakiness %, recent run pattern
- Visual run indicator: ✓✗ sequence
- Action buttons: View history, Investigate (detailed diagnosis)
- Empty state: "No flaky tests detected. Good job!"

### S-008: Project Settings
**Purpose:** Configure project-level settings

**Layout:**
```
┌─────────────────────────────────────────┐
│ Project Settings: Project Alpha         │
├─────────────────────────────────────────┤
│ General ───────────────────────────     │
│                                         │
│ Project Name                            │
│ [Project Alpha                        ] │
│                                         │
│ Authorized URLs ───────────────────     │
│ Tests can only run against these URLs   │
│                                         │
│ [http://localhost:3000                ] │
│ [https://staging.myapp.com            ] │
│ [+ Add URL]                             │
│                                         │
│ Execution ─────────────────────────     │
│                                         │
│ Default Timeout: [30] seconds           │
│ Max Retries: [3]                        │
│ Browser: [Chromium ▼]                   │
│                                         │
│ Artifacts ─────────────────────────     │
│                                         │
│ Screenshot on Failure: [✓]              │
│ Capture Traces: [✓]                     │
│ Retention: Keep last [100] runs         │
│                                         │
│                    [Save Changes]       │
└─────────────────────────────────────────┘
```

**Components:**
- Form fields: text inputs, numbers, checkboxes
- URL list: add/remove authorized targets
- Validation: URLs must be valid HTTP/HTTPS
- Save button (disabled until changes made)

### S-009: AI Provider Configuration
**Purpose:** Configure AI provider settings

**Layout:**
```
┌─────────────────────────────────────────┐
│ AI Provider Settings                    │
├─────────────────────────────────────────┤
│ Provider Type                           │
│ ○ Hosted API (OpenAI, Anthropic)        │
│ ● Local Model (Ollama, LM Studio)       │
│ ○ Disabled                              │
│                                         │
│ Local Model Settings ──────────────     │
│                                         │
│ Endpoint: [http://localhost:11434     ] │
│ Model: [llama3.2                      ] │
│                                         │
│ [Test Connection]  Status: ✓ Connected  │
│                                         │
│ Features Enabled ───────────────────    │
│ ☑ Test Generation                       │
│ ☑ Failure Diagnosis                     │
│                                         │
│ ℹ️ When AI unavailable, deterministic   │
│    fallbacks are used automatically.    │
│                                         │
│                    [Save Settings]      │
└─────────────────────────────────────────┘
```

**Components:**
- Radio buttons: provider type
- Conditional fields based on selection
- Test connection button (validates endpoint)
- Status indicator: connected/error
- Feature toggles
- Info callout: fallback behavior

### S-010: Test Execution Modal
**Purpose:** Real-time execution feedback

**Layout:**
```
┌─────────────────────────────────────────┐
│ Running Test: Login Flow                │
├─────────────────────────────────────────┤
│ ● Running... (8s elapsed)               │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ Navigate to /login                │ │
│ │ ✓ Fill email field                  │ │
│ │ ✓ Fill password field               │ │
│ │ → Clicking submit button...         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Browser: Chromium 130                   │
│ Timeout: 30s                            │
│                                         │
│              [Cancel Test]              │
└─────────────────────────────────────────┘
```

**Components:**
- Live status indicator (animated)
- Step-by-step progress (if available)
- Elapsed time
- Cancel button (kills worker)
- Closes automatically on completion

## 4. Component Library

### Atoms
- **Button:** Primary, Secondary, Danger, Ghost
- **Badge:** Status (PASSED/FAILED/etc), Count
- **Icon:** Status icons, action icons (play, edit, trash)
- **Input:** Text, Number, URL, Textarea
- **Select:** Dropdown with search
- **Checkbox:** Boolean toggle
- **Radio:** Mutually exclusive options

### Molecules
- **TestCard:** Name, status, duration, actions
- **ProjectCard:** Name, metrics, last run
- **StatusBadge:** Icon + label + color
- **ArtifactLink:** Icon + filename + download
- **RunHistoryItem:** Status + timestamp + duration
- **ErrorMessage:** Monospace, scrollable, syntax-highlighted

### Organisms
- **TestList:** Filterable, sortable list of tests
- **DiagnosisPanel:** Cause, evidence, fix
- **ComparisonView:** Side-by-side run diff
- **CodeEditor:** Syntax-highlighted Playwright code
- **HistoryTimeline:** Chronological run list

## 5. Accessibility

### Keyboard Navigation
- Tab order: logical flow through interactive elements
- Escape: Close modals
- Enter: Submit forms, execute default action
- Arrow keys: Navigate lists

### Screen Readers
- ARIA labels on icon-only buttons
- Semantic HTML: `<button>`, `<nav>`, `<main>`, `<article>`
- Status announcements: "Test passed" when execution completes
- Error alerts: aria-live regions for form validation

### Visual
- Color contrast: WCAG AA minimum (4.5:1 text, 3:1 UI)
- Status communicated by icon + color (not color alone)
- Focus indicators: visible outline on interactive elements

## 6. Responsive Behavior

### Desktop (1280px+)
- Sidebar navigation visible
- Two-column layouts (list + detail)
- Code editors full-width

### Tablet (768-1279px)
- Collapsible sidebar
- Single-column layouts
- Horizontal scrolling for wide tables

### Mobile (< 768px)
- MVP: Desktop-first, mobile usable but not optimized
- P2: Full mobile optimization

## 7. Empty States

### No Projects
"No projects yet. Create your first test project to get started."  
[+ Create Project]

### No Tests in Suite
"No tests in this suite. Add a test manually or generate one from a requirement."  
[+ Add Test] [Generate with AI]

### No Execution History
"This test hasn't been run yet."  
[▶ Run Test]

### AI Provider Not Configured
"AI features require a configured provider. Set up in Settings."  
[Configure AI]

### No Flaky Tests
"No flaky tests detected. All tests are stable! 🎉"

## 8. Loading States

### Test Execution
- Spinner + "Running test..." + elapsed time
- Progress steps if available

### AI Generation
- Spinner + "Generating test..." + estimated time
- Timeout indicator (max 30s)

### Data Fetching
- Skeleton screens for lists
- Spinner for single-item loads

## 9. Error States

### Execution Failed
- Red border around error message
- Error text (monospace, scrollable)
- Suggested actions: View diagnosis, Edit test, Retry

### AI Provider Error
- Warning badge: "AI unavailable — using fallback"
- Retry button for transient errors

### Network Error
- Toast notification: "Failed to load data. Retrying..."
- Manual retry button if auto-retry fails

## 10. Implementation Notes

### Frontend Stack
- Next.js 14 (App Router)
- React 18
- TypeScript 5
- Tailwind CSS 3
- shadcn/ui components
- Playwright for E2E tests

### Design System
- Use shadcn/ui primitives (Button, Card, Dialog, Select, etc.)
- Customize with project theme tokens
- Monospace font: `ui-monospace, 'Cascadia Code', 'Fira Code', monospace`
- Sans-serif: `system-ui, -apple-system, sans-serif`

### Performance
- Lazy load heavy components (CodeEditor, Trace viewer)
- Paginate long lists (50 items)
- Virtualize if >200 items

---

**Next:** Architecture design and threat model.
