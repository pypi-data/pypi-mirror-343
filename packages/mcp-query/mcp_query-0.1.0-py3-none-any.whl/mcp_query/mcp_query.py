import subprocess
import json
import sys
import argparse

def query_context7_mcp(library, topic, tokens, verbose=False):
    try:
        # Validate inputs
        if not library:
            raise ValueError("Library name cannot be empty.")
        if tokens <= 0:
            raise ValueError("Tokens must be a positive integer.")

        # Start the Context7 MCP server as a subprocess using npx
        process = subprocess.Popen(
            ["npx", "-y", "@upstash/context7-mcp@latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Format the query for Context7 MCP server
        query = json.dumps({
            "id": "c7_query",
            "params": {
                "context7CompatibleLibraryID": library,
                "topic": topic if topic else "overview",
                "tokens": tokens
            }
        })

        # Send the query to the MCP server and capture the response
        stdout, stderr = process.communicate(input=query, timeout=30)

        if stderr and verbose:
            print(f"Error from Context7 MCP server: {stderr}", file=sys.stderr)

        # Parse and return the response
        return json.loads(stdout)

    except subprocess.TimeoutExpired:
        if verbose:
            print("Error: Context7 MCP server query timed out.", file=sys.stderr)
        process.kill()
        return None
    except json.JSONDecodeError:
        if verbose:
            print("Error: Failed to parse response from Context7 MCP server.", file=sys.stderr)
        return None
    except Exception as e:
        if verbose:
            print(f"Error: {str(e)}", file=sys.stderr)
        return None

def main():
    # Set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Query Context7 MCP server for documentation.")
    parser.add_argument("--library", type=str, required=True, help="Library to query (e.g., 'react')")
    parser.add_argument("--topic", type=str, default="overview", help="Topic to query (e.g., 'hooks')")
    parser.add_argument("--tokens", type=int, required=True, help="Max tokens for response (e.g., 5000)")
    parser.add_argument("--verbose", action="store_true", help="Show error messages (default: False)")

    # Parse arguments
    args = parser.parse_args()

    # Query the MCP server with provided library and topic
    result = query_context7_mcp(args.library, args.topic, args.tokens, args.verbose)

    if result:
        # Clean output for Aider's /run command
        print(json.dumps({
            "library": args.library,
            "topic": args.topic,
            "documentation": result.get("result", "No documentation found.")
        }, indent=2))
    else:
        print(json.dumps({
            "error": f"Failed to retrieve documentation for {args.library} ({args.topic})."
        }, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()