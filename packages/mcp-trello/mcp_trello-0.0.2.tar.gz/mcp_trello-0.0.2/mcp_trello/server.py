# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union, Literal
import httpx

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Trello MCP")

# Environment variables for Trello configuration
TRELLO_BASE_URL = os.environ.get("TRELLO_BASE_URL", "https://api.trello.com/1")
TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

# Check if environment variables are set
if not all([TRELLO_API_KEY, TRELLO_TOKEN]):
    print("Warning: Trello environment variables not fully configured. Set TRELLO_API_KEY and TRELLO_TOKEN.", file=sys.stderr)

# Helper function for API requests
async def make_trello_request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Trello API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
        params: Query parameters to include
    
    Returns:
        Response from Trello API as dictionary
    """
    url = f"{TRELLO_BASE_URL}{endpoint}"
    
    # Add auth parameters
    if params is None:
        params = {}
    params['key'] = TRELLO_API_KEY
    params['token'] = TRELLO_TOKEN
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, params=params)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, params=params)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "error": True,
            "status_code": e.response.status_code,
            "message": e.response.text
        }
    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }

# === TOOLS ===

@mcp.tool()
async def get_boards() -> str:
    """
    Get a list of boards the user has access to.
    """
    result = await make_trello_request("GET", "/members/me/boards")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving boards: {result.get('message', 'Unknown error')}"
    
    boards = []
    for board in result:
        boards.append({
            "id": board.get("id"),
            "name": board.get("name"),
            "desc": board.get("desc"),
            "url": board.get("url")
        })
    
    return json.dumps(boards, indent=2)

@mcp.tool()
async def get_board(board_id: str) -> str:
    """
    Get details of a specific Trello board.
    
    Args:
        board_id: The Trello board ID
    """
    result = await make_trello_request("GET", f"/boards/{board_id}")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving board: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_lists(board_id: str) -> str:
    """
    Get lists within a specific Trello board.
    
    Args:
        board_id: The Trello board ID
    """
    result = await make_trello_request("GET", f"/boards/{board_id}/lists")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving lists: {result.get('message', 'Unknown error')}"
    
    lists = []
    for list_item in result:
        lists.append({
            "id": list_item.get("id"),
            "name": list_item.get("name"),
            "closed": list_item.get("closed"),
            "pos": list_item.get("pos")
        })
    
    return json.dumps(lists, indent=2)

@mcp.tool()
async def get_cards(list_id: str) -> str:
    """
    Get cards within a specific Trello list.
    
    Args:
        list_id: The Trello list ID
    """
    result = await make_trello_request("GET", f"/lists/{list_id}/cards")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving cards: {result.get('message', 'Unknown error')}"
    
    cards = []
    for card in result:
        cards.append({
            "id": card.get("id"),
            "name": card.get("name"),
            "desc": card.get("desc"),
            "due": card.get("due"),
            "url": card.get("url")
        })
    
    return json.dumps(cards, indent=2)

@mcp.tool()
async def create_card(list_id: str, name: str, desc: str = "", position: str = "bottom", due: str = None, labels: str = None) -> str:
    """
    Create a new card in a Trello list.
    
    Args:
        list_id: The Trello list ID
        name: Name/title of the card
        desc: Description of the card
        position: Position of the card (top, bottom, or a positive number)
        due: Due date in ISO format (e.g., "2023-12-31T12:00:00Z")
        labels: Comma-separated list of label IDs
    """
    data = {
        "idList": list_id,
        "name": name,
        "desc": desc,
        "pos": position
    }
    
    if due:
        data["due"] = due
    
    if labels:
        data["idLabels"] = labels.split(",")
    
    result = await make_trello_request("POST", "/cards", data=data)
    
    if isinstance(result, dict) and "error" in result:
        return f"Error creating card: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def update_card(card_id: str, name: str = None, desc: str = None, closed: bool = None, due: str = None) -> str:
    """
    Update an existing Trello card.
    
    Args:
        card_id: The Trello card ID
        name: New name/title of the card
        desc: New description of the card
        closed: Set to true to archive the card
        due: New due date in ISO format (e.g., "2023-12-31T12:00:00Z")
    """
    data = {}
    
    if name is not None:
        data["name"] = name
    
    if desc is not None:
        data["desc"] = desc
    
    if closed is not None:
        data["closed"] = closed
    
    if due is not None:
        data["due"] = due
    
    result = await make_trello_request("PUT", f"/cards/{card_id}", data=data)
    
    if isinstance(result, dict) and "error" in result:
        return f"Error updating card: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def move_card(card_id: str, list_id: str, position: str = "bottom") -> str:
    """
    Move a Trello card to a different list.
    
    Args:
        card_id: The Trello card ID
        list_id: The destination list ID
        position: Position in the new list (top, bottom, or a positive number)
    """
    data = {
        "idList": list_id,
        "pos": position
    }
    
    result = await make_trello_request("PUT", f"/cards/{card_id}", data=data)
    
    if isinstance(result, dict) and "error" in result:
        return f"Error moving card: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def search_cards(query: str, board_ids: str = None) -> str:
    """
    Search for Trello cards matching a query.
    
    Args:
        query: Search query
        board_ids: Comma-separated list of board IDs to search within
    """
    params = {
        "query": query,
        "modelTypes": "cards",
        "card_fields": "id,name,desc,due,url,labels"
    }
    
    if board_ids:
        params["idBoards"] = board_ids
    
    result = await make_trello_request("GET", "/search", params=params)
    
    if isinstance(result, dict) and "error" in result:
        return f"Error searching cards: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result.get("cards", []), indent=2)

@mcp.tool()
async def add_comment(card_id: str, text: str) -> str:
    """
    Add a comment to a Trello card.
    
    Args:
        card_id: The Trello card ID
        text: The comment text
    """
    data = {
        "text": text
    }
    
    result = await make_trello_request("POST", f"/cards/{card_id}/actions/comments", data=data)
    
    if isinstance(result, dict) and "error" in result:
        return f"Error adding comment: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("trello://boards")
async def get_boards_resource() -> str:
    """Get a list of all Trello boards the user has access to."""
    result = await make_trello_request("GET", "/members/me/boards")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving boards: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("trello://board/{board_id}")
async def get_board_resource(board_id: str) -> str:
    """Get details for a specific Trello board."""
    result = await make_trello_request("GET", f"/boards/{board_id}")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving board: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("trello://board/{board_id}/lists")
async def get_board_lists_resource(board_id: str) -> str:
    """Get lists within a specific Trello board."""
    result = await make_trello_request("GET", f"/boards/{board_id}/lists")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving lists: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("trello://list/{list_id}/cards")
async def get_list_cards_resource(list_id: str) -> str:
    """Get cards within a specific Trello list."""
    result = await make_trello_request("GET", f"/lists/{list_id}/cards")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving cards: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("trello://card/{card_id}")
async def get_card_resource(card_id: str) -> str:
    """Get details for a specific Trello card."""
    result = await make_trello_request("GET", f"/cards/{card_id}")
    
    if isinstance(result, dict) and "error" in result:
        return f"Error retrieving card: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_card")
def create_card_prompt(name: str = None, description: str = None, list_id: str = None) -> str:
    """
    A prompt template for creating a new card in Trello.
    
    Args:
        name: Name/title of the card
        description: Description of the card
        list_id: The Trello list ID
    """
    if all([name, list_id]):
        desc_text = f"\nDescription: {description}" if description else ""
        return f"Please help me create a new Trello card with these details:\n\nName: {name}{desc_text}\nList ID: {list_id}"
    else:
        return "I need to create a new Trello card. Please help me with the required details (name, description, and which list to add it to)."

@mcp.prompt("update_card")
def update_card_prompt(card_id: str = None, name: str = None, description: str = None) -> str:
    """
    A prompt template for updating an existing Trello card.
    
    Args:
        card_id: The Trello card ID
        name: New name/title of the card
        description: New description of the card
    """
    if card_id:
        details = []
        if name:
            details.append(f"New name: {name}")
        if description:
            details.append(f"New description: {description}")
        
        details_text = "\n".join(details) if details else "unspecified changes"
        
        return f"Please help me update Trello card with ID {card_id} with these changes:\n\n{details_text}"
    else:
        return "I need to update an existing Trello card. Please help me specify which card to update and what changes to make."

@mcp.prompt("search_cards")
def search_cards_prompt(query: str = None, board_id: str = None) -> str:
    """
    A prompt template for searching Trello cards.
    
    Args:
        query: Search query
        board_id: Optional board ID to limit search
    """
    if query:
        board_text = f" on board {board_id}" if board_id else ""
        return f"Please help me search for Trello cards matching '{query}'{board_text}."
    else:
        return "I need to search for Trello cards. What would you like to search for?"

if __name__ == "__main__":
    print("Starting Trello MCP server...", file=sys.stderr)
    mcp.run()