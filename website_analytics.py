class WebsiteAnalytics:
    """Comprehensive website analytics using Python sets"""
    
    def __init__(self):
        self.monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
        self.tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
        self.wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}
        
        self.analytics_results = {}
    
    def display_raw_data(self):
        """Display the raw visitor data for each day"""
        print("📊 WEBSITE ANALYTICS - RAW VISITOR DATA 📊")
        print("=" * 60)
        print()
        print(f"Monday Visitors ({len(self.monday_visitors)}): {sorted(self.monday_visitors)}")
        print(f"Tuesday Visitors ({len(self.tuesday_visitors)}): {sorted(self.tuesday_visitors)}")
        print(f"Wednesday Visitors ({len(self.wednesday_visitors)}): {sorted(self.wednesday_visitors)}")
        print()
    
    def unique_visitors_all_days(self):
        """Task 1: Find total unique visitors across all three days"""
        print("1️⃣ UNIQUE VISITORS ACROSS ALL DAYS")
        print("-" * 40)
        
        all_unique_visitors = self.monday_visitors | self.tuesday_visitors | self.wednesday_visitors
        
        print(f"   Total unique visitors: {len(all_unique_visitors)}")
        print(f"   Visitor list: {sorted(all_unique_visitors)}")
        
        self.analytics_results['total_unique'] = {
            'count': len(all_unique_visitors),
            'visitors': sorted(all_unique_visitors)
        }
        print()
        return all_unique_visitors
    
    def returning_visitors_tuesday(self):
        """Task 2: Find users who visited on both Monday and Tuesday"""
        print("2️⃣ RETURNING VISITORS ON TUESDAY")
        print("-" * 40)
        
        returning_tuesday = self.monday_visitors & self.tuesday_visitors
        
        print(f"   Returning visitors on Tuesday: {len(returning_tuesday)}")
        if returning_tuesday:
            print(f"   Visitor list: {sorted(returning_tuesday)}")
            print(f"   These users visited on both Monday and Tuesday")
        else:
            print("   No returning visitors from Monday to Tuesday")
        
        self.analytics_results['returning_tuesday'] = {
            'count': len(returning_tuesday),
            'visitors': sorted(returning_tuesday)
        }
        print()
        return returning_tuesday
    
    def new_visitors_each_day(self):
        """Task 3: Find new visitors for each day (not seen on previous days)"""
        print("3️⃣ NEW VISITORS EACH DAY")
        print("-" * 40)
        
        new_monday = self.monday_visitors.copy()
        
        new_tuesday = self.tuesday_visitors - self.monday_visitors
        
        new_wednesday = self.wednesday_visitors - (self.monday_visitors | self.tuesday_visitors)
        
        print(f"   New visitors on Monday: {len(new_monday)}")
        print(f"   → {sorted(new_monday)} (all first-time visitors)")
        print()
        
        print(f"   New visitors on Tuesday: {len(new_tuesday)}")
        if new_tuesday:
            print(f"   → {sorted(new_tuesday)} (first-time visitors)")
        else:
            print("   → No new visitors on Tuesday")
        print()
        
        print(f"   New visitors on Wednesday: {len(new_wednesday)}")
        if new_wednesday:
            print(f"   → {sorted(new_wednesday)} (first-time visitors)")
        else:
            print("   → No new visitors on Wednesday")
        
        self.analytics_results['new_visitors'] = {
            'monday': {'count': len(new_monday), 'visitors': sorted(new_monday)},
            'tuesday': {'count': len(new_tuesday), 'visitors': sorted(new_tuesday)},
            'wednesday': {'count': len(new_wednesday), 'visitors': sorted(new_wednesday)}
        }
        print()
        return new_monday, new_tuesday, new_wednesday
    
    def loyal_visitors(self):
        """Task 4: Find users who visited on all three days"""
        print("4️⃣ LOYAL VISITORS (ALL THREE DAYS)")
        print("-" * 40)
        
        loyal = self.monday_visitors & self.tuesday_visitors & self.wednesday_visitors
        
        print(f"   Loyal visitors (all 3 days): {len(loyal)}")
        if loyal:
            print(f"   Visitor list: {sorted(loyal)}")
            print(f"   These users are highly engaged with the website")
        else:
            print("   No visitors came all three days")
        
        self.analytics_results['loyal_visitors'] = {
            'count': len(loyal),
            'visitors': sorted(loyal)
        }
        print()
        return loyal
    
    def daily_visitor_overlap_analysis(self):
        """Task 5: Analyze overlaps between each pair of days"""
        print("5️⃣ DAILY VISITOR OVERLAP ANALYSIS")
        print("-" * 40)
        
        monday_tuesday_overlap = self.monday_visitors & self.tuesday_visitors
        monday_tuesday_unique = (self.monday_visitors | self.tuesday_visitors) - (self.monday_visitors & self.tuesday_visitors)
        
        tuesday_wednesday_overlap = self.tuesday_visitors & self.wednesday_visitors
        tuesday_wednesday_unique = (self.tuesday_visitors | self.wednesday_visitors) - (self.tuesday_visitors & self.wednesday_visitors)
        
        monday_wednesday_overlap = self.monday_visitors & self.wednesday_visitors
        monday_wednesday_unique = (self.monday_visitors | self.wednesday_visitors) - (self.monday_visitors & self.wednesday_visitors)
        
        print("   📈 Monday-Tuesday Analysis:")
        print(f"      Overlap: {len(monday_tuesday_overlap)} visitors")
        if monday_tuesday_overlap:
            print(f"      → {sorted(monday_tuesday_overlap)}")
        print(f"      Unique to either day: {len(monday_tuesday_unique)} visitors")
        if monday_tuesday_unique:
            print(f"      → {sorted(monday_tuesday_unique)}")
        print()
        
        print("   📈 Tuesday-Wednesday Analysis:")
        print(f"      Overlap: {len(tuesday_wednesday_overlap)} visitors")
        if tuesday_wednesday_overlap:
            print(f"      → {sorted(tuesday_wednesday_overlap)}")
        print(f"      Unique to either day: {len(tuesday_wednesday_unique)} visitors")
        if tuesday_wednesday_unique:
            print(f"      → {sorted(tuesday_wednesday_unique)}")
        print()
        
        print("   📈 Monday-Wednesday Analysis:")
        print(f"      Overlap: {len(monday_wednesday_overlap)} visitors")
        if monday_wednesday_overlap:
            print(f"      → {sorted(monday_wednesday_overlap)}")
        print(f"      Unique to either day: {len(monday_wednesday_unique)} visitors")
        if monday_wednesday_unique:
            print(f"      → {sorted(monday_wednesday_unique)}")
        
        self.analytics_results['overlap_analysis'] = {
            'monday_tuesday': {
                'overlap': {'count': len(monday_tuesday_overlap), 'visitors': sorted(monday_tuesday_overlap)},
                'unique': {'count': len(monday_tuesday_unique), 'visitors': sorted(monday_tuesday_unique)}
            },
            'tuesday_wednesday': {
                'overlap': {'count': len(tuesday_wednesday_overlap), 'visitors': sorted(tuesday_wednesday_overlap)},
                'unique': {'count': len(tuesday_wednesday_unique), 'visitors': sorted(tuesday_wednesday_unique)}
            },
            'monday_wednesday': {
                'overlap': {'count': len(monday_wednesday_overlap), 'visitors': sorted(monday_wednesday_overlap)},
                'unique': {'count': len(monday_wednesday_unique), 'visitors': sorted(monday_wednesday_unique)}
            }
        }
        print()
        return {
            'monday_tuesday': monday_tuesday_overlap,
            'tuesday_wednesday': tuesday_wednesday_overlap,
            'monday_wednesday': monday_wednesday_overlap
        }
    
    def visitor_journey_analysis(self):
        """Advanced: Analyze individual visitor journeys"""
        print("🔍 ADVANCED: VISITOR JOURNEY ANALYSIS")
        print("-" * 40)
        
        all_visitors = self.monday_visitors | self.tuesday_visitors | self.wednesday_visitors
        
        journey_patterns = {
            'monday_only': self.monday_visitors - self.tuesday_visitors - self.wednesday_visitors,
            'tuesday_only': self.tuesday_visitors - self.monday_visitors - self.wednesday_visitors,
            'wednesday_only': self.wednesday_visitors - self.monday_visitors - self.tuesday_visitors,
            'monday_tuesday_only': (self.monday_visitors & self.tuesday_visitors) - self.wednesday_visitors,
            'tuesday_wednesday_only': (self.tuesday_visitors & self.wednesday_visitors) - self.monday_visitors,
            'monday_wednesday_only': (self.monday_visitors & self.wednesday_visitors) - self.tuesday_visitors,
            'all_three_days': self.monday_visitors & self.tuesday_visitors & self.wednesday_visitors
        }
        
        print("   👤 Visitor Journey Patterns:")
        for pattern, visitors in journey_patterns.items():
            if visitors:
                pattern_name = pattern.replace('_', ' ').title()
                print(f"      {pattern_name}: {len(visitors)} visitors → {sorted(visitors)}")
        
        monday_retention_tuesday = len(self.monday_visitors & self.tuesday_visitors) / len(self.monday_visitors) * 100
        tuesday_retention_wednesday = len(self.tuesday_visitors & self.wednesday_visitors) / len(self.tuesday_visitors) * 100
        
        print()
        print("   📊 Retention Rates:")
        print(f"      Monday → Tuesday: {monday_retention_tuesday:.1f}%")
        print(f"      Tuesday → Wednesday: {tuesday_retention_wednesday:.1f}%")
        print()
        
        return journey_patterns
    
    def engagement_metrics(self):
        """Calculate engagement metrics"""
        print("📈 ENGAGEMENT METRICS")
        print("-" * 40)
        
        total_visits = len(self.monday_visitors) + len(self.tuesday_visitors) + len(self.wednesday_visitors)
        unique_visitors = len(self.monday_visitors | self.tuesday_visitors | self.wednesday_visitors)
        
        visit_frequency = total_visits / unique_visitors
        
        monday_to_tuesday_growth = ((len(self.tuesday_visitors) - len(self.monday_visitors)) / len(self.monday_visitors)) * 100
        tuesday_to_wednesday_growth = ((len(self.wednesday_visitors) - len(self.tuesday_visitors)) / len(self.tuesday_visitors)) * 100
        
        print(f"   Total visits across 3 days: {total_visits}")
        print(f"   Unique visitors: {unique_visitors}")
        print(f"   Average visits per visitor: {visit_frequency:.2f}")
        print()
        print(f"   Daily visitor growth:")
        print(f"      Monday → Tuesday: {monday_to_tuesday_growth:+.1f}%")
        print(f"      Tuesday → Wednesday: {tuesday_to_wednesday_growth:+.1f}%")
        print()
        
        daily_counts = {
            'Monday': len(self.monday_visitors),
            'Tuesday': len(self.tuesday_visitors),
            'Wednesday': len(self.wednesday_visitors)
        }
        
        most_popular_day = max(daily_counts, key=daily_counts.get)
        least_popular_day = min(daily_counts, key=daily_counts.get)
        
        print(f"   Most popular day: {most_popular_day} ({daily_counts[most_popular_day]} visitors)")
        print(f"   Least popular day: {least_popular_day} ({daily_counts[least_popular_day]} visitors)")
        print()
    
    def comprehensive_summary(self):
        """Display comprehensive analytics summary"""
        print("📋 COMPREHENSIVE ANALYTICS SUMMARY")
        print("=" * 60)
        print()
        
        total_unique = self.analytics_results.get('total_unique', {}).get('count', 0)
        loyal_count = self.analytics_results.get('loyal_visitors', {}).get('count', 0)
        new_tuesday = self.analytics_results.get('new_visitors', {}).get('tuesday', {}).get('count', 0)
        new_wednesday = self.analytics_results.get('new_visitors', {}).get('wednesday', {}).get('count', 0)
        
        print("🎯 Key Insights:")
        print(f"   • Total unique visitors: {total_unique}")
        print(f"   • Loyal visitors (all 3 days): {loyal_count}")
        print(f"   • New visitor acquisition: {new_tuesday + new_wednesday} (Tue: {new_tuesday}, Wed: {new_wednesday})")
        
        if loyal_count > 0:
            loyalty_rate = (loyal_count / total_unique) * 100
            print(f"   • Visitor loyalty rate: {loyalty_rate:.1f}%")
        
        print()
        print("💡 Recommendations:")
        if loyal_count == 0:
            print("   • Focus on retention strategies - no visitors came all 3 days")
        if new_tuesday == 0:
            print("   • Improve Tuesday marketing - no new visitors acquired")
        if new_wednesday == 0:
            print("   • Enhance Wednesday content - no new visitors acquired")
        
        overlaps = self.analytics_results.get('overlap_analysis', {})
        if overlaps:
            best_overlap = max(
                overlaps.items(),
                key=lambda x: x[1]['overlap']['count']
            )
            print(f"   • Strongest day-pair retention: {best_overlap[0].replace('_', '-').title()}")
    
    def run_complete_analysis(self):
        """Run the complete website analytics analysis"""
        self.display_raw_data()
        
        self.unique_visitors_all_days()
        self.returning_visitors_tuesday()
        self.new_visitors_each_day()
        self.loyal_visitors()
        self.daily_visitor_overlap_analysis()
        
        self.visitor_journey_analysis()
        self.engagement_metrics()
        
        self.comprehensive_summary()

def demonstrate_set_operations():
    """Demonstrate various set operations with the visitor data"""
    print("\n🔧 SET OPERATIONS DEMONSTRATION 🔧")
    print("=" * 60)
    print()
    
    monday = {"user1", "user2", "user3", "user4", "user5"}
    tuesday = {"user2", "user4", "user6", "user7", "user8"}
    wednesday = {"user1", "user3", "user6", "user9", "user10"}
    
    print("📚 Set Operations Used in Website Analytics:")
    print()
    
    union_result = monday | tuesday | wednesday
    print(f"1. Union (|) - All unique visitors:")
    print(f"   monday | tuesday | wednesday = {sorted(union_result)}")
    print()
    
    intersection_result = monday & tuesday
    print(f"2. Intersection (&) - Common visitors:")
    print(f"   monday & tuesday = {sorted(intersection_result)}")
    print()
    
    difference_result = tuesday - monday
    print(f"3. Difference (-) - New Tuesday visitors:")
    print(f"   tuesday - monday = {sorted(difference_result)}")
    print()
    
    sym_diff_result = monday ^ tuesday
    print(f"4. Symmetric Difference (^) - Visitors on exactly one day:")
    print(f"   monday ^ tuesday = {sorted(sym_diff_result)}")
    print()
    
    monday_only = monday - tuesday - wednesday
    print(f"5. Complex Operations - Monday-only visitors:")
    print(f"   monday - tuesday - wednesday = {sorted(monday_only)}")
    print()

def compare_with_alternative_approaches():
    """Compare set-based approach with other data structures"""
    print("⚖️ PERFORMANCE COMPARISON")
    print("=" * 60)
    print()
    
    import time
    
    monday_large = {f"user{i}" for i in range(10000)}
    tuesday_large = {f"user{i}" for i in range(5000, 15000)}
    
    print("Comparing performance with 10,000+ visitors:")
    
    start_time = time.time()
    intersection_set = monday_large & tuesday_large
    set_time = time.time() - start_time
    
    monday_list = list(monday_large)
    tuesday_list = list(tuesday_large)
    start_time = time.time()
    intersection_list = [user for user in monday_list if user in tuesday_list]
    list_time = time.time() - start_time
    
    print(f"   Set intersection: {set_time:.6f} seconds")
    print(f"   List comprehension: {list_time:.6f} seconds")
    print(f"   Sets are {list_time/set_time:.1f}x faster!")
    print()

def main():
    """Main function to run website analytics"""
    print("🌐 WEBSITE ANALYTICS SYSTEM 🌐")
    print("=" * 70)
    print()
    
    analytics = WebsiteAnalytics()
    analytics.run_complete_analysis()
    
    demonstrate_set_operations()
    compare_with_alternative_approaches()
    
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 70)
    print()
    print("✅ All 5 required tasks completed:")
    print("   1. ✅ Unique visitors across all days")
    print("   2. ✅ Returning visitors on Tuesday")
    print("   3. ✅ New visitors each day")
    print("   4. ✅ Loyal visitors (all three days)")
    print("   5. ✅ Daily visitor overlap analysis")
    print()
    print("🚀 Bonus features added:")
    print("   • Visitor journey pattern analysis")
    print("   • Engagement metrics & retention rates")
    print("   • Growth analysis & recommendations")
    print("   • Set operations demonstration")
    print("   • Performance comparison")
    print()

if __name__ == "__main__":
    main()
