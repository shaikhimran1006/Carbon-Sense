# 🚀 Deploy CarbonSense AI to Google Cloud Platform (GCP)

## ✨ NO LOCAL DOCKER/INSTALLS NEEDED! (ALL-WEB-CONSOLE GUIDE!)

This guide uses **only the GCP Web Console**—no Docker, no `gcloud` CLI, no local tools! Perfect for when you don't have time to install anything!

## Prerequisites

1. A GCP Account (free tier works for testing!)
2. Your code already pushed to GitHub (we did this already!)

## Step 1: Set Up Your GCP Project

1. Go to https://console.cloud.google.com/
2. Click **"Create Project"** (or select an existing one)
3. Name your project (e.g., "carbonsense-ai-12345")
4. Note your **Project ID** (top left corner of the console, next to the project name!)

## Step 2: Enable Required GCP APIs

1. In GCP Console, open **APIs & Services > Library** (left sidebar!)
2. Search for and enable each of these APIs by clicking "Enable":
   - **Cloud Run Admin API**
   - **Cloud SQL Admin API**
   - **Cloud Build API**
   - **Artifact Registry API**
   - **Cloud Source Repositories API**

## Step 3: Create Cloud SQL PostgreSQL Database

1. In GCP Console, go to **SQL** (left sidebar!)
2. Click **"Create Instance"**
3. Select **PostgreSQL**
4. Fill in the form:
   - **Instance ID**: `carbonsense-db`
   - **Password**: Choose a strong password (save this!)
   - **Database version**: PostgreSQL 15
   - **Region**: Pick one close to you (e.g., `us-central1`)
   - **Zonal availability**: Single zone (cheaper for testing!)
   - **Machine configuration**: Choose **"Shared core" > "1 vCPU, 0.614 GB" (db-f1-micro)**
5. Click **"Create Instance"** (takes ~5 mins!)
6. After it's ready:
   - Go to **"Databases"** tab > Click **"Create Database"**
   - Name: `carbonsense` > Click "Create"
   - Go to **"Users"** tab > Click **"Add User Account"**
   - Username: `carbonsense` > Password: (same as before) > Click "Add"

## Step 4: Connect Your GitHub Repo to Cloud Build

We'll use Cloud Build to build containers from your GitHub repo—no local Docker needed!

1. In GCP Console, go to **Cloud Build > Repositories** (left sidebar!)
2. Click **"Connect Repository"**
3. Select **GitHub**
4. Authenticate with GitHub, select your repo, and click **"Connect"**
5. (Don't create a trigger yet—we'll do that manually!)

## Step 5: Add Cloud Build Config Files to GitHub

Let's add these two files to your repo (edit directly in GitHub if you want!):

### File 1: `backend/cloudbuild.yaml`

```yaml
# backend/cloudbuild.yaml
steps:
  - name: "gcr.io/cloud-builders/docker"
    args:
      [
        "build",
        "-t",
        "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-backend:latest",
        ".",
      ]
  - name: "gcr.io/cloud-builders/docker"
    args:
      [
        "push",
        "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-backend:latest",
      ]
images:
  - "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-backend:latest"
```

(Change `us-central1` to your region if needed!)

### File 2: `frontend/cloudbuild.yaml`

```yaml
# frontend/cloudbuild.yaml
steps:
  - name: "gcr.io/cloud-builders/docker"
    args:
      [
        "build",
        "-t",
        "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-frontend:latest",
        ".",
      ]
  - name: "gcr.io/cloud-builders/docker"
    args:
      [
        "push",
        "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-frontend:latest",
      ]
images:
  - "us-central1-docker.pkg.dev/$PROJECT_ID/carbonsense-repo/carbonsense-frontend:latest"
```

(Change `us-central1` to your region if needed!)

## Step 6: Create Artifact Registry Repository

1. Go to **Artifact Registry > Repositories** (left sidebar!)
2. Click **"Create Repository"**
3. Name: `carbonsense-repo`
4. Format: **Docker**
5. Region: Same as before!
6. Click **"Create"**

## Step 7: Build & Deploy Backend

### Step 7a: Create Backend Build Trigger

1. Go to **Cloud Build > Triggers**
2. Click **"Create Trigger"**
3. Fill in:
   - Name: `build-backend`
   - Region: Same as before
   - Event: **Manual invocation**
   - Source: Your GitHub repo, `main` branch
   - Configuration: **Cloud Build config file** > Location: `backend/cloudbuild.yaml`
4. Click **"Create"**

### Step 7b: Run the Build!

1. In Triggers list, find `build-backend` > Click **"Run"**
2. Click **"Run Trigger"**
3. Wait ~3-5 mins for it to finish!

### Step 7c: Deploy Backend to Cloud Run!

1. Go to **Cloud Run** > "Create Service"
2. **Deploy one revision from existing container image**: Click **"Select"** > Artifact Registry > `carbonsense-repo` > `carbonsense-backend` > `latest`
3. Service name: `carbonsense-backend`
4. Region: Same as before!
5. Ingress: Allow all traffic
6. Authentication: Allow unauthenticated invocations
7. Expand **"Container, Networking, Security"**:
   - Container port: 8000
   - Environment variables: Click **Add variable** and add:
     - `DATABASE_URL`: `postgresql://carbonsense:YOUR_DB_PASSWORD@//cloudsql/YOUR_PROJECT_ID:YOUR_REGION:carbonsense-db/carbonsense`
     - `SECRET_KEY`: (long random string like `my-hackathon-secret-key-12345`)
     - `BACKEND_CORS_ORIGINS`: `https://YOUR_FRONTEND_URL.a.run.app,http://localhost:3000` (we'll update frontend part later!)
   - Cloud SQL connections: Click **Add Connection** > Select `carbonsense-db`
8. Click **"Create"**!
9. Copy your backend URL from the top! (e.g., `https://carbonsense-backend-abc123.a.run.app`)

## Step 8: Build & Deploy Frontend

### Step 8a: Add Frontend .env.production to Repo

Add this file to your repo: `frontend/.env.production`

```env
VITE_API_URL=https://your-backend-url.a.run.app
VITE_GOOGLE_MAPS_API_KEY=
VITE_GOOGLE_RECAPTCHA_SITE_KEY=
```

(Replace `your-backend-url` with your actual backend URL from step 7c!)

### Step 8b: Create Frontend Build Trigger & Run It

Same as step 7a/7b, but name it `build-frontend` and use `frontend/cloudbuild.yaml`!

### Step 8c: Deploy Frontend to Cloud Run

1. Go to Cloud Run > Create Service
2. Select frontend image from Artifact Registry
3. Service name: `carbonsense-frontend`
4. Region: Same as before
5. Ingress: Allow all, auth: Allow unauthenticated
6. Container port: 80
7. Click **"Create"**!
8. Copy your frontend URL!

## Step 9: Update Backend CORS!

1. Go to Cloud Run > Select `carbonsense-backend`
2. Click **"Edit & Deploy New Revision"**
3. Update `BACKEND_CORS_ORIGINS` to use your real frontend URL!
4. Click **"Deploy"**!

## Step 10: Test Your App!

1. Open your frontend URL!
2. Register a test user!
3. Explore CarbonSense AI!

## 🧹 Cleanup (After Hackathon!)

1. Delete Cloud Run services: Cloud Run > Select service > Delete
2. Delete Cloud SQL instance: SQL > Select > Delete
3. Delete Artifact Registry repo: Artifact Registry > Select > Delete
4. Delete Cloud Build triggers: Cloud Build > Triggers > Delete

## 🎉 Done!

You deployed CarbonSense AI to GCP using **only the web console**! No local tools needed!
