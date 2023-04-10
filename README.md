## Safe Junkey API server 
---
### Installation
1. Make a virtual environment
    ```bash
    python3 -m venv venv
    ```
    and activate it
    ```bash
    source venv/bin/activate
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

# On the Azure server
1. Fist of all, you need to install the requirements and migrate
    ```bash
    pip install -r requirements.txt
    python3 manage.py migrate
    ```
2. Restart the gunicorn server
    ```bash
    sudo systemctl restart gunicorn
    sudo systemctl daemon-reload
    ```
3. Restart the nginx server
    ```bash
    sudo systemctl restart nginx
    ```
4. Restart the celery server
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start celery-worker
    ```
    - for stoping the celery server
        ```bash
        sudo supervisorctl stop celery-worker
        ```
5. See the celery logs
    ```bash
    sudo tail -n 50 /var/log/celery/worker.log
    ```

### For debugging 
1. See the nginx logs
    ```bash
    sudo tail -f /var/log/nginx/access.log > /home/adib-safe-junkey/logs.txt
    
    sudo tail -f /var/log/nginx/access.log | tee /home/adib-safe-junkey/logs.txt
    ```