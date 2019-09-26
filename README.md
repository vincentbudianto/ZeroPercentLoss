# ZeroPercentLoss

Untuk dapat mengirim file, perlu dijalankan server.py di satu sistem dan
client.py di sistem yang lain. Pengirim file adalah client.py dan
penerima file adalah server.py

File yang ingin dikirim harus berada pada folder source.
File yang diterima oleh receiver akan berada pada folder destination.

Penggunaan :
   Command sisi receiver (server):
        python server.py

    Command sisi sender (client):
        python client.py [file_1] [file_2] [file_3] [file_4] [file_5]

    Maksimum file yang dapat dikirim sekaligus adalah 5
