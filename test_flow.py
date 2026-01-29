#!/usr/bin/env python
"""
TEST SCRIPT - Simulate Complete Login & Payment Flow
Run this on Kali Linux AFTER starting the Flask server: python test_flow.py
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000/api"

def test_login():
    """Test user login"""
    print("\n" + "="*70)
    print("TESTING LOGIN")
    print("="*70)
    
    credentials = {
        "email": "attaullah@gmail.com",
        "password": "123456789Aa1@"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            print("✓ LOGIN SUCCESSFUL!")
            print(f"  - Email: {data['user']['email']}")
            print(f"  - Role: {data['user']['role']}")
            print(f"  - Token: {data['token'][:30]}...")
            return data['token']
        else:
            print("✗ LOGIN FAILED!")
            print(f"  - Error: {data.get('error', 'Unknown error')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("✗ CANNOT CONNECT TO SERVER!")
        print("  Make sure Flask is running: flask run --debug")
        return None
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return None

def test_payment(token):
    """Test payment processing"""
    print("\n" + "="*70)
    print("TESTING PAYMENT PROCESSING")
    print("="*70)
    
    payment_data = {
        "card_number": "4111111111111111",
        "cvv": "123",
        "expiry_date": "12/26",
        "amount": "99.99",
        "cardholder_name": "Test User",
        "currency": "USD"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/payment/process",
            json=payment_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=5
        )
        
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            print("✓ PAYMENT SUCCESSFUL!")
            print(f"  - Transaction ID: {data.get('transaction_id', 'N/A')}")
            print(f"  - Amount: ${data.get('amount', 'N/A')}")
            print(f"  - Status: {data.get('status', 'N/A')}")
            return True
        else:
            print("✗ PAYMENT FAILED!")
            print(f"  - Error: {data.get('error', 'Unknown error')}")
            print(f"  - Message: {data.get('message', 'N/A')}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_transaction_history(token):
    """Get transaction history"""
    print("\n" + "="*70)
    print("TESTING TRANSACTION HISTORY")
    print("="*70)
    
    try:
        response = requests.get(
            f"{BASE_URL}/payment/history",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            transactions = data.get('transactions', [])
            print(f"✓ FOUND {len(transactions)} TRANSACTION(S)")
            
            for trans in transactions:
                print(f"\n  Transaction #{trans.get('id')}:")
                print(f"    - Amount: ${trans.get('amount')}")
                print(f"    - Status: {trans.get('status')}")
                print(f"    - Card: ****{trans.get('card_last_four')}")
                print(f"    - Date: {trans.get('created_at')}")
            
            return True
        else:
            print("✗ CANNOT RETRIEVE HISTORY!")
            print(f"  - Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "#"*70)
    print("# PAYMENT GATEWAY - COMPLETE TEST FLOW")
    print("#"*70)
    print("\nMake sure Flask is running:")
    print("  flask run --debug")
    
    # Step 1: Login
    token = test_login()
    if not token:
        print("\n✗ CANNOT PROCEED - LOGIN FAILED")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 2: Process Payment
    payment_success = test_payment(token)
    if not payment_success:
        print("\n✗ PAYMENT FAILED - Check logs for details")
    
    time.sleep(1)
    
    # Step 3: Get Transaction History
    test_transaction_history(token)
    
    # Summary
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\n✓ If all tests passed:")
    print("  1. Open browser: http://localhost:5000")
    print("  2. Login with: attaullah@gmail.com / 123456789Aa1@")
    print("  3. Click 'New Payment' to process payment via UI")
    print("  4. View transactions in dashboard")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()
