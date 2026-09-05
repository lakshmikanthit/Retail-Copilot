# 🚀 PythonAnywhere Deployment Guide for Retail Copilot

## 📋 Prerequisites
- PythonAnywhere account (free tier available)
- GitHub repository: https://github.com/lakshmikanthit/Retail-Copilot.git
- GEMINI_API_KEY from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Verify your email address

### Step 2: Create a New Web App
1. Go to the **Web** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Click **Next** to choose a framework
4. Select **Django**
5. Choose **Python 3.11** (or latest available)
6. Click **Next**
7. Set project path: `/home/YOUR_USERNAME/Retail-Copilot`
8. Click **Next** (skip manual configuration for now)

### Step 3: Clone Your Repository
In the PythonAnywhere **Bash** console (click "Bash" icon):
```bash
cd ~
git clone https://github.com/lakshmikanthit/Retail-Copilot.git
cd Retail-Copilot
```

### Step 4: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.11 retailcopilot
workon retailcopilot
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Set Environment Variables
In the PythonAnywhere Web tab:
1. Scroll to **"Environment variables"** section
2. Add the following variables:
   - `GEMINI_API_KEY`: Your actual Gemini API key
   - `DJANGO_SECRET_KEY`: Generate a secure secret key (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `YOUR_USERNAME.pythonanywhere.com`

### Step 7: Configure WSGI File
1. In the **Web** tab, scroll to **"WSGI configuration file"**
2. Click the link to edit the WSGI file
3. Replace the content with:

```python
import os
import sys

path = '/home/YOUR_USERNAME/Retail-Copilot'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_copilot.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `YOUR_USERNAME` with your actual PythonAnywhere username!

### Step 8: Run Database Migrations
In the Bash console:
```bash
cd ~/Retail-Copilot
workon retailcopilot
python manage.py migrate
```

### Step 9: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin credentials.

### Step 10: Generate Sample Data
```bash
python manage.py generate_sample_data
python manage.py generate_alerts
```

### Step 11: Collect Static Files
```bash
python manage.py collectstatic
```
Type `yes` when prompted.

### Step 12: Configure Static Files in PythonAnywhere
1. In the **Web** tab, scroll to **"Static files"** section
2. Add:
   - **URL**: `/static/`
   - **Directory**: `/home/YOUR_USERNAME/Retail-Copilot/staticfiles`

### Step 13: Reload the Web App
1. In the **Web** tab, click the **"Reload"** button at the top
2. Wait for the reload to complete

### Step 14: Test Your Deployment
1. Click your web app URL (e.g., `https://YOUR_USERNAME.pythonanywhere.com`)
2. You should see the Retail Copilot dashboard
3. Test login with your superuser credentials
4. Test the AI copilot and alerts functionality

---

## 🔧 Troubleshooting

### Issue: 500 Internal Server Error
**Solution**: Check the error log in the Web tab → "Log files" → "Error log"

### Issue: Static files not loading
**Solution**: Ensure static files are collected and configured correctly in the Web tab

### Issue: Database migrations fail
**Solution**: Make sure you're in the virtual environment and in the correct directory

### Issue: Permission denied
**Solution**: Use the Bash console and ensure you have proper file permissions

### Issue: Import errors
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

---

## 📝 Post-Deployment Checklist

- [ ] Web app loads without errors
- [ ] Static files (CSS, JS) load correctly
- [ ] Database migrations applied successfully
- [ ] Can log in with superuser account
- [ ] Dashboard displays correctly
- [ ] AI copilot responds to questions
- [ ] Inventory alerts generate and display
- [ ] Charts render properly
- [ ] User registration works
- [ ] Environment variables are set correctly

---

## 🔐 Security Notes

1. **Never commit** your actual `DJANGO_SECRET_KEY` or `GEMINI_API_KEY` to GitHub
2. Use `DEBUG=False` in production
3. Keep your PythonAnywhere account secure with a strong password
4. Regularly update dependencies: `pip install --upgrade -r requirements.txt`

---

## 🌐 Access Your Application

Your app will be available at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

For free tier, your custom domain would be:
```
YOUR_USERNAME.pythonanywhere.com
```

---

## 📚 Additional Resources

- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/Django/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [PythonAnywhere Documentation](https://help.pythonanywhere.com/)

---

## 🎉 Success!

Your Retail Copilot is now live on PythonAnywhere! Share your URL with the hackathon judges and users.
