from app import create_app
server, app = create_app()
if __name__ == "__main__":
    server.run(debug=True)