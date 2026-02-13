# Henvdall 🛡️

**The Gatekeeper of Environment Variables**

Henvdall is a professional-grade Python CLI utility that ensures your local `.env` file stays in sync with your project's `.env.example` file, preventing runtime crashes caused by "Schema Drift."

## Features

- 🔄 **Sync Logic**: Automatically detects missing environment variables
- 🎨 **Interactive TUI**: Beautiful terminal interface powered by Rich
- ✅ **Validation**: Type checking for integers, URLs, and more
- 🔒 **Safety First**: Automatic backups before modifications
- 🔍 **Audit Mode**: Detect placeholder values that need attention

## Installation

### Using Poetry (Recommended)

```bash
poetry install
```

### Using Pip

```bash
pip install -e .
```

## Usage

### Sync Environment Variables

Compare `.env.example` with `.env` and interactively fill missing values:

```bash
henvdall sync
```

### Audit Existing Values

Scan your `.env` file for placeholder values that need to be updated:

```bash
henvdall audit
```

## Validation Types

Henvdall supports inline validation comments in your `.env.example` file:

```env
# Database configuration
DB_PORT=5432  # (int)
API_ENDPOINT=https://api.example.com  # (url)
API_KEY=your_key_here
```

Supported validation types:
- `# (int)` - Ensures the value is a valid integer
- `# (url)` - Ensures the value is a valid URL

## Example

Given a `.env.example`:

```env
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your_api_key_here  # (url)
MAX_CONNECTIONS=10  # (int)
```

And a `.env` with only:

```env
DATABASE_URL=postgresql://localhost/production
```

Running `henvdall sync` will:
1. Create a backup at `.env.bak`
2. Prompt you to enter values for `API_KEY` and `MAX_CONNECTIONS`
3. Validate the inputs according to their types
4. Append the new values to `.env`

## Safety

- Never modifies `.env.example`
- Creates `.env.bak` backup before any changes
- Only appends to `.env`, never overwrites existing values

## License

MIT
