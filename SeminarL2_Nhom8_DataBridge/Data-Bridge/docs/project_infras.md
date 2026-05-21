Seminar_Final/
├── .agents/
│   ├── AGENTS.md                    # [AGENT] Luật tổng (Global Rules) - Điều phối toàn dự án
│   └── skills/                      # [SKILLS] Thư mục chứa bí kíp và quy trình (How-to)
│       ├── frontend/
│       │   └── SKILL.md             # Cách xây dựng UI, Next.js, Tailwind
│       ├── backend/
│       │  
│       │   ├── nl2sql_skill.md            # Cách viết Prompt, Pipeline Agent
│       │   └── query-executor_skill.md    # Cách xử lý SQL, DB connection
│       ├── infra/
│       │   ├── supabase.md          # Cách quản lý DB Schema, Auth, RLS
│       │   └── docker.md            # Cách quản lý Compose, Hot-reload, Ports
│       └── testing/                 # Domain Testing tập trung
│           ├── SKILL.md             # File điều phối: Khi nào dùng tool test nào?
│           ├── playwright/
│           │   └── SKILL.md         # Cách viết E2E Browser Test cho UI
│           ├── api-integration/
│           │   └── SKILL.md         # Cách viết Integration Test (Pytest + Httpx)
│           └── k6-performance/
│               └── SKILL.md         # Cách chạy Load Test đo hiệu năng (k6)
│
├── frontend/
│   └── AGENTS.md                    # [AGENT] Luật riêng cho Frontend (Quy ước UI/UX)
│
├── services/
│   ├── api-gateway/
│   │   
│   ├── nl2sql-service/
│   │   └── AGENTS.md                # [AGENT] Luật riêng cho AI (An toàn Prompt)
│   └── query-service/
│       └── AGENTS.md                # [AGENT] Luật riêng cho Query (Bảo mật SQL)
│
└── ... (Các thư mục code: frontend/, services/, database/...)

