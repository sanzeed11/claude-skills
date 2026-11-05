"""brandcopy.py — every line of approved copy used in 10_MARKETING_COLLATERAL.
Sources: 01_BRAND_STRATEGY/*.md and BRAND_KIT_SPEC.md (all confirmed from sanzeed.com unless marked).
Nothing here is invented. Fields the client must supply are written as bracketed labels, e.g. [Date]."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

NAME = "Sanzeed Mirza"
DESCRIPTOR = "Experiential Design Consultant"
CITY = "New Delhi, India"
EMAIL = "sanzeed@gmail.com"
PHONE = "+91 7827051270"
WHATSAPP = "WhatsApp @sanzeed"
LINKEDIN = "linkedin.com/in/sanzeed"
SITE = "sanzeed.com"

MASTER_LINE = "Experiential design you can walk into."
SHORT_LINE = "Vision you can walk into."
BRAND_IDEA = "Carry the light across."
PROOF_LINE = "90 projects, one continuous craft."
PERSONAL_LINE = "Strategy, craft and calm leadership, in one person."
METHOD_LINE = "A method for the monumental."
CALL = "Tell me about the room."
CALL_SUB = "A few lines are enough. I reply within two working days."
TRUST = "Trusted by PwC, Microsoft, Discovery and National Museums, from concept to public unveiling."
QUOTE = "The most powerful stories aren’t just told — they’re felt, lived, and remembered through the spaces we design and the moments we shape."
POSITIONING = "A visual storyteller drawn to the pursuit of distinct, impactful experiences — those that challenge convention and connect deeply with audiences."
BETWEEN = "Between two points of light."
BETWEEN_SUB = "A brief on one side, a visitor on the other. Seven ways to carry the light across."
ALL_SEVEN = "All seven, every time."
ALL_SEVEN_SUB = "Every room needs the whole list, held in one hand. That is the job, and the pleasure of it."
METHOD_SUB = "Every environment begins as a question and ends as a memory. The path between is deliberate — equal parts strategy and craft, ambition and discipline."
ENDURES = "Let’s shape something that endures."
AVAILABLE = "Available for new projects and collaborations. The first conversation is always free."
PROMISES = ["The first conversation is always free.", "I reply within two working days.", "If it is urgent, WhatsApp is fastest."]
RIGHTS = "Employee work for Tagbin, Sociopixel, DWS and B2W; rights remain with those companies."

ABOUT_1 = "I’m an experiential design consultant based in New Delhi, working with institutions and brands wherever the project is. Fifteen years in: first as a concept artist and VFX lead on films and animation, then eight years directing museums, experience centres, pavilions and shows."
ABOUT_2 = "I lead the whole room — story, space, graphics, media and the team that builds it. The work I want to make is calm to run and impossible to forget once you have walked through it."

BIO_10 = "Experiential design consultant. Museums, pavilions and shows you can walk into."
BIO_25 = "Sanzeed Mirza is an independent experiential design consultant in New Delhi. Fifteen years in, he leads the whole room — story, space, media and team — for institutions and brands."
BIO_50 = "Sanzeed Mirza directs museums, experience centres, pavilions, memorials and projection shows for institutions and brands. Fifteen years in — first in VFX and concept art, then eight years directing national-scale museums — he leads story, space, graphics, media and the team that builds it, so the experience is calm to run and impossible to forget."
BOILERPLATE = "Sanzeed Mirza is an Experiential Design Consultant based in New Delhi, working with institutions and brands wherever the project is. Over fifteen years he has directed more than 90 projects, including 60+ museums and experience centres and 15 projection-mapping and light shows, among them the Prime Minister Museum in New Delhi, the Ram Katha Show in Ayodhya and Buddha Park in Uttarakhand. He works independently with museums, cultural institutions and brands as creative lead from first concept to opening day. sanzeed.com"
STORY = [
 "Sanzeed Mirza started where light is made by hand: in VFX suites and concept-art studios, drawing the frames that brands and films would later build. For five years he learned how a single image carries an idea.",
 "Then the frame became a room. From 2018 he directed museums, experience centres, pavilions and shows at national scale — the Prime Minister Museum in New Delhi, where visitors walk a tricolour corridor and meet one leader at a time; the Ram Katha Show in Ayodhya, where the script came first and every surface carried a line of it; Buddha Park in Uttarakhand, where the walk itself is the meditation.",
 "Ninety projects later, the method is simple to say and hard to do: discover the one central story, direct a single vision across every discipline, craft space, light, motion and interaction into a room, and deliver it — built, tested and opened. In 2026 he began working independently, so that institutions and brands can bring the whole room to one person.",
 "A brief on one side. A visitor on the other. Sanzeed carries the light across.",
]

PROOF = [("15", "Years of experience"), ("8", "Years experiential & museum"), ("90", "Projects directed"), ("60", "Museums & centres")]

PILLARS = [
 ("i.", "Strategic Vision", "Transforming complex ideas into cohesive, purposeful stories — concept through launch."),
 ("ii.", "Immersive Craft", "Environments that engage intellectually, emotionally, and physically across every touchpoint."),
 ("iii.", "Calm Leadership", "Guiding designers, writers, architects, producers and technologists toward unified outcomes."),
]

SERVICES = [
 ("01", "Experiential Design & Creative Direction", "One vision from brief to opening night: narrative, space, media and the team that builds it.", "Prime Minister Museum", "prime-minister-museum"),
 ("02", "Museum & Cultural Exhibition Planning", "Galleries planned as a route, not a floor plan. Objects, stories and dwell time, in order.", "Yuge Yugeen Bharat Museum", "yuge-yugin-bharat-museum"),
 ("03", "Immersive Storytelling & Narrative Architecture", "The script comes first. Every room, screen and surface carries a line of it.", "Ram Katha Show", "ram-katha-show"),
 ("04", "Spatial Experience & Environmental Branding", "Brands you can stand inside: pavilions, experience centres, thresholds and wayfinding.", "India Pavilion Expo 2025", "india-pavilion-expo-2025"),
 ("05", "Event Production & Brand Activation", "Shows, launches and tableaux where light and timing do the talking.", "G20 Tree Show", "g20-tree-show"),
 ("06", "Digital ↔ Physical Experience Integration", "Projection, AR and VR, sensors and data brought into real rooms and real crowds.", "Viratswaroop Kinetic Projection", "viratswaroop-kinetic-projection"),
 ("07", "Cross-Functional Leadership & Mentorship", "Designers, writers, architects, producers and technologists moved toward one outcome, calmly.", "Buddha Park", "buddha-park"),
]

METHOD = [
 ("01", "Discover", "Immersion in the subject — its history, intent and audience — until the central story reveals itself.", "a research deck and the one central story"),
 ("02", "Direct", "A unifying creative vision that aligns designers, architects, writers, producers and technologists toward one outcome.", "a concept book and a walkthrough film"),
 ("03", "Craft", "Space, light, motion and interaction composed into environments that engage intellectually, emotionally and physically.", "detail drawings, media scripts and a prototype room"),
 ("04", "Deliver", "Concept to launch — balancing creative ambition with operational discipline. On scale, on story, on time.", "a built, tested and opened experience"),
]

TIMELINE = [
 ("Aug 2026 — Present", "Experiential Design Consultant", "Independent", "Partnering directly with museums, cultural institutions and brands as an independent consultant — leading experience vision, narrative and design direction from first concept to opening day."),
 ("Jun 2018 — Jul 2026", "Creative Director", "Tagbin", "Leading creative strategy and execution for high-profile digital museums, immersive exhibitions and cultural experiences at national scale."),
 ("Apr 2018 — May 2018", "Creative Head", "Digital Web Solutions", "Led the creative department of a fast-paced agency, developing brand identities and integrated campaigns across digital and print."),
 ("Feb 2017 — Mar 2018", "Creative Director", "SocioPixels", "Led the visual direction and creative execution for animated films, multimedia content and experiential installations."),
 ("Sep 2011 — Dec 2016", "Lead Concept Artist", "Broadcast2world", "Crafted high-impact visual narratives that helped brands communicate complex ideas with clarity and emotion."),
 ("Sep 2011 — Dec 2016 · in parallel", "VFX Artist", "Prime Focus", "Contributed to the production of high-end visual effects for international film and media projects."),
]

FEATURED = [  # "Now showing" — eight rooms, lit.
 ("prime-minister-museum", "Prime Minister Museum", "New Delhi", "Museums & Experience Centres"),
 ("buddha-park", "Buddha Park", "Uttarakhand", "Museums & Experience Centres"),
 ("india-pavilion-expo-2025", "India Pavilion Expo 2025", "Concept", "Museums & Experience Centres"),
 ("yuge-yugin-bharat-museum", "Yuge Yugeen Bharat Museum", "New Delhi", "Museums & Experience Centres"),
 ("tribal-museum", "Tribal Museum", "New Delhi", "Museums & Experience Centres"),
 ("rbi-museum-interior", "RBI Museum Interior", "Mumbai", "Museums & Experience Centres"),
 ("ram-katha-show", "Ram Katha Show", "Ayodhya", "Projection Mapping & Shows"),
 ("g20-tree-show", "G20 Tree Show", "New Delhi", "Projection Mapping & Shows"),
]

CASES = {
 "prime-minister-museum": dict(
   title="Prime Minister Museum", place="New Delhi", type="Museums & Experience Centres", role="Concept & creative direction",
   brief="One museum for every Prime Minister of India since 1947, in New Delhi — a building that has to hold schoolchildren and heads of state on the same afternoon, and give each leader a room without turning the whole into a corridor of portraits.",
   idea="A corridor you walk in order.",
   idea_text="The spine of the museum is a single long passage under a tricolour canopy. Visitors meet one Prime Minister at a time, in sequence, so the building itself tells the story of the office before any gallery does. Portraits face you at eye level; the leaders’ own words sit beside them on the walls.",
   walk="Off the spine, each gallery changes its mood to its subject: wood and light for one era, screens and sound for another. Guides stand at the thresholds; planting softens the floor so the passage reads as a walk rather than a hall.",
   visitors="Visitors walk the whole line of leaders without a map, and come out knowing the order by heart.",
   captions=["The entrance, with the old Teen Murti house behind", "The new wing from above, the chakra over the lawns", "The tricolour corridor: one Prime Minister at a time", "A leader’s gallery: early life, then the years in office", "Temples of Modern India: the dams, institutes and labs", "Each gallery changes its mood with its subject", "The projection room: portraits in moving light", "The amphitheatre and gardens at dusk"]),
 "ram-katha-show": dict(
   title="Ram Katha Show", place="Ayodhya", type="Projection Mapping & Shows", role="Show concept & direction",
   brief="A night show for Ayodhya that tells the Ram Katha without a stage or actors — the audience is seated in front of a great hall, and the story has to come out of the architecture itself.",
   idea="The building is the screen.",
   idea_text="Every dome, arch and column of the hall was mapped and painted with light, so the story seems to rise from the stone. Scenes move from the central shrine outwards along the galleries; the gilded ceiling becomes sky, then forest, then fire.",
   walk="Projection, sound and timing were composed as one score: the beats of the narration cue the light, and the architecture’s own rhythm (arch after arch) sets the pace of the scenes.",
   visitors="Visitors sit in the dark and watch a building they know by day become the story by night.",
   captions=["A field of lamps opens the night", "The name, written in light", "The hero drawn in a single line of light", "The hall in darkness: the floor mandala wakes first", "The story arrives on the walls, scene by scene", "The ceiling becomes the sky", "The whole hall lit as a court", "The darbar: the end of the story, in full light"]),
 "buddha-park": dict(
   title="Buddha Park", place="Uttarakhand", type="Museums & Experience Centres", role="Concept & creative direction",
   brief="A park in Uttarakhand around a reclining Buddha, with a stupa, shrines and gardens — a landscape that must work as a place of calm for pilgrims and a day out for families.",
   idea="A garden of gestures.",
   idea_text="The park is laid out as one loop: from the gate past the shrines to the stupa, around the reclining Buddha and back to a fountain court ringed by sculpted hands in the mudras. The walk itself is the meditation; nothing is read, everything is passed.",
   walk="Water, stone and planting carry the route. The Buddha rests against a green hillside so it is seen first from a distance and only slowly at full scale; the fountain court gives the loop a place to pause.",
   visitors="Visitors complete the loop at their own pace and end at the water, facing the Buddha.",
   captions=["The pavilion roof planted as a hillside", "The fountain court from above, the Buddha resting beyond", "Under the pavilion: benches, lamps and shade", "The route turns toward the shrines", "The reclining Buddha against the green slope", "The golden Buddha among the stupas", "Shrines and stupas along the loop", "The Buddha at full scale, at the end of the walk"]),
}
CASE_ORDER = ["prime-minister-museum", "ram-katha-show", "buddha-park"]

GALLERY = json.load(open(os.path.join(HERE, "gallery.json"), encoding="utf-8"))  # 90 projects: img, title, place, cat
CATEGORIES = [("Museums & Experience Centres", 60), ("Projection Mapping & Shows", 15), ("Explainer Videos & Others", 15)]

BUDGET_BANDS = ["Under ₹25 lakh", "₹25 lakh – ₹1 crore", "₹1 – 5 crore", "Over ₹5 crore"]
PROJECT_TYPES = ["Museum or experience centre", "Pavilion or exhibition", "Show, launch or event", "Projection or light show", "Something else"]
TIMELINES = ["Within 3 months", "3 to 6 months", "6 to 12 months", "Over a year"]

SIGNATURE_FORMAL = "Sanzeed Mirza · Experiential Design Consultant"
EMAIL_SIG = ["Sanzeed Mirza", "Experiential Design Consultant", "+91 7827051270 · sanzeed@gmail.com · sanzeed.com", "Experiential design you can walk into."]
