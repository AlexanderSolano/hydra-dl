# 🐉 HydraDL

> A high-performance, distributed video downloader built with Python 3.10+, Hexagonal Architecture, and Async I/O.

[![CI Pipeline](https://github.com/AlexanderSolano/hydra-dl/actions/workflows/quality.yml/badge.svg)](https://github.com/AlexanderSolano/hydra-dl/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Architecture](https://img.shields.io/badge/architecture-hexagonal-orange)](https://alistair.cockburn.us/hexagonal-architecture/)

## 🚀 Overview
HydraDL maximizes bandwidth utilization by splitting video streams into concurrent segments. Unlike traditional downloaders, it employs a **Hexagonal Architecture** (Ports & Adapters) to decouple core business logic from infrastructure details, allowing seamless switching between local storage, cloud environments (Azure), and different CLI/Web interfaces.

**Key Features:**
* **Smart Segmentation:** Calculates optimal chunk sizes based on file size.
* **Async I/O Core:** Built on `aiohttp` and `aiofiles` for non-blocking operations.
* **Resilient:** Exponential backoff retries and network error handling.
* **Hybrid Runtime:** Runs locally (CLI) or as a distributed Cloud Service.

## 🏗️ Architecture
This project strictly follows **Clean Architecture** principles to ensure testability and scalability.

```mermaid
graph TD
    User((User)) --> CLI[CLI Driver]
    User --> API[FastAPI Driver]
    
    subgraph "Application Core (Pure Python)"
        CLI --> UseCase[DownloadManager]
        API --> UseCase
        UseCase --> Entities[Video / Job]
    end
    
    subgraph "Infrastructure (Adapters)"
        UseCase -.-> |Port| IExtractor[IExtractor]
        UseCase -.-> |Port| IDownloader[IDownloader]
        UseCase -.-> |Port| IStorage[IStorage]
        
        IExtractor --> YtDlp[yt-dlp Adapter]
        IDownloader --> AioHttp[aiohttp Adapter]
        IStorage --> LocalDisk[Sparse File System]
    end