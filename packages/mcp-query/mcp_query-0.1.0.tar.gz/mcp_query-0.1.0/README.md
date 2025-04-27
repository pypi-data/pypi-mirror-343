# Context7 MCP Query Script

## Overview

The `mcp_query.py` script enables Aider to query the Context7 MCP server for up-to-date library documentation, enhancing coding assistance with current information.

## Why Aider?

Aider was chosen for this integration because of its:
- Seamless command-line workflow integration
- Token-efficient design
- Focused context management
- Support for cost-effective models like DeepSeek

### Key Advantages Over Alternatives

1. **Token Efficiency**  
   Aider only adds necessary files to chat sessions and pulls related context via repository mapping, saving tokens compared to tools like Cursor that may index entire codebases.

2. **Cost Effectiveness**  
   Large projects can exceed 20k tokens with other tools, while Aider's focused approach keeps token usage manageable, especially when combined with economical models.

3. **Optimized Workflow**  
   The combination of Aider and Context7 MCP ensures documentation can be fetched and utilized without exceeding token limits.

## Usage

```bash
python mcp_query.py [query]
```

Replace `[query]` with your search term for Context7 documentation.

## Requirements

- Python 3.x
- Aider installed and configured
- Context7 MCP server access
