# 💼 The Challenge - Stark Bank

## 🗓️ Deadline

You have until **August 31th, midnight BRT**, seven days from now to deliver your answer.

## 🧪 Task

You will receive an invitation to join a **Sandbox account** in your email as an **Admin**.

Create a **Project** and **Webhook endpoint** for that account and develop a simple app integration using whichever language you prefer that:

1. Issues **8 to 12 Invoices every 3 hours** to random people for 24 hours (our Sandbox emulation environment will make sure some of those are automatically paid);
2. Receives the **webhook callback** of the Invoice credit and sends the received amount (minus eventual fees) to the following account using a **Transfer**:

```
bank code: 20018183
branch: 0001
account: 6341320293482496
name: Stark Bank S.A.
tax ID: 20.018.183/0001-80
account type: payment
```

## 🚀 Submission

When you finish your app:

1. Publish your code to a **public repository** (GitHub, GitLab, etc).
2. Send an email to:
   - 📧
   - 📧  
     with the repository **link** so we can take a look at your code.

You should receive a reply from us in **up to one week** with our evaluation and, if all goes well, an invite for a chat.

## 📝 Evaluation Criteria

You will be evaluated based on:

1. **How much have you learned** during the trial?
2. **How well does your code run?** Did you write unit tests? Are there hidden bugs?
3. **How much support did you need** from us to resolve technical issues? (Less is better!)
4. **Code readability and efficiency**.
5. **Speed of delivery**. Good code is better than fast code — but both is best!

## 🌟 Bonus Points

Earn extra credit if you:

- 🌐 **Deploy your application in the cloud** (Google Cloud, AWS, Azure - free tiers are available)
- 🔍 **Find issues** in our public code or API (e.g. bugs, security flaws)

## 💡 Tips

1. Visit our website to learn more and find helpful resources.
2. Use our official **SDKs and libraries** – they’re available in several languages.
3. Take advantage of tools like:
   - [Postman](https://www.postman.com/)
   - [webhook.site](https://webhook.site)
   - [ngrok](https://ngrok.com/)
   - ...or anything else that helps you!

## 🎉 That’s it!

**Have fun and good luck.**  
We hope to hear from you soon!

— **Stark Bank Developers and HR**

# Example of the body for a request to the webhook endpoint

```json
{
  "event": {
    "log": {
      "id": "59616010000002",
      "type": "invoice",
      "invoice": {
        "id": "inv_simulacao_17945",
        "amount": 17945,
        "name": "Cliente Teste",
        "taxId": "00000000000",
        "status": "paid",
        "created": "2024-06-10T14:00:00.000Z"
      }
    },
    "id": "59616010000001",
    "subscription": "invoice",
    "type": "credited",
    "isDelivered": false,
    "created": "2024-06-10T14:00:00.000Z"
  }
}
```

# How to run the example

```bash
# Clone the repository
git clone repo_url_here
# Go to the project directory
cd stark_challenge
# Create a virtual environment (optional but recommended) and activate it virtualenv venv
python -m venv venv && source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Create a .env file with your Stark Bank credentials
# Example .env file
# STARK_BANK_PROJECT_ID=your_project_id
# STARK_BANK_PRIVATE_KEY=your_private_key
# STARK_ENVIRONMENT=sandbox
# STARK_WEBHOOK_URL=http://API.localhost:8000/v2/webhook


# Run the FastAPI app
uvicorn app.main:app --reload
```
