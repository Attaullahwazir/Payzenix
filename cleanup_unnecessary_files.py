#!/usr/bin/env python
"""
CLEANUP SCRIPT - Remove unnecessary documentation files
Run on Windows: python cleanup_unnecessary_files.py
"""
import os
from pathlib import Path

# Files to DELETE (unnecessary documentation duplicates)
FILES_TO_DELETE = [
    # Duplicate documentation files
    "ALL_FIXES_COMPLETE.txt",
    "AUDIT_COMPLETION_STATUS.md",
    "CHANGES_SUMMARY.md",
    "CODEBASE_AUDIT.json",
    "COMPLETE_FEATURE_STATUS.md",
    "COMPLETE_PROJECT_STATUS_REPORT.md",
    "COMPLETE_SETUP_GUIDE.md",
    "COMPLETION_SUMMARY.md",
    "COMPREHENSIVE_PROJECT_FIXES.md",
    "COMPREHENSIVE_TESTING.md",
    "CRITICAL_INFORMATION.md",
    "CURRENT_IMPLEMENTATION_STATUS.md",
    "DEPLOYMENT_READY.md",
    "EXECUTIVE_SUMMARY.md",
    "FEATURE_AUDIT_FINDINGS.md",
    "FINAL_DEPLOYMENT_GUIDE.md",
    "FINAL_SUMMARY.txt",
    "FINAL_VERIFICATION.md",
    "FIXES_AND_FEATURES.md",
    "FIXES_QUICK_REFERENCE.md",
    "FIXES_SUMMARY.md",
    "FLUTTER_SETUP_GUIDE.md",
    "GETTING_STARTED.md",
    "MASTER_COMPLETION_CHECKLIST.md",
    "MASTER_PROJECT_DOCUMENTATION.md",
    "MYSQL_CONNECTION_FIX.md",
    "PAYMENT_AND_UI_FIXES.md",
    "PROJECT_FILE_LISTING.md",
    "PROJECT_READY_FOR_DEPLOYMENT.md",
    "PROJECT_STATUS.md",
    "QUICK_DEPLOY_CHECKLIST.md",
    "QUICK_REFERENCE.md",
    "QUICK_REFERENCE_CARD.md",
    "QUICK_START_CARD.md",
    "README_DOCUMENTATION.md",
    "SESSION_SUMMARY.md",
    "SESSION_SUMMARY_LATEST.md",
    "SETUP_FIXES_APPLIED.md",
    "START_HERE.md",
    "START_HERE_DOCUMENTATION_INDEX.md",
    "STATUS_CARD.md",
    "SUPERVISOR_DEMO_CHECKLIST.md",
    "TESTING_GUIDE.md",
    "UI_FIXES_APPLIED.md",
    "VISUAL_SUMMARY.md",
]

# Files to KEEP (core documentation)
FILES_TO_KEEP = [
    "README.md",
    "SETUP.md",
    "QUICK_START.md",
    "START_HERE_NOW.md",
    "FINAL_CHECKLIST.md",
    "PROJECT_COMPLETE_SUMMARY.md",
    "PAYMENT_FLOW_EXPLAINED.md",
    "TROUBLESHOOTING_GUIDE.md",
    "SUPERVISOR_DEMO_WALKTHROUGH.md",
    "DOCUMENTATION_INDEX.md",
    "DOCUMENTATION_CREATED.md",
    "DEPLOYMENT.md",
    "DEPLOYMENT_NOTES.md",
    "KALI_LINUX_SETUP.md",
    "COMPLETE_DEPLOYMENT_GUIDE.md",
    "COMPLETE_IMPLEMENTATION_SUMMARY.md",
    "DEVELOPER_QUICK_REFERENCE.md",
    "COMPREHENSIVE_TESTING_CHECKLIST.md",
    "FINAL_REVIEW.md",
    "PROJECT_SUMMARY.md",
    "ADVANCED_FEATURES.md",
    "IMPLEMENTATION_CHECKLIST.md",
    "IMPLEMENTATION_COMPLETE.md",
    "ENHANCEMENTS.md",
    "FEATURES_IMPLEMENTATION.md",
    "PROJECT_REVIEW.md",
    "MOBILE_APP_FLUTTER_COMPLETE.md",
]

def cleanup():
    """Remove unnecessary files"""
    project_root = Path(__file__).parent
    
    print("=" * 70)
    print("CLEANUP SCRIPT - REMOVING UNNECESSARY FILES")
    print("=" * 70)
    
    deleted_count = 0
    kept_count = 0
    
    for filename in FILES_TO_DELETE:
        file_path = project_root / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"✓ DELETED: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ ERROR deleting {filename}: {e}")
        else:
            print(f"  SKIPPED: {filename} (not found)")
    
    print("\n" + "=" * 70)
    print("IMPORTANT FILES KEPT:")
    print("=" * 70)
    
    for filename in sorted(FILES_TO_KEEP):
        file_path = project_root / filename
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"✓ KEPT: {filename:.<45} ({size_kb:>6.1f} KB)")
            kept_count += 1
    
    print("\n" + "=" * 70)
    print(f"CLEANUP SUMMARY")
    print("=" * 70)
    print(f"✓ Deleted unnecessary files: {deleted_count}")
    print(f"✓ Kept important files: {kept_count}")
    print(f"✓ Total cleanup: COMPLETE")
    print("\n✓ Reduced project size significantly!")
    print("✓ Only essential documentation remains!")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    cleanup()
