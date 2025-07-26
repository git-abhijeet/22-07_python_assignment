from collections import deque
import time
from datetime import datetime

class BrowserHistory:
    """Efficient browser history system using collections.deque"""
    
    def __init__(self, max_history_size=5):
        """Initialize browser history with maximum size limit"""
        self.history = deque(maxlen=max_history_size)  # Main history deque
        self.forward_stack = deque()  # Forward navigation stack
        self.max_size = max_history_size
        self.operation_log = []  # Track all operations for debugging
        
        self.add_page("https://home.page", is_initial=True)
    
    def add_page(self, url, is_initial=False):
        """Add new page URL to the end of history"""
        print(f"🌐 Navigating to: {url}")
        
        self.history.append(url)
        
        if not is_initial and self.forward_stack:
            print(f"   📱 Cleared forward stack ({len(self.forward_stack)} pages)")
            self.forward_stack.clear()
        
        if not is_initial:
            self.operation_log.append({
                'action': 'add_page',
                'url': url,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'history_size': len(self.history),
                'forward_size': len(self.forward_stack)
            })
        
        print(f"   ✅ Page added to history")
        if len(self.history) == self.max_size:
            print(f"   ⚠️  History at maximum capacity ({self.max_size} pages)")
        
        self.display_current_state()
        print()
    
    def go_back(self):
        """Remove last visited page and store in forward stack"""
        if len(self.history) <= 1:
            print("🚫 Cannot go back - already at the oldest page")
            return False
        
        current_page = self.history.pop()
        self.forward_stack.append(current_page)
        
        print(f"⬅️  Going back from: {current_page}")
        print(f"   📄 Now viewing: {self.get_current_page()}")
        print(f"   📚 Added to forward stack")
        
        self.operation_log.append({
            'action': 'go_back',
            'from_url': current_page,
            'to_url': self.get_current_page(),
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'history_size': len(self.history),
            'forward_size': len(self.forward_stack)
        })
        
        self.display_current_state()
        print()
        return True
    
    def go_forward(self):
        """Restore most recently backed-out page from forward stack"""
        if not self.forward_stack:
            print("🚫 Cannot go forward - no pages in forward stack")
            return False
        
        forward_page = self.forward_stack.pop()
        self.history.append(forward_page)
        
        print(f"➡️  Going forward to: {forward_page}")
        print(f"   📄 Restored from forward stack")
        
        self.operation_log.append({
            'action': 'go_forward',
            'to_url': forward_page,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'history_size': len(self.history),
            'forward_size': len(self.forward_stack)
        })
        
        self.display_current_state()
        print()
        return True
    
    def get_current_page(self):
        """Get the currently viewed page"""
        return self.history[-1] if self.history else None
    
    def display_current_state(self):
        """Display current history and forward stack state"""
        print(f"   📚 History ({len(self.history)}/{self.max_size}):")
        for i, page in enumerate(self.history):
            current_marker = " 👈 CURRENT" if i == len(self.history) - 1 else ""
            print(f"      {i+1}. {page}{current_marker}")
        
        print(f"   📂 Forward Stack ({len(self.forward_stack)}):")
        if self.forward_stack:
            for i, page in enumerate(reversed(self.forward_stack)):
                print(f"      {i+1}. {page}")
        else:
            print("      (empty)")
    
    def get_full_history_path(self):
        """Get complete navigation path including forward stack"""
        return {
            'current_page': self.get_current_page(),
            'history': list(self.history),
            'forward_stack': list(self.forward_stack),
            'can_go_back': len(self.history) > 1,
            'can_go_forward': len(self.forward_stack) > 0
        }
    
    def display_navigation_options(self):
        """Display available navigation options"""
        state = self.get_full_history_path()
        
        print("🧭 Navigation Options:")
        print(f"   ⬅️  Go Back: {'✅ Available' if state['can_go_back'] else '❌ Disabled'}")
        print(f"   ➡️  Go Forward: {'✅ Available' if state['can_go_forward'] else '❌ Disabled'}")
        print(f"   🌐 Add New Page: ✅ Always Available")
        print()
    
    def get_operation_history(self):
        """Get detailed operation history"""
        print("📋 Operation History:")
        if not self.operation_log:
            print("   No operations performed yet")
            return
        
        for i, op in enumerate(self.operation_log, 1):
            print(f"   {i}. [{op['timestamp']}] {op['action'].upper()}")
            if op['action'] == 'add_page':
                print(f"      → Added: {op['url']}")
            elif op['action'] == 'go_back':
                print(f"      → From: {op['from_url']}")
                print(f"      → To: {op['to_url']}")
            elif op['action'] == 'go_forward':
                print(f"      → To: {op['to_url']}")
            print(f"      → State: History({op['history_size']}) Forward({op['forward_size']})")
        print()

def demonstrate_browser_history():
    """Demonstrate browser history functionality"""
    print("🌐 BROWSER HISTORY SYSTEM DEMONSTRATION 🌐")
    print("=" * 60)
    print()
    
    browser = BrowserHistory(max_history_size=5)
    
    print("1️⃣ ADDING PAGES TO HISTORY")
    print("-" * 30)
    
    pages_to_visit = [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://python.org",
        "https://docs.python.org"
    ]
    
    for page in pages_to_visit:
        browser.add_page(page)
    
    print("2️⃣ TESTING MAXIMUM CAPACITY")
    print("-" * 30)
    
    browser.add_page("https://pypi.org")
    print("   🔍 Note: Oldest page should be automatically removed")
    print()
    
    print("3️⃣ NAVIGATION - GOING BACK")
    print("-" * 30)
    
    for i in range(3):
        print(f"Going back #{i+1}:")
        browser.go_back()
    
    print("4️⃣ NAVIGATION - GOING FORWARD")
    print("-" * 30)
    
    for i in range(2):
        print(f"Going forward #{i+1}:")
        browser.go_forward()
    
    print("5️⃣ ADDING NEW PAGE AFTER NAVIGATION")
    print("-" * 30)
    
    browser.add_page("https://wikipedia.org")
    
    print("6️⃣ TESTING EDGE CASES")
    print("-" * 30)
    
    print("Testing excessive back navigation:")
    for i in range(10):
        if not browser.go_back():
            break
    
    print("Testing forward navigation when stack is empty:")
    browser.go_forward()
    
    return browser

def demonstrate_deque_efficiency():
    """Demonstrate efficiency of deque operations"""
    print("⚡ DEQUE EFFICIENCY DEMONSTRATION ⚡")
    print("=" * 60)
    print()
    
    import time
    
    print("🔬 Performance Testing with Large Dataset:")
    
    large_history = deque(maxlen=10000)
    
    start_time = time.time()
    for i in range(10000):
        large_history.append(f"https://page{i}.com")
    append_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(1000):
        if large_history:
            large_history.pop()
    pop_time = time.time() - start_time
    
    for i in range(1000):  # Refill for test
        large_history.append(f"https://newpage{i}.com")
    
    start_time = time.time()
    for i in range(1000):
        if large_history:
            large_history.popleft()
    popleft_time = time.time() - start_time
    
    print(f"   📊 Performance Results:")
    print(f"      Append 10,000 items: {append_time:.6f} seconds")
    print(f"      Pop 1,000 items: {pop_time:.6f} seconds")
    print(f"      Popleft 1,000 items: {popleft_time:.6f} seconds")
    print()
    
    print("🔬 Comparing deque vs list for front operations:")
    
    test_deque = deque(maxlen=1000)
    start_time = time.time()
    for i in range(1000):
        test_deque.appendleft(f"page{i}")
    deque_appendleft_time = time.time() - start_time
    
    test_list = []
    start_time = time.time()
    for i in range(1000):
        test_list.insert(0, f"page{i}")
    list_insert_time = time.time() - start_time
    
    print(f"   📊 Front Operations Comparison:")
    print(f"      Deque appendleft (1,000): {deque_appendleft_time:.6f} seconds")
    print(f"      List insert(0) (1,000): {list_insert_time:.6f} seconds")
    print(f"      Deque is {list_insert_time/deque_appendleft_time:.1f}x faster!")
    print()

def interactive_browser_simulation():
    """Interactive browser history simulation"""
    print("🎮 INTERACTIVE BROWSER SIMULATION 🎮")
    print("=" * 60)
    print()
    
    browser = BrowserHistory(max_history_size=5)
    
    print("Commands:")
    print("   1 - Add new page")
    print("   2 - Go back")
    print("   3 - Go forward")
    print("   4 - Show state")
    print("   5 - Show operation history")
    print("   6 - Exit")
    print()
    
    demo_commands = [
        ("1", "https://example.com"),
        ("1", "https://test.com"),
        ("2", None),  # Go back
        ("3", None),  # Go forward
        ("1", "https://new.com"),
        ("4", None),  # Show state
        ("5", None),  # Show history
    ]
    
    print("🤖 Running automated demo commands:")
    for command, url in demo_commands:
        if command == "1":
            print(f"   Command: Add page '{url}'")
            browser.add_page(url)
        elif command == "2":
            print("   Command: Go back")
            browser.go_back()
        elif command == "3":
            print("   Command: Go forward")
            browser.go_forward()
        elif command == "4":
            print("   Command: Show current state")
            browser.display_current_state()
            browser.display_navigation_options()
        elif command == "5":
            print("   Command: Show operation history")
            browser.get_operation_history()
        
        time.sleep(0.5)  # Brief pause for readability

def advanced_deque_features():
    """Demonstrate advanced deque features"""
    print("🚀 ADVANCED DEQUE FEATURES 🚀")
    print("=" * 60)
    print()
    
    print("📚 Advanced Operations:")
    
    sample_deque = deque(['a', 'b', 'c', 'd', 'e'], maxlen=5)
    print(f"   Initial deque: {list(sample_deque)}")
    
    print("\n   🔄 Rotation operations:")
    sample_deque.rotate(2)
    print(f"      After rotate(2): {list(sample_deque)}")
    
    sample_deque.rotate(-1)
    print(f"      After rotate(-1): {list(sample_deque)}")
    
    print("\n   📈 Extend operations:")
    sample_deque.extend(['f', 'g'])
    print(f"      After extend(['f', 'g']): {list(sample_deque)}")
    
    sample_deque.extendleft(['x', 'y'])
    print(f"      After extendleft(['x', 'y']): {list(sample_deque)}")
    
    print("\n   🔍 Search operations:")
    sample_deque.extend(['c', 'c'])  # Add duplicates
    print(f"      Deque with duplicates: {list(sample_deque)}")
    print(f"      Count of 'c': {sample_deque.count('c')}")
    if 'c' in sample_deque:
        print(f"      Index of first 'c': {sample_deque.index('c')}")
    
    print("\n   🗑️  Utility operations:")
    deque_copy = sample_deque.copy()
    print(f"      Copy created: {list(deque_copy)}")
    
    sample_deque.clear()
    print(f"      After clear(): {list(sample_deque)}")
    print(f"      Original copy still intact: {list(deque_copy)}")

def browser_history_use_cases():
    """Demonstrate real-world browser history use cases"""
    print("🌍 REAL-WORLD USE CASES 🌍")
    print("=" * 60)
    print()
    
    print("📱 Use Case 1: Mobile Browser with Limited Memory")
    mobile_browser = BrowserHistory(max_history_size=3)  # Limited memory
    
    mobile_pages = [
        "https://m.facebook.com",
        "https://m.twitter.com",
        "https://m.instagram.com",
        "https://m.linkedin.com"  # Should remove facebook
    ]
    
    for page in mobile_pages:
        mobile_browser.add_page(page)
    
    print("\n💻 Use Case 2: Desktop Browser with Tab Groups")
    desktop_browser = BrowserHistory(max_history_size=10)
    
    work_tabs = [
        "https://gmail.com",
        "https://calendar.google.com",
        "https://drive.google.com",
        "https://slack.com"
    ]
    
    for tab in work_tabs:
        desktop_browser.add_page(tab)
    
    desktop_browser.go_back()
    desktop_browser.go_back()
    desktop_browser.go_forward()
    
    print("\n🎯 Use Case 3: Incognito Mode with Session Management")
    incognito_browser = BrowserHistory(max_history_size=5)
    
    private_pages = [
        "https://private-search.com",
        "https://secure-site.com"
    ]
    
    for page in private_pages:
        incognito_browser.add_page(page)
    
    print("   🔒 Incognito session can be easily cleared:")
    incognito_browser.history.clear()
    incognito_browser.forward_stack.clear()
    print("   ✅ All history cleared for privacy")

def main():
    """Main function to demonstrate browser history system"""
    print("🌐 BROWSER HISTORY SYSTEM WITH DEQUE 🌐")
    print("=" * 70)
    print()
    
    browser = demonstrate_browser_history()
    
    browser.get_operation_history()
    
    demonstrate_deque_efficiency()
    
    interactive_browser_simulation()
    
    advanced_deque_features()
    
    browser_history_use_cases()
    
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print()
    print("✅ Browser History System Features:")
    print("   • ✅ Add new pages with automatic size management")
    print("   • ✅ Go back with forward stack maintenance")
    print("   • ✅ Go forward from forward stack")
    print("   • ✅ Efficient deque operations (O(1) for both ends)")
    print("   • ✅ Maximum history size enforcement")
    print("   • ✅ State tracking and navigation options")
    print()
    print("🚀 Advanced Features Demonstrated:")
    print("   • Performance comparison (deque vs list)")
    print("   • Real-world browser scenarios")
    print("   • Edge case handling")
    print("   • Operation logging and history")
    print("   • Interactive simulation")
    print()
    print("💡 Key Benefits of Using Deque:")
    print("   • O(1) append/pop operations at both ends")
    print("   • Automatic size management with maxlen")
    print("   • Memory efficient for large datasets")
    print("   • Perfect for LIFO/FIFO operations")
    print()

if __name__ == "__main__":
    main()
