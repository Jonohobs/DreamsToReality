---
description: Save all progress to GitHub at end of session
---

# Save Progress

Run this at the end of any coding session to avoid losing work.

// turbo-all

1. Stage all changes:
```powershell
git add -A
```

2. Commit with timestamp:
```powershell
git commit -m "Session save: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
```

3. Push to GitHub:
```powershell
git push
```

4. Confirm status is clean:
```powershell
git status
```
