def analyze_friendships():
    """
    Analyze friendship patterns across different social media platforms
    
    Returns:
        dict: Dictionary containing various friendship analysis results
    """
    
    # User friends on different platforms
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}
    
    print("🌐 SOCIAL MEDIA FRIEND ANALYSIS")
    print("=" * 50)
    print()
    
    # Display platform data
    print("📱 Platform Friend Lists:")
    print(f"   Facebook: {sorted(facebook_friends)}")
    print(f"   Instagram: {sorted(instagram_friends)}")
    print(f"   Twitter: {sorted(twitter_friends)}")
    print(f"   LinkedIn: {sorted(linkedin_friends)}")
    print()
    
    # 1. Find friends who are on ALL four platforms (intersection)
    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends
    print("1️⃣ Friends on ALL platforms:")
    print(f"   Facebook ∩ Instagram ∩ Twitter ∩ LinkedIn = {sorted(all_platforms)}")
    print()
    
    # 2. Find friends who are ONLY on Facebook (not on any other platform)
    facebook_only = facebook_friends - instagram_friends - twitter_friends - linkedin_friends
    print("2️⃣ Friends ONLY on Facebook:")
    print(f"   Facebook - (Instagram ∪ Twitter ∪ LinkedIn) = {sorted(facebook_only)}")
    print()
    
    # 3. Find friends who are on Instagram OR Twitter but NOT on both (symmetric difference)
    instagram_xor_twitter = instagram_friends ^ twitter_friends
    print("3️⃣ Friends on Instagram XOR Twitter (but not both):")
    print(f"   Instagram ⊕ Twitter = {sorted(instagram_xor_twitter)}")
    print(f"   Instagram only: {sorted(instagram_friends - twitter_friends)}")
    print(f"   Twitter only: {sorted(twitter_friends - instagram_friends)}")
    print()
    
    # 4. Find the total unique friends across all platforms (union)
    total_unique = facebook_friends | instagram_friends | twitter_friends | linkedin_friends
    print("4️⃣ Total unique friends across all platforms:")
    print(f"   Facebook ∪ Instagram ∪ Twitter ∪ LinkedIn = {sorted(total_unique)}")
    print(f"   Count: {len(total_unique)} unique friends")
    print()
    
    # 5. Find friends who are on exactly 2 platforms
    exactly_two_platforms = set()
    
    # Create a dictionary to count platform appearances for each friend
    friend_platform_count = {}
    for friend in total_unique:
        count = 0
        platforms = []
        
        if friend in facebook_friends:
            count += 1
            platforms.append("Facebook")
        if friend in instagram_friends:
            count += 1
            platforms.append("Instagram")
        if friend in twitter_friends:
            count += 1
            platforms.append("Twitter")
        if friend in linkedin_friends:
            count += 1
            platforms.append("LinkedIn")
        
        friend_platform_count[friend] = (count, platforms)
        
        if count == 2:
            exactly_two_platforms.add(friend)
    
    print("5️⃣ Friends on exactly 2 platforms:")
    print(f"   Friends with exactly 2 platforms: {sorted(exactly_two_platforms)}")
    
    # Show detailed breakdown
    print("   📊 Detailed platform breakdown:")
    for friend in sorted(friend_platform_count.keys()):
        count, platforms = friend_platform_count[friend]
        platform_str = ", ".join(platforms)
        status = "✅" if count == 2 else "  "
        print(f"      {status} {friend}: {count} platform(s) ({platform_str})")
    print()
    
    # Additional analytics
    print("📊 ADDITIONAL ANALYTICS:")
    print("-" * 30)
    
    # Platform popularity (most friends)
    platform_sizes = {
        "Facebook": len(facebook_friends),
        "Instagram": len(instagram_friends),
        "Twitter": len(twitter_friends),
        "LinkedIn": len(linkedin_friends)
    }
    
    most_popular = max(platform_sizes.items(), key=lambda x: x[1])
    least_popular = min(platform_sizes.items(), key=lambda x: x[1])
    
    print("🏆 Platform Popularity:")
    for platform, size in sorted(platform_sizes.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * (size // 2) if size > 0 else ""
        print(f"   {platform}: {size} friends {bar}")
    
    print(f"\n   Most popular: {most_popular[0]} ({most_popular[1]} friends)")
    print(f"   Least popular: {least_popular[0]} ({least_popular[1]} friends)")
    print()
    
    # Friend distribution analysis
    platform_distribution = {}
    for count in range(1, 5):
        friends_with_count = [friend for friend, (c, _) in friend_platform_count.items() if c == count]
        platform_distribution[count] = friends_with_count
    
    print("📈 Friend Distribution Across Platforms:")
    for count, friends in platform_distribution.items():
        plural = "platform" if count == 1 else "platforms"
        print(f"   {count} {plural}: {len(friends)} friends {sorted(friends) if friends else '[]'}")
    print()
    
    # Platform overlap analysis
    print("🔗 Platform Overlap Analysis:")
    overlaps = {
        "Facebook & Instagram": len(facebook_friends & instagram_friends),
        "Facebook & Twitter": len(facebook_friends & twitter_friends),
        "Facebook & LinkedIn": len(facebook_friends & linkedin_friends),
        "Instagram & Twitter": len(instagram_friends & twitter_friends),
        "Instagram & LinkedIn": len(instagram_friends & linkedin_friends),
        "Twitter & LinkedIn": len(twitter_friends & linkedin_friends)
    }
    
    for pair, overlap_count in sorted(overlaps.items(), key=lambda x: x[1], reverse=True):
        print(f"   {pair}: {overlap_count} common friends")
    print()
    
    # Return dictionary with all results
    results = {
        'all_platforms': all_platforms,
        'facebook_only': facebook_only,
        'instagram_xor_twitter': instagram_xor_twitter,
        'total_unique': total_unique,
        'exactly_two_platforms': exactly_two_platforms,
        'platform_sizes': platform_sizes,
        'platform_distribution': platform_distribution,
        'platform_overlaps': overlaps,
        'friend_platform_details': friend_platform_count
    }
    
    return results


def demonstrate_set_operations():
    """Demonstrate various set operations with examples"""
    print("📚 SET OPERATIONS DEMONSTRATION")
    print("=" * 50)
    print()
    
    # Basic set operations
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    
    print("🔢 Basic Set Operations:")
    print(f"   Set A: {set_a}")
    print(f"   Set B: {set_b}")
    print()
    
    print("   Union (A ∪ B):")
    union_result = set_a | set_b
    print(f"      A | B = {union_result}")
    print(f"      A.union(B) = {set_a.union(set_b)}")
    print()
    
    print("   Intersection (A ∩ B):")
    intersection_result = set_a & set_b
    print(f"      A & B = {intersection_result}")
    print(f"      A.intersection(B) = {set_a.intersection(set_b)}")
    print()
    
    print("   Difference (A - B):")
    difference_result = set_a - set_b
    print(f"      A - B = {difference_result}")
    print(f"      A.difference(B) = {set_a.difference(set_b)}")
    print()
    
    print("   Symmetric Difference (A ⊕ B):")
    sym_diff_result = set_a ^ set_b
    print(f"      A ^ B = {sym_diff_result}")
    print(f"      A.symmetric_difference(B) = {set_a.symmetric_difference(set_b)}")
    print()
    
    # Set relationships
    print("🔗 Set Relationships:")
    subset_example = {2, 3}
    superset_example = {1, 2, 3, 4, 5, 6}
    disjoint_example = {9, 10, 11}
    
    print(f"   Subset check: {subset_example} ⊆ {set_a}")
    print(f"      {subset_example}.issubset({set_a}) = {subset_example.issubset(set_a)}")
    print()
    
    print(f"   Superset check: {superset_example} ⊇ {set_a}")
    print(f"      {superset_example}.issuperset({set_a}) = {superset_example.issuperset(set_a)}")
    print()
    
    print(f"   Disjoint check: {set_a} ∩ {disjoint_example} = ∅")
    print(f"      {set_a}.isdisjoint({disjoint_example}) = {set_a.isdisjoint(disjoint_example)}")
    print()


def advanced_friendship_analysis():
    """Perform advanced friendship analysis with additional metrics"""
    print("🚀 ADVANCED FRIENDSHIP ANALYSIS")
    print("=" * 50)
    print()
    
    # Get basic analysis
    results = analyze_friendships()
    
    # Calculate friendship strength (based on platform overlap)
    print("💪 Friendship Strength Analysis:")
    print("   (Based on number of shared platforms)")
    print()
    
    friend_details = results['friend_platform_details']
    
    # Group friends by platform count
    strength_groups = {
        4: [],  # Strong (all platforms)
        3: [],  # Good (3 platforms)
        2: [],  # Moderate (2 platforms)
        1: []   # Weak (1 platform)
    }
    
    for friend, (count, platforms) in friend_details.items():
        strength_groups[count].append((friend, platforms))
    
    strength_labels = {
        4: "🔥 SUPER CONNECTED",
        3: "💪 WELL CONNECTED", 
        2: "👥 MODERATELY CONNECTED",
        1: "🔗 SINGLE PLATFORM"
    }
    
    for strength, friends in strength_groups.items():
        if friends:
            label = strength_labels[strength]
            print(f"   {label} ({strength} platforms):")
            for friend, platforms in sorted(friends):
                platform_icons = {
                    "Facebook": "📘",
                    "Instagram": "📷", 
                    "Twitter": "🐦",
                    "LinkedIn": "💼"
                }
                platform_str = " ".join([platform_icons.get(p, "📱") for p in platforms])
                print(f"      {friend}: {platform_str} {platforms}")
            print()
    
    # Network connectivity analysis
    print("🌐 Network Connectivity:")
    total_friends = len(results['total_unique'])
    connected_friends = len([f for f, (c, _) in friend_details.items() if c > 1])
    connectivity_rate = (connected_friends / total_friends) * 100 if total_friends > 0 else 0
    
    print(f"   Total friends: {total_friends}")
    print(f"   Multi-platform friends: {connected_friends}")
    print(f"   Connectivity rate: {connectivity_rate:.1f}%")
    print()
    
    # Platform loyalty analysis
    print("🎯 Platform Loyalty Analysis:")
    single_platform_friends = strength_groups[1]
    if single_platform_friends:
        platform_loyalty = {}
        for friend, platforms in single_platform_friends:
            platform = platforms[0]
            if platform not in platform_loyalty:
                platform_loyalty[platform] = []
            platform_loyalty[platform].append(friend)
        
        for platform, loyal_friends in platform_loyalty.items():
            print(f"   {platform} exclusive: {len(loyal_friends)} friends {sorted(loyal_friends)}")
    print()


def main():
    """Main function to run the friendship analysis"""
    print("🎯 SOCIAL MEDIA FRIEND ANALYSIS SYSTEM")
    print("=" * 60)
    print()
    
    # Run the main analysis
    result = analyze_friendships()
    
    print("✅ FINAL RESULTS SUMMARY:")
    print("-" * 30)
    print(f"All platforms: {sorted(result.get('all_platforms', set()))}")
    print(f"Facebook only: {sorted(result.get('facebook_only', set()))}")
    print(f"Instagram XOR Twitter: {sorted(result.get('instagram_xor_twitter', set()))}")
    print(f"Total unique friends: {len(result.get('total_unique', set()))} friends")
    print(f"Exactly 2 platforms: {sorted(result.get('exactly_two_platforms', set()))}")
    print()
    
    # Run demonstrations
    demonstrate_set_operations()
    advanced_friendship_analysis()
    
    print("🎉 FRIENDSHIP ANALYSIS COMPLETE!")
    print("=" * 60)
    print()
    print("✅ Analysis completed successfully:")
    print("   • Set intersection for common friends")
    print("   • Set difference for exclusive friends") 
    print("   • Set symmetric difference for XOR operations")
    print("   • Set union for total unique friends")
    print("   • Custom logic for multi-platform analysis")
    print("   • Advanced friendship strength metrics")
    print("   • Platform loyalty and connectivity analysis")
    print()


if __name__ == "__main__":
    main()
