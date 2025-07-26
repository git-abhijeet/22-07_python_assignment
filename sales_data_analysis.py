class SalesDataAnalysis:
    """Comprehensive sales data analysis using tuple unpacking and nested structures"""
    
    def __init__(self):
        self.sales_data = [
            ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
            ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
            ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
        ]
        
        self.analysis_results = {}
    
    def display_raw_data(self):
        """Display the raw sales data structure"""
        print("📊 SALES DATA ANALYSIS - RAW DATA 📊")
        print("=" * 60)
        print()
        print("Sales Data Structure:")
        for quarter, monthly_data in self.sales_data:
            print(f"   {quarter}: {monthly_data}")
        print()
    
    def calculate_total_sales_per_quarter(self):
        """Task 1: Calculate total sales per quarter using unpacking"""
        print("1️⃣ TOTAL SALES PER QUARTER")
        print("-" * 40)
        
        quarterly_totals = []
        
        for quarter, monthly_sales in self.sales_data:
            quarter_total = sum(sales for month, sales in monthly_sales)
            quarterly_totals.append((quarter, quarter_total))
            
            print(f"   {quarter} Total Sales: ${quarter_total:,}")
            
            print(f"      Breakdown:")
            for month, sales in monthly_sales:
                print(f"         {month}: ${sales:,}")
            print()
        
        self.analysis_results['quarterly_totals'] = quarterly_totals
        
        overall_total = sum(total for quarter, total in quarterly_totals)
        print(f"   🎯 Overall Total Sales: ${overall_total:,}")
        print()
        
        return quarterly_totals
    
    def find_highest_sales_month(self):
        """Task 2: Find the month with highest sales across all quarters"""
        print("2️⃣ MONTH WITH HIGHEST SALES")
        print("-" * 40)
        
        all_monthly_sales = []
        
        for quarter, monthly_data in self.sales_data:
            for month, sales in monthly_data:
                all_monthly_sales.append((month, sales, quarter))
        
        highest_month, highest_sales, highest_quarter = max(
            all_monthly_sales, 
            key=lambda x: x[1]  # Sort by sales (second element)
        )
        
        print(f"   🏆 Highest Sales Month: {highest_month}")
        print(f"   💰 Sales Amount: ${highest_sales:,}")
        print(f"   📅 Quarter: {highest_quarter}")
        print()
        
        print("   📈 Top 3 Performing Months:")
        sorted_sales = sorted(all_monthly_sales, key=lambda x: x[1], reverse=True)
        for i, (month, sales, quarter) in enumerate(sorted_sales[:3], 1):
            print(f"      {i}. {month} ({quarter}): ${sales:,}")
        
        self.analysis_results['highest_month'] = {
            'month': highest_month,
            'sales': highest_sales,
            'quarter': highest_quarter
        }
        print()
        
        return highest_month, highest_sales, highest_quarter
    
    def create_flat_monthly_list(self):
        """Task 3: Create a flat list of all monthly sales"""
        print("3️⃣ FLAT LIST OF MONTHLY SALES")
        print("-" * 40)
        
        flat_list_method1 = [
            (month, sales) 
            for quarter, monthly_data in self.sales_data 
            for month, sales in monthly_data
        ]
        
        flat_list_method2 = []
        for quarter, monthly_data in self.sales_data:
            for month, sales in monthly_data:
                flat_list_method2.append((month, sales))
        
        flat_list_method3 = []
        for quarter, monthly_data in self.sales_data:
            flat_list_method3.extend(monthly_data)
        
        print("   📋 Flat Monthly Sales List:")
        for month, sales in flat_list_method1:
            print(f"      (\"{month}\", {sales})")
        
        assert flat_list_method1 == flat_list_method2 == flat_list_method3
        print(f"\n   ✅ All {len(flat_list_method1)} monthly records extracted successfully")
        
        self.analysis_results['flat_monthly_list'] = flat_list_method1
        print()
        
        return flat_list_method1
    
    def demonstrate_unpacking_in_loops(self):
        """Task 4: Demonstrate various unpacking techniques in loops"""
        print("4️⃣ UNPACKING IN LOOPS DEMONSTRATION")
        print("-" * 40)
        
        print("   🔄 Method 1: Basic tuple unpacking")
        for quarter, monthly_data in self.sales_data:
            print(f"      Processing {quarter}:")
            for month, sales in monthly_data:
                print(f"         {month}: ${sales:,}")
        print()
        
        print("   🔄 Method 2: Unpacking with enumeration")
        for quarter_index, (quarter, monthly_data) in enumerate(self.sales_data, 1):
            print(f"      Quarter {quarter_index} ({quarter}):")
            for month_index, (month, sales) in enumerate(monthly_data, 1):
                print(f"         Month {month_index} - {month}: ${sales:,}")
        print()
        
        print("   🔄 Method 3: Unpacking with multiple assignments")
        for quarter_data in self.sales_data:
            quarter_name, monthly_sales = quarter_data  # Explicit unpacking
            total_sales = sum(amount for _, amount in monthly_sales)
            avg_sales = total_sales / len(monthly_sales)
            
            print(f"      {quarter_name} Analysis:")
            print(f"         Total: ${total_sales:,}")
            print(f"         Average: ${avg_sales:,.2f}")
            print(f"         Months: {len(monthly_sales)}")
        print()
        
        print("   🔄 Method 4: Nested unpacking in single loop")
        print("      All sales with quarter context:")
        for quarter, monthly_data in self.sales_data:
            for month, sales in monthly_data:
                quarter_short = quarter  # Keep quarter context
                print(f"         {quarter_short}-{month}: ${sales:,}")
        print()
    
    def advanced_unpacking_techniques(self):
        """Demonstrate advanced unpacking techniques"""
        print("🚀 ADVANCED UNPACKING TECHNIQUES")
        print("-" * 40)
        
        print("   ⭐ Technique 1: Unpacking with *args")
        sample_quarter = ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)])
        quarter_name, *monthly_data_list = sample_quarter
        monthly_data = monthly_data_list[0]  # Get the actual list
        print(f"      Quarter: {quarter_name}")
        print(f"      Monthly data: {monthly_data}")
        print()
        
        print("   ⭐ Technique 2: Unpacking in function calls")
        def analyze_month(month, sales, quarter):
            return f"{quarter}-{month}: ${sales:,}"
        
        for quarter, monthly_data in self.sales_data:
            for month_sales in monthly_data:
                month, sales = month_sales
                result = analyze_month(month, sales, quarter)
                print(f"      {result}")
        print()
        
        print("   ⭐ Technique 3: Multiple assignment with unpacking")
        first_quarter, *middle_quarters, last_quarter = self.sales_data
        
        first_q_name, first_q_data = first_quarter
        last_q_name, last_q_data = last_quarter
        
        print(f"      First Quarter: {first_q_name}")
        print(f"      Last Quarter: {last_q_name}")
        print(f"      Middle Quarters: {len(middle_quarters)}")
        print()
        
        print("   ⭐ Technique 4: Unpacking with dict creation")
        quarterly_dict = {quarter: dict(monthly_data) for quarter, monthly_data in self.sales_data}
        monthly_dict = {month: sales for quarter, monthly_data in self.sales_data for month, sales in monthly_data}
        
        print(f"      Quarterly structure: {quarterly_dict}")
        print(f"      All months: {monthly_dict}")
        print()
    
    def sales_performance_analysis(self):
        """Advanced sales performance analysis using unpacking"""
        print("📈 SALES PERFORMANCE ANALYSIS")
        print("-" * 40)
        
        quarterly_performance = []
        
        for quarter, monthly_data in self.sales_data:
            monthly_sales = [sales for month, sales in monthly_data]
            
            total_sales = sum(monthly_sales)
            avg_sales = total_sales / len(monthly_sales)
            min_sales = min(monthly_sales)
            max_sales = max(monthly_sales)
            
            min_month = next(month for month, sales in monthly_data if sales == min_sales)
            max_month = next(month for month, sales in monthly_data if sales == max_sales)
            
            quarterly_performance.append({
                'quarter': quarter,
                'total': total_sales,
                'average': avg_sales,
                'min_sales': min_sales,
                'max_sales': max_sales,
                'min_month': min_month,
                'max_month': max_month,
                'volatility': max_sales - min_sales
            })
        
        for perf in quarterly_performance:
            quarter, total, avg = perf['quarter'], perf['total'], perf['average']
            min_sales, max_sales = perf['min_sales'], perf['max_sales']
            min_month, max_month = perf['min_month'], perf['max_month']
            volatility = perf['volatility']
            
            print(f"   📊 {quarter} Performance:")
            print(f"      Total Sales: ${total:,}")
            print(f"      Average Sales: ${avg:,.2f}")
            print(f"      Best Month: {max_month} (${max_sales:,})")
            print(f"      Worst Month: {min_month} (${min_sales:,})")
            print(f"      Volatility: ${volatility:,}")
            print()
        
        return quarterly_performance
    
    def growth_trend_analysis(self):
        """Analyze growth trends using unpacking"""
        print("📈 GROWTH TREND ANALYSIS")
        print("-" * 40)
        
        all_sales_with_context = []
        for quarter, monthly_data in self.sales_data:
            for month, sales in monthly_data:
                all_sales_with_context.append((quarter, month, sales))
        
        print("   📊 Month-over-Month Growth:")
        for i in range(1, len(all_sales_with_context)):
            prev_quarter, prev_month, prev_sales = all_sales_with_context[i-1]
            curr_quarter, curr_month, curr_sales = all_sales_with_context[i]
            
            growth = ((curr_sales - prev_sales) / prev_sales) * 100
            growth_direction = "📈" if growth > 0 else "📉" if growth < 0 else "➡️"
            
            print(f"      {prev_month} → {curr_month}: {growth:+.1f}% {growth_direction}")
        
        print("\n   📊 Quarterly Growth:")
        quarterly_totals = self.analysis_results.get('quarterly_totals', [])
        
        for i in range(1, len(quarterly_totals)):
            prev_quarter, prev_total = quarterly_totals[i-1]
            curr_quarter, curr_total = quarterly_totals[i]
            
            growth = ((curr_total - prev_total) / prev_total) * 100
            growth_direction = "📈" if growth > 0 else "📉" if growth < 0 else "➡️"
            
            print(f"      {prev_quarter} → {curr_quarter}: {growth:+.1f}% {growth_direction}")
        print()
    
    def comprehensive_summary(self):
        """Display comprehensive analysis summary"""
        print("📋 COMPREHENSIVE SALES SUMMARY")
        print("=" * 60)
        print()
        
        quarterly_totals = self.analysis_results.get('quarterly_totals', [])
        highest_month_data = self.analysis_results.get('highest_month', {})
        
        if quarterly_totals:
            best_quarter, best_quarter_sales = max(quarterly_totals, key=lambda x: x[1])
            worst_quarter, worst_quarter_sales = min(quarterly_totals, key=lambda x: x[1])
            
            total_sales = sum(sales for quarter, sales in quarterly_totals)
            avg_quarterly_sales = total_sales / len(quarterly_totals)
        
        print("🎯 Key Performance Indicators:")
        print(f"   • Total Sales (All Quarters): ${total_sales:,}")
        print(f"   • Average Quarterly Sales: ${avg_quarterly_sales:,.2f}")
        print(f"   • Best Performing Quarter: {best_quarter} (${best_quarter_sales:,})")
        print(f"   • Lowest Performing Quarter: {worst_quarter} (${worst_quarter_sales:,})")
        
        if highest_month_data:
            print(f"   • Best Month Overall: {highest_month_data['month']} (${highest_month_data['sales']:,})")
        
        print()
        print("💡 Business Insights:")
        
        if len(quarterly_totals) >= 2:
            q1_sales = quarterly_totals[0][1]
            q3_sales = quarterly_totals[-1][1]
            overall_growth = ((q3_sales - q1_sales) / q1_sales) * 100
            
            if overall_growth > 0:
                print(f"   • Positive growth trend: {overall_growth:+.1f}% from Q1 to Q3")
            else:
                print(f"   • Declining trend: {overall_growth:.1f}% from Q1 to Q3")
        
        flat_list = self.analysis_results.get('flat_monthly_list', [])
        if flat_list:
            summer_months = ['Jun', 'Jul', 'Aug']
            summer_sales = sum(sales for month, sales in flat_list if month in summer_months)
            avg_summer = summer_sales / 3
            
            other_sales = sum(sales for month, sales in flat_list if month not in summer_months)
            avg_other = other_sales / (len(flat_list) - 3)
            
            if avg_summer > avg_other:
                print(f"   • Summer peak: {((avg_summer - avg_other) / avg_other * 100):+.1f}% above average")
            else:
                print(f"   • Summer dip: {((avg_summer - avg_other) / avg_other * 100):.1f}% below average")
    
    def run_complete_analysis(self):
        """Run the complete sales data analysis"""
        self.display_raw_data()
        
        self.calculate_total_sales_per_quarter()
        self.find_highest_sales_month()
        self.create_flat_monthly_list()
        self.demonstrate_unpacking_in_loops()
        
        self.advanced_unpacking_techniques()
        self.sales_performance_analysis()
        self.growth_trend_analysis()
        
        self.comprehensive_summary()

def demonstrate_tuple_unpacking_concepts():
    """Educational demonstration of tuple unpacking concepts"""
    print("\n🎓 TUPLE UNPACKING CONCEPTS 🎓")
    print("=" * 60)
    print()
    
    print("📚 Basic Unpacking Examples:")
    
    person = ("John", 25, "Engineer")
    name, age, job = person
    print(f"   Basic unpacking: {name}, {age}, {job}")
    
    nested_data = (("Q1", 1000), ("Q2", 1200))
    (q1_name, q1_sales), (q2_name, q2_sales) = nested_data
    print(f"   Nested unpacking: {q1_name}=${q1_sales}, {q2_name}=${q2_sales}")
    
    numbers = (1, 2, 3, 4, 5)
    first, *middle, last = numbers
    print(f"   Star unpacking: first={first}, middle={middle}, last={last}")
    
    def calculate_total(month, sales):
        return f"{month}: ${sales}"
    
    month_data = ("January", 1500)
    result = calculate_total(*month_data)
    print(f"   Function unpacking: {result}")
    print()

def main():
    """Main function to run sales data analysis"""
    print("💼 SALES DATA ANALYSIS SYSTEM 💼")
    print("=" * 70)
    print()
    
    analysis = SalesDataAnalysis()
    analysis.run_complete_analysis()
    
    demonstrate_tuple_unpacking_concepts()
    
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 70)
    print()
    print("✅ All 4 required tasks completed:")
    print("   1. ✅ Total sales per quarter calculated")
    print("   2. ✅ Highest sales month identified")
    print("   3. ✅ Flat monthly sales list created")
    print("   4. ✅ Unpacking in loops demonstrated")
    print()
    print("🚀 Advanced features added:")
    print("   • Performance analysis by quarter")
    print("   • Growth trend analysis")
    print("   • Advanced unpacking techniques")
    print("   • Business insights and KPIs")
    print("   • Educational tuple unpacking guide")
    print()

if __name__ == "__main__":
    main()
