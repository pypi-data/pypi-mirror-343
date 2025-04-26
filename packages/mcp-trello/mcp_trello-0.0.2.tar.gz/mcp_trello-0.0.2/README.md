# Trello MCP Server

A Model Context Protocol (MCP) server for Trello integration. This server provides tools for interacting with Trello, including managing boards, lists, and cards through the Trello API.

## Features

- **Board Management**: View and manage Trello boards
- **List Operations**: Access lists within boards
- **Card Management**: Create, update, move, and search for cards
- **Comments**: Add comments to cards
- **Resources**: Access Trello objects through URI templates
- **Prompts**: Templates for common Trello workflows

## Installation

```bash
pip install mcp-trello
```

## Configuration

Set the following environment variables:

```bash
export TRELLO_API_KEY="your_trello_api_key"
export TRELLO_TOKEN="your_trello_token"
```

You can obtain a Trello API key and token from the [Trello Developer API Keys page](https://trello.com/app-key).

## Usage

### Starting the server directly

```bash
mcp-trello
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "mcp-trello": {
      "command": "uvx",
      "args": [
        "mcp-trello"
      ],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key",
        "TRELLO_TOKEN": "your_trello_token"
      }
    }
  }
}
```

Replace the environment variables with your actual Trello credentials.

## Available Tools

* **get_boards**: Get a list of boards the user has access to
* **get_board**: Get details of a specific Trello board
* **get_lists**: Get lists within a specific Trello board
* **get_cards**: Get cards within a specific Trello list
* **create_card**: Create a new card in a Trello list
* **update_card**: Update an existing Trello card
* **move_card**: Move a Trello card to a different list
* **search_cards**: Search for Trello cards matching a query
* **add_comment**: Add a comment to a Trello card

## Available Resources

* **trello://boards**: List of all Trello boards the user has access to
* **trello://board/{board_id}**: Details for a specific Trello board
* **trello://board/{board_id}/lists**: Lists within a specific Trello board
* **trello://list/{list_id}/cards**: Cards within a specific Trello list
* **trello://card/{card_id}**: Details for a specific Trello card

## Available Prompts

* **create_card**: Template for creating a new Trello card
* **update_card**: Template for updating an existing Trello card
* **search_cards**: Template for searching Trello cards

## Example Conversations

Using Claude with the Trello MCP:

1. **Creating a new card:**

   "Create a new card called 'Update documentation' in my 'To Do' list on the 'Project Management' board."

2. **Moving a card:**

   "Move the 'Implement login feature' card from 'In Progress' to 'Done'."

3. **Searching for cards:**

   "Find all cards related to 'documentation' across all my boards."

## Development

To set up for development:

```bash
git clone https://github.com/yourusername/mcp-trello.git
cd mcp-trello
pip install -e .
```

## License

MIT

## Version

0.1.0