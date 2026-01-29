#!/usr/bin/env python3
"""
Payment Transaction Testing & Fixing Script
Tests payment processing and verifies transactions appear in history
"""

import sys
import os
import json
import time
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_validators():
    """Test the validators with various inputs"""
    print_header("Testing Validators")
    
    from app.utils.validators import (
        validate_card_number, validate_cvv, validate_expiry_date,
        validate_amount, validate_name
    )
    
    tests = [
        ("Card Number - Valid", 
         lambda: validate_card_number("4111111111111111"),
         (True, None)),
        
        ("Card Number - Too Short",
         lambda: validate_card_number("411111"),
         (False, None)),
        
        ("CVV - Valid",
         lambda: validate_cvv("123"),
         (True, None)),
        
        ("CVV - Invalid (2 digits)",
         lambda: validate_cvv("12"),
         (False, None)),
        
        ("Expiry - Valid Future",
         lambda: validate_expiry_date("12/26"),
         (True, None)),
        
        ("Expiry - Invalid Format",
         lambda: validate_expiry_date("1226"),
         (False, None)),
        
        ("Amount - Valid",
         lambda: validate_amount("99.99"),
         (True, None, 99.99)),
        
        ("Amount - Zero",
         lambda: validate_amount("0"),
         (False, None, None)),
        
        ("Name - Valid",
         lambda: validate_name("John Doe"),
         (True, None)),
        
        ("Name - Too Short",
         lambda: validate_name("J"),
         (False, None)),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func, expected_result in tests:
        try:
            result = test_func()
            # Check if result matches expected (just check first element for all)
            if (isinstance(expected_result, tuple) and len(expected_result) >= 2):
                if result[0] == expected_result[0]:
                    print_success(f"{test_name}: {result[0]}")
                    passed += 1
                else:
                    print_error(f"{test_name}: Expected {expected_result[0]}, got {result[0]}")
                    print(f"   Full result: {result}")
                    failed += 1
            else:
                print_warning(f"{test_name}: Could not verify")
        except Exception as e:
            print_error(f"{test_name}: {str(e)}")
            failed += 1
    
    print(f"\nValidator Tests: {passed} passed, {failed} failed")
    return failed == 0

def test_payment_service():
    """Test the payment service"""
    print_header("Testing Payment Service")
    
    from app import create_app, db
    from app.models.user import User
    from app.services.payment_service import PaymentService
    
    app = create_app()
    
    with app.app_context():
        # Find demo user
        user = User.query.filter_by(email='attaullah@gmail.com').first()
        if not user:
            print_error("Demo user not found. Creating demo user...")
            # Run fix script
            os.system('python fix_and_create_demo.py')
            user = User.query.filter_by(email='attaullah@gmail.com').first()
        
        if user:
            print_success(f"Found user: {user.email}")
            
            # Test payment
            service = PaymentService()
            
            print_info("Processing test payment...")
            success, response, transaction = service.process_payment(
                user_id=user.id,
                card_number='4111111111111111',
                cvv='123',
                expiry_date='12/26',
                amount='99.99',
                cardholder_name='John Doe',
                currency='USD',
                ip_address='127.0.0.1',
                user_agent='Test'
            )
            
            print(f"\nPayment Response:")
            print(f"  Success: {success}")
            print(f"  Message: {response.get('message', response.get('error', 'N/A'))}")
            
            if transaction:
                print(f"  Transaction ID: {transaction.id}")
                print(f"  Amount: ${transaction.amount}")
                print(f"  Status: {transaction.status.value}")
                print(f"  Fraud Score: {transaction.fraud_score}")
                print_success("Payment processed and transaction created!")
                
                # Verify transaction in database
                from app.models.transaction import Transaction
                saved_tx = Transaction.query.get(transaction.id)
                if saved_tx:
                    print_success(f"Transaction verified in database: #{saved_tx.id}")
                    return True
            else:
                print_error("No transaction object returned")
                print(f"Response: {response}")
                return False
        else:
            print_error("Could not find or create demo user")
            return False
    
    return False

def test_transaction_history():
    """Test transaction history retrieval"""
    print_header("Testing Transaction History")
    
    from app import create_app, db
    from app.models.user import User
    from app.models.transaction import Transaction
    
    app = create_app()
    
    with app.app_context():
        user = User.query.filter_by(email='attaullah@gmail.com').first()
        if user:
            transactions = Transaction.query.filter_by(user_id=user.id).all()
            print_success(f"Found {len(transactions)} transaction(s) for user")
            
            for tx in transactions:
                print(f"\n  Transaction #{tx.id}:")
                print(f"    Amount: ${tx.amount}")
                print(f"    Status: {tx.status.value}")
                print(f"    Card: {tx.masked_card_number}")
                print(f"    Created: {tx.created_at}")
                print(f"    Fraud Score: {tx.fraud_score}")
            
            return len(transactions) > 0
        else:
            print_error("Demo user not found")
            return False

def test_encryption():
    """Test card encryption"""
    print_header("Testing Card Encryption")
    
    from app.utils.encryption import AESCipher
    
    cipher = AESCipher()
    
    # Test data
    card_data = "4111111111111111|12/26"
    
    # Encrypt
    encrypted = cipher.encrypt(card_data)
    print_success(f"Encrypted card data: {len(encrypted)} bytes")
    
    # Decrypt
    decrypted = cipher.decrypt(encrypted)
    print_success(f"Decrypted: {decrypted}")
    
    if decrypted == card_data:
        print_success("Encryption/Decryption working correctly!")
        return True
    else:
        print_error(f"Decryption mismatch. Expected: {card_data}, Got: {decrypted}")
        return False

def create_demo_transactions():
    """Create multiple demo transactions"""
    print_header("Creating Demo Transactions")
    
    from app import create_app, db
    from app.models.user import User
    from app.services.payment_service import PaymentService
    
    app = create_app()
    
    with app.app_context():
        user = User.query.filter_by(email='attaullah@gmail.com').first()
        if not user:
            print_error("Demo user not found")
            return False
        
        service = PaymentService()
        
        test_cards = [
            ('4111111111111111', '99.99'),
            ('5555555555554444', '49.50'),
            ('378282246310005', '150.00'),
        ]
        
        successful = 0
        for card, amount in test_cards:
            print(f"\nProcessing ${amount} on card {card[:4]}...")
            success, response, tx = service.process_payment(
                user_id=user.id,
                card_number=card,
                cvv='123',
                expiry_date='12/26',
                amount=amount,
                cardholder_name='Test User',
                currency='USD',
                ip_address='127.0.0.1',
                user_agent='Demo Script'
            )
            
            if success:
                print_success(f"Transaction #{tx.id}: {response.get('message')}")
                successful += 1
            else:
                print_warning(f"Transaction failed: {response.get('message')}")
        
        print(f"\n✅ Created {successful} successful transactions")
        return successful > 0

def main():
    """Main test runner"""
    print_header("🧪 Payment Transaction Testing Suite")
    print_info("Testing validators, payment service, and transaction history\n")
    
    results = {}
    
    # Run tests
    results['validators'] = test_validators()
    results['encryption'] = test_encryption()
    results['payment_service'] = test_payment_service()
    results['transaction_history'] = test_transaction_history()
    results['demo_transactions'] = create_demo_transactions()
    
    # Summary
    print_header("📊 Test Summary")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print_success("\nAll tests passed! Payment system is working correctly.")
        print(f"\n✨ Demo User: attaullah@gmail.com / 123456789Aa1@")
        print(f"💳 Test Card: 4111 1111 1111 1111 | 12/26 | 123 | $99.99")
        print(f"\n🚀 You can now:")
        print(f"   1. Start Flask: flask run --debug")
        print(f"   2. Visit: http://localhost:5000/checkout_fixed")
        print(f"   3. Login and process payments")
        print(f"   4. View transaction history")
    else:
        print_error("\nSome tests failed. Please check the errors above.")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
