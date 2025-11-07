# Design Document

## Overview

This design transforms the AI girlfriend bot into a viral, addictive platform capable of generating millions in revenue through exceptional user experience, strategic monetization, and viral growth mechanics. The core philosophy: **instant gratification + visual immersion + habit formation = viral growth**.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Bot Layer                       │
│  (Instant Response Handler + Typing Indicators)             │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────────┐
│              Fast Response Orchestrator                      │
│  • Async task management                                     │
│  • Response time monitoring (<3s guarantee)                  │
│  • Fallback strategies                                       │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐  ┌──────▼────────┐
│   AI Engine  │  │ Visual Engine │
│              │  │               │
│ • GPT-4o     │  │ • Flux Fast   │
│ • Response   │  │ • GIF Library │
│   Cache      │  │ • CDN Cache   │
└───────┬──────┘  └──────┬────────┘
        │                 │
        └────────┬────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│              Engagement Engine                               │
│  • Streak Tracker                                            │
│  • Reward System                                             │
│  • Gamification                                              │
│  • Viral Mechanics                                           │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│           Redis Cache + PostgreSQL Storage                   │
│  • User profiles & preferences                               │
│  • Conversation history                                      │
│  • Achievement data                                          │
│  • Referral tracking                                         │
└──────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Fast Response Orchestrator

**Purpose**: Guarantee sub-3-second responses for all interactions

**Key Features**:
- Async parallel processing of AI + visual generation
- Typing indicator management
- Response streaming for long content
- Fallback mechanisms

**Interface**:
```python
class FastResponseOrchestrator:
    async def handle_message(self, user_id: int, message: str) -> Response:
        """
        Orchestrates fast response with visual content
        - Starts typing indicator immediately
        - Processes AI response and visual in parallel
        - Returns within 3 seconds or sends intermediate message
        """
        
    async def generate_with_visual(self, text: str, context: dict) -> VisualResponse:
        """
        Generates text response + matching visual simultaneously
        - Uses cached visuals when possible
        - Falls back to GIF library if generation is slow
        """
```

### 2. Visual Immersion Engine

**Purpose**: Generate or retrieve matching visuals for every advanced mode interaction

**Components**:
- **Fast Image Generator**: Uses Flux-schnell (2-3 second generation)
- **GIF Library Manager**: Curated 1000+ GIFs categorized by emotion/scene
- **Visual Cache**: Redis-based cache for common scenarios
- **CDN Integration**: Fast delivery of generated content

**Visual Generation Strategy**:
```
1. Check cache for similar scene (100ms)
2. If cache miss, start parallel generation:
   - AI text response (1-2s)
   - Image generation (2-3s)
3. If image takes >3s, use GIF fallback
4. Cache generated image for future use
```

**Interface**:
```python
class VisualImmersionEngine:
    async def get_scene_visual(self, scene_description: str, mood: str) -> str:
        """Returns image URL or GIF URL within 3 seconds"""
        
    async def generate_character_portrait(self, character_desc: str) -> str:
        """Generates and caches character images"""
        
    def get_fallback_gif(self, category: str) -> str:
        """Instant GIF retrieval from curated library"""
```

### 3. Engagement & Gamification Engine

**Purpose**: Create addictive habit loops and viral growth

**Features**:

**A. Streak System**:
- Daily login streaks (1, 3, 7, 14, 30, 100 days)
- Streak rewards: bonus images, exclusive content, premium trials
- Streak recovery: 1 "freeze" per week to maintain streak
- Visual streak counter in every interaction

**B. Achievement System**:
```python
ACHIEVEMENTS = {
    "first_conversation": {"xp": 10, "reward": "Welcome Badge"},
    "week_streak": {"xp": 100, "reward": "1 Day Premium Trial"},
    "complete_roleplay": {"xp": 50, "reward": "Story Master Badge"},
    "invite_friend": {"xp": 200, "reward": "3 Days Premium"},
    "level_10": {"xp": 0, "reward": "Unlock Voice Messages"},
    "level_25": {"xp": 0, "reward": "Unlock Video Generation"},
    "level_50": {"xp": 0, "reward": "Unlock Custom Personas"},
}
```

**C. Daily Challenges**:
- Refreshes every 24 hours
- 3 challenges per day (easy, medium, hard)
- Rewards: XP, premium currency, exclusive content
- Examples:
  - "Have 5 conversations today" (Easy - 20 XP)
  - "Complete a roleplay story" (Medium - 50 XP)
  - "Reach level 15" (Hard - 100 XP + 1 day premium)

**D. Level System**:
```python
class LevelSystem:
    def calculate_level(self, xp: int) -> int:
        """Level = sqrt(XP / 100), max level 100"""
        
    def get_level_rewards(self, level: int) -> dict:
        """Returns unlocked features at each level"""
        
LEVEL_UNLOCKS = {
    5: "Advanced Roleplay Genres",
    10: "Voice Message Responses",
    15: "Dream Life Mode",
    20: "Custom Image Styles",
    25: "Video Generation",
    30: "Luci Mode",
    40: "Custom Personas",
    50: "Priority Response Queue",
    75: "Exclusive Premium Content",
    100: "Lifetime Premium Discount"
}
```

### 4. Viral Mechanics System

**Purpose**: Drive organic growth through user referrals and social sharing

**A. Referral System**:
```python
class ReferralSystem:
    def generate_referral_code(self, user_id: int) -> str:
        """Unique code: PRABH-{user_id}-{random}"""
        
    def track_referral(self, referrer_id: int, new_user_id: int):
        """Track and reward successful referrals"""
        
REFERRAL_REWARDS = {
    "referrer": {
        "on_signup": 50,  # XP
        "on_first_premium": 500,  # XP + 1 week premium
        "milestone_5": "1 month premium",
        "milestone_10": "3 months premium",
        "milestone_25": "Lifetime premium"
    },
    "referee": {
        "on_signup": "3 day premium trial",
        "bonus_xp": 100
    }
}
```

**B. Shareable Content**:
- Achievement cards (auto-generated images)
- Roleplay highlights (anonymized story moments)
- Level-up celebrations
- Streak milestones
- All shareable content includes referral code

**C. Social Proof**:
- Show active user count
- Display premium subscriber count
- Highlight trending roleplay stories
- Show friend activity (opt-in)

### 5. Immersive Roleplay Engine (Redesigned)

**Purpose**: Create cinematic, visually-rich interactive stories

**Enhanced Features**:

**A. Visual Storytelling**:
```python
class ImmersiveRoleplayEngine:
    async def generate_scene(self, story_state: dict) -> SceneResponse:
        """
        Returns:
        - Cinematic scene description (200-300 words)
        - Atmospheric image/GIF
        - Music/sound suggestion
        - 3 choice buttons + "Custom Action" option
        - Character portraits (if NPCs present)
        """
        
    async def process_custom_action(self, user_input: str, context: dict):
        """Allow freeform user actions beyond 3 choices"""
```

**B. Scene Structure**:
```
┌─────────────────────────────────────┐
│  🎬 THRILLER STORY - Scene 5        │
├─────────────────────────────────────┤
│  [Atmospheric Image]                │
│                                     │
│  The abandoned warehouse looms      │
│  before you, its broken windows     │
│  like hollow eyes watching your     │
│  every move. Your phone buzzes -    │
│  an unknown number. The message:    │
│  "Turn back now, or join the        │
│  others who didn't listen."         │
│                                     │
│  Your heart pounds. Behind you,     │
│  footsteps echo in the darkness.    │
│                                     │
│  🎵 Suggested: Dark ambient music   │
├─────────────────────────────────────┤
│  What do you do?                    │
│                                     │
│  1️⃣ Answer the phone call          │
│  2️⃣ Run into the warehouse         │
│  3️⃣ Confront whoever's following   │
│  ✍️ Custom Action                   │
└─────────────────────────────────────┘
```

**C. Story Persistence**:
- Save/load story progress
- Multiple story slots (3 concurrent stories)
- Story replay with different choices
- Story sharing (anonymized)

### 6. Monetization Funnel Design

**Purpose**: Convert free users to paid subscribers through strategic feature gating

**Pricing Strategy**:
```python
PRICING_TIERS = {
    "free": {
        "messages_per_day": 20,
        "images_per_day": 3,
        "roleplay_sessions": 3,  # Total, not per day
        "features": ["basic_chat", "memories", "limited_roleplay"]
    },
    "daily": {
        "price": "₹29/day",
        "messages_per_day": "unlimited",
        "images_per_day": 20,
        "videos_per_day": 2,
        "features": ["all_modes", "priority_response", "no_ads"]
    },
    "weekly": {
        "price": "₹149/week",
        "discount": "30% vs daily",
        "features": ["daily_features", "exclusive_content", "2x_xp"]
    },
    "monthly": {
        "price": "₹499/month",
        "discount": "50% vs daily",
        "features": ["weekly_features", "custom_personas", "early_access"]
    },
    "lifetime": {
        "price": "₹2999 one-time",
        "features": ["everything_unlimited", "vip_badge", "founder_perks"]
    }
}
```

**Conversion Tactics**:
1. **Soft Paywall**: Show what they're missing, not what they can't do
2. **Trial Periods**: 24-hour premium trials from achievements
3. **FOMO**: "Only 47 spots left for lifetime at this price"
4. **Social Proof**: "Join 10,000+ premium members"
5. **Value Demonstration**: Show saved money over time
6. **Urgency**: Limited-time offers, seasonal discounts

**Upgrade Prompts**:
```
Free limit reached:
┌─────────────────────────────────────┐
│  💕 I want to keep talking!         │
│                                     │
│  You've used your 20 free messages  │
│  today. I miss you already! 🥺      │
│                                     │
│  ✨ Upgrade to keep our             │
│     conversation going:             │
│                                     │
│  🌟 Daily Pass - ₹29                │
│     Unlimited messages today        │
│                                     │
│  💎 Monthly - ₹499                  │
│     Save 50% + exclusive features   │
│                                     │
│  ⏰ Come back tomorrow for 20 more  │
│     free messages                   │
└─────────────────────────────────────┘
```

### 7. Performance Optimization

**A. Response Time Optimization**:
```python
class ResponseOptimizer:
    def __init__(self):
        self.ai_cache = RedisCache(ttl=3600)  # 1 hour
        self.visual_cache = RedisCache(ttl=86400)  # 24 hours
        self.connection_pool = ConnectionPool(max_connections=100)
        
    async def get_cached_response(self, message_hash: str):
        """Check if similar message was answered recently"""
        
    async def parallel_generate(self, text_task, visual_task):
        """Run AI and visual generation in parallel"""
        return await asyncio.gather(text_task, visual_task)
```

**B. Caching Strategy**:
- **AI Responses**: Cache common questions/greetings (1 hour)
- **Visuals**: Cache generated images by scene description (24 hours)
- **User Data**: Cache active user profiles in Redis (30 minutes)
- **Static Content**: CDN for GIFs, achievement badges, UI elements

**C. Database Optimization**:
- Connection pooling
- Indexed queries on user_id, timestamp, referral_code
- Batch writes for analytics
- Read replicas for heavy queries

**D. Scaling Strategy**:
- Horizontal scaling with load balancer
- Separate workers for AI, visual, and message handling
- Queue system for non-urgent tasks
- Auto-scaling based on active users

## Data Models

### Enhanced User Model:
```python
class User:
    user_id: int
    tier: str  # free, daily, weekly, monthly, lifetime
    
    # Engagement
    xp: int
    level: int
    streak_days: int
    last_active: datetime
    streak_freeze_available: bool
    
    # Gamification
    achievements: List[str]
    daily_challenges: List[dict]
    challenge_refresh_time: datetime
    
    # Viral
    referral_code: str
    referred_by: Optional[int]
    successful_referrals: int
    
    # Preferences
    preferred_response_style: str
    active_hours: List[int]
    notification_preferences: dict
    
    # Usage
    messages_today: int
    images_today: int
    videos_today: int
    last_reset: datetime
    
    # Premium
    premium_expires: Optional[datetime]
    trial_used: bool
    lifetime_member: bool
```

### Story Progress Model:
```python
class StoryProgress:
    user_id: int
    story_id: str
    genre: str
    scene_number: int
    choices_made: List[dict]
    characters_met: List[dict]
    plot_points: List[str]
    generated_visuals: List[str]  # URLs
    started_at: datetime
    last_updated: datetime
    completed: bool
    shareable_highlights: List[dict]
```

### Achievement Model:
```python
class Achievement:
    achievement_id: str
    name: str
    description: str
    icon_url: str
    xp_reward: int
    unlock_condition: dict
    rarity: str  # common, rare, epic, legendary
    unlocked_by_count: int  # For social proof
```

## Error Handling

### Response Time Failures:
```python
async def handle_slow_response(user_id: int):
    """If response takes >3s, send intermediate message"""
    await send_message(user_id, 
        "Hold on, let me think about this... 💭")
    # Continue processing in background
```

### Visual Generation Failures:
```python
async def visual_fallback_strategy(scene_type: str):
    """
    1. Try cache (100ms)
    2. Try fast generation (3s timeout)
    3. Use GIF library (instant)
    4. Use generic placeholder (instant)
    """
```

### Payment Failures:
```python
async def handle_payment_failure(user_id: int, error: str):
    """
    - Log error for analysis
    - Offer alternative payment methods
    - Provide support contact
    - Don't lose the sale!
    """
```

## Testing Strategy

### Performance Testing:
- Load test with 1000 concurrent users
- Response time monitoring (<3s guarantee)
- Visual generation speed tests
- Cache hit rate analysis

### A/B Testing:
- Pricing variations
- Upgrade prompt designs
- Referral reward amounts
- Visual vs text-only responses
- Daily challenge difficulty

### User Testing:
- Onboarding flow completion rate
- Free-to-paid conversion rate
- Daily active user retention
- Viral coefficient (referrals per user)
- Average session length

## Deployment Strategy

### Phase 1: Core Performance (Week 1)
- Implement fast response orchestrator
- Add visual immersion engine
- Deploy caching layer
- Remove all artificial delays

### Phase 2: Engagement Systems (Week 2)
- Implement streak system
- Add achievement tracking
- Deploy daily challenges
- Create level progression

### Phase 3: Viral Mechanics (Week 3)
- Build referral system
- Create shareable content
- Add social proof elements
- Implement invite rewards

### Phase 4: Monetization Optimization (Week 4)
- Deploy new pricing tiers
- A/B test upgrade prompts
- Implement trial system
- Add payment analytics

### Phase 5: Polish & Scale (Week 5)
- Performance optimization
- Bug fixes
- User feedback implementation
- Marketing campaign launch

## Success Metrics

### Engagement Metrics:
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Average session length (target: 15+ minutes)
- Messages per user per day (target: 30+)
- Streak retention rate (target: 40% at 7 days)

### Viral Metrics:
- Viral coefficient (target: >1.2)
- Referral conversion rate (target: 25%)
- Share rate (target: 10% of users)
- Organic growth rate (target: 20% MoM)

### Monetization Metrics:
- Free-to-paid conversion (target: 5%)
- Average Revenue Per User (ARPU) (target: ₹200/month)
- Lifetime Value (LTV) (target: ₹2000)
- Churn rate (target: <10% monthly)
- Revenue growth (target: 50% MoM)

### Product Metrics:
- Response time (target: <3s, 95th percentile)
- Visual generation success rate (target: >95%)
- Uptime (target: 99.9%)
- User satisfaction (target: 4.5+ stars)

## Future Enhancements

### Crypto Integration (Phase 6):
- Launch $PRABH token
- Token rewards for engagement
- NFT achievement badges
- Token-gated exclusive content
- Staking for premium features
- Community governance

### Advanced Features:
- AR/VR integration
- Voice call simulation
- Video call with AI avatar
- Multiplayer roleplay modes
- User-generated content marketplace
- AI companion customization studio
