#!/usr/bin/env python3
"""
Complete payment system setup for testing
Creates demo user and demo transactions
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, script_name], cwd=os.path.dirname(__file__))
    if result.returncode != 0:
        print(f"⚠️  {script_name} had some issues (check output above)")
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("  🚀 PAYMENT SYSTEM - COMPLETE SETUP")
    print("="*60)
    
    # Step 1: Create demo user
    if os.path.exists('fix_and_create_demo.py'):
        success = run_script('fix_and_create_demo.py', 'Step 1: Creating Demo User')
        if not success:
            print("⚠️  Demo user creation had issues (MySQL may not be running)")
            print("   Run: sudo service mysql start")
    else:
        print("❌ fix_and_create_demo.py not found")
    
    # Step 2: Create demo transactions
    if os.path.exists('create_demo_transactions.py'):
        success = run_script('create_demo_transactions.py', 'Step 2: Creating Demo Transactions')
        if not success:
            print("⚠️  Demo transactions had issues")
    else:
        print("❌ create_demo_transactions.py not found")
    
    # Step 3: Run verification
    if os.path.exists('quick_verify.py'):
        success = run_script('quick_verify.py', 'Step 3: System Verification')
    
    print("\n" + "="*60)
    print("  ✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Next steps:\n")
    print("1. Make sure MySQL is running:")
    print("   sudo service mysql start\n")
    print("2. Start Flask server:")
    print("   flask run --debug\n")
    print("3. Open browser and test:")
    print("   Simple form: http://localhost:5000/api/payment/test")
    print("   Advanced form: http://localhost:5000/checkout_fixed\n")
    print("4. Login with:")
    print("   Email: attaullah@gmail.com")
    print("   Password: 123456789Aa1@\n")
    print("5. Test payment with:")
    print("   Card: 4111 1111 1111 1111")
    print("   Expiry: 12/26")
    print("   CVV: 123")
    print("   Amount: $99.99\n")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
