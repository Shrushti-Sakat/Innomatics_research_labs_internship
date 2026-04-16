# STEP-BY-STEP EXECUTION GUIDE
## Running the AI Resume Screening System

### Phase 1: Environment Setup (Do This First!)

#### Step 1: Install Python Dependencies
```bash
cd AI_Resume_screener
pip install -r requirements.txt
```

**What gets installed:**
- langchain (LLM pipeline framework)
- langchain-openai (OpenAI integration)
- langsmith (tracing and debugging)
- jupyter (notebook environment)
- pandas (data handling)

**Expected Output:**
```
Successfully installed langchain langchain-openai langsmith jupyter pandas...
```

#### Step 2: Obtain API Keys

**OpenAI API Key:**
1. Go to: https://platform.openai.com/api-keys
2. Login with your account (create if needed)
3. Click "Create new secret key"
4. Copy the key (shows only once!)
5. Save it somewhere safe

**LangSmith API Key:**
1. Go to: https://smith.langchain.com
2. Create account (GitHub login available)
3. Go to Settings → API Keys
4. Create new API key
5. Copy the key

#### Step 3: Create .env File

Create `.env` file in `AI_Resume_screener` directory:

```
OPENAI_API_KEY=sk-your-key-here-paste-the-full-key
LANGCHAIN_API_KEY=ls_your-key-here-paste-the-full-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Resume_Screening_System
```

**⚠️ IMPORTANT:**
- Keep this file SECRET (in .gitignore)
- Never commit to GitHub
- Never share these keys
- Regenerate if accidentally exposed

---

### Phase 2: Notebook Execution (Main Processing)

#### Step 4: Start Jupyter

```bash
jupyter notebook
```

**What happens:**
- Browser opens automatically
- Jupyter dashboard shows
- Navigate to `AI_Resume_Screening_System.ipynb`
- Click to open the notebook

#### Step 5: Run the Notebook

**Method 1: Run All Cells**
```
Kernel → Restart Kernel and Run All Cells
```

**Method 2: Run Cell by Cell**
```
Cell → Run All
OR
Press Ctrl+A then Shift+Enter
```

**What should happen:**
- Cells execute sequentially
- Green checkmarks appear ✓
- Output displays below each cell
- No error messages (or they're expected errors being demonstrated)

#### Step 6: Monitor Execution

**Cell 1 (Environment Setup)**
```
Expected Output:
✓ Environment Configuration Complete
LangSmith Tracing Enabled: true
LangSmith Project: Resume_Screening_System
```

**Cell 2 (Imports)**
```
Expected Output:
✓ All libraries imported successfully
LangChain and LangSmith loaded for pipeline creation and tracing
```

**Cell 3 (Data Loading)**
```
Expected Output:
✓ Sample Data Loaded
Total Candidates: 3
Candidates: strong, average, weak
```

**Cell 4-5 (Prompt Configuration)**
```
Expected Output:
✓ Prompt Templates Created
✓ Skill Extraction Prompt: Ready
✓ Job Requirement Prompt: Ready
```

**Cell 6 (Chain Building)**
```
Expected Output:
✓ LLM Initialized: gpt-3.5-turbo
✓ Skill Extraction Chain Built (LCEL)
✓ Job Requirement Chain Built (LCEL)
```

**Cells 11-15 (Screening Process)**
```
This section takes the longest (2-5 minutes per candidate)
=================================================================
█ INITIALIZING RESUME SCREENING SYSTEM
=================================================================

STEP 0: EXTRACTING JOB REQUIREMENTS
════════════════════════════════════════════════════════════════
✓ Job Requirements Extracted Successfully

Required Skills: ['Python', 'SQL', 'Machine Learning', ...]
Experience Required: 5+ years

=================================================================
█ RUN 1: STRONG CANDIDATE (John Doe)
=================================================================

[STEP 1/4] Extracting Candidate Skills...
✓ Skills Extracted
  Technical Skills: ['Python', 'R', 'Java']...
  ML Frameworks: ['TensorFlow', 'scikit-learn', ...]...

[STEP 2/4] Matching Skills with Job Requirements...
✓ Matching Analysis Complete
  Matched Required: 8 skills
  Missing Required: 2 skills

[STEP 3/4] Calculating Fit Score...
✓ Score Calculated
  FIT SCORE: 85/100

[STEP 4/4] Generating Explanation & Recommendation...
✓ Explanation Generated
  Recommendation: STRONG PASS

FINAL EVALUATION SUMMARY
────────────────────────────────────────────────────────────────
Candidate: John Doe
Fit Score: 85/100
Recommendation: STRONG PASS
Summary: Strong ML background with 6 years experience...
Next Steps: Schedule technical interview
────────────────────────────────────────────────────────────────
```

**Similarly for Average and Weak candidates...**

#### Step 7: View Results

After all screening completes, you'll see:

**Comparison Table:**
```
Candidate Type  Candidate Name    Fit Score  Recommendation  Matched Required  Missing Required
STRONG          John Doe          85         STRONG PASS     8                 2
AVERAGE         Alice Smith       65         CONSIDER        5                 5
WEAK            Bob Johnson       28         REJECT          1                 9
```

**Output Files:**
```
✓ Results exported to screening_results.json
```

---

### Phase 3: Verify LangSmith Tracing

#### Step 8: Access LangSmith Dashboard

1. **During notebook execution**, LangSmith automatically captures traces
2. Go to: https://smith.langchain.com
3. Login with your credentials
4. Look for project: **Resume_Screening_System**

#### Step 9: Inspect Traces

For each candidate, you should see:

**Trace Structure:**
```
Run 1: Strong Candidate (John Doe)
├─ Skill Extraction
│  ├─ Input: Resume text
│  ├─ Prompt: "Extract all skills..."
│  ├─ LLM Call: gpt-3.5-turbo
│  └─ Output: JSON with skills
├─ Job Requirements
│  ├─ Input: Job description
│  └─ Output: Structured requirements
├─ Matching
│  ├─ Input: both JSON outputs
│  └─ Output: Match analysis
├─ Scoring
│  ├─ Input: Matching analysis
│  └─ Output: Fit score 85/100
└─ Explanation
   ├─ Input: All previous outputs
   └─ Output: Recommendation

Run 2: Average Candidate (Alice Smith)
[Similar structure with different outputs]

Run 3: Weak Candidate (Bob Johnson)
[Similar structure with different outputs]
```

**What to verify:**
- ✓ 3 runs present
- ✓ All 5 steps visible per run
- ✓ Inputs and outputs show proper data flow
- ✓ Token usage reasonable
- ✓ Latency acceptable (1-3 seconds per step)
- ✓ No error traces

---

### Phase 4: Prepare for Submission

#### Step 10: Save Notebook

In Jupyter:
```
File → Save Notebook
```

**Verification:**
- File shows as saved (no asterisk in title)
- All outputs are visible
- All cells have checkmarks ✓

#### Step 11: Capture LangSmith Screenshots

For documentation:

1. **Screenshot 1**: Project overview with 3 runs
   - Location: https://smith.langchain.com
   - Show: All 3 candidates listed

2. **Screenshot 2**: Strong candidate trace
   - Show: Full 5-step pipeline

3. **Screenshot 3**: Trace details
   - Show: Inputs, LLM call, outputs

4. **Screenshot 4**: Results comparison
   - Show: All 3 scores and recommendations

**Save screenshots to project root folder:**
```
AI_Resume_screener/
├── screenshots/
│   ├── langsmith_overview.png
│   ├── strong_candidate_trace.png
│   ├── trace_details.png
│   └── results_comparison.png
```

#### Step 12: Verify All Files

Check directory structure:
```bash
# List all files
ls -la  # or: dir /ah  (Windows)

# Should see:
✓ AI_Resume_Screening_System.ipynb
✓ main.py
✓ requirements.txt
✓ README.md
✓ SUBMISSION_GUIDE.md
✓ .env.example (NOT .env!)
✓ .gitignore
✓ prompts/
✓ chains/
✓ data/
✓ screening_results.json (generated after run)
```

---

### Phase 5: GitHub Submission

#### Step 13: Initialize Git Repository

```bash
cd AI_Resume_screener

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Resume Screening System with LangChain and LangSmith"
```

**Verify:**
- ✓ `.env` file is NOT added (should be in .gitignore)
- ✓ Only necessary files are committed
- ✓ No API keys in any files

#### Step 14: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `AI_Resume_screener`
3. Description: "AI Resume Screening System with LangChain and LangSmith"
4. Make it: **PUBLIC**
5. Create repository

#### Step 15: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/AI_Resume_screener.git

# Rename branch
git branch -M main

# Push
git push -u origin main
```

**Verify:**
- ✓ Files appear on GitHub
- ✓ Repository is PUBLIC
- ✓ README.md displays properly
- ✓ No .env file (API keys not exposed!)

---

### Phase 6: Create LinkedIn Post

#### Step 16: Write LinkedIn Post

Use this template:

```
🚀 Excited to share my latest project: Building an AI Resume Screening System using LangChain & LangSmith!

Project Highlights:
✅ Developed an intelligent ML pipeline for automated resume screening
✅ Implemented skill extraction, matching, and scoring using LLMs
✅ Used LangChain for modular architecture with LCEL
✅ Enabled LangSmith tracing for complete pipeline visibility
✅ Achieved production-ready code with zero hallucinations

The system evaluates candidates against job descriptions and provides:
• Skill extraction from resumes (explicit mentions only)
• Automated skill matching and analysis
• Fit scores (0-100) with clear reasoning
• Explainable recommendations

Technologies: Python, LangChain, LangSmith, OpenAI GPT-3.5-turbo, Jupyter

GitHub: [PASTE YOUR HTTPS LINK HERE]

#AI #MachineLearning #LangChain #LLM #GenAI #DataScience #GitHub
```

#### Step 17: Publish LinkedIn Post

1. Go to: https://www.linkedin.com
2. Click "Start a post"
3. Paste your content
4. Add optional image (screenshot of traces or results)
5. Click "Post"
6. Copy the URL from your published post

---

### Phase 7: Final Submission

#### Step 18: Gather Submission Links

Prepare these two links:

**Link 1: GitHub**
```
https://github.com/YOUR_USERNAME/AI_Resume_screener
```
(Must be HTTPS, not SSH)

**Link 2: LinkedIn**
```
https://www.linkedin.com/feed/update/urn:li:activity:1234567/
(Copy from your published post)
```

#### Step 19: Complete Google Form

Find the Google Form link in your LMS:
1. Full Name: Your name
2. Email: Your college email
3. GitHub Repository (HTTPS): Paste Link 1
4. LinkedIn Post: Paste Link 2
5. Submit

**Verification Checklist Before Submitting:**
- [ ] GitHub link works (can access repo)
- [ ] Repository is PUBLIC
- [ ] All files are present
- [ ] No .env file visible
- [ ] README.md is readable
- [ ] Notebook runs without errors
- [ ] LangSmith traces are visible (3 runs)
- [ ] LinkedIn post is published
- [ ] Both links are correct format
- [ ] Form filled completely

---

### Expected Timeline

| Phase | Time | Status |
|-------|------|--------|
| Setup | 15 min | ✓ Quick |
| Dependencies | 5 min | ✓ Automatic |
| API Keys | 10 min | ✓ Manual |
| Notebook Run | 10-15 min | ✓ Automatic |
| Verify Tracing | 5 min | ✓ Check online |
| GitHub Setup | 10 min | ✓ Create & push |
| LinkedIn Post | 10 min | ✓ Write & publish |
| Form Submission | 5 min | ✓ Final step |
| **TOTAL** | **~70 min** | ✓ Done! |

---

### Troubleshooting During Execution

**Problem**: Cell hangs/takes too long
**Solution**: Interrupt it (⏹ button) and check LangSmith traces console

**Problem**: JSON parse error
**Solution**: Check LangSmith for actual LLM response, may need prompt adjustment

**Problem**: API key error
**Solution**: 
1. Verify .env file has correct keys
2. Restart Jupyter kernel
3. Try keys in isolation

**Problem**: LangSmith traces not appearing
**Solution**:
1. Confirm LANGCHAIN_TRACING_V2=true
2. Wait 30 seconds for traces to upload
3. Refresh browser
4. Check project name matches

---

### Final Verification

Before declaring complete:

✅ Notebook runs start-to-finish without errors
✅ All 3 candidates screened with scores
✅ LangSmith shows 3 traces with all 5 steps
✅ screening_results.json file created
✅ GitHub repo created and public
✅ LinkedIn post published with GitHub link
✅ All links work and correct format
✅ Google Form filled and submitted
✅ Deadline met (April 16, 2026 before 11:59 PM)

---

**YOU'RE ALL SET! 🎉**

Follow this guide step-by-step, and your submission will be complete and professional!
