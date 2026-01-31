# Web POC Patterns

For claims requiring a web interface or frontend interaction.

## Basic HTML + JavaScript POC

```html
<!DOCTYPE html>
<html>
<head>
    <title>POC: [Claim]</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            max-width: 800px;
            margin: 2rem auto;
            padding: 1rem;
        }
        .result {
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .success { background: #d4edda; border-color: #28a745; }
        .failure { background: #f8d7da; border-color: #dc3545; }
        button {
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>POC: [Claim]</h1>
    <p>Testing: [Specific thing being tested]</p>

    <button onclick="runTest()">Run Test</button>
    <div id="result" class="result"></div>

    <script>
        async function runTest() {
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = 'Running...';
            resultDiv.className = 'result';

            try {
                // Core test logic here
                const result = await testTheThing();

                resultDiv.textContent = `Result: ${JSON.stringify(result, null, 2)}`;
                resultDiv.classList.add(result.success ? 'success' : 'failure');
            } catch (error) {
                resultDiv.textContent = `Error: ${error.message}`;
                resultDiv.classList.add('failure');
            }
        }

        async function testTheThing() {
            // Implement core test
            return { success: true, data: 'result' };
        }
    </script>
</body>
</html>
```

## With API Calls

```javascript
async function testTheThing() {
    const response = await fetch('/api/endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: 'value' })
    });

    const data = await response.json();
    return {
        success: response.ok,
        status: response.status,
        data: data
    };
}
```

## Measuring User Interaction

```javascript
// Track timing
const startTime = performance.now();

// After user action
const endTime = performance.now();
const duration = endTime - startTime;
console.log(`Action took ${duration}ms`);

// Track events
document.addEventListener('click', (e) => {
    console.log('Click:', e.target.tagName, e.clientX, e.clientY);
});

// Track typing
let keystrokes = [];
document.addEventListener('keydown', (e) => {
    keystrokes.push({
        key: e.key,
        time: performance.now()
    });
});
```

## Simple Python Server

```python
#!/usr/bin/env python3
"""
Serve the POC locally.

Run: python server.py
Open: http://localhost:8000
"""

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPServer

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
```

## With Live Reload (requires livereload)

```python
#!/usr/bin/env python3
from livereload import Server

server = Server()
server.watch('*.html')
server.watch('*.js')
server.watch('*.css')
server.serve(port=8000, root='.')
```

## File Structure

```
poc/
├── index.html      # Main page
├── style.css       # Optional styles
├── main.js         # Optional separate JS
├── server.py       # Local server
└── README.md       # How to run
```

## README Template

```markdown
# POC: [Claim]

## Run

1. `python server.py`
2. Open http://localhost:8000
3. Click "Run Test"

## What This Tests

[Description of what the POC demonstrates]

## Expected Result

[What success looks like]
```

## Tips

1. **Keep it minimal** — No frameworks unless necessary
2. **Show raw data** — Display actual values, not just pass/fail
3. **Log everything** — Console.log liberally
4. **Handle errors visibly** — User should see failures
5. **Document how to run** — Others need to reproduce
