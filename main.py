import re
import threading
import time
import json
from datetime import datetime

# Import your check_card function from p.py
from p import check_card

# ---------------- Helper Functions ---------------- #

def load_auth():
    """Load authorized users (kept for compatibility)"""
    try:
        with open("authorized.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_auth(data):
    """Save authorized users (kept for compatibility)"""
    with open("authorized.json", "w") as f:
        json.dump(data, f)

def normalize_card(text):
    """
    Normalize credit card from any format to cc|mm|yy|cvv
    Similar to PHP normalize_card function
    """
    if not text:
        return None

    # Replace newlines and slashes with spaces
    text = text.replace('\n', ' ').replace('/', ' ')

    # Find all numbers in the text
    numbers = re.findall(r'\d+', text)

    cc = mm = yy = cvv = ''

    for part in numbers:
        if len(part) == 16:  # Credit card number
            cc = part
        elif len(part) == 4 and part.startswith('20'):  # 4-digit year starting with 20
            yy = part
        elif len(part) == 2 and int(part) <= 12 and mm == '':  # Month (2 digits <= 12)
            mm = part
        elif len(part) == 2 and not part.startswith('20') and yy == '':  # 2-digit year
            yy = '20' + part
        elif len(part) in [3, 4] and cvv == '':  # CVV (3-4 digits)
            cvv = part

    # Check if we have all required parts
    if cc and mm and yy and cvv:
        return f"{cc}|{mm}|{yy}|{cvv}"

    return None

def extract_cc_from_text(text):
    """Extract CCs from text using improved normalization"""
    cc_lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Try to normalize each line
        normalized_cc = normalize_card(line)
        if normalized_cc:
            cc_lines.append(normalized_cc)
        else:
            # Fallback to original regex patterns
            found = re.findall(r'\b(?:\d[ -]*?){13,16}\b.*?\|.*?\|.*?\|.*', line)
            if found:
                cc_lines.extend(found)
            else:
                parts = re.findall(r'\d{12,16}[|: -]\d{1,2}[|: -]\d{2,4}[|: -]\d{3,4}', line)
                cc_lines.extend(parts)
    
    return cc_lines

def single_check():
    """Check a single credit card"""
    print("\n" + "✦"*10 + "[ SINGLE CARD CHECK ]" + "✦"*10)
    print("\nEnter credit card details in any format:")
    print("Examples:")
    print("4556737586899855|12|2026|123")
    print("4556 7375 8689 9855 12/26 123")
    print("4556737586899855 12 2026 123")
    
    user_input = input("\nEnter card details: ").strip()
    
    if not user_input:
        print("❌ No input provided!")
        return
    
    # Try to normalize the input
    cc = normalize_card(user_input)
    
    # If normalization failed, use the original input
    if not cc:
        if re.match(r'^\d{16}\|\d{2}\|\d{2,4}\|\d{3,4}$', user_input):
            cc = user_input
        else:
            print("❌ Invalid card format!")
            print("Please use format: 4556737586899855|12|2026|123")
            return
    
    print("\n✦━━━[ PROCESSING ]━━━✦")
    print("Your card is being checked...")
    print("Please wait a few seconds\n")
    
    try:
        result = check_card(cc)
        print("\n" + "="*50)
        print("RESULT:")
        print("="*50)
        print(result)
        print("="*50)
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def bulk_check():
    """Check multiple credit cards from file or text input"""
    print("\n" + "✦"*10 + "[ BULK CARD CHECK ]" + "✦"*10)
    print("\nChoose input method:")
    print("1. Load from file (cc.txt)")
    print("2. Paste cards directly")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    cc_lines = []
    
    if choice == "1":
        # Load from file
        filename = input("Enter filename (e.g., cards.txt): ").strip()
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            cc_lines = extract_cc_from_text(text)
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
            return
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
            
    elif choice == "2":
        # Paste cards directly
        print("\nPaste your cards (one per line):")
        print("Press Ctrl+D (Linux/Mac) or Ctrl+Z then Enter (Windows) to finish")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        text = '\n'.join(lines)
        cc_lines = extract_cc_from_text(text)
        
    else:
        print("❌ Invalid choice!")
        return
    
    if not cc_lines:
        print("\n✦━━━[ ⚠️ NO VALID CARDS FOUND ]━━━✦")
        print("No valid credit cards detected in the input")
        print("Please make sure the cards are in correct format")
        print("\nCorrect format:")
        print("4556737586899855|12|2026|123")
        return
    
    total = len(cc_lines)
    print(f"\nFound {total} valid card(s) to check")
    
    if choice == "2" and total > 15:
        print("\n✦━━━[ ⚠️ LIMIT EXCEEDED ]━━━✦")
        print("Only 15 cards allowed in raw paste")
        print("For more cards, please use a .txt file")
        return
    
    print("\n✦━━━[ MASS CHECK STARTED ]━━━✦")
    print("Processing your cards...")
    print("Please wait a few moments\n")
    
    approved = []
    declined = 0
    checked = 0
    
    # Create results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_filename = f"check_results_{timestamp}.txt"
    
    with open(results_filename, 'w', encoding='utf-8') as results_file:
        results_file.write(f"CC Check Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        results_file.write("="*50 + "\n\n")
        
        for i, cc in enumerate(cc_lines, 1):
            try:
                checked += 1
                cc = cc.strip()
                print(f"Checking card {i}/{total}: {cc.split('|')[0]}...")
                
                result = check_card(cc)
                
                # Write to results file
                results_file.write(f"Card {i}: {cc}\n")
                results_file.write(f"Result: {result}\n")
                results_file.write("-" * 30 + "\n")
                
                if "[APPROVED]" in result:
                    approved.append((cc, result))
                    print(f"✅ [APPROVED] Card {i}")
                else:
                    declined += 1
                    print(f"❌ [DECLINED] Card {i}")
                
                # Update progress
                print(f"Progress: {checked}/{total} | Approved: {len(approved)} | Declined: {declined}\n")
                
                # Small delay to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error checking card {i}: {e}")
                results_file.write(f"Card {i}: {cc} - ERROR: {e}\n")
                results_file.write("-" * 30 + "\n")
    
    # Final summary
    print("\n" + "✦"*10 + "[ CHECKING COMPLETED ]" + "✦"*10)
    print(f"✓ Total cards processed: {total}")
    print(f"✅ Approved: {len(approved)}")
    print(f"❌ Declined: {declined}")
    print(f"📁 Results saved to: {results_filename}")
    
    # Show approved cards
    if approved:
        print("\n" + "🎉 APPROVED CARDS:")
        print("="*50)
        for cc, result in approved:
            print(f"Card: {cc}")
            # Extract just the important info from result
            lines = result.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['APPROVED', 'Live', 'Status', 'Gateway']):
                    print(f"  {line.strip()}")
            print("-" * 30)
    
    print(f"\nAll results have been saved to '{results_filename}'")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*60)
        print("✦"*10 + " CC CHECKER BULK TOOL " + "✦"*10)
        print("="*60)
        print("\nChoose an option:")
        print("1. Single Card Check")
        print("2. Bulk Check (Multiple Cards)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            single_check()
        elif choice == "2":
            bulk_check()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()