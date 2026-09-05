# 🚀 Render Deployment Guide for Retail Copilot

## 📋 Prerequisites
- Render account (free tier available)
- GitHub repository: https://github.com/lakshmikanthit/Retail-Copilot.git
- GEMINI_API_KEY from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up for a free account (use GitHub for easy authentication)
3. Verify your email address

### Step 2: Connect GitHub Repository
1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"** (if not already connected)
3. Authorize Render to access your GitHub account
4. Select the **Retail-Copilot** repository
5. Click **"Connect"**

### Step 3: Configure Web Service
Fill in the following settings:

**Basic Configuration:**
- **Name**: `retail-copilot` (or your preferred name)
- **Region**: Choose the closest region to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repository)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn retail_copilot.wsgi:application`

**Advanced Configuration:**
- **Instance Type**: Free (for hackathon demo)
- **RAM**: 512 MB (free tier)
- **CPU**: 0.1 (free tier)

### Step 4: Add Environment Variables
Scroll to **"Environment Variables"** section and add:

1. **GEMINI_API_KEY**
   - Value: Your actual Gemini API key from Google AI Studio
   - **Important**: Keep this secret!

2. **DJANGO_SECRET_KEY**
   - Value: Click "Generate" button or use a secure key
   - To generate locally: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

3. **DEBUG**
   - Value: `False`

4. **ALLOWED_HOSTS**
   - Value: Leave empty (will be auto-configured by Render)

### Step 5: Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. **Name**: `retail-copilot-db`
3. **Database Name**: `retail_copilot`
4. **User**: `retail_copilot_user`
5. **Region**: Same as your web service
6. **Instance Type**: Free (for hackathon demo)
7. Click **"Create Database"**

### Step 6: Link Database to Web Service
1. Go back to your web service configuration
2. Scroll to **"Environment Variables"**
3. Add a new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Select from the dropdown: `retail-copilot-db → Connection String`

### Step 7: Deploy
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Start the application
3. Wait for the deployment to complete (usually 2-5 minutes)

### Step 8: Generate Sample Data
After deployment is successful:
1. Go to your web service in Render
2. Click **"Shell"** tab
3. Run the following commands:
```bash
python manage.py generate_sample_data
python manage.py generate_alerts
```

### Step 9: Create Admin User
In the Render Shell:
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin credentials.

### Step 10: Access Your Application
1. Your app URL will be: `https://retail-copilot.onrender.com`
2. Or click the URL in the Render dashboard
3. You should see the Retail Copilot dashboard
4. Log in with your superuser credentials

---

## 🔧 Troubleshooting

### Issue: Deployment Fails
**Solution**: Check the deployment logs in Render dashboard for specific error messages

### Issue: Database Connection Error
**Solution**: Ensure `DATABASE_URL` environment variable is correctly linked to your PostgreSQL database

### Issue: Static Files Not Loading
**Solution**: Ensure `collectstatic` runs successfully during deployment

### Issue: 500 Internal Server Error
**Solution**: Check the Render logs and ensure all environment variables are set correctly

### Issue: Permission Denied
**Solution**: Ensure your database user has proper permissions

### Issue: Migrations Fail
**Solution**: Check that the database is empty and the user has CREATE TABLE permissions

---

## 📝 Post-Deployment Checklist

- [ ] Web service deployed successfully
- [ ] PostgreSQL database created and linked
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Sample data generated
- [ ] Admin user created
- [ ] Application loads without errors
- [ ] Can log in with admin credentials
- [ ] Dashboard displays correctly
- [ ] AI copilot responds to questions
- [ ] Inventory alerts generate and display
- [ ] Charts render properly
- [ ] User registration works

---

## 🔐 Security Notes

1. **Never commit** your actual `DJANGO_SECRET_KEY` or `GEMINI_API_KEY` to GitHub
2. Use `DEBUG=False` in production
3. Keep your Render account secure with 2FA
4. Regularly update dependencies
5. Use strong passwords for admin accounts

---

## 🌐 Access Your Application

Your app will be available at:
```
https://retail-copilot.onrender.com
```

Or your custom service name:
```
https://YOUR-SERVICE-NAME.onrender.com
```

---

## 💰 Free Tier Limitations

Render's free tier includes:
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ PostgreSQL database (90 day limit for free)
- ✅ Automatic SSL/HTTPS
- ✅ Custom domain support (paid)

**Note**: Free tier services spin down after 15 minutes of inactivity and take ~30 seconds to wake up.

---

## 📚 Additional Resources

- [Render Django Documentation](https://render.com/docs/deploy-django)
- [Render PostgreSQL Guide](https://render.com/docs/databases)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)

---

## 🎉 Success!

Your Retail Copilot is now live on Render! Share your URL with the hackathon judges and users.

---

## 🔄 Alternative: Use render.yaml

If you prefer infrastructure-as-code, you can use the included `render.yaml` file:

1. Push your code to GitHub
2. In Render, click **"New +"** → **"Blueprint"**
3. Select your repository
4. Render will automatically create web service and database based on `render.yaml`
5. Add your `GEMINI_API_KEY` environment variable manually
6. Deploy!

This is the fastest way to deploy if you want to avoid manual configuration.
