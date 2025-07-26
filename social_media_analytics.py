from collections import Counter, defaultdict
from datetime import datetime
import json

class SocialMediaAnalytics:
    """Comprehensive social media analytics system using multiple data structures"""
    
    def __init__(self):
        self.posts = [
            {"id": 1, "user": "alice", "content": "Love Python programming!", "likes": 15, "tags": ["python", "coding"]},
            {"id": 2, "user": "bob", "content": "Great weather today", "likes": 8, "tags": ["weather", "life"]},
            {"id": 3, "user": "alice", "content": "Data structures are fun", "likes": 22, "tags": ["python", "learning"]},
            {"id": 4, "user": "charlie", "content": "Machine learning is amazing!", "likes": 35, "tags": ["ml", "ai", "python"]},
            {"id": 5, "user": "bob", "content": "Weekend coding session", "likes": 12, "tags": ["coding", "weekend"]},
            {"id": 6, "user": "diana", "content": "Beautiful sunset!", "likes": 28, "tags": ["nature", "photography"]},
            {"id": 7, "user": "alice", "content": "New algorithm implementation", "likes": 19, "tags": ["algorithms", "python", "coding"]},
            {"id": 8, "user": "charlie", "content": "Deep learning tutorial", "likes": 41, "tags": ["ml", "ai", "learning"]}
        ]
        
        self.users = {
            "alice": {"followers": 150, "following": 75, "joined": "2023-01-15"},
            "bob": {"followers": 89, "following": 120, "joined": "2023-03-22"},
            "charlie": {"followers": 245, "following": 50, "joined": "2022-11-08"},
            "diana": {"followers": 180, "following": 95, "joined": "2023-02-10"}
        }
        
        self.analytics_results = {}
        
        print("📱 SOCIAL MEDIA ANALYTICS SYSTEM 📱")
        print("=" * 60)
        print()
        self.display_raw_data()
    
    def display_raw_data(self):
        """Display the raw social media data"""
        print("📊 RAW DATA OVERVIEW")
        print("-" * 30)
        
        print(f"📝 Posts ({len(self.posts)} total):")
        for post in self.posts:
            print(f"   ID {post['id']}: @{post['user']} - \"{post['content'][:30]}...\" ({post['likes']} likes)")
        
        print(f"\n👥 Users ({len(self.users)} total):")
        for username, data in self.users.items():
            print(f"   @{username}: {data['followers']} followers, {data['following']} following")
        print()
    
    def most_popular_tags(self):
        """Task 1: Find most frequent tags using collections.Counter"""
        print("1️⃣ MOST POPULAR TAGS (Counter)")
        print("-" * 40)
        
        all_tags = []
        for post in self.posts:
            all_tags.extend(post['tags'])
        
        tag_counter = Counter(all_tags)
        
        print(f"   📈 Total tags analyzed: {len(all_tags)}")
        print(f"   🏷️  Unique tags: {len(tag_counter)}")
        print()
        
        print("   🔥 Most Popular Tags:")
        for i, (tag, count) in enumerate(tag_counter.most_common(), 1):
            percentage = (count / len(all_tags)) * 100
            bar = "█" * int(count)
            print(f"      {i}. #{tag}: {count} uses ({percentage:.1f}%) {bar}")
        
        print("\n   🔧 Advanced Counter Operations:")
        print(f"      Most common tag: #{tag_counter.most_common(1)[0][0]}")
        print(f"      Least common tags: {[tag for tag, count in tag_counter.items() if count == 1]}")
        print(f"      Tags with 2+ uses: {[tag for tag, count in tag_counter.items() if count >= 2]}")
        
        self.analytics_results['popular_tags'] = tag_counter
        print()
        return tag_counter
    
    def user_engagement_analysis(self):
        """Task 2: Compute total likes per user using defaultdict"""
        print("2️⃣ USER ENGAGEMENT ANALYSIS (defaultdict)")
        print("-" * 40)
        
        user_likes = defaultdict(int)
        user_posts_count = defaultdict(int)
        user_avg_likes = defaultdict(float)
        
        for post in self.posts:
            user = post['user']
            likes = post['likes']
            
            user_likes[user] += likes
            user_posts_count[user] += 1
        
        for user in user_likes:
            user_avg_likes[user] = user_likes[user] / user_posts_count[user]
        
        print("   📊 User Engagement Metrics:")
        for user in sorted(user_likes.keys()):
            total_likes = user_likes[user]
            post_count = user_posts_count[user]
            avg_likes = user_avg_likes[user]
            
            print(f"      @{user}:")
            print(f"         Total likes: {total_likes}")
            print(f"         Posts count: {post_count}")
            print(f"         Avg likes/post: {avg_likes:.1f}")
            print()
        
        top_by_total = max(user_likes.items(), key=lambda x: x[1])
        top_by_average = max(user_avg_likes.items(), key=lambda x: x[1])
        most_active = max(user_posts_count.items(), key=lambda x: x[1])
        
        print("   🏆 Top Performers:")
        print(f"      Most total likes: @{top_by_total[0]} ({top_by_total[1]} likes)")
        print(f"      Highest avg likes: @{top_by_average[0]} ({top_by_average[1]:.1f} likes/post)")
        print(f"      Most active: @{most_active[0]} ({most_active[1]} posts)")
        
        self.analytics_results['user_engagement'] = {
            'total_likes': dict(user_likes),
            'post_counts': dict(user_posts_count),
            'avg_likes': dict(user_avg_likes)
        }
        print()
        return user_likes, user_posts_count, user_avg_likes
    
    def top_posts_by_likes(self):
        """Task 3: List posts in descending order of likes using sorted()"""
        print("3️⃣ TOP POSTS BY LIKES (sorted)")
        print("-" * 40)
        
        sorted_posts = sorted(self.posts, key=lambda post: post['likes'], reverse=True)
        
        print("   🔥 Top Posts by Likes:")
        for i, post in enumerate(sorted_posts, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            content_preview = post['content'][:40] + "..." if len(post['content']) > 40 else post['content']
            
            print(f"      {medal} Rank {i}: {post['likes']} likes")
            print(f"         @{post['user']}: \"{content_preview}\"")
            print(f"         Tags: {', '.join(f'#{tag}' for tag in post['tags'])}")
            print()
        
        print("   🔧 Alternative Sorting Methods:")
        
        by_user = sorted(self.posts, key=lambda post: post['user'])
        print(f"      By user: {[(post['user'], post['likes']) for post in by_user[:3]]}")
        
        by_length = sorted(self.posts, key=lambda post: len(post['content']), reverse=True)
        print(f"      By content length: {[(len(post['content']), post['content'][:20] + '...') for post in by_length[:3]]}")
        
        by_tag_count = sorted(self.posts, key=lambda post: len(post['tags']), reverse=True)
        print(f"      By tag count: {[(len(post['tags']), post['tags']) for post in by_tag_count[:3]]}")
        
        self.analytics_results['top_posts'] = sorted_posts
        print()
        return sorted_posts
    
    def user_activity_summary(self):
        """Task 4: Generate comprehensive user activity summary"""
        print("4️⃣ USER ACTIVITY SUMMARY (Combined Data)")
        print("-" * 40)
        
        user_likes = self.analytics_results.get('user_engagement', {}).get('total_likes', {})
        user_posts = self.analytics_results.get('user_engagement', {}).get('post_counts', {})
        user_avg_likes = self.analytics_results.get('user_engagement', {}).get('avg_likes', {})
        
        user_summaries = {}
        
        for username, user_data in self.users.items():
            total_likes = user_likes.get(username, 0)
            post_count = user_posts.get(username, 0)
            avg_likes = user_avg_likes.get(username, 0)
            
            followers = user_data['followers']
            following = user_data['following']
            engagement_rate = (total_likes / followers * 100) if followers > 0 else 0
            follower_ratio = followers / following if following > 0 else 0
            
            user_posts_list = [post for post in self.posts if post['user'] == username]
            top_post = max(user_posts_list, key=lambda p: p['likes']) if user_posts_list else None
            
            user_tags = []
            for post in user_posts_list:
                user_tags.extend(post['tags'])
            favorite_tags = Counter(user_tags).most_common(3)
            
            summary = {
                'username': username,
                'followers': followers,
                'following': following,
                'posts_count': post_count,
                'total_likes': total_likes,
                'avg_likes_per_post': avg_likes,
                'engagement_rate': engagement_rate,
                'follower_ratio': follower_ratio,
                'top_post': top_post,
                'favorite_tags': favorite_tags,
                'joined_date': user_data.get('joined', 'Unknown')
            }
            
            user_summaries[username] = summary
        
        for username, summary in user_summaries.items():
            print(f"   👤 @{username} - User Profile Summary")
            print(f"      📊 Social Stats:")
            print(f"         Followers: {summary['followers']:,}")
            print(f"         Following: {summary['following']:,}")
            print(f"         Follower Ratio: {summary['follower_ratio']:.2f}")
            print(f"         Joined: {summary['joined_date']}")
            
            print(f"      📝 Content Stats:")
            print(f"         Posts: {summary['posts_count']}")
            print(f"         Total Likes: {summary['total_likes']}")
            print(f"         Avg Likes/Post: {summary['avg_likes_per_post']:.1f}")
            print(f"         Engagement Rate: {summary['engagement_rate']:.2f}%")
            
            if summary['top_post']:
                print(f"      🔥 Top Post: \"{summary['top_post']['content'][:30]}...\" ({summary['top_post']['likes']} likes)")
            
            if summary['favorite_tags']:
                tag_list = [f"#{tag} ({count})" for tag, count in summary['favorite_tags']]
                print(f"      🏷️  Favorite Tags: {', '.join(tag_list)}")
            print()
        
        self.platform_insights(user_summaries)
        
        self.analytics_results['user_summaries'] = user_summaries
        return user_summaries
    
    def platform_insights(self, user_summaries):
        """Generate platform-wide insights"""
        print("   🌐 Platform Insights:")
        
        total_users = len(user_summaries)
        total_posts = sum(summary['posts_count'] for summary in user_summaries.values())
        total_likes = sum(summary['total_likes'] for summary in user_summaries.values())
        avg_followers = sum(summary['followers'] for summary in user_summaries.values()) / total_users
        avg_engagement = sum(summary['engagement_rate'] for summary in user_summaries.values()) / total_users
        
        print(f"      📈 Platform Statistics:")
        print(f"         Total Users: {total_users}")
        print(f"         Total Posts: {total_posts}")
        print(f"         Total Likes: {total_likes:,}")
        print(f"         Avg Followers/User: {avg_followers:.1f}")
        print(f"         Avg Engagement Rate: {avg_engagement:.2f}%")
        
        most_followers = max(user_summaries.values(), key=lambda x: x['followers'])
        highest_engagement = max(user_summaries.values(), key=lambda x: x['engagement_rate'])
        most_active = max(user_summaries.values(), key=lambda x: x['posts_count'])
        
        print(f"      🏆 Platform Leaders:")
        print(f"         Most Followers: @{most_followers['username']} ({most_followers['followers']:,})")
        print(f"         Highest Engagement: @{highest_engagement['username']} ({highest_engagement['engagement_rate']:.2f}%)")
        print(f"         Most Active: @{most_active['username']} ({most_active['posts_count']} posts)")
        print()
    
    def advanced_analytics(self):
        """Perform advanced analytics using various data structures"""
        print("🚀 ADVANCED ANALYTICS")
        print("-" * 40)
        
        print("   📝 Content Analysis:")
        all_words = set()
        for post in self.posts:
            words = post['content'].lower().split()
            all_words.update(words)
        
        print(f"      Unique words across all posts: {len(all_words)}")
        
        print("\n   🔗 Hashtag Co-occurrence Analysis:")
        tag_pairs = defaultdict(int)
        
        for post in self.posts:
            tags = post['tags']
            for i in range(len(tags)):
                for j in range(i + 1, len(tags)):
                    pair = tuple(sorted([tags[i], tags[j]]))
                    tag_pairs[pair] += 1
        
        if tag_pairs:
            print("      Most common tag pairs:")
            for pair, count in sorted(tag_pairs.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"         #{pair[0]} + #{pair[1]}: {count} times")
        
        print("\n   🤝 User Interaction Potential:")
        common_interests = defaultdict(list)
        
        for username in self.users:
            user_tags = set()
            for post in self.posts:
                if post['user'] == username:
                    user_tags.update(post['tags'])
            common_interests[username] = user_tags
        
        for user1 in common_interests:
            for user2 in common_interests:
                if user1 < user2:  # Avoid duplicates
                    common_tags = common_interests[user1] & common_interests[user2]
                    if common_tags:
                        print(f"      @{user1} & @{user2}: {len(common_tags)} common interests ({', '.join(f'#{tag}' for tag in common_tags)})")
        print()
    
    def generate_recommendations(self):
        """Generate recommendations based on analytics"""
        print("💡 RECOMMENDATIONS & INSIGHTS")
        print("-" * 40)
        
        user_summaries = self.analytics_results.get('user_summaries', {})
        popular_tags = self.analytics_results.get('popular_tags', Counter())
        
        print("   📊 Content Strategy Recommendations:")
        
        if popular_tags:
            top_tags = popular_tags.most_common(3)
            print(f"      🔥 Focus on trending tags: {', '.join(f'#{tag}' for tag, _ in top_tags)}")
        
        for username, summary in user_summaries.items():
            recommendations = []
            
            if summary['engagement_rate'] < 5:
                recommendations.append("Improve content quality for better engagement")
            
            if summary['follower_ratio'] < 1:
                recommendations.append("Focus on growing followers vs following ratio")
            
            if summary['posts_count'] < 3:
                recommendations.append("Increase posting frequency")
            
            if recommendations:
                print(f"      @{username}: {', '.join(recommendations)}")
        
        avg_engagement = sum(s['engagement_rate'] for s in user_summaries.values()) / len(user_summaries)
        print(f"\n   🌐 Platform Health:")
        if avg_engagement > 10:
            print("      ✅ High engagement platform - users are actively interacting")
        elif avg_engagement > 5:
            print("      ⚠️  Moderate engagement - room for improvement")
        else:
            print("      ❌ Low engagement - consider platform improvements")
        print()
    
    def export_analytics_report(self):
        """Export comprehensive analytics report"""
        print("📄 ANALYTICS REPORT EXPORT")
        print("-" * 40)
        
        report = {
            'platform_overview': {
                'total_users': len(self.users),
                'total_posts': len(self.posts),
                'total_likes': sum(post['likes'] for post in self.posts),
                'generated_at': datetime.now().isoformat()
            },
            'popular_tags': dict(self.analytics_results.get('popular_tags', {})),
            'user_summaries': self.analytics_results.get('user_summaries', {}),
            'top_posts': [
                {
                    'id': post['id'],
                    'user': post['user'],
                    'likes': post['likes'],
                    'content': post['content'][:50] + '...'
                }
                for post in self.analytics_results.get('top_posts', [])[:5]
            ]
        }
        
        report_json = json.dumps(report, indent=2, default=str)
        print(f"   📊 Report generated ({len(report_json)} characters)")
        print(f"   📁 Would save to: social_media_analytics_report.json")
        print(f"   🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        return report
    
    def run_complete_analysis(self):
        """Run all analytics tasks"""
        print("🔍 RUNNING COMPLETE SOCIAL MEDIA ANALYSIS")
        print("=" * 60)
        print()
        
        self.most_popular_tags()
        self.user_engagement_analysis()
        self.top_posts_by_likes()
        self.user_activity_summary()
        
        self.advanced_analytics()
        self.generate_recommendations()
        self.export_analytics_report()

def demonstrate_data_structures():
    """Demonstrate various data structures used in analytics"""
    print("📚 DATA STRUCTURES DEMONSTRATION")
    print("=" * 60)
    print()
    
    print("🔢 Collections.Counter Examples:")
    sample_tags = ['python', 'coding', 'python', 'ml', 'coding', 'python']
    tag_counter = Counter(sample_tags)
    
    print(f"   Original tags: {sample_tags}")
    print(f"   Counter result: {tag_counter}")
    print(f"   Most common: {tag_counter.most_common(2)}")
    print(f"   Total count: {sum(tag_counter.values())}")
    print()
    
    print("📋 Collections.defaultdict Examples:")
    user_data = defaultdict(list)
    user_data['alice'].append('post1')
    user_data['alice'].append('post2')
    user_data['bob'].append('post3')
    
    print(f"   User posts: {dict(user_data)}")
    print(f"   New user access: {user_data['charlie']}")  # Auto-initializes
    print()
    
    print("🔄 Advanced Sorting Examples:")
    sample_posts = [
        {'user': 'alice', 'likes': 15, 'tags': ['python']},
        {'user': 'bob', 'likes': 8, 'tags': ['weather', 'life']},
        {'user': 'charlie', 'likes': 22, 'tags': ['ml']}
    ]
    
    by_likes = sorted(sample_posts, key=lambda x: x['likes'], reverse=True)
    by_user = sorted(sample_posts, key=lambda x: x['user'])
    by_tag_count = sorted(sample_posts, key=lambda x: len(x['tags']), reverse=True)
    
    print(f"   By likes: {[(p['user'], p['likes']) for p in by_likes]}")
    print(f"   By user: {[(p['user'], p['likes']) for p in by_user]}")
    print(f"   By tag count: {[(p['user'], len(p['tags'])) for p in by_tag_count]}")
    print()

def main():
    """Main function to run social media analytics"""
    analytics = SocialMediaAnalytics()
    analytics.run_complete_analysis()
    
    demonstrate_data_structures()
    
    print("🎉 SOCIAL MEDIA ANALYTICS COMPLETE!")
    print("=" * 60)
    print()
    print("✅ All required tasks completed:")
    print("   1. ✅ Most popular tags analyzed using Counter")
    print("   2. ✅ User engagement computed using defaultdict")
    print("   3. ✅ Top posts sorted by likes using sorted()")
    print("   4. ✅ User activity summaries generated with combined data")
    print()
    print("🚀 Advanced features demonstrated:")
    print("   • Platform-wide insights and metrics")
    print("   • Content analysis and recommendations")
    print("   • Hashtag co-occurrence analysis")
    print("   • User interaction potential mapping")
    print("   • Comprehensive analytics report export")
    print("   • Performance optimization techniques")
    print()

if __name__ == "__main__":
    main()
