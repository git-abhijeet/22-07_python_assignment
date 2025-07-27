from datetime import datetime
import uuid

class Account:
    """
    Base Account class implementing core banking functionality
    Demonstrates encapsulation, class variables, and class methods
    """
    
    # Class variables
    bank_name = "First National Bank"
    _minimum_balance = 50.0
    _total_accounts = 0
    _all_accounts = []
    
    def __init__(self, account_number, account_holder, initial_balance):
        """
        Initialize a bank account with proper validation
        
        Args:
            account_number (str): Unique account identifier
            account_holder (str): Name of the account holder
            initial_balance (float): Starting balance
        
        Raises:
            ValueError: If validation fails
        """
        print("🏦 BANK ACCOUNT MANAGEMENT SYSTEM")
        print("=" * 50)
        print()
        
        # Validate input parameters
        self._validate_account_data(account_number, account_holder, initial_balance)
        
        # Private attributes for encapsulation
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = float(initial_balance)
        self._transaction_history = []
        self._created_at = datetime.now()
        self._is_active = True
        
        # Update class variables
        Account._total_accounts += 1
        Account._all_accounts.append(self)
        
        # Record initial deposit
        self._add_transaction("Initial Deposit", initial_balance, "Account Opening")
        
        print(f"✅ Account created successfully:")
        print(f"   Account Number: {self._account_number}")
        print(f"   Account Holder: {self._account_holder}")
        print(f"   Initial Balance: ${self._balance:.2f}")
        print(f"   Bank: {Account.bank_name}")
        print()
    
    def _validate_account_data(self, account_number, account_holder, initial_balance):
        """
        Private method to validate account creation data
        
        Args:
            account_number (str): Account number to validate
            account_holder (str): Name to validate
            initial_balance (float): Balance to validate
        
        Raises:
            ValueError: If any validation fails
        """
        if not account_number or not isinstance(account_number, str):
            raise ValueError("Account number must be a non-empty string")
        
        if not account_holder or not isinstance(account_holder, str) or account_holder.strip() == "":
            raise ValueError("Account holder name must be a non-empty string")
        
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number")
        
        if initial_balance < Account._minimum_balance:
            raise ValueError(f"Initial balance must be at least ${Account._minimum_balance:.2f}")
        
        # Check for duplicate account numbers
        for account in Account._all_accounts:
            if account._account_number == account_number:
                raise ValueError(f"Account number {account_number} already exists")
    
    def _add_transaction(self, transaction_type, amount, description=""):
        """
        Private method to record transaction history
        
        Args:
            transaction_type (str): Type of transaction
            amount (float): Transaction amount
            description (str): Additional details
        """
        transaction = {
            'id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now(),
            'type': transaction_type,
            'amount': amount,
            'balance_after': self._balance,
            'description': description
        }
        self._transaction_history.append(transaction)
    
    def deposit(self, amount):
        """
        Deposit money into the account
        
        Args:
            amount (float): Amount to deposit
        
        Returns:
            bool: True if successful, False otherwise
        
        Raises:
            ValueError: If amount is invalid
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Deposit amount must be a positive number")
        
        if not self._is_active:
            print(f"❌ Cannot deposit to inactive account {self._account_number}")
            return False
        
        self._balance += amount
        self._add_transaction("Deposit", amount, f"Cash deposit of ${amount:.2f}")
        
        print(f"💰 Deposit successful:")
        print(f"   Account: {self._account_number}")
        print(f"   Amount: ${amount:.2f}")
        print(f"   New Balance: ${self._balance:.2f}")
        print()
        
        return True
    
    def withdraw(self, amount):
        """
        Withdraw money from the account (base implementation)
        
        Args:
            amount (float): Amount to withdraw
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number")
        
        if not self._is_active:
            print(f"❌ Cannot withdraw from inactive account {self._account_number}")
            return False
        
        if self._balance >= amount:
            self._balance -= amount
            self._add_transaction("Withdrawal", -amount, f"Cash withdrawal of ${amount:.2f}")
            
            print(f"💸 Withdrawal successful:")
            print(f"   Account: {self._account_number}")
            print(f"   Amount: ${amount:.2f}")
            print(f"   New Balance: ${self._balance:.2f}")
            print()
            
            return True
        else:
            print(f"❌ Insufficient funds:")
            print(f"   Account: {self._account_number}")
            print(f"   Requested: ${amount:.2f}")
            print(f"   Available: ${self._balance:.2f}")
            print()
            
            return False
    
    def get_balance(self):
        """
        Get current account balance
        
        Returns:
            float: Current balance
        """
        return self._balance
    
    def get_account_info(self):
        """
        Get comprehensive account information
        
        Returns:
            dict: Account details
        """
        return {
            'account_number': self._account_number,
            'account_holder': self._account_holder,
            'balance': self._balance,
            'account_type': self.__class__.__name__,
            'created_at': self._created_at,
            'is_active': self._is_active,
            'bank_name': Account.bank_name,
            'transaction_count': len(self._transaction_history)
        }
    
    def get_transaction_history(self, limit=10):
        """
        Get recent transaction history
        
        Args:
            limit (int): Number of recent transactions to return
        
        Returns:
            list: Recent transactions
        """
        return self._transaction_history[-limit:] if self._transaction_history else []
    
    def __str__(self):
        """String representation of the account"""
        return (f"{self.__class__.__name__}(Account: {self._account_number}, "
                f"Holder: {self._account_holder}, Balance: ${self._balance:.2f})")
    
    def __repr__(self):
        """Detailed representation of the account"""
        return (f"{self.__class__.__name__}(account_number='{self._account_number}', "
                f"account_holder='{self._account_holder}', balance={self._balance})")
    
    # Class methods
    @classmethod
    def get_total_accounts(cls):
        """
        Get total number of accounts created
        
        Returns:
            int: Total account count
        """
        return cls._total_accounts
    
    @classmethod
    def set_bank_name(cls, new_name):
        """
        Set the bank name for all accounts
        
        Args:
            new_name (str): New bank name
        """
        if not new_name or not isinstance(new_name, str):
            raise ValueError("Bank name must be a non-empty string")
        
        old_name = cls.bank_name
        cls.bank_name = new_name
        print(f"🏛️  Bank name changed from '{old_name}' to '{new_name}'")
        print()
    
    @classmethod
    def set_minimum_balance(cls, new_minimum):
        """
        Set minimum balance requirement for all accounts
        
        Args:
            new_minimum (float): New minimum balance
        """
        if not isinstance(new_minimum, (int, float)) or new_minimum < 0:
            raise ValueError("Minimum balance must be a non-negative number")
        
        old_minimum = cls._minimum_balance
        cls._minimum_balance = float(new_minimum)
        print(f"💰 Minimum balance changed from ${old_minimum:.2f} to ${new_minimum:.2f}")
        print()
    
    @classmethod
    def get_all_accounts_summary(cls):
        """
        Get summary of all accounts
        
        Returns:
            dict: Summary statistics
        """
        if not cls._all_accounts:
            return {'total_accounts': 0, 'total_balance': 0, 'account_types': {}}
        
        total_balance = sum(account.get_balance() for account in cls._all_accounts)
        account_types = {}
        
        for account in cls._all_accounts:
            account_type = account.__class__.__name__
            if account_type not in account_types:
                account_types[account_type] = {'count': 0, 'total_balance': 0}
            account_types[account_type]['count'] += 1
            account_types[account_type]['total_balance'] += account.get_balance()
        
        return {
            'total_accounts': len(cls._all_accounts),
            'total_balance': total_balance,
            'account_types': account_types,
            'bank_name': cls.bank_name
        }


class SavingsAccount(Account):
    """
    Savings Account with interest calculation capability
    Inherits from Account with additional interest functionality
    """
    
    def __init__(self, account_number, account_holder, initial_balance, interest_rate):
        """
        Initialize a savings account
        
        Args:
            account_number (str): Unique account identifier
            account_holder (str): Name of the account holder
            initial_balance (float): Starting balance
            interest_rate (float): Annual interest rate (percentage)
        """
        # Validate interest rate
        if not isinstance(interest_rate, (int, float)) or interest_rate < 0:
            raise ValueError("Interest rate must be a non-negative number")
        
        # Call parent constructor
        super().__init__(account_number, account_holder, initial_balance)
        
        # Savings-specific attributes
        self._interest_rate = float(interest_rate)
        self._interest_earned = 0.0
        
        print(f"💰 Savings Account Features:")
        print(f"   Interest Rate: {self._interest_rate}% annually")
        print(f"   Monthly Interest Rate: {self._interest_rate/12:.3f}%")
        print()
    
    def calculate_monthly_interest(self):
        """
        Calculate and add monthly interest to the account
        
        Returns:
            float: Interest amount earned
        """
        monthly_rate = self._interest_rate / 12 / 100  # Convert to monthly decimal
        interest_amount = self._balance * monthly_rate
        
        if interest_amount > 0:
            self._balance += interest_amount
            self._interest_earned += interest_amount
            self._add_transaction("Interest", interest_amount, 
                                f"Monthly interest at {self._interest_rate}% annual rate")
            
            print(f"💎 Interest calculated:")
            print(f"   Account: {self._account_number}")
            print(f"   Monthly Rate: {monthly_rate*100:.3f}%")
            print(f"   Interest Earned: ${interest_amount:.2f}")
            print(f"   New Balance: ${self._balance:.2f}")
            print(f"   Total Interest Earned: ${self._interest_earned:.2f}")
            print()
        
        return interest_amount
    
    def get_interest_rate(self):
        """Get the current interest rate"""
        return self._interest_rate
    
    def get_total_interest_earned(self):
        """Get total interest earned since account opening"""
        return self._interest_earned
    
    def withdraw(self, amount):
        """
        Override withdrawal to maintain minimum balance for savings
        
        Args:
            amount (float): Amount to withdraw
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number")
        
        if not self._is_active:
            print(f"❌ Cannot withdraw from inactive account {self._account_number}")
            return False
        
        # Check if withdrawal would leave sufficient minimum balance
        remaining_balance = self._balance - amount
        if remaining_balance >= Account._minimum_balance:
            self._balance -= amount
            self._add_transaction("Withdrawal", -amount, f"Savings withdrawal of ${amount:.2f}")
            
            print(f"💸 Savings withdrawal successful:")
            print(f"   Account: {self._account_number}")
            print(f"   Amount: ${amount:.2f}")
            print(f"   New Balance: ${self._balance:.2f}")
            print(f"   Minimum Balance Maintained: ${Account._minimum_balance:.2f}")
            print()
            
            return True
        else:
            print(f"❌ Withdrawal denied - Minimum balance requirement:")
            print(f"   Account: {self._account_number}")
            print(f"   Requested: ${amount:.2f}")
            print(f"   Current Balance: ${self._balance:.2f}")
            print(f"   Minimum Required: ${Account._minimum_balance:.2f}")
            print(f"   Maximum Withdrawal: ${self._balance - Account._minimum_balance:.2f}")
            print()
            
            return False


class CheckingAccount(Account):
    """
    Checking Account with overdraft protection
    Inherits from Account with overdraft functionality
    """
    
    def __init__(self, account_number, account_holder, initial_balance, overdraft_limit):
        """
        Initialize a checking account
        
        Args:
            account_number (str): Unique account identifier
            account_holder (str): Name of the account holder
            initial_balance (float): Starting balance
            overdraft_limit (float): Maximum overdraft allowed
        """
        # Validate overdraft limit
        if not isinstance(overdraft_limit, (int, float)) or overdraft_limit < 0:
            raise ValueError("Overdraft limit must be a non-negative number")
        
        # Call parent constructor
        super().__init__(account_number, account_holder, initial_balance)
        
        # Checking-specific attributes
        self._overdraft_limit = float(overdraft_limit)
        self._overdraft_fees = 0.0
        self._overdraft_fee_rate = 35.0  # $35 per overdraft
        
        print(f"💳 Checking Account Features:")
        print(f"   Overdraft Limit: ${self._overdraft_limit:.2f}")
        print(f"   Overdraft Fee: ${self._overdraft_fee_rate:.2f} per transaction")
        print()
    
    def withdraw(self, amount):
        """
        Override withdrawal to allow overdraft protection
        
        Args:
            amount (float): Amount to withdraw
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number")
        
        if not self._is_active:
            print(f"❌ Cannot withdraw from inactive account {self._account_number}")
            return False
        
        # Calculate available funds including overdraft
        available_funds = self._balance + self._overdraft_limit
        
        if amount <= available_funds:
            # Check if overdraft will be used
            if amount > self._balance:
                overdraft_used = amount - self._balance
                overdraft_fee = self._overdraft_fee_rate
                
                # Apply withdrawal and overdraft fee
                self._balance -= amount
                self._balance -= overdraft_fee
                self._overdraft_fees += overdraft_fee
                
                # Record transactions
                self._add_transaction("Withdrawal", -amount, f"Checking withdrawal with overdraft")
                self._add_transaction("Overdraft Fee", -overdraft_fee, f"Fee for overdraft of ${overdraft_used:.2f}")
                
                print(f"⚠️  Overdraft withdrawal processed:")
                print(f"   Account: {self._account_number}")
                print(f"   Withdrawal Amount: ${amount:.2f}")
                print(f"   Overdraft Used: ${overdraft_used:.2f}")
                print(f"   Overdraft Fee: ${overdraft_fee:.2f}")
                print(f"   New Balance: ${self._balance:.2f}")
                print(f"   Remaining Overdraft: ${self._overdraft_limit + self._balance:.2f}")
                print()
            else:
                # Regular withdrawal without overdraft
                self._balance -= amount
                self._add_transaction("Withdrawal", -amount, f"Regular checking withdrawal")
                
                print(f"💸 Checking withdrawal successful:")
                print(f"   Account: {self._account_number}")
                print(f"   Amount: ${amount:.2f}")
                print(f"   New Balance: ${self._balance:.2f}")
                print(f"   Available Overdraft: ${self._overdraft_limit:.2f}")
                print()
            
            return True
        else:
            print(f"❌ Withdrawal denied - Exceeds available funds:")
            print(f"   Account: {self._account_number}")
            print(f"   Requested: ${amount:.2f}")
            print(f"   Current Balance: ${self._balance:.2f}")
            print(f"   Overdraft Limit: ${self._overdraft_limit:.2f}")
            print(f"   Total Available: ${available_funds:.2f}")
            print()
            
            return False
    
    def get_overdraft_limit(self):
        """Get the overdraft limit"""
        return self._overdraft_limit
    
    def get_available_overdraft(self):
        """Get remaining overdraft available"""
        return max(0, self._overdraft_limit + min(0, self._balance))
    
    def get_total_overdraft_fees(self):
        """Get total overdraft fees paid"""
        return self._overdraft_fees
    
    def set_overdraft_limit(self, new_limit):
        """
        Set a new overdraft limit
        
        Args:
            new_limit (float): New overdraft limit
        """
        if not isinstance(new_limit, (int, float)) or new_limit < 0:
            raise ValueError("Overdraft limit must be a non-negative number")
        
        old_limit = self._overdraft_limit
        self._overdraft_limit = float(new_limit)
        
        print(f"📝 Overdraft limit updated:")
        print(f"   Account: {self._account_number}")
        print(f"   Old Limit: ${old_limit:.2f}")
        print(f"   New Limit: ${new_limit:.2f}")
        print()


def demonstrate_account_features():
    """Demonstrate advanced account features"""
    print("🔧 ADVANCED ACCOUNT FEATURES DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Create a test account for demonstrations
    demo_account = SavingsAccount("DEMO001", "Demo User", 1000, 3.0)
    
    print("📊 Account Information:")
    info = demo_account.get_account_info()
    for key, value in info.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    print()
    
    print("📈 Transaction History:")
    history = demo_account.get_transaction_history()
    for transaction in history:
        timestamp = transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"   {transaction['id']}: {transaction['type']} - ${transaction['amount']:.2f}")
        print(f"      {timestamp} - {transaction['description']}")
        print(f"      Balance: ${transaction['balance_after']:.2f}")
    print()


def main():
    """Main function to test the bank account management system"""
    print("🎯 TESTING BANK ACCOUNT MANAGEMENT SYSTEM")
    print("=" * 70)
    print()
    
    try:
        # Test Case 1: Creating different types of accounts
        print("📝 TEST CASE 1: Creating Different Account Types")
        print("-" * 50)
        
        savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
        checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)
        
        print(f"Savings Account: {savings_account}")
        print(f"Checking Account: {checking_account}")
        print()
        
        # Test Case 2: Deposit and Withdrawal operations
        print("📝 TEST CASE 2: Deposit and Withdrawal Operations")
        print("-" * 50)
        
        print(f"Savings balance before: ${savings_account.get_balance()}")
        savings_account.deposit(500)
        print(f"After depositing $500: ${savings_account.get_balance()}")
        
        withdrawal_result = savings_account.withdraw(200)
        print(f"Withdrawal result: {withdrawal_result}")
        print(f"Balance after withdrawal: ${savings_account.get_balance()}")
        print()
        
        # Test Case 3: Overdraft protection in checking account
        print("📝 TEST CASE 3: Overdraft Protection")
        print("-" * 50)
        
        print(f"Checking balance: ${checking_account.get_balance()}")
        overdraft_result = checking_account.withdraw(600)  # Should use overdraft
        print(f"Overdraft withdrawal: {overdraft_result}")
        print(f"Balance after overdraft: ${checking_account.get_balance()}")
        print()
        
        # Test Case 4: Interest calculation for savings
        print("📝 TEST CASE 4: Interest Calculation")
        print("-" * 50)
        
        interest_earned = savings_account.calculate_monthly_interest()
        print(f"Monthly interest earned: ${interest_earned}")
        print()
        
        # Test Case 5: Class methods and variables
        print("📝 TEST CASE 5: Class Methods and Variables")
        print("-" * 50)
        
        print(f"Total accounts created: {Account.get_total_accounts()}")
        print(f"Bank name: {Account.bank_name}")
        
        # Change bank settings using class method
        Account.set_bank_name("New National Bank")
        Account.set_minimum_balance(100)
        print()
        
        # Test Case 6: Account validation
        print("📝 TEST CASE 6: Account Validation")
        print("-" * 50)
        
        try:
            invalid_account = SavingsAccount("SA002", "", -100, 1.5)  # Should raise error
        except ValueError as e:
            print(f"Validation error: {e}")
        print()
        
        # Additional tests
        print("📝 ADDITIONAL TESTS: Advanced Features")
        print("-" * 50)
        
        # Test bank summary
        summary = Account.get_all_accounts_summary()
        print("🏦 Bank Summary:")
        print(f"   Total Accounts: {summary['total_accounts']}")
        print(f"   Total Balance: ${summary['total_balance']:.2f}")
        print(f"   Bank Name: {summary['bank_name']}")
        print()
        
        for account_type, data in summary['account_types'].items():
            print(f"   {account_type}: {data['count']} accounts, ${data['total_balance']:.2f}")
        print()
        
        # Demonstrate advanced features
        demonstrate_account_features()
        
        print("🎉 BANK ACCOUNT SYSTEM TESTING COMPLETE!")
        print("=" * 70)
        print()
        print("✅ All features tested successfully:")
        print("   • Account creation with validation")
        print("   • Inheritance (SavingsAccount, CheckingAccount)")
        print("   • Encapsulation with private attributes")
        print("   • Deposit and withdrawal operations")
        print("   • Overdraft protection for checking accounts")
        print("   • Interest calculation for savings accounts")
        print("   • Class methods and class variables")
        print("   • Comprehensive error handling")
        print("   • Transaction history tracking")
        print("   • Account summary and reporting")
        print()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == "__main__":
    main()
