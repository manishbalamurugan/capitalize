# Startup Investor Platform

## Overview

This project is a platform designed to connect investors with startups, providing a centralized hub for information, news, and engagement. The system allows investors to track startups of interest, view relevant news and updates, and manage their portfolio of interests.

## Features

- Company profiles for startups
- Investor profiles and authentication
- Bookmarking system for investors to follow startups
- News feed aggregation for tracked companies
- Database integration for persistent data storage

## Technology Stack

- Backend: Python
- Database: MongoDB
- APIs: OpenAI GPT-4, Exa API
- Frontend: (To be determined, e.g., React, Vue.js)

## Database Schema Design

We use MongoDB, a NoSQL database, for this project. Here are the main collections and their structures:

### Collections

1. **company_profiles**
   - `_id` (ObjectId, automatically generated)
   - `company_name` (String)
   - `website` (String)
   - `description` (String)
   - `size` (String)
   - `sector` (String)
   - `status` (String)
   - `phase` (String)

2. **investors**
   - `_id` (ObjectId, automatically generated)
   - `name` (String)
   - `email` (String)
   - `profile_picture` (String, URL)
   - `bio` (String)

3. **bookmarks**
   - `_id` (ObjectId, automatically generated)
   - `investor_id` (ObjectId, reference to investors collection)
   - `company_id` (ObjectId, reference to company_profiles collection)
   - `created_at` (Date)

4. **feed**
   - `_id` (ObjectId, automatically generated)
   - `company_id` (ObjectId, reference to company_profiles collection)
   - `title` (String)
   - `content` (String)
   - `published_at` (Date)
   - `source` (String, URL)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/startup-investor-platform.git
   cd startup-investor-platform
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   EXA_API_KEY=your_exa_api_key
   OPENAI_API_KEY=your_openai_api_key
   MONGODB_URI=your_mongodb_connection_string
   ```

4. Run the data import script:
   ```
   python data.py
   ```

5. Run the main script:
   ```
   python exa/script.py
   ```

## Usage

The current implementation includes the following functionalities:

1. Importing company data from a CSV file to MongoDB
2. Fetching company news using the Exa API
3. Generating concise social media posts from the fetched news using OpenAI's GPT-4
4. Storing the generated feed items in the MongoDB database

To use these features, you can modify the `exa/script.py` file to call the relevant functions with your desired input.

## Example Feed Post
