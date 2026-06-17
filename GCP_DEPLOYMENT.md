# 🚀 Deploy CarbonSense AI to Google Cloud Platform (GCP)

This guide will walk you through deploying the entire CarbonSense AI stack to GCP using **Cloud Run** (serverless containers) and **Cloud SQL** (managed PostgreSQL)!


## Prerequisites
1. A GCP Account
2. `gcloud` CLI installed locally (https://cloud.google.com/sdk/docs/install)
3. Docker installed locally
4. Your code is on GitHub (we already did this!)


## Step 1: Set up GCP Project
1. Go to https://console.cloud.google.com
2. Create a new project (or use an existing one!)
3. Note your Project ID (we'll need this!)
4. Open Cloud Shell in GCP Console (the little terminal icon at top right!)


## Step 2: Enable Required GCP Services
Run these commands in Cloud Shell (or your local terminal with `gcloud`):
```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```


## Step 3: Create a Cloud SQL PostgreSQL Instance
Run this in Cloud Shell to create a database:
```bash
# Set variables
export DB_INSTANCE="carbonsense-db"
export DB_NAME="carbonsense"
export DB_USER="carbonsense"
export DB_PASS="change-this-to-a-strong-password"
export REGION="us-central1"

# Create Cloud SQL instance
gcloud sql instances create $DB_INSTANCE \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password=$DB_PASS

# Create database inside instance
gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE

# Create a database user
gcloud sql users create $DB_USER --instance=$DB_INSTANCE --password=$DB_PASS
```


## Step 4: Build & Push Docker Containers to Artifact Registry
We need to store our Docker images in GCP's Artifact Registry!

### 4.1 Create Artifact Registry Repository
```bash
# Create repo
gcloud artifacts repositories create carbonsense-repo \
  --repository-format=docker \
  --location=$REGION \
  --description="CarbonSense Docker images"

# Configure Docker to use gcloud credentials
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

### 4.2 Build & Push Backend Image
From your project root directory:
```bash
# Build backend image
cd backend
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-backend:latest .

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-backend:latest
cd ..
```

### 4.3 Build & Push Frontend Image
```bash
cd frontend
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-frontend:latest .

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-frontend:latest
cd ..
```


## Step 5: Deploy Backend to Cloud Run
Let's deploy the backend container to Cloud Run!
```bash
export BACKEND_SERVICE_NAME="carbonsense-backend"
export DB_URL="postgresql://${DB_USER}:${DB_PASS}@//cloudsql/${PROJECT_ID}:${REGION}:${DB_INSTANCE}/${DB_NAME}"
export JWT_SECRET="your-super-secret-random-key-here-make-it-long"

# Deploy backend to Cloud Run
gcloud run deploy $BACKEND_SERVICE_NAME \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-backend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${DB_INSTANCE} \
  --set-env-vars DATABASE_URL=$DB_URL \
  --set-env-vars SECRET_KEY=$JWT_SECRET \
  --set-env-vars "BACKEND_CORS_ORIGINS=https://your-frontend-url.a.run.app,http://localhost:3000"

# After deployment, note the backend URL!
# It should look like: https://carbonsense-backend-xyz.a.run.app
```


## Step 6: Update & Deploy Frontend
1. First, update your frontend's `.env.production` to point to your Cloud Run backend URL!
2. Rebuild and push the frontend image!
3. Deploy to Cloud Run:
```bash
export FRONTEND_SERVICE_NAME="carbonsense-frontend"
export BACKEND_URL="https://your-backend-url.a.run.app"  # Replace with your backend URL from step 5

# Deploy frontend
gcloud run deploy $FRONTEND_SERVICE_NAME \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/carbonsense-repo/carbonsense-frontend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars VITE_API_URL=$BACKEND_URL

# After deployment, note the frontend URL!
```


## Step 7: Update CORS in Backend
Don't forget to go back to step 5 and update `BACKEND_CORS_ORIGINS` to include your new frontend URL!


## Step 8: Verify Your Deployment
1. Open your frontend URL in a browser!
2. Register a test user!
3. Check if everything is working!


## Optional: Set Up Custom Domain (Optional)
If you want a custom domain (like `yourdomain.com`):
1. Buy a domain from Google Domains or another provider!
2. Follow these instructions to map custom domains to Cloud Run services!
https://cloud.google.com/run/docs/mapping-custom-domains


## Cleanup (If You Want to Delete Everything Later)
```bash
# Delete Cloud Run services
gcloud run services delete $BACKEND_SERVICE_NAME --region $REGION --quiet
gcloud run services delete $FRONTEND_SERVICE_NAME --region $REGION --quiet

# Delete Cloud SQL instance
gcloud sql instances delete $DB_INSTANCE --quiet

# Delete Artifact Registry repo
gcloud artifacts repositories delete carbonsense-repo --location $REGION --quiet
```


## Tips for Production
- [ ] Enable HTTPS for everything (Cloud Run does this by default!)
- [ ] Use Secret Manager to store your `SECRET_KEY` and DB password instead of env vars!
- [ ] Set up Cloud SQL backups!
- [ ] Add monitoring with Cloud Monitoring!


## Troubleshooting Common Issues
- Backend can't connect to Cloud SQL? Make sure you added the `--add-cloudsql-instances` flag correctly!
- CORS errors? Double-check `BACKEND_CORS_ORIGINS` includes your frontend URL exactly!
- Container not starting? Check logs: `gcloud run services logs read $BACKEND_SERVICE_NAME --region $REGION`
