# 🗓️ lab13-sprint-full-stack-slop-llc

A **Python-based command-line tool** that allows users to manage personal tasks and automatically schedule them on their **Google Calendar**.  
Built using **Agile practices**, **GitHub Flow**, and with **full test coverage**.

---

## 🚀 Features

- ✅ Add a task (title, description, start time, end time)  
- 📋 View task list stored in memory  
- ☁️ Push task to Google Calendar via OAuth 2.0  
- 🔗 Returns event link on successful creation  

---

## 📦 Install from Test PyPI

> ✅ No need to clone the repository — this tool is deployed on Test PyPI and installable directly!

### 🛠️ Set Up Environment

```bash
python3 -m venv venv
```

### ▶️ Activate Environment

```bash
source venv/bin/activate
```

### 📦 Install Dependencies

While your virtual environment is still active (`(venv)` should be visible), run:

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ example-package-Higgs
```

Then resolve dependencies from the main by running:

```bash
python3 -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  example-package-Higgs
```
Finally, to run the program, just run:

```bash
calendar-app
```


---

## ⚙️ How to Run the Program From Source

From the root of the project:

```bash
cd calendar_app
```

### 🛠️ Set Up Environment

```bash
python3 -m venv venv
```

### ▶️ Activate Environment

```bash
source venv/bin/activate
```

### 📦 Install Dependencies

While your virtual environment is still active (`(venv)` should be visible), run all of these commands in one line:

```bash
pip install --break-system-packages google-auth-oauthlib
pip install --break-system-packages pytest-cov
pip install --break-system-packages google-api-python-client
```

> ✅ These are the three core dependencies for Google Calendar API access.

---

## ▶️ Run the Program (locally)

After installing dependencies, run the following command:

```bash
PYTHONPATH=src python3 -m calendar_app_package.main
```

> ⚠️ **Note:**  
> If you encounter a VS Code connection error after selecting your Google account and are unable to log in, simply reload and repeat the steps above.

---

## 🧪 Testing

Follow the setup steps above, **but instead of running the program**, run the following command to verify test coverage:

```bash
python3 -m pytest --cov=calendar_app_package
```

This will display **100% test coverage**.


Final look of readme was refined with chat gpt, but all steps and instructions were made by us