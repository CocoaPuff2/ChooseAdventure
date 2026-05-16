# Choose Your Own Adventure Game

## Overview
- Implements interactive gameplay or educational logic using Python and Pygame.
- Handles user input, game state, and rendering in real time.
- Uses event loops, classes, and object-oriented design for modular code.
- Demonstrates Python programming fundamentals, debugging, and performance optimization.
- Focuses on backend logic for game mechanics, while optionally integrating simple GUI rendering.

## Tools
- FastAPI to build the backend (creating stories, storing them in the database, and managing user sessions so multiple users could interact with the app at the same time.)
-  React to build the frontend (users could see the story, choose options, and watch the story update in real time as they made decisions)

## Backend
1. Create a story (POST /stories/create)
  - Takes a theme (e.g., “fantasy”) and a session ID.
  - Uses the AI (via LangChain/OpenAI) to generate the story structure (title, root node, branching choices).
  - Saves the story and all its nodes/options in the database.
  - Returns a job ID for background processing (async generation)
    
2. Check story progress or completion (GET /stories/{story_id}/complete)
   - Retrieves a finished story from the database.
   - Returns the structured story (title, nodes, options) in a JSON format.
   - This is what you’re currently seeing as "Story not found", because the database doesn’t yet have a story with that id.
     
3. Background tasks
 - The story generation runs asynchronously so the server can handle requests without waiting for the AI to finish.
 - That’s why there’s a job system (StoryJob) to track progress: "pending" → "processing" → "completed".

## Frontend



