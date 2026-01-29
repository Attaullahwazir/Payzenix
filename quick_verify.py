#!/usr/bin/env python3
"""
Quick Payment Fix Verification Script
Minimal, fast tests to ensure everything works
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*60)
    print("  🔧 QUICK PAYMENT SYSTEM VERIFICATION")
    print("="*60 + "\n")
    
    # Test 1: Imports
    print("1️⃣  Testing imports...")
    try:
        from app import create_app, db
        from app.models.user import User
        from app.models.transaction import Transaction
        from app.services.payment_service import PaymentService
        from app.utils.validators import validate_card_number, validate_amount
        print("   ✅ All imports successful\n")
    except Exception as e:
        print(f"   ❌ Import failed: {e}\n")
        return 1
    
    # Test 2: Database
    print("2️⃣  Testing database...")
    try:
        app = create_app()
        with app.app_context():
            user = User.query.filter_by(email='attaullah@gmail.com').first()
            if user:
                print(f"   ✅ Demo user found: {user.email}\n")
            else:
                print("   ⚠️  Demo user not found. Run: python fix_and_create_demo.py\n")
                return 1
    except Exception as e:
        print(f"   ❌ Database error: {e}\n")
        return 1
    
    # Test 3: Validators
    print("3️⃣  Testing validators...")
    try:
        # Test card validation
        valid, err = validate_card_number("4111111111111111")
        assert valid == True, f"Card validation failed: {err}"
        
        # Test amount validation
        valid, err, amount = validate_amount("99.99")
        assert valid == True, f"Amount validation failed: {err}"
        assert amount == 99.99, f"Amount mismatch: {amount}"
        
        print("   ✅ Validators working correctly\n")
    except Exception as e:
        print(f"   ❌ Validator error: {e}\n")
        return 1
    
    # Test 4: Encryption
    print("4️⃣  Testing encryption...")
    try:
        from app.utils.encryption import AESCipher
        cipher = AESCipher()
        
        test_data = "4111111111111111|12/26"
        encrypted = cipher.encrypt(test_data)
        decrypted = cipher.decrypt(encrypted)
        
        assert decrypted == test_data, "Encryption roundtrip failed"
        print("   ✅ Encryption working correctly\n")
    except Exception as e:
        print(f"   ❌ Encryption error: {e}\n")
        return 1
    
    # Test 5: Transaction Model
    print("5️⃣  Testing transaction model...")
    try:
        with app.app_context():
            txns = Transaction.query.limit(1).all()
            if txns:
                tx = txns[0]
                tx_dict = tx.to_dict()
                assert 'id' in tx_dict
                assert 'amount' in tx_dict
                assert 'status' in tx_dict
                print(f"   ✅ Transactions working ({len(Transaction.query.all())} total)\n")
            else:
                print("   ⚠️  No transactions yet (will be created on first payment)\n")
    except Exception as e:
        print(f"   ❌ Transaction error: {e}\n")
        return 1
    
    # Test 6: Payment Service
    print("6️⃣  Testing payment service...")
    try:
        service = PaymentService()
        assert service is not None
        print("   ✅ Payment service initialized\n")
    except Exception as e:
        print(f"   ❌ Payment service error: {e}\n")
        return 1
    
    # Summary
    print("="*60)
    print("  ✅ ALL CHECKS PASSED!")
    print("="*60)
    print("\n📝 Next steps:\n")
    print("   1. Start Flask:")
    print("      flask run --debug\n")
    print("   2. Open in browser:")
    print("      http://localhost:5000/checkout_fixed\n")
    print("   3. Login with:")
    print("      Email: attaullah@gmail.com")
    print("      Password: 123456789Aa1@\n")
    print("   4. Test payment with:")
    print("      Card: 4111 1111 1111 1111")
    print("      Expiry: 12/26")
    print("      CVV: 123")
    print("      Amount: $99.99\n")
    print("="*60 + "\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
