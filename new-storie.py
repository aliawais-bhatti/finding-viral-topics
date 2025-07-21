import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyBjOIk8mmJUUH618-cIQ00kzIKiVESf89M"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of broader keywords
keywords = [
"survival stories","true survival stories","wilderness survival","desert survival","ocean survival","mountain survival","plane crash survival",
"shipwreck survival","lost in wilderness","stranded survival","comeback stories","failure to success","rags to riches","business comeback",
"life transformation","second chance stories","redemption stories","against all odds","overcoming failure","success after failure","homeless to millionaire",
"homeless success stories","from streets to success","poverty to wealth","homeless entrepreneur","rags to riches real life","homeless to rich",
"street to suite",
"homeless millionaire stories",
"zero to hero",
"near death experiences",
"near death stories",
"life after death",
"clinical death experiences",
"afterlife experiences",
"dying and coming back",
"NDE stories",
"death experience stories",
"miraculous survival",
"brought back to life",
"abduction survival",
"kidnap survival",
"human trafficking survival",
"escaped kidnapping",
"abduction stories",
"kidnap victim stories",
"human trafficking stories",
"captivity survival",
"hostage survival",
"prisoner escape stories",
"escaped cults",
"cult survivor stories",
"religious cult escape",
"cult abuse survivors",
"brainwashing survivors",
"cult recovery stories",
"leaving cults",
"cult victims",
"sectarian abuse",
"cult trauma stories",
"real hero stories",
"unsung heroes",
"everyday heroes",
"anonymous heroes",
"hidden heroes",
"forgotten heroes",
"ordinary people extraordinary acts",
"heroic acts",
"selfless heroes",
"quiet heroes",
"war survivor stories",
"war veterans stories",
"combat survival",
"battlefield stories",
"prisoner of war",
"wartime survival",
"military survival",
"war trauma stories",
"holocaust survivors",
"genocide survivors",
"cancer survivor stories",
"beating cancer",
"cancer journey",
"illness recovery",
"medical miracle",
"disease survivor",
"terminal illness recovery",
"health transformation",
"overcoming illness",
"medical survival stories",
"life transformation stories",
"incredible transformation",
"personal transformation",
"life changing stories",
"dramatic life change",
"complete makeover stories",
"reinvention stories",
"lifestyle transformation",
"identity transformation",
"deep web horror",
"dark web stories",
"deep web experiences",
"dark net horror",
"deep web encounters",
"tor browser stories",
"hidden internet",
"dark web mysteries",
"deep web dangers",
"darknet stories",
"reddit nosleep",
"nosleep stories",
"reddit horror stories",
"nosleep creepypasta",
"reddit scary stories",
"nosleep podcast",
"reddit paranormal",
"nosleep compilation",
"reddit ghost stories",
"nosleep narration",
"internet rabbit holes",
"internet mysteries",
"online rabbit holes",
"web mysteries",
"internet legends",
"digital mysteries",
"online urban legends",
"cyber mysteries",
"internet folklore",
"web urban legends",
"creepypasta",
"slenderman",
"jeff the killer",
"ben drowned",
"sonic exe",
"backrooms",
"scp stories",
"creepypasta characters",
"internet horror",
"digital horror stories",
"haunted house stories",
"real haunted houses",
"ghost stories",
"haunted places",
"paranormal activity",
"haunted locations",
"ghost encounters",
"haunted mansion",
"poltergeist stories",
"haunted hotel stories",
"paranormal witness",
"paranormal encounters",
"ghost sightings",
"supernatural experiences",
"paranormal investigation",
"spirit encounters",
"paranormal activity real",
"ghostly encounters",
"supernatural stories",
"paranormal phenomena",
"urban legends",
"modern urban legends",
"city legends",
"folklore stories",
"myth stories",
"legend origins",
"urban myths",
"contemporary legends",
"cultural legends",
"local legends",
"possession stories",
"demonic possession",
"exorcism stories",
"spirit possession",
"supernatural possession",
"haunted by demons",
"evil spirits",
"paranormal possession",
"occult stories",
"demonic encounters",
"lost media stories",
"lost films",
"missing media",
"banned content",
"censored media",
"disappeared content",
"forbidden media",
"lost episodes",
"missing footage",
"erased media",
"eerie AI stories",
"AI gone wrong",
"artificial intelligence horror",
"technology horror",
"robot horror stories",
"AI malfunction",
"tech horror",
"digital horror",
"cyber horror",
"machine horror",
"flash fiction",
"short stories",
"micro fiction",
"brief stories",
"quick stories",
"mini stories",
"short narrative",
"compact stories",
"bite sized stories",
"instant stories",
"moral stories",
"life lesson stories",
"wisdom stories",
"ethical stories",
"virtue stories",
"character building stories",
"inspirational stories",
"motivational stories",
"meaningful stories",
"value based stories",
"sci-fi short stories",
"science fiction stories",
"futuristic stories",
"space stories",
"alien stories",
"cyberpunk stories",
"dystopian stories",
"utopian stories",
"time travel stories",
"parallel universe stories",
"dark fantasy",
"gothic stories",
"supernatural fantasy",
"horror fantasy",
"occult fantasy",
"mystical stories",
"magical horror",
"fantasy horror",
"paranormal fantasy",
"urban fantasy",
"futuristic dystopia",
"dystopian future",
"post apocalyptic",
"cyberpunk dystopia",
"totalitarian stories",
"surveillance state",
"authoritarian future",
"bleak future",
"dark future",
"oppressive society",
"AI love stories",
"robot romance",
"artificial intelligence romance",
"human AI relationship",
"digital love",
"cyber romance",
"technology romance",
"android love",
"virtual love",
"machine romance",
"fictional war stories",
"imaginary wars",
"fantasy warfare",
"fictional battles",
"made up conflicts",
"alternate history wars",
"fictional military",
"war fiction",
"battle stories",
"combat fiction",
"time travel stories",
"time machine stories",
"temporal stories",
"chronos stories",
"time loop stories",
"time paradox",
"time travel adventures",
"temporal displacement",
"time manipulation",
"chronological stories",
"alternate reality",
"parallel dimensions",
"alternate universe",
"multiverse stories",
"different reality",
"alternative timeline",
"parallel worlds",
"dimension hopping",
"reality shifting",
"alternate dimensions",
"reimagined mythology",
"modern mythology",
"mythology retelling",
"updated myths",
"contemporary mythology",
"myth adaptation",
"folklore retelling",
"legend reimagining",
"mythological stories",
"ancient myths modern twist"
]


# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # Check if "items" key exists
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:  # Only include channels with fewer than 3,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}  \n"
                    f"**Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
