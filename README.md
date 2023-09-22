# to_messages
A REST api written in Django to chat

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        $ pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/shakkeelbhat/to_messages.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd to_messages
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ virtualenv  venv 
            $./venv/Scripts/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    ```
        http://127.0.0.1:8000/api/register/                            > to register
        http://127.0.0.1:8000/api/login/                               > to login
        http://127.0.0.1:8000/api/logout/                              > to logout
        http://127.0.0.1:8000/api/online-users/                        > to get online-users
        http://127.0.0.1:8000/api/chat/start/                          > to start a chat between sender and recepient
        http://127.0.0.1:8000/api/suggested-friends/<int:user_id>/     > to get a list of suggested-friends
        ws://localhost:8000/api/chat/send/                             > to test the chat channel 
    ```
