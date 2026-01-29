#!/usr/bin/env bash
# Quick Start Script - Copy and paste commands below

echo "🚀 PAYMENT SYSTEM QUICK START"
echo "=============================="
echo ""
echo "Running setup and tests..."
echo ""

# Step 1: Setup demo user
echo "1️⃣  Setting up demo user..."
python fix_and_create_demo.py
if [ $? -ne 0 ]; then
    echo "❌ Demo user setup failed"
    exit 1
fi
echo ""

# Step 2: Quick verification
echo "2️⃣  Verifying system..."
python quick_verify.py
if [ $? -ne 0 ]; then
    echo "❌ System verification failed"
    exit 1
fi
echo ""

# Step 3: Run tests
echo "3️⃣  Running tests..."
python test_payment_fix.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi
echo ""

echo "✅ All checks passed!"
echo ""
echo "🎯 Next steps:"
echo "1. Start Flask: flask run --debug"
echo "2. Open: http://localhost:5000/checkout_fixed"
echo "3. Login: attaullah@gmail.com / 123456789Aa1@"
echo "4. Test payment: 4111 1111 1111 1111 | 12/26 | 123 | \$99.99"
echo ""
