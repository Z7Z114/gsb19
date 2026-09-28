# 方言保护田野调查总结会 - 乡音纪要系统

## 项目简介

乡音纪要系统是一个专为方言保护田野调查设计的全栈应用，集成了多种AI技术来辅助语言学团队进行方言记录、分析和保护工作。

## 功能特性

### 前端功能
- 🎵 **专业录音播放器**：支持波形显示、变速播放、段落跳转
- 📝 **国际音标显示**：自动生成IPA国际音标转写
- 👥 **说话人分离**：自动区分发音人和研究者身份
- 🏷️ **语法变异标注**：自动识别并标注方言语法变异点
- 💬 **团队讨论协作**：支持语言学团队在线讨论和标注修正
- 📊 **濒危等级评估**：基于UNESCO标准自动评估方言濒危等级

### 后端AI服务
- 🎙️ **Whisper语音转写**：经方言微调的语音识别模型
- 🔊 **pyannote说话人分离**：区分不同说话人身份
- 🔍 **spaCy语法分析**：标注语法变异点
- 🤖 **OpenAI智能分析**：生成方言特征报告和濒危等级评估
- 📧 **Markdown邮件提交**：自动生成报告并提交至语言文字工作委员会

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Element Plus UI组件库
- WaveSurfer.js 音频播放器
- Pinia 状态管理
- Axios HTTP客户端

### 后端
- FastAPI Python Web框架
- SQLAlchemy ORM + SQLite
- PyTorch + Transformers (Whisper)
- pyannote.audio
- spaCy + jieba 中文分词
- OpenAI API
- pypinyin + epitran 音标转换

## 项目结构

```
.
├── frontend/                    # 前端代码
│   ├── src/
│   │   ├── components/          # 组件
│   │   │   ├── AudioPlayer.vue       # 音频播放器组件
│   │   │   ├── TranscriptionSegment.vue  # 转写片段组件
│   │   │   ├── EndangermentBadge.vue    # 濒危等级徽章
│   │   │   └── DiscussionPanel.vue      # 讨论区组件
│   │   ├── pages/               # 页面
│   │   │   ├── HomePage.vue         # 首页（上传页面）
│   │   │   ├── SessionDetail.vue    # 会话详情页
│   │   │   └── ReportDetail.vue     # 报告详情页
│   │   ├── services/            # API服务
│   │   │   └── api.ts
│   │   ├── types/               # TypeScript类型定义
│   │   │   └── index.ts
│   │   ├── router/              # 路由配置
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── backend/                     # 后端代码
    ├── app/
    │   ├── routers/             # API路由
    │   │   ├── audio.py             # 音频上传和播放
    │   │   ├── processing.py        # 处理状态管理
    │   │   ├── transcriptions.py    # 转写管理
    │   │   ├── speakers.py          # 说话人管理
    │   │   ├── discussion.py        # 讨论区
    │   │   └── report.py            # 报告生成
    │   ├── services/            # 业务服务
    │   │   ├── pyannote_service.py   # 说话人分离
    │   │   ├── whisper_service.py    # 语音转写
    │   │   ├── spacy_service.py      # 语法分析
    │   │   ├── openai_service.py     # AI分析
    │   │   ├── markdown_service.py   # Markdown生成
    │   │   └── processing_service.py # 处理流程编排
    │   ├── models.py             # 数据库模型
    │   ├── schemas.py            # Pydantic模式
    │   ├── database.py           # 数据库配置
    │   └── config.py             # 应用配置
    ├── data/
    │   ├── uploads/              # 上传的音频文件
    │   └── transcriptions/       # 转写结果
    ├── main.py                   # 应用入口
    ├── requirements.txt          # Python依赖
    └── .env.example              # 环境变量示例
```

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- ffmpeg（音频处理）

### 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
# 需要 Whisper / pyannote / spaCy 等重型模型能力时再装：
# pip install -r requirements-ml.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入必要的API密钥

# 下载spaCy中文模型
python -m spacy download zh_core_web_trf

# 启动后端服务
python main.py
```

后端服务将在 http://localhost:8000 启动

### 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

### API密钥配置

在 `backend/.env` 文件中配置以下密钥：

1. **OpenAI API Key**：用于生成摘要和分析报告
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

2. **Pyannote Auth Token**：用于说话人分离
   ```
   PYANNOTE_AUTH_TOKEN=your-pyannote-auth-token
   HF_API_TOKEN=your-huggingface-token
   ```

3. **SMTP配置**：用于发送邮件至语委
   ```
   SMTP_HOST=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@example.com
   SMTP_PASSWORD=your-password
   ```

## 使用流程

1. **上传录音**：在首页填写方言信息并上传田野调查录音文件
2. **等待处理**：系统自动进行说话人分离、语音转写、语法分析
3. **查看结果**：在会话详情页查看转写结果、国际音标、语法变异点
4. **团队讨论**：使用讨论区进行标注和讨论
5. **生成报告**：点击生成报告按钮，系统自动生成方言特征报告
6. **提交语委**：导出Markdown报告并通过邮件提交至语言文字工作委员会

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档（Swagger UI）

## 主要API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/audio/upload` | POST | 上传音频文件 |
| `/api/audio/stream/{session_id}` | GET | 流式播放音频 |
| `/api/processing/start` | POST | 开始处理音频 |
| `/api/processing/status/{session_id}` | GET | 获取处理状态 |
| `/api/transcriptions/{session_id}` | GET | 获取转写结果 |
| `/api/speakers/{session_id}` | GET | 获取说话人信息 |
| `/api/discussion/{session_id}` | GET/POST | 讨论区消息 |
| `/api/report/generate` | POST | 生成方言报告 |
| `/api/report/{report_id}` | GET | 获取报告详情 |
| `/api/report/{report_id}/markdown` | GET | 导出Markdown报告 |
| `/api/report/{report_id}/submit` | POST | 提交报告至语委 |

## 许可证

本项目仅用于学术研究和方言保护目的。


---

## 行为规格（验收标准）

本节是唯一验收标准。`backend/` 下的实现必须逐条满足；编号即验收点。

### A. 上传与音频流

- **A1** `POST /api/audio/upload` 接收 multipart 字段 `file`、`dialect`、`region`，把音频落盘到
  `backend/data/uploads/`，写入会话记录（`status="uploading"`），返回
  `session_id`、`filename`、`file_size`、`upload_time`。
- **A2** `GET /api/audio/stream/{session_id}`：会话或文件不存在返回 404；存在时返回音频本体，
  且 **`Content-Type` 必须由文件真实扩展名决定**——`.wav` → `audio/wav`（`audio/x-wav` 亦可），
  `.mp3` → `audio/mpeg`，`.m4a` → `audio/mp4`。不得对非 mp3 文件返回 `audio/mpeg`。

### B. 处理流水线与结果

- **B1** `POST /api/processing/start`：会话不存在 404；正在处理中的会话 400；
  已完成的会话直接返回 `completed`，不重复处理。
- **B2** 处理顺序为「说话人分离 → 语音转写 → 语法分析 → 汇总」。**未安装/未配置模型时走离线
  mock 分支**，仍要正常完成并把会话置为 `completed`、`progress=100`。
- **B3** 说话人建档：`speaker_label` 按其在分离结果中**首次出现的顺序**建档；**同角色内编号从 1
  连续递增**，且同一会话内**不同说话人不得重名**（例如 `研究员1`、`研究员2`、`研究员3`）。
  不同角色各自独立编号。
- **B4** `GET /api/speakers/{session_id}` 返回该会话全部说话人，字段含
  `id`、`name`、`role`、`pyannote_label`。
- **B5** `GET /api/transcriptions/{session_id}` 必须**始终返回 200** 与片段列表（按 `start_time`
  升序）。即使某片段从未被编辑过（时间戳字段为空），也不得报错。
- **B6** `PUT /api/transcriptions/{session_id}/{segment_id}` 可更新
  `text`/`ipa_transcription`/`grammar_variants`；片段不存在返回 404。
- **B7** 处理幂等：对同一会话重复执行处理流程，**不得重复插入说话人或转写片段**——
  重跑前必须清理该会话既有的说话人与转写记录。

### C. 语言学分析（语法变异点）

- **C1** `grammar_variants` 每个元素含 `token`、`standard_form`、`variant_type`、`description`、
  `ipa`、`position`。`position` 为 `[起, 止]`，0 基、左闭右开。
- **C2** 同一变异词在文本中**每出现一次都要单独报告一次**；`position` 必须等于该次出现的实际
  位置，满足 `text[position[0]:position[1]] == token`。不得把后续出现的位置标成首次出现的下标。
- **C3** 不得因为「同一 `token` + 同一 `variant_type`」而去重掉后续出现。

### D. 外部服务降级语义

- **D1** 模型/服务**未安装或未配置**时（Whisper 模型未加载、OpenAI 客户端未配置、
  pyannote 管线不可用、SMTP 未配置），允许走离线 mock 降级，保证系统可用。
- **D2** 模型**已加载**（或客户端**已配置**）但调用**真的失败**时（抛异常、超时、429 等），
  **不得**用 mock 内容冒充成功：转写或说话人分离失败必须让整个处理失败，会话落到 `error`；
  报告生成失败必须返回错误响应且**不得**写入报告记录。
- **D3** 处理失败后 `GET /api/processing/status/{session_id}` 必须返回 `status="error"`。

### E. 报告与提交

- **E1** `POST /api/report/generate`：会话未处理完成返回 400；成功返回报告，含 `summary`、
  `key_features`、`endangerment`、`transcription_count`、`total_duration`。
- **E2** `endangerment.level` 必须是下列 6 个标准代码之一：

  | 代码 | 中文 |
  | --- | --- |
  | `safe` | 安全 |
  | `vulnerable` | 脆弱 |
  | `definitely` | 明显濒危 |
  | `severely` | 严重濒危 |
  | `critically` | 极度濒危 |
  | `extinct` | 已灭绝 |

  若上游模型返回非标准表述（如 `Definitely Endangered`、`明显濒危`、`SEVERELY`），必须归一化到
  对应标准代码后再返回。
- **E3** `GET /api/report/{report_id}/markdown` 导出的报告正文中，「语料统计」的转写片段数与录音
  总时长必须与实际数据一致；`POST /api/report/{report_id}/submit` 生成的邮件附件 Markdown
  **必须与导出结果一致**，不得恒为 0。
- **E4** `POST /api/report/{report_id}/submit` 发送成功后把报告状态置为 `submitted` 并记录
  `submitted_at`；邮件发送失败返回 5xx 且状态不变。

## 已知问题（现象举例，**不完整**）

以下只是真实使用中被观察到的一部分现象，**不是**验收标准；验收标准是上面的「行为规格」。

- 打开会话详情页时，「转写结果」接口报 500，片段列表打不开。
- 上传 `.wav` 录音后播放器播不出声（后端把 wav 也按 `audio/mpeg` 返回）。
- 说话人列表里出现多个同名说话人（例如好几个「研究员1」）。
- 报告里的濒危等级直接显示模型返回的英文原文（例如 `Definitely Endangered`），前端徽章样式错乱。
