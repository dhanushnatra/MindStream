import os

def create_if_uploads_folder_not_exists():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

if __name__ == '__main__':
    create_if_uploads_folder_not_exists()
    from server import app
    app.run(debug=True)