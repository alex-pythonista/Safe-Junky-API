## Safe Junkey API server 
---
### Installation
1. Make a virtual environment
    ```bash
    python3 -m venv venv
    ```
2. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Download the **.env** file from [here](https://drive.google.com/file/d/1JvT6dEh5RGB2zyXTNO1BgvMqItFeHBxF/view?usp=sharing) and place it in the root directory.
4. Run a migration
    ```bash
    python3 manage.py migrate
    ```
5. Run the server
    ```bash
    python3 manage.py runserver
    ```
