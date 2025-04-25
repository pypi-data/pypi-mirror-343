"""
This module loads data from Trello boards and converts them into a structured markdown file,
which can be used as a ToDo list for AI agents.
"""

import os
import json
import typer
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from trello import TrelloClient

app = typer.Typer(help="Loads Trello boards and converts them to Markdown for AI agents")

def setup_trello_client() -> TrelloClient:
    """
    Initializes the Trello client with API keys from environment variables.
    """
    load_dotenv()
    
    api_key = os.getenv("TRELLO_API_KEY")
    api_secret = os.getenv("TRELLO_API_SECRET")
    token = os.getenv("TRELLO_TOKEN")
    token_secret = os.getenv("TRELLO_TOKEN_SECRET")
    
    if not api_key or not token:
        typer.echo("Error: TRELLO_API_KEY and TRELLO_TOKEN must be defined in the .env file")
        raise typer.Exit(code=1)
    
    return TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=token,
        token_secret=token_secret
    )

def get_board(client: TrelloClient, board_id: str):
    """
    Loads a Trello board by its ID.
    """
    try:
        return client.get_board(board_id)
    except Exception as e:
        typer.echo(f"Error loading board with ID {board_id}: {str(e)}")
        raise typer.Exit(code=1)

def card_to_markdown(card) -> str:
    """
    Converts a Trello card to Markdown format.
    """
    md = f"- [ ] **{card.name}**"
    
    if card.description:
        # Remove comments and format markdown
        desc_lines = card.description.strip().split('\n')
        formatted_desc = '\n  '.join(desc_lines)
        md += f"\n  {formatted_desc}"
    
    # Add checklists
    checklists = card.fetch_checklists()
    if checklists:
        md += "\n  - Checklists:"
        for checklist in checklists:
            md += f"\n    - {checklist.name}"
            for item in checklist.items:
                status = "x" if item.get("checked", False) else " "
                md += f"\n      - [{status}] {item.get('name', '')}"
    
    # Add labels
    labels = card.labels
    if labels:
        label_str = ", ".join(f"`{label.name}`" for label in labels if label.name)
        if label_str:
            md += f"\n  - Tags: {label_str}"
    
    # Add due date
    if card.due_date:
        due_str = card.due_date.strftime("%Y-%m-%d %H:%M")
        md += f"\n  - Due: {due_str}"
    
    # Add link to card
    md += f"\n  - [Go to card]({card.url})"
    
    return md

def list_to_markdown(trello_list) -> str:
    """
    Converts a Trello list to Markdown format.
    """
    md = f"## {trello_list.name}\n\n"
    
    cards = trello_list.list_cards()
    if not cards:
        md += "*No cards available*\n\n"
        return md
    
    for card in cards:
        md += card_to_markdown(card) + "\n\n"
    
    return md

def board_to_markdown(board) -> str:
    """
    Converts a Trello board to Markdown format.
    """
    md = f"# {board.name}\n\n"
    
    # Add description if available
    if board.description:
        md += f"{board.description}\n\n"
    
    # Add metadata
    md += f"*Created on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    md += f"*Board ID: {board.id}*\n\n"
    md += "---\n\n"
    
    # Convert lists
    lists = board.list_lists()
    for trello_list in lists:
        md += list_to_markdown(trello_list)
    
    return md

@app.command()
def convert(
    board_id: str = typer.Argument(..., help="The ID of the Trello board"),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to output Markdown file"
    ),
    include_archived: bool = typer.Option(
        False, "--archived", "-a", help="Include archived cards"
    )
):
    """
    Converts a Trello board to a Markdown file.
    """
    typer.echo(f"Loading Trello board with ID: {board_id}")
    
    client = setup_trello_client()
    board = get_board(client, board_id)
    
    typer.echo(f"Board '{board.name}' found. Converting to Markdown...")
    
    # Default output file is board_name.md
    if not output_file:
        safe_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in board.name)
        safe_name = safe_name.replace(' ', '_').lower()
        output_file = Path(f"{safe_name}.md")
    
    markdown = board_to_markdown(board)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    typer.echo(f"Conversion completed. Output saved to: {output_file}")

@app.command()
def list_boards():
    """
    Lists all available Trello boards.
    """
    client = setup_trello_client()
    try:
        boards = client.list_boards()
        
        if not boards:
            typer.echo("No boards found.")
            return
        
        typer.echo("Available Trello boards:")
        for board in boards:
            typer.echo(f"- {board.name} (ID: {board.id})")
    
    except Exception as e:
        typer.echo(f"Error listing boards: {str(e)}")
        raise typer.Exit(code=1)

def main():
    """
    Main entry point for the command line application.
    """
    app()

if __name__ == "__main__":
    main()