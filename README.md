# About
Simple Django-based backend for a questionnaire game for a 24 hour hackathon at Eventbrite HQ.

Although built for a hackathon, the code has good test coverage. 

# API docs
## Join [/join]
### Joining a session [POST]

+ Request (application/json)

        {
        "game_id": game_id,
        "player_id": player_id
        }
        
+ Response 200 (application/json)

        {"status": "unavailable", "num_answered": 0, "players": [1, 21, 22], "game": null, "questions": [], "id": 1}


+ Response 200 (application/json)

        {"status": "available", "num_answered": 0, "players": [1, 21, 22], "game": null, "questions": [], "id": 1}
        


## Player [/create_game]

### Create new player [POST]
+ Request (application/json)

        {
        }
        
+ Response 200 (application/json)

        {"id": 3}
        
## Player [/create_player]

### Create new player [POST]
+ Request (application/json)

        {
        }
        
+ Response 200 (application/json)

        {"points": 0, "id": 30, "prize": []}

## Session [/session]

### Get the session data [GET]
+ Request (application/json)

        {
        "session_id": session_id
        }
        
+ Response 200 (application/json)

         {"pk": 321, "model": "api.session", "player_count": 0, "fields": {"status": "unavailable", "players": [], "game": null, "questions": []}}

+ Response 200 (application/json)

         {"pk": 321, "model": "api.session", "player_count": 0, "fields": {"status": "available", "players": [], "game": null, "questions": []}}

## Question endpoint [/question]
### Get a question [POST]

+ Request (application/json)

        {
        "session_id": session_id,
        }
        
+ Response 200 (application/json)

        {"third_option": "2000", "first_option": "400", "text": "How many people signed up for this event", "second_option": "500", "fourth_option": "1000", "answer": 1, "id": 2}
        

## Results endpoint [/results]
### Results [GET]
+ Request (application/json)

        {
        "session_id": session_id
        }
        
+ Response 200 (application/json)

        [{"points": 0, "id": 1, "prize": []}, {"points": 0, "id": 21, "prize": []}, {"points": 0, "id": 22, "prize": []}]

## Answer endpoint [/answer]
### Answering [POST]

+ Request (application/json)

        {
        "session_id": session_id,
        "player_id": player_id,
        "answer": answer
        }
        
+ Response 200 (application/json)

        [{"model": "api.question", "pk": 2, "fields": {"text": "", "answer": 3, "first_option": "", "second_option": "", "third_option": ""}]
