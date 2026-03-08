const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3456;
const WORKSPACE = path.resolve(__dirname, '..');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

// API: list all memory files with content
function getMemories() {
  const memories = [];
  
  // Core files
  const coreFiles = [
    { path: 'SOUL.md', icon: '🔮', type: 'soul', category: 'Kern' },
    { path: 'MEMORY.md', icon: '🧠', type: 'memory', category: 'Kern' },
    { path: 'IDENTITY.md', icon: '🪞', type: 'identity', category: 'Kern' },
  ];
  
  for (const f of coreFiles) {
    const fp = path.join(WORKSPACE, f.path);
    if (fs.existsSync(fp)) {
      memories.push({ ...f, title: f.path, content: fs.readFileSync(fp, 'utf8'), mtime: fs.statSync(fp).mtime });
    }
  }

  // Memory directory files
  const memFiles = [
    { path: 'lessons.md', icon: '💡', type: 'lesson', category: 'Wachstum' },
    { path: 'decisions.md', icon: '⚖️', type: 'decision', category: 'Wachstum' },
    { path: 'feedback.md', icon: '💬', type: 'feedback', category: 'Wachstum' },
  ];
  
  for (const f of memFiles) {
    const fp = path.join(MEMORY_DIR, f.path);
    if (fs.existsSync(fp)) {
      memories.push({ ...f, title: f.path, content: fs.readFileSync(fp, 'utf8'), mtime: fs.statSync(fp).mtime });
    }
  }

  // Daily files
  if (fs.existsSync(MEMORY_DIR)) {
    const files = fs.readdirSync(MEMORY_DIR).filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort().reverse();
    for (const f of files) {
      const fp = path.join(MEMORY_DIR, f);
      memories.push({
        path: f, title: f.replace('.md', ''), icon: '📅', type: 'daily',
        category: 'Tagesnotizen', content: fs.readFileSync(fp, 'utf8'), mtime: fs.statSync(fp).mtime
      });
    }
  }

  return memories;
}

// API: get tasks (from TASKS.md or memory)
function getTasks() {
  const fp = path.join(WORKSPACE, 'TASKS.md');
  if (fs.existsSync(fp)) return fs.readFileSync(fp, 'utf8');
  // Fallback: extract from daily notes
  return null;
}

// API: get soul
function getSoul() {
  const fp = path.join(WORKSPACE, 'SOUL.md');
  return fs.existsSync(fp) ? fs.readFileSync(fp, 'utf8') : null;
}

// API: workspace stats
function getStats() {
  const memCount = fs.existsSync(MEMORY_DIR) ? fs.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.md')).length : 0;
  const soul = fs.existsSync(path.join(WORKSPACE, 'SOUL.md'));
  const memory = fs.existsSync(path.join(WORKSPACE, 'MEMORY.md'));
  return { memoryFiles: memCount, hasSoul: soul, hasMemory: memory, uptime: process.uptime() };
}

const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.url === '/api/memories') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getMemories()));
  } else if (req.url === '/api/tasks') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ content: getTasks() }));
  } else if (req.url === '/api/soul') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ content: getSoul() }));
  } else if (req.url === '/api/stats') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getStats()));
  } else {
    // Serve static files
    let filePath = req.url === '/' ? '/index.html' : req.url;
    filePath = path.join(__dirname, filePath);
    const ext = path.extname(filePath);
    const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json' };
    
    fs.readFile(filePath, (err, data) => {
      if (err) { res.writeHead(404); res.end('Not found'); return; }
      res.writeHead(200, { 'Content-Type': types[ext] || 'text/plain' });
      res.end(data);
    });
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Viv Dashboard running on port ${PORT}`);
});
