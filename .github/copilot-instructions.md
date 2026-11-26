# Copilot Instructions

## Project Purpose

This project is a learning exercise in requirements-driven AI-assisted
software development for a university Systems Analysis and Design course.

## Source of Truth

Before implementing functionality, review the authoritative requirements
and design artifacts in this repository.

Requirements take precedence over assumptions.

Do not invent business requirements when the repository does not specify
the desired behavior. Identify the ambiguity instead.

## Requirements Traceability

When implementing a functional requirement or user story:

1. Identify the requirement IDs being implemented.
2. Implement only the requested scope.
3. Create appropriate automated tests.
4. Map tests back to requirements or acceptance criteria where practical.
5. Report any requirement that cannot be implemented as written.

## Development Practices

- Prefer simple, maintainable solutions over unnecessary complexity.
- Keep business logic separate from presentation logic and persistence.
- Use clear naming.
- Avoid duplicated business logic.
- Validate user input.
- Handle errors explicitly.
- Do not hard-code credentials or secrets.
- Add comments where they explain intent, not obvious syntax.

## AI Behavior

Do not silently invent missing requirements.

When a requirement is ambiguous:
1. Identify the ambiguity.
2. Explain why it matters.
3. Recommend an interpretation.
4. Ask for a decision when the choice materially affects business behavior.

## Change Control

Before making a major architectural change, explain:
- what will change,
- why it is necessary,
- which requirements require it,
- and what alternatives were considered.

Do not modify approved requirements merely to make implementation easier.