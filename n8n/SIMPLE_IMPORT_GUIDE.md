# PLAYALTER N8N Workflows - Simple Import Guide

## Prerequisites
- N8N running at http://localhost:5678
- .env file with API keys configured
- Admin access to N8N interface

## Workflow Files to Import
✅ **replicate-mask-workflow.json** - Face mask generation  
✅ **agora-stream-workflow.json** - Real-time streaming  
✅ **agent-orchestrate-workflow.json** - AI agent orchestration  
✅ **platform-sync-workflow.json** - Platform health monitoring  

## Step 1: Import Workflows

1. **Open N8N**: Navigate to http://localhost:5678
2. **Go to Workflows**: Click "Workflows" in sidebar
3. **Import Each File**:
   - Click "Import from File"
   - Select workflow JSON file
   - Click "Import"
   - Click "Save"

**Import Order** (recommended):
1. `replicate-mask-workflow.json`
2. `agora-stream-workflow.json`  
3. `agent-orchestrate-workflow.json`
4. `platform-sync-workflow.json`

## Step 2: Setup Credentials

### OpenAI Credential
```
Credentials → Create New → "OpenAI API"
Name: PLAYALTER-OpenAI
API Key: ${OPENAI_API_KEY}
```

### Replicate Credential  
```
Credentials → Create New → "HTTP Header Auth"
Name: PLAYALTER-Replicate
Header: Authorization
Value: Token ${REPLICATE_API_TOKEN}
```

### Agora Credential
```
Credentials → Create New → "Generic Credential Type"
Name: PLAYALTER-Agora
Fields:
- app_id: ${AGORA_APP_ID}
- app_certificate: ${AGORA_APP_CERTIFICATE}
```

### Stripe Credential
```
Credentials → Create New → "Stripe API"
Name: PLAYALTER-Stripe
Secret Key: ${STRIPE_SECRET_KEY}
```

## Step 3: Configure Environment Variables

Set these in N8N Settings → Environment Variables:
```
OPENAI_API_KEY=sk-your-key-here
REPLICATE_API_TOKEN=r8_your-token-here
AGORA_APP_ID=your-app-id-here
AGORA_APP_CERTIFICATE=your-certificate-here
STRIPE_SECRET_KEY=sk_your-key-here
VERCEL_TOKEN=your-vercel-token-here
```

## Step 4: Activate Workflows

1. **Open each workflow**
2. **Toggle "Active" switch** to ON (green)
3. **Verify webhook URLs** are set correctly
4. **Test webhook endpoints**

## Step 5: Test Workflows

### Test Replicate Mask Workflow
```bash
curl -X POST http://localhost:5678/webhook/replicate-mask \
  -H "Content-Type: application/json" \
  -d '{"input_image": "data:image/jpeg;base64,...", "face_style": "realistic"}'
```

### Test Agent Orchestration
```bash
curl -X POST http://localhost:5678/webhook/agent-orchestrate \
  -H "Content-Type: application/json" \
  -d '{"type": "face_processing", "face_mask": true, "stream_required": true}'
```

## Expected Results
- ✅ All 4 workflows imported successfully
- ✅ Credentials configured and working
- ✅ Webhooks responding to test requests
- ✅ Environment variables loaded
- ✅ Workflows showing "Active" status

## Quick Verification
1. **Workflows page**: Shows 4 PLAYALTER workflows
2. **Credentials page**: Shows 4 configured credentials  
3. **Executions page**: Shows successful test runs
4. **Settings**: Environment variables populated

## Troubleshooting
- **Import errors**: Check JSON file syntax
- **Credential issues**: Verify API keys in .env
- **Webhook 404**: Ensure workflows are active
- **Permission errors**: Check N8N user permissions

Workflows ready for import.
