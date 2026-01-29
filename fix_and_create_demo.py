#!/usr/bin/env python
"""
CREATE MULTIPLE DEMO USERS ON KALI LINUX
Run after migrations are applied: python fix_and_create_demo.py

Creates 6 demo users with different roles:
1. attaullah@gmail.com (Main account - merchant)
2. user1@demo.com (john_trader - trader)
3. user2@demo.com (sarah_merchant - merchant)
4. user3@demo.com (mike_business - business)
5. user4@demo.com (lisa_store - store owner)
6. user5@demo.com (alex_vendor - vendor)
"""
import sys
from app import create_app, db
from app.models.user import User

def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("CREATING 6 DEMO USERS")
        print("=" * 70)
        
        try:
            # Define all demo users
            demo_users = [
                {
                    'email': 'attaullah@gmail.com',
                    'role': 'merchant',
                    'display_name': 'Attaullah Admin'
                },
                {
                    'email': 'user1@demo.com',
                    'role': 'customer',
                    'display_name': 'John Trader'
                },
                {
                    'email': 'user2@demo.com',
                    'role': 'merchant',
                    'display_name': 'Sarah Merchant'
                },
                {
                    'email': 'user3@demo.com',
                    'role': 'customer',
                    'display_name': 'Mike Business'
                },
                {
                    'email': 'user4@demo.com',
                    'role': 'merchant',
                    'display_name': 'Lisa Store'
                },
                {
                    'email': 'user5@demo.com',
                    'role': 'customer',
                    'display_name': 'Alex Vendor'
                },
            ]
            
            password = '123456789Aa1@'
            created_count = 0
            updated_count = 0
            
            print("\n📝 Creating/Updating Demo Users:\n")
            
            for user_data in demo_users:
                email = user_data['email']
                role = user_data['role']
                display_name = user_data['display_name']
                
                # Check if user exists
                existing_user = User.query.filter_by(email=email).first()
                
                if existing_user:
                    print(f"   ✓ {email} (already exists)")
                    existing_user.set_password(password)
                    db.session.commit()
                    updated_count += 1
                else:
                    print(f"   ✓ Creating {email} ({role})")
                    demo_user = User(
                        email=email,
                        role=role,
                        is_active=True
                    )
                    demo_user.set_password(password)
                    db.session.add(demo_user)
                    db.session.flush()
                    created_count += 1
            
            db.session.commit()
            
            print("\n" + "=" * 70)
            print("DEMO CREDENTIALS")
            print("=" * 70)
            print(f"Created: {created_count} new users")
            print(f"Updated: {updated_count} existing users")
            print(f"\nPassword (all accounts): {password}")
            print("\nAvailable Demo Users:")
            print("-" * 70)
            
            for i, user_data in enumerate(demo_users, 1):
                print(f"{i}. {user_data['email']:25} | Role: {user_data['role']:10} | {user_data['display_name']}")
            
            print("=" * 70)
            print("\n✓ READY TO LOGIN AND DEMO!")
            print("=" * 70)
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
