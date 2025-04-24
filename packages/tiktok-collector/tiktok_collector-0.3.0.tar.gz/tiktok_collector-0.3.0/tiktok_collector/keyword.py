import datetime
import pandas as pd
import requests


class TiktokKeywordCollector:
    """
    A class to collect TikTok posts by keyword.
    """
    
    # Constants
    RAPID_URL_SEARCH = "https://tiktok-v2-rapidapi.p.rapidapi.com/search/general"
    RAPID_API_HOST = "tiktok-v2-rapidapi.p.rapidapi.com"

    def __init__(self, api_key, country_code="US", max_post_by_keyword=100, max_keyword_post_retry=3):
        """
        Initialize the collector with an API key and configuration.
        
        Args:
            api_key (str): Your RapidAPI key for TikTok API
            country_code (str): The country code to filter posts by (default: "US")
            max_post_by_keyword (int): Maximum number of posts to collect per keyword (default: 100)
            max_keyword_post_retry (int): Maximum number of retries for keyword post collection (default: 3)
        """
        self.api_key = api_key
        self.country_code = country_code
        self.MAX_POST_BY_KEYWORD = max_post_by_keyword
        self.MAX_KEYWORD_POST_RETRY = max_keyword_post_retry
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.RAPID_API_HOST
        }

    def collect_posts_by_keyword(self, keyword):
        """
        Collect posts for a single keyword.
        
        Args:
            keyword (str): The keyword to collect posts for
            
        Returns:
            pandas.DataFrame: A DataFrame containing the collected posts
        """
        try:
            content_list = self._search_posts(keyword)
            print(f"Found {len(content_list)} posts for keyword {keyword}")
            
            content_full = []
            for i in content_list:
                author = i["author"]
                try:
                    display_url = i.get("video", {}).get(
                        "origin_cover", {}).get("url_list")[-1]
                except:
                    display_url = ""
                try:
                    create_date = datetime.datetime.utcfromtimestamp(
                        i["create_time"]).strftime("%m/%d/%Y") if 'create_time' in i and i["create_time"] else ""
                    post_info = {
                        "search_method": "Keyword",
                        "input_kw_hst": keyword,
                        "post_id": i["aweme_id"],
                        "post_link": f"www.tiktok.com/@{author['uid']}/video/{i['aweme_id']}",
                        "caption": i["desc"],
                        "hashtag": ", ".join(self._hashtag_detect(i['desc'])) if i['desc'] else "",
                        "hashtags": self._hashtag_detect(i['desc']),
                        "created_date": create_date,
                        "num_view": i["statistics"]["play_count"],
                        "num_like": i["statistics"]["digg_count"],
                        "num_comment": i["statistics"]["comment_count"],
                        "num_share": i["statistics"]["share_count"],
                        "target_country": author["region"],
                        "user_id": author["uid"],
                        "username": author["unique_id"],
                        "bio": author["signature"] if author.get("signature") else "",
                        "full_name": author["nickname"],
                        "display_url": display_url,
                        "taken_at_timestamp": int(i["create_time"]),
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                content_full.append(post_info)
            
            df_post = pd.DataFrame(content_full)
            if not df_post.empty:
                df_post = df_post.drop_duplicates(subset="post_id", keep="first")
            
            return df_post

        except Exception as e:
            print(f"Error collecting posts for keyword {keyword}: {e}")
            return pd.DataFrame()

    def _search_posts(self, keyword, country_code=None):
        """
        Search posts for a given keyword.
        
        Args:
            keyword (str): The keyword to search for
            country_code (str, optional): The country code to filter by
            
        Returns:
            list: A list of posts
        """
        if country_code is None:
            country_code = self.country_code
            
        print(f"Searching posts for keyword {keyword}")
        retry = 0
        posts = []
        cursor = 0

        loop_index = 1
        while True:
            try:
                params = {
                    "keyword": keyword,
                    "count": 20,
                    "region": country_code.upper(),
                    "offset": cursor
                }
                print(params)
                response = requests.get(
                    self.RAPID_URL_SEARCH,
                    headers=self.headers,
                    params=params)

                data = response.json()
                cursor = data["cursor"]
                aweme_list = data["aweme_list"]
                if len(aweme_list) <= 0:
                    break
                else:
                    posts.extend(aweme_list)
                print(f"Total posts {loop_index}: {len(posts)}")
            except Exception as e:
                print(f"Error searching posts: {e}")
                retry += 1
            if retry > self.MAX_KEYWORD_POST_RETRY:
                break
            if len(posts) > self.MAX_POST_BY_KEYWORD:
                break
            loop_index += 1
        return posts
    
    @staticmethod
    def _hashtag_detect(text):
        """
        Detect hashtags in a text.
        
        Args:
            text (str): The text to detect hashtags in
            
        Returns:
            list: A list of hashtags
        """
        if not text:
            return []
        
        import re
        hashtags = re.findall(r'#(\w+)', text)
        return hashtags 