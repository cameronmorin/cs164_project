# CS 164 Final Project
> Cameron Morin

## Objective

Implement both server and client side for a terminal based social media.

## Implementations

* User
    * Create user with unique username and password
        * User can change password when logged in :yum:
    * Ability to add friends
        * User can view list of friends and their online status
        * Friend removal to be added
    * Ability to send messages to other users
        * Do not need to be friends to message the user
        * Can broadcast a message to all connected users
        * Message will appear in realtime if the user is online
        * Message will be archieved and available when the user logs in
    * Timeline
        * User can add posts to their timeline for their friends to see
        * Timeline is output in chronoilogical order
* Landing Page
    * User is prompted with a landing page where they can choose to login or exit the server
        * User creation to be added
* Menu
    * When logged in, the user is prompted with the main menu
        * The main menu has the following options:
            1. Change password
            2. Send message
            3. Read unread messages
            4. Send broadcast message
            5. See friends
            6. Send friend request
            7. Respond to friend requests
            8. Post status
            9. See timeline
        * The menu also gives the user the option to sign out

## Future Plans

I plan on implementing the functions as user class functions so that the code is ***cleaner*** and ***easier to read***.

## Closing Statement

All code in this project is original and the intellectual property of __Cameron Morin__. Any reuse of this code for future projects is ***strongly*** discouraged. I had a lot of fun working on this project, and I hope to explore more production-based projects in the future! :rocket:
