# Pain Study


## Backend

The backend is implemented using the **FastAPI** package in **Python**. To run the `main.py` file:  
1. **Install all required packages** as mentioned in the main.py.  
2. Execute the following command in the terminal:  
   ```bash
   uvicorn main:app --reload
   
## Backend - completed version
（Updated on Jan 18, 2025）
1. Execute the following command in the terminal:  
   ```bash
   uvicorn main_final:app --reload

## Frontend

The frontend is developed using **Vue**, a JavaScript-based framework. To run the application:  
1. Open a terminal in the frontend directory.  
2. Execute the following command:  
   ```bash
   npm run serve

## MySQL Database
（Updated on Jan 18, 2025）
The first step is to create the database named `pain_study`.

```sql
CREATE DATABASE `pain_study`;

**Table Definition**
1. question_table
This table stores information about the questions in the study.
```sql
CREATE TABLE `question_table` (
  `question_id` int NOT NULL,
  `question_type` varchar(100) NOT NULL,
  `question` mediumtext NOT NULL,
  `options` mediumtext,
  `logic` mediumtext,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

2. user_data
This table stores user-specific data like weight and height.
```sql
CREATE TABLE `user_data` (
  `username` varchar(100) NOT NULL,
  `weight_lbs` float DEFAULT NULL,
  `height_feet` float DEFAULT NULL,
  `height_inches` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

3. user_response
This table stores the responses given by users during the study.
```sql
CREATE TABLE `user_response` (
  `response_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `new_user` tinyint(1) NOT NULL,
  `answer1` mediumtext,
  `answer2` mediumtext,
  `answer3` mediumtext,
  `answer4` mediumtext,
  `answer5` mediumtext,
  `answer6` mediumtext,
  `answer7` mediumtext,
  `answer8` mediumtext,
  `answer9` mediumtext,
  `answer10` mediumtext,
  `answer11` mediumtext,
  `answer12` mediumtext,
  `answer13` mediumtext,
  `answer14` mediumtext,
  `answer15` mediumtext,
  `answer16` mediumtext,
  `answer17` mediumtext,
  `answer18` mediumtext,
  `answer19` mediumtext,
  `answer20` mediumtext,
  `answer21` mediumtext,
  `answer22` mediumtext,
  `answer23` mediumtext,
  `answer24` mediumtext,
  `answer25` mediumtext,
  `answer26` mediumtext,
  `answer27` mediumtext,
  `answer28` mediumtext,
  `answer29` mediumtext,
  `answer30` mediumtext,
  `answer31` mediumtext,
  `answer32` mediumtext,
  `answer33` mediumtext,
  `answer34` mediumtext,
  `answer35` mediumtext,
  `answer36` mediumtext,
  `start_dt` datetime NOT NULL,
  `submited_dt` datetime NOT NULL,
  PRIMARY KEY (`response_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

4. user_table
This table stores information about the users who participate in the study.
```sql
CREATE TABLE `user_table` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `user_email` varchar(100) DEFAULT NULL,
  `created_dt` datetime NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

## Suggestions for testing

To facilitate testing and frontend improvements, I have included one example for each question type to demonstrate the different types of questions.

Question 1 is a **multi-choice question**:
   - If you select any of the first three options, it will redirect to a **VAS question**.  
   - If you select the last option, it will redirect to a **text question**. After the text question, the flow will proceed to a **BMI question**.



Let me know if you have any questions or need further assistance.

