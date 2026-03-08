const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3456;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../dashboard')));

// Ensure data directory exists
const dataDir = path.join(__dirname, '../data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Initialize SQLite database
const db = new Database(path.join(dataDir, 'mission-control.db'));

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'backlog',
    assignee TEXT,
    priority TEXT DEFAULT 'medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    tags TEXT
  );

  CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    emoji TEXT,
    description TEXT,
    status TEXT DEFAULT 'idle',
    last_active DATETIME,
    config TEXT
  );

  CREATE TABLE IF NOT EXISTS cron_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    schedule TEXT NOT NULL,
    agent_id TEXT,
    payload TEXT,
    enabled INTEGER DEFAULT 1,
    last_run DATETIME,
    next_run DATETIME
  );

  CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    content TEXT NOT NULL,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    action TEXT,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

// Seed agents if empty
const agentCount = db.prepare('SELECT COUNT(*) as count FROM agents').get();
if (agentCount.count === 0) {
  const agents = [
    { id: 'fin', name: 'Fin', role: 'Finance', emoji: '💰', description: 'Bookkeeping, invoicing, reconciliation', status: 'idle' },
    { id: 'goaly', name: 'Goaly', role: 'Project Management', emoji: '📋', description: 'Tasks, planning, SOPs', status: 'idle' },
    { id: 'designy', name: 'Designy', role: 'Design', emoji: '🎨', description: 'Client design reviews, asset management', status: 'idle' },
    { id: 'contenty', name: 'Contenty', role: 'Content', emoji: '📝', description: 'SEO, social media, blog', status: 'idle' },
    { id: 'reflecty', name: 'Reflecty', role: 'Reflection', emoji: '🔮', description: 'Weekly reviews, pattern analysis', status: 'idle' },
    { id: 'processy', name: 'Processy', role: 'Optimization', emoji: '⚙️', description: 'Workflow improvements, automation suggestions', status: 'idle' }
  ];
  
  const insertAgent = db.prepare('INSERT INTO agents (id, name, role, emoji, description, status) VALUES (?, ?, ?, ?, ?, ?)');
  agents.forEach(agent => {
    insertAgent.run(agent.id, agent.name, agent.role, agent.emoji, agent.description, agent.status);
  });
}

// API Routes

// Get all tasks
app.get('/api/tasks', (req, res) => {
  const tasks = db.prepare('SELECT * FROM tasks ORDER BY updated_at DESC').all();
  res.json(tasks);
});

// Create task
app.post('/api/tasks', (req, res) => {
  const { title, description, assignee, priority, due_date, tags } = req.body;
  const result = db.prepare(
    'INSERT INTO tasks (title, description, assignee, priority, due_date, tags) VALUES (?, ?, ?, ?, ?, ?)'
  ).run(title, description, assignee, priority, due_date, tags || '');
  
  // Log activity
  db.prepare('INSERT INTO activity_log (agent_id, action, details) VALUES (?, ?, ?)')
    .run(assignee || 'system', 'task_created', JSON.stringify({ task_id: result.lastInsertRowid, title }));
  
  res.json({ id: result.lastInsertRowid, ...req.body });
});

// Update task
app.patch('/api/tasks/:id', (req, res) => {
  const { id } = req.params;
  const { status, title, description, assignee, priority } = req.body;
  
  const updates = [];
  const values = [];
  
  if (status) { updates.push('status = ?'); values.push(status); }
  if (title) { updates.push('title = ?'); values.push(title); }
  if (description) { updates.push('description = ?'); values.push(description); }
  if (assignee) { updates.push('assignee = ?'); values.push(assignee); }
  if (priority) { updates.push('priority = ?'); values.push(priority); }
  updates.push('updated_at = CURRENT_TIMESTAMP');
  
  values.push(id);
  
  db.prepare(`UPDATE tasks SET ${updates.join(', ')} WHERE id = ?`).run(...values);
  
  res.json({ success: true });
});

// Get all agents
app.get('/api/agents', (req, res) => {
  const agents = db.prepare('SELECT * FROM agents ORDER BY name').all();
  res.json(agents);
});

// Update agent status
app.patch('/api/agents/:id', (req, res) => {
  const { id } = req.params;
  const { status } = req.body;
  
  db.prepare('UPDATE agents SET status = ?, last_active = CURRENT_TIMESTAMP WHERE id = ?')
    .run(status, id);
  
  res.json({ success: true });
});

// Get cron jobs
app.get('/api/cron', (req, res) => {
  const jobs = db.prepare('SELECT * FROM cron_jobs ORDER BY next_run').all();
  res.json(jobs);
});

// Get memories
app.get('/api/memories', (req, res) => {
  const { q, agent } = req.query;
  let query = 'SELECT * FROM memories WHERE 1=1';
  const params = [];
  
  if (q) {
    query += ' AND content LIKE ?';
    params.push(`%${q}%`);
  }
  
  if (agent) {
    query += ' AND agent_id = ?';
    params.push(agent);
  }
  
  query += ' ORDER BY created_at DESC LIMIT 100';
  
  const memories = db.prepare(query).all(...params);
  res.json(memories);
});

// Get activity log
app.get('/api/activity', (req, res) => {
  const activities = db.prepare(
    'SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 50'
  ).all();
  res.json(activities);
});

// Dashboard stats
app.get('/api/stats', (req, res) => {
  const taskStats = db.prepare(`
    SELECT status, COUNT(*) as count FROM tasks GROUP BY status
  `).all();
  
  const agentStats = db.prepare(`
    SELECT status, COUNT(*) as count FROM agents GROUP BY status
  `).all();
  
  const totalTasks = db.prepare('SELECT COUNT(*) as count FROM tasks').get();
  const activeAgents = db.prepare("SELECT COUNT(*) as count FROM agents WHERE status = 'active'").get();
  
  res.json({
    tasks: taskStats,
    agents: agentStats,
    totalTasks: totalTasks.count,
    activeAgents: activeAgents.count
  });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`🚀 Mission Control running on port ${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}`);
});
