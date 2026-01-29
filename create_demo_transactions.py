#!/usr/bin/env python3
"""
Create demo transactions for all demo users
Adds sample transactions to show the history tab working

Creates realistic transaction history for 6 demo users:
- attaullah@gmail.com: 15 transactions
- user1@demo.com: 12 transactions  
- user2@demo.com: 18 transactions
- user3@demo.com: 8 transactions
- user4@demo.com: 22 transactions
- user5@demo.com: 10 transactions

Total: 95+ transactions with realistic distribution
Status: SUCCESS 75%, FAILED 20%, PENDING 4%, FRAUD 1%
Dates: Spread across last 60 days
"""

from app import db, create_app
from app.models.user import User
from app.models.transaction import Transaction, TransactionStatus
from datetime import datetime, timedelta
import random

def create_demo_transactions():
    """Create demo transactions for all demo users"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 70)
            print("CREATING DEMO TRANSACTIONS FOR ALL USERS")
            print("=" * 70)
            
            # Define transaction templates per user
            user_transactions = {
                'attaullah@gmail.com': {
                    'count': 15,
                    'amounts': [50, 100, 150, 200, 75, 99.99, 125, 175],
                    'cards': ['4111 1111 1111 1111', '5555 5555 5555 4444'],
                    'role': 'merchant'
                },
                'user1@demo.com': {
                    'count': 12,
                    'amounts': [25, 50, 75, 100, 150, 80],
                    'cards': ['4111 1111 1111 1111', '5555 5555 5555 4444', '378282246310005'],
                    'role': 'customer'
                },
                'user2@demo.com': {
                    'count': 18,
                    'amounts': [100, 250, 500, 150, 200, 350, 75, 125],
                    'cards': ['4111 1111 1111 1111', '5555 5555 5555 4444'],
                    'role': 'merchant'
                },
                'user3@demo.com': {
                    'count': 8,
                    'amounts': [25, 50, 75, 100, 150],
                    'cards': ['4111 1111 1111 1111', '378282246310005'],
                    'role': 'customer'
                },
                'user4@demo.com': {
                    'count': 22,
                    'amounts': [100, 200, 300, 500, 150, 250, 350, 75, 125, 175],
                    'cards': ['4111 1111 1111 1111', '5555 5555 5555 4444'],
                    'role': 'merchant'
                },
                'user5@demo.com': {
                    'count': 10,
                    'amounts': [50, 100, 150, 75, 125, 200],
                    'cards': ['4111 1111 1111 1111', '378282246310005'],
                    'role': 'customer'
                },
            }
            
            from app.utils.encryption import mask_card_number, AESCipher
            encryptor = AESCipher()
            
            total_transactions = 0
            
            for email, config in user_transactions.items():
                # Get user
                user = User.query.filter_by(email=email).first()
                
                if not user:
                    print(f"\n⚠️  User not found: {email}")
                    continue
                
                user_id = user.id
                
                # Delete existing transactions for this user
                Transaction.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                
                print(f"\n👤 {email} ({config['role']}):")
                
                # Create transactions for this user
                for i in range(config['count']):
                    # Random amount
                    amount = random.choice(config['amounts'])
                    if random.random() > 0.8:  # Vary amounts sometimes
                        amount = round(random.uniform(10, 500), 2)
                    
                    # Random card
                    card = random.choice(config['cards'])
                    card_num = card.replace(' ', '')
                    
                    # Random status (75% SUCCESS, 20% FAILED, 4% PENDING, 1% FRAUD)
                    status_roll = random.random()
                    if status_roll < 0.75:
                        status = TransactionStatus.SUCCESS
                    elif status_roll < 0.95:
                        status = TransactionStatus.FAILED
                    elif status_roll < 0.99:
                        status = TransactionStatus.PENDING
                    else:
                        status = TransactionStatus.FRAUD
                    
                    # Random date in last 60 days
                    days_ago = random.randint(0, 60)
                    hours_ago = random.randint(0, 23)
                    total_hours = days_ago * 24 + hours_ago
                    created_at = datetime.utcnow() - timedelta(hours=total_hours)
                    
                    # Create transaction
                    masked = mask_card_number(card_num)
                    encrypted_token = encryptor.encrypt(f"{card_num}|12/26")
                    
                    transaction = Transaction(
                        user_id=user_id,
                        amount=amount,
                        currency='USD',
                        status=status,
                        masked_card_number=masked,
                        encrypted_card_token=encrypted_token,
                        fraud_score=random.uniform(0.1, 0.9) if status != TransactionStatus.FRAUD else 0.85,
                        ip_address=f"192.168.1.{random.randint(1, 254)}",
                        user_agent='Mozilla/5.0 Demo',
                        created_at=created_at,
                        processed_at=created_at + timedelta(seconds=random.randint(1, 5)) if status in [TransactionStatus.SUCCESS, TransactionStatus.FAILED] else None,
                        external_transaction_id=f"BANK_{random.randint(100000, 999999)}" if status == TransactionStatus.SUCCESS else None
                    )
                    
                    db.session.add(transaction)
                    total_transactions += 1
                
                db.session.commit()
                print(f"   ✓ Created {config['count']} transactions")
            
            # Print summary
            print("\n" + "=" * 70)
            print("TRANSACTION CREATION SUMMARY")
            print("=" * 70)
            print(f"Total Transactions Created: {total_transactions}")
            print(f"Users: 6 (attaullah@gmail.com + 5 additional demo users)")
            print(f"\nTransaction Distribution:")
            print(f"   - Merchant Users: 3 (sarah, lisa, attaullah)")
            print(f"   - Customer Users: 3 (john, mike, alex)")
            print(f"\nStatus Distribution:")
            print(f"   - SUCCESS: ~75% ({int(total_transactions * 0.75)})")
            print(f"   - FAILED: ~20% ({int(total_transactions * 0.20)})")
            print(f"   - PENDING: ~4% ({int(total_transactions * 0.04)})")
            print(f"   - FRAUD: ~1% ({int(total_transactions * 0.01)})")
            print(f"\nDate Range: Last 60 days")
            print(f"Amount Range: $10 - $500 per transaction")
            print("=" * 70)
            print("\n✅ Demo transactions successfully created!")
            
        except Exception as e:
            print(f"❌ Error creating transactions: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    create_demo_transactions()
