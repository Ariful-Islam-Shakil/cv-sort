# 📄 CV SORTING


A Streamlit-based application to automatically extract, format, and manage CV data and sorting with there skills score based on strength and weakness using an AI-powered pipeline.

---

## ⚙️ Create Environment

```bash
python -m venv .cvs
```
## ▶️ Activate Environment
```bash
source .cvs/bin/activate
```
## 🌍 Set Environment Variable
```.env
GROQ_API_KEY=your_api_key_here
```
## 🚀 Run Streamlit Project
```bash
streamlit run app.py
```

## 🖥️ Using the App (UI Steps)

### 1. Run the Streamlit App
After starting Streamlit, open the URL shown in your terminal (usually `http://localhost:8502`).

---

### 2. Open the Sidebar Configuration Panel
In the left sidebar, choose one of the following options:

- **🔍 Run New Sorting** → to analyze a new folder of CVs  
- **📂 View Existing Results** → to view or download previously generated CSV files  

---

### 3. If Running a New Sorting
Fill in the following input fields:

- 📁 **Folder Path** — location of your CV files (e.g., `/Users/.../AI-Intern-9-Nov-2025`)  
- 🆔 **Job Description ID (JDI)** — unique ID for the job (e.g., `SE001`)  
- 🏢 **Department Name** — department the job belongs to (e.g., `Software_Engineering`)  
- 📄 **Output Version Tag** — version label for result file (e.g., `v2`)  
- 📝 **Job Description** — paste the full text of the job description  

---

### 4. Start the Analysis
Click **🚀 Start CV Sorting & Analysis** to begin processing.  
The app will:

1. Read all CVs from the provided folder  
2. Batch-process them through the LLM in one call per batch  
3. Extract structured candidate data  
4. Display the formatted results in a table  

---

### 5. View and Download Results
Once processing is complete:

- ✅ The analyzed CV data will be shown directly in the app  
- ⬇️ Use the **“Download Analyzed CSV”** button to save the results  

---

### 6. If Viewing Existing Results
- Select a file from the list of existing CSVs in `/results`  
- Click **📂 Load Selected CSV** to view it  
- Optionally download the file again using the **⬇️ Download This CSV** button  

# Dockerize
- Build docker
```bash
  docker build -t cv-sort . 
```
- Run Docker with `.env` file
```bash
docker run --env-file .env -p 8501:8501 cv-sort
```
- Server will be loaded at : [http://localhost:8501](http://localhost:8501)










##########################################################

# Dockerize

## 1. Build Docker Image
Build your Docker image from the project folder:

```bash
docker build -t cv-sort .
````

---

## 2. Run Docker Container with `.env` file

Run the container and map port 8501 to access Streamlit:

```bash
docker run --env-file .env -p 8501:8501 cv-sort
```

Open your browser at: [http://localhost:8501](http://localhost:8501)

---

## 3. Run Docker Container in Detached Mode (Background)

```bash
docker run -d --env-file .env -p 8501:8501 cv-sort
```

* `-d` runs container in background
* Use `docker ps` to see running containers

---

## 4. List Running Containers

```bash
docker ps
```

* Shows container ID, ports, and status

---

## 5. View Container Logs

```bash
docker logs <container_id>
```

* Replace `<container_id>` with the ID from `docker ps`
* Useful for debugging

---

## 6. Stop a Running Container

```bash
docker stop <container_id>
```

---

## 7. Remove a Container

```bash
docker rm <container_id>
```

* Optional, cleans up stopped containers

---

## 8. Remove Docker Image

```bash
docker rmi cv-sort
```

* Optional, removes the image from your system

---

## 9. Run Container with Volume Mount (Optional)

Mount a local folder inside container:

```bash
docker run --env-file .env -p 8501:8501 -v $(pwd)/data:/app/data cv-sort
```

* Useful if your app reads/writes files locally

---

## Notes

* Always use `localhost:8501` to access the app
* `.env` file should contain all required API keys and environment variables
* Rebuild the image after updating dependencies in `req-lock.txt`:

```bash
docker build -t cv-sort .
```
