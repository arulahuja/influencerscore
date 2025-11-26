document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const btn = document.getElementById('analyzeBtn');
    const btnText = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.loader');
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');
    
    // Reset UI
    errorDiv.style.display = 'none';
    resultsDiv.style.display = 'none';
    btn.disabled = true;
    btnText.textContent = 'Analyzing...';
    loader.style.display = 'inline-block';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze');
        }
        
        displayResults(data);
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Analyze';
        loader.style.display = 'none';
    }
});

function displayResults(data) {
    const { profile, engagement, content, score } = data;
    
    // Profile Section
    document.getElementById('profilePic').src = profile.profile_pic;
    document.getElementById('fullName').textContent = profile.full_name || data.username;
    document.getElementById('usernameDisplay').textContent = data.username;
    document.getElementById('categoryBadge').textContent = profile.category;
    
    if (profile.is_verified) {
        document.getElementById('verifiedBadge').style.display = 'inline-block';
    }
    if (profile.is_business) {
        document.getElementById('businessBadge').style.display = 'inline-block';
    }
    
    // Score Section
    const totalScore = score.total_score;
    document.getElementById('totalScore').textContent = totalScore;
    document.getElementById('scoreTier').textContent = score.tier;
    
    // Set tier class
    const tierClass = 'tier-' + score.tier.toLowerCase().replace(/\+/g, '-plus').replace(' ', '-');
    document.getElementById('scoreTier').className = `tier-badge ${tierClass}`;
    
    // Animate score circle
    const circle = document.getElementById('scoreCircle');
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (totalScore / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    
    // Set circle color based on score
    if (totalScore >= 80) circle.style.stroke = '#ffd700';
    else if (totalScore >= 70) circle.style.stroke = '#4CAF50';
    else if (totalScore >= 60) circle.style.stroke = '#2196F3';
    else if (totalScore >= 50) circle.style.stroke = '#9C27B0';
    else if (totalScore >= 40) circle.style.stroke = '#FF9800';
    else circle.style.stroke = '#f44336';
    
    // Score Breakdown
    updateBreakdown('engagement', score.breakdown.engagement_quality.score, 40);
    updateBreakdown('reach', score.breakdown.reach.score, 25);
    updateBreakdown('content', score.breakdown.content_quality.score, 15);
    updateBreakdown('credibility', score.breakdown.credibility.score, 10);
    updateBreakdown('brand', score.breakdown.brand_collaboration.score, 10);
    
    // Metrics
    document.getElementById('followers').textContent = formatNumber(profile.followers);
    document.getElementById('avgLikes').textContent = formatNumber(engagement.avg_likes);
    document.getElementById('avgComments').textContent = formatNumber(engagement.avg_comments);
    document.getElementById('engagementRate').textContent = engagement.avg_engagement_rate + '%';
    document.getElementById('postsCount').textContent = formatNumber(profile.posts_count);
    document.getElementById('brandsCount').textContent = content.brands_count;
    
    // Content Distribution
    document.getElementById('numImages').textContent = content.num_images;
    document.getElementById('numCarousels').textContent = content.num_carousel;
    document.getElementById('numVideos').textContent = content.num_videos;
    
    // Show results
    document.getElementById('results').style.display = 'block';
}

function updateBreakdown(id, score, max) {
    document.getElementById(`${id}Score`).textContent = score.toFixed(1);
    const percentage = (score / max) * 100;
    document.getElementById(`${id}Bar`).style.width = percentage + '%';
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}
