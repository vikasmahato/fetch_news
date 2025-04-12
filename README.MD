# Setup Instructions: Running `app.py` as a Service on EC2

This guide explains how to run your Flask app (`app.py`) as a background service using **Systemd** on an EC2 instance. This ensures the app starts automatically on boot and can be easily managed (start, stop, restart).

## Prerequisites
- EC2 instance running Amazon Linux, Ubuntu, or other similar Linux distributions.
- Python 3.11 installed.
- Your Flask app (`app.py`) and necessary files should be located in `/home/ec2-user/fetch_news/` (or adjust the paths accordingly).

## Steps

### 1. Upload Your Files

Ensure the following files are on your EC2 instance:
- `app.py` (Flask app)
- `output.log` (Log output)
- Any other app dependencies or folders

### 2. Create the Systemd Service File

1. SSH into your EC2 instance:
   ```bash
   ssh ec2-user@<your-ec2-public-ip>

2. Create a new Systemd service file:
    ```bash
    sudo nano /etc/systemd/system/fetch_news.service

3. Paste the following configuration (update paths where necessary):
   ```ini
   [Unit]
    Description=Fetch News Flask App
    After=network.target
    
   [Service]
    User=ec2-user
    WorkingDirectory=/home/ec2-user/fetch_news
    ExecStart=/usr/bin/python3.11 /home/ec2-user/fetch_news/app.py
    Restart=always
    StandardOutput=file:/home/ec2-user/fetch_news/output.log
    StandardError=file:/home/ec2-user/fetch_news/error.log
    Environment=PYTHONUNBUFFERED=1
    
   [Install]
    WantedBy=multi-user.target
   ```
   **Note**: Make sure that the `WorkingDirectory` and `ExecStart` paths match the actual location of your `app.py` file.

4. Save and exit the editor (CTRL + X, then Y, then Enter).

### 3. Reload Systemd and Enable the Service

Run the following commands to reload the Systemd configuration and enable your service to start on boot:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable fetch_news
```

###  4. Start the Service
To start your Flask app as a background service, run:

```bash
sudo systemctl start fetch_news
```
###  5. Verify the Service Status
Check the status of the service to ensure it's running properly:

```bash
sudo systemctl status fetch_news
```
You should see output indicating that the service is active and running. Logs will be written to `output.log` and `error.log` in your app directory.


### 6. (Optional) Check Logs
If you need to check logs while the app is running:

```bash
tail -f /home/ec2-user/fetch_news/output.log
```
Or for errors:
```bash
tail -f /home/ec2-user/fetch_news/error.log
```

### 7. Control the Service
You can stop, restart, or disable the service using these commands:

Stop the service:

```bash
sudo systemctl stop fetch_news
```
Restart the service:

```bash
sudo systemctl restart fetch_news
```

Disable the service from starting on boot:

```bash
sudo systemctl disable fetch_news
```

**Additional Notes:**
Rebooting the EC2 instance: The service will automatically start on boot if enabled.

**System resource limits:** If your app requires more resources (e.g., memory or CPU), consider adjusting the limits in the service file under the [Service] section.

**Logging:** Logs are directed to output.log and error.log. Make sure to monitor these files to ensure the app runs smoothly.

## 🛠 Handling "No Space Left on Device" Errors During Pip Install
By default, pip uses the `/tmp` directory for temporary storage during installation, which may be limited (often less than 500MB). Installing large packages like torch may fail due to insufficient space in /tmp.

✅ Fix: Use an Alternative Temp Directory
Run the following before installing:

```bash
mkdir -p ~/tmp
TMPDIR=~/tmp pip install torch
```
Or, if using a `requirements.txt`:

```bash
TMPDIR=~/tmp pip install -r requirements.txt
```
### Make It Permanent (Optional)
To always use a custom temp directory for `pip`, add the following to your shell profile:

```bash
echo 'export TMPDIR=~/tmp' >> ~/.bashrc
source ~/.bashrc
```
For zsh users:

```bash
echo 'export TMPDIR=~/tmp' >> ~/.zshrc
source ~/.zshrc
```
This ensures pip uses your home directory (which has more space) instead of the limited `/tmp`.

