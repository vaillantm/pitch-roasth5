import json
import random
import requests
from datetime import datetime
from supabase import create_client, Client
import streamlit as st
import pandas as pd
import base64

# --- Supabase Config ---
SUPABASE_URL = "https://ekwlberslednlfxhnytq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrd2xiZXJzbGVkbmxmeGhueXRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg4NzAwMzksImV4cCI6MjA2NDQ0NjAzOX0.TaBGlA2c-2CFqpOLyS-yIRrIN56Pcb07ow2Dz-_1yL8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Load Roast Data ---
# --- Embedded Roast Data ---
roast_data = {
    "keyword_roasts": [
    { "keyword": "Uber", "roast": "Uber? More like 'overpriced taxi with attitude.'", "rating": 19 },
    { "keyword": "AI", "roast": "AI: Artificial Ignorance, clearly.", "rating": 6 },
    { "keyword": "Voice", "roast": "Voice assistants? More like 'voice irritants.'", "rating": 22 },
    { "keyword": "Dog", "roast": "Dog? More like 'barking up the wrong tree.'", "rating": 31 },
    { "keyword": "Chat", "roast": "Your chat is as lively as a dead battery.", "rating": 9 },
    { "keyword": "Blockchain", "roast": "Blockchain? More like 'block the fun.'", "rating": 11 },
    { "keyword": "Cloud", "roast": "Cloud computing? More like 'fog of disappointment.'", "rating": 2 },
    { "keyword": "Crypto", "roast": "Crypto? More like 'crippling your finances.'", "rating": 29 },
    { "keyword": "Fintech", "roast": "Fintech or just fancy finance nonsense?", "rating": 3 },
    { "keyword": "SaaS", "roast": "SaaS sounds like a bad acronym for laziness.", "rating": 17 },
    { "keyword": "Food", "roast": "Food startup? Hope you serve more than stale ideas.", "rating": 26 },
    { "keyword": "Fitness", "roast": "Fitness startup? Your gains are in bugs, not muscle.", "rating": 13 },
    { "keyword": "Tutor", "roast": "Tutor? Your lessons must be on how to fail.", "rating": 0 },
    { "keyword": "Farm", "roast": "Farming innovation? More like crop of errors.", "rating": 14 },
    { "keyword": "Drone", "roast": "Drone startup? Sounds like a flying paperweight.", "rating": 10 },
    { "keyword": "Ride", "roast": "Ride-sharing? More like ride to nowhere.", "rating": 1 },
    { "keyword": "Sleep", "roast": "Sleep tech? Hope your product isn't a nightmare.", "rating": 15 },
    { "keyword": "Pet", "roast": "Pet startup? Even your ideas need a walk.", "rating": 27 },
    { "keyword": "Eco", "roast": "Eco-friendly? Your green is just envy.", "rating": 4 },
    { "keyword": "Loan", "roast": "Loan startup? Prepare for a bankruptcy lesson.", "rating": 28 },
    { "keyword": "Bike", "roast": "Bike startup? Spinning wheels, going nowhere.", "rating": 8 },
    { "keyword": "Car", "roast": "Car tech? You drive investors away.", "rating": 6 },
    { "keyword": "Home", "roast": "Home startup? More like house of cards.", "rating": 31 },
    { "keyword": "Data", "roast": "Data startup? Data error: idea not found.", "rating": 16 },
    { "keyword": "Social", "roast": "Social app? Socially awkward, more like.", "rating": 20 },
    { "keyword": "Green", "roast": "Green startup? Your idea's more toxic than helpful.", "rating": 5 },
    { "keyword": "Health", "roast": "Health tech? Your app gives headaches.", "rating": 25 },
    { "keyword": "Chatbot", "roast": "Chatbot? More like chat-boring bot.", "rating": 7 },
    { "keyword": "App", "roast": "App? Another useless icon on my phone.", "rating": 30 },
    { "keyword": "Delivery", "roast": "Delivery? Delivering disappointment on time.", "rating": 12 },
    { "keyword": "Market", "roast": "Market startup? Just a flea market of ideas.", "rating": 18 },
    { "keyword": "Travel", "roast": "Travel tech? Your business plan took a detour.", "rating": 24 },
    { "keyword": "Bot", "roast": "Bot startup? Your bots are broken beyond repair.", "rating": 21 },
    { "keyword": "Book", "roast": "Book startup? Reading between your lines is painful.", "rating": 13 },
    { "keyword": "Photo", "roast": "Photo app? Your pics are as blurry as your vision.", "rating": 1 },
    { "keyword": "Video", "roast": "Video startup? Buffering your failures endlessly.", "rating": 23 },
    { "keyword": "Game", "roast": "Game startup? More like a game of chance, and you lose.", "rating": 2 },
    { "keyword": "Learn", "roast": "Learn startup? Your lessons are lessons in failure.", "rating": 0 },
    { "keyword": "Music", "roast": "Music app? Sounds like static noise to me.", "rating": 9 },
    { "keyword": "Shop", "roast": "Shop startup? Your shelves are empty.", "rating": 22 },
    { "keyword": "Smart", "roast": "Smart tech? Your smarts must be artificial too.", "rating": 3 },
    { "keyword": "Pay", "roast": "Payment startup? You owe your users an apology.", "rating": 15 },
    { "keyword": "Taxi", "roast": "Taxi app? You just rerouted to disaster.", "rating": 5 },
    { "keyword": "Wear", "roast": "Wearable tech? You just accessorize your errors.", "rating": 19 },
    { "keyword": "Money", "roast": "Money startup? Your profits are imaginary.", "rating": 11 },
    { "keyword": "Finance", "roast": "Finance app? Your balance sheets don't add up.", "rating": 8 },
    { "keyword": "MedTech", "roast": "MedTech? Your cure is a virus.", "rating": 20 },
    { "keyword": "Insure", "roast": "Insurance startup? You can’t even insure your ideas.", "rating": 26 },
    { "keyword": "Legal", "roast": "Legal startup? Your arguments don’t hold up.", "rating": 14 },
    { "keyword": "Robot", "roast": "Robot startup? Your bots can't even clean up.", "rating": 16 },
    { "keyword": "Edu", "roast": "Edu startup? Your curriculum is all fail.", "rating": 6 },
    { "keyword": "News", "roast": "News app? You spread fake failure faster.", "rating": 17 },
    { "keyword": "Tech", "roast": "Tech startup? You tech me not to invest.", "rating": 0 },
    { "keyword": "Sport", "roast": "Sport startup? You just dropped the ball.", "rating": 29 },
    { "keyword": "Cloudify", "roast": "Cloudify? Your cloud just rains bugs.", "rating": 7 },
    { "keyword": "Track", "roast": "Track startup? You lost the trail already.", "rating": 23 },
    { "keyword": "Scan", "roast": "Scan tech? You just scanned yourself out of business.", "rating": 32 },
    { "keyword": "Print", "roast": "Print startup? Your pages are blank.", "rating": 28 },
    { "keyword": "Link", "roast": "Link startup? Your connections are dead ends.", "rating": 18 },
    { "keyword": "Grow", "roast": "Grow startup? Your growth is just weeds.", "rating": 12 },
    { "keyword": "Drive", "roast": "Drive startup? You just stalled.", "rating": 21 },
    { "keyword": "Clean", "roast": "Clean tech? Your mess is digital.", "rating": 13 },
    { "keyword": "Build", "roast": "Build startup? Your foundation is shaky.", "rating": 27 },
    { "keyword": "Code", "roast": "Code startup? Your code crashed before launch.", "rating": 30 },
    { "keyword": "Map", "roast": "Map startup? You lost your own way.", "rating": 10 },
    { "keyword": "Test", "roast": "Test startup? You failed every one.", "rating": 25 },
    { "keyword": "Secure", "roast": "Security startup? You leak more than protect.", "rating": 24 },
    { "keyword": "Save", "roast": "Save app? You just wasted my time.", "rating": 4 },
    { "keyword": "Jump", "roast": "Jump startup? You fell flat.", "rating": 31 },
    { "keyword": "Lift", "roast": "Lift startup? You just pulled your own plug.", "rating": 19 },
    { "keyword": "Assistant", "roast": "As helpful as a screen door on a submarine. Useless.", "rating": 5 },
    { "keyword": "Sharing", "roast": "Never has their wallet. Convenient.", "rating": 2 },
    { "keyword": "Care", "roast": "Cares less than I do about diets. Zero.", "rating": 1 },
    { "keyword": "Friendly", "roast": "Like a telemarketer. Unwanted.", "rating": 7 },
    { "keyword": "Electric", "roast": "Shocks worse than a surprise bill. Ouch.", "rating": 20 },
    { "keyword": "Analytics", "roast": "Random noise. My grandma's TikToks make more sense.", "rating": 22 },
    { "keyword": "Media", "roast": "Spreads gossip. Fast and furious.", "rating": 17 },
    { "keyword": "Service", "roast": "Slower than molasses. Is anyone working?", "rating": 6 },
    { "keyword": "Mobile", "roast": "Heavy as a brick. My foot hurts.", "rating": 11 },
    { "keyword": "Online", "roast": "Ghosting everyone. Where did they go?", "rating": 8 },
    { "keyword": "Booking", "roast": "Stressful. Like last-minute concert tickets.", "rating": 23 },
    { "keyword": "Automation", "roast": "Automates failures. One job!", "rating": 9 },
    { "keyword": "Club", "roast": "Empty. No one showed up.", "rating": 26 },
    { "keyword": "Editing", "roast": "Makes it worse. Like a bad haircut.", "rating": 0 },
    { "keyword": "Conference", "roast": "Email would be better. Waste of time.", "rating": 12 },
    { "keyword": "Development", "roast": "Creates problems faster. Endless cycle.", "rating": 14 },
    { "keyword": "Platform", "roast": "Sinks faster than my mood. Bye bye.", "rating": 16 },
    { "keyword": "Streaming", "roast": "Drips like a leaky faucet. So little.", "rating": 32 },
    { "keyword": "Wearables", "roast": "Fashion disaster. And useless.", "rating": 3 },
    { "keyword": "Gateway", "roast": "To frustration. Access denied.", "rating": 21 },
    { "keyword": "Watch", "roast": "Wrong time. Like my ex's promises.", "rating": 15 },
    { "keyword": "Digital", "roast": "Old as a rotary phone. Outdated.", "rating": 13 },
    { "keyword": "Exchange", "roast": "Promises gains, delivers empty. Tricked.", "rating": 30 },
    { "keyword": "Gaming", "roast": "Powered by rage quits. Not relaxing.", "rating": 18 },
    { "keyword": "Virtual", "roast": "All surface, no substance. Fake.", "rating": 28 },
    { "keyword": "Augmented", "roast": "Adds problems. Makes things worse.", "rating": 7 },
    { "keyword": "Machine", "roast": "Jams more than it runs. Get a new one.", "rating": 29 },
    { "keyword": "Learning", "roast": "Slow like a toddler. It's a process.", "rating": 4 },
    { "keyword": "Big", "roast": "Big talk, tiny results. All bark.", "rating": 27 },
    { "keyword": "Storage", "roast": "Full of junk. Declutter!", "rating": 25 },
    { "keyword": "Cyber", "roast": "Security as weak as my diet resolve. Broken.", "rating": 9 },
    { "keyword": "Security", "roast": "Protects like a wet paper bag. Easy access.", "rating": 19 },
    { "keyword": "Tutoring", "roast": "Gives up fast. Like my diet.", "rating": 6 },
    { "keyword": "Rental", "roast": "Glitches galore. Just return it.", "rating": 10 },
    { "keyword": "Renewable", "roast": "Like my excuses. Never-ending.", "rating": 8 },
    { "keyword": "Energy", "roast": "Drains phone battery. Fast.", "rating": 3 },
    { "keyword": "Agriculture", "roast": "More weeds than yield. Time to clean.", "rating": 11 },
    { "keyword": "Coach", "roast": "Yells, teaches nothing. Broken record.", "rating": 2 },
    { "keyword": "Meditation", "roast": "Stresses me out. Mind racing.", "rating": 24 },
    { "keyword": "Podcast", "roast": "Puts listeners in a coma. So boring.", "rating": 1 },
    { "keyword": "Graphic", "roast": "Colors clash. My eyes hurt.", "rating": 5 },
    { "keyword": "Design", "roast": "Pixel mess. Did a toddler draw this?", "rating": 20 },
    { "keyword": "Tool", "roast": "More toy than tool. Useless.", "rating": 22 },
    { "keyword": "Software", "roast": "Crashes like my social life. Abruptly.", "rating": 31 },
    { "keyword": "VPN", "roast": "Leaks data. What's the point?", "rating": 17 },
    { "keyword": "Password", "roast": "Forgets keys. Like my grocery list.", "rating": 1 },
    { "keyword": "Email", "roast": "Spam factory. Zero respect.", "rating": 6 },
    { "keyword": "SEO", "roast": "Buries you in search hell. Lost.", "rating": 12 },
    { "keyword": "Content", "roast": "So boring. Invisible.", "rating": 2 },
    { "keyword": "Management", "roast": "Messes everything up. Chaos.", "rating": 3 },
    { "keyword": "Event", "roast": "Forgotten fast. What happened?", "rating": 7 },
    { "keyword": "Hosting", "roast": "Slow as paint drying. Load already!", "rating": 16 },
    { "keyword": "Customer", "roast": "Ghosts you. Support? Never heard of it.", "rating": 13 }
  ],
    "fallback_roasts": [
{ "roast": "That idea? I've seen better pitches at a little league game.", "rating": 41 },
    { "roast": "Your startup's so confusing, even ChatGPT gave up.", "rating": 32 },
    { "roast": "Sounds like a solution desperately looking for a problem.", "rating": 33 },
    { "roast": "That’s not a pitch. That’s a cry for funding.", "rating": 26 },
    { "roast": "Your startup could get ghosted by investors *and* Tinder matches.", "rating": 22 },
    { "roast": "If ambition were execution, you'd still be in beta.", "rating": 4 },
    { "roast": "It’s giving ‘pivot in six months’ energy.", "rating": 7 },
    { "roast": "That pitch was so dry, even your TAM fell asleep.", "rating": 45 },
    { "roast": "Your idea’s got potential. To waste everyone's time.", "rating": 43 },
    { "roast": "Startup so vague it makes Web3 look straightforward.", "rating": 31 },
    { "roast": "Your elevator pitch needs stairs. And a nap.", "rating": 14 },
    { "roast": "That startup would be hot—if it were on fire.", "rating": 36 },
    { "roast": "You really said: ‘What if we made it worse, but scalable?’", "rating": 15 },
    { "roast": "Investors will pass faster than your page load time.", "rating": 8 },
    { "roast": "The only thing you’re disrupting is investor patience.", "rating": 27 },
    { "roast": "Your pitch deck just caused a market crash. Emotionally.", "rating": 50 },
    { "roast": "That idea belongs in a group chat, not a cap table.", "rating": 12 },
    { "roast": "You just reinvented failure. But with worse UX.", "rating": 37 },
    { "roast": "If buzzwords could code, maybe you'd have a product.", "rating": 35 },
    { "roast": "I’ve seen stealth startups with more clarity.", "rating": 2 },
    { "roast": "That pitch just soft-launched my will to live.", "rating": 39 },
    { "roast": "The future is here — and it's asking you to stop.", "rating": 13 },
    { "roast": "Your MVP stands for 'Most Vague Pitch.'", "rating": 18 },
    { "roast": "You just pitched a PowerPoint with trauma.", "rating": 40 },
    { "roast": "It's not a startup, it's a startup-themed escape room.", "rating": 28 },
    { "roast": "If confusion were a business model, you’d be profitable.", "rating": 9 },
    { "roast": "Your roadmap looks like a toddler’s crayon drawing.", "rating": 10 },
    { "roast": "Even your burn rate is ashamed of being associated.", "rating": 25 },
    { "roast": "You’re not pre-revenue, you're pre-relevance.", "rating": 6 },
    { "roast": "The pitch was so weak, it needs a Series A... of therapy.", "rating": 24 },
    { "roast": "You should pivot. Preferably into another industry.", "rating": 34 },
    { "roast": "Your ‘tech stack’ is just buzzwords duct-taped together.", "rating": 48 },
    { "roast": "That idea should’ve stayed in your Notes app.", "rating": 11 },
    { "roast": "You’re solving a problem no one has with tools no one needs.", "rating": 1 },
    { "roast": "I’ve heard fewer red flags in a North Korean parade.", "rating": 17 },
    { "roast": "Your market size is you, your cofounder, and your moms.", "rating": 23 },
    { "roast": "Investors would rather Venmo a scammer.", "rating": 46 },
    { "roast": "You talk lean but that pitch was all bloat.", "rating": 30 },
    { "roast": "The best part of your startup is the logo — maybe.", "rating": 42 },
    { "roast": "That’s not disruption. That’s digital littering.", "rating": 3 },
    { "roast": "Is your valuation based on vibes?", "rating": 19 },
    { "roast": "Your idea was so bad, autocorrect changed it to ‘stop.’", "rating": 38 },
    { "roast": "You're a unicorn — if failure was rare.", "rating": 47 },
    { "roast": "That’s not a pitch. That’s a DDoS on common sense.", "rating": 16 },
    { "roast": "Your startup's USP is how fast people walk away.", "rating": 20 },
    { "roast": "You built a rocket to nowhere. Congrats on lift-off.", "rating": 29 },
    { "roast": "Your ‘innovation’ is just a rerun with worse actors.", "rating": 21 },
    { "roast": "That pitch was so early, it’s still an embryo.", "rating": 44 },
    { "roast": "Your addressable market is probably just your reflection.", "rating": 49 },
    { "roast": "You made a startup nobody needed — not even ironically.", "rating": 5 },
    { "roast": "It’s like Uber, but for disappointing your parents.", "rating": 43 },
    { "roast": "Your demo crashed and so did our hopes.", "rating": 29 },
    { "roast": "You pitched an app that solves nothing but your boredom.", "rating": 7 },
    { "roast": "Even your NDA wants to forget this.", "rating": 27 }
    ]
}

keyword_roasts = roast_data["keyword_roasts"]
fallback_roasts = roast_data["fallback_roasts"]

# --- Roast Logic ---
def find_roast(pitch):
    pitch_lower = pitch.lower()
    for item in keyword_roasts:
        if item["keyword"].lower() in pitch_lower:
            return item["roast"], item["rating"], item["keyword"]
    fallback = random.choice(fallback_roasts)
    return fallback["roast"], fallback["rating"], "fallback"

# --- TTS URL Generator ---
def free_tts_url(text, voice):
    return f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={requests.utils.quote(text)}"

# --- Streamlit Page Config ---
st.set_page_config(page_title="Pitch Roast 🔥", layout="wide")

# --- Custom Styles ---
st.markdown("""
<style>
/* Background and text */
body, .stApp {
    background-color: #121212;
    color: white !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Headings, labels */
h1, h2, h3, h4, h5, h6, .stTextInput label, .stSelectbox label, .stCaption {
    color: white !important;
}

/* Links */
a {
    color: #ff4500;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

/* Tables */
table, th, td {
    border: 1px solid #3a4d6c;
    color: white;
}
th {
    background-color: #ff4500;
    color: white !important;
}
tr:nth-child(even) {
    background-color: #2b2b2b;
}

/* Buttons */
.stButton > button {
    background-color: #ff4500;
    color: white;
}
.stButton > button:hover {
    background-color: #e03e00;
}

/* Sidebar style */
.sidebar-style {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 12px;
    height: 100%;
}

/* Sidebar options - make text white and highlight selected */
.sidebar-option {
    padding: 10px 0;
    font-weight: bold;
    cursor: pointer;
    color: white !important;
}
.sidebar-selected {
    color: #ff4500 !important;
}

/* Sidebar radio buttons fix - white text */
[role="radiogroup"] > div > label {
    color: white !important;
}

/* Responsive adjustments */
@media (max-width: 600px) {
    /* Stack sidebar and content vertically on mobile */
    .css-1d391kg {  /* Streamlit columns container */
        flex-direction: column !important;
    }
    .css-1d391kg > div {
        width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Load and encode logo.png once ---
with open("logo.png", "rb") as f:
    data = f.read()
    encoded_logo = base64.b64encode(data).decode()

# --- Layout ---
sidebar_col, content_col = st.columns([1, 4])

# --- Sidebar ---
with sidebar_col:
    st.markdown("## 🔥 Pitch Roast")
    st.markdown('<div class="sidebar-style">', unsafe_allow_html=True)
    menu_options = {
        "🏠 Home": "home",
        "🏆 Leaderboard": "leaderboard",
        "📊 Your Stats": "stats"
    }
    selected = st.radio("Navigate", list(menu_options.keys()), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Content ---
with content_col:
    if menu_options[selected] == "home":
        # Clickable logo image linked to https://bolt.new
        st.markdown(
            f'''
            <a href="https://bolt.new" target="_blank" rel="noopener noreferrer">
                <img src="data:image/png;base64,{encoded_logo}" alt="Logo" style="width:auto; height:auto; max-width:100px;" />
            </a>
            ''',
            unsafe_allow_html=True
        )

        st.title("🎤 Pitch Roast 🔥")
        st.caption("Type your startup idea and get roasted mercilessly by AI.")

        user_name = st.text_input("Your name or alias (optional):", placeholder="Anonymous")
        pitch = st.text_input("Your startup pitch:", placeholder="e.g. Uber for dog walking")
        voice = st.selectbox("Choose TTS voice:", ["Brian", "Ivy", "Justin", "Joey", "Salli", "Matthew"])

        if st.button("🔥 Roast Me"):
            if not pitch.strip():
                st.warning("Please enter a pitch.")
            else:
                roast, rating, keyword = find_roast(pitch)
                st.error(f"💣 {roast} (🔥 {rating}/50)")
                st.audio(free_tts_url(roast, voice), format="audio/mp3")

                supabase.table("pitch_roasts").insert({
                    "idea": pitch,
                    "roast": roast,
                    "rating": rating,
                    "user_name": user_name.strip() if user_name.strip() else "Anonymous",
                    "created_at": datetime.utcnow().isoformat()
                }).execute()

                st.success("🔥 Roasted and logged successfully!")

        st.markdown("### 📜 Recent Roasts")
        rows = supabase.table("pitch_roasts").select("*").order("created_at", desc=True).limit(5).execute()
        for row in rows.data:
            st.write(f"**{row['idea']}** — _{row['roast']}_ (🔥 {row['rating']}/50) — by *{row.get('user_name', 'Anonymous')}*")

    elif menu_options[selected] == "leaderboard":
        st.title("🏆 Roast Leaderboard")

        # Search input to filter by username for both best and worst ideas
        search_user = st.text_input("Search by username:", key="leaderboard_search")

        # Pagination params for infinite scroll simulation
        batch_size = 10
        if "best_offset" not in st.session_state:
            st.session_state.best_offset = 0
        if "worst_offset" not in st.session_state:
            st.session_state.worst_offset = 0

        def load_best_ideas(offset=0, limit=10, username=None):
            query = supabase.table("pitch_roasts").select("*").order("rating", desc=True).range(offset, offset + limit - 1)
            if username:
                query = query.eq("user_name", username)
            return query.execute().data

        def load_worst_ideas(offset=0, limit=10, username=None):
            query = supabase.table("pitch_roasts").select("*").order("rating", desc=False).range(offset, offset + limit - 1)
            if username:
                query = query.eq("user_name", username)
            return query.execute().data

        # Load initial data
        best_data = load_best_ideas(st.session_state.best_offset, batch_size, search_user if search_user else None)
        worst_data = load_worst_ideas(st.session_state.worst_offset, batch_size, search_user if search_user else None)

        def render_ideas(title, data, is_best=True):
            if not data:
                st.info("No ideas found.")
                return
            table_data = [{
                "Rank": i + 1 + (st.session_state.best_offset if is_best else st.session_state.worst_offset),
                "Idea": row['idea'],
                "Rating": f"{row['rating']}/50",
                "User": row.get('user_name', 'Anonymous')
            } for i, row in enumerate(data)]
            st.table(table_data)

        st.markdown("### 🌟 Best Ideas")
        render_ideas("Best Ideas", best_data, True)

        if st.button("Load more best ideas"):
            st.session_state.best_offset += batch_size
            best_data = load_best_ideas(st.session_state.best_offset, batch_size, search_user if search_user else None)
            render_ideas("Best Ideas", best_data, True)

        st.markdown("### 💩 Worst Ideas")
        render_ideas("Worst Ideas", worst_data, False)

        if st.button("Load more worst ideas"):
            st.session_state.worst_offset += batch_size
            worst_data = load_worst_ideas(st.session_state.worst_offset, batch_size, search_user if search_user else None)
            render_ideas("Worst Ideas", worst_data, False)

    elif menu_options[selected] == "stats":
        st.title("📊 Your Stats")

        # Search bar for username (retrieve stats on submit)
        name = st.text_input("Enter your username to view your stats:")

        if name:
            data = supabase.table("pitch_roasts").select("*").eq("user_name", name).execute()
            pitches = data.data
            if pitches:
                df = pd.DataFrame(pitches)
                total = len(df)
                average = round(df["rating"].mean(), 2)
                st.markdown(f"👤 **{name}** has submitted **{total}** pitches.")
                st.markdown(f"⭐ Average Roast Rating: **{average}/50**")
                st.markdown("### 🗒 Your Ideas")
                df_display = df[["idea", "roast", "rating", "created_at"]].rename(columns={
                    "idea": "Pitch",
                    "roast": "Roast",
                    "rating": "Rating",
                    "created_at": "Timestamp"
                })
                st.table(df_display)
            else:
                st.info("No data found for that user.")
