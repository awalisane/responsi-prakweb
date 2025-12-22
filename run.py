from app import create_app

# Membuat instance aplikasi Flask
app = create_app()

if __name__ == '__main__':
    # Menjalankan aplikasi dalam mode development
    # debug=True memungkinkan auto-reload saat ada perubahan kode
    app.run(debug=True, host='0.0.0.0', port=5000)