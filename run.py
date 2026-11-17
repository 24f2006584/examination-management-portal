from app import create_app

app = create_app()

@app.route('/')
def home():
    return "Placement Portal is Running! The database has been initialized."

if __name__ == '__main__':
    app.run(debug=True)