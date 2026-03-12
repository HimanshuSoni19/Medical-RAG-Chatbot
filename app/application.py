from flask import Flask, render_template, request, session, redirect, url_for
from app.components.retriever import create_qa_chain
from dotenv import load_dotenv
from markupsafe import Markup
from app.common.logger import get_logger
import os

# Initialize logger for this file
logger = get_logger(__name__)

# Load environment variables
load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")

app = Flask(__name__)
# Secret key for session management
app.secret_key = os.urandom(24)

@app.template_filter('nl2br')
def nl2br(text):
    """Jinja2 filter to convert newlines to HTML line breaks."""
    if not text:
        return ""
    return Markup(text.replace("\n", "<br>\n"))

@app.route("/", methods=["GET", "POST"])
def index():
    logger.info(f"--- Index Route Accessed ({request.method}) ---")
    
    # 1. Initialize session message history if it doesn't exist
    if "messages" not in session:
        logger.info("Initializing new session messages list.")
        session["messages"] = []
    
    # 2. Handle POST Request (User sending a message)
    if request.method == "POST":
        user_input = request.form.get("prompt", "").strip()
        logger.info(f"User POST Input: {user_input[:50]}...")

        if user_input:
            # Update session messages with user query
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages
            
            try:
                logger.info("Generating AI response...")
                qa_chain = create_qa_chain()
                
                if qa_chain is None:
                    raise Exception("Internal Error: QA Chain failed to initialize.")

                # Invoke the chain
                response = qa_chain.invoke({"query": user_input})
                result = response.get("result", "I'm sorry, I couldn't process that.")

                # Update session messages with AI response
                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages
                logger.info("AI response saved to session.")

            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                logger.error(f"Chat Execution Error: {e}\nTraceback: {error_trace}")
                # Important: Return the template even on error so user sees the message
                return render_template("index.html", messages=session["messages"], error=str(e) or "An unknown error occurred.")
        
        # Always redirect after a successful POST to avoid "Form Resubmission" warnings on refresh
        logger.info("Redirecting after POST.")
        return redirect(url_for("index"))

    # 3. Handle GET Request (Opening the page)
    # This is the point where the server usually returns the initial page
    current_messages = session.get("messages", [])
    logger.info(f"GET Request successful. Rendering with {len(current_messages)} messages.")
    return render_template("index.html", messages=current_messages)

@app.route("/clear")
def clear():
    logger.info("Clearing chat history.")
    session.pop("messages", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # We use debug=True to get detailed error pages in the browser if something fails
    logger.info("Starting Medical Chatbot Server...")
    app.run(host="0.0.0.0", port=5000, debug=False)
