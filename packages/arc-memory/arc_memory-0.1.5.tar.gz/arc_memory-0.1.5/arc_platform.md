## **The Arc Memory Ecosystem**

The SDK we're releasing today is just the first component of a broader ecosystem we're building:

### **1. Arc Memory SDK (Available Now)**

The core Python SDK and CLI provides the foundation for building and querying the knowledge graph. It's designed to be lightweight, extensible, and privacy-focused, keeping all your data local.

### **2. Arc Memory MCP Server (Coming Soon)**

Our upcoming Model Context Protocol (MCP) server will integrate with Anthropic's open standard for connecting AI assistants to data sources:

- **Standardized AI Access**: Following Anthropic's MCP specification for secure, standardized AI access to knowledge graphs
- **Persistent Memory**: Knowledge graph-based persistent memory system for AI agents
- **Contextual Retrieval**: Intelligent retrieval of relevant code history and decisions
- **Seamless Integration**: Works with Claude and other MCP-compatible AI assistants
- **Privacy Controls**: Fine-grained access controls for sensitive information
- **Verifiable Citations**: Enables AI to cite specific evidence from the knowledge graph

This will allow any MCP-compatible AI assistant to access your codebase's memory and context, providing deeper insights and more accurate assistance.

### **3. VS Code Extension (Coming Soon)**

Our VS Code extension will bring the power of Arc Memory directly into your development environment:

- Hover cards showing the decision trail behind code
- Inline context for functions, classes, and variables
- Integration with VS Code's Agent Mode for AI-assisted development
- Visual exploration of the knowledge graph
- Quick access to related PRs, issues, and documentation

## **The Foundation for AI-Assisted Development**

Arc Memory is designed from the ground up to be the memory layer for AI-assisted development. By providing structured, verifiable context about code history and decisions, it enables AI agents to:

1. **Understand code in context** - not just what it does, but why it was written that way
2. **Reference relevant discussions** - pointing to PRs, issues, and ADRs that explain decisions
3. **Avoid repeating mistakes** - by having access to the full history of changes and their rationale
4. **Generate better suggestions** - grounded in the project's actual history and patterns
5. **Verify its own reasoning** - by citing specific evidence from the knowledge graph