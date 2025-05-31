import csv
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta, timezone

# Helper to parse ISO timestamps (with or without timezone)
def parse_iso(ts):
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        if ts.endswith('Z'):
            return datetime.fromisoformat(ts[:-1]).replace(tzinfo=timezone.utc)
        raise

user_action_counts = Counter()
user_action_timestamps = defaultdict(list)

with open('activity.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = parse_iso(row['timestamp'])
        user = row['user_id']
        action = row['action']
        user_action_counts[user] += 1
        user_action_timestamps[(user, action)].append(ts)

print("Top 5 users by action count:")
for user, count in user_action_counts.most_common(5):
    print(f"  {user}: {count} actions")
print()

print("Users with >10 same actions in any 5-minute window:")
for (user, action), timestamps in user_action_timestamps.items():
    timestamps.sort()
    window = deque()
    for ts in timestamps:
        window.append(ts)
        while (window[-1] - window[0]) > timedelta(minutes=5):
            window.popleft()
        if len(window) > 10:
            print(f"  User '{user}' performed '{action}' {len(window)} times between {window[0]} and {window[-1]}")
            break  # Only report first occurrence per user/action 