import requests

class InfluencerTracker:
    def __init__(self, username):
        self.username = username
        self.data = None
        
    def fetch_data(self):
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.username}"
        headers = {
            "User-Agent": "Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                self.data = response.json()
                return True
            return False
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return False
    
    def get_profile_metrics(self):
        if not self.data:
            return None
        
        user = self.data['data']['user']
        return {
            'followers': user['edge_followed_by']['count'],
            'following': user['edge_follow']['count'],
            'posts_count': user['edge_owner_to_timeline_media']['count'],
            'biography': user['biography'],
            'category': user.get('category_name', 'N/A'),
            'is_verified': user['is_verified'],
            'is_business': user['is_business_account'],
            'full_name': user['full_name'],
            'profile_pic': user['profile_pic_url_hd']
        }
    
    def get_engagement_metrics(self, num_posts=12):
        if not self.data:
            return None
        
        posts = self.data['data']['user']['edge_owner_to_timeline_media']['edges'][:num_posts]
        followers = self.data['data']['user']['edge_followed_by']['count']
        
        if not posts or followers == 0:
            return None
        
        total_likes = 0
        total_comments = 0
        engagement_rates = []
        
        for post in posts:
            node = post['node']
            likes = node['edge_liked_by']['count']
            comments = node['edge_media_to_comment']['count']
            
            total_likes += likes
            total_comments += comments
            
            engagement = likes + comments
            eng_rate = (engagement / followers) * 100
            engagement_rates.append(eng_rate)
        
        avg_likes = total_likes / len(posts)
        avg_comments = total_comments / len(posts)
        
        return {
            'avg_likes': round(avg_likes, 2),
            'avg_comments': round(avg_comments, 2),
            'avg_engagement_rate': round(sum(engagement_rates) / len(engagement_rates), 2),
            'median_engagement_rate': round(sorted(engagement_rates)[len(engagement_rates)//2], 2) if engagement_rates else 0,
            'total_engagement': total_likes + total_comments,
            'comment_like_ratio': round((avg_comments / (avg_likes + 1)) * 100, 2)
        }
    
    def get_content_analysis(self):
        if not self.data:
            return None
        
        posts = self.data['data']['user']['edge_owner_to_timeline_media']['edges']
        
        if not posts:
            return None
        
        content_types = {}
        brands_mentioned = set()
        
        for post in posts:
            node = post['node']
            
            post_type = node['__typename']
            content_types[post_type] = content_types.get(post_type, 0) + 1
            
            for tagged in node.get('edge_media_to_tagged_user', {}).get('edges', []):
                brands_mentioned.add(tagged['node']['user']['username'])
        
        return {
            'num_carousel': content_types.get('GraphSidecar', 0),
            'num_images': content_types.get('GraphImage', 0),
            'num_videos': content_types.get('GraphVideo', 0),
            'brands_count': len(brands_mentioned),
            'brands_list': list(brands_mentioned)
        }
