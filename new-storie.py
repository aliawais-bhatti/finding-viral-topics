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
keywords =[
  "unsolved historical mysteries", "ancient civilizations lost to time", "mysteries of the pyramids", "disappearance of the Roanoke colony", "real history behind Atlantis", "unsolved codes in ancient texts", "mysterious deaths of historical figures", "hidden chambers in pyramids", "vanished empires", "ancient aliens in human history",
  "mystery of the Nazca lines", "who were the Sea Peoples", "forgotten languages of history", "bizarre artifacts historians can't explain", "ancient maps that defy logic", "who built the Sphinx", "true story of the Voynich manuscript", "mystery behind the Antikythera mechanism", "ancient ruins that shouldn't exist", "lost city of Z",
  "hidden messages in religious texts", "real secrets of the Templars", "unsolved murders in royal families", "legend of the Black Knight satellite", "disappearances in ancient history", "mystery civilizations before recorded history", "biblical mysteries never solved", "ancient prophecies that came true", "evidence of time travel in history", "hidden scrolls found in deserts",
  "ghost ships of history", "strange tombs with no records", "who built Stonehenge", "megaliths that defy explanation", "mysteries of Easter Island", "ancient structures aligned with stars", "unsolved rituals from the past", "secret societies in ancient history", "hidden underground cities", "buried treasures never found",
  "secret codes in Renaissance art", "missing royal bloodlines", "unsolved cases in ancient Rome", "dark ages unsolved mysteries", "mysteries of ancient India", "hidden truths in mythologies", "sacred relics that vanished", "what happened to the Library of Alexandria", "mystery behind ancient curses", "real story behind the Tower of Babel",
  "mystery of the Bermuda Triangle", "legend of El Dorado", "hidden history of the Vatican", "ancient death rituals", "Mayan calendar secrets", "lost cities in the Amazon", "unsolved ancient plagues", "mystery of the Baghdad battery", "secrets of the Knights Templar", "unsolved cave paintings",
  "prehistoric civilizations wiped out", "strange ancient skeletons", "underground tunnels in Europe", "artifacts out of place in history", "biblical relics never recovered", "mystery surrounding the Ark of the Covenant", "oldest pyramids not in Egypt", "ancient giant theories", "mystery of the Anunnaki", "unexplained mass disappearances",
  "dark secrets of ancient Egypt", "truth behind the Trojan War", "real story of King Arthur", "historical anomalies scientists can't explain", "sacred texts hidden from the public", "evidence of lost advanced technology", "mystery of the Crystal Skulls", "strange energy spots around the world", "ancient symbols still used today", "mystery religions of the past",
  "unsolved medieval crimes", "plagues that vanished without a trace", "historical figures who faked death", "pyramids underwater", "myths that might be true", "ancient records destroyed by war", "secrets buried under the Vatican", "unsolved church conspiracies", "ancient manuscripts yet to be decoded", "time anomalies in history",
  "disappearances of entire tribes", "cursed artifacts found by explorers", "mystery of the Green Children", "evidence of prehistoric nuclear war", "maps that show Antarctica ice-free", "mystery planets in old star charts", "strange lights recorded in history", "wars started by unknown causes", "ancient objects made with modern tools", "mystery of the ancient star gates"
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
