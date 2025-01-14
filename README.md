# Trusted Lodger

![Trusted Lodger Responsive Screenshot](documentation/final_views/trustedlodger_amiresponsive.png)

## Introduction

Trusted Lodger is a web-based platform designed to connect lodgers with homesharers in the UK. The platform uses AI-powered matching to pair individuals based on personality types and lifestyle preferences, ensuring harmonious living arrangements. Built with Django/Python, HTML/CSS, and JavaScript, the platform is hosted on Heroku and integrates with HubSpot for CRM and marketing automation. PostgreSQL is used as the database for secure and scalable data storage.

View live site here: [Trusted Lodger](https://trustedlodger.herokuapp.com/)  

For Admin access with relevant sign-in information: [Trusted Lodger Admin](https://trustedlodger.herokuapp.com/admin/)

<hr>

## Table of Contents

- [Trusted Lodger](#trusted-lodger)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
- [UX - User Experience](#ux---user-experience)
  - [Design Inspiration](#design-inspiration)
    - [Colour Scheme](#colour-scheme)
    - [Font](#font)
- [Project Planning](#project-planning)
  - [Strategy Plane](#strategy-plane)
    - [Site Goals](#site-goals)
  - [Agile Methodologies - Project Management](#agile-methodologies---project-management)
    - [MoSCoW Prioritization](#moscow-prioritization)
    - [Sprints](#sprints)
  - [User Stories](#user-stories)
  - [Scope Plane](#scope-plane)
  - [Structural Plane](#structural-plane)
  - [Skeleton \& Surface Planes](#skeleton--surface-planes)
    - [Wireframes](#wireframes)
    - [Database Schema - Entity Relationship Diagram](#database-schema---entity-relationship-diagram)
    - [Security](#security)
- [Features](#features)
  - [User View - Lodgers and Homesharers](#user-view---lodgers-and-homesharers)
  - [CRUD Functionality](#crud-functionality)
  - [Feature Showcase](#feature-showcase)
  - [Future Features](#future-features)
- [Technologies \& Languages Used](#technologies--languages-used)
  - [Libraries \& Frameworks](#libraries--frameworks)
  - [Tools \& Programs](#tools--programs)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Connecting to GitHub](#connecting-to-github)
  - [Django Project Setup](#django-project-setup)
  - [Cloudinary API](#cloudinary-api)
  - [Elephant SQL](#elephant-sql)
  - [Heroku Deployment](#heroku-deployment)
  - [Clone Project](#clone-project)
  - [Fork Project](#fork-project)
- [Credits](#credits)
  - [Code](#code)
  - [Media](#media)
  - [Acknowledgements](#acknowledgements)

---

## Overview

Trusted Lodger is a platform that connects lodgers and homesharers through personality-based matching. Users can:

- Create profiles and list rooms.
- Use a personality questionnaire to find compatible matches.
- Manage listings, matches, and subscriptions.
- Access secure payment processing and background checks.

The platform is accessible via all browsers and is fully responsive on different screen sizes. Its goal is to create a safe, trustworthy environment for homesharing in the UK.

---

## UX - User Experience

### Design Inspiration

The design of Trusted Lodger focuses on professionalism, trust, and simplicity. The platform uses a clean layout with intuitive navigation to ensure a seamless user experience.

#### Colour Scheme

The colour scheme will be finalized soon, but it will reflect the brand's values of trust, professionalism, and warmth. Placeholder colours include:

- **Primary Colour**: #007BFF (Blue for trust and reliability)
- **Secondary Colour**: #F4F4F4 (Light grey for simplicity and cleanliness)
- **Accent Colour**: #FFC107 (Yellow for warmth and friendliness)

#### Font

The font choices will be provided soon. Placeholder fonts include:

- **Primary Font**: Open Sans (for readability and professionalism)
- **Secondary Font**: Montserrat (for headings and emphasis)

---

## Project Planning

### Strategy Plane

The goal of Trusted Lodger is to create a platform that simplifies the process of finding compatible housemates while ensuring trust and security.

#### Site Goals

- Provide a seamless user experience for lodgers and homesharers.
- Build trust through personality-based matching and secure payments.
- Offer value-added services like background checks and contract drafting.

### Agile Methodologies - Project Management

Trusted Lodger follows Agile methodologies, with tasks organized into sprints and prioritized using the MoSCoW framework.

#### MoSCoW Prioritization

- **Must-Have**: Profile creation, room listings, personality matching, secure payments.
- **Should-Have**: Saved listings, boosted listings, advanced filters.
- **Could-Have**: Personalized recommendations, eco-friendly filters.
- **Won’t-Have**: Virtual tours (for now).

#### Sprints

| Sprint No. | Sprint Content                | Start/Finish Dates |
|------------|-------------------------------|--------------------|
| #1         | Project Setup                 | TBD                |
| #2         | User Authentication           | TBD                |
| #3         | Profile and Listings Features | TBD                |
| #4         | Personality Matching          | TBD                |
| #5         | Testing and Deployment        | TBD                |

---

### User Stories

| User Story | Priority |
|------------|----------|
| As a lodger, I want to create a profile quickly so that I can start searching for rooms immediately. | Must-Have |
| As a homesharer, I want to list my room with detailed information so that I can attract suitable lodgers. | Must-Have |
| As a user, I want to create a personalised profile so that I can be matched with other users effectively. | Must-Have |
| As a lodger, I want to see matches ranked by compatibility so that I can find the best options. | Must-Have |

---

### Scope Plane

The initial scope includes core features like profile creation, room listings, and personality matching. Advanced features like AI-powered recommendations will be added in future updates.

---

### Structural Plane

The platform's structure is designed for scalability, with separate dashboards for lodgers and homesharers. The navigation is intuitive, with clear CTAs for key actions.

---

### Skeleton & Surface Planes

#### Wireframes

Wireframes for Trusted Lodger include layouts for the homepage, dashboards, and matching questionnaire. [View Wireframes](#).

#### Database Schema - Entity Relationship Diagram

![ERD Image](/workspace/trusted-lodger/images/ERD.png)

---

## ERD Database Table Structure

Here’s the proposed database table structure:

### 1. Users Table
Stores information about all users (lodgers and homesharers).

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| user_id             | UUID      | Primary key, unique identifier for each user.        |
| first_name          | VARCHAR(50)| User's first name.                                   |
| last_name           | VARCHAR(50)| User's last name.                                    |
| email               | VARCHAR(100)| User's email address (unique).                       |
| password            | VARCHAR(255)| Hashed password for authentication.                  |
| user_type           | ENUM      | Lodger or homesharer.                                |
| date_joined         | TIMESTAMP | Date and time the user registered.                   |
| subscription_plan    | ENUM      | Free, Silver, Gold, or Premium.                      |

### 2. Lodger Profiles Table
Stores additional details specific to lodgers.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| lodger_id           | UUID      | Foreign key referencing user_id in Users.            |
| preferences         | JSON      | Lodger's preferences (e.g., location, budget).      |
| personality_traits   | JSON      | Personality traits for AI matching.                   |
| saved_listings      | JSON      | List of saved room listings.                          |

### 3. Homesharer Profiles Table
Stores additional details specific to homesharers.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| homesharer_id       | UUID      | Foreign key referencing user_id in Users.            |
| property_count      | INT       | Number of properties listed by the homesharer.       |
| boost_status        | BOOLEAN   | Whether the homesharer's listing is boosted.         |

### 4. Room Listings Table
Stores details about rooms listed by homesharers.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| listing_id          | UUID      | Primary key, unique identifier for each listing.     |
| homesharer_id       | UUID      | Foreign key referencing homesharer_id.               |
| rent                | DECIMAL(10,2)| Monthly rent for the room.                          |
| location            | VARCHAR(255)| Address or general location of the room.            |
| house_rules         | TEXT      | Rules set by the homesharer.                         |
| eco_friendly        | BOOLEAN   | Whether the property is eco-friendly.                |
| availability        | BOOLEAN   | Whether the room is currently available.             |

### 5. Matches Table
Stores AI-powered matches between lodgers and homesharers.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| match_id            | UUID      | Primary key, unique identifier for each match.       |
| lodger_id           | UUID      | Foreign key referencing lodger_id.                   |
| listing_id          | UUID      | Foreign key referencing listing_id.                   |
| compatibility_score  | DECIMAL(5,2)| Compatibility score between lodger and listing.     |
| match_date          | TIMESTAMP | Date and time the match was created.                 |

### 6. Payments Table
Tracks payment transactions for subscriptions and upgrades.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| payment_id          | UUID      | Primary key, unique identifier for each payment.     |
| user_id             | UUID      | Foreign key referencing user_id.                      |
| amount              | DECIMAL(10,2)| Payment amount.                                     |
| payment_date        | TIMESTAMP | Date and time of the payment.                         |
| payment_method      | ENUM      | Payment method (e.g., Stripe, PayPal).               |
| subscription_type    | ENUM      | Free, Silver, Gold, or Premium.                      |

### 7. Reviews Table
Stores reviews left by lodgers and homesharers.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| review_id           | UUID      | Primary key, unique identifier for each review.      |
| reviewer_id         | UUID      | Foreign key referencing user_id.                      |
| reviewee_id         | UUID      | Foreign key referencing user_id.                      |
| rating              | INT       | Rating out of 5.                                     |
| comments            | TEXT      | Review comments.                                     |
| review_date         | TIMESTAMP | Date and time the review was submitted.              |

### 8. Support Tickets Table
Tracks user support and dispute resolution.

| Field Name          | Data Type | Description                                           |
|---------------------|-----------|-------------------------------------------------------|
| ticket_id           | UUID      | Primary key, unique identifier for each ticket.      |
| user_id             | UUID      | Foreign key referencing user_id.                      |
| issue_type          | ENUM      | Type of issue (e.g., payment, listing, other).       |
| description         | TEXT      | Detailed description of the issue.                    |
| status              | ENUM      | Open, In Progress, Resolved.                          |
| created_at          | TIMESTAMP | Date and time the ticket was created.                |
| resolved_at         | TIMESTAMP | Date and time the ticket was resolved.               |

### Relationships
1. **Users:**
   - One-to-one relationship with Lodger Profiles and Homesharer Profiles.
   - One-to-many relationship with Room Listings, Payments, Reviews, and Support Tickets.
   
2. **Room Listings:**
   - One-to-many relationship with Matches.
   
3. **Matches:**
   - Many-to-one relationship with Lodger Profiles and Room Listings.
   
4. **Payments:**
   - Many-to-one relationship with Users.
   
5. **Reviews:**
   - Many-to-one relationship with Users (reviewer and reviewee).
   
6. **Support Tickets:**
   - Many-to-one relationship with Users.

## Features

### User View - Lodgers and Homesharers

| Feature   | Lodger View | Homesharer View |
|-----------|-------------|-----------------|
| Dashboard | View matches and saved listings | Manage room listings and view potential lodgers |
| Listings  | Search and save room listings | Create and edit room listings |
| Matching  | Personality-based matching | View compatibility scores |

---

### CRUD Functionality

| Feature | Create | Read | Update | Delete |
|---------|--------|------|--------|--------|
| Profile | Yes    | Yes  | Yes    | Yes    |
| Listings| Yes    | Yes  | Yes    | Yes    |
| Matches | Yes    | Yes  | No     | No     |

---

### Feature Showcase

- **Personality Matching**: Users answer a questionnaire to find compatible matches.
- **Secure Payments**: Integrated with Stripe for subscription management.
- **Boosted Listings**: Homesharers can upgrade their listings for better visibility.

---

### Future Features

- AI-powered recommendations.
- Virtual tours for room listings.
- Expansion to Europe and North America.

---

## Technologies & Languages Used

- **Languages**: HTML, CSS, JavaScript, Python.
- **Frameworks**: Django, Bootstrap.
- **Database**: PostgreSQL.
- **Hosting**: Heroku.

---

## Deployment

### Connecting to GitHub

1. Create a new repository on GitHub.
2. Clone the repository to your local machine.
3. Push your project files to GitHub.

### Django Project Setup

1. Install Django and dependencies.
2. Set up the database with PostgreSQL.
3. Configure the project for Heroku deployment.

---

## Credits

### Code

- Django documentation.
- Bootstrap documentation.

### Media

- Placeholder images from Unsplash.

### Acknowledgements

- Thanks to the Code Institute for guidance and support.
