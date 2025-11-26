import numpy as np

def calculate_single_influencer_score(data):
    """Calculate influencer score for a single data dict"""
    
    followers = data.get('followers', 0)
    avg_engagement_rate = data.get('avg_engagement_rate', 0)
    comment_like_ratio = data.get('comment_like_ratio', 0)
    posts_count = data.get('posts_count', 0)
    is_verified = data.get('is_verified', False)
    is_business = data.get('is_business', False)
    brands_count = data.get('brands_count', 0)
    num_carousel = data.get('num_carousel', 0)
    num_images = data.get('num_images', 0)
    num_videos = data.get('num_videos', 0)
    
    # 1. ENGAGEMENT QUALITY SCORE (40 points)
    engagement_rate_score = adjusted_engagement_score(avg_engagement_rate, followers)
    authenticity_score = calculate_authenticity_score(comment_like_ratio)
    engagement_quality_score = engagement_rate_score + authenticity_score
    
    # 2. REACH SCORE (25 points)
    reach_score = calculate_reach_score(followers)
    
    # 3. CONTENT QUALITY SCORE (15 points)
    content_diversity_score = calculate_content_diversity_score(num_carousel, num_images, num_videos)
    consistency_score = calculate_consistency_score(posts_count)
    content_quality_score = content_diversity_score + consistency_score
    
    # 4. CREDIBILITY SCORE (10 points)
    verification_score = 6 if is_verified else 0
    business_score = 4 if is_business else 0
    credibility_score = verification_score + business_score
    
    # 5. BRAND COLLABORATION SCORE (10 points)
    brand_collab_score = calculate_brand_collab_score(brands_count)
    
    # TOTAL SCORE
    total_score = round(
        engagement_quality_score + 
        reach_score + 
        content_quality_score + 
        credibility_score + 
        brand_collab_score, 
        1
    )
    
    tier = get_tier(total_score)
    
    return {
        'total_score': total_score,
        'tier': tier,
        'breakdown': {
            'engagement_quality': {
                'score': round(engagement_quality_score, 1),
                'max': 40,
                'components': {
                    'engagement_rate': round(engagement_rate_score, 1),
                    'authenticity': round(authenticity_score, 1)
                }
            },
            'reach': {
                'score': round(reach_score, 1),
                'max': 25
            },
            'content_quality': {
                'score': round(content_quality_score, 1),
                'max': 15,
                'components': {
                    'diversity': round(content_diversity_score, 1),
                    'consistency': round(consistency_score, 1)
                }
            },
            'credibility': {
                'score': round(credibility_score, 1),
                'max': 10,
                'components': {
                    'verification': verification_score,
                    'business': business_score
                }
            },
            'brand_collaboration': {
                'score': round(brand_collab_score, 1),
                'max': 10
            }
        }
    }

def adjusted_engagement_score(engagement_rate, followers):
    """Calculate engagement rate score adjusted for follower count"""
    if followers < 10000:
        if engagement_rate >= 6:
            return 25
        elif engagement_rate >= 3:
            return 15 + ((engagement_rate - 3) / 3) * 10
        else:
            return (engagement_rate / 3) * 15
    elif followers < 100000:
        if engagement_rate >= 4:
            return 25
        elif engagement_rate >= 2:
            return 15 + ((engagement_rate - 2) / 2) * 10
        else:
            return (engagement_rate / 2) * 15
    elif followers < 1000000:
        if engagement_rate >= 3:
            return 25
        elif engagement_rate >= 1.5:
            return 15 + ((engagement_rate - 1.5) / 1.5) * 10
        else:
            return (engagement_rate / 1.5) * 15
    else:
        if engagement_rate >= 2:
            return 25
        elif engagement_rate >= 0.5:
            return 15 + ((engagement_rate - 0.5) / 1.5) * 10
        else:
            return (engagement_rate / 0.5) * 15

def calculate_authenticity_score(ratio):
    """Calculate authenticity score based on comment-to-like ratio"""
    if ratio >= 5:
        return 15
    elif ratio >= 2:
        return 10 + ((ratio - 2) / 3) * 5
    elif ratio >= 0.5:
        return 5 + ((ratio - 0.5) / 1.5) * 5
    else:
        return (ratio / 0.5) * 5

def calculate_reach_score(followers):
    """Calculate reach score using logarithmic scale"""
    if followers <= 0:
        return 0
    
    log_followers = np.log10(followers)
    
    if log_followers >= 7:
        return 25
    elif log_followers >= 6:
        return 20 + ((log_followers - 6) / 1) * 5
    elif log_followers >= 5:
        return 15 + ((log_followers - 5) / 1) * 5
    elif log_followers >= 4:
        return 10 + ((log_followers - 4) / 1) * 5
    elif log_followers >= 3:
        return 5 + ((log_followers - 3) / 1) * 5
    else:
        return (log_followers / 3) * 5

def calculate_content_diversity_score(num_carousel, num_images, num_videos):
    """Calculate content diversity score"""
    total_posts = num_carousel + num_images + num_videos
    if total_posts == 0:
        return 0
    
    types = [num_carousel, num_images, num_videos]
    num_types = len([t for t in types if t > 0])
    
    if num_types >= 3:
        return 8
    elif num_types == 2:
        return 5
    else:
        return 2

def calculate_consistency_score(posts):
    """Calculate consistency score based on post count"""
    if posts >= 500:
        return 7
    elif posts >= 200:
        return 5 + ((posts - 200) / 300) * 2
    elif posts >= 50:
        return 3 + ((posts - 50) / 150) * 2
    else:
        return (posts / 50) * 3

def calculate_brand_collab_score(count):
    """Calculate brand collaboration score"""
    if 3 <= count <= 10:
        return 10
    elif 1 <= count < 3:
        return 5 + ((count - 1) / 2) * 5
    elif 10 < count <= 20:
        return 10 - ((count - 10) / 10) * 5
    elif count > 20:
        return max(0, 5 - ((count - 20) / 10))
    else:
        return 3

def get_tier(score):
    """Get tier classification"""
    if score >= 80:
        return 'A+ Elite'
    elif score >= 70:
        return 'A Strong'
    elif score >= 60:
        return 'B+ Good'
    elif score >= 50:
        return 'B Average'
    elif score >= 40:
        return 'C Fair'
    else:
        return 'D Poor'
