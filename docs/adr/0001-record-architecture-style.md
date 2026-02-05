# 1. Use Hexagonal Architecture (Ports and Adapters)

Date: 2026-02-02
Status: Accepted

## Context
We are building a video downloader application (HydraDL) that needs to support multiple video sources (YouTube, Vimeo, etc.) and potentially different user interfaces (CLI, Web API, Desktop GUI) in the future.
The application logic needs to be isolated from external tools (yt-dlp) and frameworks (FastAPI) to ensure testability and maintainability.

## Decision
We will use **Hexagonal Architecture** (also known as Ports and Adapters).

The application will be structured into three main layers:
1.  **Core (Domain & Use Cases):** Pure Python code. No external dependencies.
2.  **Ports (Interfaces):** Abstract definitions of what the app needs.
3.  **Adapters (Infrastructure):** Concrete implementations (FastAPI, yt-dlp, FileSystem).

## Consequences
### Positive
* **Testability:** We can test the core logic without downloading real videos or starting a server.
* **Flexibility:** We can swap `yt-dlp` for another library later without rewriting the business logic.
* **Independence:** The UI (CLI/API) is decoupled from the logic.

### Negative
* **Complexity:** Requires more boilerplate code (interfaces, DTOs) than a simple script.
* **Learning Curve:** Requires understanding of dependency injection.
