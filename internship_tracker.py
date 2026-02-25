import json
import os
from datetime import datetime, timedelta
from collections import Counter

# Data stored - json file
DATA_FILE = "internships.json"

# ROle names
ROLE_SKILLS = {
    "Software Development": ["Python", "Java", "C++", "JavaScript", "Git"],
    "Data Science": ["Python", "Machine Learning", "Statistics", "SQL", "Data Analysis"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Mobile Development": ["Java", "Kotlin", "Swift", "React Native", "Flutter"],
    "DevOps": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD"],
    "Machine Learning": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning"],
    "Backend Development": ["Python", "Java", "Node.js", "SQL", "REST API"],
    "Frontend Development": ["HTML", "CSS", "JavaScript", "React", "Vue.js"],
    "Data Analysis": ["Python", "SQL", "Excel", "Data Visualization", "Statistics"],
    "Cybersecurity": ["Network Security", "Cryptography", "Ethical Hacking", "Linux", "Security Tools"]
}

class InternshipTracker:
    def __init__(self):
        self.internships = self.load_data()
    
    def load_data(self):
        """Grab all the internship data from our JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_data(self):
        """Save all our internship data - don't wanna lose anything!"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.internships, f, indent=4)
    
    def add_internship(self):
        """Time to add a new internship to track!"""
        print("\n" + "="*50)
        print("ADD NEW INTERNSHIP")
        print("="*50)
        
        internship = {}
        internship['id'] = len(self.internships) + 1
        internship['company'] = input("Company Name: ").strip()
        internship['role'] = input("Role/Position: ").strip()
        internship['location'] = input("Location: ").strip()
        internship['stipend'] = input("Stipend (e.g., 10000 or Unpaid): ").strip()
        internship['duration'] = input("Duration (e.g., 3 months): ").strip()
        
        # skill selection
        print("Skills Required (comma-separated): ", end="")
        skills_input = input().strip()
        internship['skills'] = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        
        internship['status'] = 'Not Applied'
        internship['date_added'] = datetime.now().strftime("%Y-%m-%d")
        
        # Deadline tracker
        deadline_input = input("Application Deadline (YYYY-MM-DD) [optional]: ").strip()
        if deadline_input:
            try:
                
                datetime.strptime(deadline_input, "%Y-%m-%d")
                internship['deadline'] = deadline_input
            except ValueError:
                print("⚠️ Invalid date format. Deadline not set.")
                internship['deadline'] = ""
        else:
            internship['deadline'] = ""
        
        internship['notes'] = input("Notes (optional): ").strip()
        
        self.internships.append(internship)
        self.save_data()
        
        print("\n✓ Internship added successfully!")
        print(f"ID: {internship['id']} - {internship['role']} at {internship['company']}")
    
    def view_all_internships(self):
        """Let's see everything you've got saved!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*100)
        print("ALL INTERNSHIPS")
        print("="*100)
        
        for internship in self.internships:
            print(f"\nID: {internship['id']}")
            print(f"Company: {internship['company']}")
            print(f"Role: {internship['role']}")
            print(f"Location: {internship['location']}")
            print(f"Stipend: {internship['stipend']}")
            print(f"Duration: {internship['duration']}")
            print(f"Skills: {', '.join(internship['skills'])}")
            print(f"Status: {internship['status']}")
            print(f"Date Added: {internship['date_added']}")
            if internship.get('deadline'):
                deadline_str = internship['deadline']
                try:
                    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")
                    days_left = (deadline_date - datetime.now()).days
                    if days_left < 0:
                        print(f"Deadline: {deadline_str} ⚠️ OVERDUE by {abs(days_left)} days")
                    elif days_left == 0:
                        print(f"Deadline: {deadline_str} 🔥 TODAY!")
                    elif days_left <= 3:
                        print(f"Deadline: {deadline_str} ⏰ {days_left} days left")
                    else:
                        print(f"Deadline: {deadline_str} ({days_left} days left)")
                except:
                    print(f"Deadline: {deadline_str}")
            if internship.get('notes'):
                print(f"Notes: {internship['notes']}")
            print("-" * 100)
    
    def update_status(self):
        """Change where you're at with an internship - applied? interviewed? accepted?"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*50)
        print("UPDATE INTERNSHIP STATUS")
        print("="*50)
        
        # internships
        for internship in self.internships:
            print(f"ID: {internship['id']} - {internship['role']} at {internship['company']} (Current: {internship['status']})")
        
        try:
            intern_id = int(input("\nEnter Internship ID to update: "))
            internship = next((i for i in self.internships if i['id'] == intern_id), None)
            
            if not internship:
                print("❌ Invalid ID!")
                return
            
            print("\nStatus Options:")
            statuses = ['Not Applied', 'Applied', 'Interview Scheduled', 'Interview Completed', 
                       'Accepted', 'Rejected', 'Withdrawn']
            for idx, status in enumerate(statuses, 1):
                print(f"{idx}. {status}")
            
            choice = int(input("\nSelect status (1-7): "))
            if 1 <= choice <= len(statuses):
                old_status = internship['status']
                internship['status'] = statuses[choice - 1]
                internship['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data()
                print(f"\n✓ Status updated from '{old_status}' to '{internship['status']}'")
            else:
                print("❌ Invalid choice!")
        
        except ValueError:
            print("❌ Invalid input!")
    
    def show_statistics(self):
        """Let's crunch some numbers and see how you're doing!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*50)
        print("INTERNSHIP STATISTICS")
        print("="*50)
        
        # intrenships enrolled
        print(f"\n📊 Total Internships: {len(self.internships)}")
        
        
        status_count = Counter(i['status'] for i in self.internships)
        print("\n📈 Status Breakdown:")
        for status, count in status_count.items():
            percentage = (count / len(self.internships)) * 100
            print(f"   {status}: {count} ({percentage:.1f}%)")
        
        # internship interests
        company_count = Counter(i['company'] for i in self.internships)
        print("\n🏢 Top Companies:")
        for company, count in company_count.most_common(5):
            print(f"   {company}: {count}")
        
        # trending skills
        all_skills = []
        for internship in self.internships:
            all_skills.extend(internship['skills'])
        skill_count = Counter(all_skills)
        print("\n💡 Most Required Skills:")
        for skill, count in skill_count.most_common(10):
            print(f"   {skill}: {count}")
        
        # achievement tracker
        accepted = status_count.get('Accepted', 0)
        applied = sum(status_count.get(s, 0) for s in ['Applied', 'Interview Scheduled', 
                                                         'Interview Completed', 'Accepted', 'Rejected'])
        if applied > 0:
            success_rate = (accepted / applied) * 100
            print(f"\n✨ Success Rate: {success_rate:.1f}% ({accepted} accepted out of {applied} applied)")
    
    def skill_based_suggestion(self):
        """Tell me what you know, and I'll suggest some cool roles for you!"""
        print("\n" + "="*50)
        print("SKILL-BASED ROLE SUGGESTION")
        print("="*50)
        
        print("\nEnter your skills (comma-separated): ", end="")
        user_skills_input = input().strip()
        user_skills = set(skill.strip().lower() for skill in user_skills_input.split(',') if skill.strip())
        
        if not user_skills:
            print("❌ No skills entered!")
            return
        
        print(f"\n🎯 Your Skills: {', '.join(sorted(user_skills))}")
        print("\n" + "="*50)
        print("RECOMMENDED ROLES")
        print("="*50)
        
        # recommending roles
        role_matches = []
        for role, required_skills in ROLE_SKILLS.items():
            required_skills_lower = set(skill.lower() for skill in required_skills)
            matching_skills = user_skills.intersection(required_skills_lower)
            match_percentage = (len(matching_skills) / len(required_skills_lower)) * 100
            
            if match_percentage > 0:
                role_matches.append({
                    'role': role,
                    'match': match_percentage,
                    'matching_skills': matching_skills,
                    'required_skills': required_skills_lower
                })
        
        # recommendation
        role_matches.sort(key=lambda x: x['match'], reverse=True)
        
        if not role_matches:
            print("\n❌ No matching roles found. Try adding more relevant skills!")
            return
        
        
        for idx, match in enumerate(role_matches[:5], 1):
            print(f"\n{idx}. {match['role']}")
            print(f"   Match: {match['match']:.1f}%")
            print(f"   ✓ You have: {', '.join(sorted(match['matching_skills']))}")
            missing = match['required_skills'] - match['matching_skills']
            if missing:
                print(f"   ✗ Consider learning: {', '.join(sorted(missing))}")
        
        
        print("\n" + "="*50)
        print("MATCHING INTERNSHIPS FROM YOUR LIST")
        print("="*50)
        
        matching_internships = []
        for internship in self.internships:
            internship_skills = set(skill.lower() for skill in internship['skills'])
            matching = user_skills.intersection(internship_skills)
            if matching:
                match_pct = (len(matching) / len(internship_skills)) * 100 if internship_skills else 0
                matching_internships.append({
                    'internship': internship,
                    'match': match_pct,
                    'matching_skills': matching
                })
        
        matching_internships.sort(key=lambda x: x['match'], reverse=True)
        
        if matching_internships:
            for idx, match in enumerate(matching_internships[:5], 1):
                internship = match['internship']
                print(f"\n{idx}. {internship['role']} at {internship['company']}")
                print(f"   Match: {match['match']:.1f}%")
                print(f"   Matching Skills: {', '.join(sorted(match['matching_skills']))}")
                print(f"   Status: {internship['status']}")
        else:
            print("\nNo matching internships in your list yet!")
    
    def search_filter(self):
        """Looking for something specific? Let's find it!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*50)
        print("SEARCH & FILTER INTERNSHIPS")
        print("="*50)
        print("\n1. Search by Company Name")
        print("2. Search by Role")
        print("3. Filter by Status")
        print("4. Filter by Location")
        print("5. Search by Skill")
        print("6. Show Upcoming Deadlines")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        results = []
        
        if choice == '1':
            search_term = input("\nEnter company name: ").strip().lower()
            results = [i for i in self.internships if search_term in i['company'].lower()]
        
        elif choice == '2':
            search_term = input("\nEnter role/position: ").strip().lower()
            results = [i for i in self.internships if search_term in i['role'].lower()]
        
        elif choice == '3':
            print("\nStatuses: Not Applied, Applied, Interview Scheduled, Interview Completed, Accepted, Rejected, Withdrawn")
            status = input("Enter status: ").strip()
            results = [i for i in self.internships if i['status'].lower() == status.lower()]
        
        elif choice == '4':
            location = input("\nEnter location: ").strip().lower()
            results = [i for i in self.internships if location in i['location'].lower()]
        
        elif choice == '5':
            skill = input("\nEnter skill: ").strip().lower()
            results = [i for i in self.internships if any(skill in s.lower() for s in i['skills'])]
        
        elif choice == '6':
            self.show_upcoming_deadlines()
            return
        
        elif choice == '7':
            return
        
        else:
            print("❌ Invalid choice!")
            return
        
        
        if results:
            print(f"\n✓ Found {len(results)} matching internship(s):\n")
            print("=" * 100)
            for internship in results:
                print(f"\nID: {internship['id']}")
                print(f"Company: {internship['company']}")
                print(f"Role: {internship['role']}")
                print(f"Location: {internship['location']}")
                print(f"Stipend: {internship['stipend']}")
                print(f"Duration: {internship['duration']}")
                print(f"Skills: {', '.join(internship['skills'])}")
                print(f"Status: {internship['status']}")
                print(f"Date Added: {internship['date_added']}")
                if internship.get('deadline'):
                    print(f"Deadline: {internship['deadline']}")
                if internship.get('notes'):
                    print(f"Notes: {internship['notes']}")
                print("-" * 100)
        else:
            print("\n❌ No matching internships found!")
    
    def show_upcoming_deadlines(self):
        """Don't miss those deadlines! Let's see what's coming up"""
        print("\n" + "="*50)
        print("UPCOMING DEADLINES")
        print("="*50)
        
        # Filtering deadline internships
        internships_with_deadlines = [i for i in self.internships if i.get('deadline')]
        
        if not internships_with_deadlines:
            print("\n❌ No internships with deadlines set!")
            return
        
        # Sorting by date so we see the urgent ones first
        try:
            internships_with_deadlines.sort(key=lambda x: datetime.strptime(x['deadline'], "%Y-%m-%d"))
        except:
            pass
        
        today = datetime.now()
        overdue = []
        upcoming = []
        future = []
        
        for internship in internships_with_deadlines:
            try:
                deadline_date = datetime.strptime(internship['deadline'], "%Y-%m-%d")
                days_left = (deadline_date - today).days
                
                if days_left < 0:
                    overdue.append((internship, days_left))
                elif days_left <= 7:
                    upcoming.append((internship, days_left))
                else:
                    future.append((internship, days_left))
            except:
                continue
        
        # deadlines
        if overdue:
            print("\n🚨 OVERDUE:")
            for internship, days in overdue:
                print(f"   ID {internship['id']}: {internship['role']} at {internship['company']}")
                print(f"   Deadline: {internship['deadline']} (Overdue by {abs(days)} days)")
                print(f"   Status: {internship['status']}")
                print()
        
        # upcoming ones
        if upcoming:
            print("\n⏰ UPCOMING (Next 7 Days):")
            for internship, days in upcoming:
                urgency = "🔥 TODAY!" if days == 0 else f"{days} day{'s' if days != 1 else ''} left"
                print(f"   ID {internship['id']}: {internship['role']} at {internship['company']}")
                print(f"   Deadline: {internship['deadline']} ({urgency})")
                print(f"   Status: {internship['status']}")
                print()
        
        # furutre deadlines
        if future:
            print("\n📅 FUTURE DEADLINES:")
            for internship, days in future[:5]:  # Just showing the first 5 to keep it clean
                print(f"   ID {internship['id']}: {internship['role']} at {internship['company']}")
                print(f"   Deadline: {internship['deadline']} ({days} days left)")
                print(f"   Status: {internship['status']}")
                print()
    
    def edit_internship(self):
        """Made a mistake or got new info? Let's fix it up!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*50)
        print("EDIT INTERNSHIP")
        print("="*50)
        
        # Pick which one you wanna edit
        for internship in self.internships:
            print(f"ID: {internship['id']} - {internship['role']} at {internship['company']}")
        
        try:
            intern_id = int(input("\nEnter Internship ID to edit: "))
            internship = next((i for i in self.internships if i['id'] == intern_id), None)
            
            if not internship:
                print("❌ Invalid ID!")
                return
            
            print("\nWhat would you like to edit?")
            print("1. Company Name")
            print("2. Role/Position")
            print("3. Location")
            print("4. Stipend")
            print("5. Duration")
            print("6. Skills")
            print("7. Deadline")
            print("8. Notes")
            print("9. Cancel")
            
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                new_value = input(f"Current Company: {internship['company']}\nNew Company: ").strip()
                if new_value:
                    internship['company'] = new_value
            
            elif choice == '2':
                new_value = input(f"Current Role: {internship['role']}\nNew Role: ").strip()
                if new_value:
                    internship['role'] = new_value
            
            elif choice == '3':
                new_value = input(f"Current Location: {internship['location']}\nNew Location: ").strip()
                if new_value:
                    internship['location'] = new_value
            
            elif choice == '4':
                new_value = input(f"Current Stipend: {internship['stipend']}\nNew Stipend: ").strip()
                if new_value:
                    internship['stipend'] = new_value
            
            elif choice == '5':
                new_value = input(f"Current Duration: {internship['duration']}\nNew Duration: ").strip()
                if new_value:
                    internship['duration'] = new_value
            
            elif choice == '6':
                print(f"Current Skills: {', '.join(internship['skills'])}")
                new_value = input("New Skills (comma-separated): ").strip()
                if new_value:
                    internship['skills'] = [skill.strip() for skill in new_value.split(',') if skill.strip()]
            
            elif choice == '7':
                current_deadline = internship.get('deadline', 'Not set')
                new_value = input(f"Current Deadline: {current_deadline}\nNew Deadline (YYYY-MM-DD): ").strip()
                if new_value:
                    try:
                        datetime.strptime(new_value, "%Y-%m-%d")
                        internship['deadline'] = new_value
                    except ValueError:
                        print("⚠️ Invalid date format. Deadline not updated.")
                        return
            
            elif choice == '8':
                current_notes = internship.get('notes', 'None')
                new_value = input(f"Current Notes: {current_notes}\nNew Notes: ").strip()
                internship['notes'] = new_value
            
            elif choice == '9':
                print("\n❌ Edit cancelled.")
                return
            
            else:
                print("❌ Invalid choice!")
                return
            
            internship['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
            print("\n✓ Internship updated successfully!")
        
        except ValueError:
            print("❌ Invalid input!")
    
    def delete_internship(self):
        """Getting rid of one? No worries, we got you!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*50)
        print("DELETE INTERNSHIP")
        print("="*50)
        
       
        for internship in self.internships:
            print(f"ID: {internship['id']} - {internship['role']} at {internship['company']}")
        
        try:
            intern_id = int(input("\nEnter Internship ID to delete: "))
            internship = next((i for i in self.internships if i['id'] == intern_id), None)
            
            if not internship:
                print("❌ Invalid ID!")
                return
            
            # delete funct
            print(f"\n⚠️ Are you sure you want to delete:")
            print(f"   {internship['role']} at {internship['company']}?")
            confirm = input("\nType 'yes' to confirm: ").strip().lower()
            
            if confirm == 'yes':
                self.internships.remove(internship)
                
                for idx, intern in enumerate(self.internships, 1):
                    intern['id'] = idx
                self.save_data()
                print("\n✓ Internship deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")
        
        except ValueError:
            print("❌ Invalid input!")
    
    def smart_advisor(self):
        """AI-powered advisor that analyzes your internships and gives smart recommendations!"""
        if not self.internships:
            print("\n❌ No internships found. Add some first!")
            return
        
        print("\n" + "="*60)
        print("🤖 SMART APPLICATION ADVISOR (AI-Powered)")
        print("="*60)
        print("\nAnalyzing your internships and generating recommendations...\n")
        
        # Calculate scores for each internship
        scored_internships = []
        
        for internship in self.internships:
            score = 0
            reasons = []
            
            # Skip if already accepted or rejected
            if internship['status'] in ['Accepted', 'Rejected']:
                continue
            
            # Factor 1: Deadline urgency (0-30 points)
            if internship.get('deadline'):
                try:
                    deadline_date = datetime.strptime(internship['deadline'], "%Y-%m-%d")
                    days_left = (deadline_date - datetime.now()).days
                    
                    if days_left < 0:
                        score += 5
                        reasons.append("⚠️ Overdue - apply ASAP if still interested")
                    elif days_left == 0:
                        score += 30
                        reasons.append("🔥 Deadline is TODAY - urgent!")
                    elif days_left <= 3:
                        score += 25
                        reasons.append(f"⏰ Only {days_left} days left - very urgent")
                    elif days_left <= 7:
                        score += 20
                        reasons.append(f"📌 {days_left} days left - should apply soon")
                    elif days_left <= 14:
                        score += 15
                        reasons.append(f"📅 {days_left} days left - good time to apply")
                    else:
                        score += 10
                except:
                    pass
            
            # Factor 2: Application status (0-25 points)
            if internship['status'] == 'Not Applied':
                score += 25
                reasons.append("✨ Haven't applied yet - fresh opportunity")
            elif internship['status'] == 'Applied':
                score += 15
                reasons.append("📬 Already applied - might want to follow up")
            elif internship['status'] == 'Interview Scheduled':
                score += 30
                reasons.append("💼 Interview coming up - prep time!")
            elif internship['status'] == 'Interview Completed':
                score += 20
                reasons.append("🤞 Waiting for response - consider follow-up")
            
            # Factor 3: Skill requirements (0-20 points)
            if len(internship['skills']) <= 3:
                score += 20
                reasons.append("💪 Fewer skills required - good match potential")
            elif len(internship['skills']) <= 5:
                score += 15
            else:
                score += 10
            
            # Factor 4: Stipend value (0-15 points) - higher stipend = higher priority
            stipend_str = internship['stipend'].lower()
            if 'unpaid' in stipend_str or stipend_str == '0':
                score += 5
            else:
                # Try to extract numbers and score based on amount
                import re
                numbers = re.findall(r'\d+', stipend_str)
                if numbers:
                    amount = int(numbers[0])
                    if amount >= 50000:
                        score += 15
                        reasons.append("💰 Great stipend - high value opportunity")
                    elif amount >= 20000:
                        score += 12
                        reasons.append("💵 Good stipend offered")
                    else:
                        score += 8
            
            # Factor 5: How long it's been in your list (0-10 points)
            try:
                date_added = datetime.strptime(internship['date_added'], "%Y-%m-%d")
                days_in_list = (datetime.now() - date_added).days
                
                if days_in_list >= 30:
                    score += 10
                    reasons.append("⌛ Been in your list for a while - time to act")
                elif days_in_list >= 14:
                    score += 5
            except:
                pass
            
            scored_internships.append({
                'internship': internship,
                'score': score,
                'reasons': reasons
            })
        
        # Sort by score (highest first)
        scored_internships.sort(key=lambda x: x['score'], reverse=True)
        
        if not scored_internships:
            print("\n✨ All caught up! No pending applications to prioritize.")
            print("Either everything's been accepted/rejected, or you need to add more internships.")
            return
        
        # Display top recommendations
        print("\n" + "="*60)
        print("🎯 TOP PRIORITY APPLICATIONS")
        print("="*60)
        
        for idx, item in enumerate(scored_internships[:5], 1):
            internship = item['internship']
            score = item['score']
            reasons = item['reasons']
            
            # Determine priority level
            if score >= 70:
                priority = "🔴 CRITICAL"
            elif score >= 50:
                priority = "🟠 HIGH"
            elif score >= 30:
                priority = "🟡 MEDIUM"
            else:
                priority = "🟢 LOW"
            
            print(f"\n{idx}. {internship['role']} at {internship['company']}")
            print(f"   Priority: {priority} (Score: {score}/100)")
            print(f"   Status: {internship['status']}")
            if internship.get('deadline'):
                print(f"   Deadline: {internship['deadline']}")
            print(f"   Location: {internship['location']}")
            print(f"   \n   Why prioritize this:")
            for reason in reasons:
                print(f"      • {reason}")
        
        # Generate personalized insights
        print("\n" + "="*60)
        print("💡 PERSONALIZED INSIGHTS")
        print("="*60)
        
        # Analyze application patterns
        total = len(self.internships)
        not_applied = len([i for i in self.internships if i['status'] == 'Not Applied'])
        applied = len([i for i in self.internships if i['status'] == 'Applied'])
        interviews = len([i for i in self.internships if i['status'] in ['Interview Scheduled', 'Interview Completed']])
        accepted = len([i for i in self.internships if i['status'] == 'Accepted'])
        rejected = len([i for i in self.internships if i['status'] == 'Rejected'])
        
        print(f"\n📊 Your Application Pipeline:")
        print(f"   • Total tracked: {total}")
        print(f"   • Not applied yet: {not_applied}")
        print(f"   • Applied: {applied}")
        print(f"   • In interview stage: {interviews}")
        print(f"   • Accepted: {accepted}")
        print(f"   • Rejected: {rejected}")
        
        # Give actionable advice
        print(f"\n🎯 Recommended Actions:")
        
        if not_applied > 10:
            print(f"   • You have {not_applied} pending applications - try to apply to 2-3 per day")
        elif not_applied > 0:
            print(f"   • Focus on completing your {not_applied} pending applications")
        
        if applied > 0 and interviews == 0:
            print(f"   • Consider following up on your {applied} applications")
        
        if interviews > 0:
            print(f"   • 💼 Prep for your {interviews} upcoming/completed interviews!")
        
        if total > 0:
            conversion_rate = (accepted / total) * 100 if total > 0 else 0
            if conversion_rate > 20:
                print(f"   • 🎉 Great job! {conversion_rate:.1f}% acceptance rate is solid!")
            elif conversion_rate > 10:
                print(f"   • 👍 Decent {conversion_rate:.1f}% acceptance rate - keep going!")
            else:
                print(f"   • Keep applying! More applications = better chances")
        
        # Check for overdue deadlines
        overdue = 0
        for internship in self.internships:
            if internship.get('deadline'):
                try:
                    deadline_date = datetime.strptime(internship['deadline'], "%Y-%m-%d")
                    if (deadline_date - datetime.now()).days < 0:
                        overdue += 1
                except:
                    pass
        
        if overdue > 0:
            print(f"   • ⚠️ You have {overdue} overdue deadline(s) - check if applications are still open")
        
        print("\n" + "="*60)
        print("💪 Keep hustling! You've got this!")
        print("="*60)

def display_menu():
    """Show the main menu - what do you wanna do today?"""
    print("\n" + "="*50)
    print("🎓 INTERNSHIP TRACKER")
    print("="*50)
    print("1. Add Internship")
    print("2. View All Internships")
    print("3. Search & Filter")
    print("4. Edit Internship")
    print("5. Delete Internship")
    print("6. Update Status")
    print("7. Show Statistics")
    print("8. Show Upcoming Deadlines")
    print("9. Skill-Based Role Suggestion")
    print("10. 🤖 Smart Application Advisor (AI)")
    print("11. Exit")
    print("="*50)

def main():
    tracker = InternshipTracker()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            tracker.add_internship()
        elif choice == '2':
            tracker.view_all_internships()
        elif choice == '3':
            tracker.search_filter()
        elif choice == '4':
            tracker.edit_internship()
        elif choice == '5':
            tracker.delete_internship()
        elif choice == '6':
            tracker.update_status()
        elif choice == '7':
            tracker.show_statistics()
        elif choice == '8':
            tracker.show_upcoming_deadlines()
        elif choice == '9':
            tracker.skill_based_suggestion()
        elif choice == '10':
            tracker.smart_advisor()
        elif choice == '11':
            print("\n👋 Thank you for using Internship Tracker!")
            print("Good luck with your internship applications! 🚀")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 11.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
