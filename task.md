# TASK

## Description

Create a simple RESTful API using FastAPI for a social networking application

## Functional requirements:

- There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own
- The API needs a UI Documentation (Swagger/ReDoc)

## Bonus section (not required):

- Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
- Use emailhunter.co for verifying email existence on registration
- Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added)

## Technology Requirements

Tasks should be completed:

- Using FastAPI 0.50.0+
- With any DBMS (Sqlite, PostgreSQL, MySQL)
- Uploaded to GitHub

## Requirements

When implementing your solution, please make sure that the code is:

- Well-structured
- Contains instructions (best to be put into readme.md) about how to deploy and test it
- Clean The program you implement _must be a complete program product_, i.e. should be easy to install, provide for the handling of non-standard situations, be resistant to incorrect user actions, etc.
