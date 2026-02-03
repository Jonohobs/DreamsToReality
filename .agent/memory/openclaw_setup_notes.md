# OpenClaw Setup Notes
*Saved from Claude Code session - 2026-02-03*

## Decision Summary
- **Goal**: Try OpenClaw cheaply and safely
- **Approach**: Use WSL2 (1-2GB) instead of VirtualBox (25GB was too heavy)
- **Cost**: Free with local Ollama models

## Setup Plan

### Step 1: Install WSL2 (Admin PowerShell)
```powershell
wsl --install -d Ubuntu
```
After reboot, create Ubuntu username/password.

### Step 2: Install OpenClaw
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

### Onboarding Options
- **Gateway**: Local
- **AI Provider**: Ollama (free, local)
- **Chat Platform**: Start with Telegram (easiest)
- **Security**: Accept defaults (DMs require approval codes)

## Security Considerations

> [!CAUTION]
> Recent vulnerabilities - proceed carefully:
> - **CVE-2026-25253**: Critical RCE patched Jan 29, 2026
> - Hundreds of exposed dashboards found with no auth
> - Prompt injection risks if misconfigured

### Recommended Hardening
```bash
# Run security audit
openclaw security audit --deep

# Check paired devices
openclaw pairing list whatsapp
```

### If using Docker
```bash
--read-only --cap-drop=ALL --security-opt=no-new-privileges
```

## Cost Breakdown
| Component | Cost |
|-----------|------|
| OpenClaw | Free |
| Ollama models | Free (already have) |
| Cloud API tokens | $0 with local models |
| Storage | ~1-2GB (WSL2) |

## Resources
- Setup guide: https://claw.openknot.ai/start/getting-started
- Security best practices: https://composio.dev/blog/secure-openclaw-moltbot-clawdbot-setup

## Next Steps
1. ~~Consider waiting 2-4 weeks for security dust to settle~~ (or proceed carefully)
2. Install WSL2 with Ubuntu
3. Install OpenClaw in WSL2
4. Configure with Ollama (local, free)
5. Start with single messaging channel only
