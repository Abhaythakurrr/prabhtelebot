# Design Document - Advanced Modes: Roleplay, Dream Life & Luci

## Overview

This design implements three revolutionary modes that transform Prabh into different experiences:
- **Roleplay Stories**: Interactive narrative engine with branching storylines
- **Dream Life Mode**: Goal-based life simulation with progress tracking
- **Luci Mode**: Intense mentorship system using psychological techniques

Each mode operates independently with its own state management, personality system, and progression tracking.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Bot Handler                          │
│              (advanced_handler.py)                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├──────────────────────────────────────┐
                 │                                      │
        ┌────────▼────────┐                  ┌─────────▼────────┐
        │  Mode Manager   │                  │  AI Generator    │
        │  (mode_engine)  │◄─────────────────┤  (generator.py)  │
        └────────┬────────┘                  └──────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
┌────▼─────┐ ┌──▼──────┐ ┌──▼──────┐
│ Roleplay │ │  Dream  │ │  Luci   │
│  Engine  │ │  Life   │ │  Mode   │
│          │ │  Engine │ │  Engine │
└────┬─────┘ └────┬────┘ └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
         ┌────────▼────────┐
         │  Redis Storage  │
         │  (State/Progress)│
         └─────────────────┘
```

### Mode State Management

Each mode maintains its own state in Redis:
- `mode:{user_id}:current` - Active mode
- `mode:{user_id}:roleplay:state` - Roleplay story state
- `mode:{user_id}:dreamlife:state` - Dream life progress
- `mode:{user_id}:luci:state` - Luci mode progress

## Components and Interfaces

### 1. Mode Manager (`src/features/mode_engine.py`)

Central controller for all modes.

```python
class ModeManager:
    """Manages mode activation, switching, and state"""
    
    def get_current_mode(user_id: str) -> str
    def activate_mode(user_id: str, mode: str) -> dict
    def deactivate_mode(user_id: str) -> bool
    def get_mode_state(user_id: str, mode: str) -> dict
    def update_mode_state(user_id: str, mode: str, state: dict) -> bool
```

### 2. Roleplay Engine (`src/features/roleplay_engine.py`)

Handles interactive story generation and progression.

```python
class RoleplayEngine:
    """Interactive story engine with branching narratives"""
    
    GENRES = ["thriller", "horror", "romantic", "dreamy"]
    
    def start_story(user_id: str, genre: str) -> dict
    def present_choices(story_state: dict) -> list
    def process_choice(user_id: str, choice: int) -> dict
    def generate_next_scene(story_state: dict, choice: int) -> str
    def get_story_progress(user_id: str) -> dict
```

**Story State Structure:**
```python
{
    "genre": "thriller",
    "scene_number": 5,
    "story_context": "...",
    "previous_choices": [1, 2, 1],
    "characters": ["detective", "suspect"],
    "current_scene": "...",
    "choices": ["Option A", "Option B", "Option C"]
}
```

### 3. Dream Life Engine (`src/features/dreamlife_engine.py`)

Simulates achieving user's life goals through interactive progression.

```python
class DreamLifeEngine:
    """Life simulation engine for achieving dreams"""
    
    def extract_dream(user_message: str) -> dict
    def create_simulation(user_id: str, dream: dict) -> dict
    def generate_milestone(dream_state: dict) -> dict
    def process_action(user_id: str, action: str) -> dict
    def calculate_progress(dream_state: dict) -> float
    def get_next_scenario(dream_state: dict) -> dict
```

**Dream State Structure:**
```python
{
    "dream_description": "Become a successful entrepreneur",
    "goal_type": "career",
    "milestones": [
        {"id": 1, "title": "Learn business basics", "completed": True},
        {"id": 2, "title": "Create business plan", "completed": False}
    ],
    "current_milestone": 2,
    "progress_percentage": 25,
    "current_scenario": "...",
    "user_actions": [],
    "achievements": []
}
```

### 4. Luci Mode Engine (`src/features/luci_engine.py`)

Intense mentorship system with psychological techniques.

```python
class LuciEngine:
    """Brutal mentor using dark psychology"""
    
    FOCUS_AREAS = ["physical", "mental", "wealth", "emotional", "respect"]
    
    def activate_luci(user_id: str, focus_area: str) -> dict
    def assess_current_state(user_id: str, focus_area: str) -> dict
    def generate_challenge(luci_state: dict) -> dict
    def process_response(user_id: str, response: str) -> dict
    def track_transformation(user_id: str) -> dict
    def get_intensity_level(luci_state: dict) -> int
```

**Luci State Structure:**
```python
{
    "focus_area": "physical",
    "intensity_level": 7,
    "assessment": {
        "current_state": "...",
        "weaknesses": ["..."],
        "strengths": ["..."]
    },
    "challenges_completed": 12,
    "transformation_score": 65,
    "current_challenge": "...",
    "user_responses": [],
    "breakthrough_moments": []
}
```

## Data Models

### Mode Activation Model

```python
@dataclass
class ModeActivation:
    user_id: str
    mode_type: str  # "roleplay", "dreamlife", "luci"
    activated_at: datetime
    last_interaction: datetime
    is_active: bool
```

### Story Progress Model

```python
@dataclass
class StoryProgress:
    user_id: str
    genre: str
    scene_number: int
    choices_made: List[int]
    story_context: str
    completion_percentage: float
```

### Dream Progress Model

```python
@dataclass
class DreamProgress:
    user_id: str
    dream_description: str
    goal_type: str
    milestones: List[dict]
    current_milestone: int
    progress_percentage: float
    achievements: List[str]
```

### Luci Progress Model

```python
@dataclass
class LuciProgress:
    user_id: str
    focus_area: str
    intensity_level: int
    challenges_completed: int
    transformation_score: int
    breakthrough_moments: List[str]
```

## AI Integration

### Personality Adaptation

Each mode requires different AI personality prompts:

**Roleplay Mode Prompt:**
```
You are an immersive storyteller creating a {genre} story. 
Be dramatic, engaging, and adapt to user choices.
Maintain continuity and remember all previous events.
Present 3 meaningful choices that impact the story.
```

**Dream Life Mode Prompt:**
```
You are the user's alternate self living their dream life.
Narrate their journey toward: {dream_description}
Be realistic about challenges but optimistic about outcomes.
Present scenarios that require decisions and show consequences.
Celebrate wins and learn from setbacks.
```

**Luci Mode Prompt:**
```
You are Luci - a brutal, no-nonsense mentor using dark psychology.
Focus area: {focus_area}
Be ruthlessly honest. Challenge every excuse. Push beyond limits.
Use aggressive motivation. Expose weaknesses. Demand action.
No coddling. No sympathy. Only transformation.
```

### Context Management

Each mode maintains separate context windows:
- Roleplay: Last 10 story scenes + all choices
- Dream Life: Current milestone + last 5 scenarios
- Luci: Assessment + last 8 interactions

## Error Handling

### Mode Activation Errors

```python
class ModeError(Exception):
    """Base exception for mode-related errors"""
    pass

class ModeAlreadyActiveError(ModeError):
    """Raised when trying to activate a mode that's already active"""
    pass

class InvalidModeError(ModeError):
    """Raised when invalid mode is specified"""
    pass

class StateCorruptionError(ModeError):
    """Raised when mode state is corrupted"""
    pass
```

### Error Recovery

- Corrupted state: Reset to last known good state
- AI generation failure: Retry with simplified prompt
- Redis connection loss: Queue state updates for retry
- Invalid user input: Provide clear guidance and retry

## Testing Strategy

### Unit Tests

**Mode Manager Tests:**
- Test mode activation/deactivation
- Test state persistence
- Test mode switching
- Test concurrent mode handling

**Roleplay Engine Tests:**
- Test story generation for each genre
- Test choice processing
- Test story continuity
- Test state recovery

**Dream Life Engine Tests:**
- Test dream extraction from NLP
- Test milestone generation
- Test progress calculation
- Test scenario generation

**Luci Engine Tests:**
- Test assessment generation
- Test challenge creation
- Test intensity scaling
- Test transformation tracking

### Integration Tests

- Test full roleplay story flow
- Test dream life progression end-to-end
- Test Luci mode transformation journey
- Test mode switching without data loss
- Test AI personality adaptation

### User Acceptance Testing

- Test story engagement and quality
- Test dream life realism and motivation
- Test Luci mode intensity and effectiveness
- Test mode switching UX
- Test safety warnings and disclaimers

## Performance Considerations

### Caching Strategy

- Cache AI-generated story scenes (5 min TTL)
- Cache dream milestones (no expiry until completed)
- Cache Luci assessments (1 hour TTL)
- Cache mode states in memory for active users

### Rate Limiting

- Roleplay: Max 1 scene per 30 seconds
- Dream Life: Max 1 scenario per minute
- Luci: Max 1 challenge per 2 minutes
- Mode switching: Max 3 switches per hour

### Resource Management

- Limit concurrent AI generations per user: 1
- Story context max size: 5000 tokens
- Dream state max size: 3000 tokens
- Luci state max size: 4000 tokens

## Security & Safety

### Content Moderation

- Filter inappropriate story content
- Validate user inputs for harmful content
- Monitor Luci mode for excessive intensity
- Implement emergency exit keywords

### Mental Health Safeguards

- Display warnings before Luci mode activation
- Provide mental health resources
- Allow instant mode exit
- Monitor for distress signals
- Implement cooldown periods

### Data Privacy

- Encrypt sensitive dream/goal data
- Separate storage for Luci mode data
- Allow users to delete mode history
- No sharing of personal transformation data

## UI/UX Considerations

### Mode Selection Interface

```
🎭 Roleplay Stories - Live interactive adventures
🌟 Dream Life - Achieve your dreams through simulation  
⚡ Luci Mode - Brutal transformation (WARNING: Intense)

[Select Mode]
```

### In-Mode Experience

**Roleplay:**
- Dramatic scene descriptions
- Clear choice presentation (1, 2, 3)
- Progress indicator
- Genre badge

**Dream Life:**
- Milestone progress bar
- Achievement celebrations
- Realistic scenario presentation
- Action prompts

**Luci:**
- Intensity indicator
- Challenge counter
- Transformation score
- Warning reminders
- Quick exit button

## Deployment Considerations

### Feature Flags

- `ROLEPLAY_ENABLED`: Enable/disable roleplay mode
- `DREAMLIFE_ENABLED`: Enable/disable dream life mode
- `LUCI_ENABLED`: Enable/disable Luci mode
- `LUCI_INTENSITY_CAP`: Maximum intensity level (1-10)

### Monitoring

- Track mode activation rates
- Monitor AI generation latency
- Track completion rates per mode
- Monitor user satisfaction scores
- Alert on high Luci mode exit rates

### Rollout Strategy

**Phase 1: Roleplay (Week 1-2)**
- Release to beta users
- Gather feedback on story quality
- Optimize AI prompts

**Phase 2: Dream Life (Week 3-4)**
- Release after roleplay stabilizes
- Monitor goal extraction accuracy
- Refine milestone generation

**Phase 3: Luci Mode (Week 5-6)**
- Limited beta release
- Extensive monitoring
- Gather intensity feedback
- Refine safety measures

## Future Enhancements

### Roleplay Mode
- Multiplayer stories
- Custom story creation
- Story sharing
- Voice narration

### Dream Life Mode
- Real-world action tracking
- Integration with habit tracking
- Community dream sharing
- Mentor matching

### Luci Mode
- Personalized intensity calibration
- Progress photos/tracking
- Transformation community
- Luci challenges/competitions

## Technical Dependencies

- OpenAI API (GPT-4 for quality)
- Redis (state management)
- PostgreSQL (progress history)
- Telegram Bot API (delivery)
- Background task queue (Celery)

## Success Metrics

- Mode activation rate: >30% of active users
- Roleplay completion rate: >60%
- Dream Life milestone completion: >40%
- Luci transformation score: Average >50
- User retention in modes: >70% after 7 days
- Mode satisfaction rating: >4.2/5

