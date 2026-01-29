#!/usr/bin/env python
"""
TROUBLESHOOTING SCRIPT - Check Login and Payment Processing
Run on Kali Linux after migrations and user creation
"""
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.transaction import Transaction
from app.utils.jwt_service import generate_token, verify_token

def main():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("PAYMENT GATEWAY - LOGIN & PAYMENT VERIFICATION")
        print("="*70)
        
        # Check demo user
        print("\n1. CHECKING DEMO USER...")
        demo_user = User.query.filter_by(email='attaullah@gmail.com').first()
        
        if not demo_user:
            print("   ✗ Demo user NOT found!")
            print("   Run: python fix_and_create_demo.py")
            return
        
        print(f"   ✓ Demo user found!")
        print(f"     - Email: {demo_user.email}")
        print(f"     - ID: {demo_user.id}")
        print(f"     - Role: {demo_user.role}")
        print(f"     - Active: {demo_user.is_active}")
        
        # Test password
        print("\n2. CHECKING PASSWORD...")
        password_match = demo_user.check_password('123456789Aa1@')
        if password_match:
            print("   ✓ Password verification working!")
        else:
            print("   ✗ Password verification FAILED!")
            print("   Re-creating user with correct password...")
            demo_user.set_password('123456789Aa1@')
            db.session.commit()
            print("   ✓ Password updated!")
        
        # Test JWT token generation
        print("\n3. CHECKING JWT TOKEN GENERATION...")
        try:
            token = generate_token(demo_user.id, demo_user.email, demo_user.role)
            print(f"   ✓ Token generated: {token[:50]}...")
            
            # Verify token
            payload = verify_token(token)
            if payload:
                print(f"   ✓ Token verified successfully!")
                print(f"     - User ID: {payload['user_id']}")
                print(f"     - Email: {payload['email']}")
                print(f"     - Role: {payload['role']}")
            else:
                print("   ✗ Token verification failed!")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Check if user has transactions
        print("\n4. CHECKING EXISTING TRANSACTIONS...")
        transactions = Transaction.query.filter_by(user_id=demo_user.id).all()
        print(f"   ✓ Found {len(transactions)} transaction(s)")
        for trans in transactions:
            print(f"     - ID: {trans.id}, Amount: ${trans.amount}, Status: {trans.status}")
        
        print("\n" + "="*70)
        print("VERIFICATION COMPLETE")
        print("="*70)
        print("\n✓ YOUR LOGIN CREDENTIALS:")
        print("  Email:    attaullah@gmail.com")
        print("  Password: 123456789Aa1@")
        print("\n✓ NEXT STEPS:")
        print("  1. Login at: http://localhost:5000/login")
        print("  2. Go to: http://localhost:5000/checkout")
        print("  3. Process a test payment (use card: 4111111111111111)")
        print("\n✓ TEST CARD FOR PAYMENTS:")
        print("  - Card Number: 4111 1111 1111 1111")
        print("  - Expiry: 12/26")
        print("  - CVV: 123")
        print("  - Amount: Any amount (e.g., 99.99)")
        print("="*70 + "\n")

if __name__ == '__main__':
    main()
