# curlmock

Start a local mock API from a cURL command in one line. No config files, no Postman export — paste the curl, get a server.

## Install

```bash
pip install git+https://github.com/etailup/curlmock.git
```

Or locally:

```bash
git clone https://github.com/etailup/curlmock.git
cd curlmock
pip install -e .
```

## Usage

```bash
# Mock a GET endpoint with a default JSON response
curlmock 'curl https://api.example.com/users'

# Return a custom response file
curlmock 'curl -X POST https://api.example.com/users' -r response.json

# Echo mode — see exactly what your client sends
curlmock 'curl -X POST https://api.example.com/users' --echo
```

Then point your app at `http://127.0.0.1:8787`:

```bash
curl http://127.0.0.1:8787/users
```

## Example

**Terminal 1**

```bash
curlmock 'curl https://api.example.com/v1/status' -r examples/status.json --port 8787
```

**Terminal 2**

```bash
curl http://127.0.0.1:8787/v1/status
```

**response.json**

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

## Why

Frontend and integration work often starts before the backend exists. `curlmock` turns any cURL into a working local endpoint so you can unblock development immediately.

## License

MIT
